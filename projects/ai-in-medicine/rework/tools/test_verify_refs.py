"""Network test for verify_refs.py (needs api.crossref.org)."""
import pathlib, subprocess, sys, tempfile

TOOL = pathlib.Path(__file__).with_name("verify_refs.py")

# Task 7.3: the tool is gated, so it runs inside a temp repo holding the bypass fixture project (core §9.6).
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4]))
import atexit, contextlib  # noqa: E402
from tests.helpers import temp_repo  # noqa: E402

_stack = contextlib.ExitStack()
atexit.register(_stack.close)
_ROOT = None


def _gated(*args):
    global _ROOT
    if _ROOT is None:
        _ROOT = _stack.enter_context(temp_repo("bypass", slug="bypass-book", stamp=True, with_legacy=True))
    tool = _ROOT / TOOL.resolve().relative_to(pathlib.Path(__file__).resolve().parents[4])
    return subprocess.run([sys.executable, str(tool), "--project", "projects/bypass-book", *map(str, args)],
                          cwd=_ROOT, capture_output=True, text=True, encoding="utf-8")


def run(refs):
    f = pathlib.Path(tempfile.mkdtemp()) / "ch.md"
    f.write_text("# Chapter 1: X\n\n## References\n" + refs, encoding="utf-8")
    r = _gated(f)
    return r.returncode, r.stdout


def test_real_doi_ok():
    code, out = run("1. Obermeyer Z, et al. Dissecting racial bias in an algorithm used to manage the health of populations. Science. 2019. DOI: 10.1126/science.aax2342\n")
    assert code == 0 and "OK 1" in out, out


def test_fake_doi_fails():
    code, out = run("1. Nobody A. Fake paper. J. 2020. DOI: 10.9999/fake.123\n")
    assert code == 1 and "NOT FOUND 1" in out, out


def test_wrong_title_fails():
    code, out = run("1. Obermeyer Z. Deep learning for retinal photographs in diabetes. Science. 2019. DOI: 10.1126/science.aax2342\n")
    assert code == 1 and "TITLE MISMATCH 1" in out, out


def test_no_doi_reported():
    code, out = run("1. European Parliament. Regulation (EU) 2024/1689 (AI Act). 2024. https://eur-lex.europa.eu/eli/reg/2024/1689/oj\n")
    assert code == 0 and "NO DOI 1" in out, out


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
