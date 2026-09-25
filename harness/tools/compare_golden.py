"""Walk two golden JSON trees and report every difference (core §9.2, plan N7/N8)."""
import argparse, fnmatch, json, sys

_MISSING = object()


def _walk(a, b, ptr, out):
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            _walk(a.get(k, _MISSING), b.get(k, _MISSING), f"{ptr}/{k}", out)
    elif isinstance(a, list) and isinstance(b, list):
        for i in range(max(len(a), len(b))):
            _walk(a[i] if i < len(a) else _MISSING, b[i] if i < len(b) else _MISSING, f"{ptr}/{i}", out)
    elif a != b:
        out.append((ptr or "/", None if a is _MISSING else a, None if b is _MISSING else b))


def _project_checks(b, checks_from):
    keep = {(c["id"], c["target"]) for c in checks_from.get("checks", [])}
    kept = [c for c in b.get("checks", []) if (c["id"], c["target"]) in keep]
    extra = [c for c in b.get("checks", []) if (c["id"], c["target"]) not in keep]
    return dict(b, checks=kept), extra


def diff(a, b, allow, *, checks_from=None):
    a = {k: v for k, v in a.items() if k != "provenance"}
    b = {k: v for k, v in b.items() if k != "provenance"}
    extra = []
    if checks_from is not None:
        b, extra = _project_checks(b, checks_from)
    found = []
    _walk(a, b, "", found)
    diffs = []
    for ptr, before, after in found:
        rule = next((r for r in allow if fnmatch.fnmatchcase(ptr, r["pointer_glob"])), None)
        diffs.append(dict(pointer=ptr, before=before, after=after,
                          allowed=rule is not None, reason=rule["reason"] if rule else ""))
    for c in extra:
        if c["status"] not in ("pass", "not_applicable"):
            diffs.append(dict(pointer=f"/checks/+{c['id']}@{c['target']}", before=None, after=c["status"],
                              allowed=False, reason="new check ID must pass (plan N7)"))
    return {"schema_version": 1, "diffs": diffs}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("a"); ap.add_argument("b")
    ap.add_argument("--allow", required=True)
    ap.add_argument("--checks-from")
    ap.add_argument("--out")
    x = ap.parse_args()
    load = lambda p: json.load(open(p, encoding="utf-8"))
    allow = load(x.allow)
    allow = allow.get("expected_diff") if isinstance(allow, dict) else allow
    if not isinstance(allow, list) or any(not isinstance(r, dict) or set(r) != {"pointer_glob", "reason"} for r in allow):
        print("ERROR ALLOWLIST: expected a list (or a manifest's expected_diff) of {pointer_glob, reason}", file=sys.stderr)
        sys.exit(2)
    result = diff(load(x.a), load(x.b), allow, checks_from=load(x.checks_from) if x.checks_from else None)
    text = json.dumps(result, ensure_ascii=False, indent=1, sort_keys=True)
    if x.out:
        open(x.out, "w", encoding="utf-8", newline="\n").write(text + "\n")
    for d in result["diffs"]:
        print(("ALLOWED " if d["allowed"] else "DIFF ") + d["pointer"])
    sys.exit(0 if all(d["allowed"] for d in result["diffs"]) else 1)


if __name__ == "__main__":
    main()
