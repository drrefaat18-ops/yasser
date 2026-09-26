# tests/test_build.py
"""Config-driven build (plan Task 8.2). The medical build must reproduce the STEP 6 golden (N3, N7)."""
import json, os, pathlib, unittest
from harness import preflight
from harness.tools import build_book, capture_golden, compare_golden, config
from tests.helpers import REPO, run_cli, temp_repo

FIX = REPO / "tests/fixtures/ai-in-medicine"
WORD = preflight.check_word()["ok"]


def load(p):
    return json.loads(pathlib.Path(p).read_text(encoding="utf-8"))


class FactoryTest(unittest.TestCase):
    def setUp(self):
        self.cfg = config.load(REPO / "projects/ai-in-medicine")
        self.d = build_book._docx()

    def test_language_comes_from_theme(self):
        doc = self.d["Document"]()
        cfg = config.load(REPO / "projects/ai-in-medicine")
        cfg["theme"]["lang_tag"] = "en-US"
        build_book.setup_styles(self.d, doc, build_book.Book(cfg))
        lang = doc.styles["Normal"].element.rPr.find(self.d["qn"]("w:lang"))
        self.assertEqual(lang.get(self.d["qn"]("w:val")), "en-US")

    def test_ltr_run_has_no_direction_properties(self):
        doc = self.d["Document"]()
        f = build_book.Factory(self.d, self.cfg["theme"])
        r = f.make_run(f.make_paragraph(doc), "x", bold=True)
        xml = r._r.xml
        self.assertNotIn("w:rtl", xml)
        self.assertNotIn("w:bidi", xml)

    def test_rtl_is_refused_until_step10(self):
        with self.assertRaises(build_book.BuildError):
            build_book.Factory(self.d, dict(self.cfg["theme"], direction="rtl"))

    def test_callout_styles_come_from_theme(self):
        bk = build_book.Book(self.cfg)
        th = self.cfg["theme"]["callouts"]
        for key in ("safety", "opening", "objectives"):
            fill, colour, layout, border = bk.style_of(key)
            self.assertEqual((fill, colour, layout), (th[key]["fill"], th[key]["label_colour"], th[key]["layout"]))
        self.assertEqual(bk.style_of("objectives")[3], {"size_eighths_pt": 6, "colour": "C9D1D9"})
        self.assertEqual(bk.style_of("no-such-id")[0], build_book.DEFAULT_BOX)

    def test_parts_need_the_chapters_label(self):
        cfg = config.load(REPO / "projects/ai-in-medicine")
        del cfg["theme"]["labels"]["chapters"]
        with self.assertRaises(build_book.BuildError):
            build_book.build(cfg)


@unittest.skipUnless(WORD, "Microsoft Word COM is not available")
class BuildTest(unittest.TestCase):
    def test_medical_build_matches_golden(self):
        """`run build` in a temp repo (tests never touch the real project state), then capture from build/ and compare
        with the STEP 6 golden under allow-step8.json; new check IDs must pass (N7)."""
        with temp_repo(project_from="projects/ai-in-medicine", stamp=True, with_legacy=True) as root:
            r = run_cli(root, "--project", "projects/ai-in-medicine", "run", "build")
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            p = root / "projects/ai-in-medicine"
            rec = load(p / "state.json")["receipts"]["build"]
            self.assertEqual((rec["status"], rec["figures"], rec["backend"]), ("ok", "legacy", "word_com"))
            report = load(p / "build/build-report.json")
            self.assertTrue(report["docx"]["toc_field"])
            self.assertEqual(rec["page_count"], report["pdf"]["pages"])
            v = run_cli(root, "--project", "projects/ai-in-medicine", "verify", "--through", "build")
            self.assertEqual(v.returncode, 0, v.stderr)
            refs = os.environ.get("HARNESS_EVIDENCE_OUT") is not None   # the network evidence run also checks references
            g = capture_golden.capture_harness(p, slug="ai-in-medicine", run_refs=refs, docx_from="build")
        out = os.environ.get("HARNESS_EVIDENCE_OUT")
        if out:
            capture_golden.write(g, out)
        step6 = load(FIX / "golden-step6.json")
        allow = load(FIX / "allow-step8.json") + ([] if refs else [{"pointer_glob": "/verify_refs", "reason": "not captured offline"}])
        diffs = [d for d in compare_golden.diff(step6, g, allow, checks_from=step6)["diffs"] if not d["allowed"]]
        self.assertEqual(diffs, [])


if __name__ == "__main__":
    unittest.main()
