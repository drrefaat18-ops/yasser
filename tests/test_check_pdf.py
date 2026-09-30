# tests/test_check_pdf.py
"""PDF quality gates (plan Task 9b.3): the medical deliverable passes; one defect per ID fails with that ID."""
import pathlib, tempfile, unittest
from harness.tools import check_pdf, config
from tests.helpers import REPO

PROJECT = REPO / "projects/ai-in-medicine"
GOOD = PROJECT / "deliverables/AI_in_Health_Care_Interprofessional.pdf"
TTF = r"C:\Windows\Fonts\arial.ttf"   # the base-14 fonts cannot draw an em dash


# the frozen Word deliverable has two real defects, found when the layout gates were added: a bad break (page 90: a
# glossary line starts with "—", PDF-DASH) and a white strip above the cover image (page 1, PDF-BLEED since D-02).
# It stays as it is, so the baseline is subtracted
BASELINE = {"PDF-DASH", "PDF-BLEED"}


def fitz_rect(page, fx0, fy0, fx1, fy1):
    import fitz
    r = page.rect
    return fitz.Rect(r.width * fx0, r.height * fy0, r.width * fx1, r.height * fy1)


def failing(report):
    return {c["id"] for c in check_pdf.failures(report)} - BASELINE


class CheckPdfTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cfg = config.load(PROJECT)
        cls.tmp = tempfile.TemporaryDirectory()

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def defect(self, name, edit, outline=True):
        from pypdf import PdfReader, PdfWriter
        if outline:
            w = PdfWriter(clone_from=PdfReader(str(GOOD)))
        else:
            w = PdfWriter()
            w.append(str(GOOD), import_outline=False)
            w.add_metadata(PdfReader(str(GOOD)).metadata)
        edit(w)
        out = pathlib.Path(self.tmp.name) / f"{name}.pdf"
        with open(out, "wb") as fh:
            w.write(fh)
        return check_pdf.check(self.cfg, out)

    @staticmethod
    def add_font(w, font):
        from pypdf.generic import DictionaryObject, NameObject
        page = w.pages[0]
        fonts = page["/Resources"].get_object()["/Font"].get_object()
        fonts[NameObject("/FX")] = w._add_object(DictionaryObject(font))

    def test_medical_deliverable_passes(self):
        self.assertEqual(failing(check_pdf.check(self.cfg, GOOD)), set())

    def test_each_id(self):
        from pypdf.generic import DictionaryObject, NameObject, TextStringObject
        N = NameObject
        cases = {
            "PDF-SIZE": lambda w: setattr(w.pages[0], "mediabox", w.pages[0].mediabox.__class__([0, 0, 570, 810])),
            "PDF-BLANK": lambda w: w.add_blank_page(),
            "PDF-META": lambda w: w.add_metadata({"/Title": "Untitled"}),
            "PDF-TYPE3": lambda w: self.add_font(w, {N("/Type"): N("/Font"), N("/Subtype"): N("/Type3")}),
            "PDF-EMBED": lambda w: self.add_font(w, {N("/Type"): N("/Font"), N("/Subtype"): N("/Type1"),
                                                     N("/BaseFont"): N("/SitkaText")}),
            "PDF-FONTS": lambda w: self.add_font(w, {
                N("/Type"): N("/Font"), N("/Subtype"): N("/TrueType"), N("/BaseFont"): N("/ABCDEF+Papyrus"),
                N("/FontDescriptor"): DictionaryObject({N("/FontFile2"): TextStringObject("x")})}),
        }
        for cid, edit in cases.items():
            with self.subTest(cid):
                self.assertEqual(failing(self.defect(cid, edit)), {cid})
        with self.subTest("PDF-OUTLINE"):
            self.assertEqual(failing(self.defect("outline", lambda w: None, outline=False)), {"PDF-OUTLINE"})

    def test_medical_deliverable_dash_is_found(self):
        report = check_pdf.check(self.cfg, GOOD)
        dash = next(c for c in report["checks"] if c["id"] == "PDF-DASH")
        self.assertEqual((dash["status"], dash["measured"]["count"]), ("fail", 1))
        self.assertIn("page 90", dash["message"])
        bleed = next(c for c in report["checks"] if c["id"] == "PDF-BLEED")
        self.assertEqual((bleed["status"], bleed["measured"]["count"]), ("fail", 1))
        self.assertIn("page 1: paper shows at top-left, top-right, top", bleed["message"])

    def layout(self, draw):
        """layout_problems of a one-page A4 PDF on the theme's paper, drawn by `draw(page)`."""
        import fitz
        th = self.cfg["theme"]
        paper = tuple(int((th["palette"].get("paper") or "FFFFFF").lstrip("#")[i:i + 2], 16) / 255 for i in (0, 2, 4))
        doc = fitz.open()
        page = doc.new_page(width=595.28, height=841.89)
        page.draw_rect(page.rect, color=None, fill=paper)
        draw(page)
        out = pathlib.Path(self.tmp.name) / "layout.pdf"
        doc.save(str(out))
        doc.close()
        return {k: len(v) for k, v in check_pdf.layout_problems(self.cfg, out).items()}

    def test_layout_ids(self):
        left = self.cfg["theme"]["page"]["margins"]["left"] * check_pdf.PT_PER_CM
        head_y = self.cfg["theme"]["page"]["margins"]["top"] * check_pdf.PT_PER_CM - 20
        ok = lambda p: (p.insert_text((left, head_y), "Book title", fontsize=8),
                        p.insert_text((left + 250, head_y), "Chapter 1", fontsize=8),
                        p.insert_text((left, 300), "A line of body text - with a hyphen", fontsize=10))
        self.assertEqual(self.layout(ok), {"PDF-HEAD": 0, "PDF-BLEED": 0, "PDF-DASH": 0})
        cases = {
            "PDF-HEAD": lambda p: p.insert_text((left + 250, head_y), "A running head far too long to fit " * 3, fontsize=8),
            "PDF-DASH": lambda p: p.insert_text((left, 300), "— a line that starts with a dash", fontsize=10,
                                                  fontname="F0", fontfile=TTF),
            "PDF-BLEED": lambda p: p.draw_rect(fitz_rect(p, 0, 0, 1, 0.97), color=None, fill=(0.1, 0.1, 0.4)),
        }
        # D-02: paper only at the top-left corner is still a leak; D-03: a dash on a full-bleed page is still a bad break
        corner = lambda p: (p.draw_rect(fitz_rect(p, 0.1, 0, 1, 1), color=None, fill=(0.1, 0.1, 0.4)),
                            p.draw_rect(fitz_rect(p, 0, 0.1, 1, 1), color=None, fill=(0.1, 0.1, 0.4)))
        cases["PDF-BLEED (top-left)"] = corner
        cases["PDF-DASH (bleed page)"] = lambda p: (
            p.draw_rect(fitz_rect(p, 0, 0, 1, 1), color=None, fill=(0.1, 0.1, 0.4)),
            p.insert_text((left, 300), "— a dash on an opener", fontsize=10, fontname="F0", fontfile=TTF, color=(1, 1, 1)))
        for name, draw in cases.items():
            cid = name.split(" ")[0]
            with self.subTest(name):
                got = self.layout(draw)
                self.assertGreater(got[cid], 0)
                self.assertEqual({k for k, v in got.items() if v}, {cid})

    def test_wrapped_head_collides(self):
        left = self.cfg["theme"]["page"]["margins"]["left"] * check_pdf.PT_PER_CM
        top = self.cfg["theme"]["page"]["margins"]["top"] * check_pdf.PT_PER_CM
        got = self.layout(lambda p: (p.insert_text((left, top - 30), "Practical Pharmacology of the", fontsize=8),
                                     p.insert_text((left, top - 20), "System", fontsize=8)))
        self.assertEqual(got["PDF-HEAD"], 1)

    def test_font_family_names(self):
        self.assertEqual(check_pdf.family("/ABCDEF+SitkaHeading-Bold"), "sitkaheading")
        self.assertEqual(check_pdf.family("Sitka Heading"), "sitkaheading")
        self.assertEqual(check_pdf.family("/BCDEEE+SegoeUI"), "segoeui")
        self.assertEqual(check_pdf.family("/ABCDEF+SourceSerif4-BoldIt"), "sourceserif4")   # Adobe "It" suffix
        self.assertEqual(check_pdf.family("SourceSerif4-It"), "sourceserif4")


if __name__ == "__main__":
    unittest.main()
