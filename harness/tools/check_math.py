"""Symbolic check of the numbers a book prints (plan Task 9c.1). Emits one checker-report.v1 document,
target `math`.

Usage: python harness/tools/check_math.py --project projects/<slug> [--file F] [--json]

The book states a claim about its own arithmetic in a fenced ```math-check block, and this tool
recomputes it with SymPy. The blocks live in `math-checks.md` beside the chapters, not inside them,
so that they never reach the assembled book and never count against a chapter's word budget. The
block is declarative, never executed as Python:

    ```math-check
    label: ch10 Example 10.1 - time to halve from 6 mg/L
    given: Vd=45, Vmax=500, Km=4, C0=6
    expr:  (Vd/Vmax)*(Km*log(2) + C0/2)*24
    expect: 12.5 +- 0.05
    ```

`given` binds names, `expr` is the quantity under test and `expect` is what the chapter prints.
`expect: exact <expr>` compares symbolically instead of numerically, so `1/3` does not have to be
rounded. Every name in `expr` must be bound in `given`; an unbound name is an error, not a free
symbol, because a typo would otherwise pass as algebra.

Checks:
  MATH-SYNTAX   a block is missing a key, or an expression does not parse
  MATH-UNBOUND  an expression uses a name `given` does not bind
  MATH-MISMATCH the recomputed value is not what the chapter prints
Exit 0 iff every check passes; 1 otherwise or on a refused gate; 2 on a config error.
"""
import json, pathlib, re, sys

REPO = pathlib.Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))
from harness.tools import config  # noqa: E402

IDS = ["MATH-SYNTAX", "MATH-UNBOUND", "MATH-MISMATCH"]
CHECKS_FILE = "math-checks.md"   # beside the chapters; absent means the book declares no checks
BLOCK = re.compile(r"^```math-check[ \t]*\n(.*?)^```[ \t]*$", re.M | re.S)
TOL = re.compile(r"^(?P<value>.+?)\s*(?:\+-|±)\s*(?P<tol>[^\s]+)$")
KEYS = ("label", "given", "expr", "expect")


def _parse_block(body):
    """-> {key: text}; later lines continue the previous key when indented."""
    out, key = {}, None
    for raw in body.split("\n"):
        if not raw.strip():
            continue
        m = re.match(r"^(\w+):\s*(.*)$", raw)
        if m and m.group(1) in KEYS:
            key = m.group(1)
            out[key] = m.group(2).strip()
        elif key:
            out[key] += " " + raw.strip()
    return out


def _bindings(text, sympify, problems, where):
    """`a=1, b=2` -> {name: expression}, each parsed in the namespace built so far."""
    env = {}
    for part in _split_top(text):
        if not part.strip():
            continue
        if "=" not in part:
            problems.append(("MATH-SYNTAX", f"{where}: `given` item is not an assignment: {part.strip()}"))
            continue
        name, expr = part.split("=", 1)
        name = name.strip()
        try:
            env[name] = sympify(expr.strip(), locals=dict(env))
        except Exception as e:                                    # noqa: BLE001 - reported, never raised
            problems.append(("MATH-SYNTAX", f"{where}: cannot parse `{name}`: {e}"))
    return env


def _split_top(text):
    """Split on commas that are not inside brackets, so `f(a, b)` stays one item."""
    out, depth, cur = [], 0, ""
    for c in text:
        if c in "([{":
            depth += 1
        elif c in ")]}":
            depth -= 1
        if c == "," and depth == 0:
            out.append(cur)
            cur = ""
        else:
            cur += c
    return out + [cur]


def _names(expr):
    return {s.name for s in expr.free_symbols}


def check_text(text, where, found):
    import sympy
    from sympy import sympify

    for m in BLOCK.finditer(text):
        b = _parse_block(m.group(1))
        label = b.get("label") or f"{where}: unlabelled block"
        missing = [k for k in ("given", "expr", "expect") if k not in b]
        if missing:
            found["MATH-SYNTAX"].append(f"{label}: missing {', '.join(missing)}")
            continue
        problems = []
        env = _bindings(b["given"], sympify, problems, label)
        for cid, msg in problems:
            found[cid].append(msg)
        try:
            expr = sympify(b["expr"], locals=dict(env))
        except Exception as e:                                    # noqa: BLE001
            found["MATH-SYNTAX"].append(f"{label}: cannot parse `expr`: {e}")
            continue
        unbound = sorted(_names(expr) - set(env))
        if unbound:
            found["MATH-UNBOUND"].append(f"{label}: `expr` uses unbound {', '.join(unbound)}")
            continue
        got = expr.subs(env)
        want_text = b["expect"]
        exact = want_text.startswith("exact ")
        try:
            if exact:
                want = sympify(want_text[len("exact "):].strip(), locals=dict(env)).subs(env)
                ok = sympy.simplify(got - want) == 0
                shown = want
            else:
                t = TOL.match(want_text)
                want = sympify((t.group("value") if t else want_text).strip(), locals=dict(env)).subs(env)
                tol = float(sympify(t.group("tol"), locals=dict(env))) if t else 5e-3 * abs(float(want))
                ok = abs(float(got) - float(want)) <= tol
                shown = f"{float(want):g} +- {tol:g}"
        except Exception as e:                                    # noqa: BLE001
            found["MATH-SYNTAX"].append(f"{label}: cannot compare with `expect`: {e}")
            continue
        if not ok:
            value = got if exact else f"{float(got):g}"
            found["MATH-MISMATCH"].append(f"{label}: chapter prints {shown}, SymPy gives {value}")


def check(cfg, files):
    found = {i: [] for i in IDS}
    for path in files:
        check_text(path.read_text(encoding="utf-8"), path.name, found)
    checks = [{"id": i, "status": "fail" if found[i] else "pass", "message": "; ".join(found[i]),
               "measured": {"count": len(found[i])}} for i in IDS]
    checks[0]["measured"]["blocks"] = sum(len(BLOCK.findall(p.read_text(encoding="utf-8"))) for p in files)
    return {"schema_version": 1, "target": "math", "checks": checks}


def files(cfg):
    """-> [path] the book's declared checks file, or [] when it declares none."""
    f = cfg.path("chapters") / CHECKS_FILE
    return [f] if f.is_file() else []


def failures(report):
    return [c for c in report["checks"] if c["status"] == "fail"]


def main(project, argv):
    import argparse
    ap = argparse.ArgumentParser(prog="check_math.py")
    ap.add_argument("--file", action="append", help=f"check this file instead of {CHECKS_FILE}")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv[1:])
    try:
        cfg = config.load(project)
        if a.file:
            files = [pathlib.Path(f) for f in a.file]
            for f in files:
                if not f.is_file():
                    raise FileNotFoundError(f"{f} missing")
        else:
            default = cfg.path("chapters") / CHECKS_FILE
            files = [default] if default.is_file() else []
        report = check(cfg, files)
    except (config.ConfigError, KeyError, FileNotFoundError) as e:
        print(f"ERROR CONFIG: {e}", file=sys.stderr)
        return 2
    if a.json:
        print(json.dumps(report, ensure_ascii=False, indent=1))
    else:
        for c in report["checks"]:
            print(f"{c['status']:4} {c['id']}" + (f": {c['message']}" if c["message"] else ""))
    return 1 if failures(report) else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    from harness.gate import enforce
    PROJECT = enforce("build", sys.argv)
    sys.exit(main(PROJECT, sys.argv))
