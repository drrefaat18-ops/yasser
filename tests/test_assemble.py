# tests/test_assemble.py
"""Assembler (plan Task 8.1): path-relative asset rewrite (INV-40), config-driven order and contents list."""
import re, subprocess, sys, unittest
from harness.tools import assemble, config
from tests.helpers import REPO, temp_repo

MED = REPO / "projects/ai-in-medicine"
LINK = re.compile(r"(!\[[^\]]*\]\()([^)\s]+)(\))")


def normalise_links(text, base):
    """Image links -> project-relative paths of their targets, so two outputs in different folders compare."""
    return LINK.sub(lambda m: m.group(1) + (base / m.group(2)).resolve().relative_to(MED.resolve()).as_posix() + m.group(3), text)


class AssembleTest(unittest.TestCase):
    def test_medical_book_equals_deliverable_up_to_link_base(self):
        """The deliverable was assembled at the repo root before STEP 6 (its links are root-relative, DEC-035);
        build/ output links are relative to build/. With both resolved to their targets the books are identical."""
        cfg = config.load(MED)
        book, probs = assemble.assemble(cfg)
        self.assertEqual(probs, [])
        deliv = (MED / "deliverables/AI_in_Health_Care_Interprofessional.md").read_text(encoding="utf-8").replace("\r\n", "\n")
        self.assertEqual(normalise_links(book, MED / "build"), normalise_links(deliv, MED))
        self.assertNotIn("](rework/", book)
        self.assertIn("](../rework/figures/", book)
        self.assertIn("](../images/", book)

    def test_asset_outside_roots_and_missing(self):
        cfg = config.load(REPO / "tests/fixtures/positive-config/no-mcq")
        ch = cfg.path("chapters") / "ch01-forces.md"
        self.assertTrue(assemble.resolve_asset(ch, "figures/ball.png", cfg).is_file())
        self.assertFalse(assemble.resolve_asset(ch, "figures/none.png", cfg).is_file())
        for bad in ("../brief.json", "../../x.png", "../design/p.png"):
            with self.assertRaises(assemble.AssetOutside):
                assemble.resolve_asset(ch, bad, cfg)

    def test_cli_gated_on_rework_and_dry_run(self):   # S9-03: `run build` is the only writer of build/
        run = lambda root, slug: subprocess.run([sys.executable, "harness/tools/assemble.py", "--project", f"projects/{slug}"],
                                                cwd=root, capture_output=True, text=True, encoding="utf-8")
        with temp_repo("positive-config/no-mcq", slug="no-mcq", stamp=True) as root:
            r = run(root, "no-mcq")   # build needs a valid rework receipt; this fixture has none (Rule 7)
            self.assertEqual(r.returncode, 1)
            self.assertIn("ERROR UPSTREAM-MISSING", r.stderr)
        with temp_repo(project_from="projects/ai-in-medicine", stamp=True) as root:
            r = run(root, "ai-in-medicine")
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn("(dry run, not written)", r.stdout)
            self.assertFalse((root / "projects/ai-in-medicine/build/AI_in_Health_Care_Interprofessional.md").exists())

    def test_missing_image_is_a_problem(self):
        # through the CLI a changed chapter or asset stales an upstream receipt first; the check itself is here
        with temp_repo("positive-config/no-mcq", slug="no-mcq") as root:
            cfg = config.load(root / "projects/no-mcq")
            ch = cfg.path("chapters") / "ch01-forces.md"
            ch.write_text(ch.read_text(encoding="utf-8") + "\n![x](figures/none.png)\n![y](fig:no-such)\n", encoding="utf-8")
            self.assertEqual(assemble.assemble(cfg)[1], ["ch01-forces.md: missing image figures/none.png",
                                                         "ch01-forces.md: fig:no-such is not in the figure manifest"])

    def test_contents_inserted_before_configured_section(self):
        cfg = config.load(REPO / "tests/fixtures/positive-config/no-mcq")
        book, probs = assemble.assemble(cfg)
        self.assertEqual(probs, [])
        self.assertLess(book.index("## Contents"), book.index("## Using This Book"))
        self.assertIn("- [Chapter 1: Forces and Motion](#chapter-1-forces-and-motion)", book)
        self.assertIn("- [Glossary](#glossary)", book)
        self.assertIn("![An orange ball slowing down on grass](../figures/out/ball.png)\n\n"   # manifest figure (STEP 9):
                      "*Figure 1.1 — A ball rolling to a stop*  \nTest fixture (original)\n", book)   # alt, caption, credit, licence


if __name__ == "__main__":
    unittest.main()
