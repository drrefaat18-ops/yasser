# tests/test_check_pdf.py
"""PDF quality gates (plan Task 9b.3): the medical deliverable passes; one defect per ID fails with that ID."""
import pathlib, tempfile, unittest
from harness.tools import check_pdf, config
from tests.helpers import REPO

PROJECT = REPO / "projects/ai-in-medicine"
GOOD = PROJECT / "deliverables/AI_in_Health_Care_Interprofessional.pdf"


def failing(report):
    return {c["id"] for c in check_pdf.failures(report)}


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

    def test_font_family_names(self):
        self.assertEqual(check_pdf.family("/ABCDEF+SitkaHeading-Bold"), "sitkaheading")
        self.assertEqual(check_pdf.family("Sitka Heading"), "sitkaheading")
        self.assertEqual(check_pdf.family("/BCDEEE+SegoeUI"), "segoeui")


if __name__ == "__main__":
    unittest.main()
