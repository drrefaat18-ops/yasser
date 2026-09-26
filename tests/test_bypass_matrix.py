# tests/test_bypass_matrix.py
import json, pathlib, subprocess, sys, unittest
from harness import registry, state
from tests.helpers import temp_repo, REPO

AFTER_INTAKE = set(state.ORDER[state.ORDER.index("intake") + 1:])
AFTER_INGEST = set(state.ORDER[state.ORDER.index("ingest") + 1:])
DESIGN_GATED = set(state.ORDER[state.ORDER.index("translate"):])


def edit_json(path, fn):
    d = json.loads(path.read_text(encoding="utf-8")); fn(d); path.write_text(json.dumps(d), encoding="utf-8")


SETUPS = {
    "no-approval": lambda p: edit_json(p / "state.json", lambda st: st["approvals"].pop("intake")),
    "edit-after-approval": lambda p: edit_json(p / "brief.json", lambda b: b["identity"].update(title=b["identity"]["title"] + " ")),
    "dec-row-edited": lambda p: (p / "decisions.md").write_text((p / "decisions.md").read_text(encoding="utf-8").replace("approve intake", "approve intake (edited)"), encoding="utf-8"),
    "stale-upstream": lambda p: (p / "ingest" / "normalized.md").write_text("tampered\n", encoding="utf-8"),
    "no-design": lambda p: edit_json(p / "state.json", lambda st: st["approvals"].pop("design")),
}
CODE = {"no-approval": "NO-APPROVAL", "edit-after-approval": "APPROVAL-STALE", "dec-row-edited": "DEC-ROW-CHANGED",
        "stale-upstream": "UPSTREAM-STALE", "no-design": "NO-APPROVAL"}


def applies(case, stage):
    if case in ("no-approval", "edit-after-approval", "dec-row-edited"):   # the plan table: every stage after intake
        return stage in AFTER_INTAKE
    if case == "stale-upstream":
        return stage in AFTER_INGEST
    if case == "no-design":
        return stage in DESIGN_GATED
    return True


def invocations():
    for row in registry.EXECUTABLES:
        if row["gate"] not in (None, "per-command"):
            yield row["path"], row["gate"], lambda proj, t=row["path"]: [sys.executable, t] + (["--project", proj] if proj else [])
    for cmd in registry.RUNNER_COMMANDS:
        yield f"run_stage {cmd['argv']}", cmd["gate"], lambda proj, c=cmd: [sys.executable, "harness/run_stage.py", "--project", proj, *c["argv"].split()]


def run(root, argv):
    return subprocess.run(argv, cwd=root, capture_output=True, text=True, encoding="utf-8")


class BypassMatrix(unittest.TestCase):
    def test_cases(self):
        for name, stage, argv in invocations():
            for case, code in CODE.items():
                with self.subTest(exe=name, case=case), temp_repo("bypass", slug="bypass-book", stamp=True, with_legacy=True) as root:
                    SETUPS[case](root / "projects" / "bypass-book")
                    r = run(root, argv("projects/bypass-book"))
                    if applies(case, stage):
                        self.assertNotEqual(r.returncode, 0, r.stdout)
                        self.assertIn(f"ERROR {code}", r.stderr)
                    else:
                        self.assertNotIn(f"ERROR {code}", r.stderr)
            with self.subTest(exe=name, case="outside"), temp_repo("bypass", slug="bypass-book", stamp=True, with_legacy=True) as root:
                r = run(root, argv("harness"))
                self.assertIn("ERROR PROJECT-OUTSIDE", r.stderr)

    def test_missing_project_flag(self):
        for row in registry.EXECUTABLES:
            if row["gate"] in (None, "per-command"):
                continue
            with self.subTest(exe=row["path"]), temp_repo("bypass", slug="bypass-book", stamp=True, with_legacy=True) as root:
                self.assertIn("ERROR PROJECT-REQUIRED", run(root, [sys.executable, row["path"]]).stderr)

    def test_staleness_during_agentic_work(self):
        for sid in [s["id"] for s in state.STAGES if s["kind"] == "agentic" and s["id"] in ("evaluate", "design")]:
            with self.subTest(stage=sid), temp_repo("bypass", slug="bypass-book", stamp=True, with_legacy=True) as root:
                p = ["--project", "projects/bypass-book"]
                b = run(root, [sys.executable, "harness/run_stage.py", *p, "begin", sid])
                self.assertEqual(b.returncode, 0, b.stderr)
                nonce = b.stdout.split("nonce=")[1].split()[0]
                SETUPS["edit-after-approval"](root / "projects" / "bypass-book")
                c = run(root, [sys.executable, "harness/run_stage.py", *p, "complete", sid, "--nonce", nonce])
                self.assertIn("ERROR APPROVAL-STALE", c.stderr)

    def test_registry_covers_every_script(self):
        mains = {str(p.relative_to(REPO)).replace("\\", "/") for p in REPO.rglob("*.py")
                 if "__main__" in p.read_text(encoding="utf-8", errors="replace")
                 and not str(p.relative_to(REPO)).startswith(("tests", ".git"))
                 and not p.name.startswith("test_")}
        self.assertEqual(mains, {r["path"] for r in registry.EXECUTABLES})
        for r in registry.EXECUTABLES:
            self.assertTrue(r["gate"] or r["why_ungated"], r["path"])

    def test_runner_commands_cover_every_stage(self):
        gated = {c["gate"] for c in registry.RUNNER_COMMANDS}
        self.assertEqual(gated - {None}, set(state.ORDER) - {"new"})
