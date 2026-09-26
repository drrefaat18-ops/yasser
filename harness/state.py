"""Receipts, approvals, gates, lease (core §2.3, §3)."""
import datetime, json, os, pathlib, re, secrets, subprocess
from harness import hashing, paths, schema
from harness.stages import contracts

CONTROL_PLANE = {"state.json", "state.lock", "decisions.md"}


class GateError(Exception):
    def __init__(self, code, message):
        super().__init__(f"{code}: {message}")
        self.code = code


# Tool provenance design (plan fix S4-01): a stage's tool_paths list only the code that decides that stage's
# outputs or checks. The control plane (state.py, paths.py, hashing.py) is not listed: it is covered by tests,
# and listing it would stale every receipt of every project on any control-plane fix. Stages that have no tool
# yet list harness/stages/contracts.py (their file-set definition); the task that ships a stage's tool replaces
# it (Tasks 8.x, 9.x, 11.x state their STAGES edit). tool_sha refuses untracked paths.
STAGES = [
    {"id": "new", "kind": "auto", "tool_paths": ["harness/stages/new.py"]},
    {"id": "intake", "kind": "agentic", "tool_paths": ["harness/schema.py", "harness/schemas/brief.v1.json", "harness/schemas/rubric.v1.json",
                                                       "harness/schemas/template.v1.json", "harness/schemas/theme.v1.json",
                                                       "harness/schemas/overlay.v1.json", "harness/stages/complete_checks/common.py",
                                                       "harness/stages/complete_checks/intake.py", "harness/locales.py"]},
    {"id": "ingest", "kind": "auto", "tool_paths": ["harness/stages/contracts.py"]},     # -> ingest.py, convert_docx.py in 8.4
    {"id": "evaluate", "kind": "agentic", "tool_paths": ["harness/stages/complete_checks/common.py", "harness/stages/complete_checks/evaluate.py",
                                                         "harness/schemas/findings.v1.json", "harness/schemas/scorecard.v1.json"]},
    {"id": "design", "kind": "agentic", "tool_paths": ["harness/stages/complete_checks/common.py", "harness/stages/complete_checks/design.py",
                                                       "harness/schemas/chapter-plan.v1.json"]},
    {"id": "translate", "kind": "agentic", "tool_paths": ["harness/stages/contracts.py"]},  # -> check_translation.py, complete_checks/translate.py in 11.x
    {"id": "rework", "kind": "agentic", "tool_paths": ["harness/tools/check_book.py", "harness/tools/assemble.py",   # + verify_refs.py,
                                                       "harness/tools/config.py", "harness/text.py", "harness/locales.py"]},  # complete_checks/rework.py (8.3)
    {"id": "build", "kind": "auto", "tool_paths": ["harness/stages/build.py", "harness/tools/assemble.py", "harness/tools/build_book.py",
                                                   "harness/tools/config.py", "harness/tools/capture_golden.py",   # report facts
                                                   "harness/tools/check_book.py", "harness/text.py", "harness/locales.py",  # via capture
                                                   "harness/preflight.py", "harness/presets"]},   # + figures (9.1)
    {"id": "audit", "kind": "agentic", "tool_paths": ["harness/stages/complete_checks/common.py", "harness/stages/complete_checks/audit.py",
                                                      "harness/schemas/findings.v1.json", "harness/schemas/scorecard.v1.json"]},
]
RESERVED = {"stage", "status", "args", "inputs", "outputs", "tool_sha", "time", "error", "invalidated_by",
            "units", "imported", "imported_at_commit", "dec_id", "dec_row_sha256"}
ORDER = [s["id"] for s in STAGES]
BY_ID = {s["id"]: s for s in STAGES}
DESIGN_GATED_FROM = "translate"


def required_approvals(stage_id):
    i = ORDER.index(stage_id)
    if i <= ORDER.index("intake"):
        return []
    return ["intake"] + (["design"] if i >= ORDER.index(DESIGN_GATED_FROM) else [])


def _translation_applies(project):
    brief = _read_json(project / "brief.json") or {}
    return brief.get("language", {}).get("translation_required") is True


APPROVAL_SETS = {
    "intake": lambda p: ["brief.json", "rubric.json", "template.json", "theme.json"]
                        + sorted(f"agents/{f.name}" for f in (p / "agents").glob("*.json")),
    "design": lambda p: ["design/design.md", "design/chapter-plan.json", "design/errata-seed.md"]
                        + (["termbase.json"] if _translation_applies(p) else []),
}


def mandatory_stages(brief):
    if brief["goal"]["mode"] == "evaluate_only":
        return ["new", "intake", "ingest", "evaluate"]
    base = ["new", "intake", "ingest", "evaluate", "design", "rework", "build", "audit"]
    if brief["language"]["translation_required"]:
        base.insert(base.index("rework"), "translate")
    return base


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _read_json(path):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def load(project):
    st = _read_json(project / "state.json")
    if st is None:
        raise GateError("PROJECT-MISSING", f"{project / 'state.json'} missing; run `new` first")
    errs = schema.validate(st, schema.load_schema("state"))
    if errs:
        raise GateError("SCHEMA", "state.json: " + "; ".join(errs))
    return st


def write(project, mutate):
    lock = project / "state.lock"
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        raise GateError("LOCKED", f"{lock} exists ({lock.read_text(encoding='utf-8', errors='replace').strip()}); "
                                  "another process holds it or crashed; remove it by hand after checking")
    try:
        os.write(fd, f"pid={os.getpid()} time={now()}".encode())
        os.close(fd)
        st = load(project)
        mutate(st)
        tmp = project / "state.json.tmp"
        tmp.write_text(json.dumps(st, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
        os.replace(tmp, project / "state.json")
        return st
    finally:
        lock.unlink(missing_ok=True)


def _git(repo, *args):
    r = subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True)
    if r.returncode != 0:
        raise GateError("GIT-ERROR", f"git {' '.join(args)} failed: {r.stderr.strip()}")
    return r.stdout


def tool_sha(tool_paths, repo=None):
    repo = repo or paths.REPO
    for tp in tool_paths:
        if not _git(repo, "ls-files", "--", tp).strip():
            raise GateError("TOOL-UNTRACKED", f"{tp} is not a tracked file or directory")
    dirty = _git(repo, "status", "--porcelain", "--", *tool_paths)
    if dirty.strip():
        raise GateError("DIRTY-TOOL", f"uncommitted changes in {', '.join(tool_paths)}:\n{dirty}")
    sha = _git(repo, "log", "-1", "--format=%H", "--", *tool_paths).strip()
    if not sha:
        raise GateError("GIT-ERROR", f"no commit touches {tool_paths}")
    return sha


def hash_map(project, rels):
    out = {}
    for rel in rels:
        if pathlib.PurePosixPath(rel).name in CONTROL_PLANE:
            continue
        out[rel] = hashing.hash_file(project / rel)
    return out


def dec_row_hash(project, dec):
    text = (project / "decisions.md").read_text(encoding="utf-8").replace("\r\n", "\n")
    rows = [l.rstrip() for l in text.split("\n") if l.startswith(f"| {dec} |")]
    if len(rows) != 1:
        raise GateError("DEC-MISSING", f"{dec}: expected exactly one row in decisions.md, found {len(rows)}")
    return hashing.hash_bytes(rows[0].encode("utf-8")), rows[0]


IMPORT_MANIFEST = "history/import.json"


def _import_files(project, stage_id):
    """(inputs, outputs) an imported receipt must hash: the stage's history/import.json lists plus import.json itself (N2)."""
    spec = (_read_json(project / IMPORT_MANIFEST) or {}).get("stages", {}).get(stage_id) or {}
    return sorted(set(spec.get("inputs", [])) | {IMPORT_MANIFEST}), sorted(spec.get("outputs", []))


def _expected_files(project, stage_id, r, unit=None):
    """The file sets a receipt must cover, rebuilt from the contract (or the import manifest), never from state.json."""
    if r.get("imported"):
        if unit is not None:
            return [], [contracts._chapter_file(project, unit)]
        return _import_files(project, stage_id)
    return contracts.files(project, stage_id, unit)


def _keyset_problems(label, r, ins, outs):
    probs = []
    for kind, want in (("inputs", ins), ("outputs", outs)):
        got = set(r.get(kind, {}))
        if got != {w for w in want if pathlib.PurePosixPath(w).name not in CONTROL_PLANE}:
            probs.append(f"{label}: {kind} recorded {sorted(got)} do not match the contract {sorted(want)}")
    return probs


def receipt_problems(project, stage_id, st, repo=None):
    r = st["receipts"].get(stage_id)
    if r is None:
        return [f"{stage_id}: no receipt"]
    probs = []
    if r.get("stage", stage_id) != stage_id:
        probs.append(f"{stage_id}: receipt names stage {r.get('stage')!r}")
    if r.get("imported") and (stage_id not in IMPORTABLE or r.get("tool_sha") != "imported"):
        probs.append(f"{stage_id}: imported flag on a stage that cannot be imported, or tool_sha is not `imported`")
    if r["status"] == "ok":
        try:
            probs += _keyset_problems(stage_id, r, *_expected_files(project, stage_id, r))
        except (KeyError, TypeError) as e:
            probs.append(f"{stage_id}: file contract cannot be rebuilt ({e})")
        if stage_id in contracts.UNIT_STAGES:
            want = contracts.units(project, stage_id)
            got = r.get("units", {})
            if sorted(got) != sorted(want):
                probs.append(f"{stage_id}: unit receipts {sorted(got)} != units {sorted(want)}")
            for u in want:
                if u in got:
                    probs += _unit_problems(project, stage_id, u, got[u], repo)
    if r["status"] != "ok":
        probs.append(f"{stage_id}: status {r['status']}")
    if r.get("invalidated_by"):
        probs.append(f"{stage_id}: invalidated by {r['invalidated_by']}")
    for kind in ("inputs", "outputs"):
        for rel, h in r[kind].items():
            f = project / rel
            if not f.exists():
                probs.append(f"{stage_id}: {kind[:-1]} missing {rel}")
            elif hashing.hash_file(f) != h:
                probs.append(f"{stage_id}: {kind[:-1]} changed {rel}")
    for fid, ru in (r.get("rulings") or {}).items():   # Task 7.2: an edited ruling row stales the receipt
        try:
            if dec_row_hash(project, ru["dec_id"])[0] != ru["dec_row_sha256"]:
                probs.append(f"{stage_id}: ruling {fid} ({ru['dec_id']}) DEC row changed")
        except GateError as e:
            probs.append(f"{stage_id}: ruling {fid}: {e}")
    if r.get("imported"):
        try:
            if dec_row_hash(project, r["dec_id"])[0] != r["dec_row_sha256"]:
                probs.append(f"{stage_id}: import DEC row changed")
        except GateError as e:
            probs.append(f"{stage_id}: {e}")
        return probs  # plan N2: imported artifacts are bound by content, not by a harness tool SHA
    try:
        if tool_sha(BY_ID[stage_id]["tool_paths"], repo) != r["tool_sha"]:
            probs.append(f"{stage_id}: tool changed since receipt")
    except GateError as e:
        probs.append(f"{stage_id}: {e}")
    return probs


def approval_problems(project, kind, st):
    a = st["approvals"].get(kind)
    if a is None:
        return [("NO-APPROVAL", f"{kind} approval missing")]
    probs = []
    expected = sorted(APPROVAL_SETS[kind](project))
    if sorted(a["files"]) != expected:
        probs.append(("APPROVAL-SET-CHANGED", f"{kind} approval covers {sorted(a['files'])}, current set is {expected}"))
    for rel, h in a["files"].items():
        f = project / rel
        if not f.exists() or hashing.hash_file(f) != h:
            probs.append(("APPROVAL-STALE", f"{kind} approval: {rel} changed or missing; the user must re-approve"))
    try:
        if dec_row_hash(project, a["dec_id"])[0] != a["dec_row_sha256"]:
            probs.append(("DEC-ROW-CHANGED", f"{a['dec_id']} row in decisions.md changed after approval"))
    except GateError as e:
        probs.append((e.code, str(e)))
    return probs


def upstream(stage_id, brief):
    mand = mandatory_stages(brief) if brief else ORDER[: ORDER.index("intake") + 1]
    return [s for s in ORDER[: ORDER.index(stage_id)] if s in mand]


def require_gates(project, stage_id, repo=None):
    st = load(project)
    for kind in required_approvals(stage_id):
        probs = approval_problems(project, kind, st)
        if probs:
            raise GateError(probs[0][0], "; ".join(m for _, m in probs))
    brief = _read_json(project / "brief.json")
    for up in upstream(stage_id, brief):
        if up not in st["receipts"]:
            raise GateError("UPSTREAM-MISSING", f"{stage_id} needs a valid {up} receipt; none exists")
        probs = receipt_problems(project, up, st, repo)
        if probs:
            raise GateError("UPSTREAM-STALE", "; ".join(probs))
    return st


def invalidate_downstream(st, stage_id):
    mark = f"{stage_id}@{now()}"
    for sid in ORDER[ORDER.index(stage_id) + 1:]:
        if sid in st["receipts"]:
            st["receipts"][sid]["invalidated_by"] = mark


def _allowed_stages(project):
    brief = _read_json(project / "brief.json")
    return mandatory_stages(brief) if brief else ["new", "intake"]


def begin(project, stage_id, amend=False, author_model=None, repo=None):
    if amend and stage_id != "intake":
        raise ValueError("--amend is only for intake (core §3)")
    require_gates(project, stage_id, repo)
    if stage_id not in _allowed_stages(project):
        raise GateError("NOT-MANDATORY", f"{stage_id} is not in this project's mandatory stages {_allowed_stages(project)}")
    nonce = secrets.token_hex(8)

    def mutate(st):
        ar = st["active_run"]
        if ar:
            raise GateError("RUN-ACTIVE", f"{ar['stage']} (unit {ar['unit']}) is active since {ar['started_at']}, "
                                          f"nonce={ar['nonce']}; complete it or `abort {ar['stage']} --reason TEXT`")
        st["active_run"] = {"stage": stage_id, "unit": None, "nonce": nonce, "pid": os.getpid(),
                            "started_at": now(), "author_model": author_model}
        if not amend:
            invalidate_downstream(st, stage_id)
    write(project, mutate)
    return nonce


def _hashed(project, rels):
    missing = [r for r in rels if not (project / r).is_file()]
    if missing:
        raise GateError("SCHEMA", "required file(s) missing: " + ", ".join(missing))
    return hash_map(project, rels)


def _unit_problems(project, stage_id, name, r, repo):
    probs = []
    if r.get("status") != "ok":
        probs.append(f"{stage_id}/{name}: status {r.get('status')}")
    if bool(r.get("imported")) != (r.get("tool_sha") == "imported"):
        probs.append(f"{stage_id}/{name}: imported flag and tool_sha disagree")
    try:
        probs += _keyset_problems(f"{stage_id}/{name}", r, *_expected_files(project, stage_id, r, unit=name))
    except (KeyError, TypeError) as e:
        probs.append(f"{stage_id}/{name}: file contract cannot be rebuilt ({e})")
    for kind in ("inputs", "outputs"):
        for rel, h in r[kind].items():
            f = project / rel
            if not f.exists() or hashing.hash_file(f) != h:
                probs.append(f"{stage_id}/{name}: {kind[:-1]} changed or missing {rel}")
    if not r.get("imported"):
        try:
            if tool_sha(BY_ID[stage_id]["tool_paths"], repo) != r["tool_sha"]:
                probs.append(f"{stage_id}/{name}: tool changed since receipt")
        except GateError as e:
            probs.append(f"{stage_id}/{name}: {e}")
    return probs


def check_lease(st, stage_id, nonce):
    ar = st["active_run"]
    if not ar or ar["stage"] != stage_id:
        raise GateError("NO-ACTIVE-RUN", f"no active {stage_id} run; `begin {stage_id}` first")
    if ar["nonce"] != nonce:
        raise GateError("NONCE-MISMATCH", f"--nonce does not match the active {stage_id} run")


def complete(project, stage_id, nonce, extras, unit=None, final=False, repo=None):
    """Write the receipt. Unit stages: `unit=U` writes one unit receipt and keeps the lease; `unit=None, final=True`
    writes the stage receipt once every unit is valid, and clears the lease."""
    st = require_gates(project, stage_id, repo)
    check_lease(st, stage_id, nonce)
    reserved = sorted(RESERVED & set(extras))
    if reserved:
        raise GateError("RESERVED-FIELD", f"extras may not set {reserved}")
    unit_based = stage_id in contracts.UNIT_STAGES
    if unit is not None and (not unit_based or unit not in contracts.units(project, stage_id)):
        raise GateError("UNIT-UNKNOWN", f"{unit!r} is not a unit of {stage_id}: {contracts.units(project, stage_id)}")
    if unit_based and unit is None and not final:
        raise ValueError(f"{stage_id} is unit-based: pass a unit, or final=True for the stage receipt")
    ins, outs = contracts.files(project, stage_id, unit)
    rec = {"status": "ok", "args": {"unit": unit} if unit else {}, "inputs": _hashed(project, ins),
           "outputs": _hashed(project, outs), "tool_sha": tool_sha(BY_ID[stage_id]["tool_paths"], repo),
           "time": now(), **extras}

    if unit is not None:
        def mutate(s):
            r = s["receipts"].setdefault(stage_id, {
                "stage": stage_id, "status": "failed", "error": "units in progress; stage not completed",
                "args": {}, "inputs": {}, "outputs": {}, "tool_sha": rec["tool_sha"], "time": rec["time"]})
            r.setdefault("units", {})[unit] = rec
        return write(project, mutate)

    units_done = {}
    if unit_based:
        units_done = st["receipts"].get(stage_id, {}).get("units", {})
        want = contracts.units(project, stage_id)
        probs = [f"{stage_id}/{u}: no unit receipt" for u in want if u not in units_done]
        for u in want:
            if u in units_done:
                probs += _unit_problems(project, stage_id, u, units_done[u], repo)
        if probs:
            raise GateError("UNIT-INCOMPLETE", "; ".join(probs))

    def mutate(s):
        s["receipts"][stage_id] = {"stage": stage_id, **rec, **({"units": units_done} if unit_based else {})}
        s["active_run"] = None
    return write(project, mutate)


def run_auto(project, stage_id, fn, repo=None):
    """`fn(project) -> extras`. File sets come from contracts, never from fn."""
    nonce = begin(project, stage_id, repo=repo)
    try:
        return complete(project, stage_id, nonce, fn(project) or {}, final=True, repo=repo)
    except BaseException as e:
        try:
            sha = tool_sha(BY_ID[stage_id]["tool_paths"], repo)
        except GateError:
            sha = "unknown"

        def mutate(s):
            s["receipts"][stage_id] = {"stage": stage_id, "status": "failed", "args": {}, "inputs": {}, "outputs": {},
                                       "tool_sha": sha, "time": now(), "error": f"{type(e).__name__}: {e}"}
            s["active_run"] = None
        write(project, mutate)
        raise


def abort(project, stage_id, reason):
    if not reason or not reason.strip():
        raise ValueError("abort needs a non-empty --reason")

    def mutate(st):
        ar = st["active_run"]
        if not ar or ar["stage"] != stage_id:
            raise GateError("NO-ACTIVE-RUN", f"no active {stage_id} run to abort")
        st["aborts"].append({"stage": stage_id, "nonce": ar["nonce"], "reason": reason, "time": now()})
        st["active_run"] = None
    return write(project, mutate)


def approve(project, kind, dec, repo=None):
    if kind not in APPROVAL_SETS:
        raise ValueError(f"unknown approval kind {kind!r}")
    # gates first (R19), then the DEC row; the stage whose outputs are approved must hold a valid receipt (R4),
    # so unchecked files cannot be approved. For design, require_gates(design) is everything but the design approval.
    st = require_gates(project, kind, repo)
    h, row = dec_row_hash(project, dec)
    if kind.lower() not in row.lower():
        raise GateError("DEC-MISSING", f"{dec} row does not name the {kind} approval: {row}")
    probs = receipt_problems(project, kind, st, repo)
    if probs:
        raise GateError("UPSTREAM-STALE", "; ".join(probs))
    files = _hashed(project, APPROVAL_SETS[kind](project))
    shown = sorted(rel for rel, fh in files.items() if fh not in row)
    if shown:   # the user approved the hashes in the DEC row; they must be the hashes the gate will check
        raise GateError("DEC-HASH-MISMATCH", f"{dec} row does not show the full SHA-256 (hashing.hash_file) of {shown}")
    rec = {"kind": kind, "files": files, "dec_id": dec,
           "dec_row_sha256": h, "approved_at": now(), "approved_by": "user"}
    return write(project, lambda s: s["approvals"].__setitem__(kind, rec))


IMPORTABLE = {"ingest", "evaluate", "design", "rework"}


def import_history(project, stage_id, dec, replace=False, repo=None):
    """Adopt pre-harness artifacts as an imported receipt (plan N2). Refused unless every condition holds.
    `replace` (ruling R25) re-imports over an existing *imported* receipt under a new DEC; never over a harness receipt."""
    project = pathlib.Path(project)
    if stage_id not in IMPORTABLE:
        raise GateError("IMPORT-REFUSED", f"{stage_id}: only {sorted(IMPORTABLE)} can be imported")
    st = require_gates(project, stage_id, repo)   # gates first (R19)

    def refuse(why):
        raise GateError("IMPORT-REFUSED", f"{stage_id}: {why}")
    if st["receipts"].get("new", {}).get("args", {}).get("adopted") is not True:
        refuse("the project was not created as adopted (`new` receipt args.adopted)")
    old = st["receipts"].get(stage_id)
    if old is not None and not (replace and old.get("imported")):
        refuse("the stage already has a receipt" + (" that the harness wrote; only an imported one can be replaced"
                                                     if replace else ""))
    if replace and old is None:
        refuse("--replace needs an existing imported receipt")
    later = [s for s in ORDER[ORDER.index(stage_id) + 1:] if s in st["receipts"] and not st["receipts"][s].get("imported")]
    if later:
        refuse(f"later stage(s) {later} already ran in the harness")
    earlier = [s for s in ORDER[:ORDER.index(stage_id)] if s in IMPORTABLE and s in st["receipts"]
               and not st["receipts"][s].get("imported")]
    if earlier:
        refuse(f"earlier stage(s) {earlier} ran in the harness; history cannot sit on top of harness work")
    h, row = dec_row_hash(project, dec)
    if "import-history" not in row or stage_id not in row:
        refuse(f"{dec} row must contain `import-history` and `{stage_id}`: {row}")
    if replace and dec == old.get("dec_id"):
        refuse(f"--replace needs a new DEC row, not {dec}")
    if not (_read_json(project / IMPORT_MANIFEST) or {}).get("stages", {}).get(stage_id):
        refuse(f"{IMPORT_MANIFEST} does not list this stage")
    ins, outs = _import_files(project, stage_id)
    prev = [s for s in ORDER[:ORDER.index(stage_id)] if s in IMPORTABLE and s in st["receipts"]]
    if prev and set(_import_files(project, prev[-1])[1]) - set(ins):   # lineage: history consumed what came before it
        refuse(f"inputs must include every output of the imported {prev[-1]} stage; missing "
               f"{sorted(set(_import_files(project, prev[-1])[1]) - set(ins))}")
    rels = ins + outs
    root = project.resolve()
    for rel in rels:
        f = (project / rel).resolve()
        if not f.is_relative_to(root) or not f.is_file():
            refuse(f"{rel} is missing or outside the project")
    head = _git(repo or paths.REPO, "rev-parse", "HEAD").strip()
    base = {"status": "ok", "imported": True, "imported_at_commit": head, "dec_id": dec, "dec_row_sha256": h,
            "tool_sha": "imported", "time": now()}
    rec = {"stage": stage_id, "args": {}, "inputs": hash_map(project, ins), "outputs": hash_map(project, outs), **base}
    if stage_id == "rework":
        chapters = contracts.units(project, "rework")
        rec["units"] = {u: {"args": {"unit": u}, "inputs": {}, "outputs": hash_map(project, [contracts._chapter_file(project, u)]),
                            **base} for u in chapters}
    return write(project, lambda s: s["receipts"].__setitem__(stage_id, rec))


def independent_review_problems(extras):
    """EXT-TR-4: a stage that declares both models must have reviewer_model != author_model."""
    a, r = extras.get("author_model"), extras.get("reviewer_model")
    return [f"reviewer_model equals author_model ({a})"] if a and r and a == r else []


def verify(project, through=None, repo=None):
    """-> failure lines (empty means ok). Imported receipts are valid; the runner prints them as info."""
    try:
        st = load(project)
    except GateError as e:
        return [str(e)]
    mand = _allowed_stages(project)
    if through is not None and through not in ORDER:
        raise ValueError(f"unknown stage {through!r}")
    boundary = [s for s in mand if through is None or ORDER.index(s) <= ORDER.index(through)]
    last = through or mand[-1]
    nxt = ORDER[ORDER.index(last) + 1] if through and ORDER.index(last) + 1 < len(ORDER) else last
    fails = []
    try:
        require_gates(project, nxt, repo)
    except GateError as e:
        fails.append(str(e))
    for s in boundary:
        fails += [f"RECEIPT-STALE: {x}" for x in receipt_problems(project, s, st, repo)]
    ar = st["active_run"]
    if ar:
        fails.append(f"RUN-ACTIVE: {ar['stage']} nonce={ar['nonce']} started={ar['started_at']}")
    return fails
