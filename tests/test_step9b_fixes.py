# tests/test_step9b_fixes.py
"""Regression tests for the STEP 9b Codex review fixes (docs/harness/reviews/step9b-fixes.md)."""
import copy, json, pathlib, shutil, tempfile, unittest
from harness.figures import annotated
from harness.tools import build_book, build_html, check_book, check_pdf, config
from tests.helpers import REPO

FIX = REPO / "tests/fixtures/editorial-book"
MED = REPO / "projects/ai-in-medicine"
MED_PDF = MED / "deliverables/AI_in_Health_Care_Interprofessional.pdf"


class Fixes(unittest.TestCase):
    def test_s9b01_h3_markup_same_in_both_writers(self):
        cfg = config.load(FIX)
        text = "# Chapter 1: A\n\n## 1.1 Part\n\n### Water, H~2~O and **bold**\n\nText.\n"
        d = build_book._docx()
        doc = d["Document"]()
        bk = build_book.Book(cfg)
        build_book.setup_styles(d, doc, bk)
        build_book.Renderer(d, doc, bk).markdown(text, "chapter", FIX / "chapters/x.md")
        h3 = next(p for p in doc.paragraphs if p.style.name == "Heading 3")
        self.assertEqual(h3.text, "Water, H2O and bold")
        self.assertTrue(any(r.font.subscript for r in h3.runs))
        html, _ = build_html.Writer(bk).render(text, "chapter", FIX / "chapters/x.md")
        self.assertIn("<h3>Water, H<sub>2</sub>O and <strong>bold</strong></h3>", html)

    def test_s9b02_missing_logo_or_font_is_a_config_error(self):
        with tempfile.TemporaryDirectory() as t:
            p = pathlib.Path(t) / "editorial-book"
            shutil.copytree(FIX, p)
            th = json.loads((p / "theme.json").read_text(encoding="utf-8"))
            th["cover"]["design"]["logos"] = ["chapters/figures/missing.png"]
            th["font_files"] = {"Some Face": {"regular": "chapters/figures/missing.ttf"}}
            (p / "theme.json").write_text(json.dumps(th), encoding="utf-8")
            with self.assertRaises(config.ConfigError) as e:
                config.load(p)
            self.assertIn("missing.png", str(e.exception))
            self.assertIn("missing.ttf", str(e.exception))

    def test_s9b02_configured_files_are_build_inputs(self):
        from harness.stages import contracts
        ins, _ = contracts.files(FIX, "build")
        self.assertIn("chapters/figures/logo.png", ins)

    def _outline(self, edit):
        """The medical PDF with a flat outline built from its own bookmarks after `edit(marks)`."""
        from pypdf import PdfReader, PdfWriter
        r = PdfReader(str(MED_PDF))
        marks = check_pdf.outline_titles(r)
        edit(marks)
        w = PdfWriter()
        w.append(str(MED_PDF), import_outline=False)
        for title, page in marks:
            w.add_outline_item(title, page)
        with tempfile.TemporaryDirectory() as t:
            out = pathlib.Path(t) / "x.pdf"
            with open(out, "wb") as fh:
                w.write(fh)
            return check_pdf.outline_problems(config.load(MED), PdfReader(str(out)))

    def test_s9b03_outline_is_exact(self):
        self.assertEqual(self._outline(lambda m: None), [])
        k = lambda m: next(i for i, (t, _) in enumerate(m) if t.startswith("1 "))
        def wrong_page(m):
            m[k(m)] = (m[k(m)][0], 0)
        self.assertTrue(any("does not show" in p for p in self._outline(wrong_page)))
        self.assertTrue(any("exactly 1" in p for p in self._outline(lambda m: m.append(m[k(m)]))))
        def swap(m):
            i = k(m)
            j = next(x for x, (t, _) in enumerate(m) if t.startswith("2 "))
            m[i], m[j] = m[j], m[i]
        self.assertTrue(any("out of chapter order" in p for p in self._outline(swap)))
        def superstring(m):
            m[k(m)] = ("Appendix: " + m[k(m)][0], m[k(m)][1])
        self.assertTrue(any("exactly 1" in p for p in self._outline(superstring)))

    def test_s9b04_general_tex(self):
        cfg = config.load(FIX)
        for bad in (r"\alpha", r"\sqrt{x}", r"\begin{equation}", r"\[x\]"):
            self.assertTrue(check_book.check_typography(f"# Chapter 1: A\n\nSee {bad} here.\n", cfg)["TYPO-LATEX"], bad)
        for ok in ("It costs $5 and $10.", "Code `\\frac` in a span.", "CO~2~"):
            self.assertEqual(check_book.check_typography(f"# Chapter 1: A\n\n{ok}\n", cfg)["TYPO-LATEX"], [], ok)

    def test_s9b06_corrupt_base_is_reported(self):
        with tempfile.TemporaryDirectory() as t:
            p = pathlib.Path(t) / "editorial-book"
            shutil.copytree(FIX, p)
            (p / "chapters/figures/apparatus.png").write_bytes(b"not an image")
            cfg = config.load(p)
            spec = json.loads((p / "figures/src/reflux-setup.json").read_text(encoding="utf-8"))
            self.assertIn("not a readable image", annotated.problems(cfg, spec)[0])

    def test_s9b_c01_css_string_cannot_close_style(self):
        self.assertNotIn("<", build_html.css_string("</style><script>x</script>"))


if __name__ == "__main__":
    unittest.main()
