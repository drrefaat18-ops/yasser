# tests/test_author_year.py
"""citations.style `author-year`: APA-style in-text citations resolve against an unnumbered reference list."""
import copy, unittest
from harness.tools import check_book, config
from tests.helpers import REPO

FIX = REPO / "tests/fixtures/editorial-book"
CITE = r"(?P<author>[A-Z][\w'’-]+)(?:\s+et al\.|\s+(?:&|and)\s+[A-Z][\w'’-]+)?(?:,\s*|\s+\()(?P<year>\d{4}[a-z]?)"
ENTRY = r"^(?:[-*]\s+)?(?P<author>[^()\n]+?)\s*\((?P<year>\d{4}[a-z]?|n\.d\.)\)"
REFS = """
## References
Kotler, P., & Keller, K. L. (2016). *Marketing management* (15th ed.). Pearson.
Drummond, M. F., Sculpher, M. J., Claxton, K., Stoddart, G. L., & Torrance, G. W. (2015). *Methods for the economic evaluation of health care programmes* (4th ed.). Oxford University Press.
World Health Organization. (2019). *Guide to cost-effectiveness analysis*. WHO.
"""


class AuthorYear(unittest.TestCase):
    def setUp(self):
        self.cfg = copy.deepcopy(config.load(FIX))
        self.cfg["template"]["citations"] = {"style": "author-year", "pattern": CITE}
        self.cfg["template"]["references"]["entry_pattern"] = ENTRY

    def run_on(self, body, refs=REFS):
        return check_book.check_citations("# Chapter 1: T\n\n" + body + "\n" + refs, self.cfg)

    def test_every_form_resolves(self):
        body = ("Marketing creates exchanges (Kotler & Keller, 2016; Drummond et al., 2015). "
                "Kotler and Keller (2016) call it a process. The World Health Organization (2019) sets a method.")
        self.assertEqual(self.run_on(body), {"CIT-MISSING": [], "CIT-UNCITED": [], "CIT-DUPLICATE": []})

    def test_missing_uncited_duplicate(self):
        refs = REFS + "Kotler, P., & Armstrong, G. (2016). *Principles of marketing*. Pearson.\n"
        r = self.run_on("As shown (Kotler & Keller, 2016; Smith, 2020).", refs)
        self.assertEqual(r["CIT-MISSING"], ["missing reference Smith (2020)"])
        self.assertIn("uncited reference Drummond (2015)", r["CIT-UNCITED"])
        self.assertEqual(r["CIT-DUPLICATE"], ["reference Kotler (2016) is listed 2 times"])

    def test_year_must_agree(self):
        r = self.run_on("As shown (Kotler & Keller, 2012; Drummond et al., 2015; World Health Organization, 2019).")
        self.assertEqual(r["CIT-MISSING"], ["missing reference Kotler (2012)"])

    def test_prose_years_are_not_citations(self):
        r = self.run_on("In 2016 prices rose. (Kotler & Keller, 2016; Drummond et al., 2015; World Health Organization, 2019)")
        self.assertEqual(r["CIT-MISSING"], [])

    def test_config_needs_named_groups(self):
        t = copy.deepcopy(self.cfg["template"])
        self.assertEqual([p for p in config.feature_problems(t) if "author-year" in p], [])
        t["citations"]["pattern"] = r"\((\d{4})\)"
        self.assertTrue(any("citations.pattern needs named groups" in p for p in config.feature_problems(t)))


if __name__ == "__main__":
    unittest.main()
