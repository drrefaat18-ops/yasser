# tests/test_state.py
import json, pathlib, subprocess, unittest
from harness import state
from tests.helpers import temp_repo

class StateTest(unittest.TestCase):
    def test_graph_order_and_mandatory_sets(self):
        ids = [s["id"] for s in state.STAGES]
        self.assertEqual(ids, ["new", "intake", "ingest", "evaluate", "design", "translate", "rework", "build", "audit"])
        self.assertEqual(state.mandatory_stages({"goal": {"mode": "evaluate_only"}, "language": {"translation_required": False}}),
                         ["new", "intake", "ingest", "evaluate"])
        self.assertIn("translate", state.mandatory_stages({"goal": {"mode": "evaluate_and_rework"},
                                                           "language": {"translation_required": True}}))

    def test_required_approvals_derived_from_graph(self):
        self.assertEqual(state.required_approvals("ingest"), ["intake"])
        self.assertEqual(state.required_approvals("rework"), ["intake", "design"])
        self.assertEqual(state.required_approvals("intake"), [])

    def test_output_edit_makes_receipt_stale(self):
        with temp_repo("state-basic", stamp=True) as root:
            p = root / "projects" / "fixture-book"
            (p / "ingest" / "normalized.md").write_text("tampered\n", encoding="utf-8")
            probs = state.receipt_problems(p, "ingest", state.load(p), repo=root)
            self.assertTrue(any("output" in x for x in probs))

    def test_missing_approval_fails_not_skips(self):
        with temp_repo("state-basic", stamp=True) as root:
            p = root / "projects" / "fixture-book"
            state.write(p, lambda st: st["approvals"].pop("intake"))
            with self.assertRaises(state.GateError) as cm:
                state.require_gates(p, "evaluate", repo=root)
            self.assertEqual(cm.exception.code, "NO-APPROVAL")

    def test_dec_row_edit_makes_approval_stale(self):
        with temp_repo("state-basic", stamp=True) as root:
            p = root / "projects" / "fixture-book"
            d = p / "decisions.md"
            d.write_text(d.read_text(encoding="utf-8").replace("approve", "approve (edited)"), encoding="utf-8")
            with self.assertRaises(state.GateError) as cm:
                state.require_gates(p, "evaluate", repo=root)
            self.assertEqual(cm.exception.code, "DEC-ROW-CHANGED")

    def test_dirty_tool_refuses_receipt(self):
        with temp_repo("state-basic", stamp=True) as root:
            (root / "harness" / "state.py").write_text("# dirty\n" + (root / "harness" / "state.py").read_text(encoding="utf-8"), encoding="utf-8")
            with self.assertRaises(state.GateError) as cm:
                state.tool_sha(["harness/state.py"], repo=root)
            self.assertEqual(cm.exception.code, "DIRTY-TOOL")

    def test_tool_sha_rejects_untracked_and_empty(self):
        with temp_repo() as root:
            with self.assertRaises(state.GateError) as cm:
                state.tool_sha(["harness/does_not_exist.py"], repo=root)
            self.assertEqual(cm.exception.code, "TOOL-UNTRACKED")

    def test_extras_cannot_override_reserved_fields(self):
        with temp_repo("state-basic", stamp=True) as root:
            p = root / "projects" / "fixture-book"
            nonce = state.begin(p, "evaluate", repo=root)
            with self.assertRaises(state.GateError) as cm:
                state.complete(p, "evaluate", nonce, extras={"outputs": {}}, repo=root)
            self.assertEqual(cm.exception.code, "RESERVED-FIELD")

    def test_import_history_refused_unless_adopted_and_one_shot(self):
        with temp_repo("state-basic", stamp=True) as root:
            p = root / "projects" / "fixture-book"
            with self.assertRaises(state.GateError) as cm:
                state.import_history(p, "evaluate", "DEC-001", repo=root)
            self.assertEqual(cm.exception.code, "IMPORT-REFUSED")   # not adopted
            state.write(p, lambda st: st["receipts"]["new"]["args"].update(adopted=True))
            with self.assertRaises(state.GateError) as cm:
                state.import_history(p, "ingest", "DEC-001", repo=root)
            self.assertEqual(cm.exception.code, "IMPORT-REFUSED")   # ingest already has a receipt

    def test_leftover_lock_is_named_not_removed(self):
        with temp_repo("state-basic", stamp=True) as root:
            p = root / "projects" / "fixture-book"
            (p / "state.lock").write_text("pid=1 time=2026-09-25T00:00:00Z", encoding="utf-8")
            with self.assertRaises(state.GateError) as cm:
                state.write(p, lambda st: None)
            self.assertEqual(cm.exception.code, "LOCKED")
            self.assertIn("pid=1", str(cm.exception))
            self.assertTrue((p / "state.lock").exists())


class LifecycleTest(unittest.TestCase):
    def test_verify_through_ingest(self):
        with temp_repo("state-basic", stamp=True) as root:
            p = root / "projects" / "fixture-book"
            self.assertEqual(state.verify(p, "ingest", repo=root), [])
            (p / "ingest" / "normalized.md").write_text("tampered\n", encoding="utf-8")
            self.assertTrue(state.verify(p, "ingest", repo=root))

    def test_begin_complete_writes_receipt_and_clears_lease(self):
        with temp_repo("state-basic", stamp=True) as root:
            p = root / "projects" / "fixture-book"
            nonce = state.begin(p, "evaluate", repo=root)
            with self.assertRaises(state.GateError) as cm:   # required outputs missing
                state.complete(p, "evaluate", nonce, {}, repo=root)
            self.assertEqual(cm.exception.code, "SCHEMA")
            (p / "evaluation").mkdir()
            for f in ("findings.json", "scorecard.json"):
                (p / "evaluation" / f).write_text("{}", encoding="utf-8")
            for f in ("report.md", "codex-review.md", "fixes.md"):
                (p / "evaluation" / f).write_text("x\n", encoding="utf-8")
            (p / "ingest" / "conversion-report.json").write_text("{}", encoding="utf-8")
            st = state.complete(p, "evaluate", nonce, {"reviewer_model": "codex"}, repo=root)
            self.assertIsNone(st["active_run"])
            self.assertEqual(st["receipts"]["evaluate"]["status"], "ok")
            self.assertEqual(state.receipt_problems(p, "evaluate", st, repo=root), [])

    def test_run_auto_failure_writes_failed_receipt(self):
        with temp_repo("state-basic", stamp=True) as root:
            p = root / "projects" / "fixture-book"
            def boom(project):
                raise RuntimeError("converter crashed")
            with self.assertRaises(RuntimeError):
                state.run_auto(p, "ingest", boom, repo=root)
            st = state.load(p)
            self.assertEqual(st["receipts"]["ingest"]["status"], "failed")
            self.assertIn("converter crashed", st["receipts"]["ingest"]["error"])
            self.assertIsNone(st["active_run"])

    def test_approve_needs_row_naming_kind(self):
        with temp_repo("state-basic", stamp=True) as root:
            p = root / "projects" / "fixture-book"
            d = p / "decisions.md"
            d.write_text(d.read_text(encoding="utf-8") + "| DEC-009 | 2026-09-25 | user | approve something else | \"ok\" |\n",
                         encoding="utf-8")
            with self.assertRaises(state.GateError) as cm:
                state.approve(p, "intake", "DEC-009", repo=root)
            self.assertEqual(cm.exception.code, "DEC-MISSING")

    def test_unit_lifecycle(self):
        with temp_repo("state-basic", stamp=True) as root:
            p = root / "projects" / "fixture-book"
            # isolate the unit logic from the design/evaluate gates, which other tests cover
            orig = state.require_gates
            state.require_gates = lambda project, stage_id, repo=None: state.load(project)
            try:
                (p / "design").mkdir(); (p / "chapters").mkdir(); (p / "figures").mkdir()
                plan = {"schema_version": 1, "project_id": "fixture-book", "parts": [], "dropped": [],
                        "chapters": [{"id": c, "file": f"{c}.md", "title": c, "word_budget": 100, "part_id": None,
                                      "source_refs": []} for c in ("ch01", "ch02")]}
                (p / "design" / "chapter-plan.json").write_text(json.dumps(plan), encoding="utf-8")
                for f in ("design.md", "errata-seed.md"):
                    (p / "design" / f).write_text("x\n", encoding="utf-8")
                for c in ("ch01", "ch02"):
                    (p / "chapters" / f"{c}.md").write_text(f"# {c}\n", encoding="utf-8")
                (p / "figures" / "figures.json").write_text('{"schema_version": 1, "figures": []}', encoding="utf-8")
                nonce = state.begin(p, "rework", repo=root)
                with self.assertRaises(state.GateError) as cm:
                    state.complete(p, "rework", nonce, {}, unit="ch09", repo=root)
                self.assertEqual(cm.exception.code, "UNIT-UNKNOWN")
                st = state.complete(p, "rework", nonce, {}, unit="ch01", repo=root)
                self.assertIsNotNone(st["active_run"])                      # a unit keeps the lease
                with self.assertRaises(state.GateError) as cm:
                    state.complete(p, "rework", nonce, {}, final=True, repo=root)
                self.assertEqual(cm.exception.code, "UNIT-INCOMPLETE")
                state.complete(p, "rework", nonce, {}, unit="ch02", repo=root)
                (p / "chapters" / "ch01.md").write_text("# ch01 edited\n", encoding="utf-8")
                with self.assertRaises(state.GateError) as cm:              # a stale unit blocks the stage receipt
                    state.complete(p, "rework", nonce, {}, final=True, repo=root)
                self.assertEqual(cm.exception.code, "UNIT-INCOMPLETE")
                state.complete(p, "rework", nonce, {}, unit="ch01", repo=root)
                st = state.complete(p, "rework", nonce, {}, final=True, repo=root)
                self.assertIsNone(st["active_run"])
                self.assertEqual(sorted(st["receipts"]["rework"]["units"]), ["ch01", "ch02"])
                self.assertEqual(st["receipts"]["rework"]["status"], "ok")
            finally:
                state.require_gates = orig
