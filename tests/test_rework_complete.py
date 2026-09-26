# tests/test_rework_complete.py
"""`complete rework` (plan Task 8.3): unit receipts per chapter, then the stage receipt; Rule 11 cap across units."""
import json, unittest
from tests.helpers import run_cli, temp_repo

SLUG = "no-errata"
P = ["--project", f"projects/{SLUG}"]


def begin(root):
    r = run_cli(root, *P, "begin", "rework")
    assert r.returncode == 0, r.stderr
    return r.stdout.split("nonce=")[1].split()[0]


def state(root):
    return json.loads((root / "projects" / SLUG / "state.json").read_text(encoding="utf-8"))


class ReworkComplete(unittest.TestCase):
    def test_failing_unit_names_the_check_id(self):
        with temp_repo(f"positive-config/{SLUG}", slug=SLUG, stamp=True) as root:
            ch = root / "projects" / SLUG / "chapters/ch01-forces.md"
            ch.write_text(ch.read_text(encoding="utf-8").replace("[2]", "[9]", 1), encoding="utf-8")
            n = begin(root)
            r = run_cli(root, *P, "complete", "rework", "--nonce", n, "--unit", "ch01")
            self.assertEqual(r.returncode, 1)
            self.assertIn("CIT-MISSING ch01", r.stderr)

    def test_units_then_final_writes_one_stage_receipt(self):
        with temp_repo(f"positive-config/{SLUG}", slug=SLUG, stamp=True) as root:
            n = begin(root)
            final = run_cli(root, *P, "complete", "rework", "--nonce", n)
            self.assertEqual(final.returncode, 1)
            self.assertIn("ERROR UNIT-INCOMPLETE", final.stderr)   # R3 (STEP 7): a unit receipt is missing
            u = run_cli(root, *P, "complete", "rework", "--nonce", n, "--unit", "ch01")
            self.assertEqual(u.returncode, 0, u.stderr)
            again = run_cli(root, *P, "complete", "rework", "--nonce", n, "--unit", "ch01")   # the lease is kept
            self.assertEqual(again.returncode, 0, again.stderr)
            unit = state(root)["receipts"]["rework"]["units"]["ch01"]
            self.assertEqual(unit["verify_refs_summary"], {"total": 2, "exists": 0, "no_doi_allowed": 2})
            self.assertIn("chapters/glossary.md", unit["inputs"])
            final = run_cli(root, *P, "complete", "rework", "--nonce", n)
            self.assertEqual(final.returncode, 0, final.stderr)
            rec = state(root)["receipts"]["rework"]
            self.assertEqual((rec["status"], sorted(rec["units"])), ("ok", ["ch01"]))
            self.assertIsNone(state(root)["active_run"])
            v = run_cli(root, *P, "verify", "--through", "rework")
            self.assertEqual(v.returncode, 0, v.stderr)

    def test_book_level_failure_blocks_final(self):
        with temp_repo(f"positive-config/{SLUG}", slug=SLUG, stamp=True) as root:
            n = begin(root)
            self.assertEqual(run_cli(root, *P, "complete", "rework", "--nonce", n, "--unit", "ch01").returncode, 0)
            g = root / "projects" / SLUG / "chapters/glossary.md"
            g.write_text("# Glossary\n", encoding="utf-8")
            final = run_cli(root, *P, "complete", "rework", "--nonce", n)
            self.assertEqual(final.returncode, 1)
            self.assertIn("ERROR CHECK: GLOSS-MIN book", final.stderr)

    def test_subagent_cap_spans_units(self):                           # S7-10
        with temp_repo(f"positive-config/{SLUG}", slug=SLUG, stamp=True) as root:
            n = begin(root)
            u = run_cli(root, *P, "complete", "rework", "--nonce", n, "--unit", "ch01", "--subagent", "a", "--subagent", "b")
            self.assertEqual(u.returncode, 0, u.stderr)
            final = run_cli(root, *P, "complete", "rework", "--nonce", n, "--subagent", "c")
            self.assertEqual(final.returncode, 1)
            self.assertIn("ERROR SUBAGENT-CAP", final.stderr)
            redo = run_cli(root, *P, "complete", "rework", "--nonce", n, "--unit", "ch01", "--subagent", "a")   # replaces its own
            self.assertEqual(redo.returncode, 0, redo.stderr)


if __name__ == "__main__":
    unittest.main()
