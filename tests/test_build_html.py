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

    def test_clip_and_fit_heads(self):
        self.assertEqual(build_html.clip("Short", 10), "Short")
        self.assertEqual(build_html.clip("Practical Pharmacology of the Central", 24), "Practical Pharmacology…")
        left, right = build_html.fit_heads("A very long book title that goes on", "Chapter 2 · A long chapter title", 40)
        self.assertLessEqual(len(left) + len(right) + 4, 40)
        self.assertTrue(right.startswith("Chapter 2"))
        self.assertEqual(build_html.fit_heads("Book", "Chapter 1", 40), ("Book", "Chapter 1"))

    def test_running_heads_fit_their_budget(self):
        th = self.cfg["theme"]
        th["running"] = {"style": "caps", "footer_left": "An author", "footer_center": "Course 101", "page_number": "right"}
        css = build_html.stylesheet(self.w.bk, [(1, "A chapter title long enough to need cutting " * 3)])
        page = css.split("@page ch1{", 1)[1]
        left, right = re.findall(r'@top-(?:left|right)\{content:"([^"]*)"', page)[:2]
        m, pg = th["page"]["margins"], self.w.bk.preset["page"]
        budget = int((pg["width_cm"] - m["left"] - m["right"]) * 72 / 2.54 / (build_html.HEAD_PT["caps"] * build_html.HEAD_EM["caps"]))
        self.assertLessEqual(len(left) + len(right), budget)
        self.assertIn("text-transform:uppercase", page.split("}", 1)[0])
        self.assertIn('@bottom-right{content:counter(page)', css)
        self.assertIn('@bottom-center{content:"Course 101"', css)
        th["running"] = {"footer_center": "Course 101"}   # the centre already holds the page number
        with self.assertRaises(build_html.BuildError):
            build_html.stylesheet(self.w.bk, [(1, "A")])

    def test_spaced_dash_is_bound_to_the_word_before(self):
        self.assertEqual(self.w.inline("Term — definition, 20–80"), "Term — definition, 20–80")

    def test_section_eyebrow(self):
        sec = next(s for s in self.cfg["template"]["sections"] if s["id"] not in self.cfg["theme"]["boxed_section_ids"])
        self.cfg["theme"]["section_eyebrows"] = {sec["id"]: "Kicker"}
        html_text, _ = self.w.render(f"## {sec['label']}\n\nText.\n", "chapter", FIX / "chapters" / "x.md")
        self.assertIn(f'<div class="eyebrow">Kicker</div><h2>{sec["label"]}</h2>', html_text)

    def test_toc_chapters_style(self):
        self.cfg["theme"]["toc"]["style"] = "chapters"
        heads = [(1, "Part I Basics"), (1, "1 First"), (2, "1.1 Alpha"), (3, "Deep"), (2, "1.2 Beta"), (1, "Glossary")]
        kinds = [("part", "Part I", "Basics"), ("chapter", 1, "First"), ("other",), ("other",), ("other",), ("other",)]
        toc = build_html.toc_html(self.w.bk, heads, kinds, ["1", "3", "3", "4", "5", "40"])
        self.assertIn('<div class="tc-part">Part I · Basics</div>', toc)
        self.assertIn(f'<div class="tc-k">{self.cfg["theme"]["labels"]["chapter"]} 01</div>', toc)
        self.assertIn('<div class="tc-sub">1.1 Alpha · 1.2 Beta</div>', toc)   # level 3 left out
        self.assertIn('<div class="tc-pg">3</div>', toc)
        self.assertEqual(toc.count('class="tc-row"'), 2)   # chapter and glossary

    def test_chapter_opener_page(self):
        part = {"label": "Part I", "title": "Basics"}
        html_text = build_html.opener_html(self.w.bk, 3, "Title", part, ["3.1 Alpha", "3.2 Beta"])
        self.assertIn('<h1><span class="num">3</span> Title</h1>', html_text)   # the outline's h1 is on the opener
        self.assertIn('<div class="partline">Part I · Basics</div>', html_text)
        self.assertNotIn("inchap", html_text)   # no theme.labels.in_this_chapter: no list
        self.cfg["theme"]["labels"]["in_this_chapter"] = "In this chapter"
        html_text = build_html.opener_html(self.w.bk, 3, "Title", None, ["3.1 Alpha", "3.2 Beta"])
        self.assertIn('<div class="lbl">In this chapter</div><ol><li>3.1 Alpha</li><li>3.2 Beta</li></ol>', html_text)

    def test_centered_title_page_holds_the_notices(self):
        self.cfg["theme"]["title_page"] = {"layout": "centered", "notices": ["For teaching only."]}
        tp = build_html.title_page_html(self.w.bk)
        self.assertIn('<section class="titlepage centered">', tp)
        self.assertIn('<div class="tp-notices"><p>For teaching only.</p></div>', tp)
        self.assertNotIn('class="notices"', tp)
        for a in self.cfg["brief"]["identity"]["authors"]:
            self.assertIn(f'<div class="tp-author">{a["credit_line"]}</div>', tp)

    def test_ending_page(self):
        self.assertIsNone(build_html.ending_html(self.w.bk))
        self.cfg["theme"]["ending"] = {"quote": "Learn well.", "attribution": "The authors"}
        end = build_html.ending_html(self.w.bk)
        self.assertIn('<div class="quote">Learn well.</div><div class="who">The authors</div>', end)
        self.assertIn('class="cover bleed ending"', end)   # page:cover, full bleed

    def test_design_merge_order(self):
        bk, th = self.w.bk, self.cfg["theme"]
        self.assertNotIn("design", bk.preset)
        self.assertEqual(build_html.design(bk, "toc_style"), "leaders")   # built-in default
        bk.preset = dict(bk.preset, design={"toc_style": "chapters", "page_number": "right"})
        self.assertEqual(build_html.design(bk, "toc_style"), "chapters")   # preset default
        th["toc"]["style"] = "leaders"
        self.assertEqual(build_html.design(bk, "toc_style"), "leaders")   # the theme wins
        th.pop("running", None)
        self.assertEqual(build_html.design(bk, "page_number"), "right")   # no theme section at all
        bk.preset["design"] = {"toc_style": "chapter"}
        th["toc"].pop("style")
        with self.assertRaises(build_html.BuildError):
            build_html.design(bk, "toc_style")

    def test_preset_without_design_keeps_the_old_look(self):
        # D-01: the built-in defaults are the look of a preset with no `design`, byte for byte
        bk = self.w.bk
        heads = [(1, "1 First"), (2, "1.1 Alpha")]
        kinds = [("chapter", 1, "First"), ("other",)]
        out = lambda: (build_html.stylesheet(bk, [(1, "First")]), build_html.title_page_html(bk),
                       build_html.toc_html(bk, heads, kinds, ["1", "2"]))
        before = out()
        bk.preset = dict(bk.preset, design={k: allowed[0] for k, (_, allowed) in build_html.DESIGN.items()})
        self.assertEqual(out(), before)

    def test_editorial_preset_turns_the_design_on(self):
        bk = self.w.bk
        plain = build_html.stylesheet(bk, [(1, "A")])
        bk.preset = json.loads((REPO / "harness/presets/ltr-textbook-editorial.json").read_text(encoding="utf-8"))
        self.assertEqual({k: build_html.design(bk, k) for k in build_html.DESIGN},
                         {"chapter_opener": "page", "toc_style": "chapters", "title_page": "centered",
                          "running_style": "caps", "page_number": "right"})
        css = build_html.stylesheet(bk, [(1, "A")])
        self.assertNotEqual(css, plain)
        self.assertIn("@bottom-right{content:counter(page)", css)
        self.assertIn('<section class="titlepage centered">', build_html.title_page_html(bk))

    def test_engine_defaults_to_word(self):
        cfg = config.load(REPO / "projects/ai-in-medicine")
        self.assertEqual(build_html.engine(cfg), "word_com")


@unittest.skipUnless(EDGE and WORD, "Edge and Word are needed for the HTML engine build")
class CoverAccentTest(unittest.TestCase):
    def test_low_contrast_accent_falls_back_to_light_tint(self):
        self.assertEqual(build_html.cover_accent("#2F6F7A", "#A4472B"), "#F3E6D8")   # petrol on terracotta: ~1.2:1

    def test_readable_accent_is_kept(self):
        self.assertEqual(build_html.cover_accent("#B08534", "#1B2A8C"), "#B08534")   # gold on navy: >3:1


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


@unittest.skipUnless(EDGE and WORD, "Edge and Word are needed for the HTML engine build")
class EditorialPresetBuildTest(unittest.TestCase):
    """The fixture on the editorial preset: a real `run build`, every PDF gate passed or not applicable."""

    def test_build_passes_the_pdf_gates(self):
        from tests.helpers import stamp_project
        with temp_repo(SLUG, slug=SLUG, stamp=True) as root:
            project = root / "projects" / SLUG
            theme = json.loads((project / "theme.json").read_text(encoding="utf-8"))
            theme["preset"] = "ltr-textbook-editorial"
            (project / "theme.json").write_text(json.dumps(theme, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
            st = (project / "state.json").read_text(encoding="utf-8")   # the receipts name the preset among their inputs
            (project / "state.json").write_text(st.replace("presets/ltr-textbook.json", "presets/ltr-textbook-editorial.json"),
                                                encoding="utf-8")
            stamp_project(root, project)
            finish_rework(root)
            r = run_cli(root, *P, "run", "build")
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            checks = json.loads((project / "build" / "build-report.json").read_text(encoding="utf-8"))["pdf_checks"]
            self.assertEqual(len(checks), 10)
            self.assertEqual([c["id"] for c in checks if c["status"] not in ("pass", "not_applicable")], [])


if __name__ == "__main__":
    unittest.main()
