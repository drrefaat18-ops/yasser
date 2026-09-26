# tests/test_run_stage.py
import json, unittest
from tests.helpers import temp_repo, run_cli

class RunnerTest(unittest.TestCase):
    def test_new_then_verify_through_new(self):
        with temp_repo() as root:
            r = run_cli(root, "--project", "projects/book-one", "new")
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual(run_cli(root, "--project", "projects/book-one", "verify", "--through", "new").returncode, 0)

    def test_begin_ingest_without_intake_approval(self):
        with temp_repo() as root:
            run_cli(root, "--project", "projects/book-one", "new")
            r = run_cli(root, "--project", "projects/book-one", "run", "ingest")
            self.assertEqual(r.returncode, 1)
            self.assertIn("ERROR NO-APPROVAL", r.stderr)

    def test_crashed_run_needs_abort(self):
        with temp_repo("state-basic", stamp=True) as root:
            p = ["--project", "projects/fixture-book"]
            r = run_cli(root, *p, "begin", "evaluate")
            self.assertEqual(r.returncode, 0, r.stderr)
            r2 = run_cli(root, *p, "begin", "evaluate")
            self.assertEqual(r2.returncode, 1)
            self.assertIn("ERROR RUN-ACTIVE", r2.stderr)
            self.assertIn("evaluate", r2.stderr)
            self.assertEqual(run_cli(root, *p, "abort", "evaluate", "--reason", "crash test").returncode, 0)
            self.assertEqual(run_cli(root, *p, "begin", "evaluate").returncode, 0)

    def test_complete_needs_matching_nonce(self):
        with temp_repo("state-basic", stamp=True) as root:
            p = ["--project", "projects/fixture-book"]
            run_cli(root, *p, "begin", "evaluate")
            r = run_cli(root, *p, "complete", "evaluate", "--nonce", "0000")
            self.assertIn("ERROR NONCE-MISMATCH", r.stderr)

    def test_approve_needs_dec_row(self):
        with temp_repo("state-basic", stamp=True) as root:
            r = run_cli(root, "--project", "projects/fixture-book", "approve", "intake", "--dec", "DEC-999")
            self.assertIn("ERROR DEC-MISSING", r.stderr)

    def test_begin_prints_nonce_and_brief(self):
        with temp_repo("state-basic", stamp=True) as root:
            r = run_cli(root, "--project", "projects/fixture-book", "begin", "evaluate")
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertRegex(r.stdout, r"nonce=[0-9a-f]{16}")
            self.assertIn("evaluation/findings.json", r.stdout)

    def test_init_state_refuses_existing(self):
        with temp_repo() as root:
            (root / "projects" / "old-book").mkdir()
            self.assertEqual(run_cli(root, "--project", "projects/old-book", "init-state").returncode, 0)
            r = run_cli(root, "--project", "projects/old-book", "init-state")
            self.assertEqual(r.returncode, 1)
            self.assertIn("ERROR PROJECT-EXISTS", r.stderr)
            st = json.loads((root / "projects" / "old-book" / "state.json").read_text(encoding="utf-8"))
            self.assertIs(st["receipts"]["new"]["args"]["adopted"], True)

    def test_new_refuses_existing_and_outside(self):
        with temp_repo() as root:
            self.assertEqual(run_cli(root, "--project", "projects/book-one", "new").returncode, 0)
            self.assertIn("ERROR PROJECT-EXISTS", run_cli(root, "--project", "projects/book-one", "new").stderr)
            self.assertIn("ERROR PROJECT-OUTSIDE", run_cli(root, "--project", "harness", "new").stderr)


class SubagentCapTest(unittest.TestCase):
    def test_more_than_two_subagents_refused(self):                            # S7-10
        with temp_repo("state-basic", stamp=True) as root:
            p = ["--project", "projects/fixture-book"]
            nonce = run_cli(root, *p, "begin", "evaluate").stdout.split("nonce=")[1].split()[0]
            r = run_cli(root, *p, "complete", "evaluate", "--nonce", nonce, *["--subagent", "x"] * 3)
            self.assertEqual(r.returncode, 1)
            self.assertIn("ERROR SUBAGENT-CAP", r.stderr)
            r = run_cli(root, *p, "complete", "evaluate", "--nonce", nonce, "--subagent", " ")
            self.assertEqual(r.returncode, 2)
