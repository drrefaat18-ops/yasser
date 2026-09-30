# tests/test_text_checks.py
"""Text checks from the Dr. Mo comparison (plan Task 9b.5): TYPO-LATEX, RHYTHM-PROSE, CHEM-FORMULA-PLAIN."""
import copy, unittest
from harness.figures.packs import chemistry
from harness.tools import check_book, config
from tests.helpers import REPO

FIX = REPO / "tests/fixtures/editorial-book"


def status(report, cid):
    return {c["status"] for c in report["checks"] if c["id"] == cid}


class TextChecks(unittest.TestCase):
    def setUp(self):
        self.cfg = config.load(FIX)
        self.entry, self.path = self.cfg.chapters()[0]
        self.text = self.path.read_text(encoding="utf-8")

    def run_on(self, text, cfg=None):
        import tempfile, pathlib
        with tempfile.TemporaryDirectory() as t:
            p = pathlib.Path(t) / self.path.name
            p.write_text(text, encoding="utf-8")
            return check_book.check_chapter(p, cfg or self.cfg, self.entry)

    def test_fixture_passes(self):
        r = check_book.check_chapter(self.path, self.cfg, self.entry)
        for cid in ("TYPO-LATEX", "RHYTHM-PROSE", "CHEM-FORMULA-PLAIN"):
            self.assertEqual(status(r, cid), {"pass"}, cid)

    def test_raw_tex(self):
        for bad in ("$CO_2$", r"\frac{a}{b}", r"\ce{H2O}", r"A \xrightarrow{550} B"):
            with self.subTest(bad):
                r = self.run_on(self.text.replace("A force is a push", f"{bad} A force is a push", 1))
                self.assertEqual(status(r, "TYPO-LATEX"), {"fail"})

    def test_long_prose_run(self):
        filler = " ".join(["Friction slows the box."] * 120)   # 480 words, no figure, table or box
        r = self.run_on(self.text.replace("## 1.3 Friction\n", f"## 1.3 Friction\n\n{filler}\n", 1))
        self.assertEqual(status(r, "RHYTHM-PROSE"), {"fail"})

    def test_rhythm_off_without_a_limit(self):
        cfg = copy.deepcopy(self.cfg)
        cfg["template"]["readability"].pop("max_prose_run_words")
        self.assertEqual(status(self.run_on(self.text, cfg), "RHYTHM-PROSE"), {"not_applicable"})

    def test_plain_formula(self):
        r = self.run_on(self.text.replace("A force is a push", "Water is H2O. A force is a push", 1))
        self.assertEqual(status(r, "CHEM-FORMULA-PLAIN"), {"fail"})
        r = self.run_on(self.text.replace("A force is a push", "Water is H~2~O. A force is a push", 1))
        self.assertEqual(status(r, "CHEM-FORMULA-PLAIN"), {"pass"})

    def test_formula_off_without_the_pack(self):
        cfg = copy.deepcopy(self.cfg)
        cfg["brief"]["figures"]["packs"] = ["charts"]
        r = self.run_on(self.text.replace("A force is a push", "Water is H2O. A force is a push", 1), cfg)
        self.assertEqual(status(r, "CHEM-FORMULA-PLAIN"), {"not_applicable"})

    def test_formula_detector(self):
        self.assertEqual(chemistry.plain_formulas("CO2, H2SO4, (NH4)2SO4, O2, NaCl, B12, LO1, Q3, CO~2~, COVID19, 21 CFR"),
                         ["CO2", "H2SO4", "(NH4)2SO4", "O2"])

    def test_wiki_link(self):
        r = self.run_on(self.text.replace("A force is a push", "See [[force]]. A force is a push", 1))
        self.assertEqual(status(r, "TYPO-WIKILINK"), {"fail"})
        r = self.run_on(self.text.replace("A force is a push", "Write `[[force]]` in code. A force is a push", 1))
        self.assertEqual(status(r, "TYPO-WIKILINK"), {"pass"})
        self.assertEqual(check_book.wikilinks("a [[x]] b [[x]] [y](#y) [[ ]]"), ["[[ ]]", "[[x]]"])

    def test_control_character(self):
        r = self.run_on(self.text.replace("A force is a push", "$$x = \x0crac{a}{b}$$ A force is a push", 1))
        self.assertEqual(status(r, "TYPO-CONTROL"), {"fail"})
        self.assertEqual(status(self.run_on(self.text), "TYPO-CONTROL"), {"pass"})


if __name__ == "__main__":
    unittest.main()
