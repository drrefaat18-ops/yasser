# tests/test_positive_config.py
"""Core §9.4: five books, each with one feature disabled, pass the checker; the disabled checks are not_applicable."""
import importlib.util, json, pathlib, subprocess, sys, tempfile, unittest
from tests.helpers import temp_repo, REPO

CASES = {"no-mcq": ["MCQ-COUNT", "KEY-BALANCE", "MCQ-CASE", "LO-UNASSESSED"], "no-glossary": ["GLOSS-MISSING", "GLOSS-MIN"],
         "no-cases": ["MCQ-CASE"], "no-perspectives": ["PERSP-MISSING", "PERSP-BALANCE"], "no-errata": ["ERRATA-OPEN"]}
ALWAYS_ON = ["TPL-H1", "TPL-SECTION-MISSING", "CIT-MISSING", "READ-MEAN", "BUDGET-CHAPTER", "ASSET-MISSING"]


class PositiveConfig(unittest.TestCase):
    def test_disabled_checks_not_applicable_and_book_passes(self):
        for name, disabled in CASES.items():
            with self.subTest(name), temp_repo(f"positive-config/{name}", slug=name, stamp=True) as root:
                r = subprocess.run([sys.executable, "harness/tools/check_book.py", "--project", f"projects/{name}", "--json"],
                                   cwd=root, capture_output=True, text=True, encoding="utf-8")
                self.assertEqual(r.returncode, 0, r.stdout[-2000:] + r.stderr)
                checks = [c for t in json.loads(r.stdout)["targets"] for c in t["checks"]]
                for cid in disabled:
                    got = [c["status"] for c in checks if c["id"] == cid]
                    self.assertTrue(got and all(s == "not_applicable" for s in got), (cid, got))
                for cid in ALWAYS_ON:   # the features that stay on are really checked, never skipped
                    self.assertEqual({c["status"] for c in checks if c["id"] == cid}, {"pass"}, cid)
                others = {c["id"] for c in checks if c["status"] == "not_applicable"} - set(disabled)
                self.assertEqual(others - DISABLED_ELSEWHERE[name] - OPT_IN, set(), f"{name}: unexpected not_applicable")

    def test_committed_fixtures_equal_the_generator(self):
        spec = importlib.util.spec_from_file_location("make_positive_config", REPO / "tests/tools/make_positive_config.py")
        gen = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(gen)
        tree = lambda d: {p.relative_to(d).as_posix(): p.read_bytes().replace(b"\r\n", b"\n")
                          for p in sorted(d.rglob("*")) if p.is_file()}
        with tempfile.TemporaryDirectory() as tmp:
            gen.OUT = pathlib.Path(tmp)
            for n in gen.NAMES:
                gen.make(n)
                self.assertEqual(tree(gen.OUT / n), tree(REPO / "tests/fixtures/positive-config" / n), n)


# not_applicable IDs that follow from the disabled feature beyond the named ones (e.g. no MCQs -> no keys)
DISABLED_ELSEWHERE = {
    "no-mcq": {"MCQ-EXTRA-OPTION", "MCQ-OPTIONS", "MCQ-LO-TAG", "MCQ-LO-UNKNOWN", "KEY-RATIONALE", "KEY-MISSING", "KEY-RUN"},
    "no-glossary": set(), "no-cases": set(), "no-perspectives": set(), "no-errata": set(),
}

# checks a book turns on in its own config (Task 9b.5): prose rhythm needs a limit, formulas need the chemistry pack
OPT_IN = {"RHYTHM-PROSE", "CHEM-FORMULA-PLAIN"}

if __name__ == "__main__":
    unittest.main()
