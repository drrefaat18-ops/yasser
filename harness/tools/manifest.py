"""Migration manifest validator (STEP 6; plan "Migration manifest format"). Repo-level, reads no project.

Usage:
  python harness/tools/manifest.py --phase pre|post [--manifest FILE]
  python harness/tools/manifest.py --scope-commit HEAD [--extra PATH ...] [--manifest FILE]
Exit 0 iff no problems; each problem is printed on its own line.
"""
import argparse, json, pathlib, subprocess, sys

REPO = pathlib.Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))
from harness import hashing  # noqa: E402

DEFAULT = "docs/harness/migration-manifest.json"


def _git(repo, *args):
    r = subprocess.run(["git", *args], cwd=repo, capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {r.stderr.decode('utf-8', 'replace').strip()}")
    return r.stdout.decode("utf-8")


def problems(repo, m, phase):
    repo = pathlib.Path(repo)
    probs = []
    for item in m.get("expected_diff", []):
        if not isinstance(item, dict) or set(item) != {"pointer_glob", "reason"}:
            probs.append(f"expected_diff item {item!r} must have exactly pointer_glob and reason")
    tracked = set(_git(repo, "ls-files", "-z").split("\0")) if phase == "pre" else set()
    reserved = set(m.get("reserved", []))
    prefix = f"projects/{m.get('project')}/"
    seen = set()
    for e in m.get("moves", []):
        src, dst, sha = e.get("source"), e.get("destination"), e.get("sha256")
        if src in reserved or dst in reserved:
            probs.append(f"reserved path in move: {src} -> {dst}")
        if dst in seen:
            probs.append(f"duplicate destination: {dst}")
        seen.add(dst)
        if not str(dst).startswith(prefix):
            probs.append(f"destination outside {prefix}: {dst}")
        if phase == "pre":
            if src not in tracked:
                probs.append(f"source not tracked: {src}")
            if (repo / dst).exists():
                probs.append(f"destination exists: {dst}")
            if (repo / src).is_file() and hashing.hash_bytes((repo / src).read_bytes()) != sha:
                probs.append(f"hash mismatch before move: {src}")
        else:
            if not (repo / dst).is_file():
                probs.append(f"destination missing after move: {dst}")
            elif hashing.hash_bytes((repo / dst).read_bytes()) != sha:
                probs.append(f"hash mismatch after move: {dst}")
            if (repo / src).exists():
                probs.append(f"source still present after move: {src}")
    return probs


def scope_problems(repo, m, changed, extra_allowed):
    allowed = set(m.get("path_fix_allowlist", [])) | set(extra_allowed)
    return [f"not allowlisted: {p}" for p in changed if p not in allowed]


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", default=DEFAULT)
    ap.add_argument("--phase", choices=["pre", "post"])
    ap.add_argument("--scope-commit")
    ap.add_argument("--extra", action="append", default=[])
    a = ap.parse_args()
    if bool(a.phase) == bool(a.scope_commit):
        ap.error("give exactly one of --phase or --scope-commit")
    m = json.loads((REPO / a.manifest).read_text(encoding="utf-8"))
    if a.phase:
        probs = problems(REPO, m, a.phase)
    else:
        changed = [p for p in _git(REPO, "diff-tree", "--no-commit-id", "--name-only", "-r", a.scope_commit).splitlines() if p]
        probs = scope_problems(REPO, m, changed, a.extra)
    for p in probs:
        print(p)
    print(f"{len(probs)} problem(s)")
    sys.exit(1 if probs else 0)


if __name__ == "__main__":
    main()
