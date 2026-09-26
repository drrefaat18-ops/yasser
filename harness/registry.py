"""Every executable in the repo and the gate it enforces (Task 7.3). The bypass matrix runs each row.

Harness scripts are listed here. Project scripts (legacy tools under projects/) are discovered: each one declares
its gate in its own shim, `enforce("<stage>", sys.argv)`, so this shared file names no project (Rule 8).
"""
import pathlib, re
from harness import state

REPO = pathlib.Path(__file__).resolve().parents[1]
SHIM = re.compile(r'enforce\("([a-z]+)"')
MAIN_GUARD = re.compile(r"^if __name__ ==", re.M)

HARNESS = [
    {"path": "harness/run_stage.py", "gate": "per-command", "why_ungated": None},
    {"path": "harness/preflight.py", "gate": None, "why_ungated": "environment probe, reads no project"},
    {"path": "harness/tools/compare_golden.py", "gate": None, "why_ungated": "compares two JSON files"},
    {"path": "harness/tools/manifest.py", "gate": None, "why_ungated": "repo migration validator"},
    {"path": "harness/tools/check_book.py", "gate": "rework", "why_ungated": None},
    {"path": "harness/tools/assemble.py", "gate": "build", "why_ungated": None},
    {"path": "harness/tools/build_book.py", "gate": "build", "why_ungated": None},
    {"path": "harness/tools/verify_refs.py", "gate": "rework", "why_ungated": None},
    {"path": "harness/tools/renumber_refs.py", "gate": "rework", "why_ungated": None},
    {"path": "harness/tools/leak_scan.py", "gate": None, "why_ungated": "scans shared harness code, reads no project"},
    {"path": "harness/tools/capture_golden.py", "gate": None,
     "why_ungated": "read-only regression capture; still enforces the projects rule"},
]


def _project_scripts(repo):
    rows = []
    for p in sorted((repo / "projects").rglob("*.py")):
        text = p.read_text(encoding="utf-8", errors="replace")
        if not MAIN_GUARD.search(text) or p.name.startswith("test_"):
            continue
        m = SHIM.search(text)
        rows.append({"path": p.relative_to(repo).as_posix(), "gate": m.group(1) if m else None,
                     "why_ungated": None})   # an ungated project script has no reason: the registry test fails
    return rows


EXECUTABLES = HARNESS + _project_scripts(REPO)


def _runner_commands():
    rows = []
    for s in state.STAGES:
        sid = s["id"]
        if sid == "new":
            continue
        if s["kind"] == "auto":
            rows.append({"argv": f"run {sid}", "gate": sid})
        else:
            rows.append({"argv": f"begin {sid}", "gate": sid})
            rows.append({"argv": f"complete {sid} --nonce 0", "gate": sid})
            if sid in ("rework", "translate"):
                rows.append({"argv": f"complete {sid} --nonce 0 --unit u", "gate": sid})
        if sid in state.IMPORTABLE:
            rows.append({"argv": f"import-history {sid} --dec DEC-000", "gate": sid})
    rows.append({"argv": "approve design --dec DEC-000", "gate": "design"})
    rows.append({"argv": "verify", "gate": state.ORDER[-1]})   # verify with no boundary gates the last stage
    return rows


RUNNER_COMMANDS = _runner_commands()
