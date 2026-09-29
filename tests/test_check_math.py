"""check_math: the symbolic gate over the numbers a book prints."""
import pathlib
import sys
import unittest

REPO = pathlib.Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))
from harness.tools import check_math  # noqa: E402


def run(text):
    found = {i: [] for i in check_math.IDS}
    check_math.check_text(text, "t.md", found)
    return found


def block(**kw):
    return "```math-check\n" + "".join(f"{k}: {v}\n" for k, v in kw.items()) + "```\n"


class CheckMathTest(unittest.TestCase):
    def test_a_true_claim_passes(self):
        f = run(block(label="ok", given="a=2, b=3", expr="a*b", expect="6"))
        self.assertEqual([v for v in f.values() if v], [])

    def test_a_false_claim_is_named_with_both_values(self):
        f = run(block(label="wrong", given="a=2, b=3", expr="a*b", expect="7"))
        self.assertEqual(len(f["MATH-MISMATCH"]), 1)
        self.assertIn("wrong", f["MATH-MISMATCH"][0])
        self.assertIn("6", f["MATH-MISMATCH"][0])

    def test_tolerance_is_honoured(self):
        near = block(label="near", given="a=1", expr="a*10", expect="10.02 +- 0.05")
        far = block(label="far", given="a=1", expr="a*10", expect="10.02 +- 0.001")
        self.assertEqual(run(near)["MATH-MISMATCH"], [])
        self.assertEqual(len(run(far)["MATH-MISMATCH"]), 1)

    def test_exact_compares_symbolically(self):
        """A third does not have to be rounded to be checked."""
        f = run(block(label="third", given="a=1, b=3", expr="a/b", expect="exact 1/3"))
        self.assertEqual(f["MATH-MISMATCH"], [])

    def test_exact_refuses_float_residue(self):
        """`exact` means exact: a Float that only nearly cancels is a mismatch, not a pass."""
        f = run(block(label="residue", given="a=0.1, b=0.2", expr="a + b", expect="exact 3/10"))
        self.assertEqual(len(f["MATH-MISMATCH"]), 1)

    def test_unbound_name_is_an_error_not_a_free_symbol(self):
        """A typo in a name must fail, not quietly become algebra in an unknown."""
        f = run(block(label="typo", given="Vd=45", expr="Vd*Km", expect="180"))
        self.assertEqual(len(f["MATH-UNBOUND"]), 1)
        self.assertIn("Km", f["MATH-UNBOUND"][0])
        self.assertEqual(f["MATH-MISMATCH"], [])

    def test_missing_key_is_named(self):
        f = run("```math-check\nlabel: bare\nexpr: 1+1\n```\n")
        self.assertEqual(len(f["MATH-SYNTAX"]), 1)
        self.assertIn("given", f["MATH-SYNTAX"][0])
        self.assertIn("expect", f["MATH-SYNTAX"][0])

    def test_unparsable_expression_is_reported_not_raised(self):
        f = run(block(label="bad", given="a=1", expr="a +* 2", expect="3"))
        self.assertEqual(len(f["MATH-SYNTAX"]), 1)

    def test_commas_inside_a_call_do_not_split_the_bindings(self):
        f = run(block(label="call", given="a=Rational(1,2), b=4", expr="a*b", expect="exact 2"))
        self.assertEqual([v for v in f.values() if v], [])

    def test_a_binding_may_use_an_earlier_one(self):
        f = run(block(label="chain", given="K=log(2)/3, tau=6", expr="exp(-K*tau)", expect="exact 1/4"))
        self.assertEqual([v for v in f.values() if v], [])

    def test_text_without_blocks_yields_nothing(self):
        self.assertEqual([v for v in run("# A chapter\n\nProse only.\n").values() if v], [])

    def test_report_counts_blocks_and_marks_status(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            p = pathlib.Path(d) / "math-checks.md"
            p.write_text(block(label="ok", given="a=1", expr="a", expect="1")
                         + block(label="no", given="a=1", expr="a", expect="2"), encoding="utf-8")
            report = check_math.check(None, [p])
        by = {c["id"]: c for c in report["checks"]}
        self.assertEqual(report["target"], "math")
        self.assertEqual(by["MATH-SYNTAX"]["measured"]["blocks"], 2)
        self.assertEqual(by["MATH-MISMATCH"]["status"], "fail")
        self.assertEqual(by["MATH-SYNTAX"]["status"], "pass")
        self.assertEqual(len(check_math.failures(report)), 1)


if __name__ == "__main__":
    unittest.main()
