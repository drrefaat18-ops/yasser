"""The one stage runner (core §2). Every command routes through harness/state.py gates.

  python harness/run_stage.py --project projects/<slug> <command> ...
Commands: new | init-state | begin STAGE [--amend] [--author-model M] | complete STAGE --nonce N [--unit U]
          [--subagent REASON ...] | run STAGE | abort STAGE --reason TEXT | approve intake|design --dec DEC-NNN
          | import-history STAGE --dec DEC-NNN [--replace] | verify [--through STAGE]
Exit: 0 ok; 1 gate or check failure (stderr `ERROR <CODE>: ...`, one line per problem); 2 usage error.
"""
import argparse, json, pathlib, sys

REPO = pathlib.Path(__file__).resolve().parents[1]
MAX_SUBAGENTS = 2   # Rule 11
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))
from harness import paths, state  # noqa: E402
from harness.stages import build as build_stage, complete_checks, contracts, new as new_stage  # noqa: E402

# auto stages register their implementation here: stage -> fn(project) -> extras (ingest 8.4, build 8.2)
AUTO_RUNNERS = {"build": build_stage.run}
AGENTIC = [s["id"] for s in state.STAGES if s["kind"] == "agentic"]
AUTO = [s["id"] for s in state.STAGES if s["kind"] == "auto" and s["id"] != "new"]


class CheckFailed(Exception):
    def __init__(self, problems):
        super().__init__("; ".join(problems))
        self.problems = problems


def _brief(project, stage_id):
    _, outs = contracts.files(project, stage_id)
    lines = [f"stage {stage_id}: required outputs"] + [f"  {o}" for o in outs]
    if stage_id in contracts.UNIT_STAGES:
        st = state.load(project)
        done = st["receipts"].get(stage_id, {}).get("units", {})
        todo = [u for u in contracts.units(project, stage_id)
                if u not in done or state._unit_problems(project, stage_id, u, done[u], None)]
        lines.append("units missing or stale: " + (", ".join(todo) if todo else "none"))
    return "\n".join(lines)


def cmd_begin(project, a):
    if a.stage not in AGENTIC:
        raise ValueError(f"{a.stage} is an auto stage; use `run {a.stage}`")
    state.require_gates(project, a.stage)   # gate errors before usage checks (bypass matrix)
    if a.stage == "translate" and not a.author_model:
        raise ValueError("begin translate needs --author-model (translation contract §6)")
    nonce = state.begin(project, a.stage, amend=a.amend, author_model=a.author_model or "claude")
    print(f"nonce={nonce}")
    print(_brief(project, a.stage))


def cmd_complete(project, a):
    st = state.require_gates(project, a.stage)   # gate errors first, before any content check
    state.check_lease(st, a.stage, a.nonce)
    reasons = a.subagent or []
    if any(not r.strip() for r in reasons):
        raise ValueError("--subagent needs a non-empty reason")
    if len(reasons) > MAX_SUBAGENTS:   # ponytail: per complete call; a unit stage's cap across units is STEP 8's
        raise state.GateError("SUBAGENT-CAP", f"{len(reasons)} subagents logged; Rule 11 allows at most {MAX_SUBAGENTS}")
    if a.stage not in complete_checks.CHECKS:
        raise state.GateError("NOT-IMPLEMENTED", f"{a.stage} has no completion checks yet (STEP 8/11)")
    extras, probs = complete_checks.CHECKS[a.stage](project, st["active_run"], a.unit)
    if probs:
        raise CheckFailed(probs)
    if reasons:
        extras["subagents"] = [{"reason": r} for r in reasons]
    state.complete(project, a.stage, a.nonce, extras, unit=a.unit, final=a.unit is None)
    print(f"completed {a.stage}" + (f" unit {a.unit}" if a.unit else ""))


def cmd_run(project, a):
    if a.stage not in AUTO:
        raise ValueError(f"{a.stage} is not an auto stage; use begin/complete")
    state.require_gates(project, a.stage)
    if a.stage not in AUTO_RUNNERS:
        raise state.GateError("NOT-IMPLEMENTED", f"`run {a.stage}` is implemented in STEP 8")
    state.run_auto(project, a.stage, AUTO_RUNNERS[a.stage])
    print(f"ran {a.stage}")


def cmd_verify(project, a):
    fails = state.verify(project, a.through)
    for sid, r in state.load(project)["receipts"].items() if (project / "state.json").exists() else []:
        if r.get("imported"):
            print(f"info: {sid} receipt is imported ({r['dec_id']}, commit {r['imported_at_commit'][:12]})")
    for line in fails:   # each line is `CODE: message`
        print(f"ERROR {line}", file=sys.stderr)
    if fails:
        raise SystemExit(1)
    print("verify ok" + (f" through {a.through}" if a.through else ""))


def parser():
    ap = argparse.ArgumentParser(prog="run_stage.py")
    ap.add_argument("--project", required=True)
    sub = ap.add_subparsers(dest="command", required=True)
    sub.add_parser("new")
    sub.add_parser("init-state")
    b = sub.add_parser("begin")
    b.add_argument("stage", choices=state.ORDER)
    b.add_argument("--amend", action="store_true")
    b.add_argument("--author-model")
    c = sub.add_parser("complete")
    c.add_argument("stage", choices=state.ORDER)
    c.add_argument("--nonce", required=True)
    c.add_argument("--unit")
    c.add_argument("--subagent", action="append", help="one per Claude subagent spawned, with its reason (Rule 11)")
    r = sub.add_parser("run")
    r.add_argument("stage", choices=state.ORDER)
    x = sub.add_parser("abort")
    x.add_argument("stage", choices=state.ORDER)
    x.add_argument("--reason", required=True)
    p = sub.add_parser("approve")
    p.add_argument("kind", choices=sorted(state.APPROVAL_SETS))
    p.add_argument("--dec", required=True)
    i = sub.add_parser("import-history")
    i.add_argument("stage", choices=state.ORDER)
    i.add_argument("--dec", required=True)
    i.add_argument("--replace", action="store_true", help="re-import over an imported receipt under a new DEC (R25)")
    v = sub.add_parser("verify")
    v.add_argument("--through", choices=state.ORDER)
    return ap


def main(argv=None):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    a = parser().parse_args(argv)
    try:
        if a.command == "new":
            print(f"created {new_stage.run(a.project)}")
            return 0
        project = paths.resolve_project(a.project, must_exist=True)
        if a.command == "init-state":
            print(f"adopted {new_stage.init_state(a.project)}")
        elif a.command == "begin":
            cmd_begin(project, a)
        elif a.command == "complete":
            cmd_complete(project, a)
        elif a.command == "run":
            cmd_run(project, a)
        elif a.command == "abort":
            state.abort(project, a.stage, a.reason)
            print(f"aborted {a.stage}")
        elif a.command == "approve":
            state.approve(project, a.kind, a.dec)
            print(f"approved {a.kind} ({a.dec})")
        elif a.command == "import-history":
            state.import_history(project, a.stage, a.dec, replace=a.replace)
            print(f"imported {a.stage} ({a.dec})")
        elif a.command == "verify":
            cmd_verify(project, a)
    except state.GateError as e:
        print(f"ERROR {e}", file=sys.stderr)
        return 1
    except CheckFailed as e:
        for p in e.problems:
            print(f"ERROR CHECK: {p}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as e:
        print(f"ERROR SCHEMA: invalid JSON: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"usage error: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
