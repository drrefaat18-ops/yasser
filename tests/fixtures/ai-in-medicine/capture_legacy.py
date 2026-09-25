"""Test-side, one-time STEP 5 capture of the pre-migration repo-root layout (plan N1).

Usage: python tests/fixtures/ai-in-medicine/capture_legacy.py --out FILE [--copy-src DIR]
Not a shipped executable: it is the only caller that passes a path outside projects/ to capture().
"""
import argparse, json, pathlib, shutil, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO))
from harness import hashing  # noqa: E402
from harness.tools import capture_golden  # noqa: E402


def tracked(paths):
    r = subprocess.run(["git", "ls-files", "-z", "--", *paths], cwd=REPO, capture_output=True, check=True)
    return sorted(p for p in r.stdout.decode("utf-8").split("\0") if p)


def copy_src(layout, dest):
    """Immutable copy: refuse if dest holds any file that differs from, or is absent in, the source."""
    files = tracked(layout["src_copy"])
    if dest.exists():
        existing = sorted(p.relative_to(dest).as_posix() for p in dest.rglob("*")
                          if p.is_file() and "__pycache__" not in p.parts)  # git-ignored bytecode caches
        extra = sorted(set(existing) - set(files))
        changed = [f for f in files if (dest / f).exists() and hashing.hash_file(dest / f) != hashing.hash_file(REPO / f)]
        if extra or changed:
            sys.exit(f"ERROR SRC-DIFFERS: {dest} differs from the sources: extra={extra} changed={changed}")
    for f in files:
        if not (dest / f).exists():
            (dest / f).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(REPO / f, dest / f)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--copy-src")
    a = ap.parse_args()
    layout = json.loads((HERE / "layout-legacy.json").read_text(encoding="utf-8"))
    try:
        golden = capture_golden.capture(REPO, layout, slug="ai-in-medicine")
    except (capture_golden.NetworkError, capture_golden.Unclassified) as e:
        print(f"ERROR {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(2)
    if a.copy_src:
        copy_src(layout, pathlib.Path(a.copy_src).resolve())
    capture_golden.write(golden, a.out)


if __name__ == "__main__":
    main()
