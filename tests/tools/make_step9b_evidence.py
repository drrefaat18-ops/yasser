"""Build the editorial-book fixture with the HTML engine in a temp repo and save STEP 9b evidence PNGs (plan Task 9b.6).

Usage: python tests/tools/make_step9b_evidence.py   -> docs/harness/reviews/step9b-evidence/*.png
Saves the four build checkpoints (cover, first chapter page, first figure page, last page), the contents page, the
annotated-figure page and the table page, and fails unless check_pdf passes every ID. Exit 0 ok, 1 otherwise.
"""
import pathlib, shutil, sys

REPO = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
from tests.helpers import run_cli, temp_repo  # noqa: E402

SLUG = "editorial-book"
P = ["--project", f"projects/{SLUG}"]
OUT = REPO / "docs/harness/reviews/step9b-evidence"


def main():
    import fitz
    with temp_repo(SLUG, slug=SLUG, stamp=True) as root:
        r = run_cli(root, *P, "begin", "rework")
        n = r.stdout.split("nonce=")[1].split()[0]
        for u in ("ch01", "ch02"):
            run_cli(root, *P, "complete", "rework", "--nonce", n, "--unit", u)
        run_cli(root, *P, "complete", "rework", "--nonce", n)
        r = run_cli(root, *P, "run", "build")
        if r.returncode != 0:
            print(r.stdout + r.stderr, file=sys.stderr)
            return 1
        project = root / "projects" / SLUG
        sys.path.insert(0, str(root))
        from harness.tools import check_pdf, config
        pdf = project / "build" / f"{SLUG}.pdf"
        bad = check_pdf.failures(check_pdf.check(config.load(project), pdf))
        if bad:
            print(bad, file=sys.stderr)
            return 1
        if OUT.exists():
            shutil.rmtree(OUT)
        OUT.mkdir(parents=True)
        for png in (project / "build/checkpoints").glob("*.png"):
            shutil.copyfile(png, OUT / png.name)
        doc = fitz.open(str(pdf))
        wanted = {"contents": "Contents", "annotated-figure": "reflux condenser", "table": "Slowing car"}
        for name, needle in wanted.items():
            i = next(k for k in range(doc.page_count) if needle in doc[k].get_text())
            doc[i].get_pixmap(dpi=100).save(str(OUT / f"{name}.png"))
        doc.close()
    for p in sorted(OUT.glob("*.png")):
        print(p.relative_to(REPO).as_posix())
    return 0


if __name__ == "__main__":
    sys.exit(main())
