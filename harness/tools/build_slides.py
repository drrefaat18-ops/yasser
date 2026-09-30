"""Teaching slide decks (.pptx), one per chapter, from the reworked chapters. Gate: build.

Usage: python harness/tools/build_slides.py --project projects/<book>
Output: <project>/<slides.out_dir, default "slides">/<chapter-file>.pptx, plus _assets/ (logo badges).

Everything book-specific comes from the project (Rule 8): palette, callout colours, cover logos and institution
(theme.json); chapter heading, section labels, callout syntax, MCQ letters and case label (template.json); title
(brief.json); and the optional slides.json:

    {"out_dir": "slides", "unit_label": "Section", "minutes": 45,
     "mcq_slides": true, "explain_on_slide": true, "speaker_notes": true,
     "feature_callout": "<callout id shown on a half-bleed panel>", "feature_glyph": "<one character>",
     "case_glyph": "?", "fonts": {"head": "Cambria", "body": "Calibri"}}

Deck: title; objectives with a stat card; per core section, each figure/table/list with the explanation that
precedes it in the chapter (above the visual when short, beside it, or on its own slide first when long); callout
cards; the feature callout on a half-bleed panel; one question slide and one answer slide per MCQ; the case (model
answer in the notes); key takeaways on a dark closing slide. Section prose is also kept in the speaker notes.
Lessons behind these rules: docs/harness/SLIDES.md.
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
        self.pri_d = mix(self.pri, "000000", 0.15)                 # tone-on-tone numeral on the dark slides
        self.light = mix(self.pri, WHITE_HEX, 0.86)                # light text on the primary colour
        self.warm = mix(self.pri, WHITE_HEX, 0.94)                 # zebra rows, cards
        self.warm2 = mix(self.pri, WHITE_HEX, 0.85)
        self.acc_l = mix(self.acc, WHITE_HEX, 0.88)
        self.faded = mix(self.mut, WHITE_HEX, 0.93)
        self.faded_disc = mix(self.mut, WHITE_HEX, 0.80)
        fonts = slides_cfg.get("fonts") or {}
        self.head, self.body = fonts.get("head", "Cambria"), fonts.get("body", "Calibri")   # ship with Office
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
        self.b, self.st, self.ch, self.logos, self.figs, self.captions = book, style, ch, logos, figs, captions
        self.prs = Presentation(); self.prs.slide_width, self.prs.slide_height = Inches(W_IN), Inches(H_IN)
        self.blank = self.prs.slide_layouts[6]
        self.num = f"{int(ch['num']):02d}"
        self.unit = f"{book.unit} {int(ch['num'])}"
        self.book_title = book.brief["identity"]["title"]

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
        per = max(int(w * 72 / (size * 0.5)), 1)
        return sum(max(1, -(-len(clean(t)) // per)) * size * 1.3 / 72 + 0.12 for t in text)

    def slide(self, notes="", dark=False):
        s = self.prs.slides.add_slide(self.blank)
        bg = s.background.fill; bg.solid(); bg.fore_color.rgb = rgb(self.st.pri if dark else WHITE_HEX)
        if notes and self.b.cfg.get("speaker_notes", True):
            s.notes_slide.notes_text_frame.text = clean(notes).replace("**", "")
        return s

    def footer(self, s, x=M, label=None):
        f = self.text(s, x, 7.02, 9, 0.3)
        self.runs(f.paragraphs[0], label or f"{self.book_title}  ·  {self.unit}  ·  {self.ch['title']}", 10, self.st.mut)
        n = self.text(s, 11.4, 7.02, 0.8, 0.3); n.paragraphs[0].alignment = PP_ALIGN.RIGHT
        self.runs(n.paragraphs[0], str(len(self.prs.slides)), 10, self.st.mut, True)
        if self.logos:
            s.shapes.add_picture(str(self.logos[-1]), Inches(12.3), Inches(6.9), height=Inches(0.42))

    def content(self, kicker, title, notes=""):
        """White content slide: number chip (the deck's motif), kicker, title, footer."""
        s = self.slide(notes)
        self.centred(self.rect(s, M, 0.52, 0.72, 0.72, self.st.acc, MSO_SHAPE.OVAL), self.num, 18, WHITE_HEX,
                     font=self.st.head)
        k = self.text(s, M + 0.95, 0.48, CW - 1, 0.32)
        self.runs(k.paragraphs[0], kicker.upper(), 12, self.st.acc, True, spacing=150)
        t = self.text(s, M + 0.95, 0.74, CW - 1, 0.7)
        self.runs(t.paragraphs[0], title, 32 if len(title) < 42 else 27, self.st.ink, True, self.st.head)
        self.footer(s)
        return s

    def rows(self, s, items, y=TOP, h=BOTTOM - TOP, x=M, w=CW, size=20, dark=False):
        """Numbered rows (a numbered disc beside each point) instead of plain bullets; the font shrinks, never
        below 15 pt, until the rows fit."""
        items = [i for i in items if i]
        if not items:
            return
        lines = lambda t, sz: max(1, -(-len(clean(t).replace("**", "")) // max(int((w - 0.65) * 72 / (sz * 0.5)), 1)))
        while size > 15 and sum(lines(t, size) * size * 1.25 / 72 + 0.22 for t in items) > h:
            size -= 1
        hs = [lines(t, size) * size * 1.25 / 72 + 0.22 for t in items]
        pad = min(0.35, (h - sum(hs)) / len(items)) if sum(hs) < h else 0
        yy = y
        for i, it in enumerate(items):
            d = self.rect(s, x, yy + 0.02, 0.44, 0.44, self.st.light if dark else self.st.acc_l, MSO_SHAPE.OVAL)
            self.centred(d, str(i + 1), 13, self.st.pri if dark else self.st.acc)
            t = self.text(s, x + 0.65, yy + 0.04, w - 0.65, hs[i] + pad - 0.05)
            self.runs(t.paragraphs[0], it, size, WHITE_HEX if dark else self.st.ink)
            yy += hs[i] + pad

    def explain(self, s, text, x, y, w, h, size=18):
        tf = self.text(s, x, y, w, h)
        for i, para in enumerate(text):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph(); p.space_after = Pt(8)
            self.runs(p, para, size)

    def card(self, s, label, body, x, y, w, h, fill, tone, size=17):
        self.rect(s, x, y, w, h, fill, MSO_SHAPE.ROUNDED_RECTANGLE, 0.06)
        pill = self.rect(s, x + 0.3, y + 0.25, 0.25 + 0.105 * len(label), 0.34, tone, MSO_SHAPE.ROUNDED_RECTANGLE, 0.5)
        self.centred(pill, label.upper(), 10.5, WHITE_HEX)
        t = self.text(s, x + 0.3, y + 0.75, w - 0.6, h - 0.95)
        self.runs(t.paragraphs[0], body, size)

    def table(self, s, rows, y=TOP, h=BOTTOM - TOP, x=M, w=CW):
        nr, nc = len(rows), max(len(r) for r in rows)
        chars = sum(len(c) for r in rows for c in r)
        size = 20 if chars < 300 else 18 if chars < 550 else 16 if chars < 850 else 14 if chars < 1250 else 12
        # shrink until the wrapped rows fit the band
        need = lambda sz: sum(max(1, max(-(-len(c) // max(int((w / nc) * 72 / (sz * 0.5)), 1)) for c in r)) * sz * 1.25 / 72 + 0.12 for r in rows)
        while size > 11 and need(size) > h * 0.85:
            size -= 1
        rh = min(h / nr, 0.7)
        shape = s.shapes.add_table(nr, nc, Inches(x), Inches(y), Inches(w), Inches(rh * nr))
        tblPr = shape._element.graphic.graphicData.tbl.tblPr      # our own fills; no banding from the default style
        tblPr.set("bandRow", "0"); tblPr.set("firstRow", "0")
        tbl = shape.table
        lens = [min(max(len(r[j]) if j < len(r) else 0 for r in rows), 60) + 8 for j in range(nc)]
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
            pic = s.shapes.add_picture(str(self.figs[c["data"]]), Inches(x), Inches(y), width=Inches(w))
            if pic.height > Inches(h - 0.45):
                pic.width = int(pic.width * Inches(h - 0.45) / pic.height); pic.height = Inches(h - 0.45)
            pic.left = Inches(x) + int((Inches(w) - pic.width) / 2)
            cap = self.text(s, x, y + pic.height / 914400 + 0.1, w, 0.4); cap.paragraphs[0].alignment = PP_ALIGN.CENTER
            self.runs(cap.paragraphs[0], self.captions.get(c["data"], ""), 13, self.st.mut, italic=True)
        elif c["kind"] == "table":
            self.table(s, c["data"], y=y, h=h, x=x, w=w)
        elif c["kind"] == "list":
            self.rows(s, c["data"][:7], y=y, h=h, x=x, w=w, size=21)

    def section(self, sec):
        items = sec["items"]
        notes = " ".join(i[1] for i in items if i[0] == "para")
        feature = self.b.cfg.get("feature_callout")
        for c in self.chunks(items):
            title, text = c["sub"] or sec["title"], c["text"] if self.b.cfg.get("explain_on_slide", True) else []
            s = self.content(self.unit, title, notes)
            if c["kind"] == "prose":                      # explanation only: paragraphs as numbered points
                self.rows(s, c["text"] if text else [re.split(r"(?<=[.!?])\s", t)[0] for t in c["text"]], size=21)
                continue
            if not text:
                self.visual(s, c, M, TOP, CW, BOTTOM - TOP); continue
            wide = c["kind"] == "table" and max(len(r) for r in c["data"]) >= 3
            lead = self.height(text, CW, 18)
            if lead <= 1.5:                               # short explanation above the visual
                self.explain(s, text, M, TOP, CW, lead + 0.1, 18)
                self.visual(s, c, M, TOP + lead + 0.3, CW, BOTTOM - TOP - lead - 0.3)
            elif not wide and self.height(text, 4.9, 17) <= BOTTOM - TOP:   # explanation column beside the visual
                self.explain(s, text, M, TOP, 4.9, BOTTOM - TOP, 17)
                self.visual(s, c, M + 5.3, TOP, CW - 5.3, BOTTOM - TOP)
            else:                                         # long explanation on its own slide, visual next
                fits = self.height(text, CW, 21) <= BOTTOM - TOP
                self.explain(s, text, M, TOP, CW, BOTTOM - TOP, 21 if fits else 18)
                self.visual(self.content(self.unit, title, notes), c, M, TOP, CW, BOTTOM - TOP)
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
        for sec in self.ch["sections"]:
            self.section(sec)
        for q in self.ch["mcq"] if self.b.cfg.get("mcq_slides", True) else []:
            self.mcq(q)
        if self.ch["case"]:
            self.split(self.b.case_label.rstrip("."), self.b.cfg.get("case_glyph", "?"), self.ch["case"],
                       "Model answer: " + self.ch["case_answer"], self.st.pri, self.st.warm2)
        if self.ch["takeaways"]:
            self.closing()
        return self.prs


def main(project):
    book = Book(project)
    style = Style(book.theme, book.cfg)
    p = book.project
    fig_dir = p / "figures" / "out"
    figs = {f.stem: f for f in fig_dir.glob("*.png")} if fig_dir.is_dir() else {}
    fj = p / "figures" / "figures.json"
    captions = {f["id"]: f["caption"] for f in json.loads(fj.read_text(encoding="utf-8"))["figures"]} if fj.is_file() else {}
    out = p / (book.cfg.get("out_dir") or "slides"); out.mkdir(exist_ok=True)
    assets = out / "_assets"; assets.mkdir(exist_ok=True)
    logos = [badge(p / rel, assets / pathlib.Path(rel).name)
             for rel in ((book.theme.get("cover") or {}).get("design") or {}).get("logos") or []]
    chapters = p / book.template["paths"]["chapters"]   # plan entries name files inside it
    status = 0
    for c in book.plan["chapters"]:
        ch = parse((chapters / c["file"]).read_text(encoding="utf-8"), book)
        prs = Deck(book, style, ch, logos, figs, captions).build()
        path = out / (pathlib.Path(c["file"]).stem + ".pptx")
        try:
            prs.save(path)
        except PermissionError:                      # the deck is open in PowerPoint
            print(f"{path.name}: SKIPPED, file is open; close it and run again"); status = 1; continue
        print(f"{path.name}: {len(prs.slides)} slides")
    return status


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
    from harness.gate import enforce
    PROJECT = enforce("build", sys.argv)
    sys.exit(main(PROJECT))
