# tests/test_preflight.py
import json, subprocess, sys, unittest
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

if __name__ == "__main__":
    unittest.main()
