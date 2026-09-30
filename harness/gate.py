"""Gate for every executable outside the runner (Rule 7, core §2.3). Legacy shim:

    import sys, pathlib
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4]))  # repo root
    from harness.gate import enforce
    PROJECT = enforce("<stage>", sys.argv)
"""
import sys
from harness import paths, state


def _take_project(argv):
    for i, a in enumerate(argv):
        if a == "--project" and i + 1 < len(argv):
            value = argv[i + 1]
            del argv[i:i + 2]
            return value
        if a.startswith("--project="):
            del argv[i]
            return a.split("=", 1)[1]
    return None


def enforce(stage_id, argv, content_only=False):
    """Removes `--project P` from argv (in place), resolves it inside projects/, runs require_gates(stage_id).
    Any failure prints `ERROR <CODE>: ...` and exits 1; there is no bypass."""
    try:
        arg = _take_project(argv)
        if arg is None:
            raise state.GateError("PROJECT-REQUIRED", f"{argv[0]} needs --project projects/<slug>")
        project = paths.resolve_project(arg, must_exist=True)
        state.require_gates(project, stage_id, content_only=content_only)
        return project
    except state.GateError as e:
        print(f"ERROR {e}", file=sys.stderr)
        sys.exit(1)
