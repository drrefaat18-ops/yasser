"""Checks shared by the evaluate and audit completers (core §5.4, §8; Fix Protocol tables, DEC-030)."""
import json, re
from harness import hashing, schema, state

CLOSED = {"fixed + verified", "rejected", "ruled by user"}
HEADER_KEYS = ("reviewed_commit", "verdict", "open_blocker_major", "reviewer_model")


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate_file(path, name):
    if not path.is_file():
        return None, [f"SCHEMA {path.name}: missing"]
    try:
        doc = read_json(path)
    except json.JSONDecodeError as e:
        return None, [f"SCHEMA {path.name}: not JSON ({e})"]
    return doc, [f"SCHEMA {path.name}{e}" for e in schema.validate(doc, schema.load_schema(name))]


def table(path, first_col):
    """Rows of the first Markdown table whose header starts with `| <first_col> |`, as dicts keyed by header."""
    if not path.is_file():
        return []
    lines = [l.strip() for l in path.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")]
    cells = lambda l: [c.strip() for c in l.strip("|").split("|")]
    for i, l in enumerate(lines):
        if l.startswith("|") and cells(l)[0] == first_col:
            head, rows = cells(l), []
            for r in lines[i + 2:]:
                if not r.startswith("|"):
                    break
                rows.append(dict(zip(head, cells(r))))
            return rows
    return []


def fixes_rows(project, path):
    """-> ({finding_id: status}, problems). A `ruled by user` row needs a DEC that exists in decisions.md."""
    rows, probs = {}, []
    for r in table(path, "ID"):
        fid, status = r.get("ID", ""), r.get("status", r.get("fix", "")).strip().lower()
        rows[fid] = status
        if status == "ruled by user":
            dec = r.get("DEC", "").strip()
            try:
                if not re.fullmatch(r"DEC-\d{3,}", dec):
                    raise state.GateError("DEC-MISSING", "no DEC cited")
                state.dec_row_hash(project, dec)
            except state.GateError as e:
                probs.append(f"RULING-NO-DEC {path.name} {fid}: `ruled by user` needs a DEC row in decisions.md ({e})")
    return rows, probs


def rulings(project, path):
    """{finding_id: dec_row_sha256} for every `ruled by user` row; recorded so an edited ruling row stales the receipt."""
    out = {}
    for r in table(path, "ID"):
        if r.get("status", "").strip().lower() == "ruled by user" and r.get("DEC"):
            try:
                out[r["ID"]] = {"dec_id": r["DEC"], "dec_row_sha256": state.dec_row_hash(project, r["DEC"])[0]}
            except state.GateError:
                pass  # reported by fixes_rows
    return out


def review_header(path):
    """`key: value` header lines of a saved review (reviewed_commit, verdict, open_blocker_major, reviewer_model)."""
    out = {}
    if path.is_file():
        for line in path.read_text(encoding="utf-8").splitlines():
            m = re.match(r"^\s*(" + "|".join(HEADER_KEYS) + r")\s*:\s*(.+?)\s*$", line)
            if m and m.group(1) not in out:
                out[m.group(1)] = m.group(2)
    return out


def review_gate(project, review, fixes):
    """Every blocker/major finding in the saved review has a closed row in fixes.md (Fix Protocol)."""
    probs = []
    head = review_header(review)
    for k in ("verdict", "open_blocker_major", "reviewer_model"):
        if not head.get(k):
            probs.append(f"REVIEW-HEADER {review.name}: `{k}:` line missing")
    rows, rprobs = fixes_rows(project, fixes)
    probs += rprobs
    sev_col = lambda r: next((v for k, v in r.items() if k.lower().startswith("severity")), "")
    found = table(review, "ID")
    serious = sum(sev_col(r).strip().lower() in ("blocker", "major") for r in found)
    verdict, count = head.get("verdict", "").lower(), head.get("open_blocker_major", "")
    if verdict and verdict not in ("pass", "fail"):
        probs.append(f"REVIEW-HEADER {review.name}: verdict {verdict!r} must be pass or fail")
    if count and not count.isdigit():
        probs.append(f"REVIEW-HEADER {review.name}: open_blocker_major {count!r} is not a number")
    elif count and int(count) != serious:   # a header that counts findings the table does not carry cannot be fixed row by row
        probs.append(f"REVIEW-HEADER {review.name}: open_blocker_major {count} but the findings table has {serious} "
                     "blocker/major rows")
    if verdict in ("pass", "fail") and count.isdigit() and (verdict == "fail") != (int(count) > 0):
        probs.append(f"REVIEW-HEADER {review.name}: verdict {verdict} contradicts open_blocker_major {count}")
    for r in found:
        if sev_col(r).strip().lower() in ("blocker", "major") and rows.get(r["ID"]) not in CLOSED:
            probs.append(f"FIX-OPEN {r['ID']}: {sev_col(r)} review finding has no closed row in {fixes.name} "
                         f"(status must be one of {sorted(CLOSED)})")
    return head, rows, probs


def score(rubric, scorecard, findings, fixes):
    """Core §5.4: pillar set, score range, hard caps against open findings, and the weighted total."""
    probs = []
    pillars = {p["id"]: p for p in rubric["pillars"]}
    card = {p["id"]: p for p in scorecard["pillars"]}
    if len(card) != len(scorecard["pillars"]):
        probs.append("scorecard lists a pillar more than once")
    if set(card) != set(pillars):
        probs.append(f"scorecard pillars {sorted(card)} != rubric pillars {sorted(pillars)}")
    ids = {f["id"] for f in findings}
    for pid, c in card.items():
        missing = sorted(set(c.get("evidence_finding_ids", [])) - ids)
        if missing:
            probs.append(f"{pid}: evidence cites unknown findings {missing}")
        p = pillars.get(pid)
        if p and c.get("applicable", True) != p["applicable"]:
            probs.append(f"{pid}: applicable {c.get('applicable')} but the rubric says {p['applicable']}")
        s = c.get("score")
        if p and p["applicable"] and (s is None or not 1 <= s <= 10 or (s * 2) % 1):
            probs.append(f"{pid}: score {s} must be 1-10 in 0.5 steps")
    caps = scorecard.get("caps_applied", [])
    listed = {(c["pillar_id"], c["cap_index"]): c for c in caps}
    if len(listed) != len(caps):
        probs.append("caps_applied lists a cap more than once")
    for pid, p in pillars.items():
        for i, cap in enumerate(p.get("hard_caps", [])):
            t = cap["trigger"]
            hits = [f["id"] for f in findings if f["pillar_id"] == pid and f["severity"] == t["severity"]
                    and (t["tag"] is None or t["tag"] in f.get("tags", [])) and fixes.get(f["id"]) != "fixed + verified"]
            fires = len(hits) >= t["min_count"]
            if fires and (pid, i) not in listed:
                probs.append(f"{pid}: hard cap {i} fires ({hits}) but is not in caps_applied")
            elif fires and sorted(listed[(pid, i)].get("finding_ids", [])) != sorted(hits):
                probs.append(f"{pid}: caps_applied cap {i} cites {listed[(pid, i)].get('finding_ids')}, "
                             f"the triggering findings are {hits}")
            if not fires and (pid, i) in listed:
                probs.append(f"{pid}: caps_applied lists cap {i}, which does not fire")
            s = card.get(pid, {}).get("score")
            if fires and s is not None and s > cap["max_score"]:
                probs.append(f"{pid}: score {s} exceeds hard cap {i} max {cap['max_score']}")
    total = round(sum(card[i]["score"] * p["weight"] for i, p in pillars.items()
                      if p["applicable"] and card.get(i, {}).get("score") is not None) / 10, 1)
    if abs(total - scorecard.get("total", -1)) > 0.05:
        probs.append(f"total {scorecard.get('total')} != computed {total}")
    return probs


def findings_scorecard(project, stage_dir, review_name, kind):
    """Shared evaluate/audit checks -> (extras, problems)."""
    d = project / stage_dir
    rubric = read_json(project / "rubric.json")
    fdoc, probs = validate_file(d / "findings.json", "findings")
    card, p2 = validate_file(d / "scorecard.json", "scorecard")
    probs += p2
    if probs:
        return {}, probs
    findings = fdoc["findings"]
    pillar_ids = {p["id"] for p in rubric["pillars"]}
    seen = {}
    for f in findings:
        if f["pillar_id"] not in pillar_ids:
            probs.append(f"{f['id']}: pillar_id {f['pillar_id']!r} is not a rubric pillar")
        key = (f["location"]["file"], f["location"]["line_start"], f["claim"].strip().lower())
        if key in seen:
            probs.append(f"{f['id']}: same location and claim as {seen[key]}; merge them, keeping the pillar by "
                         "the overlap order (core §5.3)")
        seen.setdefault(key, f["id"])
    if len({f["id"] for f in findings}) != len(findings):
        probs.append("findings.json: duplicate finding IDs")
    digest = hashing.hash_file(project / "rubric.json")
    if card["rubric_digest"] != digest:
        probs.append(f"scorecard rubric_digest {card['rubric_digest'][:12]}… != rubric.json {digest[:12]}…")
    if card["review_kind"] != kind:
        probs.append(f"scorecard review_kind must be {kind!r}")
    head, rows, p3 = review_gate(project, d / review_name, d / "fixes.md")
    probs += p3
    probs += score(rubric, card, findings, rows)
    extras = {"rubric_digest": digest, "reviewer_model": head.get("reviewer_model", ""),
              "rulings": rulings(project, d / "fixes.md")}
    return extras, probs
