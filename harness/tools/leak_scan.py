"""Scoped leak scan over shared production code and schemas (core §9.5, Rule 8). Stdlib only; reads no project.

Usage: python harness/tools/leak_scan.py [--root DIR]
Scope: harness/**/*.py, harness/**/*.json, harness/agents/*.md, .claude/skills/book-*/**.
Fails on any term in tests/fixtures/leak/forbidden.txt (case-insensitive, at word boundaries; a trailing * matches any
word starting with the term) and on absolute paths. Prints `path:line: literal`.
Exit 0 clean; 1 on any hit; 2 if the term list is missing.
"""
import argparse, pathlib, re, sys

ABSOLUTE = [re.compile(r"(?<![A-Za-z])[A-Za-z]:\\"), re.compile(r"/(?:Users|home)/")]
SCOPE = [("harness", "**/*.py"), ("harness", "**/*.json"), ("harness/agents", "*.md"), (".claude/skills", "book-*/**/*")]


def files(root):
    seen = set()
    for base, pattern in SCOPE:
        for p in sorted((root / base).glob(pattern)):
            if p.is_file() and "__pycache__" not in p.parts and p not in seen:
                seen.add(p)
                yield p


def compile_terms(lines):
    out = []
    for t in (x.strip() for x in lines):
        if not t or t.startswith("#"):
            continue
        prefix = t.endswith("*")
        body = re.escape(t.rstrip("*")).replace(r"\ ", r"\s+")
        out.append((t, re.compile(rf"(?<![A-Za-z0-9]){body}" + ("" if prefix else r"(?![A-Za-z0-9])"), re.I)))
    return out


def scan(root, terms):
    hits = []
    for p in files(root):
        rel = p.relative_to(root).as_posix()
        for n, line in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            for t, rx in terms:
                m = rx.search(line)
                if m:
                    hits.append(f"{rel}:{n}: {m.group(0)} (term {t})")
            for rx in ABSOLUTE:
                m = rx.search(line)
                if m:
                    hits.append(f"{rel}:{n}: {m.group(0)} (absolute path)")
    return hits


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(pathlib.Path(__file__).resolve().parents[2]), help="tree to scan (read-only)")
    a = ap.parse_args()
    root = pathlib.Path(a.root).resolve()
    lst = root / "tests" / "fixtures" / "leak" / "forbidden.txt"
    if not lst.is_file():
        print(f"ERROR LEAK-LIST: {lst} missing; run tests/tools/make_forbidden.py", file=sys.stderr)
        return 2
    hits = scan(root, compile_terms(lst.read_text(encoding="utf-8").splitlines()))
    for h in hits:
        print(h)
    print(f"leak scan: {len(hits)} hit(s)")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
