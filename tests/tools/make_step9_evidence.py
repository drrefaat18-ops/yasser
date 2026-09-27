"""Test-side: render the figures-book fixture in a temporary repo and copy the STEP 9 evidence PNGs (plan Task 9.3).

Usage: python tests/tools/make_step9_evidence.py
Writes docs/harness/reviews/step9-evidence/{bar-chart,line-chart,diagram,aspirin,caffeine,ethanol-oxidation}.png.
Exit 0 when all six were rendered and copied; 1 otherwise.
"""
import pathlib, shutil, sys

REPO = pathlib.Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))
from tests.helpers import temp_repo  # noqa: E402

OUT = REPO / "docs" / "harness" / "reviews" / "step9-evidence"
EVIDENCE = {"bar-chart": "speed-bar", "line-chart": "speed-line", "diagram": "friction-diagram",
            "aspirin": "aspirin", "caffeine": "caffeine", "ethanol-oxidation": "ethanol-oxidation"}


def main():
    with temp_repo("figures-book", slug="figures-book", stamp=True) as root:
        sys.path.insert(0, str(root))   # render with the committed copy of the harness in the temp repo
        from harness.figures import render
        from harness.tools import config
        project = root / "projects" / "figures-book"
        cfg = config.load(project)
        results = {r["id"]: r for r in render.render_all(project, cfg)}
        OUT.mkdir(parents=True, exist_ok=True)
        missing = []
        for name, fid in EVIDENCE.items():
            r = results.get(fid)
            if not r or r["status"] != "rendered":
                missing.append(fid)
                continue
            shutil.copyfile(project / r["png"], OUT / f"{name}.png")
            print(f"wrote {(OUT / f'{name}.png').relative_to(REPO).as_posix()}")
    if missing:
        print(f"ERROR not rendered: {missing}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
