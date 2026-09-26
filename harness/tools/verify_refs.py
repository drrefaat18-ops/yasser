"""Reference checks for chapters (plan Task 8.3; core §2.2 rework QA, §4.3 references, EXT-LOC-4). Stdlib only.

Usage: python harness/tools/verify_refs.py --project projects/<slug> [--chapter ID ...] [--json]
Every entry of a chapter's references section gets two separate results: DOI existence (`doi_status`) and title
match (`title_status`). A reference without an identifier passes only when its type (first matching pattern in
template.references.type_patterns) is in no_doi_policy.allowed_types and, if requires_url, it carries a URL;
otherwise REF-NO-DOI-DISALLOWED (fixes INV-46: the legacy tool printed NO DOI and passed).
Exit 0 when no reference has a blocking check ID; 1 otherwise or on a refused gate; 2 on a config error.
"""
import argparse, json, pathlib, re, sys, time, urllib.error, urllib.parse, urllib.request

REPO = pathlib.Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))
from harness import text as tx  # noqa: E402
from harness.tools import check_book, config  # noqa: E402

BLOCKING = {"REF-NOT-FOUND", "REF-ERROR", "REF-TITLE-MISMATCH", "REF-NO-DOI-DISALLOWED"}
URL = re.compile(r"https?://\S+")
TITLE_WORD = re.compile(r"[^\W_]+")


class ConfigError(Exception):
    pass


def providers(cfg):
    base = json.loads((REPO / "harness" / "defaults.json").read_text(encoding="utf-8"))["references"]["providers"]
    over = cfg["template"]["references"].get("providers") or {}
    return {k: {**v, **over.get(k, {})} for k, v in base.items()}


def crossref_title(doi, prov):
    """Title registered for `doi`, None when Crossref says 404; raises on network or parse failure."""
    url = prov["endpoint"] + urllib.parse.quote(doi, safe="/")
    req = urllib.request.Request(url, headers={"User-Agent": prov["user_agent"]})
    for attempt in range(prov["retries"]):
        try:
            with urllib.request.urlopen(req, timeout=prov["timeout_s"]) as r:
                msg = json.load(r)["message"]
            break
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            if e.code != 429 or attempt == prov["retries"] - 1:
                raise
            time.sleep(prov["backoff_s"] * (attempt + 1))  # rate limit
    time.sleep(0.5)
    return " ".join(msg.get("title") or [""])


def title_matches(line, title, cfg):
    tm = cfg["template"]["references"]["title_match"]
    if tm["mode"] != "heuristic":
        raise ConfigError(f"title_match.mode {tm['mode']!r} is implemented in STEP 10 (Arabic contract §5)")
    norm = lambda s: tx.normalise(s, cfg["profile_out"], "compare")
    want = [w for w in TITLE_WORD.findall(norm(title)) if len(w) > 2][:tm["words"]]
    have = set(TITLE_WORD.findall(norm(line)))
    return bool(want) and sum(w in have for w in want) / len(want) >= tm["threshold"]


def identifier(line, cfg):
    for pat in cfg["template"]["references"]["identifier_patterns"]:
        m = re.search(pat, line)
        if m:
            return next((g for g in m.groups() if g), m.group(0))
    return None


def ref_type(line, cfg):
    for kind, pat in (cfg["template"]["references"].get("type_patterns") or {}).items():
        if re.search(pat, line):
            return kind
    return None


def classify_line(n, line, cfg, fetch):
    doi = identifier(line, cfg)
    ref = {"n": n, "doi": doi, "type": None}
    if doi is None:
        pol = cfg["template"]["references"]["no_doi_policy"]
        kind = ref_type(line, cfg)
        ok = kind in pol["allowed_types"] and (URL.search(line) is not None or not pol["requires_url"])
        return dict(ref, type=kind, doi_status="no_doi", title_status="not_applicable",
                    check_id=None if ok else "REF-NO-DOI-DISALLOWED")
    try:
        title = fetch(doi)
    except Exception as e:  # network or parse failure: never a pass
        return dict(ref, doi_status="error", title_status="not_applicable", check_id="REF-ERROR", error=str(e)[:200])
    if title is None:
        return dict(ref, doi_status="not_found", title_status="not_applicable", check_id="REF-NOT-FOUND")
    if title_matches(line, title, cfg):
        return dict(ref, doi_status="exists", title_status="match", check_id=None)
    return dict(ref, doi_status="exists", title_status="mismatch", check_id="REF-TITLE-MISMATCH", registered_title=title[:120])


def default_fetch(cfg):
    prov = providers(cfg)["crossref"]
    return lambda doi: crossref_title(doi, prov)


def check_chapter(path, cfg, fetch=None):
    fetch = fetch or default_fetch(cfg)
    text = pathlib.Path(path).read_text(encoding="utf-8")
    return [classify_line(n, line, cfg, fetch) for n, line in check_book.reference_entries(text, cfg)]


def blocking(refs):
    return [r for r in refs if r["check_id"] in BLOCKING]


def summary(refs):
    out = {"total": len(refs), "exists": 0, "no_doi_allowed": 0}
    for r in refs:
        if r["doi_status"] == "exists" and r["check_id"] is None:
            out["exists"] += 1
        elif r["doi_status"] == "no_doi" and r["check_id"] is None:
            out["no_doi_allowed"] += 1
        if r["check_id"]:
            out[r["check_id"]] = out.get(r["check_id"], 0) + 1
    return out


def line_of(r):
    label = {"REF-NOT-FOUND": "NOT FOUND", "REF-TITLE-MISMATCH": "TITLE MISMATCH", "REF-ERROR": "ERROR",
             "REF-NO-DOI-DISALLOWED": "NO DOI DISALLOWED"}
    if r["check_id"]:
        return f"{label[r['check_id']]} {r['n']}" + (f": {r['doi']}" if r["doi"] else "")
    return f"OK {r['n']}" if r["doi"] else f"NO DOI ALLOWED {r['n']} ({r['type']})"


def main(project, argv):
    ap = argparse.ArgumentParser(prog="verify_refs.py")
    ap.add_argument("--chapter", action="append")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv[1:])
    try:
        cfg = config.load(project)
        chosen = [(c, p) for c, p in cfg.chapters() if not a.chapter or c["id"] in a.chapter]
        if a.chapter and len(chosen) != len(set(a.chapter)):
            raise ConfigError(f"unknown chapter in {a.chapter}")
        fetch = default_fetch(cfg)
        result = {c["id"]: check_chapter(p, cfg, fetch) for c, p in chosen}
    except (ConfigError, check_book.ConfigError, KeyError, FileNotFoundError) as e:
        print(f"ERROR CONFIG: {e}", file=sys.stderr)
        return 2
    if a.json:
        print(json.dumps({"schema_version": 1, "project": project.name, "chapters": result}, ensure_ascii=False, indent=1,
                         sort_keys=True))
    else:
        for cid, refs in result.items():
            for r in refs:
                print(f"{cid} {line_of(r)}")
    return 1 if any(blocking(refs) for refs in result.values()) else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    from harness.gate import enforce
    PROJECT = enforce("rework", sys.argv)   # first call: no stage work before the gates pass
    sys.exit(main(PROJECT, sys.argv))
