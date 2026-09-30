"""One block grammar for every writer (plan Task 9b.1, DEC-045).

The DOCX writer (build_book.py) and the HTML writer (build_html.py) both consume `parse()`, so the two outputs
cannot drift in content. `parse` only reads the markdown and the config; how a block looks is the writer's job.

Blocks (dicts, key "t"):
  section   id, role, label, boxed, unlisted   (a `## ` heading; ids and roles from check_book.parse)
  h3        text
  para      text                               (consecutive plain lines joined by one space)
  callout   key, text, paras                   (key None: a quote block that is no configured callout; a paras
                                               item is a string, or {"rows": ...} for a table inside the box)
  grid      key, label, items [(name, text)]
  table     rows [[cell, ...], ...]            (the delimiter row removed)
  image     link, alt, caption                 (caption: the legacy `*Figure n.m ...*` line, "" if none)
  question  num, stem, los [digits], options [(label, text)]
  bullet    text
  numbered  num, body
  glossary  text
  answer    head, text
Inline markdown: `inline(text)` -> spans {text, bold, italic, sub, sup, url}; `~x~` is subscript, `^x^` superscript.
"""
import re

from harness.tools import check_book

Q_LINE = re.compile(r"\*\*(Q\d+)\.\*\*\s*(.+)")   # marker grammar constant (core §4.3)
LO_TAIL = re.compile(r"\s*(\[LO\d+(?:,\s*LO\d+)*\])\s*$")
INLINE = re.compile(r"(\*\*\*.+?\*\*\*|\*\*.+?\*\*|(?<![\w*])\*[^*\s][^*]*?\*(?![\w*])|\[[^\]]+\]\([^)\s]+\))")
SUBSUP = re.compile(r"(~[^~\s]+~|\^[^^\s]+\^)")
URL = re.compile(r"(https?://[^\s)]+[^\s).,;])")
SUP_CH, SUB_CH = "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾", "₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎"
SCRIPT_RUN = re.compile(f"[{SUP_CH}]+|[{SUB_CH}]+")


def _script_markup(t):
    """Unicode super/subscript runs (Ca²⁺, CO₂) -> `^2+^` / `~2~`: real sup/sub text, never a glyph the font may lack."""
    def one(m):
        run = m.group()
        if run[0] in SUP_CH:
            return "^" + run.translate(str.maketrans(SUP_CH, "0123456789+-=()")) + "^"
        return "~" + run.translate(str.maketrans(SUB_CH, "0123456789+-=()")) + "~"
    return SCRIPT_RUN.sub(one, t)


def _span(text, bold=False, italic=False, sub=False, sup=False, url=None):
    return {"text": text, "bold": bold, "italic": italic, "sub": sub, "sup": sup, "url": url}


def inline(text, links=True):
    """Spans of one line of inline markdown. With `links` False, link markup keeps only its text and bare URLs stay
    plain text (running heads, captions of the legacy builder)."""
    out = []
    for tok in INLINE.split(text):
        if not tok:
            continue
        b, i, t, url = False, False, tok, None
        if tok.startswith("***") and tok.endswith("***") and len(tok) > 6:
            b, i, t = True, True, tok[3:-3]
        elif tok.startswith("**") and tok.endswith("**") and len(tok) > 4:
            b, t = True, tok[2:-2]
        elif tok.startswith("[") and "](" in tok and tok.endswith(")"):
            t, url = tok[1:].split("](", 1)
            url = url[:-1]
        elif tok.startswith("*") and tok.endswith("*") and len(tok) > 2:
            i, t = True, tok[1:-1]
        if url and links:
            out.append(_span(t, b, i, url=url))
            continue
        for seg in SUBSUP.split(_script_markup(t)):
            if not seg:
                continue
            if SUBSUP.fullmatch(seg):
                out.append(_span(seg[1:-1], b, i, sub=seg[0] == "~", sup=seg[0] == "^"))
            elif links and URL.search(seg):
                for k, part in enumerate(URL.split(seg)):
                    if part:
                        out.append(_span(part, b, i, url=part if k % 2 else None))
            else:
                out.append(_span(seg, b, i))
    return out


def plain(text):
    """The text a reader sees: inline markup removed (bookmarks, running heads, parity checks)."""
    return "".join(s["text"] for s in inline(text, links=False))


def table_rows(lines):
    """Markdown table lines -> rows of cell text, the delimiter row removed."""
    cells = [[x.strip() for x in r.strip().strip("|").split("|")] for r in lines]
    return [r for r in cells if not all(re.fullmatch(r":?-+:?", x) for x in r)]


def parse(text, cfg, kind, is_cover=None):
    """-> [block]. `kind`: 'chapter' or 'glossary'. `is_cover(link)`: True for the cover image, which is dropped
    (it is placed by the writer's title pages)."""
    lines = text.splitlines()
    parsed = check_book.parse(text, cfg)   # INV-30: sections and callouts by ID, from the checker's parser
    sec_at = {x["line"]: x for x in parsed["sections"]}
    callout_at = {x["line"]: x["id"] for x in parsed["callouts"]}
    th, t = cfg["theme"], cfg["template"]
    callout_by_id = {c["id"]: c for c in t["callouts"]}
    mcq = t["assessment"]["mcq"]
    options = mcq["option_labels"] if mcq["enabled"] else []
    opt = re.compile(r"(" + "|".join(re.escape(o) for o in options) + r")\)\s") if options else None
    figure_label = th["labels"]["figure"]
    out, buf, role, i = [], [], None, 0

    def flush():
        if buf:
            out.append({"t": "para", "text": " ".join(buf)})
            buf.clear()

    while i < len(lines):
        s = lines[i].strip()
        if not s:
            flush()
            i += 1
            continue
        if s.startswith("# "):
            flush()
            i += 1
            continue   # the H1 is placed by the writer
        if s.startswith("## "):
            flush()
            sec = sec_at[i + 1]
            role = sec["role"]
            out.append({"t": "section", "id": sec["id"], "role": role, "label": sec["label"],
                        "boxed": sec["id"] in th["boxed_section_ids"], "unlisted": sec["id"] in th["toc_excluded_section_ids"]})
            i += 1
            continue
        if s.startswith("### "):
            flush()
            out.append({"t": "h3", "text": s[4:]})
            i += 1
            continue
        if s.startswith(">"):
            flush()
            key = callout_at.get(i + 1)
            block = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                block.append(lines[i].strip()[1:].strip())
                i += 1
            if key and (th["callouts"].get(key) or {}).get("layout") == "grid":
                items = [(m.group(1), m.group(2)) for m in (re.match(r"-\s*\*\*(.+?):\*\*\s*(.+)", b) for b in block[1:]) if m]
                out.append({"t": "grid", "key": key, "label": callout_by_id[key]["label"], "items": items})
            else:
                body = block[0][len(callout_by_id[key]["syntax"].lstrip("> ")):].strip() if key else block[0]
                # a blank `>` line is a paragraph break inside the box: an author who put an equation on
                # its own line meant it to stay there, not to run into the sentence before it
                # a run of `|` lines inside the box is a table, kept as {"rows": ...}: joined into the
                # paragraph it printed as raw pipes and dashes
                paras, cur, rows = [], [body] if body else [], []
                for line in block[1:]:
                    if line.startswith("|"):
                        if cur:
                            paras.append(" ".join(cur))
                            cur = []
                        rows.append(line)
                        continue
                    if rows:
                        paras.append({"rows": table_rows(rows)})
                        rows = []
                    if line:
                        cur.append(line)
                    elif cur:
                        paras.append(" ".join(cur))
                        cur = []
                if rows:
                    paras.append({"rows": table_rows(rows)})
                if cur:
                    paras.append(" ".join(cur))
                text_paras = [x for x in paras if isinstance(x, str)]
                out.append({"t": "callout", "key": key, "text": " ".join(text_paras), "paras": paras})
            continue
        if s.startswith("|"):
            flush()
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(lines[i])
                i += 1
            out.append({"t": "table", "rows": table_rows(rows)})
            continue
        m = re.match(r"!\[(.*?)\]\((.+?)\)", s)
        if m:
            flush()
            link = m.group(2)
            if is_cover and is_cover(link):
                i += 1
                continue
            cap = ""
            if not link.startswith("fig:"):
                j = i + 1
                while j < len(lines) and not lines[j].strip():
                    j += 1
                if j < len(lines) and re.match(rf"\*{re.escape(figure_label)}", lines[j].strip()):
                    cap = lines[j].strip().strip("*")
                    i = j
            out.append({"t": "image", "link": link, "alt": m.group(1), "caption": cap})
            i += 1
            continue
        m = Q_LINE.match(s)
        if m and role == "assessment" and opt:
            flush()
            stem, los = m.group(2), []
            lo = LO_TAIL.search(stem)
            if lo:
                stem, los = stem[: lo.start()], re.findall(r"LO(\d+)", lo.group(1))
            i += 1
            opts = []
            while i < len(lines) and opt.match(lines[i].strip()):
                o = lines[i].strip()
                label = opt.match(o).group(1)
                opts.append((label, o[len(label) + 1:].strip()))
                i += 1
            out.append({"t": "question", "num": m.group(1)[1:], "stem": stem, "los": los, "options": opts})
            continue
        m = re.match(r"[-*]\s+(.+)", s)
        if m:
            flush()
            out.append({"t": "bullet", "text": m.group(1)})
            i += 1
            continue
        m = re.match(r"(\d+)\.\s+(.+)", s)
        if m:
            flush()
            out.append({"t": "numbered", "num": m.group(1), "body": m.group(2)})
            i += 1
            continue
        if kind == "glossary":
            out.append({"t": "glossary", "text": s})
            i += 1
            continue
        if role == "answers" and s.startswith("**"):
            flush()
            m = re.match(r"\*\*(.+?)\*\*\s*(.*)", s)
            out.append({"t": "answer", "head": m.group(1), "text": m.group(2)})
            i += 1
            continue
        buf.append(s)
        i += 1
    flush()
    return out
