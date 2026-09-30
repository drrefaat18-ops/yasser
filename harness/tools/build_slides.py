"""Teaching slide decks (.pptx), one per chapter, from the reworked chapters. Gate: build.

Usage: python harness/tools/build_slides.py --project projects/<book>
Output: <project>/<slides.out_dir, default "slides">/<chapter-file>.pptx, plus _assets/ (logo badges).

Everything book-specific comes from the project (Rule 8): palette, callout colours, cover logos and institution
(theme.json); chapter heading, section labels, callout syntax, MCQ letters and case label (template.json); title
(brief.json); and the optional slides.json:

    {"out_dir": "slides", "unit_label": "Section", "minutes": 45,
     "mcq_slides": true, "explain_on_slide": true, "speaker_notes": true,
     "feature_callout": "<callout id shown on a half-bleed panel>", "feature_glyph": "<one character>",
     "case_glyph": "?", "fonts": {"head": "Cambria", "body": "Calibri"},
     "preset": null | one of PRESETS (overrides the book palette), "agenda": true,
     "background": "<hex for content slides; default theme.palette.paper>"}

Deck: title; objectives with a stat card; per core section, each figure/table/list with the explanation that
precedes it in the chapter (above the visual when short, beside it, or on its own slide first when long); callout
cards; the feature callout on a half-bleed panel; one question slide and one answer slide per MCQ; the case (model
answer in the notes); key takeaways on a dark closing slide. Section prose is also kept in the speaker notes.
Density: at most 6 points or 8 table rows per slide (more splits into "(1/2)" slides, never shrinks below the font
floor); page numbers "05 / 24"; notes end with a timing estimate and the next slide; every picture has alt text; a
lint pass writes <out_dir>/qa-report.json (overflow, font floor, contrast, placeholders, density, rhythm).
Rules distilled from open-source slide skills; sources and lessons in docs/harness/SLIDES.md.
"""
import json, pathlib, re, sys
from PIL import Image, ImageDraw
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

W_IN, H_IN, M = 13.333, 7.5, 0.6          # 16:9 canvas and side margin, inches
CW = W_IN - 2 * M
TOP, BOTTOM = 1.7, 6.75                   # content band under the header, above the footer
WHITE_HEX = "FFFFFF"


def mix(hex_a, hex_b, t):
    """t=0 -> a, t=1 -> b."""
    a = [int(hex_a[i:i + 2], 16) for i in (0, 2, 4)]
    b = [int(hex_b[i:i + 2], 16) for i in (0, 2, 4)]
    return "".join(f"{round(x + (y - x) * t):02X}" for x, y in zip(a, b))


# name: (primary, accent, ink, muted, head font, body font) -- professional sets from the slide-skill survey
PRESETS = {
    "academic-defense": ("2D4A7A", "B03A2E", "1B2A4A", "44506B", "Cambria", "Calibri"),
    "light-corporate": ("1D4ED8", "0284C7", "0F172A", "334155", "Calibri", "Calibri"),
    "data-forward": ("0284C7", "0F7B6C", "0F172A", "475569", "Calibri", "Calibri"),
    "academic-royal": ("4B0082", "B03A2E", "1A1A2E", "3F3F5E", "Cambria", "Calibri"),
    "warm-editorial": ("C2410C", "1C1917", "1C1917", "57534E", "Georgia", "Calibri"),
    "indigo-porcelain": ("0A1F3D", "3366A8", "0A1F3D", "4A5568", "Cambria", "Calibri"),
    "forest-ink": ("1A2E1F", "2E7D5B", "1A2E1F", "4A5A4E", "Cambria", "Calibri"),
    "swiss-ikb": ("002FA7", "002FA7", "0A0A0A", "737373", "Arial", "Arial"),
    "strategy-consulting": ("1B3A6B", "3366A8", "1A2B4A", "6B7A90", "Calibri", "Calibri"),
    "executive": ("1E3A5F", "C9A227", "2C3E50", "6B7A90", "Georgia", "Calibri"),
}


def luminance(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def contrast(a, b):
    hi, lo = sorted((luminance(a), luminance(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def readable_on_white(h, target=4.5):
    """Darken a colour until white text on it (and it on white) reaches the WCAG ratio."""
    t = 0.0
    while contrast(mix(h, "000000", t), WHITE_HEX) < target and t < 0.9:
        t += 0.05
    return mix(h, "000000", t)


def rgb(h):
    return RGBColor.from_string(h.lstrip("#").upper())


def clean(t):
    t = re.sub(r"\s*\[(\d+(?:\s*[,–-]\s*\d+)*)\]", "", t)          # citations are for the book, not the slide
    t = re.sub(r"\^([^^]+)\^", r"\1", t)
    return re.sub(r"(?<!\*)\*(?!\*)", "", t)


class Style:
    def __init__(self, theme, slides_cfg):
        pal = {k: v.lstrip("#").upper() for k, v in theme["palette"].items()}
        self.pri, self.acc, self.ink, self.mut = pal["primary"], pal["accent"], pal["ink"], pal["muted"]
        preset = PRESETS.get(slides_cfg.get("preset") or "")
        if preset:
            self.pri, self.acc, self.ink, self.mut = preset[:4]
        self.pri, self.acc = readable_on_white(self.pri), readable_on_white(self.acc)   # white text on both
        self.mut = readable_on_white(self.mut)
        self.pri_d = mix(self.pri, "000000", 0.15)                 # tone-on-tone numeral on the dark slides
        self.light = next(mix(self.pri, WHITE_HEX, t) for t in (0.86, 0.9, 0.94, 1.0)   # light text on the primary
                          if contrast(mix(self.pri, WHITE_HEX, t), self.pri) >= 4.5 or t == 1.0)
        self.warm = mix(self.pri, WHITE_HEX, 0.94)                 # zebra rows, cards
        self.warm2 = mix(self.pri, WHITE_HEX, 0.85)
        self.acc_l = mix(self.acc, WHITE_HEX, 0.88)
        self.faded = mix(self.mut, WHITE_HEX, 0.93)
        self.faded_disc = mix(self.mut, WHITE_HEX, 0.80)
        # content-slide background: slides.json "background", else the book's paper colour, else white
        self.bg = (slides_cfg.get("background") or pal.get("paper") or WHITE_HEX).lstrip("#").upper()
        fonts = slides_cfg.get("fonts") or {}
        self.head = fonts.get("head") or (preset[4] if preset else "Cambria")      # fonts that ship with Office
        self.body = fonts.get("body") or (preset[5] if preset else "Calibri")
        self.callouts = theme.get("callouts") or {}

    def tone(self, callout_id):
        """(fill, label colour) of a callout card, from theme.callouts; primary tint otherwise."""
        c = self.callouts.get(callout_id) or {}
        return (c.get("fill") or self.warm).lstrip("#"), (c.get("label_colour") or self.pri).lstrip("#")


class Book:
    """The parts of the project config the parser needs."""

    def __init__(self, project):
        from harness.tools import config                      # template with locale defaults filled in
        cfg = config.load(project)
        self.project = pathlib.Path(project)
        self.brief, self.template, self.theme, self.plan = cfg["brief"], cfg["template"], cfg["theme"], cfg["chapter_plan"]
        sp = self.project / "slides.json"
        self.cfg = json.loads(sp.read_text(encoding="utf-8")) if sp.is_file() else {}
        roles = {s["role"]: s["label"] for s in self.template["sections"]}
        self.section_role = {v: k for k, v in roles.items()}
        self.callout_by_label = {c["label"]: c["id"] for c in self.template["callouts"]}
        labels = self.theme.get("labels") or {}
        self.q_prefix = labels.get("question_prefix") or "Q"
        self.lo_prefix = labels.get("objective_prefix") or "LO"
        a = self.template["assessment"]
        self.case_label = (a.get("case_question") or {}).get("label") or ""
        self.letters = a["mcq"]["option_labels"] if a.get("mcq", {}).get("enabled") else []
        self.chapter_rx = re.compile(self.template["chapter_heading_pattern"])
        self.unit = self.cfg.get("unit_label") or labels.get("chapter") or "Chapter"


def parse(md, book):
    """Chapter markdown -> {num, title, los, intro, sections[{title, items}], takeaways, mcq, answers, case,
    case_answer}. Items keep document order: para, table, fig, list, callout(id, label, text), sub, break."""
    ch = {"title": "", "num": "", "los": [], "sections": [], "takeaways": [], "mcq": [], "case": "", "case_answer": "",
          "answers": {}, "intro": []}
    qp, lp = re.escape(book.q_prefix), re.escape(book.lo_prefix)
    letters = "".join(book.letters) or "ABCD"
    case = re.escape(book.case_label) if book.case_label else None
    cur, role = None, None
    for ln in md.splitlines():
        m = book.chapter_rx.match(ln)
        if m:
            ch["num"], ch["title"] = m.group("num"), m.group("title").strip(); continue
        if ln.startswith("## "):
            name = ln[3:].strip()
            role = book.section_role.get(name, "core")
            if role == "core":
                cur = {"title": re.sub(r"^\d+\.\d+\s*", "", name), "items": []}
                ch["sections"].append(cur)
            continue
        s = ln.strip()
        if not s or role in ("references", "how_to_use"):
            continue
        if role == "objectives":
            m = re.match(rf"^\d+\. \[{lp}\d+\] (.+)$", s)
            if m: ch["los"].append(m.group(1))
            elif not s.endswith(":"): ch["intro"].append(s)
        elif role == "takeaways" and s.startswith("- "):
            ch["takeaways"].append(s[2:])
        elif role == "assessment":
            m = re.match(rf"^\*\*{qp}(\d+)\.\*\* (.+?)(?: \[{lp}\d+\])?$", s)
            if m: ch["mcq"].append({"n": m.group(1), "q": m.group(2), "opts": []})
            elif re.match(rf"^[{letters}]\) ", s) and ch["mcq"]: ch["mcq"][-1]["opts"].append(s)
            elif case and re.match(rf"^\*\*{case}\*\*", s): ch["case"] = re.sub(rf"^\*\*{case}\*\*\s*", "", s)
            elif ch["case"]: ch["case"] += " " + s
        elif role == "answers":
            m = re.match(rf"^\*\*{qp}(\d+)\. ([{letters}])\*\* — (.+)$", s)
            if m: ch["answers"][m.group(1)] = (m.group(2), m.group(3))
            elif case and s.startswith("**" + book.case_label.rstrip(".")):
                ch["case_answer"] = s.split("**", 2)[2].strip()
        elif role == "core" and cur is not None:
            it = cur["items"]
            if s.startswith("|"):
                cells = [c.strip() for c in s.strip("|").split("|")]
                if all(re.fullmatch(r":?-+:?", c) for c in cells): continue
                if it and it[-1][0] == "table": it[-1][1].append(cells)
                else: it.append(["table", [cells]])
            elif s.startswith("![](fig:"):
                it.append(["fig", s[len("![](fig:"):-1]])
            elif s.startswith("> **"):
                m = re.match(r"^> \*\*(.+?):\*\* (.+)$", s)
                if m: it.append(["callout", book.callout_by_label.get(m.group(1), ""), m.group(1), m.group(2)])
            elif re.match(r"^(- |\d+\. )", s):
                txt = re.sub(r"^(- |\d+\. )", "", s)
                if it and it[-1][0] == "list": it[-1][1].append(txt)
                else: it.append(["list", [txt]])
            elif s.startswith("### "):
                it.append(["sub", s[4:]])
            elif s.startswith("*") and s.endswith("*") and not s.startswith("**"):
                it.append(["break"])                                # a table caption ends the table
            else:
                it.append(["para", s])
    return ch


def badge(src, dst, px=600):
    """A logo clipped to a circle and centred on a white disc: square logos show no corners, and every logo reads
    the same on dark or light slides."""
    im = Image.open(src).convert("RGBA")
    disc = Image.new("RGBA", (px, px), (0, 0, 0, 0))
    mask = Image.new("L", (px, px), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, px - 1, px - 1), fill=255)
    disc.paste(Image.new("RGBA", (px, px), (255, 255, 255, 255)), (0, 0), mask)
    inner = int(px * 0.94)
    im.thumbnail((inner, inner), Image.LANCZOS)
    clip = Image.new("L", im.size, 0)
    ImageDraw.Draw(clip).ellipse((0, 0, im.width - 1, im.height - 1), fill=255)
    im.putalpha(Image.composite(im.getchannel("A"), clip, clip))
    disc.alpha_composite(im, ((px - im.width) // 2, (px - im.height) // 2))
    disc.save(dst)
    return dst


class Deck:
    def __init__(self, book, style, ch, logos, figs, captions):
        self.b, self.st, self.ch, self.logos, self.figs, self.captions = book, style, ch, logos, figs, captions[0]
        self.alts = captions[1]
        self.prs = Presentation(); self.prs.slide_width, self.prs.slide_height = Inches(W_IN), Inches(H_IN)
        self.blank = self.prs.slide_layouts[6]
        self.num = f"{int(ch['num']):02d}"
        self.unit = f"{book.unit} {int(ch['num'])}"
        self.book_title = book.brief["identity"]["title"]
        self.pages, self.titles, self.kinds = [], [], []    # footer number boxes; per-slide title and layout kind

    # ---- primitives -------------------------------------------------------------------------------------------
    def runs(self, p, text, size, color=None, bold=False, font=None, italic=False, spacing=None):
        """Write text with **bold** spans into paragraph p."""
        for i, part in enumerate(re.split(r"\*\*", clean(text))):
            if not part:
                continue
            r = p.add_run(); r.text = part
            f = r.font
            f.size, f.name, f.italic = Pt(size), font or self.st.body, italic
            f.color.rgb = rgb(color or self.st.ink)
            f.bold = bold or i % 2 == 1
            if spacing:
                r._r.get_or_add_rPr().set("spc", str(spacing))

    def rect(self, s, x, y, w, h, fill, shape=MSO_SHAPE.RECTANGLE, radius=None):
        sh = s.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
        sh.fill.solid(); sh.fill.fore_color.rgb = rgb(fill); sh.line.fill.background(); sh.shadow.inherit = False
        if radius is not None and shape == MSO_SHAPE.ROUNDED_RECTANGLE:
            sh.adjustments[0] = radius
        return sh

    def text(self, s, x, y, w, h, anchor=MSO_ANCHOR.TOP):
        tf = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)).text_frame
        tf.word_wrap = True; tf.vertical_anchor = anchor
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        return tf

    def centred(self, shape, text, size, color, bold=True, font=None):
        tf = shape.text_frame; tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
        self.runs(p, text, size, color, bold, font)

    @staticmethod
    def height(text, w, size):
        """Estimated height (inches) of paragraphs at a font size in a box w inches wide."""
        per = max(int((w - 0.15) * 72 / (size * 0.52)), 1)          # conservative: matches the lint estimate
        return sum(max(1, -(-len(clean(t)) // per)) * size * 1.3 / 72 + 0.12 for t in text)

    def slide(self, notes="", dark=False):
        s = self.prs.slides.add_slide(self.blank)
        bg = s.background.fill; bg.solid(); bg.fore_color.rgb = rgb(self.st.pri if dark else self.st.bg)
        self.titles.append(""); self.kinds.append("anchor" if dark else "content")
        if notes and self.b.cfg.get("speaker_notes", True):
            s.notes_slide.notes_text_frame.text = clean(notes).replace("**", "")
        return s

    def footer(self, s, x=M, label=None):
        f = self.text(s, x, 7.02, 9, 0.3)
        self.runs(f.paragraphs[0], label or f"{self.book_title}  ·  {self.unit}  ·  {self.ch['title']}", 12, self.st.mut)
        n = self.text(s, 11.0, 7.02, 1.2, 0.3); n.paragraphs[0].alignment = PP_ALIGN.RIGHT
        self.pages.append((len(self.prs.slides), n))       # "05 / 24" filled in once the deck is complete
        if self.logos:
            self.alt(s.shapes.add_picture(str(self.logos[-1]), Inches(12.3), Inches(6.9), height=Inches(0.42)), "logo")

    @staticmethod
    def alt(pic, text):
        pic._element.nvPicPr.cNvPr.set("descr", text)
        return pic

    def content(self, kicker, title, notes="", kind="content"):
        """White content slide: number chip (the deck's motif), kicker, title, footer."""
        s = self.slide(notes)
        self.titles[-1], self.kinds[-1] = title, kind
        self.centred(self.rect(s, M, 0.52, 0.72, 0.72, self.st.acc, MSO_SHAPE.OVAL), self.num, 18, WHITE_HEX,
                     font=self.st.head)
        k = self.text(s, M + 0.95, 0.48, CW - 1, 0.32)
        self.runs(k.paragraphs[0], kicker.upper(), 12, self.st.acc, True, spacing=150)
        t = self.text(s, M + 0.95, 0.74, CW - 1, 0.7)
        self.runs(t.paragraphs[0], title, 32 if len(title) < 42 else 27, self.st.ink, True, self.st.head)
        self.footer(s)
        return s

    def rows(self, s, items, y=TOP, h=BOTTOM - TOP, x=M, w=CW, size=20, dark=False, start=1):
        """Numbered rows (a numbered disc beside each point) instead of plain bullets; the font shrinks, never
        below 15 pt, until the rows fit."""
        items = [i for i in items if i]
        if not items:
            return
        lines = lambda t, sz: max(1, -(-len(clean(t).replace("**", "")) // max(int((w - 0.65) * 72 / (sz * 0.5)), 1)))
        while size > 16 and sum(lines(t, size) * size * 1.25 / 72 + 0.22 for t in items) > h:
            size -= 1
        hs = [lines(t, size) * size * 1.25 / 72 + 0.22 for t in items]
        pad = min(0.35, (h - sum(hs)) / len(items)) if sum(hs) < h else 0
        yy = y
        for i, it in enumerate(items):
            d = self.rect(s, x, yy + 0.02, 0.44, 0.44, self.st.light if dark else self.st.acc_l, MSO_SHAPE.OVAL)
            self.centred(d, str(i + start), 13, self.st.pri if dark else self.st.acc)
            t = self.text(s, x + 0.65, yy + 0.04, w - 0.65, hs[i] + pad - 0.05)
            self.runs(t.paragraphs[0], it, size, WHITE_HEX if dark else self.st.ink)
            yy += hs[i] + pad

    def explain(self, s, text, x, y, w, h, size=18):
        tf = self.text(s, x, y, w, h)
        for i, para in enumerate(text):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph(); p.space_after = Pt(8)
            self.runs(p, para, size)

    def card(self, s, label, body, x, y, w, h, fill, tone, size=17):
        need = lambda sz: self.height([body], w - 0.6, sz) + 0.95   # long callouts: shrink to 18 pt, then grow the card
        while size > 18 and need(size) > h:
            size -= 1
        if need(size) > h:
            h = min(need(size), BOTTOM - TOP); y = min(y, BOTTOM - h)
        self.rect(s, x, y, w, h, fill, MSO_SHAPE.ROUNDED_RECTANGLE, 0.06)
        pill = self.rect(s, x + 0.3, y + 0.25, 0.3 + 0.125 * len(label), 0.38, tone, MSO_SHAPE.ROUNDED_RECTANGLE, 0.5)
        self.centred(pill, label.upper(), 12, WHITE_HEX)
        t = self.text(s, x + 0.3, y + 0.75, w - 0.6, h - 0.95)
        self.runs(t.paragraphs[0], body, size)

    def table(self, s, rows, y=TOP, h=BOTTOM - TOP, x=M, w=CW):
        nr, nc = len(rows), max(len(r) for r in rows)
        chars = sum(len(c) for r in rows for c in r)
        size = 20 if chars < 300 else 18 if chars < 550 else 16 if chars < 850 else 14 if chars < 1250 else 12
        # shrink until the wrapped rows fit the band
        lens = [min(max(len(r[j]) if j < len(r) else 0 for r in rows), 60) + 8 for j in range(nc)]
        cols = [w * n / sum(lens) - 0.24 for n in lens]              # real column widths, minus cell margins
        need = lambda sz: sum(max(1, max(-(-len(c) // max(int(cols[j] * 72 / (sz * 0.5)), 1))
                                         for j, c in enumerate(r[:nc]))) * sz * 1.25 / 72 + 0.12 for r in rows)
        while size > 12 and need(size) > h * 0.95:
            size -= 1
        rh = min(h / nr, 0.7)
        shape = s.shapes.add_table(nr, nc, Inches(x), Inches(y), Inches(w), Inches(rh * nr))
        tblPr = shape._element.graphic.graphicData.tbl.tblPr      # our own fills; no banding from the default style
        tblPr.set("bandRow", "0"); tblPr.set("firstRow", "0")
        tbl = shape.table
        for j in range(nc):
            tbl.columns[j].width = Emu(int(Inches(w) * lens[j] / sum(lens)))
        for i, r in enumerate(rows):
            tbl.rows[i].height = Inches(rh)
            for j in range(nc):
                cell = tbl.cell(i, j); cell.text = ""
                cell.fill.solid()
                cell.fill.fore_color.rgb = rgb(self.st.pri if i == 0 else (self.st.warm if i % 2 == 0 else WHITE_HEX))
                cell.margin_left = cell.margin_right = Inches(0.12)
                cell.margin_top = cell.margin_bottom = Inches(0.05)
                cell.vertical_anchor = MSO_ANCHOR.MIDDLE
                self.runs(cell.text_frame.paragraphs[0], r[j] if j < len(r) else "", size - (1 if i == 0 else 0),
                          WHITE_HEX if i == 0 else self.st.ink, i == 0 or (j == 0 and nc > 1))

    def split(self, label, glyph, body, notes, panel, tint, size=22):
        """Half-bleed panel on the left (large glyph + label), text on the right."""
        s = self.slide(notes)
        self.rect(s, 0, 0, 4.3, H_IN, panel)
        if glyph:
            g = self.text(s, M, 1.3, 3.2, 2.6)
            self.runs(g.paragraphs[0], glyph, 130, tint, True, self.st.head)
        k = self.text(s, M, 4.35, 3.3, 1.4)
        self.runs(k.paragraphs[0], label, 30, WHITE_HEX, True, self.st.head)
        self.runs(k.add_paragraph(), self.unit, 14, tint, True, spacing=150)
        t = self.text(s, 4.95, 0.9, 7.8, 5.6, MSO_ANCHOR.MIDDLE)
        self.runs(t.paragraphs[0], body, size if len(body) < 420 else size - 2 if len(body) < 620 else size - 4)
        self.footer(s, 4.95, f"{self.book_title}  ·  {self.ch['title']}")

    # ---- slides -----------------------------------------------------------------------------------------------
    def title_slide(self):
        st, design = self.st, (self.b.theme.get("cover") or {}).get("design") or {}
        s = self.slide(dark=True)
        big = self.text(s, 8.3, 1.2, 5.2, 5.6, MSO_ANCHOR.MIDDLE); big.paragraphs[0].alignment = PP_ALIGN.RIGHT
        self.runs(big.paragraphs[0], self.num, 280, st.pri_d, True, st.head)
        for k, lg in enumerate(self.logos):
            s.shapes.add_picture(str(lg), Inches(M + k * 1.25), Inches(0.55), height=Inches(1.05))
        inst = [x.strip() for x in (design.get("institution") or "").split(",", 1)]
        if inst[0]:
            tf = self.text(s, M + 1.25 * len(self.logos) + 0.15, 0.72, 7, 0.8, MSO_ANCHOR.MIDDLE)
            self.runs(tf.paragraphs[0], inst[0], 18, WHITE_HEX, True, st.head)
            if len(inst) > 1:
                self.runs(tf.add_paragraph(), inst[1].upper(), 12, st.light, True, spacing=200)
        t = self.text(s, M, 2.75, 7.4, 3.4)
        self.runs(t.paragraphs[0], f"{self.book_title}  ·  {self.unit}".upper(), 14, st.light, True, spacing=200)
        p = t.add_paragraph(); p.space_before = Pt(14)
        self.runs(p, self.ch["title"], 44 if len(self.ch["title"]) < 30 else 36, WHITE_HEX, True, st.head)
        sub = self.b.brief["identity"].get("subtitle")
        if sub:
            p = t.add_paragraph(); p.space_before = Pt(16)
            self.runs(p, sub, 20, st.light, italic=True, font=st.head)
        facts = self.facts()
        if facts:
            f = self.text(s, M, 6.55, 9, 0.5)
            self.runs(f.paragraphs[0], "  ·  ".join(f"{a} {b}" for a, b in facts), 13, st.light)

    def facts(self):
        out = []
        if self.b.cfg.get("minutes"):
            out.append((str(self.b.cfg["minutes"]), "minutes"))
        if self.ch["mcq"]:
            out.append((str(len(self.ch["mcq"])), "questions"))
        if self.ch["case"]:
            out.append(("1", self.b.case_label.rstrip(".").lower() or "case"))
        return out

    def objectives(self):
        label = next((x["label"] for x in self.b.template["sections"] if x["role"] == "objectives"), "Objectives")
        s = self.content(self.unit, label, " ".join(self.ch["intro"]))
        facts = self.facts()
        self.rows(s, self.ch["los"], w=7.9 if facts else CW, size=21)
        if facts:
            self.rect(s, 9.15, 1.75, 3.58, 4.95, self.st.warm, MSO_SHAPE.ROUNDED_RECTANGLE, 0.05)
            tf = self.text(s, 9.45, 2.05, 3.0, 4.4)
            for i, (big, small) in enumerate(facts):
                p = tf.paragraphs[0] if i == 0 else tf.add_paragraph(); p.space_before = Pt(0 if i == 0 else 16)
                self.runs(p, big, 54, self.st.pri, True, self.st.head)
                self.runs(tf.add_paragraph(), small.upper(), 12, self.st.mut, True, spacing=150)

    def agenda(self):
        """Roadmap of the core sections."""
        titles = [x["title"] for x in self.ch["sections"]]
        if len(titles) < 2 or not self.b.cfg.get("agenda", True):
            return
        s = self.content(self.unit, "Roadmap", "What we will cover, in order.", "agenda")
        two = len(titles) > 4
        half = -(-len(titles) // 2) if two else len(titles)
        self.rows(s, titles[:half], w=CW / 2 - 0.3 if two else CW, size=22)
        if two:
            self.rows(s, titles[half:], x=M + CW / 2 + 0.3, w=CW / 2 - 0.3, size=22, start=half + 1)

    def chunks(self, items):
        """Pair each visual (figure, table, list) with the paragraphs written just before it; trailing paragraphs
        join the last visual. A subheading titles the visuals under it."""
        out, pend, sub = [], [], None
        for it in items:
            if it[0] == "para":
                pend.append(it[1])
            elif it[0] == "sub":
                sub = it[1]
            elif it[0] in ("fig", "table", "list"):
                if it[0] == "fig" and it[1] not in self.figs:
                    continue
                out.append({"kind": it[0], "data": it[1], "text": pend, "sub": sub}); pend = []
        if pend:
            if out: out[-1]["text"] = out[-1]["text"] + pend
            else: out.append({"kind": "prose", "data": None, "text": pend, "sub": sub})
        return out

    def visual(self, s, c, x, y, w, h):
        if c["kind"] == "fig":
            pic = self.alt(s.shapes.add_picture(str(self.figs[c["data"]]), Inches(x), Inches(y), width=Inches(w)),
                           self.alts.get(c["data"], self.captions.get(c["data"], "")))
            if pic.height > Inches(h - 0.45):
                pic.width = int(pic.width * Inches(h - 0.45) / pic.height); pic.height = Inches(h - 0.45)
            pic.left = Inches(x) + int((Inches(w) - pic.width) / 2)
            cap = self.text(s, x, y + pic.height / 914400 + 0.1, w, 0.4); cap.paragraphs[0].alignment = PP_ALIGN.CENTER
            self.runs(cap.paragraphs[0], self.captions.get(c["data"], ""), 13, self.st.mut, italic=True)
        elif c["kind"] == "table":
            self.table(s, c["data"], y=y, h=h, x=x, w=w)
        elif c["kind"] == "list":
            self.rows(s, c["data"], y=y, h=h, x=x, w=w, size=21)

    @staticmethod
    def pages_of(seq, n):
        return [seq[i:i + n] for i in range(0, len(seq), n)] or [seq]

    def split_chunk(self, c):
        """Density caps: 6 points per list slide, 8 rows per table slide (header repeated), 5 prose points."""
        if c["kind"] == "list" and len(c["data"]) > 6:
            parts = self.pages_of(c["data"], 6)
        elif c["kind"] == "table" and len(c["data"]) > 8:
            parts = [[c["data"][0]] + p for p in self.pages_of(c["data"][1:], 7)]
        elif c["kind"] == "prose" and len(c["text"]) > 5:
            parts = self.pages_of(c["text"], 5)
        else:
            return [c]
        out = []
        for i, part in enumerate(parts):
            d = dict(c, text=c["text"] if i == 0 else [], suffix=f" ({i + 1}/{len(parts)})")
            if c["kind"] == "prose":
                d["text"] = part
            else:
                d["data"] = part
            out.append(d)
        return out

    def section(self, sec):
        items = sec["items"]
        notes = " ".join(i[1] for i in items if i[0] == "para")
        feature = self.b.cfg.get("feature_callout")
        for c in (x for ch in self.chunks(items) for x in self.split_chunk(ch)):
            title = (c["sub"] or sec["title"]) + c.get("suffix", "")
            text = c["text"] if self.b.cfg.get("explain_on_slide", True) else []
            s = self.content(self.unit, title, notes, "dense" if c["kind"] == "table" else c["kind"])
            if c["kind"] == "prose":                      # explanation only: paragraphs as numbered points
                self.rows(s, c["text"] if text else [re.split(r"(?<=[.!?])\s", t)[0] for t in c["text"]], size=21)
                continue
            if not text:
                self.visual(s, c, M, TOP, CW, BOTTOM - TOP); continue
            wide = c["kind"] == "table" and max(len(r) for r in c["data"]) >= 3
            lead = self.height(text, CW, 18)
            load = sum(len(t) for t in text) + sum(len(x) for r in (c["data"] if c["kind"] in ("table", "list") else [])
                                                   for x in (r if isinstance(r, list) else [r]))
            if load > 850 and sum(len(t) for t in text) > 300:   # density cap: a long explanation takes its own slide
                lead = 99
            if lead <= 1.5:                               # short explanation above the visual
                self.explain(s, text, M, TOP, CW, lead + 0.1, 18)
                self.visual(s, c, M, TOP + lead + 0.3, CW, BOTTOM - TOP - lead - 0.3)
            elif lead != 99 and not wide and self.height(text, 4.9, 17) <= BOTTOM - TOP:   # explanation column beside the visual
                self.explain(s, text, M, TOP, 4.9, BOTTOM - TOP, 17)
                self.visual(s, c, M + 5.3, TOP, CW - 5.3, BOTTOM - TOP)
            else:                                         # long explanation on its own slide(s), visual next
                self.kinds[-1] = "text"
                groups, cur = [], []
                for para in text:                          # never below 18 pt: overflow goes to another slide
                    if cur and self.height(cur + [para], CW, 18) > BOTTOM - TOP:
                        groups.append(cur); cur = []
                    cur.append(para)
                groups.append(cur)
                for gi, g in enumerate(groups):
                    if gi:
                        s = self.content(self.unit, title, notes, "text")
                    fits = self.height(g, CW, 21) <= BOTTOM - TOP
                    self.explain(s, g, M, TOP, CW, BOTTOM - TOP, 21 if fits else 18)
                self.visual(self.content(self.unit, title, notes, "dense" if c["kind"] == "table" else c["kind"]),
                            c, M, TOP, CW, BOTTOM - TOP)
        for c in (i for i in items if i[0] == "callout" and i[1] != feature):
            s = self.content(self.unit, sec["title"], notes)
            fill, tone = self.st.tone(c[1])
            self.card(s, c[2], c[3], M + 1.2, 2.3, CW - 2.4, 2.6, fill, tone, 26)
        for c in (i for i in items if i[0] == "callout" and feature and i[1] == feature):
            self.split(c[2], self.b.cfg.get("feature_glyph", c[2][:1]), c[3],
                       "Discuss with the class: what would you ask, check and say?", self.st.acc, self.st.acc_l)

    def mcq(self, q):
        key, why = self.ch["answers"].get(q["n"], ("", ""))
        total = len(self.ch["mcq"])
        st = self.st
        for reveal in (False, True):
            kick = f"{self.unit}  ·  question {q['n']} of {total}" + ("  ·  answer" if reveal else "")
            s = self.content(kick, "Check your answer" if reveal else "Your turn", "" if reveal else f"Answer {key}: {why}")
            t = self.text(s, M, 1.7, CW, 1.1)
            self.runs(t.paragraphs[0], q["q"], 24 if len(q["q"]) < 120 else 21, st.ink, True)
            top, gap = (2.85, 0.74) if reveal else (2.95, 0.84)
            for k, o in enumerate(q["opts"]):
                letter, body = o[0], o[3:]
                hit, faded = reveal and letter == key, reveal and letter != key
                self.rect(s, M, top + k * gap, CW, gap - 0.14, st.acc if hit else (st.faded if faded else st.warm),
                          MSO_SHAPE.ROUNDED_RECTANGLE, 0.18)
                d = self.rect(s, M + 0.18, top + k * gap + (gap - 0.6) / 2, 0.46, 0.46,
                              WHITE_HEX if hit else (st.faded_disc if faded else st.pri), MSO_SHAPE.OVAL)
                self.centred(d, letter, 15, st.acc if hit else (st.mut if faded else WHITE_HEX))
                b = self.text(s, M + 0.9, top + k * gap, CW - 1.1, gap - 0.14, MSO_ANCHOR.MIDDLE)
                self.runs(b.paragraphs[0], body, 19, WHITE_HEX if hit else (st.mut if faded else st.ink), hit)
            if reveal and why:
                r = self.text(s, M, top + len(q["opts"]) * gap + 0.05, CW, 0.75)
                self.runs(r.paragraphs[0], "Why:  ", 15, st.acc, True); self.runs(r.paragraphs[0], why, 15, st.ink)

    def closing(self):
        label = next((x["label"] for x in self.b.template["sections"] if x["role"] == "takeaways"), "Key Takeaways")
        s = self.slide(dark=True)
        k = self.text(s, M, 0.55, 8, 0.4)
        self.runs(k.paragraphs[0], f"{self.unit}  ·  summary".upper(), 13, self.st.light, True, spacing=200)
        t = self.text(s, M, 0.9, 10, 0.8)
        self.runs(t.paragraphs[0], label, 36, WHITE_HEX, True, self.st.head)
        self.rows(s, self.ch["takeaways"], y=2.0, h=4.6, size=21, dark=True)
        for i, lg in enumerate(self.logos):
            s.shapes.add_picture(str(lg), Inches(12.07 - 0.72 * (len(self.logos) - 1 - i)), Inches(6.72), height=Inches(0.6))

    def build(self):
        self.title_slide()
        self.objectives()
        self.agenda()
        for sec in self.ch["sections"]:
            self.section(sec)
        for q in self.ch["mcq"] if self.b.cfg.get("mcq_slides", True) else []:
            self.mcq(q)
        if self.ch["case"]:
            self.split(self.b.case_label.rstrip("."), self.b.cfg.get("case_glyph", "?"), self.ch["case"],
                       "Model answer: " + self.ch["case_answer"], self.st.pri, self.st.warm2)
        if self.ch["takeaways"]:
            self.closing()
        self.finish()
        return self.prs

    def finish(self):
        n = len(self.prs.slides)
        for i, tf in self.pages:
            self.runs(tf.paragraphs[0], f"{i:02d} / {n:02d}", 12, self.st.mut, True)
        if not self.b.cfg.get("speaker_notes", True):
            return
        for i, s in enumerate(self.prs.slides):          # notes: talking points, then timing and the next slide
            nf = s.notes_slide.notes_text_frame
            words = len(nf.text.split()) + sum(len(sh.text_frame.text.split()) for sh in s.shapes if sh.has_text_frame)
            nxt = next((t for t in self.titles[i + 1:] if t), "")
            tail = f"About {max(1, round(words / 140 * 2)) * 30} s." + (f"  Next: {nxt}." if nxt else "")
            nf.text = (nf.text + "\n\n" if nf.text else "") + tail


PLACEHOLDER = re.compile(r"\bx{3,}\b|lorem|ipsum|placeholder|\bTODO\b", re.I)


def lint(prs, kinds):
    """Deck QA distilled from the slide skills: text overflow (>15% over its box), font floor (<12 pt), contrast
    (<4.5:1; <3:1 at 24 pt and up), placeholder text, density (>900 characters) and three dense/text/list slides in
    a row."""
    issues = []
    for i, s in enumerate(prs.slides, 1):
        bg = str(s.background.fill.fore_color.rgb) if s.background.fill.type == 1 else WHITE_HEX
        chars, filled = 0, []
        for sh in s.shapes:
            own = sh.fill.type == 1 if hasattr(sh, "fill") else False
            if own:
                filled.append(sh)
            if not sh.has_text_frame or not sh.text_frame.text.strip():
                continue
            cx, cy = sh.left + sh.width / 2, sh.top + sh.height / 2
            under = [f for f in filled if f is not sh and f.left <= cx <= f.left + f.width and f.top <= cy <= f.top + f.height]
            fill = str(sh.fill.fore_color.rgb) if own else (str(under[-1].fill.fore_color.rgb) if under else bg)
            need = 0.0
            for p in sh.text_frame.paragraphs:
                size = max((r.font.size.pt for r in p.runs if r.font.size), default=18)
                text = "".join(r.text for r in p.runs)
                chars += len(text)
                per = max(int((sh.width / 914400 - 0.1) * 72 / (size * 0.5)), 1)
                need += max(1, -(-len(text) // per)) * size * 1.2 / 72
                for r in p.runs:
                    if not r.text.strip():
                        continue
                    if r.font.size and r.font.size.pt < 12:
                        issues.append((i, "font", f"{r.font.size.pt:.0f} pt: {r.text[:30]}"))
                    try:
                        col = str(r.font.color.rgb)
                    except AttributeError:
                        col = None
                    decorative = r.font.size and r.font.size.pt >= 100      # tone-on-tone numerals and glyphs
                    if col and not decorative:
                        ratio = contrast(col, fill)
                        if ratio < (3 if (r.font.size and r.font.size.pt >= 24) else 4.45):
                            issues.append((i, "contrast", f"{ratio:.1f}:1 {r.text[:30]}"))
                if PLACEHOLDER.search(text):
                    issues.append((i, "placeholder", text[:40]))
            box = sh.height / 914400
            if sh.shape_type == 17 and box > 0.35 and need > box * 1.15:
                issues.append((i, "overflow", f"{need:.2f}in of text in a {box:.2f}in box"))
        if chars > 900:
            issues.append((i, "density", f"{chars} characters"))
    for i in range(2, len(kinds)):
        if kinds[i] == kinds[i - 1] == kinds[i - 2] and kinds[i] in ("dense", "text", "list"):
            issues.append((i + 1, "rhythm", f"3 {kinds[i]} slides in a row"))
    return issues


def main(project):
    book = Book(project)
    style = Style(book.theme, book.cfg)
    p = book.project
    fig_dir = p / "figures" / "out"
    figs = {f.stem: f for f in fig_dir.glob("*.png")} if fig_dir.is_dir() else {}
    fj = p / "figures" / "figures.json"
    figdoc = json.loads(fj.read_text(encoding="utf-8"))["figures"] if fj.is_file() else []
    captions = ({f["id"]: f["caption"] for f in figdoc}, {f["id"]: f.get("alt") or f["caption"] for f in figdoc})
    out = p / (book.cfg.get("out_dir") or "slides"); out.mkdir(exist_ok=True)
    assets = out / "_assets"; assets.mkdir(exist_ok=True)
    logos = [badge(p / rel, assets / pathlib.Path(rel).name)
             for rel in ((book.theme.get("cover") or {}).get("design") or {}).get("logos") or []]
    chapters = p / book.template["paths"]["chapters"]   # plan entries name files inside it
    status, report = 0, {}
    for c in book.plan["chapters"]:
        ch = parse((chapters / c["file"]).read_text(encoding="utf-8"), book)
        deck = Deck(book, style, ch, logos, figs, captions)
        prs = deck.build()
        report[c["file"]] = [{"slide": i, "check": k, "detail": d} for i, k, d in lint(prs, deck.kinds)]
        path = out / (pathlib.Path(c["file"]).stem + ".pptx")
        try:
            prs.save(path)
        except PermissionError:                      # the deck is open in PowerPoint
            print(f"{path.name}: SKIPPED, file is open; close it and run again"); status = 1; continue
        counts = {}
        for x in report[c["file"]]:
            counts[x["check"]] = counts.get(x["check"], 0) + 1
        print(f"{path.name}: {len(prs.slides)} slides  QA: {counts or 'clean'}")
    (out / "qa-report.json").write_text(json.dumps(report, indent=1, ensure_ascii=False), encoding="utf-8")
    return status


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
    from harness.gate import enforce
    PROJECT = enforce("build", sys.argv, content_only=True)   # read-only side product (DEC-H01)
    sys.exit(main(PROJECT))
