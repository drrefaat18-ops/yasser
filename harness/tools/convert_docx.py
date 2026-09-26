"""DOCX -> Markdown with a fidelity report (core §2.4; plan Task 8.4; INV-01..07).

Usage: python harness/tools/convert_docx.py --project projects/<slug>
Converts the project's DOCX source (brief.source.files) in memory and prints the conversion report; it writes
nothing (`run ingest` writes the outputs). Exit 0 ok; 2 if a structure is `lost`; 1 on a refused gate.

Headings come from Word heading styles and template.ingest.heading_rules only (the same predicate counts the
source and the output). A source TOC is dropped when template.ingest.drop_source_toc is true and recorded as a
configured omission. Equations and footnotes are inlined as `[equation: …]` / `[footnote: …]` (lossy).
"""
import hashlib, json, os, pathlib, re, sys

REPO = pathlib.Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
      "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
      "m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
      "mc": "http://schemas.openxmlformats.org/markup-compatibility/2006",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}
TEXT_MIN_SHARE = 0.98
CHAPTER_CAPS = re.compile(r"^CHAPTER\s+(\d+):")   # legacy: an all-caps chapter heading is written in title case
STRUCTURES = ["headings", "tables", "callouts", "figures", "equations", "footnotes", "text"]
BULLETS = "•·•●○▪▫"


def xp(el, expr):
    from lxml import etree
    return etree._Element.xpath(el, expr, namespaces=NS)


def _w(tag):
    return f"{{{NS['w']}}}{tag}"


def nonspace(s):
    return len(re.sub(r"\s", "", s))


# ---------- inline formatting (legacy algorithm) ----------

def line_tokens(p):
    lines = [[]]
    for r in p.runs:
        for idx, part in enumerate(r.text.split("\n")):
            if idx > 0:
                lines.append([])
            if part:
                lines[-1].append({"text": part, "bold": bool(r.bold), "italic": bool(r.italic),
                                  "font_size": r.font.size.pt if r.font and r.font.size else None})
    return lines


def format_tokens(tokens):
    if not tokens:
        return ""
    merged = []
    for t in tokens:
        if merged and merged[-1]["bold"] == t["bold"] and merged[-1]["italic"] == t["italic"]:
            merged[-1]["text"] += t["text"]
        else:
            merged.append(dict(t))
    out = ""
    for item in merged:
        raw, b, i = item["text"], item["bold"], item["italic"]
        if not b and not i:
            out += raw
            continue
        lead, trail = re.match(r"^\s*", raw).group(), re.search(r"\s*$", raw).group()
        core = raw[len(lead):len(raw) - len(trail)]
        if not core:
            out += raw
            continue
        styled = f"*{core}*" if i else core
        out += lead + (f"**{styled}**" if b else styled) + trail
    return out


class Converter:
    def __init__(self, docx_path, cfg):
        import docx
        self.doc = docx.Document(str(docx_path))
        self.cfg = cfg
        ing = cfg["template"]["ingest"]
        self.rules = [(re.compile(r["pattern"]), r["level"]) for r in ing["heading_rules"]]
        pat = lambda k: re.compile(ing[k]) if ing.get(k) else None
        self.toc_start, self.toc_entry, self.toc_end = pat("toc_start_pattern"), pat("toc_entry_pattern"), pat("toc_end_pattern")
        self.drop_toc = bool(ing["drop_source_toc"])
        project = cfg["project"]
        self.link_base = pathlib.Path(os.path.relpath(project / cfg["template"]["paths"]["assets"],
                                                     (project / cfg["template"]["paths"]["normalized_source"]).parent)).as_posix()
        self.assets, self.counts = {}, {k: 0 for k in STRUCTURES}
        self.omitted, self.footnotes = [], self._footnotes()
        self.dropped = set()   # paragraphs left out as a configured omission (not counted as source headings)

    def _footnotes(self):
        for rel in self.doc.part.rels.values():
            if rel.reltype.endswith("/footnotes"):
                from lxml import etree
                root = etree.fromstring(rel.target_part.blob)
                return {f.get(_w("id")): "".join(xp(f, ".//w:t/text()")).strip() for f in xp(root, "//w:footnote")}
        return {}

    def heading_level(self, p, clean):
        for rx, level in self.rules:
            if rx.search(clean):
                return level
        m = re.fullmatch(r"Heading ([1-6])", p.style.name or "")
        return int(m.group(1)) if m else 0

    def images(self, el):
        out = []
        for b in xp(el, ".//a:blip[not(ancestor::mc:Fallback)]"):
            rid = b.get(f"{{{NS['r']}}}embed")
            if rid and rid in self.doc.part.rels:
                part = self.doc.part.rels[rid].target_part
                name = os.path.basename(self.doc.part.rels[rid].target_ref)
                self.assets[name] = part.blob
                out.append(f"![Image]({self.link_base}/{name})")
        return out

    def extras(self, p):
        out = []
        for m in xp(p._p, ".//m:oMath[not(ancestor::m:oMath)]"):
            out.append(f"[equation: {''.join(xp(m, './/m:t/text()')).strip()}]")
        for ref in xp(p._p, ".//w:footnoteReference"):
            out.append(f"[footnote: {self.footnotes.get(ref.get(_w('id')), '')}]")
        return out

    def paragraph(self, p, quote=False):
        lines = []
        if p.text.strip():
            for tokens in line_tokens(p):
                text = format_tokens(tokens)
                if not text.strip():
                    continue
                clean = re.sub(r"[*_`]", "", text).strip()
                level = self.heading_level(p, clean)
                if level and not quote:
                    lines.append("#" * level + " " + CHAPTER_CAPS.sub(r"Chapter \1:", clean))
                elif p.style.name == "List Bullet" or clean[:1] in BULLETS:
                    lines.append("- " + re.sub(rf"^[{BULLETS}\t ]+", "", text).strip())
                else:
                    lines.append(text.strip())
        return lines + self.extras(p) + self.images(p._p)

    def table(self, tbl):
        from docx.table import Table
        t = Table(tbl, self.doc)
        rows, cols = len(t.rows), len(t.columns)
        if rows == 1 and cols == 1:
            self.counts["callouts"] += 1
            out = []
            for p in t.rows[0].cells[0].paragraphs:
                out += [f"> {l}" if l.strip() else ">" for l in self.paragraph(p, quote=True)]
            return "\n".join(out)
        self.counts["tables"] += 1
        cell = lambda c: (" ".join(format_tokens(line_tokens(p)[0]).strip() for p in c.paragraphs if p.text.strip())
                          .replace("\n", "<br>").replace("|", "\\|") or " ")
        lines = ["| " + " | ".join(cell(c) for c in t.rows[0].cells) + " |", "| " + " | ".join(["---"] * cols) + " |"]
        lines += ["| " + " | ".join(cell(c) for c in row.cells) + " |" for row in t.rows[1:]]
        return "\n".join(lines)

    def blocks(self):
        """Body children in document order; content controls (w:sdt) are unwrapped."""
        def walk(parent):
            for child in parent.iterchildren():
                if child.tag == _w("sdt"):
                    for content in child.iterchildren(_w("sdtContent")):
                        yield from walk(content)
                elif child.tag in (_w("p"), _w("tbl")):
                    yield child
        yield from walk(self.doc.element.body)

    def convert(self):
        from docx.text.paragraph import Paragraph
        out, in_toc, toc_start, toc_chars = [], False, None, 0
        for idx, el in enumerate(self.blocks(), 1):
            if el.tag == _w("tbl"):
                md = self.table(el)
                if md.strip():
                    out.append(md)
                continue
            p = Paragraph(el, self.doc)
            raw = p.text.strip()
            if self.toc_start and not in_toc and self.toc_start.search(raw):
                in_toc, toc_start = True, idx
            elif in_toc and self.toc_end and self.toc_end.search(raw):
                in_toc = False
                if self.drop_toc:
                    self.omitted.append({"reason": "source_toc", "chars": toc_chars, "line_start": toc_start, "line_end": idx - 1})
            if in_toc:
                if self.drop_toc:
                    toc_chars += nonspace("".join(xp(el, ".//w:t/text()")))
                    self.dropped.add(el)
                    continue
                m = self.toc_entry.search(raw) if self.toc_entry else None
                if m:
                    out.append(f"- {m.group(1).strip()}")
                    continue
            out += self.paragraph(p) or [""]
        cleaned, prev_blank = [], False
        for b in out:
            blank = not b.strip()
            if not (blank and prev_blank):
                cleaned.append("" if blank else b)
            prev_blank = blank
        return re.sub(r"\n{3,}", "\n\n", "\n\n".join(cleaned)).strip("\n") + "\n"


def _status(src, got, lossy=False):
    if src == got:
        return "lossy" if lossy and src else "ok"
    return "lost"


def source_counts(conv):
    body = conv.doc.element.body
    heads = 0
    for el in conv.blocks():
        if el.tag == _w("p") and el not in conv.dropped:
            from docx.text.paragraph import Paragraph
            p = Paragraph(el, conv.doc)   # per line, as the converter writes them (a paragraph may hold line breaks)
            for line in p.text.split("\n"):
                clean = re.sub(r"[*_`]", "", line).strip()
                if clean and conv.heading_level(p, clean):
                    heads += 1
    tbls = xp(body, ".//w:tbl[not(ancestor::mc:Fallback)]")
    one = [t for t in tbls if len(xp(t, "./w:tr")) == 1 and len(xp(t, "./w:tr/w:tc")) == 1]
    return {"headings": heads, "tables": len(tbls) - len(one), "callouts": len(one),
            "figures": len(xp(body, ".//a:blip[not(ancestor::mc:Fallback)]")),
            "equations": len(xp(body, ".//m:oMath[not(ancestor::m:oMath)]")),
            "footnotes": len(xp(body, ".//w:footnoteReference")),
            "text": nonspace("".join(xp(body, ".//w:t[not(ancestor::mc:Fallback)]/text()")))}


def output_counts(md):
    lines = md.splitlines()
    stripped = re.sub(r"!\[[^\]]*\]\([^)]*\)|\[(?:equation|footnote): |^#{1,6} |^> ?|^- |^\| ---.*$|[*|]", "", md, flags=re.M)
    return {"headings": sum(1 for l in lines if re.match(r"^#{1,6} ", l)),
            "tables": sum(1 for l in lines if l.startswith("| ---")),
            "figures": len(re.findall(r"!\[[^\]]*\]\(", md)),
            "equations": md.count("[equation: "), "footnotes": md.count("[footnote: "),
            "text": nonspace(stripped)}


def convert(docx_path, cfg):
    """-> (markdown, assets {file name: bytes}, conversion report)."""
    conv = Converter(docx_path, cfg)
    md = conv.convert()
    src, got = source_counts(conv), output_counts(md)
    got["callouts"] = conv.counts["callouts"]
    omitted = sum(o["chars"] for o in conv.omitted)
    structures = {k: {"source_count": src[k], "output_count": got[k], "status": _status(src[k], got[k])}
                  for k in ("headings", "tables", "callouts", "figures")}
    for k in ("equations", "footnotes"):
        structures[k] = {"source_count": src[k], "output_count": got[k], "status": _status(src[k], got[k], lossy=True)}
    base = src["text"] - omitted
    structures["text"] = {"source_count": src["text"], "output_count": got["text"],
                          "status": "ok" if got["text"] >= TEXT_MIN_SHARE * base else "lost", "omitted": conv.omitted}
    report = {"schema_version": 1, "converter": "docx-native", "source_formats": ["docx"], "structures": structures}
    return md, dict(sorted(conv.assets.items())), report


def lost(report):
    return sorted(k for k, v in report["structures"].items() if v["status"] == "lost")


def units(md):
    """units.v1 (EXT-TR-3): src-chNN per level-1 heading, src-chNN-sMM per level-2 heading inside it, in document order."""
    lines = md.split("\n")
    heads = [(i + 1, len(m.group(1)), m.group(2).strip()) for i, l in enumerate(lines)
             for m in [re.match(r"^(#{1,2}) (.+)$", l)] if m]
    out, ch, sec = [], 0, 0
    for k, (line, level, text) in enumerate(heads):
        nxt = [h for h in heads[k + 1:] if h[1] <= level]
        end = (nxt[0][0] - 1) if nxt else len(lines)
        while end > line and not lines[end - 1].strip():
            end -= 1
        if level == 1:
            ch, sec = ch + 1, 0
            uid = f"src-ch{ch:02d}"
        elif ch:
            sec += 1
            uid = f"src-ch{ch:02d}-s{sec:02d}"
        else:
            continue
        span = "\n".join(lines[line - 1:end])
        out.append({"id": uid, "heading": text, "level": level, "line_start": line, "line_end": end,
                    "sha256": hashlib.sha256(span.encode("utf-8")).hexdigest()})
    return {"schema_version": 1, "units": out}


def main(project):
    from harness.tools import config
    cfg = config.load(project)
    docx = [f for f in cfg["brief"]["source"]["files"] if f["format"] == "docx"]
    if len(docx) != 1:
        print(f"ERROR CONFIG: expected exactly one docx source, found {len(docx)}", file=sys.stderr)
        return 2
    _, _, report = convert(project / docx[0]["path"], cfg)
    print(json.dumps(report, ensure_ascii=False, indent=1, sort_keys=True))
    return 2 if lost(report) else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    from harness.gate import enforce
    PROJECT = enforce("ingest", sys.argv)   # first call: no stage work before the gates pass
    sys.exit(main(PROJECT))
