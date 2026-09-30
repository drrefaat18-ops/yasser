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


class ReviewFixTest(unittest.TestCase):
    """STEP 7 Codex review findings S7-01..S7-05 (docs/harness/reviews/step7-fixes.md)."""

    def _adopted(self, root):
        p = root / "projects" / "fixture-book"
        state.write(p, lambda st: (st["receipts"].pop("ingest"), st["receipts"]["new"]["args"].update(adopted=True)))
        (p / "history").mkdir()
        (p / "history" / "old-review.md").write_text("old review\n", encoding="utf-8")
        (p / "history" / "import.json").write_text(json.dumps({"schema_version": 1, "stages": {
            "ingest": {"inputs": ["source/book.md"], "outputs": ["ingest/normalized.md"]},
            "evaluate": {"inputs": ["ingest/normalized.md"], "outputs": ["history/old-review.md"]}}}), encoding="utf-8")
        d = p / "decisions.md"
        d.write_text(d.read_text(encoding="utf-8") + "| DEC-010 | 2026-09-26 | user | import-history ingest evaluate | \"ok\" |\n"
                     "| DEC-011 | 2026-09-26 | user | import-history ingest evaluate again | \"ok\" |\n", encoding="utf-8")
        return p

    def test_import_binds_manifest_and_lineage(self):                         # S7-01
        with temp_repo("state-basic", stamp=True) as root:
            p = self._adopted(root)
            st = state.import_history(p, "ingest", "DEC-010", repo=root)
            self.assertIn("history/import.json", st["receipts"]["ingest"]["inputs"])
            m = json.loads((p / "history" / "import.json").read_text(encoding="utf-8"))
            m["stages"]["evaluate"]["inputs"] = ["source/book.md"]              # does not consume ingest's output
            (p / "history" / "import.json").write_text(json.dumps(m), encoding="utf-8")
            self.assertTrue(any("import.json" in x for x in state.receipt_problems(p, "ingest", state.load(p), repo=root)))

    def test_lineage_refused(self):                                             # S7-01
        with temp_repo("state-basic", stamp=True) as root:
            p = self._adopted(root)
            m = json.loads((p / "history" / "import.json").read_text(encoding="utf-8"))
            m["stages"]["evaluate"]["inputs"] = ["source/book.md"]
            (p / "history" / "import.json").write_text(json.dumps(m), encoding="utf-8")
            state.import_history(p, "ingest", "DEC-010", repo=root)
            with self.assertRaises(state.GateError) as cm:
                state.import_history(p, "evaluate", "DEC-010", repo=root)
            self.assertIn("every output", str(cm.exception))

    def test_removed_entry_and_forged_import_are_stale(self):                   # S7-02
        with temp_repo("state-basic", stamp=True) as root:
            p = root / "projects" / "fixture-book"
            state.write(p, lambda st: st["receipts"]["ingest"]["outputs"].pop("ingest/normalized.md"))
            self.assertTrue(state.receipt_problems(p, "ingest", state.load(p), repo=root))
        with temp_repo("state-basic", stamp=True) as root:
            p = root / "projects" / "fixture-book"
            state.write(p, lambda st: st["receipts"]["intake"].update(imported=True, dec_id="DEC-001",
                                                                       dec_row_sha256=state.dec_row_hash(p, "DEC-001")[0]))
            self.assertTrue(any("imported flag" in x for x in state.receipt_problems(p, "intake", state.load(p), repo=root)))

    def test_import_cannot_sit_on_harness_receipt(self):                        # S7-05
        with temp_repo("state-basic", stamp=True) as root:
            p = self._adopted(root)
            nonce = state.begin(p, "ingest", repo=root)
            state.complete(p, "ingest", nonce, {}, final=True, repo=root)
            with self.assertRaises(state.GateError) as cm:
                state.import_history(p, "evaluate", "DEC-010", repo=root)
            self.assertIn("earlier stage", str(cm.exception))

    def test_replace_only_over_imported_with_new_dec(self):                     # R25
        with temp_repo("state-basic", stamp=True) as root:
            p = self._adopted(root)
            state.import_history(p, "ingest", "DEC-010", repo=root)
            with self.assertRaises(state.GateError):
                state.import_history(p, "ingest", "DEC-010", repo=root)          # one-shot without --replace
            with self.assertRaises(state.GateError):
                state.import_history(p, "ingest", "DEC-010", replace=True, repo=root)   # same DEC
            st = state.import_history(p, "ingest", "DEC-011", replace=True, repo=root)
            self.assertEqual(st["receipts"]["ingest"]["dec_id"], "DEC-011")
        with temp_repo("state-basic", stamp=True) as root:
            p = root / "projects" / "fixture-book"
            state.write(p, lambda st: st["receipts"]["new"]["args"].update(adopted=True))
            with self.assertRaises(state.GateError):
                state.import_history(p, "ingest", "DEC-001", replace=True, repo=root)   # harness receipt

    def test_approve_needs_full_hashes_in_dec_row(self):                        # S7-03
        with temp_repo("state-basic", stamp=True) as root:
            p = root / "projects" / "fixture-book"
            with self.assertRaises(state.GateError) as cm:
                state.approve(p, "intake", "DEC-001", repo=root)
            self.assertEqual(cm.exception.code, "DEC-HASH-MISMATCH")
            from harness import hashing
            hs = " ".join(f"{f} {hashing.hash_file(p / f)}" for f in state.APPROVAL_SETS["intake"](p))
            d = p / "decisions.md"
            d.write_text(d.read_text(encoding="utf-8") + f"| DEC-012 | 2026-09-26 | user | approve intake: {hs} | \"ok\" |\n",
                         encoding="utf-8")
            self.assertEqual(state.approve(p, "intake", "DEC-012", repo=root)["approvals"]["intake"]["dec_id"], "DEC-012")

    def test_tool_paths_cover_check_modules_and_schemas(self):                  # S7-04
        import re
        root = pathlib.Path(__file__).resolve().parents[1]
        control = {"state", "hashing", "paths", "schema"}
        for stage in ("intake", "evaluate", "design", "audit"):
            tp = set(state.BY_ID[stage]["tool_paths"])
            mods, seen = [f"harness/stages/complete_checks/{stage}.py"], set()
            while mods:
                m = mods.pop()
                if m in seen:
                    continue
                seen.add(m)
                self.assertIn(m, tp, f"{stage}: {m} is executed but not in tool_paths")
                src = (root / m).read_text(encoding="utf-8")
                for name in re.findall(r"^from harness import (.+)$", src, re.M):
                    for n in (x.strip() for x in name.split(",")):
                        if n not in control or (stage == "intake" and n == "schema"):
                            mods.append(f"harness/{n}.py")
                mods += [f"harness/stages/complete_checks/{n}.py"
                         for n in re.findall(r"^from harness\.stages\.complete_checks\.(\w+) import", src, re.M)]
                for sch in re.findall(r'validate_file\([^)]*"([\w-]+)"\)', src) if m.endswith(f"/{stage}.py") else []:
                    self.assertIn(f"harness/schemas/{sch}.v1.json", tp, f"{stage}: schema {sch} not in tool_paths")
            if stage in ("evaluate", "audit"):
                self.assertTrue({"harness/schemas/findings.v1.json", "harness/schemas/scorecard.v1.json"} <= tp)


class ContentOnlyGate(unittest.TestCase):   # DEC-H01: a finished book's side products ignore later tool commits only
    def test_tool_commit_blocks_normal_gate_not_content_only(self):
        with temp_repo("bypass", slug="bypass-book", stamp=True, with_legacy=True) as root:
            p = root / "projects" / "bypass-book"
            with open(root / "harness" / "schema.py", "a", encoding="utf-8") as f:
                f.write("\n# later tool change\n")
            subprocess.run(["git", "commit", "-qam", "tool change"], cwd=root, check=True, capture_output=True)
            with self.assertRaises(state.GateError) as cm:
                state.require_gates(p, "rework", repo=root)
            self.assertIn("tool changed", str(cm.exception))
            state.require_gates(p, "rework", repo=root, content_only=True)
            (p / "ingest" / "normalized.md").write_text("tampered\n", encoding="utf-8")
            with self.assertRaises(state.GateError) as cm:
                state.require_gates(p, "rework", repo=root, content_only=True)
            self.assertEqual(cm.exception.code, "UPSTREAM-STALE")
