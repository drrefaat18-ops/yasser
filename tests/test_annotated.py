# tests/test_annotated.py
"""Annotated figures (plan Task 9b.4): FIG-ANNOT, deterministic renders, the key under the caption."""
import copy, json, pathlib, tempfile, unittest
from harness import preflight
from harness.figures import annotated, check_figures
from harness.tools import build_book, build_html, config
from tests.helpers import REPO, temp_repo

FIX = REPO / "tests/fixtures/editorial-book"
BROWSER = preflight.check_browser("figures")["ok"]


class AnnotatedTest(unittest.TestCase):
    def setUp(self):
        self.cfg = config.load(FIX)
        self.fig = next(f for f in json.loads((FIX / "figures/figures.json").read_text(encoding="utf-8"))["figures"]
                        if f["kind"] == annotated.KIND)
        self.spec = annotated.load(self.cfg, self.fig)

    def test_fixture_spec_is_sound(self):
        self.assertEqual(annotated.problems(self.cfg, self.spec), [])

    def test_each_defect(self):
        def bad(edit):
            s = copy.deepcopy(self.spec)
            edit(s)
            return annotated.problems(self.cfg, s)
        cases = {
            "base outside the asset roots": lambda s: s.update(base="figures/src/reflux-setup.json"),
            "base missing": lambda s: s.update(base="chapters/figures/nope.png"),
            "numbers out of order": lambda s: s["callouts"][0].update(n=3),
            "point outside the image": lambda s: s["callouts"][1].update(at=[99999, 10]),
            "blank label": lambda s: s["callouts"][2].update(label=" "),
            "no callouts": lambda s: s.update(callouts=[]),
        }
        for name, edit in cases.items():
            with self.subTest(name):
                self.assertTrue(bad(edit))

    def test_svg_is_deterministic_and_themed(self):
        a, b = annotated.to_svg(self.cfg, self.spec), annotated.to_svg(self.cfg, self.spec)
        self.assertEqual(a, b)
        self.assertIn("#" + self.cfg["theme"]["palette"]["primary"], a)
        self.assertNotIn(self.spec["callouts"][0]["label"], a)   # labels live in the key, not on the image

    def test_key_in_both_writers(self):
        labels = [c["label"] for c in self.spec["callouts"]]
        w = build_html.Writer(build_book.Book(self.cfg))
        html = w.image(FIX / self.spec["base"], self.fig, None)
        positions = [html.index(label) for label in labels]
        self.assertEqual(positions, sorted(positions))
        d = build_book._docx()
        doc = d["Document"]()
        bk = build_book.Book(self.cfg)
        build_book.setup_styles(d, doc, bk)
        R = build_book.Renderer(d, doc, bk)
        R.figure(doc, FIX / self.spec["base"], None, self.fig)
        text = "\n".join(p.text for p in doc.paragraphs)
        self.assertIn("1 " + labels[0], text)
        self.assertLess(text.index(labels[0]), text.index(labels[-1]))

    def test_checker_reports_fig_annot(self):
        with temp_repo("editorial-book", slug="editorial-book", stamp=True) as root:
            p = root / "projects/editorial-book"
            src = p / self.fig["source"]
            s = json.loads(src.read_text(encoding="utf-8"))
            s["callouts"][0]["n"] = 7
            src.write_text(json.dumps(s), encoding="utf-8")
            report = check_figures.check(p, config.load(p), rendered=False)
            ids = {c["id"] for c in check_figures.blocking(report)}
            self.assertEqual(ids, {"FIG-ANNOT"})

    @unittest.skipUnless(BROWSER, "no browser for SVG rasterising")
    def test_render_bytes_identical(self):
        with tempfile.TemporaryDirectory() as t:
            runs = []
            for k in (1, 2):
                svg, png = pathlib.Path(t, f"{k}.svg"), pathlib.Path(t, f"{k}.png")
                annotated.render(self.cfg, self.spec, svg, png, 14, 300)
                runs.append((svg.read_bytes(), png.read_bytes()))
            self.assertEqual(runs[0], runs[1])


if __name__ == "__main__":
    unittest.main()
