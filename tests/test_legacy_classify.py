# tests/test_legacy_classify.py — every row of the N6 table, driven by a real legacy call on a mutated input
import contextlib, importlib.util, io, pathlib, re, shutil, sys, tempfile, unittest
from harness.tools import capture_golden

REPO = pathlib.Path(__file__).resolve().parents[1]
SRC = REPO / "tests/fixtures/ai-in-medicine/src"          # immutable STEP 5 copy
CH = (SRC / "rework/ch01-what-ai-is.md").read_text(encoding="utf-8")
GLOSSARY = SRC / "rework/glossary.md"


def legacy():
    sys.dont_write_bytecode = True  # the src copy is immutable: never write __pycache__ into it
    spec = importlib.util.spec_from_file_location("legacy_check", SRC / "rework/tools/check_book.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod


def call(mod, fn, text):
    if fn == "check_budget":
        return mod.check_budget(text, 10)
    if fn == "check_glossary":
        return mod.check_glossary(text, GLOSSARY)
    return getattr(mod, fn)(text)


def before(heading, extra):
    return lambda t: t.replace(f"\n## {heading}", f"\n{extra}\n\n## {heading}", 1)


def key(q, letter):
    return lambda t: re.sub(rf"^\*\*Q{q}\. [A-D]\*\*", f"**Q{q}. {letter}**", t, count=1, flags=re.M)


MUTATIONS = [  # (legacy function, mutation of the chapter text, expected ID)
    ("check_budget", lambda t: t, "BUDGET-CHAPTER"),
    ("check_sentences", lambda t: t.replace(". ", " and "), "READ-MEAN"),
    ("check_sentences", lambda t: t.replace(". ", " and "), "READ-LONG"),
    ("check_sentences", lambda t: "", "READ-NOPROSE"),
    ("check_template", lambda t: re.sub(r"^# Chapter \d+: .*$", "# Intro", t, count=1, flags=re.M), "TPL-H1"),
    ("check_template", lambda t: t.replace("\n## References", "\n## Refs", 1), "TPL-SECTION-MISSING"),
    ("check_template", lambda t: t.replace("## Opening Case", "## Intro", 1) + "\n## Opening Case\nx\n", "TPL-SECTION-ORDER"),
    ("check_template", lambda t: t.replace("> **Safety Alert:**", "> **Alert:**"), "TPL-CALLOUT-MISSING"),
    ("check_lenses", lambda t: re.sub(r"\n> - \*\*[^*]+:\*\*[^\n]*", "", t, count=1), "PERSP-MISSING"),
    ("check_lenses", lambda t: re.sub(r"^(> - \*\*[^*]+:\*\*)", r"\1" + " word" * 80, t, count=1, flags=re.M), "PERSP-BALANCE"),
    ("check_los", lambda t: re.sub(r"^[234]\. \[LO[234]\].*\n", "", t, flags=re.M), "LO-COUNT"),
    ("check_los", lambda t: re.sub(r"\[LO1\] \w+", "[LO1] Understand", t, count=1), "LO-VERB"),
    ("check_mcqs", lambda t: t.replace("\nD) ", "\nE) extra\nD) ", 1), "MCQ-EXTRA-OPTION"),
    ("check_mcqs", lambda t: re.sub(r"^C\) .*\n", "", t, count=1, flags=re.M), "MCQ-OPTIONS"),
    ("check_mcqs", lambda t: re.sub(r"^(\*\*Q1\.\*\*.*?) \[LO\d+\]", r"\1", t, count=1, flags=re.M), "MCQ-LO-TAG"),
    ("check_mcqs", lambda t: t.replace("**Q10.**", "Q10.", 1), "MCQ-COUNT"),
    ("check_mcqs", lambda t: t.replace("**Case Question.**", "Case Question.", 1), "MCQ-CASE"),
    ("check_mcqs", lambda t: re.sub(r"^(\*\*Q1\.\*\*.*?)\[LO\d+\]", r"\1[LO9]", t, count=1, flags=re.M), "MCQ-LO-UNKNOWN"),
    ("check_mcqs", lambda t: re.sub(r"^(\d+)\. (\[LO1\])", r"\1. \2 Name.\n5. [LO5]", t, count=1, flags=re.M), "LO-UNASSESSED"),
    ("check_mcqs", lambda t: re.sub(r"^(\*\*Q1\. [A-D]\*\*).*$", r"\1 — …", t, count=1, flags=re.M), "KEY-RATIONALE"),
    ("check_mcqs", lambda t: re.sub(r"(\*\*Q1\.) [A-D]\*\*", r"\1**", t, count=1), "KEY-MISSING"),
    ("check_mcqs", key(1, "A"), "KEY-BALANCE"),
    ("check_mcqs", lambda t: key(2, "A")(key(1, "A")(key(3, "A")(t))), "KEY-RUN"),
    ("check_citations", lambda t: t.replace(".\n", " [999].\n", 1), "CIT-MISSING"),
    ("check_citations", lambda t: t.rstrip("\n") + "\n999. Extra reference.\n", "CIT-UNCITED"),
    ("check_glossary", before("Key Takeaways", "**Zzyzxterm** is new."), "GLOSS-MISSING"),
    ("check_banned", before("Key Takeaways", "A master-slave setup."), "BANNED-TERM"),
]


def drop(name):
    return lambda root: (root / name).unlink()


def errata_open(root):
    p = root / "errata-ledger.md"
    p.write_text(re.sub(r"\| fixed[^|]*\|", "| open |", p.read_text(encoding="utf-8"), count=1), encoding="utf-8")


def small_glossary(root):
    p = root / "glossary.md"
    p.write_text("\n\n".join(p.read_text(encoding="utf-8").split("\n\n")[:10]) + "\n", encoding="utf-8")


BOOK_MUTATIONS = [  # (mutation of a copy of the chapters dir, expected ID)
    (drop("ch01-what-ai-is.md"), "BOOK-CHAPTER-COUNT"),
    (drop("00-front-matter.md"), "BOOK-FRONT-MISSING"),
    (lambda root: [p.unlink() for p in sorted(root.glob("ch*.md"))[:4]], "BUDGET-TOTAL"),
    (errata_open, "ERRATA-OPEN"),
    (small_glossary, "GLOSS-MIN"),
]


class LegacyClassify(unittest.TestCase):
    def test_every_mapping_row(self):
        mod = legacy()
        self.assertEqual(call(mod, "check_template", CH), [], "unmutated chapter must pass")
        for fn, mutate, expected in MUTATIONS:
            with self.subTest(fn=fn, expected=expected):
                msgs = call(mod, fn, mutate(CH))
                self.assertTrue(msgs, "mutation produced no legacy message")
                self.assertIn(expected, {capture_golden.classify(fn, m) for m in msgs})

    def test_every_book_mapping_row(self):
        for mutate, expected in BOOK_MUTATIONS:
            with self.subTest(expected=expected), tempfile.TemporaryDirectory() as tmp:
                root = pathlib.Path(tmp) / "rework"
                shutil.copytree(SRC / "rework", root, ignore=shutil.ignore_patterns("tools", "__pycache__"))
                mutate(root)
                mod = legacy()
                mod.ROOT = root
                with contextlib.redirect_stdout(io.StringIO()):
                    msgs = [m for m in mod.check_all() if m.startswith("book:")]
                self.assertTrue(msgs, "mutation produced no book message")
                self.assertIn(expected, {capture_golden.classify("check_all", m) for m in msgs})

    def test_table_complete(self):
        ids = {row[2] for row in MUTATIONS} | {row[1] for row in BOOK_MUTATIONS}
        self.assertEqual(ids, set(capture_golden.ALL_LEGACY_IDS))

    def test_unknown_message_raises(self):
        with self.assertRaises(capture_golden.Unclassified):
            capture_golden.classify("check_template", "something the table does not know")


if __name__ == "__main__":
    unittest.main()
