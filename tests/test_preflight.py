# tests/test_preflight.py
import json, os, subprocess, sys, unittest
from unittest import mock
from harness import preflight

class PreflightTest(unittest.TestCase):
    def test_missing_module_is_named(self):
        checks = preflight.check_module("definitely_not_a_module_xyz", group="core", required=True)
        self.assertFalse(checks["ok"])
        self.assertIn("definitely_not_a_module_xyz", checks["detail"])

    def test_optional_group_does_not_fail_default_run(self):
        checks = preflight.run(["core"]) + [dict(name="rdkit", group="chemistry", ok=False, detail="missing", required=False)]
        self.assertEqual(preflight.exit_code(checks), 0 if all(c["ok"] for c in checks if c["required"]) else 1)

    def test_cli_json_lists_every_check(self):
        out = subprocess.run([sys.executable, "harness/preflight.py", "--group", "core", "--json"],
                             capture_output=True, text=True)
        names = {c["name"] for c in json.loads(out.stdout)}
        self.assertTrue({"python>=3.11", "git", "write-lock"} <= names)

    def test_group_matrix(self):
        """Task 5.1 table: every check runs in each group it is listed under."""
        names = lambda g: {c["name"] for c in preflight.run([g])}
        self.assertTrue({"python-docx", "lxml", "Pillow", "pywin32", "word-com", "browser", "fonts"} <= names("build"))
        self.assertTrue({"matplotlib", "browser"} <= names("figures"))
        self.assertTrue({"python-docx", "lxml", "markitdown"} <= names("ingest"))
        self.assertEqual(names("golden"), {"pypdf"})
        self.assertEqual(len(preflight.run(["build", "figures"])), len({c["name"] for c in preflight.run(["build", "figures"])}))

    def test_unknown_group_is_refused(self):
        out = subprocess.run([sys.executable, "harness/preflight.py", "--group", "bulid"], capture_output=True, text=True)
        self.assertNotEqual(out.returncode, 0)
        self.assertIn("bulid", out.stderr)

    def _fonts_dir(self, names):
        import tempfile, pathlib
        d = tempfile.TemporaryDirectory()
        self.addCleanup(d.cleanup)
        fonts = pathlib.Path(d.name) / "Fonts"
        fonts.mkdir()
        for n in names:
            (fonts / n).write_bytes(b"")
        return {"WINDIR": d.name}

    def test_fonts_scoped_to_named_preset(self):
        """A book is checked against its own preset only, not the union of every preset."""
        preset = "ltr-textbook"
        need = preflight.preset_fonts(preset)
        self.assertLess(len(need), len(preflight.preset_fonts()))
        env = self._fonts_dir(need)
        with mock.patch.dict(os.environ, env, clear=True):
            self.assertTrue(preflight.check_fonts(preset)["ok"])
            self.assertFalse(preflight.check_fonts()["ok"])   # the union still demands the other presets' fonts

    def test_unknown_preset_fails_named(self):
        with mock.patch.dict(os.environ, self._fonts_dir([]), clear=True):
            c = preflight.check_fonts("no-such-preset")
        self.assertFalse(c["ok"])
        self.assertIn("no-such-preset", c["detail"])

    def test_fonts_without_windir_fails_named(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            c = preflight.check_fonts()
        self.assertFalse(c["ok"])
        self.assertIn("WINDIR", c["detail"])


if __name__ == "__main__":
    unittest.main()
