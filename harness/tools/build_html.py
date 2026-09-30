"""HTML PDF engine (plan Task 9b.2; DEC-043): the same blocks as the DOCX, laid out by CSS and printed by headless Edge.

Usage: python harness/tools/build_html.py --project projects/<slug>   (dry run into a temporary folder)
`theme.build.pdf.engine: "html"` makes `run build` write build/<basename>.pdf with this engine; Word still writes
the DOCX. Every value comes from brief.json, theme.json and the theme's preset; the stylesheet is generated.

Up to four prints, merged with pypdf: the cover (no page number), the front (title page, contents, how-to-use; lower
roman), the body (parts, chapters, glossary; arabic from 1). The body is printed first: its outline (Edge's
--generate-pdf-document-outline) gives the page of every heading, which fills the contents. A front with headings of
its own is printed twice for the same reason. pypdf then writes the bookmarks and the metadata.
Exit 0 ok; 1 on a refused gate or a build error; 2 on a config error.
"""
import html, pathlib, re, subprocess, sys, tempfile

REPO = pathlib.Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))
from harness import figures, preflight  # noqa: E402
from harness.figures import annotated  # noqa: E402
from harness.tools import blocks, build_book, config, mathml  # noqa: E402

GRID, STRIPE, LINK = build_book.GRID, build_book.STRIPE, build_book.LINK
BuildError = build_book.BuildError
TIMEOUT_S = 300


def engine(cfg):
    return cfg["theme"]["build"]["pdf"].get("engine", "word_com")


def esc(s):
    return html.escape(s, quote=True)


def css_string(s):
    """A CSS string literal; `<` is escaped too, so a config string cannot close the <style> element (S9b-C01)."""
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ").replace("<", "\\3c ") + '"'


def hexc(v):
    return "#" + v.lstrip("#")


def contrast(a, b):
    """WCAG contrast ratio of two #rrggbb colours."""
    def lum(v):
        c = [int(v.lstrip("#")[i:i + 2], 16) / 255 for i in (0, 2, 4)]
        c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
        return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
    hi, lo = sorted((lum(a), lum(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def cover_accent(acc, pri):
    """The accent drawn on the primary-coloured cover, or a light tint when the accent is too dark to read there."""
    return acc if contrast(acc, pri) >= 3 else "#F3E6D8"


def darker(v, f=0.62):
    v = v.lstrip("#")
    return "#" + "".join(f"{round(int(v[i:i + 2], 16) * f):02x}" for i in (0, 2, 4))


# Edge keeps a page-margin box on one line with `nowrap` but ignores `width` and `text-overflow` there, so a long
# running head runs past the text block. The writer cuts it to a character budget instead; PDF-HEAD measures the result.
# ponytail: average advance per character in em, per head style; a font-metrics measure if a font breaks it
HEAD_EM = {"plain": 0.56, "caps": 0.72, "serif_italic": 0.47, "caps_wide": 0.8}
HEAD_PT = {"plain": 8, "caps": 6.5}


def clip(text, n):
    """`text` cut at a word boundary to at most `n` characters, ending in an ellipsis."""
    if len(text) <= n:
        return text
    cut = text[:max(n - 1, 1)]
    cut = (cut.rsplit(" ", 1)[0] if " " in cut else cut).rstrip(" ·,:;–—-")
    return cut + "…"


def fit_heads(left, right, budget):
    """(left, right) cut so that both fit on one line of `budget` characters; the right (the chapter) keeps more."""
    gap = 4
    if len(left) + len(right) + gap <= budget:
        return left, right
    right = clip(right, max(budget - len(left) - gap, int(budget * 0.6)))
    return clip(left, max(budget - len(right) - gap, 0)) if budget - len(right) - gap > 3 else "", right


# The design switches: theme value, else the preset's `design` default, else the built-in default (the plain look of
# a book whose preset has no `design`). key -> ((theme section, theme key), allowed values; the first is the default)
DESIGN = {"chapter_opener": (("layout", "chapter_opener"), ("inline", "page")),
          "toc_style": (("toc", "style"), ("leaders", "chapters")),
          "title_page": (("title_page", "layout"), ("preset", "centered")),
          "running_style": (("running", "style"), ("plain", "caps")),
          "page_number": (("running", "page_number"), ("center", "right"))}


def design(bk, key):
    (section, name), allowed = DESIGN[key]
    v = (bk.cfg["theme"].get(section) or {}).get(name)
    if v is None:
        v = (bk.preset.get("design") or {}).get(key, allowed[0])
    if v not in allowed:   # the theme schema checks the theme; the preset has no schema
        raise BuildError(f"preset {bk.preset['id']}: design.{key} is {v!r}, not one of {', '.join(allowed)}")
    return v


def two(n):
    return str(n).zfill(2) if str(n).isdigit() else str(n)


class Writer:
    """Blocks -> HTML. Mirrors build_book.Renderer.markdown: the same blocks, the same roles, the same labels."""

    def __init__(self, bk):
        self.bk = bk
        self.dropcap_pending = False

    def inline(self, text, links=True):
        if (self.bk.cfg["template"].get("math") or {}).get("enabled"):
            parts = mathml.split_inline(text)
            if any(is_math for is_math, _ in parts):
                return "".join(mathml.mathml(frag) if is_math else self._spans(frag, links)
                               for is_math, frag in parts)
        return self._spans(text, links)

    def _spans(self, text, links=True):
        out = []
        for sp in blocks.inline(text, links):
            t = esc(blocks.bind_dash(sp["text"]))
            if sp["sub"]:
                t = f"<sub>{t}</sub>"
            if sp["sup"]:
                t = f"<sup>{t}</sup>"
            if sp["italic"]:
                t = f"<em>{t}</em>"
            if sp["bold"]:
                t = f"<strong>{t}</strong>"
            if sp["url"]:
                t = f'<a href="{esc(sp["url"])}">{t}</a>'
            out.append(t)
        return "".join(out)

    def reference(self, text):
        m = re.search(r"DOI:\s*" + build_book.DOI.pattern, text)
        if not m:
            return self.inline(text)
        doi = m.group(1)
        return self.inline(text[: m.start(1)]) + f'<a href="https://doi.org/{esc(doi)}">{esc(doi)}</a>' + self.inline(text[m.end(1):])

    def image(self, src, fig, caption):
        from PIL import Image
        with Image.open(src) as im:
            w_px, h_px = im.size
        width = figures.placed_width_cm(w_px, h_px, self.bk.cfg["theme"]["layout"]["text_width"])
        alt = fig["alt"] if fig else caption
        out = [f'<figure><img src="{pathlib.Path(src).resolve().as_uri()}" alt="{esc(alt or "")}" style="width:{width}cm">']
        if fig is not None:
            out.append(f'<figcaption><span class="fignum">{esc(self.bk.fig_numbers[fig["id"]])}</span> '
                       f'{self.inline(fig["caption"])}</figcaption>')
            if fig["kind"] == annotated.KIND:   # the numbered key under the caption (Task 9b.4)
                out.append('<div class="figkey">' + "".join(f'<span class="badge">{n}</span>{self.inline(label)}'
                                                            for n, label in annotated.key(self.bk.cfg, fig)) + "</div>")
            out.append(f'<div class="credit">{esc(fig["credit"])} ({esc(fig["licence"])})</div>')
        elif caption:
            m = re.match(rf"({re.escape(self.bk.labels['figure'])} \d+\.\d+)\s*[—-]\s*(.+)", caption)
            out.append(f'<figcaption><span class="fignum">{esc(m.group(1))}</span> {self.inline(m.group(2))}</figcaption>'
                       if m else f"<figcaption>{self.inline(caption)}</figcaption>")
        return "".join(out) + "</figure>"

    def callout(self, key, text, paras=None):
        """`paras` keeps the author's paragraph breaks inside the box; `text` is the whole body for a split layout."""
        bk = self.bk
        label = bk.callout_by_id[key]["label"] if key else None
        layout = bk.style_of(key)[2]
        parts = bk.callout_by_id[key]["parts"] if key else []
        body = "".join(self._box_para(x) for x in (paras or [text]))
        if layout == "split" and parts:
            rx = r"\s+".join(rf"{re.escape(pt)}:\s*(.+?)" for pt in parts[:-1]) + rf"\s+{re.escape(parts[-1])}:\s*(.+)"
            m = re.match(rx, text)
            if m:
                body = "".join(f'<p><span class="part">{esc(pt)}</span> {self.inline(g)}</p>' for pt, g in zip(parts, m.groups()))
        head = f'<div class="label">{esc(label)}</div>' if label is not None else ""
        return f'<div class="box {self._cls(key)}">{head}{body}</div>'

    def _table(self, rows):
        n = len(rows[0])
        pad = lambda r: r + [""] * (n - len(r))
        head = "".join(f"<th>{self.inline(c)}</th>" for c in pad(rows[0]))
        body = "".join("<tr>" + "".join(f"<td>{self.inline(c)}</td>" for c in pad(r)[:n]) + "</tr>" for r in rows[1:])
        return f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>"

    def _box_para(self, text):
        """One paragraph inside a box; a paragraph that is only `$$...$$` is centred as a display equation, and a
        {"rows": ...} item is a table the author put inside the box."""
        if isinstance(text, dict):
            return self._table(text["rows"])
        tex = mathml.display(text) if (self.bk.cfg["template"].get("math") or {}).get("enabled") else None
        if tex is not None:
            return f'<p class="display-math">{mathml.mathml(tex, display=True)}</p>'
        return f"<p>{self.inline(text)}</p>"

    @staticmethod
    def _cls(key):
        return f"c-{key}" if key else "c-none"

    def render(self, text, kind, source):
        """-> (html, [(level, plain title)] of the headings it places, in order)."""
        bk, out, heads = self.bk, [], []
        state = {"box": False, "list": False, "role": None}
        resolved = {}

        def is_cover(link):
            resolved[link] = self.figure_file(source, link)
            return bool(bk.cover) and resolved[link].resolve() == bk.cover

        def close_list():
            if state["list"]:
                out.append("</ul>")
                state["list"] = False

        def close_box():
            close_list()
            if state["box"]:
                out.append("</div>")
                state["box"] = False

        for b in blocks.parse(text, bk.cfg, kind, is_cover):
            t = b["t"]
            if t != "bullet":
                close_list()
            if t == "para":
                tex = mathml.display(b["text"]) if (bk.cfg["template"].get("math") or {}).get("enabled") else None
                if tex is not None:
                    out.append(f'<p class="display-math">{mathml.mathml(tex, display=True)}</p>')
                    continue
                cls = "answer" if state["role"] == "answers" else ""
                if not state["box"] and self.dropcap_pending and state["role"] not in ("opening", "objectives"):
                    cls, self.dropcap_pending = "dropcap", False
                out.append(f'<p class="{cls}">{self.inline(b["text"])}</p>' if cls else f"<p>{self.inline(b['text'])}</p>")
            elif t == "section":
                close_box()
                state["role"] = b["role"]
                eyebrow = (bk.cfg["theme"].get("section_eyebrows") or {}).get(b["id"]) if b["id"] else None
                if eyebrow and not b["boxed"]:
                    out.append(f'<div class="eyebrow">{esc(eyebrow)}</div>')
                if b["boxed"]:
                    out.append(f'<div class="box {self._cls(b["id"])}"><div class="label">{esc(b["label"])}</div>')
                    state["box"] = True
                elif b["unlisted"]:
                    out.append(f'<div class="h2 unlisted">{esc(b["label"])}</div>')
                else:
                    out.append(f"<h2>{esc(b['label'])}</h2>")
                    heads.append((2, b["label"]))
            elif t == "h3":
                out.append(f"<h3>{self.inline(b['text'], links=False)}</h3>")
                heads.append((3, blocks.plain(b["text"])))
            elif t == "grid":
                items = "".join(f'<div class="cell"><div class="name">{esc(n)}</div><p>{self.inline(x)}</p></div>'
                                for n, x in b["items"])
                out.append(f'<div class="box grid {self._cls(b["key"])}"><div class="label">{esc(b["label"])}</div>'
                           f'<div class="cells">{items}</div></div>')
            elif t == "callout":
                out.append(self.callout(b["key"], b["text"], b.get("paras")))
            elif t == "table":
                out.append(self._table(b["rows"]))
            elif t == "image":
                fig = bk.manifest[b["link"][4:]] if b["link"].startswith("fig:") else None
                out.append(self.image(resolved[b["link"]], fig, None if fig else (b["caption"] or b["alt"])))
            elif t == "question":
                los = (f' <span class="lo">{esc(", ".join(bk.objective(x) for x in b["los"]))}</span>' if b["los"] else "")
                opts = "".join(f'<li><span class="opt">{esc(bk.option_display[label])}</span>{self.inline(body)}</li>'
                               for label, body in b["options"])
                out.append(f'<div class="question"><p class="stem"><span class="qnum">{esc(bk.question(b["num"]))}</span>'
                           f'{self.inline(b["stem"])}{los}</p><ol class="options">{opts}</ol></div>')
            elif t == "bullet":
                if not state["list"]:
                    out.append("<ul>")
                    state["list"] = True
                out.append(f"<li>{self.inline(b['text'])}</li>")
            elif t == "numbered":
                num, body = b["num"], b["body"]
                if state["role"] == "references":
                    out.append(f'<p class="reference"><span class="num">{esc(num)}.</span>{self.reference(body)}</p>')
                elif state["role"] == "objectives":
                    lo = build_book.LO_ITEM.match(body)
                    tag = bk.objective(lo.group(1)[2:]) if lo else num + "."
                    out.append(f'<p class="objective"><span class="num">{esc(tag)}</span>{self.inline(lo.group(2) if lo else body)}</p>')
                else:
                    out.append(f'<p class="numbered"><span class="num">{esc(num)}.</span>{self.inline(body)}</p>')
            elif t == "glossary":
                out.append(f'<p class="glossary-entry">{self.inline(b["text"])}</p>')
            elif t == "answer":
                key_m = re.fullmatch(r"Q(\d+)\. (\S+)", b["head"])
                head = (f"{bk.question(key_m.group(1))}. {bk.option_display.get(key_m.group(2), key_m.group(2))}"
                        if key_m else b["head"])
                out.append(f'<p class="answer"><strong>{esc(head)}</strong> {self.inline(b["text"])}</p>')
        close_box()
        return "".join(out), heads

    figure_file = build_book.Renderer.figure_file   # it reads only self.bk


# ---------- stylesheet ----------

def font_faces(cfg):
    out = []
    weights = {"regular": ("400", "normal"), "bold": ("700", "normal"), "italic": ("400", "italic"),
               "bold_italic": ("700", "italic")}
    for family, files in (cfg["theme"].get("font_files") or {}).items():
        for k, rel in files.items():
            w, s = weights[k]
            out.append(f"@font-face{{font-family:{css_string(family)};src:url({css_string((cfg['project'] / rel).resolve().as_uri())});"
                       f"font-weight:{w};font-style:{s}}}")
    return "".join(out)


def stylesheet(bk, chapters):
    th, pg = bk.cfg["theme"], bk.preset["page"]
    m = th["page"]["margins"]
    # a glyph missing from a display or UI font falls back to the body serif, never to the browser default
    ff = lambda k: css_string(bk.fonts[k]) + ("" if k == "serif" else "," + css_string(bk.fonts["serif"]))
    ink, pri, acc, mut = hexc(bk.ink), hexc(bk.primary), hexc(bk.accent), hexc(bk.muted)
    cacc = cover_accent(acc, pri)
    align = {"left": "left", "justify": "justify", "right": "right", "center": "center"}
    body_align, head_align = align[th["alignment"]["body"]], align[th["alignment"]["headings"]]
    run = th.get("running") or {}
    style, num_at = design(bk, "running_style"), design(bk, "page_number")
    if num_at == "center" and run.get("footer_center"):
        raise BuildError("theme.running: footer_center needs page_number 'right' (the centre holds the page number)")
    size = HEAD_PT[style]
    width_pt = (pg["width_cm"] - m["left"] - m["right"]) * 72 / 2.54
    chars = lambda pt, em, share=1.0: int(width_pt * share / (pt * HEAD_EM[em]))
    budget = chars(size, style)
    caps = ";text-transform:uppercase;letter-spacing:0.06em" if style == "caps" else ""
    head_box = (f"font-family:{ff('sans')};font-size:{size}pt;color:{mut};vertical-align:bottom;white-space:nowrap;"
                f"padding-bottom:0.25cm;border-bottom:0.5pt solid #{GRID}{caps}")
    right_box = f"font-weight:700;color:{acc if style == 'caps' else mut}"
    left_text = run.get("head_left") or bk.title

    def heads(right):
        left, right = fit_heads(left_text, right, budget)
        return (f"@top-left{{content:{css_string(left)};{head_box}}}"
                f"@top-right{{content:{css_string(right)};{head_box};{right_box}}}")

    def foot(counter):
        num = (f"content:{counter};font-family:{ff('serif_heading')};font-size:10pt;font-weight:700;color:{pri}"
               if num_at == "right" else f"content:{counter};font-family:{ff('sans')};font-size:8.5pt;color:{mut}")
        out = f"@bottom-{num_at}{{{num}}}"
        if run.get("footer_left"):
            out += (f"@bottom-left{{content:{css_string(clip(run['footer_left'], chars(8.5, 'serif_italic', 0.4)))};white-space:nowrap;"
                    f"font-family:{ff('serif')};font-style:italic;font-size:8.5pt;color:{mut}}}")
        if run.get("footer_center"):
            out += (f"@bottom-center{{content:{css_string(clip(run['footer_center'], chars(7, 'caps_wide', 0.34)))};white-space:nowrap;"
                    f"font-family:{ff('sans')};font-size:7pt;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:{acc}}}")
        return out
    none = "".join(f"@{box}{{content:none;border:0}}" for box in ("top-left", "top-right", "bottom-left", "bottom-center", "bottom-right"))
    pages = [
        f"@page{{size:{pg['width_cm']}cm {pg['height_cm']}cm;margin:{m['top']}cm {m['right']}cm {m['bottom']}cm {m['left']}cm;"
        f"background:{hexc(bk.pal.get('paper') or 'FFFFFF')};{heads('')}{foot('counter(page)')}}}",
        f"@page plain{{{none}}}",
        f"@page cover{{margin:0;{none}}}",
        f"@page how{{{heads(bk.role.get('how_to_use') or '')}{foot('counter(page,lower-roman)')}}}",
        f"@page gloss{{{heads(bk.labels['glossary'])}}}",
    ]
    for n, title_n in chapters:
        pages.append(f"@page ch{n}{{{heads(bk.labels['chapter'] + ' ' + str(n) + ' · ' + blocks.plain(title_n))}}}")
    boxes = []
    for key, e in th["callouts"].items():
        border = e.get("border")
        edge = (f"border:{border['size_eighths_pt'] / 8}pt solid {hexc(border['colour'])}" if border
                else f"border-top:0;border-left:3pt solid {hexc(e['label_colour'])}" if e.get("edge") == "left"
                else f"border-top:1.5pt solid {hexc(e['label_colour'])}")
        boxes.append(f".c-{key}{{background:{hexc(e['fill'])};{edge}}}.c-{key} .label,.c-{key} .part,.c-{key} .name"
                     f"{{color:{hexc(e['label_colour'])}}}")
    drop = (f".dropcap::first-letter{{float:left;font-family:{ff('serif_heading')};font-size:3.4em;line-height:0.86;"
            f"padding:0.06em 0.08em 0 0;color:{pri};font-weight:700}}") if th["layout"].get("drop_cap") else ""
    paper = hexc(bk.pal.get("paper") or "FFFFFF")   # page background, margins included (theme.palette.paper; also on @page)
    return "".join(pages) + font_faces(bk.cfg) + f"""
*{{box-sizing:border-box;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
html{{font-family:{ff('serif')};font-size:10.5pt;color:{ink};line-height:1.42;background:{paper}}}
body{{margin:0}}
p{{margin:0 0 6pt;text-align:{body_align};orphans:2;widows:2;hyphens:auto}}
a{{color:#{LINK};text-decoration:none}}
sub,sup{{font-size:0.72em;line-height:0}}
h1,h2,h3,.h2,.label,.qnum,.stem,figcaption,th,td,.toc,.part-page{{text-align:{head_align}}}
h1{{font-family:{ff('serif_heading')};font-size:25pt;font-weight:700;color:{pri};line-height:1.08;margin:1.6cm 0 0.75cm;
  padding-bottom:0.3cm;border-bottom:1.5pt solid {acc};break-after:avoid}}
h1 .num{{color:{acc};margin-right:0.15em}}
h2,.h2{{font-family:{ff(th['layout'].get('heading2_font') or 'sans')};font-size:{13.5 if th['layout'].get('heading2_font') == 'serif_heading' else 12.5}pt;font-weight:700;color:{pri};margin:16pt 0 5pt;break-after:avoid}}
h3{{font-family:{ff('sans')};font-size:11pt;font-weight:700;color:{ink};margin:10pt 0 3pt;break-after:avoid}}
ul{{margin:0 0 6pt;padding-left:0.6cm}}li{{margin-bottom:3pt}}
.box{{background:#F1F1EE;border-top:1.5pt solid {pri};padding:0.3cm 0.34cm;margin:8pt 0 10pt;break-inside:avoid;border-radius:1.5pt}}
.box .label{{font-family:{ff('sans')};font-size:8.5pt;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;color:{pri};margin-bottom:3pt}}
.box p{{font-size:9.8pt;margin-bottom:4pt}}.box p:last-child{{margin-bottom:0}}
.box .part{{font-weight:700;margin-right:0.4em}}
.grid .cells{{display:grid;grid-template-columns:1fr 1fr;gap:0.3cm}}
.grid .name{{font-weight:700;font-size:9.8pt}}
{''.join(boxes)}
table{{width:100%;border-collapse:collapse;margin:8pt 0 10pt;font-family:{ff('sans')};font-size:8.8pt;line-height:1.25;
  border-top:1pt solid {pri};border-bottom:1pt solid {pri}}}
thead{{display:table-header-group}}tr{{break-inside:avoid}}
th{{background:{pri};color:#fff;font-weight:700;padding:0.15cm}}
td{{padding:0.15cm;border-top:0.5pt solid #{GRID};vertical-align:top}}
tbody tr:nth-child(even) td{{background:#{STRIPE}}}
figure{{margin:8pt 0 12pt;text-align:center;break-inside:avoid}}
figure img{{display:block;margin:0 auto 4pt}}
figcaption{{font-family:{ff('sans')};font-size:8.5pt;color:{mut}}}
.fignum{{font-weight:700;color:{pri};margin-right:0.4em}}
.credit{{font-family:{ff('sans')};font-size:8pt;color:{mut};text-align:{head_align}}}
.figkey{{font-family:{ff('sans')};font-size:8.5pt;color:{ink};text-align:{head_align};margin-top:2pt}}
.figkey .badge{{display:inline-block;min-width:1.35em;height:1.35em;line-height:1.35em;border-radius:50%;background:{pri};
  color:#fff;font-weight:700;text-align:center;font-size:0.85em;margin:0 0.3em 0 0.8em}}
.figkey .badge:first-child{{margin-left:0}}
.question{{break-inside:avoid;margin:8pt 0 6pt}}
.stem{{margin-bottom:3pt}}.qnum{{font-weight:700;color:{pri};margin-right:0.5em}}
.lo{{font-family:{ff('sans')};font-size:8pt;color:{mut}}}
.options{{list-style:none;margin:0;padding:0}}
.options li{{font-size:10pt;padding-left:{th['lists']['indent']}cm;text-indent:-{th['lists']['hanging']}cm;margin-bottom:1pt}}
.opt{{display:inline-block;width:{th['lists']['hanging']}cm;text-indent:0;font-weight:700;color:{pri}}}
.answer{{font-size:9.8pt}}.answer strong{{color:{pri}}}
p.display-math{{text-align:center;margin:8pt 0}}
math{{font-size:1.02em}}
.reference{{font-size:8.8pt;padding-left:0.8cm;text-indent:-0.8cm;margin-bottom:3pt;text-align:{head_align}}}
.reference .num{{display:inline-block;width:0.8cm;text-indent:0;color:{mut}}}
.objective,.numbered{{padding-left:1.1cm;text-indent:-1.1cm;text-align:left}}
.numbered{{padding-left:0.7cm;text-indent:-0.7cm}}
.objective .num{{display:inline-block;width:1.1cm;text-indent:0;font-family:{ff('sans')};font-size:8.5pt;font-weight:700;color:{acc}}}
.numbered .num{{display:inline-block;width:0.7cm;text-indent:0;font-weight:700;color:{pri}}}
.glossary-entries{{column-count:2;column-gap:0.8cm}}
.glossary-entry{{font-size:9.3pt;margin-bottom:4pt;break-inside:avoid;text-align:{head_align}}}
.chapter{{break-before:page}}.chapter:first-child{{break-before:auto}}
.part-page{{page:plain;break-before:page;break-after:page;padding-top:6cm}}
.part-page h1{{margin-top:0}}.part-page .span{{font-family:{ff('sans')};font-size:9.5pt;color:{mut};margin-bottom:14pt}}
.part-page .entry{{font-family:{ff('serif_heading')};font-size:13pt;margin-bottom:4pt}}
.part-page .entry .k{{display:inline-block;width:1cm;font-weight:700;color:{acc}}}
.gloss{{page:gloss;break-before:page}}
.how{{page:how}}
.titlepage{{page:plain;break-after:page}}
.titlepage .tp{{margin:0}}
.notices{{page:plain;break-before:page;break-after:page}}
.toc{{page:plain}}
.toc-title{{font-family:{ff('serif_heading')};font-size:25pt;font-weight:700;color:{pri};margin:1.6cm 0 0.75cm;
  padding-bottom:0.3cm;border-bottom:1.5pt solid {acc}}}
.toc-entry{{display:flex;align-items:baseline;gap:0.3em}}
.toc-entry .t{{flex:0 1 auto}}.toc-entry .dots{{flex:1 1 auto;border-bottom:0.6pt dotted {mut};margin:0 0.2em;transform:translateY(-0.25em)}}
.toc-entry .pg{{flex:0 0 auto;min-width:1.6em;text-align:right}}
.toc-1{{font-family:{ff('sans')};font-size:10.5pt;font-weight:700;color:{pri};margin-top:8pt}}
.toc-2{{font-size:10pt;margin-left:1cm;margin-top:1pt}}
{drop}
.cover{{page:cover;position:relative;width:{pg['width_cm']}cm;height:calc({pg['height_cm']}cm - 1px);overflow:hidden;color:#fff;
  background:linear-gradient(160deg,{pri} 0%,{darker(bk.primary)} 100%)}}
.cover img.full{{width:100%;height:100%;object-fit:cover;display:block}}
.cover .frame{{position:absolute;inset:0.8cm;border:0.6pt solid {cacc};opacity:0.55}}
.cover .top{{position:absolute;top:1.6cm;left:1.8cm;right:1.8cm;display:flex;align-items:center;gap:0.45cm;
  padding-bottom:0.5cm;border-bottom:0.6pt solid {cacc}}}
.cover .top img{{height:1.9cm;width:auto;background:#fff;border-radius:50%;padding:0.08cm}}
.cover .inst{{flex:1;font-family:{ff('sans')};font-size:10pt;font-weight:700;letter-spacing:0.08em;text-transform:uppercase}}
.cover .mid{{position:absolute;top:35%;left:1.8cm;right:1.8cm;text-align:center}}
.cover .eyebrow{{display:inline-block;font-family:{ff('sans')};font-size:8pt;font-weight:700;letter-spacing:0.16em;
  text-transform:uppercase;color:{cacc};border:0.8pt solid {cacc};border-radius:1cm;padding:0.14cm 0.5cm;margin-bottom:0.7cm}}
.cover .title{{font-family:{ff('serif_heading')};font-size:34pt;font-weight:700;line-height:1.1}}
.cover .subtitle{{font-family:{ff('serif_heading')};font-style:italic;font-size:14pt;color:{cacc};margin-top:0.35cm}}
.cover .rule{{width:3.2cm;height:1.6pt;background:{cacc};margin:0.8cm auto 0}}
.cover .bottom{{position:absolute;bottom:1.8cm;left:1.8cm;right:1.8cm;padding-top:0.5cm;border-top:0.6pt solid {cacc};
  display:flex;justify-content:space-between;align-items:flex-end;gap:1cm}}
.cover .credits{{font-family:{ff('serif_heading')};font-size:14pt;font-weight:700}}
.cover .meta{{font-family:{ff('sans')};font-size:8.5pt;text-align:right;opacity:0.85}}
.eyebrow{{font-family:{ff('sans')};font-size:7.5pt;font-weight:700;letter-spacing:0.14em;text-transform:uppercase;color:{acc};
  margin:18pt 0 0;break-after:avoid;text-align:{head_align}}}
.eyebrow+h2,.eyebrow+.h2{{margin-top:2pt}}
.bleed{{position:relative;width:{pg['width_cm']}cm;height:calc({pg['height_cm']}cm - 1px);overflow:hidden;color:#fff;
  background:linear-gradient(160deg,{pri} 0%,{darker(bk.primary)} 100%)}}
.bleed .frame{{position:absolute;inset:0.8cm;border:0.6pt solid {acc};opacity:0.55}}
.opener{{page:cover;break-after:page}}
.opener .mid{{position:absolute;top:27%;left:2.2cm;right:2.2cm}}
.opener .kicker{{font-family:{ff('sans')};font-size:8.5pt;font-weight:700;letter-spacing:0.22em;text-transform:uppercase;color:{acc}}}
.opener .partline{{font-family:{ff('sans')};font-size:8pt;letter-spacing:0.1em;text-transform:uppercase;opacity:0.8;margin-bottom:0.5cm}}
.opener h1{{color:#fff;border:0;padding:0;margin:0.15cm 0 0;font-size:31pt;line-height:1.1;text-align:left}}
.opener h1 .num{{display:block;font-size:64pt;line-height:1;color:{acc};margin:0 0 0.25cm}}
.opener .rule{{width:3.2cm;height:1.6pt;background:{acc};margin-top:0.8cm}}
.opener .inchap{{position:absolute;left:2.2cm;right:2.2cm;bottom:2.2cm;border-top:0.6pt solid {acc};padding-top:0.4cm}}
.opener .inchap .lbl{{font-family:{ff('sans')};font-size:7.5pt;font-weight:700;letter-spacing:0.16em;text-transform:uppercase;
  color:{acc};margin-bottom:0.25cm}}
.opener .inchap ol{{list-style:none;margin:0;padding:0;columns:2;column-gap:0.8cm;font-family:{ff('sans')};font-size:8.5pt;
  line-height:1.35;opacity:0.9}}
.opener .inchap li{{break-inside:avoid;margin-bottom:3pt}}
.part-page.bleed{{page:cover;padding:7cm 2.2cm 0;break-before:page;break-after:page}}
.part-page.bleed h1{{color:#fff;border-bottom-color:{acc}}}.part-page.bleed .span{{color:{acc}}}
.part-page.bleed .entry{{color:#fff}}
.tc-part{{font-family:{ff('sans')};font-size:8pt;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:{acc};
  margin:14pt 0 2pt;padding-bottom:3pt;border-bottom:0.8pt solid {acc};break-after:avoid}}
.tc-row{{display:grid;grid-template-columns:2.2cm 1fr 1.3cm;column-gap:0.3cm;padding:6pt 0;border-bottom:0.5pt solid #{GRID};
  break-inside:avoid}}
.tc-k{{font-family:{ff('sans')};font-size:7.5pt;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:{acc};padding-top:3pt}}
.tc-t{{font-family:{ff('serif_heading')};font-size:11.5pt;font-weight:700;color:{pri};line-height:1.2}}
.tc-sub{{font-family:{ff('sans')};font-size:7.5pt;color:{mut};line-height:1.4;margin-top:2pt;display:-webkit-box;
  -webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}}
.tc-pg{{font-family:{ff('serif_heading')};font-size:11pt;font-weight:700;color:{pri};text-align:right}}
.titlepage.centered{{display:flex;flex-direction:column;align-items:center;text-align:center;
  height:calc({pg['height_cm'] - m['top'] - m['bottom']}cm - 2px);padding-top:1.2cm}}
.centered .logos img{{height:1.8cm;width:auto;margin:0 0.2cm}}
.centered .inst{{font-family:{ff('sans')};font-size:8.5pt;font-weight:700;letter-spacing:0.14em;text-transform:uppercase;color:{pri};
  margin-top:0.35cm}}
.centered .tp-title{{font-family:{ff('serif_heading')};font-size:28pt;font-weight:700;color:{pri};line-height:1.12;margin-top:1.6cm}}
.centered .tp-sub{{font-family:{ff('serif_heading')};font-style:italic;font-size:13pt;color:{mut};margin-top:0.35cm}}
.centered .pill{{font-family:{ff('sans')};font-size:7.5pt;font-weight:700;letter-spacing:0.14em;text-transform:uppercase;color:{pri};
  border:0.8pt solid {acc};border-radius:1cm;padding:0.12cm 0.45cm;margin-top:0.6cm}}
.centered .tp-rule{{width:3cm;height:1.4pt;background:{acc};margin:0.8cm 0}}
.centered .tp-author{{font-family:{ff('serif_heading')};font-size:12pt;font-weight:700;color:{ink};margin-bottom:3pt}}
.centered .tp-aud{{font-family:{ff('sans')};font-size:8.5pt;color:{mut};margin-top:0.3cm}}
.centered .tp-notices{{margin-top:auto;font-family:{ff('sans')};font-size:7.8pt;color:{mut};max-width:12cm}}
.centered .tp-notices p{{text-align:center;margin-bottom:3pt}}
.ending .mid{{position:absolute;top:38%;left:2.8cm;right:2.8cm;text-align:center}}
.ending .logos{{position:absolute;top:2.2cm;left:0;right:0;text-align:center}}
.ending .logos img{{height:1.9cm;width:auto;background:#fff;border-radius:50%;padding:0.08cm;margin:0 0.2cm}}
.ending .mark{{font-family:{ff('serif_heading')};font-size:54pt;line-height:0.6;color:{acc}}}
.ending .quote{{font-family:{ff('serif_heading')};font-style:italic;font-size:15pt;line-height:1.45;margin-top:0.5cm}}
.ending .who{{font-family:{ff('sans')};font-size:8pt;font-weight:700;letter-spacing:0.16em;text-transform:uppercase;color:{acc};margin-top:0.6cm}}
.ending .foot{{position:absolute;bottom:1.8cm;left:0;right:0;text-align:center;font-family:{ff('sans')};font-size:8pt;opacity:0.8}}
"""


# ---------- document parts ----------

def page_html(bk, css, body):
    lang = esc(bk.cfg["theme"]["lang_tag"])
    return (f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><title>{esc(bk.title)}</title>'
            f"<style>{css}</style></head><body>{body}</body></html>")


def cover_html(bk):
    th, b = bk.cfg["theme"], bk.cfg["brief"]["identity"]
    if bk.cover:
        return f'<section class="cover"><img class="full" src="{bk.cover.as_uri()}" alt=""></section>'
    design = th["cover"].get("design")
    if not design:
        return None
    logos = "".join(f'<img src="{(bk.cfg["project"] / p).resolve().as_uri()}" alt="">' for p in design.get("logos", []))
    inst = f'<div class="inst">{esc(design["institution"])}</div>' if design.get("institution") else '<div class="inst"></div>'
    top = f'<div class="top">{logos}{inst}</div>' if (logos or design.get("institution")) else ""
    eyebrow = f'<div class="eyebrow">{esc(design["eyebrow"])}</div>' if design.get("eyebrow") else ""
    sub = f'<div class="subtitle">{esc(bk.subtitle)}</div>' if bk.subtitle else ""
    meta = "<br>".join(esc(x) for x in (bk.audience, b.get("edition")) if x)
    return (f'<section class="cover"><div class="frame"></div>{top}<div class="mid">{eyebrow}<div class="title">'
            f'{esc(bk.title)}</div>{sub}<div class="rule"></div></div><div class="bottom"><div class="credits">'
            f'{esc(bk.credits)}</div><div class="meta">{meta}</div></div></section>')


def logos_html(bk):
    design = bk.cfg["theme"]["cover"].get("design") or {}
    return "".join(f'<img src="{(bk.cfg["project"] / p).resolve().as_uri()}" alt="">' for p in design.get("logos", []))


def title_page_centered(bk):
    """theme.title_page.layout 'centered': logos, institution, title, subtitle, edition, authors, audience, and the
    notices at the foot of the same page (no page of its own)."""
    th, ident = bk.cfg["theme"], bk.cfg["brief"]["identity"]
    inst = (th["cover"].get("design") or {}).get("institution")
    logos = logos_html(bk)
    out = [f'<div class="logos">{logos}</div>' if logos else "", f'<div class="inst">{esc(inst)}</div>' if inst else "",
           f'<div class="tp-title">{esc(bk.title)}</div>', f'<div class="tp-sub">{esc(bk.subtitle)}</div>' if bk.subtitle else "",
           f'<div class="pill">{esc(ident["edition"])}</div>' if ident.get("edition") else "", '<div class="tp-rule"></div>']
    out += [f'<div class="tp-author">{esc(a["credit_line"])}</div>' for a in ident["authors"]]
    out.append(f'<div class="tp-aud">{esc(bk.audience)}</div>' if bk.audience else "")
    notices = th["title_page"]["notices"]
    if notices:
        out.append('<div class="tp-notices">' + "".join(f"<p>{esc(n)}</p>" for n in notices) + "</div>")
    return f'<section class="titlepage centered">{"".join(out)}</section>'


def ending_html(bk):
    """theme.ending: a full-bleed closing page (logos, quotation, attribution); None without it."""
    e = bk.cfg["theme"].get("ending")
    if not e:
        return None
    logos = logos_html(bk)
    who = f'<div class="who">{esc(e["attribution"])}</div>' if e.get("attribution") else ""
    return (f'<section class="cover bleed ending"><div class="frame"></div>'
            + (f'<div class="logos">{logos}</div>' if logos else "")
            + f'<div class="mid"><div class="mark">“</div><div class="quote">{esc(e["quote"])}</div>{who}</div>'
            f'<div class="foot">{esc(bk.title)}</div></section>')


def title_page_html(bk):
    if design(bk, "title_page") == "centered":
        return title_page_centered(bk)
    values ={"title": bk.title, "subtitle": bk.subtitle, "credits": bk.credits, "audience_line": bk.audience}
    notices = bk.cfg["theme"]["title_page"]["notices"]
    main, extra = [], ""
    for spec in bk.preset["title_page_layout"]:
        style = (f"font-family:{css_string(bk.fonts[spec['font']])};font-size:{spec['size_pt']}pt;"
                 f"font-weight:{700 if spec.get('bold') else 400};font-style:{'italic' if spec.get('italic') else 'normal'};"
                 f"color:{hexc(bk.pal[spec['colour']]) if spec.get('colour') else 'inherit'};text-align:left")
        if spec["field"] == "notices":
            if notices:
                extra = ('<section class="notices">' + "".join(
                    f'<p class="tp" style="{esc(style)};margin-bottom:{spec["space_after_pt"]}pt">{esc(n)}</p>' for n in notices)
                    + "</section>")
            continue
        text = values[spec["field"]]
        if not text:
            continue
        rule = spec.get("rule_below")
        deco = (f";padding-bottom:{rule['space_pt']}pt;border-bottom:{rule['size_eighths_pt'] / 8}pt solid {hexc(rule['colour'])}"
                if rule else "")
        main.append(f'<p class="tp" style="{esc(style)};margin-top:{spec.get("space_before_pt", 0)}pt{esc(deco)}">{esc(text)}</p>')
    return f'<section class="titlepage">{"".join(main)}</section>{extra}'


def toc_html(bk, heads, kinds, pages):
    """heads: every placed heading [(level, title)]; kinds: the same length, ('part', label, title),
    ('chapter', n, title) or ('other',); pages: the same length, a page label or '' (the probe print).
    theme.toc.style 'leaders' (default): one dotted row per heading down to theme.toc.levels. 'chapters': one row per
    level-1 heading (the chapter label, its title, its level-2 headings as one muted line, the page); parts as bands."""
    title = f'<div class="toc-title">{esc(bk.labels["contents"])}</div>'
    if design(bk, "toc_style") == "leaders":
        levels = bk.cfg["theme"]["toc"]["levels"]
        rows = "".join(f'<div class="toc-entry toc-{lvl}"><span class="t">{esc(t)}</span><span class="dots"></span>'
                       f'<span class="pg">{esc(p)}</span></div>' for (lvl, t), p in zip(heads, pages) if lvl <= levels)
        return f'<section class="toc">{title}{rows}</section>'
    rows = []
    for i, ((lvl, t), kind, p) in enumerate(zip(heads, kinds, pages)):
        if lvl != 1:
            continue
        if kind[0] == "part":
            rows.append(f'<div class="tc-part">{esc(kind[1])} · {esc(kind[2])}</div>')
            continue
        subs = []
        for lvl2, t2 in heads[i + 1:]:
            if lvl2 == 1:
                break
            if lvl2 == 2:
                subs.append(t2)
        k, name = (f"{bk.labels['chapter']} {two(kind[1])}", blocks.plain(kind[2])) if kind[0] == "chapter" else ("", t)
        sub = f'<div class="tc-sub">{esc(" · ".join(subs))}</div>' if subs else ""
        rows.append(f'<div class="tc-row"><div class="tc-k">{esc(k)}</div><div><div class="tc-t">{esc(name)}</div>{sub}</div>'
                    f'<div class="tc-pg">{esc(p)}</div></div>')
    return f'<section class="toc">{title}{"".join(rows)}</section>'


def opener_html(bk, n, title_html, part, h2s):
    """theme.layout.chapter_opener 'page': a full-bleed page that holds the chapter's h1 (the outline and the contents
    point at it), the part it belongs to, and its level-2 headings when theme.labels.in_this_chapter is set."""
    partline = f'<div class="partline">{esc(part["label"])} · {esc(part["title"])}</div>' if part else ""
    lbl = bk.labels.get("in_this_chapter")
    inchap = (f'<div class="inchap"><div class="lbl">{esc(lbl)}</div><ol>' + "".join(f"<li>{esc(t)}</li>" for t in h2s)
              + "</ol></div>") if lbl and h2s else ""
    return (f'<div class="bleed opener"><div class="frame"></div><div class="mid">{partline}'
            f'<div class="kicker">{esc(bk.labels["chapter"])}</div><h1><span class="num">{esc(str(n))}</span> '
            f'{title_html}</h1><div class="rule"></div></div>{inchap}</div>')


def body_parts(cfg, bk, w):
    """-> (front how-to-use html or '', its heads, body html, body heads [(level, title)], [(n, title)], body kinds).
    Kinds run with the body heads: ('part', label, title), ('chapter', n, title) or ('other',) (see toc_html)."""
    opener = design(bk, "chapter_opener") == "page"
    how_html, how_heads = "", []
    front_file = cfg.book_file("front_matter")
    how = bk.role.get("how_to_use")
    if front_file is not None and how:
        front = front_file.read_text(encoding="utf-8")
        marker = f"\n## {how}"
        if marker in front:
            inner, heads = w.render(front.split(marker, 1)[1], "chapter", front_file)
            how_html = f'<section class="how"><h1>{esc(how)}</h1>{inner}</section>'
            how_heads = [(1, how)] + heads
    chapters = []
    for c, path in cfg.chapters():
        text = path.read_text(encoding="utf-8")
        chapters.append((c, path, text, *build_book.chapter_heading(text, cfg)))
    parts = {p["id"]: p for p in cfg["chapter_plan"].get("parts", [])}
    members = {}
    for c, _, _, n, _ in chapters:
        if c.get("part_id"):
            members.setdefault(c["part_id"], []).append(n)
    if parts and "chapters" not in bk.labels:
        raise BuildError("theme.labels.chapters is required when chapter-plan.json has parts")
    out, heads, kinds, current = [], [], [], None
    for c, path, text, n, title in chapters:
        pid = c.get("part_id")
        part = parts[pid] if pid else None
        if pid and pid != current:
            current = pid
            span = members[pid]
            label = (f"{bk.labels['chapters']} {span[0]}–{span[-1]}" if len(span) > 1 else f"{bk.labels['chapter']} {span[0]}")
            entries = "".join(f'<div class="entry"><span class="k">{k}</span>{esc(blocks.plain(t2))}</div>'
                              for c2, _, _, k, t2 in chapters if c2.get("part_id") == pid)
            out.append(f'<section class="part-page{" bleed" if opener else ""}">'
                       + ('<div class="frame"></div>' if opener else "")
                       + f'<h1><span class="num">{esc(part["label"])}</span> {esc(part["title"])}</h1>'
                       f'<div class="span">{esc(label)}</div>{entries}</section>')
            heads.append((1, f"{part['label']} {part['title']}"))
            kinds.append(("part", part["label"], part["title"]))
        w.dropcap_pending = True
        inner, h = w.render(text, "chapter", path)
        h1 = (opener_html(bk, n, w.inline(title, links=False), part, [t for lvl, t in h if lvl == 2]) if opener
              else f'<h1><span class="num">{n}</span> {w.inline(title, links=False)}</h1>')
        out.append(f'<section class="chapter" style="page:ch{n}">{h1}{inner}</section>')
        heads += [(1, f"{n} {blocks.plain(title)}")] + h
        kinds += [("chapter", n, title)] + [("other",)] * len(h)
    glossary = cfg.book_file("glossary") if cfg["template"]["glossary"]["enabled"] else None
    if glossary is not None:
        inner, _ = w.render(glossary.read_text(encoding="utf-8"), "glossary", glossary)
        out.append(f'<section class="gloss"><h1>{esc(bk.labels["glossary"])}</h1><div class="glossary-entries">{inner}</div></section>')
        heads.append((1, bk.labels["glossary"]))
        kinds.append(("other",))
    return how_html, how_heads, "".join(out), heads, [(n, t) for _, _, _, n, t in chapters], kinds


# ---------- printing and merging ----------

def print_pdf(html_text, out_pdf, work):
    exe = preflight.check_browser("build")
    if not exe["ok"]:
        raise BuildError(exe["detail"])
    src = work / (out_pdf.stem + ".html")
    src.write_text(html_text, encoding="utf-8")
    if out_pdf.exists():
        out_pdf.unlink()
    try:
        r = subprocess.run([exe["detail"], "--headless", "--disable-gpu", "--no-first-run", "--allow-file-access-from-files",
                            f"--user-data-dir={work / 'profile'}", "--no-pdf-header-footer", "--generate-pdf-document-outline",
                            f"--print-to-pdf={out_pdf}", src.as_uri()], capture_output=True, text=True, timeout=TIMEOUT_S)
    except subprocess.TimeoutExpired:   # headless Edge can hang on exit after writing the file
        r = None
    if not out_pdf.is_file() or out_pdf.stat().st_size == 0:
        raise BuildError(f"Edge print of {src.name} failed: {r.stderr.strip()[-300:] if r else 'timed out'}")
    return out_pdf


def outline(pdf):
    """[(level, title, 0-based page)] of a printed PDF, in order."""
    from pypdf import PdfReader
    r = PdfReader(str(pdf))
    out = []

    def walk(items, level):
        for it in items:
            if isinstance(it, list):
                walk(it, level + 1)
            else:
                out.append((level, it.title, r.get_destination_page_number(it)))
    walk(r.outline, 1)
    return out, len(r.pages)


def _depths(levels):
    """Tree depth of each heading, as a PDF outline nests them: a skipped level (h2 under no h1) closes up."""
    stack, out = [], []
    for lvl in levels:
        while stack and stack[-1] >= lvl:
            stack.pop()
        stack.append(lvl)
        out.append(len(stack))
    return out


def _match(heads, marks, what):
    """Edge's outline lists the same headings the writer placed, in the same order; anything else is a bug."""
    got = [(lvl, re.sub(r"\s+", " ", t).strip()) for lvl, t, _ in marks]
    want = [(d, re.sub(r"\s+", " ", t).strip()) for d, (_, t) in zip(_depths([lvl for lvl, _ in heads]), heads)]
    key = lambda xs: [(lvl, re.sub(r"\s+", "", t)) for lvl, t in xs]   # Edge drops the space at a wrapped heading's line break
    if key(got) != key(want):
        first = next((k for k, (a, b) in enumerate(zip(key(got), key(want))) if a != b), min(len(got), len(want)))
        raise BuildError(f"{what}: the printed outline ({len(got)} headings) does not match the placed headings "
                         f"({len(want)}); first difference at #{first + 1}: "
                         f"{got[first] if first < len(got) else None} vs {want[first] if first < len(want) else None}")


def roman(n):
    vals = [(1000, "m"), (900, "cm"), (500, "d"), (400, "cd"), (100, "c"), (90, "xc"), (50, "l"), (40, "xl"),
            (10, "x"), (9, "ix"), (5, "v"), (4, "iv"), (1, "i")]
    out = ""
    for v, s in vals:
        while n >= v:
            out, n = out + s, n - v
    return out


def build_pdf(cfg, out_pdf):
    """-> (pdf path, page count). Writes only `out_pdf`; the prints happen in a temporary folder."""
    if cfg["theme"]["direction"] != "ltr":
        raise BuildError("RTL rendering is STEP 10 (Arabic contract §3); the HTML engine renders LTR only")
    from pypdf import PdfReader, PdfWriter
    bk = build_book.Book(cfg)
    w = Writer(bk)
    how_html, how_heads, body, body_heads, chapters, body_kinds = body_parts(cfg, bk, w)
    css = stylesheet(bk, chapters)
    with tempfile.TemporaryDirectory() as t:
        work = pathlib.Path(t)
        body_pdf = print_pdf(page_html(bk, css, body), work / "body.pdf", work)
        body_marks, _ = outline(body_pdf)
        _match(body_heads, body_marks, "body")
        body_pages = [str(p + 1) for _, _, p in body_marks]   # _match paired them one to one
        toc_heads, toc_kinds = how_heads + body_heads, [("other",)] * len(how_heads) + body_kinds
        tp = title_page_html(bk)

        def front(how_pages):
            return page_html(bk, css, tp + toc_html(bk, toc_heads, toc_kinds, how_pages + body_pages) + how_html)
        front_pdf = print_pdf(front([""] * len(how_heads)), work / "front.pdf", work)
        front_marks, _ = outline(front_pdf)
        _match(how_heads, front_marks, "front")
        if how_heads:   # the how-to-use pages depend on the contents length: print again with its numbers
            front_pdf = print_pdf(front([roman(p + 1) for _, _, p in front_marks]), work / "front.pdf", work)
            front_marks, _ = outline(front_pdf)
        cover, ending = cover_html(bk), ending_html(bk)
        pieces = (([print_pdf(page_html(bk, css, cover), work / "cover.pdf", work)] if cover else []) + [front_pdf, body_pdf]
                  + ([print_pdf(page_html(bk, css, ending), work / "ending.pdf", work)] if ending else []))
        writer = PdfWriter()
        offset, starts = 0, {}
        for p in pieces:
            starts[p.stem] = offset
            writer.append(str(p), import_outline=False)
            offset = len(writer.pages)
        if cfg["theme"]["build"]["pdf"]["bookmarks"] == "headings":
            parents = {}
            for name, marks, heads in (("front", front_marks, how_heads), ("body", body_marks, body_heads)):
                for (lvl, _, p), (_, title) in zip(marks, heads):   # _match paired them; the placed title keeps its spaces
                    item = writer.add_outline_item(re.sub(r"\s+", " ", title).strip(), starts[name] + p, parent=parents.get(lvl - 1))
                    parents[lvl] = item
        writer.add_metadata({"/Title": f"{bk.title}: {bk.subtitle}" if bk.subtitle else bk.title, "/Author": bk.credits,
                             "/Creator": "book harness (HTML engine)", "/Producer": "pypdf"})
        from pypdf.generic import NameObject, TextStringObject
        writer._root_object[NameObject("/Lang")] = TextStringObject(cfg["theme"]["lang_tag"])
        out_pdf.parent.mkdir(parents=True, exist_ok=True)
        with open(out_pdf, "wb") as fh:
            writer.write(fh)
    return out_pdf, len(PdfReader(str(out_pdf)).pages)


def main(project, argv):
    try:
        cfg = config.load(project)
        with tempfile.TemporaryDirectory() as t:
            pdf, pages = build_pdf(cfg, pathlib.Path(t) / f"{cfg['theme']['output']['basename']}.pdf")
            print(f"built {pdf.name}: {pages} pages (dry run, not kept)")
    except (config.ConfigError, KeyError, FileNotFoundError) as e:
        print(f"ERROR CONFIG: {e}", file=sys.stderr)
        return 2
    except BuildError as e:
        print(f"ERROR BUILD: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    from harness.gate import enforce
    PROJECT = enforce("build", sys.argv)   # first call: no stage work before the gates pass
    sys.exit(main(PROJECT, sys.argv))
