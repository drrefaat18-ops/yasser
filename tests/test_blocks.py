# tests/test_blocks.py
"""The shared block grammar (plan Task 9b.1): one parse for the DOCX and the HTML writer."""
import unittest
from harness.tools import blocks, build_book, config
from tests.helpers import REPO


class BlocksTest(unittest.TestCase):
    def setUp(self):
        self.cfg = config.load(REPO / "projects/ai-in-medicine")

    def test_medical_chapters_cover_every_block_type(self):   # h3 is not used by the medical book
        seen = set()
        for _, path in self.cfg.chapters():
            seen |= {b["t"] for b in blocks.parse(path.read_text(encoding="utf-8"), self.cfg, "chapter")}
        glossary = self.cfg.book_file("glossary")
        seen |= {b["t"] for b in blocks.parse(glossary.read_text(encoding="utf-8"), self.cfg, "glossary")}
        self.assertLessEqual({"section", "para", "callout", "grid", "table", "image", "question", "bullet",
                              "numbered", "glossary", "answer"}, seen)

    def test_sub_and_superscript(self):
        spans = [(s["text"], s["sub"], s["sup"]) for s in blocks.inline("H~2~O and Ca^2+^")]
        self.assertEqual(spans, [("H", False, False), ("2", True, False), ("O and Ca", False, False), ("2+", False, True)])
        self.assertEqual(blocks.plain("**CO~2~** [site](https://x.org)"), "CO2 site")

    def test_unicode_scripts_become_sub_and_sup(self):
        spans = [(s["text"], s["sub"], s["sup"]) for s in blocks.inline("Ca²⁺ and CO₂")]
        self.assertEqual(spans, [("Ca", False, False), ("2+", False, True), (" and CO", False, False), ("2", True, False)])

    def test_tilde_with_spaces_is_text(self):
        self.assertEqual([s["text"] for s in blocks.inline("about ~5 % and ~10 %")], ["about ~5 % and ~10 %"])

    def test_table_inside_a_box_stays_a_table(self):
        text = ("# Chapter 1: T\n\n## 1.1 A\n\n> **Deeper Dive:** Before the table.\n>\n> | Item | Cost |\n"
                "> |---|---|\n> | Visit | 20 |\n>\n> After the table.\n")
        box = [b for b in blocks.parse(text, self.cfg, "chapter") if b["t"] == "callout"][0]
        self.assertEqual(box["paras"], ["Before the table.", {"rows": [["Item", "Cost"], ["Visit", "20"]]}, "After the table."])
        self.assertEqual(box["text"], "Before the table. After the table.")
        d = build_book._docx()
        doc = d["Document"]()
        bk = build_book.Book(self.cfg)
        build_book.setup_styles(d, doc, bk)
        R = build_book.Renderer(d, doc, bk)
        R.callout(doc, box["key"], box["text"], box["paras"])
        inner = doc.tables[0].cell(0, 0).tables
        self.assertEqual([[c.text for c in r.cells] for r in inner[0].rows], [["Item", "Cost"], ["Visit", "20"]])

    def test_docx_subscript_run(self):
        d = build_book._docx()
        doc = d["Document"]()
        bk = build_book.Book(self.cfg)
        R = build_book.Renderer(d, doc, bk)
        p = doc.add_paragraph()
        R.inline(p, "CO~2~")
        self.assertEqual([r.text for r in p.runs], ["CO", "2"])
        self.assertIn('w:vertAlign w:val="subscript"', p.runs[1]._r.xml)


if __name__ == "__main__":
    unittest.main()
