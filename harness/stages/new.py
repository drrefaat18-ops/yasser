"""`new` (create a project skeleton) and `init-state` (adopt an existing project directory), core §2.2 `new` row."""
import json, shutil
from harness import paths, schema, state

DIRS = ["agents", "source", "ingest", "evaluation", "design", "figures/src", "build", "audit"]
DECISIONS_HEADER = "| DEC | Date | Kind | Decision | User words |\n|---|---|---|---|---|\n"


def _write_state(project, args, repo):
    rec = {"stage": "new", "status": "ok", "args": args, "inputs": {},
           "outputs": state.hash_map(project, sorted(p.relative_to(project).as_posix() for p in project.rglob(".keep"))),
           "tool_sha": state.tool_sha(state.BY_ID["new"]["tool_paths"], repo), "time": state.now()}
    st = {"schema_version": 1, "project_id": project.name, "receipts": {"new": rec}, "approvals": {},
          "active_run": None, "aborts": []}
    errs = schema.validate(st, schema.load_schema("state"))
    if errs:
        raise state.GateError("SCHEMA", "; ".join(errs))
    (project / "state.json").write_text(json.dumps(st, ensure_ascii=False, indent=1, sort_keys=True) + "\n",
                                        encoding="utf-8", newline="\n")


def run(project_arg, repo=None):
    project = paths.resolve_project(project_arg, must_exist=False, repo=repo)
    if project.exists():
        raise state.GateError("PROJECT-EXISTS", f"{project} already exists; `new` never touches an existing directory")
    project.mkdir()
    try:
        for d in DIRS:
            (project / d).mkdir(parents=True)
            (project / d / ".keep").write_text("", encoding="utf-8")
        (project / "decisions.md").write_text(DECISIONS_HEADER, encoding="utf-8", newline="\n")
        _write_state(project, {"slug": project.name}, repo)
    except BaseException:
        shutil.rmtree(project)   # only this invocation created it
        raise
    return project


def init_state(project_arg, repo=None):
    """Adopt a project directory that predates the harness: write state.json with `new` args.adopted = true."""
    project = paths.resolve_project(project_arg, must_exist=True, repo=repo)
    if (project / "state.json").exists():
        raise state.GateError("PROJECT-EXISTS", f"{project / 'state.json'} already exists")
    if not (project / "decisions.md").exists():
        (project / "decisions.md").write_text(DECISIONS_HEADER, encoding="utf-8", newline="\n")
    _write_state(project, {"slug": project.name, "adopted": True}, repo)
    return project
