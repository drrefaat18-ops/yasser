"""Study-summary decks (.pptx, optional .pdf): a short, source-faithful revision deck per chapter. Gate: build.

Usage: python harness/tools/build_study.py --project projects/<book> [--chapter chNN] [--pdf]
Input:  <project>/<slides.out_dir, default "slides">/study/<chapter stem>.json, one outline per chapter (only chapters
        with an outline are built). Output: .../study/out/<stem>-study.pptx (and .pdf), study/out/study-qa.json.

The outline holds only the condensed parts, written by the agent; every point names the chapter sentence it shortens:

    {"chapter": "ch01.md",
     "sections": [{"sec": "1.3", "slides": [
        {"kind": "points", "title": "...", "figure": "<figure id, optional>",
         "points": [{"text": "A **term** is ... (shortened).", "src": "<verbatim words from the chapter>"}]},
        {"kind": "table", "title": "...", "head": ["", "Meaning"], "rows": [["...", "..."]],
         "src": ["<verbatim words>", "..."]},
        {"kind": "flow" | "cards" | "versus" | "equation" | "spectrum", "title": "...",
         "nodes": [{"label": "...", "text": "...", "sub": "<example, italic>", "src": "<verbatim words>"}],
         "caption": [{"text": "<key message under the diagram>", "src": "..."}],
         "ops": ["-", "="] (equation), "highlight": <node index>, "numbered": true (cards),
         "ends": ["<left end>", "<right end>"] (spectrum)}]}]}

Diagrams are native shapes (editable in PowerPoint): flow = boxes joined by arrows (a sequence); cards = a grid of
up to 10 (a list of parts); versus = two or three columns with "vs" (a contrast); equation = boxes joined by
operators (a definition that is a sum or difference); spectrum = boxes under one arrow (a scale), one highlighted.
Every node and caption line is checked like a point. Content slides carry the title in bold inside a framed band.

Fidelity (the build stops on any failure; the report is study-qa.json):
- every `src` is a verbatim span of the chapter (markup, quote style, case and spacing ignored);
- every content word and number on a slide occurs in the chapter (crude stems), so nothing comes from outside it;
- a point shares at least SRC_SHARE of its content words with its own `src`, so it is a shortening of that sentence;
- every core section of the chapter has at least one slide.
Taken word for word from the chapter, not from the outline: objectives, callouts (cards, in their section), key terms
(each bold term with its glossary entry), MCQs (question slide, then answer slide with the reason), and the
one-page revision slide (key takeaways and the key-term list). Speaker notes hold the section's own prose.
Design primitives, palette, lint and the MCQ slides come from build_slides.py (docs/harness/SLIDES.md).
"""
import json, pathlib, re, subprocess, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from harness.tools import build_slides as bs                    # noqa: E402
from pptx.oxml import parse_xml                                  # noqa: E402
from pptx.oxml.ns import qn                                      # noqa: E402

SRC_SHARE = 0.5
MAX_POINTS, MAX_ROWS, TERMS_PER_SLIDE, MAX_CARDS = 4, 5, 4, 6   # few words per slide (user, 2026-10-01)
MCQ_PER_SLIDE, ANSWERS_PER_SLIDE, CALLOUT_CHARS = 2, 3, 300
DIAGRAMS = {"flow": 5, "cards": 12, "versus": 3, "equation": 4, "spectrum": 6}   # kind: most nodes
STOP = set("""a an the and or but nor of in on at to for from by with as is are was were be been being it its this that
these those their there they them then than so such not no can may must will would should could do does did done has have
had which who whom whose what when where why how each every all any some most more less only also very into onto out up
over under one two three four five six seven eight nine ten first second third both either neither own same other""".split())


def norm(t):
    t = t.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    t = t.replace("–", "-").replace("—", "-").replace(" ", " ")
    t = re.sub(r"[*_`>]", "", t)
    return re.sub(r"\s+", " ", t).strip().lower()


def stem(w):
    w = w.lower().replace("'s", "")
    for suf, rep in (("ies", "y"), ("ing", ""), ("ed", ""), ("es", ""), ("s", ""), ("ly", "")):
        if len(w) > len(suf) + 3 and w.endswith(suf):
            return w[: -len(suf)] + rep
    return w


def words(t):
    """Content stems and numbers of a text."""
    toks = re.findall(r"[a-z]+|\d+(?:[.,]\d+)?", norm(t))
    out = {stem(w) if w[0].isalpha() else w for w in toks if not w[0].isalpha() or (len(w) > 2 and w not in STOP)}
    return out - STOP


def sections_of(md):
    """{'1.3': (title, [prose paragraphs], [callouts])}; callout = (label, [paragraphs])."""
    out, cur, quote = {}, None, None
    for ln in md.splitlines() + [""]:
        m = re.match(r"^## (\d+\.\d+)\s+(.+)$", ln)
        if m:
            cur = out.setdefault(m.group(1), (m.group(2).strip(), [], [])); quote = None; continue
        if ln.startswith("## "):
            cur = None; quote = None; continue
        if cur is None:
            continue
        s = ln.strip()
        if s.startswith(">"):
            body = s.lstrip(">").strip()
            if quote is None:
                m = re.match(r"^\*\*(.+?):?\*\*:?\s*(.*)$", body)
                quote = (m.group(1).rstrip(":") if m else "", [m.group(2)] if m and m.group(2) else [])
                cur[2].append(quote)
            elif body:
                quote[1].append(re.sub(r"^- ", "• ", body))
        else:
            quote = None
            if s and not s.startswith(("![", "|", "#")):
                cur[1].append(s)
    return out


def bold_terms(md, sections):
    """Bold terms of the core sections in reading order; labels ending in '.' or ':' are not terms."""
    seen, out = set(), []
    for _, prose, _ in sections.values():
        for para in prose:
            for t in re.findall(r"\*\*(.+?)\*\*", para):
                k = t.lower()
                if t.endswith((".", ":")) or re.match(r"^\d", t) or k in seen:
                    continue
                seen.add(k); out.append(t)
    return out


def glossary(path):
    g = {}
    if path and path.is_file():
        for ln in path.read_text(encoding="utf-8").splitlines():
            m = re.match(r"^\*\*(.+?)\*\* — (.+)$", ln.strip())
            if m:
                g[m.group(1).lower()] = re.sub(r"\s*\(Chapter \d+[^)]*\)\.?$", ".", m.group(2)).rstrip(".") + "."
    return g


def check(outline, md, sections):
    """Fidelity report: list of (where, problem)."""
    text, vocab, issues = norm(md), words(md), []
    covered = {s["sec"] for s in outline["sections"]}
    for sec in sections:
        if sec not in covered:
            issues.append((f"section {sec}", "no slide"))
    for s in outline["sections"]:
        if s["sec"] not in sections:
            issues.append((f"section {s['sec']}", "not a section of the chapter"))
        for k, sl in enumerate(s["slides"]):
            where = f"{s['sec']} slide {k + 1} ({sl.get('title', '')[:30]})"
            items = sl.get("points", []) + sl.get("caption", [])
            nodes = sl.get("nodes", [])
            srcs = [p["src"] for p in items + nodes if p.get("src")] + list(sl.get("src", []))
            for q in srcs:
                if norm(q) not in text:
                    issues.append((where, f"src not verbatim in the chapter: {q[:60]}"))
            cells = [sl.get("title", "")] + [p["text"] for p in items] + list(sl.get("ends", [])) + \
                    [n.get(f, "") for n in nodes for f in ("label", "text", "sub")] + \
                    [c for c in sl.get("head", [])] + [c for r in sl.get("rows", []) for c in r]
            for c in cells:
                foreign = sorted(words(c) - vocab)
                if foreign:
                    issues.append((where, f"words not in the chapter {foreign}: {c[:50]}"))
            for p in items + nodes:
                body = " ".join(p.get(f, "") for f in ("label", "text", "sub"))
                if not p.get("src"):
                    issues.append((where, f"no src: {body[:50]}")); continue
                own = words(body)
                share = len(own & words(p["src"])) / max(len(own), 1)
                if share < SRC_SHARE:
                    issues.append((where, f"point shares {share:.0%} with its src: {body[:50]}"))
            if sl["kind"] in DIAGRAMS and not 1 <= len(nodes) <= DIAGRAMS[sl["kind"]]:
                issues.append((where, f"{sl['kind']} takes 1 to {DIAGRAMS[sl['kind']]} nodes"))
            elif sl["kind"] not in DIAGRAMS and sl["kind"] not in ("points", "table"):
                issues.append((where, f"unknown kind {sl['kind']}"))
            if sl["kind"] == "points" and len(sl.get("points", [])) > MAX_POINTS:
                issues.append((where, f"more than {MAX_POINTS} points"))
            if sl["kind"] == "table" and not sl.get("src"):
                issues.append((where, "table without src"))
    return issues


A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"


def _effects(sh, shadow=True, bevel=False):
    """Soft drop shadow, and for solid parts a soft-round bevel (the 3D look). Call after the line is set."""
    sp = sh._element.spPr
    for tag in ("a:effectLst", "a:scene3d", "a:sp3d"):
        for old in sp.findall(qn(tag)):
            sp.remove(old)
    if shadow:
        sp.append(parse_xml(f'<a:effectLst xmlns:a="{A_NS}"><a:outerShdw blurRad="203200" dist="50800" dir="5400000" '
                            f'algn="t" rotWithShape="0"><a:srgbClr val="1A2340"><a:alpha val="20000"/></a:srgbClr>'
                            f'</a:outerShdw></a:effectLst>'))
    if bevel:
        sp.append(parse_xml(f'<a:scene3d xmlns:a="{A_NS}"><a:camera prst="orthographicFront"/>'
                            f'<a:lightRig rig="threePt" dir="t"/></a:scene3d>'))
        sp.append(parse_xml(f'<a:sp3d xmlns:a="{A_NS}"><a:bevelT w="44450" h="25400" prst="softRound"/></a:sp3d>'))


def _alpha(sh, opacity):
    clr = sh._element.spPr.find(qn("a:solidFill"))[0]
    clr.append(parse_xml(f'<a:alpha xmlns:a="{A_NS}" val="{int(opacity * 1000)}"/>'))


def backgrounds(st, assets):
    """Blurred colour fields for the glass look: light for content slides, dark for title slides."""
    from PIL import Image, ImageDraw, ImageFilter
    W, H = 1920, 1080
    hexrgb = lambda h: tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    out = {}
    for dark in (False, True):
        base = bs.mix(st.pri, "000000", 0.35) if dark else bs.mix(st.pri, bs.WHITE_HEX, 0.95)
        im = Image.new("RGB", (W, H), hexrgb(base))
        blobs = ([(st.acc, 0.85, 0.18, 0.42, 150), (bs.mix(st.pri, bs.WHITE_HEX, 0.35), 0.12, 0.92, 0.45, 130),
                  (st.pri, 0.5, 0.45, 0.35, 110)] if dark else
                 [(bs.mix(st.pri, bs.WHITE_HEX, 0.35), 0.06, 0.1, 0.45, 170), (bs.mix(st.acc, bs.WHITE_HEX, 0.35), 0.95, 0.9, 0.5, 150),
                  (bs.mix(st.pri, bs.WHITE_HEX, 0.6), 0.8, 0.02, 0.35, 160), (bs.mix(st.acc, bs.WHITE_HEX, 0.65), 0.12, 1.0, 0.32, 140),
                  (bs.WHITE_HEX, 0.5, 0.5, 0.55, 200)])
        for col, cx, cy, r, a in blobs:
            layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            ImageDraw.Draw(layer).ellipse((cx * W - r * H, cy * H - r * H, cx * W + r * H, cy * H + r * H),
                                          fill=hexrgb(col) + (a,))
            im = Image.alpha_composite(im.convert("RGBA"), layer.filter(ImageFilter.GaussianBlur(170))).convert("RGB")
        path = assets / f"glass-{'dark' if dark else 'light'}.png"
        im.save(path)
        out[dark] = path
    return out


class StudyDeck(bs.Deck):
    POINTS_FONT = 24

    @staticmethod
    def pages_of(seq, n):
        """Split into the fewest pages of at most n, spread evenly (no half-empty last slide)."""
        parts = max(1, -(-len(seq) // n)); q, extra = divmod(len(seq), parts)
        out, i = [], 0
        for k in range(parts):
            j = i + q + (1 if k < extra else 0); out.append(seq[i:j]); i = j
        return [x for x in out if x] or [seq]

    def __init__(self, book, style, ch, logos, figs, captions, outline, md, gloss, bg=None):
        super().__init__(book, style, ch, logos, figs, captions)
        self.minutes, self.fit = None, False
        self.outline, self.secs = outline, sections_of(md)
        self.terms = [(t, gloss.get(t.lower(), "")) for t in bold_terms(md, self.secs)]
        self.bg = bg or {}
        st = self.st
        self.kick_col = next(bs.mix(st.acc, "000000", z) for z in (0, 0.08, 0.16, 0.24, 0.32, 0.4)
                             if bs.contrast(bs.mix(st.acc, "000000", z), st.glass_bg) >= 4.6 or z == 0.4)

    # ---- glass primitives ---------------------------------------------------------------------------------
    def slide(self, notes="", dark=False):
        s = super().slide(notes, dark)
        if not dark:
            s.background.fill.fore_color.rgb = bs.rgb(self.st.glass_bg)     # what the lint measures against
        if self.bg.get(dark):
            pic = s.shapes.add_picture(str(self.bg[dark]), 0, 0, bs.Inches(bs.W_IN), bs.Inches(bs.H_IN))
            self.alt(pic, "")                                                # decorative
            tree = s.shapes._spTree; tree.remove(pic._element); tree.insert(2, pic._element)
        return s

    def panel(self, s, x, y, w, h, opacity=58, border=None, bw=1.5, fill=bs.WHITE_HEX, radius=0.08):
        """Frosted glass: translucent fill, light border, soft shadow."""
        sh = self.rect(s, x, y, w, h, fill, bs.MSO_SHAPE.ROUNDED_RECTANGLE, radius)
        _alpha(sh, opacity)
        sh.line.color.rgb = bs.rgb(border or bs.WHITE_HEX); sh.line.width = bs.Pt(bw)
        _effects(sh)
        return sh

    def solid(self, s, x, y, w, h, fill, shape=bs.MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.18):
        sh = self.rect(s, x, y, w, h, fill, shape, radius)
        _effects(sh, bevel=True)
        return sh

    def label(self, sh, text, size, color=bs.WHITE_HEX, font=None, align=bs.PP_ALIGN.CENTER):
        small = sh.width < bs.Inches(1.0)                                   # discs and chips: never wrap
        tf = sh.text_frame; tf.word_wrap = not small
        tf.margin_left = tf.margin_right = bs.Inches(0 if small else 0.12); tf.margin_top = tf.margin_bottom = 0
        tf.vertical_anchor = bs.MSO_ANCHOR.MIDDLE
        q = tf.paragraphs[0]; q.alignment = align
        self.runs(q, text, size, color, True, font)

    def content(self, kicker, title, notes="", kind="content"):
        """Content slide: the title in bold inside a framed glass band."""
        st = self.st
        s = self.slide(notes)
        self.titles[-1], self.kinds[-1] = title, kind
        self.panel(s, bs.M - 0.15, 0.3, bs.CW + 0.3, 1.2, 70, st.pri, 2.25, radius=0.14)
        self.label(self.solid(s, bs.M + 0.1, 0.54, 0.72, 0.72, st.acc, bs.MSO_SHAPE.OVAL), self.num, 18, font=st.head)
        k = self.text(s, bs.M + 1.1, 0.44, bs.CW - 1.3, 0.3)
        self.runs(k.paragraphs[0], kicker.upper(), 12, self.kick_col, True, spacing=150)
        t = self.text(s, bs.M + 1.1, 0.72, bs.CW - 1.3, 0.7, bs.MSO_ANCHOR.MIDDLE)
        self.runs(t.paragraphs[0], title, 30 if len(title) < 46 else 25, st.pri, True, st.head)
        self.footer(s)
        return s

    def glass_rows(self, s, items, x, y, w, h, size=None, start=1):
        """Numbered points inside one glass panel; large type, few words."""
        self.panel(s, x, y, w, h)
        self.rows(s, items, y=y + 0.35, h=h - 0.6, x=x + 0.35, w=w - 0.7, size=size or self.POINTS_FONT, start=start)

    # ---- sizing --------------------------------------------------------------------------------------------
    @staticmethod
    def dh(paras, w, z, em=0.43):
        """Height of short text. Average character width measured on PowerPoint exports: body text about 0.43 em,
        bold heading font about 0.56 em."""
        per = max(int((w - 0.1) * 72 / (z * em)), 1)
        return sum(max(1, -(-len(bs.clean(t).replace("**", "")) // per)) * z * 1.22 / 72 + 0.1 for t in paras)

    def fitsize(self, paras, w, h, sizes=(22, 20, 19, 18, 17, 16, 15, 14, 13, 12), em=0.43):
        """Largest size at which the text fits the box and its longest word fits one line (no broken words)."""
        word = max((len(x) for t in paras for x in re.split(r"[\s\-–]+", bs.clean(t).replace("**", ""))), default=1)
        return next((z for z in sizes if self.dh(paras, w, z, em) <= h and word * z * (em + 0.14) / 72 <= w - 0.15),
                    sizes[-1])

    def layout(self, nodes, w, h, labels=None):
        """One label size, header height and text size for a row of nodes (uniform look); the height they need."""
        labels = labels or [n["label"] for n in nodes]
        lsz = min(self.fitsize([l], w - 0.3, 0.9, (20, 19, 18, 17, 16, 15, 14), 0.56) for l in labels)
        hh = max(0.66, max(self.dh([l], w - 0.3, lsz, 0.56) for l in labels) + 0.16)
        paras = [[t for t in (n.get("text", ""), n.get("sub", "")) if t] for n in nodes]
        z = min((self.fitsize(ps, w - 0.4, h - hh - 0.3) for ps in paras if ps), default=22)
        need = hh + max((self.dh(ps, w - 0.4, z) for ps in paras if ps), default=0) + 0.45
        if not any(paras):
            need = max(1.2, hh + 0.4)                                       # label-only blocks
        return lsz, hh, z, need

    # ---- diagrams ------------------------------------------------------------------------------------------
    def box(self, s, x, y, w, h, node, lay, fill, label=None):
        """A node: a 3D header with the label on a glass card, the text below, an italic example under it."""
        st, (lsz, hh, z, _) = self.st, lay
        paras = [t for t in (node.get("text", ""), node.get("sub", "")) if t]
        if not paras:                                                       # label only: one 3D block
            self.label(self.solid(s, x, y, w, h, fill, radius=0.12), label or node["label"],
                       self.fitsize([label or node["label"]], w - 0.3, h - 0.2, (22, 20, 19, 18, 17, 16), 0.56), font=st.head)
            return
        self.panel(s, x, y, w, h)
        self.label(self.solid(s, x, y, w, hh, fill), label or node["label"], lsz, font=st.head)
        body = self.text(s, x + 0.2, y + hh + 0.18, w - 0.4, h - hh - 0.28)
        for i, t in enumerate(paras):
            q = body.paragraphs[0] if i == 0 else body.add_paragraph(); q.space_before = bs.Pt(0 if i == 0 else 8)
            ex = bool(node.get("sub")) and i == len(paras) - 1
            self.runs(q, t, z, st.mut if ex else st.ink, italic=ex)

    def connector(self, s, x, y, w, glyph=None):
        if glyph:
            self.label(self.solid(s, x + (w - 0.62) / 2, y - 0.31, 0.62, 0.62, self.st.acc, bs.MSO_SHAPE.OVAL),
                       glyph, 22, font=self.st.head)
        else:
            self.solid(s, x + 0.08, y - 0.24, w - 0.16, 0.48, self.st.acc, bs.MSO_SHAPE.RIGHT_ARROW)

    def caption_bar(self, s, items):
        """Key-message glass bar under a diagram, with an accent tab; returns the height it takes."""
        if not items:
            return 0
        texts = [c["text"] for c in items]
        z = self.fitsize(texts, bs.CW - 1.0, 1.2, (22, 20, 19, 18))
        h = self.dh(texts, bs.CW - 1.0, z) + 0.35
        y = bs.BOTTOM - h
        self.panel(s, bs.M, y, bs.CW, h, 72)
        self.solid(s, bs.M + 0.18, y + 0.18, 0.12, h - 0.36, self.st.acc, bs.MSO_SHAPE.RECTANGLE)
        tf = self.text(s, bs.M + 0.5, y + 0.12, bs.CW - 0.8, h - 0.24, bs.MSO_ANCHOR.MIDDLE)
        for i, t in enumerate(texts):
            q = tf.paragraphs[0] if i == 0 else tf.add_paragraph(); q.space_before = bs.Pt(0 if i == 0 else 4)
            self.runs(q, t, z)
        return h + 0.3

    def diagram(self, sec, sl, notes):
        kind, nodes = sl["kind"], sl["nodes"]
        if kind == "cards" and len(nodes) > MAX_CARDS:                 # fewer words per slide: split the grid
            parts = -(-len(nodes) // MAX_CARDS); per = -(-len(nodes) // parts)
            for k in range(parts):
                part = dict(sl, nodes=nodes[k * per:(k + 1) * per], start=k * per,
                            title=f"{sl['title']} ({k + 1}/{parts})", caption=sl.get("caption", []) if k == parts - 1 else [])
                self.diagram(sec, part, notes)
            return
        s = self.content(self.kick(sec), sl["title"], notes, "diagram")
        st = self.st
        top = bs.TOP + 0.05
        band = bs.BOTTOM - top - self.caption_bar(s, sl.get("caption", []))
        n, x0, cw, hi = len(nodes), bs.M, bs.CW, sl.get("highlight", -99)
        if kind in ("flow", "equation", "versus"):
            gap = 0.75 if kind == "versus" else 0.6
            w = (cw - gap * (n - 1)) / n
            lay = self.layout(nodes, w, band)
            h = min(band, max(lay[3], 2.0)); y = top + (band - h) / 2        # boxes fit their text, centred
            ops = sl.get("ops") or []
            for i, nd in enumerate(nodes):
                x = x0 + i * (w + gap)
                strong = i == hi or (kind == "equation" and i == n - 1) or (kind == "versus" and i % 2 == 1)
                self.box(s, x, y, w, h, nd, lay, st.acc if strong else st.pri)
                if i < n - 1:
                    glyph = (ops[i] if i < len(ops) else None) if kind == "equation" else ("vs" if kind == "versus" else None)
                    self.connector(s, x + w, y + h / 2, gap, glyph)
        elif kind == "cards":
            cols = n if n <= 5 else -(-n // 2)
            rws, gx, gy = -(-n // cols), 0.25, 0.3
            w, cell = (cw - gx * (cols - 1)) / cols, (band - gy * (rws - 1)) / rws
            k0 = sl.get("start", 0)
            labs = [f"{k0 + i + 1}. {nd['label']}" if sl.get("numbered") else nd["label"] for i, nd in enumerate(nodes)]
            lay = self.layout(nodes, w, cell, labs)
            hh = min(cell, max(lay[3], 1.6 if any(n.get("text") for n in nodes) else 1.2))
            y0 = top + (band - (hh * rws + gy * (rws - 1))) / 2
            for i, nd in enumerate(nodes):
                r, c = divmod(i, cols)
                self.box(s, x0 + c * (w + gx), y0 + r * (hh + gy), w, hh, nd, lay, st.acc if i == hi else st.pri, labs[i])
        elif kind == "spectrum":
            gx = 0.2; w = (cw - gx * (n - 1)) / n
            lay = self.layout(nodes, w, band - 0.7)
            h = min(band - 0.7, max(lay[3], 2.0)); y = top + (band - 0.7 - h) / 2
            self.solid(s, x0, y, cw, 0.55, st.warm2, bs.MSO_SHAPE.RIGHT_ARROW)
            for j, e in enumerate(sl.get("ends") or []):
                tf = self.text(s, x0 + 0.25 + j * (cw / 2 - 0.6), y + 0.1, cw / 2 - 0.4, 0.35, bs.MSO_ANCHOR.MIDDLE)
                tf.paragraphs[0].alignment = bs.PP_ALIGN.RIGHT if j else bs.PP_ALIGN.LEFT
                self.runs(tf.paragraphs[0], e.upper(), 12, st.pri, True, spacing=120)
            for i, nd in enumerate(nodes):
                self.box(s, x0 + i * (w + gx), y + 0.7, w, h, nd, lay, st.acc if i == hi else st.pri)

    # ---- section slides ------------------------------------------------------------------------------------
    def facts(self):
        return [(str(len(self.secs)), "sections"), (str(len(self.terms)), "key terms"), (str(len(self.mcqs)), "questions")]

    def kick(self, sec):
        return f"§{sec}  ·  {self.secs[sec][0]}"

    def objectives(self):
        label = next((x["label"] for x in self.b.template["sections"] if x["role"] == "objectives"), "Objectives")
        s = self.content(self.unit, label, " ".join(self.ch["intro"]))
        self.glass_rows(s, self.ch["los"], bs.M, bs.TOP, 8.4, bs.BOTTOM - bs.TOP, 20)
        self.panel(s, 9.35, bs.TOP, bs.CW + bs.M - 9.35, bs.BOTTOM - bs.TOP, 66)
        tf = self.text(s, 9.7, bs.TOP + 0.35, 2.8, bs.BOTTOM - bs.TOP - 0.6)
        for i, (big, small) in enumerate(self.facts()):
            q = tf.paragraphs[0] if i == 0 else tf.add_paragraph(); q.space_before = bs.Pt(0 if i == 0 else 16)
            self.runs(q, big, 54, self.st.pri, True, self.st.head)
            self.runs(tf.add_paragraph(), small.upper(), 12, self.st.mut, True, spacing=150)

    def agenda(self, titles):
        s = self.content(self.unit, "Roadmap", "What we will cover, in order.", "agenda")
        half = -(-len(titles) // 2)
        for k, part in enumerate((titles[:half], titles[half:])):
            if part:
                self.glass_rows(s, part, bs.M + k * (bs.CW / 2 + 0.15), bs.TOP, bs.CW / 2 - 0.15, bs.BOTTOM - bs.TOP,
                                21, start=1 + k * half)

    def points(self, sec, sl, notes):
        s = self.content(self.kick(sec), sl["title"], notes, "list")
        pts = [p["text"] for p in sl["points"]]
        fig = sl.get("figure")
        if fig and fig in self.figs:
            self.glass_rows(s, pts, bs.M, bs.TOP, 4.6, bs.BOTTOM - bs.TOP, 20)
            self.panel(s, bs.M + 4.85, bs.TOP, bs.CW - 4.85, bs.BOTTOM - bs.TOP, 80)
            self.visual(s, {"kind": "fig", "data": fig}, bs.M + 5.05, bs.TOP + 0.15, bs.CW - 5.25, bs.BOTTOM - bs.TOP - 0.3)
        else:
            self.glass_rows(s, pts, bs.M, bs.TOP, bs.CW, bs.BOTTOM - bs.TOP)

    def table_slides(self, title, kicker, head, rows, notes):
        parts = self.pages_of(rows, MAX_ROWS)
        for i, part in enumerate(parts):
            suffix = f" ({i + 1}/{len(parts)})" if len(parts) > 1 else ""
            s = self.content(kicker, title + suffix, notes, "dense")
            self.table(s, [head] + part)

    @staticmethod
    def chunks(paras, limit=CALLOUT_CHARS):
        """Split a long callout at sentence ends so each slide carries little text (every word is kept)."""
        out, cur = [], []
        for para in paras:
            for sent in re.split(r"(?<=[.!?])\s+(?=[A-Z\"“•])", para):
                if cur and sum(len(x) for x in cur) + len(sent) > limit:
                    out.append(cur); cur = []
                if cur and para.startswith("• ") and sent.startswith("• "):
                    out.append(cur); cur = []                          # one lens bullet per slide
                cur.append(sent)
        if cur:
            out.append(cur)
        return [[" ".join(c)] for c in out]

    def callout(self, sec, label, body, notes):
        fill, tone = self.st.tone(self.b.callout_by_label.get(label, ""))
        parts = self.chunks([b for b in body if b])
        for i, part in enumerate(parts):
            suffix = f" ({i + 1}/{len(parts)})" if len(parts) > 1 else ""
            s = self.content(self.kick(sec), label + suffix, notes, "callout")
            x, w, band = bs.M + 0.5, bs.CW - 1.0, bs.BOTTOM - bs.TOP - 0.3
            z = self.fitsize(part, w - 0.8, band - 1.4, (26, 24, 22, 20, 19, 18))
            h = min(band, max(2.6, self.dh(part, w - 0.8, z) + 1.6)); y = bs.TOP + 0.15 + (band - h) / 2
            self.panel(s, x, y, w, h, 62, fill=fill)
            self.label(self.solid(s, x + 0.4, y + 0.35, 0.4 + 0.13 * len(label), 0.46, tone, radius=0.5), label.upper(), 13)
            tf = self.text(s, x + 0.4, y + 1.1, w - 0.8, h - 1.3)
            for k, t in enumerate(part):
                q = tf.paragraphs[0] if k == 0 else tf.add_paragraph(); q.space_before = bs.Pt(0 if k == 0 else 10)
                self.runs(q, t.replace("• ", ""), z)

    # ---- end of the deck -----------------------------------------------------------------------------------
    def key_terms(self):
        rows = [(t[:1].upper() + t[1:], d) for t, d in self.terms if d]
        parts = self.pages_of(rows, TERMS_PER_SLIDE)
        per = max(len(x) for x in parts) if parts else TERMS_PER_SLIDE
        gap = 0.2
        for i, part in enumerate(parts):
            s = self.content(f"{self.unit}  ·  definitions", f"Key terms ({i + 1}/{len(parts)})" if len(parts) > 1
                             else "Key terms", "Definitions from the book's glossary.", "terms")
            h = (bs.BOTTOM - bs.TOP - gap * (per - 1)) / per
            for k, (term, d) in enumerate(part):
                y = bs.TOP + k * (h + gap)
                self.panel(s, bs.M, y, bs.CW, h)
                self.label(self.solid(s, bs.M + 0.2, y + 0.18, 3.3, h - 0.36, self.st.pri), term,
                           self.fitsize([term], 3.0, h - 0.4, (20, 18, 17, 16), 0.56), font=self.st.head)
                tf = self.text(s, bs.M + 3.8, y + 0.1, bs.CW - 4.1, h - 0.2, bs.MSO_ANCHOR.MIDDLE)
                self.runs(tf.paragraphs[0], d, self.fitsize([d], bs.CW - 4.1, h - 0.2, (20, 19, 18, 17, 16)))

    def strip_lo(self, q):
        return re.sub(r"^\[[^\]]+\]\s*", "", q)

    def mcq_pairs(self):
        """Two questions per slide, no answers on them; the answer key closes the deck."""
        qs, total = self.mcqs, len(self.mcqs)
        st, gap = self.st, 0.25
        bh = (bs.BOTTOM - bs.TOP - gap) / 2
        for k in range(0, total, MCQ_PER_SLIDE):
            pair = qs[k:k + MCQ_PER_SLIDE]
            nums = f"{pair[0]['n']}–{pair[-1]['n']}" if len(pair) > 1 else pair[0]["n"]
            s = self.content(f"{self.unit}  ·  self-test", f"Questions {nums}",
                             "Answers and reasons are on the answer-key slides at the end.", "mcq")
            for j, q in enumerate(pair):
                y = bs.TOP + j * (bh + gap)
                self.panel(s, bs.M, y, bs.CW, bh)
                self.label(self.solid(s, bs.M + 0.25, y + 0.22, 0.95, 0.5, st.pri), f"Q{q['n']}", 16, font=st.head)
                text = self.strip_lo(q["q"])
                qz = self.fitsize([text], bs.CW - 1.9, 0.75, (20, 19, 18, 17))
                tf = self.text(s, bs.M + 1.45, y + 0.2, bs.CW - 1.75, 0.8, bs.MSO_ANCHOR.MIDDLE)
                self.runs(tf.paragraphs[0], text, qz, st.ink, True)
                opts = [(o[0], o[3:]) for o in q["opts"]]
                cols = 2                                                  # long options wrap inside their pill
                ow = (bs.CW - 0.5 - 0.25 * (cols - 1)) / cols
                oy = y + 1.1
                oh = (bh - 1.25 - 0.1 * (-(-len(opts) // cols) - 1)) / (-(-len(opts) // cols))
                for i, (letter, body) in enumerate(opts):
                    r, c = divmod(i, cols)
                    x = bs.M + 0.25 + c * (ow + 0.25); yy = oy + r * (oh + 0.1)
                    self.panel(s, x, yy, ow, oh, 80, st.warm2, 1, radius=0.3)
                    d = min(oh - 0.08, 0.42)
                    self.label(self.solid(s, x + 0.1, yy + (oh - d) / 2, d, d, st.acc, bs.MSO_SHAPE.OVAL), letter, 13)
                    b = self.text(s, x + 0.65, yy, ow - 0.75, oh, bs.MSO_ANCHOR.MIDDLE)
                    self.runs(b.paragraphs[0], body, self.fitsize([body], ow - 0.75, oh, (18, 17, 16, 15)), st.ink)

    def answer_key(self):
        rows = []
        for q in self.mcqs:
            key, why = self.ch["answers"].get(q["n"], ("", ""))
            opt = next((o[3:] for o in q["opts"] if o[0] == key), "")
            rows.append((q["n"], key, opt, why))
        parts = self.pages_of(rows, ANSWERS_PER_SLIDE)
        gap, st = 0.18, self.st
        for i, part in enumerate(parts):
            s = self.content(f"{self.unit}  ·  self-test", f"Answer key ({i + 1}/{len(parts)})" if len(parts) > 1
                             else "Answer key", "", "answers")
            h = (bs.BOTTOM - bs.TOP - gap * (ANSWERS_PER_SLIDE - 1)) / ANSWERS_PER_SLIDE
            for k, (n, key, opt, why) in enumerate(part):
                y = bs.TOP + k * (h + gap)
                self.panel(s, bs.M, y, bs.CW, h)
                self.label(self.solid(s, bs.M + 0.2, y + (h - 0.6) / 2, 0.95, 0.6, st.pri), f"Q{n}", 16, font=st.head)
                self.label(self.solid(s, bs.M + 1.3, y + (h - 0.6) / 2, 0.6, 0.6, st.acc, bs.MSO_SHAPE.OVAL), key, 18,
                           font=st.head)
                tf = self.text(s, bs.M + 2.15, y + 0.08, bs.CW - 2.4, h - 0.16, bs.MSO_ANCHOR.MIDDLE)
                self.runs(tf.paragraphs[0], opt, 18, st.pri, True)
                q = tf.add_paragraph(); q.space_before = bs.Pt(3)
                self.runs(q, why, self.fitsize([why], bs.CW - 2.4, h - 0.6, (18, 17, 16, 15)), st.ink)

    def revision(self):
        items = self.ch["takeaways"]
        parts = self.pages_of(items, MAX_POINTS)
        for i, part in enumerate(parts):
            s = self.content(f"{self.unit}  ·  revision", f"Key takeaways ({i + 1}/{len(parts)})" if len(parts) > 1
                             else "Key takeaways", "The chapter's key takeaways, for last-minute revision.", "revision")
            self.glass_rows(s, part, bs.M, bs.TOP, bs.CW, bs.BOTTOM - bs.TOP, 22, start=1 + sum(len(x) for x in parts[:i]))
        terms = [t[:1].upper() + t[1:] for t, _ in self.terms]
        if not terms:
            return
        s = self.content(f"{self.unit}  ·  revision", "Key terms at a glance", "Every key term of the chapter.", "revision")
        cols = 4; rws = -(-len(terms) // cols); gx, gy = 0.2, 0.16
        w = (bs.CW - gx * (cols - 1)) / cols; h = min(0.8, (bs.BOTTOM - bs.TOP - gy * (rws - 1)) / rws)
        for i, t in enumerate(terms):
            r, c = divmod(i, cols)
            sh = self.panel(s, bs.M + c * (w + gx), bs.TOP + r * (h + gy), w, h, 70, radius=0.3)
            self.label(sh, t, self.fitsize([t], w - 0.3, h - 0.1, (18, 17, 16, 15), 0.5), self.st.pri, self.st.head)

    def build(self):
        self.title_slide(); self.objectives()
        self.agenda([self.secs[s["sec"]][0] for s in self.outline["sections"]])
        for s in self.outline["sections"]:
            sec = s["sec"]; title, prose, callouts = self.secs[sec]
            notes = f"Source: §{sec} {title}.\n\n" + "\n\n".join(prose)
            for sl in s["slides"]:
                if sl["kind"] == "points":
                    self.points(sec, sl, notes)
                elif sl["kind"] == "table":
                    self.table_slides(sl["title"], self.kick(sec), sl["head"], sl["rows"], notes)
                elif sl["kind"] in DIAGRAMS:
                    self.diagram(sec, sl, notes)
            for label, body in callouts:
                self.callout(sec, label, body, f"Source: §{sec}, {label} box (verbatim).")
        self.key_terms()
        if self.b.cfg.get("mcq_slides", True) and self.mcqs:
            self.mcq_pairs()
        if self.ch["takeaways"]:
            self.revision()
        if self.b.cfg.get("mcq_slides", True) and self.mcqs:
            self.answer_key()
        self.finish()
        return self.prs


def to_pdf(pptx):
    """PowerPoint COM export (Windows); returns the PDF path or None when PowerPoint is not available."""
    pdf = pptx.with_suffix(".pdf")
    ps = (f"$p=New-Object -ComObject PowerPoint.Application; $d=$p.Presentations.Open('{pptx}', $true, $false, $false);"
          f" $d.SaveAs('{pdf}', 32); $d.Close(); $p.Quit()")
    try:
        subprocess.run(["powershell", "-NoProfile", "-Command", ps], check=True, capture_output=True, timeout=300)
    except (OSError, subprocess.SubprocessError):
        return None
    return pdf if pdf.is_file() else None


def main(project, only=None, pdf=False):
    book = bs.Book(project)
    style = bs.Style(book.theme, book.cfg)
    p = book.project
    figs, captions = bs.figures(book)
    base = p / (book.cfg.get("out_dir") or "slides") / "study"
    out = base / "out"; out.mkdir(parents=True, exist_ok=True)
    assets = out / "_assets"; assets.mkdir(exist_ok=True)
    logos = [bs.badge(p / rel, assets / pathlib.Path(rel).name)
             for rel in ((book.theme.get("cover") or {}).get("design") or {}).get("logos") or []]
    chapters = p / book.template["paths"]["chapters"]
    gpath = book.template["paths"].get("glossary")
    gloss = glossary(chapters / gpath if gpath else None)
    style.glass_bg = bs.mix(style.pri, bs.WHITE_HEX, 0.9)
    bg = backgrounds(style, assets)
    status, report = 0, {}
    for c in book.plan["chapters"]:
        stem_ = pathlib.Path(c["file"]).stem
        src = base / f"{stem_}.json"
        if not src.is_file() or (only and not stem_.startswith(only)):
            continue
        md = (chapters / c["file"]).read_text(encoding="utf-8")
        outline = json.loads(src.read_text(encoding="utf-8"))
        issues = check(outline, md, sections_of(md))
        deck = StudyDeck(book, style, bs.parse(md, book), logos, figs, captions, outline, md, gloss, bg)
        missing = [t for t, d in deck.terms if not d]
        issues += [("key terms", f"no glossary entry: {t}") for t in missing]
        report[stem_] = {"fidelity": [{"where": w, "problem": x} for w, x in issues]}
        if issues:
            print(f"{stem_}: FIDELITY FAILED ({len(issues)})")
            for w, x in issues:
                print(f"  {w}: {x}")
            status = 1; continue
        prs = deck.build()
        report[stem_]["lint"] = [{"slide": i, "check": k, "detail": d} for i, k, d in bs.lint(prs, deck.kinds)]
        path = out / f"{stem_}-study.pptx"
        try:
            prs.save(path)
        except PermissionError:
            print(f"{path.name}: SKIPPED, file is open; close it and run again"); status = 1; continue
        made = to_pdf(path.resolve()) if pdf else None
        counts = {}
        for x in report[stem_]["lint"]:
            counts[x["check"]] = counts.get(x["check"], 0) + 1
        print(f"{path.name}: {len(prs.slides)} slides  fidelity: ok  QA: {counts or 'clean'}"
              + (f"  PDF: {made.name}" if made else ""))
    (out / "study-qa.json").write_text(json.dumps(report, indent=1, ensure_ascii=False), encoding="utf-8")
    return status


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    from harness.gate import enforce
    PROJECT = enforce("build", sys.argv, content_only=True)   # read-only side product, like build_slides
    args = sys.argv[1:]
    only = args[args.index("--chapter") + 1] if "--chapter" in args else None
    sys.exit(main(PROJECT, only, "--pdf" in args))
