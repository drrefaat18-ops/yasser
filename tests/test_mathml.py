"""TeX math: splitting it out of prose, and converting it for the two writers."""
import pathlib
import unittest.mock
import sys
import unittest

REPO = pathlib.Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))
from harness.tools import mathml  # noqa: E402


class SplitTest(unittest.TestCase):
    def test_math_is_separated_from_prose(self):
        self.assertEqual(mathml.split_inline("where $K_e$ is the constant"),
                         [(False, "where "), (True, "K_e"), (False, " is the constant")])

    def test_prices_are_not_math(self):
        """A lone dollar, and two of them with spaces beside, stay ordinary text."""
        for s in ("It costs $5 and $10.", "Between $5 and $10 per pack.", "A $ on its own."):
            self.assertEqual(mathml.split_inline(s), [(False, s)], s)

    def test_an_escaped_dollar_is_a_literal(self):
        self.assertEqual(mathml.split_inline(r"costs \$5"), [(False, "costs $5")])

    def test_two_equations_on_one_line(self):
        got = mathml.split_inline("$a$ and $b$")
        self.assertEqual([f for is_math, f in got if is_math], ["a", "b"])

    def test_display_needs_the_whole_paragraph(self):
        self.assertEqual(mathml.display("$$C = C_0 e^{-Kt}$$"), "C = C_0 e^{-Kt}")
        self.assertIsNone(mathml.display("text $$x$$ more"))
        self.assertIsNone(mathml.display("$x$"))

    def test_strip_leaves_readable_text(self):
        """Bookmarks and running heads take the TeX without its delimiters."""
        self.assertEqual(mathml.strip("where $K_e$ is"), "where K_e is")
        self.assertEqual(mathml.strip("$$a + b$$"), "a + b")


class ConvertTest(unittest.TestCase):
    def test_mathml_is_produced(self):
        out = mathml.mathml("a + b")
        self.assertIn("<math", out)
        self.assertIn("</math>", out)

    def test_display_differs_from_inline(self):
        self.assertNotEqual(mathml.mathml("a", display=True), mathml.mathml("a", display=False))

    def test_bad_tex_is_a_named_matherror(self):
        with self.assertRaises(mathml.MathError) as e:
            mathml.mathml(r"\frac{")
        self.assertIn(r"\frac{", str(e.exception))

    @unittest.skipUnless(mathml.omml_available(), "MML2OMML.XSL (ships with Word) not on this machine")
    def test_omml_is_word_math_not_a_picture(self):
        out = mathml.omml_xml("C_p = C_p^0 e^{-Kt}")
        self.assertIn("oMath", out)
        self.assertIn("http://schemas.openxmlformats.org/officeDocument/2006/math", out)
        self.assertNotIn("<w:drawing", out)     # an equation, not an image

    @unittest.skipUnless(mathml.omml_available(), "MML2OMML.XSL (ships with Word) not on this machine")
    def test_subscript_survives_the_round_trip(self):
        self.assertIn("sSub", mathml.omml_xml("K_e"))


class TypographyGateTest(unittest.TestCase):
    """The TeX check must not call a book's own math stray TeX, and must keep doing so when math is off."""

    def _cfg(self, enabled):
        class C(dict):
            pass
        c = C()
        c["template"] = {"math": {"enabled": enabled}, "sections": [], "citations": {"style": "numeric-bracket"}}
        return c

    def test_math_off_still_reports_tex(self):
        from harness.tools import check_book
        cfg = self._cfg(False)
        with unittest.mock.patch.object(check_book, "_prose_lines", lambda t, c: ["The gas is $CO_2$."]):
            self.assertTrue(check_book.check_typography("x", cfg)["TYPO-LATEX"])

    def test_math_on_allows_delimited_tex_but_not_stray_tex(self):
        from harness.tools import check_book
        cfg = self._cfg(True)
        with unittest.mock.patch.object(check_book, "_prose_lines", lambda t, c: ["The gas is $CO_2$."]):
            self.assertEqual(check_book.check_typography("x", cfg)["TYPO-LATEX"], [])
        with unittest.mock.patch.object(check_book, "_prose_lines", lambda t, c: [r"A stray \alpha here."]):
            self.assertTrue(check_book.check_typography("x", cfg)["TYPO-LATEX"])


if __name__ == "__main__":
    import unittest.mock  # noqa: F401
    unittest.main()
