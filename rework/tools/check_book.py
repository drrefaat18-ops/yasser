"""Acceptance checks for rework chapters (spec §12). Stdlib only.

Usage:
  python rework/tools/check_book.py rework/ch04-....md [--budget N] [--glossary PATH]
  python rework/tools/check_book.py --all
"""
import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
BUDGETS = {1: 2000, 2: 2000, 3: 2400, 4: 2700, 5: 2400, 6: 2800,
           7: 2400, 8: 2400, 9: 2300, 10: 2200, 11: 2400}
FRONT_BUDGET = 500
REQUIRED_H2 = ["Opening Case", "Learning Objectives", "Key Takeaways",
               "Self-Assessment", "Answers and Rationales", "References"]
BOXES = ["Medical Background in 60 Seconds:", "Through Four Lenses",
         "Myth vs Evidence:", "Safety Alert:"]
LENSES = ["Medicine", "Pharmacy", "Physical Therapy", "Health Sciences"]
WORD = re.compile(r"[A-Za-z0-9][A-Za-z0-9'’\-–./%]*")


def sections(text):
    """Map H2 title -> body text; order preserved."""
    out, cur = {}, None
    for line in text.splitlines():
        m = re.match(r"^## (.+?)\s*$", line)
        if m:
            cur = m.group(1)
            out[cur] = []
        elif cur is not None:
            out[cur].append(line)
    return {k: "\n".join(v) for k, v in out.items()}


def split_at(text, heading):
    i = text.find(f"\n## {heading}")
    return (text, "") if i < 0 else (text[:i], text[i:])


def no_refs(text):
    return split_at(text, "References")[0]


def prose_body(text):
    return split_at(text, "Self-Assessment")[0]


def words(text):
    return len(WORD.findall(no_refs(text)))


def check_budget(text, budget):
    if not budget:
        return []
    n = words(text)
    lo, hi = budget * 0.85, budget * 1.15
    return [] if lo <= n <= hi else [f"budget: {n} words, allowed {int(lo)}–{int(hi)}"]


def clean_prose_lines(text):
    out, fence = [], False
    for line in prose_body(text).splitlines():
        s = line.strip()
        if s.startswith("```"):
            fence = not fence
            continue
        if fence or not s or s.startswith("#") or s.startswith("|") or s.startswith("!["):
            continue
        s = re.sub(r"^>\s?", "", s)
        s = re.sub(r"^[-*]\s+|^\d+\.\s+", "", s)
        s = re.sub(r"\*\*[^*]+?:\*\*", "", s)          # labels
        s = re.sub(r"\[LO\d+\]", "", s)
        s = re.sub(r"[*_`]", "", s)
        if s:
            out.append(s)
    return out


def check_sentences(text):
    sents = []
    for line in clean_prose_lines(text):
        sents += [s for s in re.split(r"(?<=[.!?])\s+", line) if WORD.search(s)]
    if not sents:
        return ["sentences: no prose found"]
    lens = [len(WORD.findall(s)) for s in sents]
    mean = sum(lens) / len(lens)
    long_share = sum(1 for n in lens if n > 40) / len(lens)
    fails = []
    if mean > 22:
        fails.append(f"sentences: mean length {mean:.1f} > 22")
    if long_share >= 0.05:
        longest = max(sents, key=lambda s: len(WORD.findall(s)))
        fails.append(f"sentences: {long_share:.0%} over 40 words (e.g. '{longest[:80]}…')")
    return fails


def check_template(text):
    fails = []
    if not re.search(r"^# Chapter \d+: .+", text, re.M):
        fails.append("template: missing '# Chapter N: Title'")
    titles = list(sections(text))
    pos = []
    for h in REQUIRED_H2:
        if h not in titles:
            fails.append(f"template: missing section '## {h}'")
        else:
            pos.append(titles.index(h))
    if pos != sorted(pos):
        fails.append("template: required sections out of order")
    for b in BOXES:
        if f"> **{b}**" not in text:
            fails.append(f"template: missing box '{b}'")
    return fails


def check_lenses(text):
    counts, fails = {}, []
    for lens in LENSES:
        m = re.search(rf"^> - \*\*{re.escape(lens)}:\*\*(.+)$", text, re.M)
        if not m:
            fails.append(f"lens missing: {lens}")
        else:
            counts[lens] = len(WORD.findall(m.group(1)))
    if len(counts) == 4:
        mean = sum(counts.values()) / 4
        for lens, n in counts.items():
            if abs(n - mean) > 0.2 * mean:
                fails.append(f"lens imbalance: {lens} {n} words vs mean {mean:.0f}")
    return fails


def lo_ids(text):
    return re.findall(r"^\d+\. \[LO(\d+)\]", sections(text).get("Learning Objectives", ""), re.M)


def check_los(text):
    los = sections(text).get("Learning Objectives", "")
    ids = lo_ids(text)
    fails = [] if 3 <= len(ids) <= 5 else [f"LOs: {len(ids)} objectives, need 3–5"]
    for line in los.splitlines():
        if re.match(r"^\d+\. \[LO\d+\]", line) and "understand" in line.lower():
            fails.append(f"LOs: avoid 'understand': {line.strip()[:60]}")
    return fails


def check_mcqs(text):
    sa = sections(text).get("Self-Assessment", "")
    ans = sections(text).get("Answers and Rationales", "")
    fails = []
    blocks = re.split(r"^(?=\*\*Q\d+\.\*\*)", sa, flags=re.M)
    qs = {}
    for b in blocks:
        m = re.match(r"\*\*Q(\d+)\.\*\*(.*)", b)
        if not m:
            continue
        n = int(m.group(1))
        body = b.split("**Case Question.**")[0]
        opts = re.findall(r"^([A-Z])\) ", body, re.M)
        if "E" in opts:
            fails.append(f"Q{n}: option E present")
        if opts[:4] != ["A", "B", "C", "D"] or len([o for o in opts if o != "E"]) != 4:
            fails.append(f"Q{n}: options must be exactly A–D, found {''.join(opts)}")
        lo = re.search(r"\[LO(\d+)\]", m.group(2))
        qs[n] = lo.group(1) if lo else None
        if not lo:
            fails.append(f"Q{n}: missing [LOn] tag")
    if len(qs) != 10:
        fails.append(f"MCQ count {len(qs)}, need 10")
    if "**Case Question.**" not in sa:
        fails.append("missing **Case Question.**")
    ids = set(lo_ids(text))
    for n, lo in qs.items():
        if lo and lo not in ids:
            fails.append(f"Q{n}: tag LO{lo} not among objectives")
    for lo in ids:
        if lo not in qs.values():
            fails.append(f"LO{lo} has no question")
    keys = {}
    for m in re.finditer(r"^\*\*Q(\d+)\. ([A-D])\*\*\s*[—-]?\s*(.*)$", ans, re.M):
        keys[int(m.group(1))] = m.group(2)
        if len(WORD.findall(m.group(3))) < 1:
            fails.append(f"Q{m.group(1)}: empty rationale")
    for n in qs:
        if n not in keys:
            fails.append(f"Q{n}: no answer key")
    seq = [keys[n] for n in sorted(keys)]
    for letter in "ABCD":
        c = seq.count(letter)
        if seq and not 2 <= c <= 3:
            fails.append(f"key imbalance: {letter} correct {c}× (need 2–3)")
    for i in range(len(seq) - 2):
        if seq[i] == seq[i + 1] == seq[i + 2]:
            fails.append(f"key run: {seq[i]} three times from Q{sorted(keys)[i]}")
            break
    return fails


def cited_numbers(text):
    nums = set()
    for grp in re.findall(r"\[(\d+(?:\s*[,–-]\s*\d+)*)\]", no_refs(text)):
        for part in re.split(r"\s*,\s*", grp):
            r = re.split(r"\s*[–-]\s*", part)
            if len(r) == 2:
                nums.update(range(int(r[0]), int(r[1]) + 1))
            else:
                nums.add(int(r[0]))
    return nums


def ref_numbers(text):
    return {int(n) for n in re.findall(r"^(\d+)\. ", sections(text).get("References", ""), re.M)}


def check_citations(text):
    cited, refs = cited_numbers(text), ref_numbers(text)
    fails = [f"missing reference {n}" for n in sorted(cited - refs)]
    fails += [f"uncited reference {n}" for n in sorted(refs - cited)]
    return fails


def glossary_terms(text):
    body = prose_body(text)
    terms = []
    for line in body.splitlines():
        if line.startswith("#"):
            continue
        for t in re.findall(r"\*\*([^*]+?)\*\*", line):
            t = t.strip()
            if t.endswith(":") or t == "Through Four Lenses" or t.endswith("."):
                continue
            terms.append(t)
    return terms


def load_glossary(path):
    p = pathlib.Path(path)
    if not p.exists():
        return set()
    return {m.lower() for m in re.findall(r"^\*\*(.+?)\*\*", p.read_text(encoding="utf-8"), re.M)}


def check_glossary(text, glossary_path):
    known = load_glossary(glossary_path)
    missing = sorted({t for t in glossary_terms(text) if t.lower() not in known})
    return [f"glossary missing: {t}" for t in missing]


def check_banned(text):
    return ["banned term: master-slave (use leader–follower)"] if re.search(r"master[-–]slave", text, re.I) else []


def check_chapter(path, budget=None, glossary=None):
    text = pathlib.Path(path).read_text(encoding="utf-8")
    if budget is None:
        m = re.search(r"ch(\d+)", pathlib.Path(path).name)
        budget = BUDGETS.get(int(m.group(1)), 0) if m else 0
    glossary = glossary or ROOT / "glossary.md"
    fails = []
    for fn in (check_template, check_lenses, check_los, check_mcqs, check_citations, check_sentences, check_banned):
        fails += fn(text)
    fails += check_budget(text, budget)
    fails += check_glossary(text, glossary)
    return fails


def check_all():
    fails, total = [], 0
    chapters = sorted(ROOT.glob("ch*.md"))
    if len(chapters) != 11:
        fails.append(f"book: {len(chapters)} chapters, need 11")
    for ch in chapters:
        fails += [f"{ch.name}: {f}" for f in check_chapter(ch)]
        total += words(ch.read_text(encoding="utf-8"))
    front = ROOT / "00-front-matter.md"
    if front.exists():
        total += words(front.read_text(encoding="utf-8"))
    else:
        fails.append("book: missing 00-front-matter.md")
    if not 24000 <= total <= 29000:
        fails.append(f"book: total {total} words, need 24,000–29,000")
    ledger = ROOT / "errata-ledger.md"
    if not ledger.exists() or "| open |" in ledger.read_text(encoding="utf-8"):
        fails.append("book: errata ledger missing or has open rows")
    if len(load_glossary(ROOT / "glossary.md")) < 120:
        fails.append(f"book: glossary has {len(load_glossary(ROOT / 'glossary.md'))} entries, need ≥ 120")
    print(f"total words: {total}")
    return fails


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("path", nargs="?")
    ap.add_argument("--budget", type=int)
    ap.add_argument("--glossary")
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()
    if a.all:
        fails = check_all()
    elif a.path and pathlib.Path(a.path).exists():
        fails = check_chapter(a.path, a.budget, a.glossary)
    else:
        fails = [f"file not found: {a.path}"]
    for f in fails:
        print(f)
    if not fails:
        print("PASS")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
