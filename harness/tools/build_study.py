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

SRC_SHARE = 0.5
MAX_POINTS, MAX_ROWS, TERMS_PER_SLIDE = 6, 7, 6
DIAGRAMS = {"flow": 5, "cards": 10, "versus": 3, "equation": 4, "spectrum": 6}   # kind: most nodes
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


class StudyDeck(bs.Deck):
    def __init__(self, book, style, ch, logos, figs, captions, outline, md, gloss):
        super().__init__(book, style, ch, logos, figs, captions)
        self.minutes, self.fit = None, False
        self.outline, self.secs = outline, sections_of(md)
        self.terms = [(t, gloss.get(t.lower(), "")) for t in bold_terms(md, self.secs)]

    def content(self, kicker, title, notes="", kind="content"):
        """Content slide with the title in bold inside a framed band (slides.json study.title_frame, default on)."""
        if not (self.b.cfg.get("study") or {}).get("title_frame", True):
            return super().content(kicker, title, notes, kind)
        st = self.st
        s = self.slide(notes)
        self.titles[-1], self.kinds[-1] = title, kind
        band = self.rect(s, bs.M - 0.15, 0.3, bs.CW + 0.3, 1.2, st.warm, bs.MSO_SHAPE.ROUNDED_RECTANGLE, 0.14)
        band.line.color.rgb = bs.rgb(st.pri); band.line.width = bs.Pt(2.25)
        self.centred(self.rect(s, bs.M + 0.1, 0.54, 0.72, 0.72, st.acc, bs.MSO_SHAPE.OVAL), self.num, 18,
                     bs.WHITE_HEX, font=st.head)
        k = self.text(s, bs.M + 1.1, 0.44, bs.CW - 1.3, 0.3)
        kc = next(bs.mix(st.acc, "000000", z) for z in (0, 0.08, 0.16, 0.24, 0.32, 0.4)   # readable on the band
                  if bs.contrast(bs.mix(st.acc, "000000", z), st.warm) >= 4.6 or z == 0.4)
        self.runs(k.paragraphs[0], kicker.upper(), 12, kc, True, spacing=150)
        t = self.text(s, bs.M + 1.1, 0.72, bs.CW - 1.3, 0.7, bs.MSO_ANCHOR.MIDDLE)
        self.runs(t.paragraphs[0], title, 30 if len(title) < 46 else 25, st.pri, True, st.head)
        self.footer(s)
        return s

    # ---- diagrams: native shapes, every word checked like a point ------------------------------------------
    @staticmethod
    def dh(paras, w, z, em=0.43):
        """Height of short diagram text. Average character width measured on PowerPoint exports: body text about
        0.43 em, bold heading font about 0.56 em."""
        per = max(int((w - 0.1) * 72 / (z * em)), 1)
        return sum(max(1, -(-len(bs.clean(t).replace("**", "")) // per)) * z * 1.22 / 72 + 0.1 for t in paras)

    def fitsize(self, paras, w, h, sizes=(20, 18, 17, 16, 15, 14, 13, 12), em=0.43):
        return next((z for z in sizes if self.dh(paras, w, z, em) <= h), sizes[-1])

    def layout(self, nodes, w, h, labels=None):
        """One label size, header height and text size for a whole row of nodes (uniform look); the height the
        nodes need at that size."""
        labels = labels or [n["label"] for n in nodes]
        lsz = min(self.fitsize([l], w - 0.3, 0.9, (19, 18, 17, 16, 15, 14), 0.56) for l in labels)
        hh = max(0.62, max(self.dh([l], w - 0.3, lsz, 0.56) for l in labels) + 0.14)
        paras = [[t for t in (n.get("text", ""), n.get("sub", "")) if t] for n in nodes]
        z = min((self.fitsize(ps, w - 0.36, h - hh - 0.3, (20, 19, 18, 17, 16, 15, 14, 13, 12)) for ps in paras if ps),
                default=20)                                 # capped at 20 pt so slides read alike
        need = hh + max((self.dh(ps, w - 0.36, z) for ps in paras if ps), default=0) + 0.45
        return lsz, hh, z, need

    def box(self, s, x, y, w, h, node, lay, fill, label=None):
        """A node: coloured header with the label, the text below, an italic example under it."""
        st, (lsz, hh, z, _) = self.st, lay
        card = self.rect(s, x, y, w, h, bs.WHITE_HEX, bs.MSO_SHAPE.ROUNDED_RECTANGLE, 0.07)
        card.line.color.rgb = bs.rgb(st.warm2); card.line.width = bs.Pt(1.5)
        head = self.rect(s, x, y, w, hh, fill, bs.MSO_SHAPE.ROUNDED_RECTANGLE, 0.18)
        tf = head.text_frame; tf.word_wrap = True
        tf.margin_left = tf.margin_right = bs.Inches(0.12); tf.margin_top = tf.margin_bottom = 0
        tf.vertical_anchor = bs.MSO_ANCHOR.MIDDLE
        q = tf.paragraphs[0]; q.alignment = bs.PP_ALIGN.CENTER
        self.runs(q, label or node["label"], lsz, bs.WHITE_HEX, True, st.head)
        text, sub = node.get("text", ""), node.get("sub", "")
        paras = [t for t in (text, sub) if t]
        if not paras:
            return
        body = self.text(s, x + 0.18, y + hh + 0.16, w - 0.36, h - hh - 0.26)
        for i, t in enumerate(paras):
            q = body.paragraphs[0] if i == 0 else body.add_paragraph(); q.space_before = bs.Pt(0 if i == 0 else 8)
            ex = bool(sub) and i == len(paras) - 1
            self.runs(q, t, z, st.mut if ex else st.ink, italic=ex)

    def connector(self, s, x, y, w, glyph=None):
        if glyph:
            d = self.rect(s, x + (w - 0.62) / 2, y - 0.31, 0.62, 0.62, self.st.acc, bs.MSO_SHAPE.OVAL)
            self.centred(d, glyph, 22, bs.WHITE_HEX, font=self.st.head)
        else:
            self.rect(s, x + 0.08, y - 0.24, w - 0.16, 0.48, self.st.acc, bs.MSO_SHAPE.RIGHT_ARROW)

    def caption_bar(self, s, items):
        """Key-message bar under a diagram (primary tint, accent stripe); returns the height it takes."""
        if not items:
            return 0
        texts = [c["text"] for c in items]
        z = self.fitsize(texts, bs.CW - 1.0, 1.4, (20, 19, 18, 17, 16))
        h = self.height(texts, bs.CW - 1.0, z) + 0.3
        y = bs.BOTTOM - h
        self.rect(s, bs.M, y, bs.CW, h, self.st.warm, bs.MSO_SHAPE.RECTANGLE)
        self.rect(s, bs.M, y, 0.14, h, self.st.acc)
        tf = self.text(s, bs.M + 0.45, y + 0.12, bs.CW - 0.8, h - 0.24, bs.MSO_ANCHOR.MIDDLE)
        for i, t in enumerate(texts):
            q = tf.paragraphs[0] if i == 0 else tf.add_paragraph(); q.space_before = bs.Pt(0 if i == 0 else 4)
            self.runs(q, t, z)
        return h + 0.3

    def diagram(self, sec, sl, notes):
        s = self.content(self.kick(sec), sl["title"], notes, "diagram")
        st, kind, nodes = self.st, sl["kind"], sl["nodes"]
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
            rws, gx, gy = -(-n // cols), 0.22, 0.25
            w, cell = (cw - gx * (cols - 1)) / cols, (band - gy * (rws - 1)) / rws
            labs = [f"{i + 1}. {nd['label']}" if sl.get("numbered") else nd["label"] for i, nd in enumerate(nodes)]
            lay = self.layout(nodes, w, cell, labs)
            hh = min(cell, max(lay[3], 1.6))
            y0 = top + (band - (hh * rws + gy * (rws - 1))) / 2
            for i, nd in enumerate(nodes):
                r, c = divmod(i, cols)
                self.box(s, x0 + c * (w + gx), y0 + r * (hh + gy), w, hh, nd, lay, st.acc if i == hi else st.pri, labs[i])
        elif kind == "spectrum":
            gx = 0.2; w = (cw - gx * (n - 1)) / n
            lay = self.layout(nodes, w, band - 0.7)
            h = min(band - 0.7, max(lay[3], 2.0)); y = top + (band - 0.7 - h) / 2
            self.rect(s, x0, y, cw, 0.55, st.warm2, bs.MSO_SHAPE.RIGHT_ARROW)
            for j, e in enumerate(sl.get("ends") or []):
                tf = self.text(s, x0 + 0.25 + j * (cw / 2 - 0.6), y + 0.1, cw / 2 - 0.4, 0.35, bs.MSO_ANCHOR.MIDDLE)
                tf.paragraphs[0].alignment = bs.PP_ALIGN.RIGHT if j else bs.PP_ALIGN.LEFT
                self.runs(tf.paragraphs[0], e.upper(), 12, st.pri, True, spacing=120)
            for i, nd in enumerate(nodes):
                self.box(s, x0 + i * (w + gx), y + 0.7, w, h, nd, lay, st.acc if i == hi else st.pri)

    def facts(self):
        return [(str(len(self.secs)), "sections"), (str(len(self.terms)), "key terms"), (str(len(self.mcqs)), "questions")]

    def kick(self, sec):
        return f"§{sec}  ·  {self.secs[sec][0]}"

    def points(self, sec, sl, notes):
        s = self.content(self.kick(sec), sl["title"], notes, "list")
        pts = [p["text"] for p in sl["points"]]
        fig = sl.get("figure")
        if fig and fig in self.figs:
            self.rows(s, pts, w=4.5, size=18)                     # short points beside a large figure
            self.visual(s, {"kind": "fig", "data": fig}, bs.M + 4.9, bs.TOP, bs.CW - 4.9, bs.BOTTOM - bs.TOP)
        else:
            self.rows(s, pts, size=22)

    def table_slides(self, title, kicker, head, rows, notes, first_bold=True):
        parts = self.pages_of(rows, MAX_ROWS)
        for i, part in enumerate(parts):
            suffix = f" ({i + 1}/{len(parts)})" if len(parts) > 1 else ""
            s = self.content(kicker, title + suffix, notes, "dense")
            self.table(s, [head] + part)

    def callout(self, sec, label, body, notes):
        s = self.content(self.kick(sec), label, notes, "callout")
        fill, tone = self.st.tone(self.b.callout_by_label.get(label, ""))
        self.card(s, label, body or [""], bs.M + 0.6, bs.TOP + 0.2, bs.CW - 1.2, 3.2, fill, tone, 24)

    def key_terms(self):
        rows = [[t[:1].upper() + t[1:], d] for t, d in self.terms if d]
        if rows:
            self.table_slides("Key terms", f"{self.unit}  ·  definitions", ["Term", "Definition"], rows,
                              "Definitions from the book's glossary.")

    def revision(self):
        s = self.content(f"{self.unit}  ·  revision", f"{self.unit} on one page",
                         "The chapter's key takeaways and key terms, for last-minute revision.", "revision")
        items, w = self.ch["takeaways"], 7.6                   # compact numbered list: one slide, nothing dropped
        size = next(z for z in (18, 17, 16, 15, 14) if self.height(items, w - 0.5, z) <= bs.BOTTOM - bs.TOP - 0.1 or z == 14)
        tf = self.text(s, bs.M, bs.TOP, w, bs.BOTTOM - bs.TOP)
        for i, t in enumerate(items):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph(); p.space_after = bs.Pt(6)
            self.runs(p, f"{i + 1}   ", size, self.st.acc, True); self.runs(p, t, size)
        x, cw = bs.M + w + 0.4, bs.CW - w - 0.4                  # key terms card, two columns
        terms = [t[:1].upper() + t[1:] for t, _ in self.terms]
        half = -(-len(terms) // 2)
        self.rect(s, x, bs.TOP, cw, bs.BOTTOM - bs.TOP, self.st.warm, bs.MSO_SHAPE.ROUNDED_RECTANGLE, 0.05)
        pill = self.rect(s, x + 0.3, bs.TOP + 0.25, 1.6, 0.38, self.st.pri, bs.MSO_SHAPE.ROUNDED_RECTANGLE, 0.5)
        self.centred(pill, "KEY TERMS", 12, bs.WHITE_HEX)
        tsz = 15 if half <= 11 else 13
        for k, col in enumerate((terms[:half], terms[half:])):
            tf = self.text(s, x + 0.3 + k * (cw - 0.5) / 2, bs.TOP + 0.85, (cw - 0.7) / 2, bs.BOTTOM - bs.TOP - 1.0)
            for i, t in enumerate(col):
                p = tf.paragraphs[0] if i == 0 else tf.add_paragraph(); p.space_after = bs.Pt(4)
                self.runs(p, t, tsz, self.st.ink)

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
        if self.b.cfg.get("mcq_slides", True):
            for q in self.mcqs:
                self.mcq(q)
        if self.ch["takeaways"]:
            self.revision()
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
    status, report = 0, {}
    for c in book.plan["chapters"]:
        stem_ = pathlib.Path(c["file"]).stem
        src = base / f"{stem_}.json"
        if not src.is_file() or (only and not stem_.startswith(only)):
            continue
        md = (chapters / c["file"]).read_text(encoding="utf-8")
        outline = json.loads(src.read_text(encoding="utf-8"))
        issues = check(outline, md, sections_of(md))
        deck = StudyDeck(book, style, bs.parse(md, book), logos, figs, captions, outline, md, gloss)
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
