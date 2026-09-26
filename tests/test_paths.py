# tests/test_paths.py
import os, pathlib, unittest
from harness import paths, state
from tests.helpers import temp_repo

class ResolveProjectTest(unittest.TestCase):
    def test_resolve_project_rejects_escape(self):
        for bad in ["projects/../harness", "projects/a/b", "harness", "projects/../projects/../x"]:
            with self.assertRaises(state.GateError) as cm:
                paths.resolve_project(bad, must_exist=False)
            self.assertIn(cm.exception.code, {"PROJECT-OUTSIDE", "PROJECT-NAME"})

    def test_rejects_bad_name(self):
        with self.assertRaises(state.GateError) as cm:
            paths.resolve_project("projects/Bad_Name", must_exist=False)
        self.assertEqual(cm.exception.code, "PROJECT-NAME")

    def test_trailing_slash_ok(self):
        p = paths.resolve_project("projects/good-name/", must_exist=False)
        self.assertEqual(p.name, "good-name")

    def test_symlink_out_rejected(self):
        with temp_repo() as root:
            link = root / "projects" / "linked"
            try:
                os.symlink(root / "harness", link, target_is_directory=True)
            except OSError:
                self.skipTest("symlinks need developer mode on Windows")
            with self.assertRaises(state.GateError):
                paths.resolve_project(str(link), must_exist=True, repo=root)
