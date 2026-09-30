"""Build one PowerPoint deck per chapter from the reworked chapters (teaching slides for 45-minute sections).

Usage: python projects/drug-information-practical/tools/make_slides.py --project projects/drug-information-practical
Output: slides/<chapter-file>.pptx
Each deck: title, objectives, one slide per core section (its figure, main table or key points), At the Pharmacy,
one question slide and one answer slide per MCQ, the practice case, and the key takeaways. Section prose goes into
the speaker notes.

Design: dark terracotta title and closing slides, white content slides; the motif is a petrol number chip beside
every title. Fonts are Office-safe (Cambria headings, Calibri body) so the deck renders the same on any PC.
"""
import json, re, pathlib
from PIL import Image, ImageDraw
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

C = lambda h: RGBColor.from_string(h)
PRI, PRI_D, ACC, ACC_L, INK, MUT, WHITE = (C(x) for x in ("A4472B", "8C3A22", "2F6F7A", "E0EEF0", "2B211C", "6E625B", "FFFFFF"))
WARM, WARM_2, CREAM, RED, RED_L = (C(x) for x in ("FBF3EE", "F6E5DE", "F3E6D8", "B3261E", "FBEAEA"))
HEAD, BODY = "Cambria", "Calibri"
W, H = Inches(13.333), Inches(7.5)
M = 0.6                     # side margin, inches
CW = 13.333 - 2 * M         # content width


def clean(t):
    t = re.sub(r"\s*\[(\d+(?:\s*[,–-]\s*\d+)*)\]", "", t)          # drop citations
    t = re.sub(r"\^([^^]+)\^", r"\1", t)
    return re.sub(r"(?<!\*)\*(?!\*)", "", t)


def runs(p, text, size, color=INK, bold=False, font=BODY, italic=False, spacing=None):
    """Write text with **bold** spans into paragraph p."""
    for i, part in enumerate(re.split(r"\*\*", clean(text))):
        if not part:
            continue
        r = p.add_run(); r.text = part
        f = r.font
        f.size, f.name, f.color.rgb, f.italic = Pt(size), font, color, italic
        f.bold = bold or i % 2 == 1
        if spacing:
            r._r.get_or_add_rPr().set("spc", str(spacing))


def parse(md):
    ch = {"title": "", "num": "", "los": [], "sections": [], "takeaways": [], "mcq": [], "case": "", "case_answer": "",
          "answers": {}, "intro": []}
    cur, block = None, None
    for ln in md.splitlines():
        m = re.match(r"^# Chapter (\d+): (.+)$", ln)
        if m:
            ch["num"], ch["title"] = m.groups(); continue
        if ln.startswith("## "):
            name = ln[3:].strip()
            block = {"In This Section": "los", "Key Takeaways": "take", "Self-Assessment": "sa",
                     "Answers and Rationales": "ans", "References": "refs"}.get(name, "sec")
            if block == "sec":
                cur = {"title": re.sub(r"^\d+\.\d+\s*", "", name), "items": []}
                ch["sections"].append(cur)
            continue
        s = ln.strip()
        if not s or block == "refs":
            continue
        if block == "los":
            m = re.match(r"^\d+\. \[LO\d+\] (.+)$", s)
            if m: ch["los"].append(m.group(1))
            elif not s.startswith("By the end"): ch["intro"].append(s)
        elif block == "take" and s.startswith("- "):
            ch["takeaways"].append(s[2:])
        elif block == "sa":
            m = re.match(r"^\*\*Q(\d+)\.\*\* (.+?)(?: \[LO\d+\])?$", s)
            if m: ch["mcq"].append({"n": m.group(1), "q": m.group(2), "opts": []})
            elif re.match(r"^[A-D]\) ", s): ch["mcq"][-1]["opts"].append(s)
            elif s.startswith("**Practice Case.**"): ch["case"] = s.replace("**Practice Case.**", "").strip()
            elif ch["case"]: ch["case"] += " " + s
        elif block == "ans":
            m = re.match(r"^\*\*Q(\d+)\. ([A-D])\*\* — (.+)$", s)
            if m: ch["answers"][m.group(1)] = (m.group(2), m.group(3))
            elif s.startswith("**Practice Case — model answer.**"):
                ch["case_answer"] = s.split("**", 2)[2].strip()
        elif block == "sec" and cur is not None:
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
                if m: it.append(["callout", m.group(1), m.group(2)])
            elif re.match(r"^(- |\d+\. )", s):
                txt = re.sub(r"^(- |\d+\. )", "", s)
                if it and it[-1][0] == "list": it[-1][1].append(txt)
                else: it.append(["list", [txt]])
            elif s.startswith("*Table") or s.startswith("### "):
                it.append(["sub", s[4:]] if s.startswith("### ") else ["break"])
            else:
                it.append(["para", s])
    return ch


def badge(src, dst, px=600):
    """A logo centred on a white disc, so every logo reads the same on dark or light slides."""
    im = Image.open(src).convert("RGBA")
    disc = Image.new("RGBA", (px, px), (0, 0, 0, 0))
    mask = Image.new("L", (px, px), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, px - 1, px - 1), fill=255)
    disc.paste(Image.new("RGBA", (px, px), (255, 255, 255, 255)), (0, 0), mask)
    inner = int(px * 0.94)
    im.thumbnail((inner, inner), Image.LANCZOS)
    clip = Image.new("L", im.size, 0)            # clip the logo to its inscribed circle: square corners never show
    ImageDraw.Draw(clip).ellipse((0, 0, im.width - 1, im.height - 1), fill=255)
    im.putalpha(Image.composite(im.getchannel("A"), clip, clip))
    disc.alpha_composite(im, ((px - im.width) // 2, (px - im.height) // 2))
    disc.save(dst)
    return dst


class Deck:
    def __init__(self, ch, logos, figs, captions):
        self.ch, self.logos, self.figs, self.captions = ch, logos, figs, captions
        self.prs = Presentation(); self.prs.slide_width, self.prs.slide_height = W, H
        self.blank = self.prs.slide_layouts[6]
        self.num = f"{int(ch['num']):02d}"

    # ---- primitives -------------------------------------------------------------------------------------------
    def rect(self, s, x, y, w, h, fill, shape=MSO_SHAPE.RECTANGLE, radius=None):
        sh = s.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
        sh.fill.solid(); sh.fill.fore_color.rgb = fill; sh.line.fill.background(); sh.shadow.inherit = False
        if radius is not None and shape == MSO_SHAPE.ROUNDED_RECTANGLE:
            sh.adjustments[0] = radius
        return sh

    def text(self, s, x, y, w, h, anchor=MSO_ANCHOR.TOP, margin=0):
        tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = tb.text_frame; tf.word_wrap = True; tf.vertical_anchor = anchor
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = Inches(margin)
        return tf

    def para(self, tf, first):
        return tf.paragraphs[0] if first else tf.add_paragraph()

    def slide(self, notes="", dark=False):
        s = self.prs.slides.add_slide(self.blank)
        bg = s.background.fill; bg.solid(); bg.fore_color.rgb = PRI if dark else WHITE
        if notes:
            s.notes_slide.notes_text_frame.text = clean(notes).replace("**", "")
        return s

    def header(self, s, kicker, title):
        chip = self.rect(s, M, 0.52, 0.72, 0.72, ACC, MSO_SHAPE.OVAL)
        tf = chip.text_frame; tf.margin_left = tf.margin_right = 0
        p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER; runs(p, self.num, 18, WHITE, True, HEAD)
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        k = self.text(s, M + 0.95, 0.48, CW - 1, 0.32)
        runs(k.paragraphs[0], kicker.upper(), 12, ACC, True, spacing=150)
        t = self.text(s, M + 0.95, 0.74, CW - 1, 0.7)
        runs(t.paragraphs[0], title, 32 if len(title) < 42 else 27, INK, True, HEAD)

    def footer(self, s, dark=False):
        col = CREAM if dark else MUT
        f = self.text(s, M, 7.02, 9, 0.3)
        runs(f.paragraphs[0], f"Drug Information  ·  Section {int(self.ch['num'])}  ·  {self.ch['title']}", 10, col)
        n = self.text(s, 11.4, 7.02, 0.8, 0.3); n.paragraphs[0].alignment = PP_ALIGN.RIGHT
        runs(n.paragraphs[0], str(len(self.prs.slides)), 10, col, True)
        s.shapes.add_picture(str(self.logos[1]), Inches(12.3), Inches(6.9), height=Inches(0.42))

    def content(self, kicker, title, notes=""):
        s = self.slide(notes); self.header(s, kicker, title); self.footer(s)
        return s

    def rows(self, s, items, y=1.75, h=4.95, x=M, w=CW, size=20, dark=False):
        """Numbered rows: a small numbered disc beside each point (replaces plain bullets)."""
        def lines(t, sz):   # estimated wrapped lines of one point at font size sz
            per = (w - 0.65) * 72 / (sz * 0.5)
            return max(1, -(-len(clean(t).replace("**", "")) // int(per)))
        while size > 15 and sum(lines(t, size) * size * 1.25 / 72 + 0.22 for t in items) > h:
            size -= 1
        hs = [lines(t, size) * size * 1.25 / 72 + 0.22 for t in items]
        pad = min(0.35, (h - sum(hs)) / max(len(items), 1)) if sum(hs) < h else 0
        yy = y
        for i, it in enumerate(items):
            step = hs[i] + pad
            d = self.rect(s, x, yy + 0.02, 0.44, 0.44, CREAM if dark else ACC_L, MSO_SHAPE.OVAL)
            tf = d.text_frame; tf.margin_left = tf.margin_right = 0; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER; runs(p, str(i + 1), 13, PRI if dark else ACC, True)
            t = self.text(s, x + 0.65, yy + 0.04, w - 0.65, step - 0.05)
            runs(t.paragraphs[0], it, size, WHITE if dark else INK)
            yy += step

    def card(self, s, label, body, x, y, w, h, fill=WARM, tone=PRI, size=17):
        self.rect(s, x, y, w, h, fill, MSO_SHAPE.ROUNDED_RECTANGLE, 0.06)
        pill = self.rect(s, x + 0.3, y + 0.25, 0.25 + 0.105 * len(label), 0.34, tone, MSO_SHAPE.ROUNDED_RECTANGLE, 0.5)
        tf = pill.text_frame; tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER; runs(p, label.upper(), 10.5, WHITE, True, spacing=100)
        t = self.text(s, x + 0.3, y + 0.75, w - 0.6, h - 0.95)
        runs(t.paragraphs[0], body, size)

    def table(self, s, rows, y=1.75, h=4.95):
        nr, nc = len(rows), max(len(r) for r in rows)
        chars = sum(len(c) for r in rows for c in r)
        size = 20 if chars < 300 else 18 if chars < 550 else 16 if chars < 850 else 14 if chars < 1250 else 12
        rh = min(h / nr, 0.85)
        shape = s.shapes.add_table(nr, nc, Inches(M), Inches(y), Inches(CW), Inches(rh * nr))
        tbl = shape.table
        tblPr = shape._element.graphic.graphicData.tbl.tblPr   # plain look: no banding from the default style
        tblPr.set("bandRow", "0"); tblPr.set("firstRow", "0")
        lens = [min(max(len(r[j]) if j < len(r) else 0 for r in rows), 60) + 8 for j in range(nc)]
        for j in range(nc):
            tbl.columns[j].width = Emu(int(Inches(CW) * lens[j] / sum(lens)))
        for i, r in enumerate(rows):
            tbl.rows[i].height = Inches(rh)
            for j in range(nc):
                cell = tbl.cell(i, j); cell.text = ""
                cell.fill.solid(); cell.fill.fore_color.rgb = PRI if i == 0 else (WARM if i % 2 == 0 else WHITE)
                cell.margin_left = cell.margin_right = Inches(0.12)
                cell.margin_top = cell.margin_bottom = Inches(0.05)
                cell.vertical_anchor = MSO_ANCHOR.MIDDLE
                bold = i == 0 or (j == 0 and nc > 1)
                runs(cell.text_frame.paragraphs[0], r[j] if j < len(r) else "",
                     size - (1 if i == 0 else 0), WHITE if i == 0 else INK, bold)

    def split(self, label, glyph, body, notes, panel=ACC, tint=ACC_L, size=22):
        """Half-bleed panel on the left (label + large glyph), text on the right."""
        s = self.slide(notes)
        self.rect(s, 0, 0, 4.3, 7.5, panel)
        g = self.text(s, 0.6, 1.3, 3.2, 2.6); g.paragraphs[0].alignment = PP_ALIGN.LEFT
        runs(g.paragraphs[0], glyph, 130, tint, True, HEAD)
        k = self.text(s, 0.6, 4.35, 3.3, 1.4)
        runs(k.paragraphs[0], label, 30, WHITE, True, HEAD)
        p = k.add_paragraph(); runs(p, f"Section {int(self.ch['num'])}", 14, tint, True, spacing=150)
        t = self.text(s, 4.95, 0.9, 7.8, 5.6, MSO_ANCHOR.MIDDLE)
        runs(t.paragraphs[0], body, size if len(body) < 420 else size - 2 if len(body) < 620 else size - 4)
        f = self.text(s, 4.95, 7.02, 6, 0.3)
        runs(f.paragraphs[0], f"Drug Information  ·  {self.ch['title']}", 10, MUT)
        n = self.text(s, 11.4, 7.02, 0.8, 0.3); n.paragraphs[0].alignment = PP_ALIGN.RIGHT
        runs(n.paragraphs[0], str(len(self.prs.slides)), 10, MUT, True)
        s.shapes.add_picture(str(self.logos[1]), Inches(12.3), Inches(6.9), height=Inches(0.42))
        return s

    # ---- slides -----------------------------------------------------------------------------------------------
    def title_slide(self):
        ch = self.ch
        s = self.slide(dark=True)
        big = self.text(s, 8.3, 1.2, 5.2, 5.6, MSO_ANCHOR.MIDDLE)          # oversized section numeral, tone-on-tone
        big.paragraphs[0].alignment = PP_ALIGN.RIGHT
        runs(big.paragraphs[0], self.num, 280, PRI_D, True, HEAD)
        for k, lg in enumerate(self.logos):
            s.shapes.add_picture(str(lg), Inches(M + k * 1.25), Inches(0.55), height=Inches(1.05))
        inst = self.text(s, M + 2.65, 0.72, 7, 0.8, MSO_ANCHOR.MIDDLE)
        runs(inst.paragraphs[0], "Faculty of Pharmacy", 18, WHITE, True, HEAD)
        runs(inst.add_paragraph(), "PORT SAID UNIVERSITY", 12, CREAM, True, spacing=200)
        t = self.text(s, M, 2.75, 7.4, 3.4)
        runs(t.paragraphs[0], f"DRUG INFORMATION  ·  SECTION {int(ch['num'])}", 14, CREAM, True, spacing=200)
        p = t.add_paragraph(); p.space_before = Pt(14)
        runs(p, ch["title"], 44 if len(ch["title"]) < 30 else 36, WHITE, True, HEAD)
        p = t.add_paragraph(); p.space_before = Pt(16)
        runs(p, "A Practical Section Guide", 20, CREAM, italic=True, font=HEAD)
        b = self.text(s, M, 6.55, 9, 0.5)
        runs(b.paragraphs[0], "45-minute practical section  ·  5 questions  ·  1 practice case", 13, CREAM)

    def objectives(self):
        ch = self.ch
        s = self.content("Section goals", "In This Section", " ".join(ch["intro"]))
        self.rows(s, ch["los"], x=M, w=7.9, size=21)
        self.rect(s, 9.15, 1.75, 3.58, 4.95, WARM, MSO_SHAPE.ROUNDED_RECTANGLE, 0.05)
        st = self.text(s, 9.45, 2.05, 3.0, 4.4)
        for i, (big, small) in enumerate((("45", "minutes"), ("5", "questions"), ("1", "practice case"))):
            p = self.para(st, i == 0); p.space_before = Pt(0 if i == 0 else 16)
            runs(p, big, 54, PRI, True, HEAD)
            q = st.add_paragraph(); runs(q, small.upper(), 12, MUT, True, spacing=150)

    def section(self, sec):
        items = sec["items"]
        notes = " ".join(i[1] for i in items if i[0] == "para")
        figs = [i[1] for i in items if i[0] == "fig" and i[1] in self.figs]
        tables = [i[1] for i in items if i[0] == "table"]
        call = [i for i in items if i[0] == "callout" and i[1] != "At the Pharmacy"]
        paras = [i[1] for i in items if i[0] == "para"]
        kick = f"Section {int(self.ch['num'])}"
        tone = lambda lab: (RED_L, RED) if lab == "Caution" else (WARM, PRI)
        if figs:
            s = self.content(kick, sec["title"], notes)
            pic = s.shapes.add_picture(str(self.figs[figs[0]]), Inches(M), Inches(1.7), height=Inches(4.55))
            if pic.width > Inches(CW):
                pic.height = int(pic.height * Inches(CW) / pic.width); pic.width = Inches(CW)
            pic.left = int((W - pic.width) / 2)
            cap = self.text(s, M, 6.4, CW, 0.4); cap.paragraphs[0].alignment = PP_ALIGN.CENTER
            runs(cap.paragraphs[0], self.captions.get(figs[0], ""), 13, MUT, italic=True)
        big = max(tables, key=len) if tables else None
        for t in tables:
            if t is big or len(t) >= 3:
                s = self.content(kick, sec["title"], notes)
                room = t is big and call and len(t) <= 6
                self.table(s, t, h=3.5 if room else 4.95)
                if room:
                    fill, tn = tone(call[0][1])
                    self.card(s, call[0][1], call[0][2], M, 5.45, CW, 1.35, fill, tn, 15)
                    call = call[1:]
        sub = sec["title"]
        lists = []
        for i in items:
            if i[0] == "sub": sub = i[1]
            if i[0] == "list": lists.append((sub, i[1]))
        if not figs and not tables and not lists:
            lists = [(sec["title"], [re.split(r"(?<=[.!?])\s", p)[0] for p in paras][:5])]
        for title, pts in lists:
            s = self.content(kick, title, notes)
            if call and sum(len(x) for x in pts) < 420:   # long points get the full width; the card moves on
                fill, tn = tone(call[0][1])
                self.rows(s, pts[:6], w=7.6, size=20)
                self.card(s, call[0][1], call[0][2], 8.75, 1.75, 3.98, 4.95, fill, tn, 16)
                call = call[1:]
            else:
                self.rows(s, pts[:7], size=24 if len(pts) <= 3 else 21)
        for c in call:   # a callout that found no room above gets its own card slide
            s = self.content(kick, sec["title"], notes)
            fill, tn = tone(c[1]); self.card(s, c[1], c[2], M + 1.2, 2.3, CW - 2.4, 2.6, fill, tn, 26)
        for c in (i for i in items if i[0] == "callout" and i[1] == "At the Pharmacy"):
            self.split("At the Pharmacy", "℞", c[2], "Discuss with the class: what would you ask, check and say?")

    def mcq(self, q):
        key, why = self.ch["answers"].get(q["n"], ("", ""))
        total = len(self.ch["mcq"])
        for reveal in (False, True):
            s = self.content(f"Self-assessment  ·  question {q['n']} of {total}" + ("  ·  answer" if reveal else ""),
                             "Check your answer" if reveal else "Your turn", "" if reveal else f"Answer {key}: {why}")
            t = self.text(s, M, 1.7, CW, 1.1)
            runs(t.paragraphs[0], q["q"], 24 if len(q["q"]) < 120 else 21, INK, True)
            top = 2.95 if not reveal else 2.85
            gap = 0.84 if not reveal else 0.74
            for k, o in enumerate(q["opts"]):
                letter, body = o[0], o[3:]
                hit = reveal and letter == key
                faded = reveal and not hit
                self.rect(s, M, top + k * gap, CW, gap - 0.14, ACC if hit else (C("F7F4F2") if faded else WARM),
                          MSO_SHAPE.ROUNDED_RECTANGLE, 0.18)
                d = self.rect(s, M + 0.18, top + k * gap + (gap - 0.14 - 0.46) / 2, 0.46, 0.46,
                              WHITE if hit else (C("E6DFDA") if faded else PRI), MSO_SHAPE.OVAL)
                tf = d.text_frame; tf.margin_left = tf.margin_right = 0; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
                p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
                runs(p, letter, 15, ACC if hit else (MUT if faded else WHITE), True)
                b = self.text(s, M + 0.9, top + k * gap, CW - 1.1, gap - 0.14, MSO_ANCHOR.MIDDLE)
                runs(b.paragraphs[0], body, 19, WHITE if hit else (MUT if faded else INK), hit)
            if reveal:
                r = self.text(s, M, top + 4 * gap + 0.05, CW, 0.75)
                runs(r.paragraphs[0], "Why:  ", 15, ACC, True); runs(r.paragraphs[0], why, 15, INK)

    def closing(self):
        s = self.slide(dark=True)
        k = self.text(s, M, 0.55, 8, 0.4); runs(k.paragraphs[0], f"SECTION {int(self.ch['num'])}  ·  SUMMARY", 13, CREAM, True, spacing=200)
        t = self.text(s, M, 0.9, 10, 0.8); runs(t.paragraphs[0], "Key Takeaways", 36, WHITE, True, HEAD)
        self.rows(s, self.ch["takeaways"], y=2.0, h=4.6, size=21, dark=True)
        for k2, lg in enumerate(self.logos):
            s.shapes.add_picture(str(lg), Inches(11.35 + k2 * 0.72), Inches(6.72), height=Inches(0.6))

    def build(self):
        self.title_slide()
        self.objectives()
        for sec in self.ch["sections"]:
            self.section(sec)
        for q in self.ch["mcq"]:
            self.mcq(q)
        self.split("Practice Case", "?", self.ch["case"], "Model answer: " + self.ch["case_answer"], PRI, WARM_2, 22)
        self.closing()
        return self.prs


def main(project):
    project = pathlib.Path(project)
    plan = json.loads((project / "design" / "chapter-plan.json").read_text(encoding="utf-8"))
    figs = {p.stem: p for p in (project / "figures" / "out").glob("*.png")}
    captions = {f["id"]: f["caption"] for f in json.loads((project / "figures" / "figures.json").read_text(encoding="utf-8"))["figures"]}
    out = project / "slides"; out.mkdir(exist_ok=True)
    assets = out / "_assets"; assets.mkdir(exist_ok=True)
    logos = [badge(project / "images/logos" / n, assets / n) for n in ("port-said-university.png", "faculty-of-pharmacy.png")]
    for c in plan["chapters"]:
        ch = parse((project / "chapters" / c["file"]).read_text(encoding="utf-8"))
        prs = Deck(ch, logos, figs, captions).build()
        path = out / c["file"].replace(".md", ".pptx")
        try:
            prs.save(path)
        except PermissionError:   # the deck is open in PowerPoint
            print(f"{path.name}: SKIPPED, file is open; close it and run again"); continue
        print(f"{path.name}: {len(prs.slides)} slides")


if __name__ == "__main__":
    import pathlib, sys  # gate shim (Task 7.3): no stage work before the gates pass
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))  # repo root
    from harness.gate import enforce
    PROJECT = enforce("build", sys.argv)
    main(PROJECT)
