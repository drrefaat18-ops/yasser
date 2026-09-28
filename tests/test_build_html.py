# tests/test_build_html.py
"""HTML/Edge PDF engine (plan Task 9b.2; DEC-043) and the PDF gates on its output (Task 9b.3)."""
import json, pathlib, re, unittest
from harness import preflight
from harness.tools import blocks, build_book, build_html, config
from tests.helpers import REPO, run_cli, temp_repo

SLUG = "editorial-book"
P = ["--project", f"projects/{SLUG}"]
FIX = REPO / "tests/fixtures" / SLUG
EDGE = preflight.check_browser("build")["ok"]
WORD = preflight.check_word()["ok"]


def finish_rework(root):
    r = run_cli(root, *P, "begin", "rework")
    assert r.returncode == 0, r.stderr
    n = r.stdout.split("nonce=")[1].split()[0]
    for u in ("ch01", "ch02"):
        r = run_cli(root, *P, "complete", "rework", "--nonce", n, "--unit", u)
        assert r.returncode == 0, r.stderr
    r = run_cli(root, *P, "complete", "rework", "--nonce", n)
    assert r.returncode == 0, r.stderr


class WriterTest(unittest.TestCase):
    def setUp(self):
        self.cfg = config.load(FIX)
        self.w = build_html.Writer(build_book.Book(self.cfg))

    def test_sub_sup_and_escaping(self):
        self.assertEqual(self.w.inline("H~2~O <b> Ca^2+^"), "H<sub>2</sub>O &lt;b&gt; Ca<sup>2+</sup>")

    def test_stylesheet_uses_only_theme_fonts(self):
        css = build_html.stylesheet(self.w.bk, [(1, "A")])
        fonts = set(re.findall(r'font-family:"([^"]+)"', css))
        self.assertEqual(fonts, {self.cfg["theme"]["fonts"][k] for k in ("serif", "serif_heading", "sans")})

    def test_paper_colour_is_the_page_background(self):
        css = build_html.stylesheet(self.w.bk, [(1, "A")])
        self.assertIn("background:#" + self.cfg["theme"]["palette"]["paper"], css.split("}")[0])   # on @page itself

    def test_left_callout_edge_and_serif_h2(self):
        th = self.cfg["theme"]
        key = next(iter(th["callouts"]))
        th["callouts"][key].pop("border", None)
        th["callouts"][key]["edge"] = "left"
        th["layout"]["heading2_font"] = "serif_heading"
        css = build_html.stylesheet(self.w.bk, [(1, "A")])
        self.assertIn(f".c-{key}{{background:#{th['callouts'][key]['fill']};border-top:0;border-left:3pt solid", css)
        self.assertIn('h2,.h2{font-family:"' + th["fonts"]["serif_heading"] + '"', css)

    def test_fonts_fall_back_to_the_body_serif(self):
        css = build_html.stylesheet(self.w.bk, [(1, "A")])
        f = self.cfg["theme"]["fonts"]
        self.assertIn(f'font-family:"{f["sans"]}","{f["serif"]}"', css)

    def test_css_string_escapes_quotes(self):
        self.assertEqual(build_html.css_string('a "b" \\ c'), '"a \\"b\\" \\\\ c"')

    def test_outline_match_ignores_a_wrapped_heading_space(self):
        heads = [(1, "2 Psychosis and Antipsychotic Drugs")]
        build_html._match(heads, [(1, "2 Psychosis and AntipsychoticDrugs", 0)], "body")   # Edge drops the wrap space
        with self.assertRaises(build_html.BuildError):
            build_html._match(heads, [(1, "2 Psychosis and Antidepressant Drugs", 0)], "body")

    def test_outline_match_closes_a_skipped_level(self):
        heads = [(2, "How to Use This Book"), (3, "The boxes"), (2, "Next")]
        build_html._match(heads, [(1, "How to Use This Book", 0), (2, "The boxes", 0), (1, "Next", 0)], "front")
        with self.assertRaises(build_html.BuildError):
            build_html._match(heads, [(1, "How to Use This Book", 0), (1, "The boxes", 0), (1, "Next", 0)], "front")

    def test_engine_defaults_to_word(self):
        cfg = config.load(REPO / "projects/ai-in-medicine")
        self.assertEqual(build_html.engine(cfg), "word_com")


@unittest.skipUnless(EDGE and WORD, "Edge and Word are needed for the HTML engine build")
class HtmlBuildTest(unittest.TestCase):
    """One real `run build` of the fixture; every assertion reads its outputs."""

    @classmethod
    def setUpClass(cls):
        cls.ctx = temp_repo(SLUG, slug=SLUG, stamp=True)
        cls.root = cls.ctx.__enter__()
        finish_rework(cls.root)
        cls.result = run_cli(cls.root, *P, "run", "build")
        cls.project = cls.root / "projects" / SLUG
        cls.pdf = cls.project / "build" / f"{SLUG}.pdf"

    @classmethod
    def tearDownClass(cls):
        cls.ctx.__exit__(None, None, None)

    def reader(self):
        from pypdf import PdfReader
        return PdfReader(str(self.pdf))

    def test_build_ok_with_html_engine(self):
        self.assertEqual(self.result.returncode, 0, self.result.stdout + self.result.stderr)
        rec = json.loads((self.project / "state.json").read_text(encoding="utf-8"))["receipts"]["build"]
        self.assertEqual((rec["status"], rec["pdf_engine"]), ("ok", "html"))
        self.assertEqual(run_cli(self.root, *P, "verify", "--through", "build").returncode, 0)

    def test_bookmarks_follow_the_headings(self):
        r = self.reader()
        titles = []

        def walk(items):
            for it in items:
                walk(it) if isinstance(it, list) else titles.append(it.title)
        walk(r.outline)
        cfg = config.load(self.project)
        want = []
        for _, path in cfg.chapters():
            text = path.read_text(encoding="utf-8")
            n, title = build_book.chapter_heading(text, cfg)
            want.append(f"{n} {blocks.plain(title)}")
        for t in want:
            self.assertIn(t, titles)
        self.assertEqual(titles[0], cfg["template"]["sections"][-1]["label"])   # the how-to-use page comes first

    def test_contents_numbers_are_outline_pages(self):
        r = self.reader()
        body_start = None
        marks = []

        def walk(items):
            for it in items:
                if isinstance(it, list):
                    walk(it)
                else:
                    marks.append((it.title, r.get_destination_page_number(it)))
        walk(r.outline)
        chapter = next((t, p) for t, p in marks if re.match(r"1 ", t))
        body_start = chapter[1]   # printed page 1
        contents = next(p.extract_text() for p in r.pages if "Contents" in p.extract_text())
        for title, page in marks:
            if re.match(r"\d+ ", title):
                self.assertRegex(contents.replace("\n", " "), re.escape(title) + r"[ .]*" + str(page - body_start + 1) + r"\b")

    def test_metadata(self):
        meta = self.reader().metadata
        brief = json.loads((self.project / "brief.json").read_text(encoding="utf-8"))["identity"]
        self.assertEqual(meta["/Title"], f"{brief['title']}: {brief['subtitle']}")
        self.assertEqual(meta["/Author"], brief["authors"][0]["credit_line"])

    def test_subscript_is_real_text(self):
        text = "".join(p.extract_text() for p in self.reader().pages)
        self.assertIn("CO2", text.replace(" ", ""))   # CO~2~ printed as CO with a lowered 2, still one word


if __name__ == "__main__":
    unittest.main()
