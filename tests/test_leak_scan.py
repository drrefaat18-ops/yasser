# tests/test_leak_scan.py
"""Scoped leak scan (core §9.5)."""
import pathlib, shutil, subprocess, sys, tempfile, unittest
from tests.helpers import REPO


def copy_scope(tmp):
    shutil.copytree(REPO / "harness", pathlib.Path(tmp) / "harness", ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copytree(REPO / "tests/fixtures/leak", pathlib.Path(tmp) / "tests/fixtures/leak")


def scan(root):
    return subprocess.run([sys.executable, str(REPO / "harness/tools/leak_scan.py"), "--root", str(root)],
                          capture_output=True, text=True, encoding="utf-8")


class LeakScan(unittest.TestCase):
    def test_clean_tree_passes(self):
        r = subprocess.run([sys.executable, "harness/tools/leak_scan.py"], cwd=REPO, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_term_list_is_current(self):
        r = subprocess.run([sys.executable, "tests/tools/make_forbidden.py", "--check"], cwd=REPO, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout)
        terms = (REPO / "tests/fixtures/leak/forbidden.txt").read_text(encoding="utf-8").split("\n")
        for t in ("diagnos*", "DSM", "CBT", "Through Four Lenses", "Pharmacy"):   # S7-09 carry-forward; config labels
            self.assertIn(t, terms)

    def test_planted_literal_fails(self):
        forbidden = (REPO / "tests/fixtures/leak/forbidden.txt").read_text(encoding="utf-8").split("\n")[0]
        with tempfile.TemporaryDirectory() as tmp:
            copy_scope(tmp)
            (pathlib.Path(tmp) / "harness" / "planted.py").write_text(f"X = {forbidden!r}\n", encoding="utf-8")
            r = scan(tmp)
            self.assertEqual(r.returncode, 1)
            self.assertIn("planted.py", r.stdout)

    def test_prefix_term_and_word_boundary(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy_scope(tmp)
            (pathlib.Path(tmp) / "harness" / "agents" / "x.md").write_text("A diagnostic step.\n", encoding="utf-8")
            self.assertIn("x.md:1: diagnos", scan(tmp).stdout)
        with tempfile.TemporaryDirectory() as tmp:
            copy_scope(tmp)
            (pathlib.Path(tmp) / "harness" / "ok.py").write_text("# comedic timing, a DSMX flag\n", encoding="utf-8")
            self.assertEqual(scan(tmp).returncode, 0)

    def test_skill_files_are_in_scope(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy_scope(tmp)
            skill = pathlib.Path(tmp) / ".claude/skills/book-x/SKILL.md"
            skill.parent.mkdir(parents=True)
            skill.write_text("Run it for each patient.\n", encoding="utf-8")
            self.assertIn("SKILL.md:1", scan(tmp).stdout)

    def test_absolute_path_fails(self):
        for planted in ("P = r'D:\\\\data'\n", "P = '/home/me'\n", "P = '/Users/me'\n"):
            with self.subTest(planted), tempfile.TemporaryDirectory() as tmp:
                copy_scope(tmp)
                (pathlib.Path(tmp) / "harness" / "abs.py").write_text(planted, encoding="utf-8")
                r = scan(tmp)
                self.assertEqual(r.returncode, 1)
                self.assertIn("absolute path", r.stdout)

    def test_missing_list_is_exit_2(self):
        with tempfile.TemporaryDirectory() as tmp:
            shutil.copytree(REPO / "harness", pathlib.Path(tmp) / "harness", ignore=shutil.ignore_patterns("__pycache__"))
            self.assertEqual(scan(tmp).returncode, 2)


if __name__ == "__main__":
    unittest.main()
