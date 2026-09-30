"""Config-driven chapter and book checker (core §9.3; plan Task 8.1). Stdlib only.

Usage: python harness/tools/check_book.py --project projects/<slug> [--chapter ID] [--json]
Exit 0 iff no blocking check fails; 1 on a blocking fail or a refused gate; 2 on a config error.
Each check reports `pass`, `fail` or `not_applicable` (its feature is disabled in template.json). A fail of an ID in
NON_BLOCKING is printed as WARN and does not change the exit code.
"""
import argparse, json, pathlib, re, sys

REPO = pathlib.Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))
from harness import text as tx  # noqa: E402
from harness.tools import assemble, config  # noqa: E402

# Marker grammar: a harness constant, the same for every language (core §4.3 assessment.mcq; Arabic contract P1)
Q_START = re.compile(r"^(?=\*\*Q\d+\.\*\*)", re.M)
Q_HEAD = re.compile(r"\*\*Q(\d+)\.\*\*(.*)")
Q_ANY = re.compile(r"^\*\*Q(\d+)\.\*\*", re.M)
LO_TAG = re.compile(r"\[LO(\d+)\]")
LO_LINE = re.compile(r"^\d+\. \[LO(\d+)\]", re.M)
OPTION = re.compile(r"^([^\s)*]+)\) ", re.M)
IMAGE = re.compile(r"!\[[^\]]*\]\(([^)\s]+)")

IDS = {  # emission order per function; every ID appears once per target
    "template": ["TPL-H1", "TPL-SECTION-MISSING", "TPL-SECTION-ORDER", "TPL-CALLOUT-MISSING", "TPL-CALLOUT-COUNT"],
    "perspectives": ["PERSP-MISSING", "PERSP-BALANCE"],
    "objectives": ["LO-COUNT", "LO-VERB"],
    "mcqs": ["MCQ-EXTRA-OPTION", "MCQ-OPTIONS", "MCQ-LO-TAG", "MCQ-COUNT", "MCQ-CASE", "MCQ-LO-UNKNOWN",
             "LO-UNASSESSED", "KEY-RATIONALE", "KEY-MISSING", "KEY-BALANCE", "KEY-RUN"],
    "citations": ["CIT-MISSING", "CIT-UNCITED"],
    "sentences": ["READ-MEAN", "READ-LONG", "READ-NOPROSE"],
    "banned": ["BANNED-TERM"],
    "budget": ["BUDGET-CHAPTER"],
    "glossary": ["GLOSS-MISSING"],
    "assets": ["ASSET-MISSING", "ASSET-OUTSIDE-ROOT"],
    "typography": ["TYPO-LATEX"],
    "rhythm": ["RHYTHM-PROSE"],
    "book": ["BOOK-CHAPTER-COUNT", "BOOK-FRONT-MISSING", "BUDGET-TOTAL", "BUDGET-FRONT", "ERRATA-OPEN", "GLOSS-MIN"],
}


# a `fail` of these is a warning: it stays in the report but blocks neither this tool nor `complete rework`
# (user, 2026-09-28: some sections are prose by design, such as an introduction or a case)
NON_BLOCKING = {"RHYTHM-PROSE"}
NA = "not_applicable"   # a check result may list IDs whose sub-feature is disabled under this key


ConfigError = config.ConfigError   # one config error type for every tool (S8-05)


# ---------- parsing ----------

def _labels(cfg):
    return {s["role"]: s["label"] for s in cfg["template"]["sections"]}


def sections(text):
    """H2 label -> body, order preserved."""
    out, cur = {}, None
    for line in text.splitlines():
        m = re.match(r"^## (.+?)\s*$", line)
        if m:
            cur = m.group(1)
            out[cur] = []
        elif cur is not None:
            out[cur].append(line)
    return {k: "\n".join(v) for k, v in out.items()}


def split_at(text, label):
    if label is None:
        return text, ""
    i = text.find(f"\n## {label}")
    return (text, "") if i < 0 else (text[:i], text[i:])


def section_body(text, cfg, role):
    label = _labels(cfg).get(role)
    return sections(text).get(label, "") if label else ""


def no_refs(text, cfg):
    return split_at(text, _labels(cfg).get("references"))[0]


def prose_body(text, cfg):
    return split_at(text, _labels(cfg).get("assessment"))[0]


def words(text, cfg):
    return tx.words(no_refs(text, cfg), cfg["profile_out"])


def clean_prose_lines(text, cfg):
    out, fence = [], False
    for line in prose_body(text, cfg).splitlines():
        s = line.strip()
        if s.startswith("```"):
            fence = not fence
            continue
        if fence or not s or s.startswith("#") or s.startswith("|") or s.startswith("!["):
            continue
        s = re.sub(r"^>\s?", "", s)
        s = re.sub(r"^[-*]\s+|^\d+\.\s+", "", s)
        s = re.sub(r"\*\*[^*]+?:\*\*", "", s)          # labels
        s = LO_TAG.sub("", s)
        s = re.sub(r"[*_`]", "", s)
        if s:
            out.append(s)
    return out


def sentence_lengths(text, cfg):
    prof = cfg["profile_out"]
    return [tx.words(s, prof) for line in clean_prose_lines(text, cfg) for s in tx.sentences(line, prof)]


def lo_ids(text, cfg):
    return LO_LINE.findall(section_body(text, cfg, "objectives"))


def cited_numbers(text, cfg):
    nums = set()
    for grp in re.findall(cfg["template"]["citations"]["pattern"], no_refs(text, cfg)):
        for part in re.split(r"\s*,\s*", grp):
            r = re.split(r"\s*[–-]\s*", part)
            if len(r) == 2:
                nums.update(range(int(r[0]), int(r[1]) + 1))
            else:
                nums.add(int(r[0]))
    return nums


def reference_entries(text, cfg):
    """[(number, entry line)] from the references section."""
    rx = re.compile(cfg["template"]["references"]["entry_pattern"])
    out = []
    for line in section_body(text, cfg, "references").splitlines():
        m = rx.search(line)
        if m:
            out.append(entry_parts(m, line))
    return out


def entry_parts(m, line):
    """references.entry_pattern contract: the number is group `n` (or group 1); the body is group `body`
    (or group 2), else the rest of the line after the match."""
    names = m.re.groupindex
    n = m.group("n") if "n" in names else m.group(1)
    body = m.group("body") if "body" in names else (m.group(2) if m.re.groups >= 2 else line[m.end():])
    return int(n), body


def glossary_terms(text, cfg):
    g = cfg["template"]["glossary"]
    if g["term_syntax"] != "bold":
        raise ConfigError(f"glossary.term_syntax {g['term_syntax']!r} is not supported")
    excluded = {c["label"] for c in cfg["template"]["callouts"] if c["id"] in g["excluded_callout_ids"]}
    terms = []
    for line in prose_body(text, cfg).splitlines():
        if line.startswith("#"):
            continue
        for t in re.findall(r"\*\*([^*]+?)\*\*", line):
            t = t.strip()
            if t.endswith(":") or t in excluded or t.endswith("."):
                continue
            terms.append(t)
    return terms


def load_glossary(path):
    if path is None or not path.exists():
        return set()
    return {m.lower() for m in re.findall(r"^\*\*(.+?)\*\*", path.read_text(encoding="utf-8"), re.M)}


def parse(text, cfg):
    """The parsed representation the renderer consumes (INV-30), keyed by section and callout IDs."""
    t = cfg["template"]
    by_label = {s["label"]: s for s in t["sections"]}
    h1 = re.search(t["chapter_heading_pattern"], text, re.M)
    secs, callouts = [], []
    lines = text.splitlines()
    for i, line in enumerate(lines):
        m = re.match(r"^## (.+?)\s*$", line)
        if m:
            s = by_label.get(m.group(1))
            secs.append({"id": s["id"] if s else None, "role": s["role"] if s else "core", "label": m.group(1), "line": i + 1})
        for c in t["callouts"]:
            if line.startswith(c["syntax"]):
                callouts.append({"id": c["id"], "line": i + 1, "parts": c["parts"]})
    body = sections(text)
    for s in secs:
        s["body"] = body.get(s["label"], "")
    keys = {}
    for m in re.finditer(r"^\*\*Q(\d+)\. (\S+?)\*\*", section_body(text, cfg, t["assessment"]["mcq"]["answers_section_role"] or "answers"), re.M):
        keys[int(m.group(1))] = m.group(2)
    return {"h1": {"num": h1.group("num"), "title": h1.group("title")} if h1 else None, "sections": secs,
            "callouts": callouts, "objectives": lo_ids(text, cfg),
            "mcqs": [int(n) for n in Q_ANY.findall(section_body(text, cfg, "assessment"))], "key": keys,
            "citations": sorted(cited_numbers(text, cfg)), "references": reference_entries(text, cfg),
            "glossary_terms": [{"term": x, "gloss": None} for x in glossary_terms(text, cfg)]
            if t["glossary"]["enabled"] else []}


# ---------- checks: each returns {id: [messages]} for the IDs it owns ----------

def check_template(text, cfg):
    t, f = cfg["template"], {i: [] for i in IDS["template"]}
    if not re.search(t["chapter_heading_pattern"], text, re.M):
        f["TPL-H1"].append("template: missing chapter heading")
    titles = list(sections(text))
    pos = []
    for s in t["sections"]:
        if not s["required"]:
            continue
        if s["label"] not in titles:
            f["TPL-SECTION-MISSING"].append(f"template: missing section '## {s['label']}'")
        else:
            pos.append(titles.index(s["label"]))
    if pos != sorted(pos):
        f["TPL-SECTION-ORDER"].append("template: required sections out of order")
    lines = text.splitlines()
    for c in t["callouts"]:
        n = sum(1 for line in lines if line.startswith(c["syntax"]))
        if c["required"] and n == 0:   # a marker line, not a mention in prose (S8-03)
            f["TPL-CALLOUT-MISSING"].append(f"template: missing box '{c['label']}'")
        elif n and ((c["min"] is not None and n < c["min"]) or (c["max"] is not None and n > c["max"])):
            f["TPL-CALLOUT-COUNT"].append(f"template: box '{c['label']}' appears {n}×, allowed {c['min']}–{c['max']}")
    return f


def check_perspectives(text, cfg):
    p, f = cfg["template"]["perspectives"], {i: [] for i in IDS["perspectives"]}
    if not p["enabled"]:
        return None
    counts = {}
    for item in p["items"]:
        m = re.search(rf"^> - \*\*{re.escape(item['label'])}:\*\*(.+)$", text, re.M)
        if not m:
            f["PERSP-MISSING"].append(f"lens missing: {item['label']}")
        else:
            counts[item["label"]] = tx.words(m.group(1), cfg["profile_out"])
    if counts and len(counts) == len(p["items"]):
        mean = sum(counts.values()) / len(counts)
        for label, n in counts.items():
            if abs(n - mean) > p["balance_tolerance"] * mean:
                f["PERSP-BALANCE"].append(f"lens imbalance: {label} {n} words vs mean {mean:.0f}")
    return f


def _lo_enabled(cfg):
    return cfg["template"]["learning_objectives"]["enabled"]


def check_objectives(text, cfg):
    lo, f = cfg["template"]["learning_objectives"], {i: [] for i in IDS["objectives"]}
    if not lo["enabled"]:
        return None
    ids = lo_ids(text, cfg)
    if not lo["min"] <= len(ids) <= lo["max"]:
        f["LO-COUNT"].append(f"LOs: {len(ids)} objectives, need {lo['min']}–{lo['max']}")
    verbs = lo["discouraged_verbs"] or cfg["profile_out"]["discouraged_objective_verbs"]
    for line in section_body(text, cfg, "objectives").splitlines():
        if LO_LINE.match(line):
            for v in verbs:
                if v in line.lower():
                    f["LO-VERB"].append(f"LOs: avoid '{v}': {line.strip()[:60]}")
    return f


def check_mcqs(text, cfg):
    a = cfg["template"]["assessment"]
    mcq, case = a["mcq"], a["case_question"]
    if not mcq["enabled"]:
        return None
    f = {i: [] for i in IDS["mcqs"]}
    f[NA] = set()
    if not _lo_enabled(cfg):
        f[NA] |= {"MCQ-LO-TAG", "MCQ-LO-UNKNOWN", "LO-UNASSESSED"}
    if not case["required"]:
        f[NA].add("MCQ-CASE")
    if not mcq["rationale_required"]:
        f[NA].add("KEY-RATIONALE")
    labels = mcq["option_labels"]
    sa = section_body(text, cfg, "assessment")
    ans = section_body(text, cfg, mcq["answers_section_role"])
    case_marker = f"**{case['label']}**" if case["required"] else None
    qs = {}
    for b in Q_START.split(sa):
        m = Q_HEAD.match(b)
        if not m:
            continue
        n = int(m.group(1))
        body = b.split(case_marker)[0] if case_marker else b
        opts = OPTION.findall(body)
        extra = [o for o in opts if o not in labels]
        if extra and not mcq["allow_other_labels"]:
            f["MCQ-EXTRA-OPTION"].append(f"Q{n}: option {', '.join(extra)} present")
        if [o for o in opts if o in labels] != labels:
            f["MCQ-OPTIONS"].append(f"Q{n}: options must be exactly {'/'.join(labels)}, found {''.join(opts)}")
        lo = LO_TAG.search(m.group(2))
        qs[n] = lo.group(1) if lo else None
        if not lo and _lo_enabled(cfg):
            f["MCQ-LO-TAG"].append(f"Q{n}: missing [LOn] tag")
    if len(qs) != mcq["count"]:
        f["MCQ-COUNT"].append(f"MCQ count {len(qs)}, need {mcq['count']}")
    if case_marker and not any(line.startswith(case_marker) for line in sa.splitlines()):
        f["MCQ-CASE"].append(f"missing {case_marker}")
    if _lo_enabled(cfg):
        ids = set(lo_ids(text, cfg))
        for n, lo in qs.items():
            if lo and lo not in ids:
                f["MCQ-LO-UNKNOWN"].append(f"Q{n}: tag LO{lo} not among objectives")
        for lo in ids:
            if lo not in qs.values():
                f["LO-UNASSESSED"].append(f"LO{lo} has no question")
    alt = "|".join(re.escape(x) for x in labels)
    keys = {}
    for m in re.finditer(rf"^\*\*Q(\d+)\. ({alt})\*\*\s*[—-]?\s*(.*)$", ans, re.M):
        keys[int(m.group(1))] = m.group(2)
        if mcq["rationale_required"] and tx.words(m.group(3), cfg["profile_out"]) < 1:
            f["KEY-RATIONALE"].append(f"Q{m.group(1)}: empty rationale")
    for n in qs:
        if n not in keys:
            f["KEY-MISSING"].append(f"Q{n}: no answer key")
    seq = [keys[n] for n in sorted(keys)]
    bal = mcq["key_balance"]
    for label in labels:
        c = seq.count(label)
        if seq and not bal["min"] <= c <= bal["max"]:
            f["KEY-BALANCE"].append(f"key imbalance: {label} correct {c}× (need {bal['min']}–{bal['max']})")
    run = mcq["max_run"]
    for i in range(len(seq) - run):
        if len(set(seq[i:i + run + 1])) == 1:
            f["KEY-RUN"].append(f"key run: {seq[i]} {run + 1} times from Q{sorted(keys)[i]}")
            break
    return f


def check_citations(text, cfg):
    if cfg["template"]["citations"]["style"] != "numeric-bracket":
        raise ConfigError(f"citations.style {cfg['template']['citations']['style']!r} is not supported")
    cited, refs = cited_numbers(text, cfg), {n for n, _ in reference_entries(text, cfg)}
    return {"CIT-MISSING": [f"missing reference {n}" for n in sorted(cited - refs)],
            "CIT-UNCITED": [f"uncited reference {n}" for n in sorted(refs - cited)]}


def check_sentences(text, cfg):
    f = {i: [] for i in IDS["sentences"]}
    r = cfg["template"]["readability"]
    prof = cfg["profile_out"]
    sents = [s for line in clean_prose_lines(text, cfg) for s in tx.sentences(line, prof)]
    if not sents:
        f["READ-NOPROSE"].append("sentences: no prose found")
        return f
    lens = [tx.words(s, prof) for s in sents]
    mean = sum(lens) / len(lens)
    long_share = sum(1 for n in lens if n > r["long_sentence_words"]) / len(lens)
    if mean > r["mean_sentence_max"]:
        f["READ-MEAN"].append(f"sentences: mean length {mean:.1f} > {r['mean_sentence_max']}")
    if long_share >= r["long_share_max"]:
        longest = max(sents, key=lambda s: tx.words(s, prof))
        f["READ-LONG"].append(f"sentences: {long_share:.0%} over {r['long_sentence_words']} words (e.g. '{longest[:80]}…')")
    return f


def _banned(cfg):
    return cfg["template"]["banned_terms"] + cfg["profile_out"]["banned_terms"]


def check_banned(text, cfg):
    return {"BANNED-TERM": [f"banned term: {b['pattern']} (use {b['replacement']})" for b in _banned(cfg)
                            if re.search(b["pattern"], text)]}


def _budget_range(budget, cfg):
    tol = cfg["template"]["budgets"]["tolerance"]
    return budget * (1 - tol), budget * (1 + tol)


def check_budget(text, cfg, budget):
    if not budget:
        return {"BUDGET-CHAPTER": []}
    n = words(text, cfg)
    lo, hi = _budget_range(budget, cfg)
    return {"BUDGET-CHAPTER": [] if lo <= n <= hi else [f"budget: {n} words, allowed {int(lo)}–{int(hi)}"]}


def check_glossary(text, cfg):
    if not cfg["template"]["glossary"]["enabled"]:
        return None
    known = load_glossary(cfg.book_file("glossary"))
    missing = sorted({t for t in glossary_terms(text, cfg) if t.lower() not in known})
    return {"GLOSS-MISSING": [f"glossary missing: {t}" for t in missing]}


def check_assets(text, cfg, path):
    f = {i: [] for i in IDS["assets"]}
    for link in IMAGE.findall(text):
        if re.match(r"^[a-z][a-z0-9+.-]*:", link, re.I) or link.startswith("#"):
            continue
        try:
            if not assemble.resolve_asset(path, link, cfg).is_file():
                f["ASSET-MISSING"].append(f"missing image: {link}")
        except assemble.AssetOutside as e:
            f["ASSET-OUTSIDE-ROOT"].append(str(e))
    return f


# TeX math between dollars (with a TeX sign inside, so prices pass), any control word (\frac, \alpha, \begin),
# display delimiters \[ \] \( \) (step9b fix S9b-04: a short allowlist missed most TeX)
LATEX = re.compile(r"\$[^$\n]*[\\_^{][^$\n]*\$|(?<![\w\\])\\[A-Za-z]+|\\[\[\]()]")
CODE_SPAN = re.compile(r"`[^`]*`")
VISUAL_BLOCKS = ("image", "table", "callout", "grid", "question")   # each breaks a prose run (plan Task 9b.5)


def _prose_lines(text, cfg):
    """Chapter lines before the references, outside code fences."""
    fence = False
    for line in no_refs(text, cfg).splitlines():
        s = line.strip()
        if s.startswith("```"):
            fence = not fence
            continue
        if not fence:
            yield s


def check_typography(text, cfg):
    """TYPO-LATEX: TeX left in the text; the writers print none of it (formulas use ~sub~ and ^sup^)."""
    hits = sorted({m.group(0) for s in _prose_lines(text, cfg) for m in LATEX.finditer(CODE_SPAN.sub("", s))})
    return {"TYPO-LATEX": [f"raw TeX in text: {h}" for h in hits[:10]]}


def check_rhythm(text, cfg):
    """RHYTHM-PROSE: words of consecutive paragraphs and list items, read with the writers' parser (blocks.parse), between
    two visual breaks (a figure, table, box, grid, boxed section or question) above template.readability.max_prose_run_words."""
    limit = cfg["template"]["readability"].get("max_prose_run_words")
    if not limit:
        return None
    from harness.tools import blocks   # blocks imports this module
    prof, out = cfg["profile_out"], []
    run, start, where, head, boxed = 0, None, None, None, False
    body = "\n".join(_prose_lines(prose_body(text, cfg), cfg))
    for b in blocks.parse(body, cfg, "chapter") + [{"t": "table"}]:
        t = b["t"]
        if t == "section":
            head, boxed = b["label"], b["boxed"]
        elif t == "h3":
            head = blocks.plain(b["text"])
        if t in VISUAL_BLOCKS or (t == "section" and boxed):
            if run > limit:
                out.append(f"{where or '(chapter start)'}: {run} words without a figure, table or box "
                           f"(starts '{start[:60]}…'), limit {limit}")
            run, start = 0, None
        elif t in ("para", "bullet", "numbered") and not boxed:
            s = blocks.plain(b.get("text") or b.get("body"))
            run += tx.words(s, prof)
            if start is None:
                start, where = s, head
    return {"RHYTHM-PROSE": out}


def pack_checks(text, cfg):
    """[(group, result)] from each figure pack in brief.figures.packs that checks text (TEXT_IDS, check_text)."""
    from harness.figures import packs
    on = set(cfg["brief"]["figures"]["packs"])
    out = []
    for name, mod in packs.text_packs().items():
        IDS.setdefault(f"pack:{name}", list(mod.TEXT_IDS))
        body = "\n".join(_prose_lines(text, cfg))
        out.append((f"pack:{name}", mod.check_text(body) if name in on else None))
    return out


# ---------- measured values (the golden records these, core §9.1) ----------

def measured(text, cfg, budget):
    lens = sentence_lengths(text, cfg)
    long = cfg["template"]["readability"]["long_sentence_words"]
    out = {"BUDGET-CHAPTER": {"words": words(text, cfg), "budget": budget},
           "READ-MEAN": {"mean_sentence": round(sum(lens) / len(lens), 3)} if lens else {},
           "READ-LONG": {"long_share": round(sum(1 for n in lens if n > long) / len(lens), 4)} if lens else {}}
    if _lo_enabled(cfg):
        out["LO-COUNT"] = {"lo_count": len(lo_ids(text, cfg))}
    mcq = cfg["template"]["assessment"]["mcq"]
    if mcq["enabled"]:
        alt = "|".join(re.escape(x) for x in mcq["option_labels"])
        keys = re.findall(rf"^\*\*Q\d+\. ({alt})\*\*", section_body(text, cfg, mcq["answers_section_role"]), re.M)
        out["MCQ-COUNT"] = {"mcq_count": len(set(Q_ANY.findall(section_body(text, cfg, "assessment"))))}
        out["KEY-BALANCE"] = {"key_counts": {k: keys.count(k) for k in mcq["option_labels"]}}
    return out


def _entries(target, groups, meas):
    out = []
    for group, result in groups:
        for cid in IDS[group]:
            if result is None:
                out.append({"id": cid, "status": "not_applicable", "message": "disabled in template.json", "measured": {}})
                continue
            if cid in result.get(NA, ()):
                out.append({"id": cid, "status": "not_applicable", "message": "disabled in template.json", "measured": {}})
                continue
            msgs = result.get(cid, [])
            out.append({"id": cid, "status": "fail" if msgs else "pass", "message": "; ".join(msgs),
                        "measured": meas.get(cid, {})})
    return {"schema_version": 1, "target": target, "checks": out}


def check_chapter(path, cfg, chapter):
    """checker-report.v1 for one chapter (`chapter` is its chapter-plan entry)."""
    text = pathlib.Path(path).read_text(encoding="utf-8")
    budget = chapter.get("word_budget") or 0
    groups = [("template", check_template(text, cfg)), ("perspectives", check_perspectives(text, cfg)),
              ("objectives", check_objectives(text, cfg)), ("mcqs", check_mcqs(text, cfg)),
              ("citations", check_citations(text, cfg)), ("sentences", check_sentences(text, cfg)),
              ("banned", check_banned(text, cfg)), ("budget", check_budget(text, cfg, budget)),
              ("glossary", check_glossary(text, cfg)), ("assets", check_assets(text, cfg, pathlib.Path(path))),
              ("typography", check_typography(text, cfg)), ("rhythm", check_rhythm(text, cfg))] + pack_checks(text, cfg)
    return _entries(chapter["id"], groups, measured(text, cfg, budget))


def errata_open(path, cfg):
    """Rows of the errata ledger whose status cell starts with an open value."""
    e = cfg["template"]["errata"]
    rows, col = [], None
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            col = None
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if col is None:
            col = cells.index(e["status_column"]) if e["status_column"] in cells else -1
            continue
        if col < 0 or col >= len(cells) or set(cells[col]) <= set("-: "):
            continue
        first = re.split(r"[\s(]", cells[col], maxsplit=1)[0]
        if first in e["open_values"]:
            rows.append(cells[0])
    return rows


def check_book_level(cfg, chapter_words):
    t = cfg["template"]
    f = {i: [] for i in IDS["book"]}
    na, missing_input = set(), set()
    meas = {}
    found = sorted(cfg.path("chapters").glob(t["paths"]["chapter_glob"]))
    planned = [p for _, p in cfg.chapters()]
    meas["BOOK-CHAPTER-COUNT"] = {"chapters": len(found)}
    if sorted(found) != sorted(planned):
        f["BOOK-CHAPTER-COUNT"].append(f"book: {len(found)} chapters, need {len(planned)} (chapter-plan.json)")
    total = sum(chapter_words)
    front = cfg.book_file("front_matter")
    if front is None:
        na |= {"BOOK-FRONT-MISSING", "BUDGET-FRONT"}
    elif front.exists():
        fw = words(front.read_text(encoding="utf-8"), cfg)
        total += fw
        meas["BUDGET-FRONT"] = {"words": fw, "budget": t["budgets"]["front_matter"]}
        if t["budgets"]["front_matter"]:
            lo, hi = _budget_range(t["budgets"]["front_matter"], cfg)
            if not lo <= fw <= hi:
                f["BUDGET-FRONT"].append(f"book: front matter {fw} words, allowed {int(lo)}–{int(hi)}")
    else:
        f["BOOK-FRONT-MISSING"].append(f"book: missing {t['paths']['front_matter']}")
        missing_input.add("BUDGET-FRONT")
    if t["budgets"]["front_matter"] is None:
        na.add("BUDGET-FRONT")
    meas["BUDGET-TOTAL"] = {"total_words": total}
    tot = t["budgets"]["total"]
    if tot is None:
        na.add("BUDGET-TOTAL")
    elif not tot["min"] <= total <= tot["max"]:
        f["BUDGET-TOTAL"].append(f"book: total {total} words, need {tot['min']:,}–{tot['max']:,}")
    if not t["errata"]["enabled"]:
        na.add("ERRATA-OPEN")
    else:
        ledger = cfg.book_file("errata")
        opened = errata_open(ledger, cfg) if ledger and ledger.exists() else None
        if opened is None or opened:
            f["ERRATA-OPEN"].append("book: errata ledger missing or has open rows"
                                    + (f" ({', '.join(opened)})" if opened else ""))
    g = t["glossary"]
    if not g["enabled"]:
        na.add("GLOSS-MIN")
    else:
        n = len(load_glossary(cfg.book_file("glossary")))
        meas["GLOSS-MIN"] = {"glossary_terms": n}
        if n < g["minimum_terms"]:
            f["GLOSS-MIN"].append(f"book: glossary has {n} entries, need ≥ {g['minimum_terms']}")
    rep = _entries("book", [("book", f)], meas)
    for c in rep["checks"]:
        if c["id"] in na:
            c.update(status="not_applicable", message="disabled in template.json", measured={})
        elif c["id"] in missing_input:   # S8-06: never `pass` without its input; BOOK-FRONT-MISSING carries the failure
            c.update(status="not_applicable", message="front matter file missing (see BOOK-FRONT-MISSING)", measured={})
    return rep, total


def check_book(cfg, chapter=None):
    """{schema_version, project, targets: [checker-report.v1 ...], total_words}; with `chapter`, that chapter only."""
    targets, cw = [], []
    for c, p in cfg.chapters():
        if chapter and c["id"] != chapter:
            continue
        targets.append(check_chapter(p, cfg, c))
        cw.append(words(p.read_text(encoding="utf-8"), cfg))
    if chapter and not targets:
        raise ConfigError(f"chapter {chapter!r} is not in chapter-plan.json")
    out = {"schema_version": 1, "project": cfg["project"].name, "targets": targets}
    if not chapter:
        book, total = check_book_level(cfg, cw)
        out["targets"].append(book)
        out["total_words"] = total
    return out


def blocking(checks):
    return [c for c in checks if c["status"] == "fail" and c["id"] not in NON_BLOCKING]


def failures(report, warnings=False):
    """[(target, check)] of blocking fails; `warnings=True`: the non-blocking fails instead."""
    return [(t["target"], c) for t in report["targets"] for c in t["checks"]
            if c["status"] == "fail" and (c["id"] in NON_BLOCKING) == warnings]


def main(project, argv):
    ap = argparse.ArgumentParser(prog="check_book.py")
    ap.add_argument("--chapter")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv[1:])
    try:
        report = check_book(config.load(project), a.chapter)
    except (ConfigError, KeyError, FileNotFoundError) as e:
        print(f"ERROR CONFIG: {e}", file=sys.stderr)
        return 2
    fails = failures(report)
    if a.json:
        print(json.dumps(report, ensure_ascii=False, indent=1, sort_keys=True))
    else:
        for target, c in fails:
            print(f"FAIL {target} {c['id']}: {c['message']}")
        for target, c in failures(report, warnings=True):
            print(f"WARN {target} {c['id']}: {c['message']}")
        if "total_words" in report:
            print(f"total words: {report['total_words']}")
        if not fails:
            print("PASS")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    from harness.gate import enforce
    PROJECT = enforce("rework", sys.argv)   # first call: no stage work before the gates pass
    sys.exit(main(PROJECT, sys.argv))
