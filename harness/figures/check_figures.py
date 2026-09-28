"""Figure checker (core §7.3, §7.5; plan Task 9.1). Emits one checker-report.v1 document, target `figures`.

Usage: python harness/figures/check_figures.py --project projects/<slug> [--json]
The CLI is a dry run: it renders into a temporary folder and checks those renders. `run build` checks the real
<figures>/out after rendering. Exit 0 iff no blocking check fails (CHEM-UNVERIFIED does not block, core §7.5);
1 otherwise or on a refused gate; 2 on a config error.
"""
import copy, json, os, pathlib, sys, tempfile

REPO = pathlib.Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))
from harness import figures, schema  # noqa: E402
from harness.figures import annotated, packs  # noqa: E402
from harness.tools import config  # noqa: E402

FIG_IDS = ["FIG-MANIFEST", "FIG-UNREFERENCED", "FIG-UNKNOWN", "FIG-CAPTION", "FIG-ALT", "FIG-LICENCE",
           "FIG-RESOLUTION", "FIG-AUTHOR-ASSET", "FIG-ANNOT"]
CHEM_IDS = ["CHEM-SMILES-INVALID", "CHEM-SANITIZE", "CHEM-SMARTS-INVALID", "CHEM-PUBCHEM-MISMATCH", "CHEM-UNVERIFIED"]
NON_BLOCKING = {"CHEM-UNVERIFIED"}
OWN_FIELDS = {"caption": "FIG-CAPTION", "alt": "FIG-ALT", "licence": "FIG-LICENCE", "credit": "FIG-LICENCE"}
MIN_DPI = 299.5          # 300 dpi at the placed width, allowing for the pixel rounding of the width
STATUS_OF = {"raster.existing": "existing", "author-asset": "needs-author-asset"}   # every other kind: generated
OFFLINE_ENV = "HARNESS_OFFLINE"   # set: cross-checks run offline and report `unverified`, never `pass`


def _item_schema():
    """figures.v1 without the fields that have their own check IDs, so a blank caption is FIG-CAPTION, not FIG-MANIFEST."""
    s = copy.deepcopy(schema.load_schema("figures"))
    item = s["properties"]["figures"]["items"]
    for f in OWN_FIELDS:
        item["properties"][f] = {}
    item["required"] = [r for r in item["required"] if r not in OWN_FIELDS]
    return s


def _inside(path, root):
    try:
        return path.resolve().is_relative_to(root.resolve())
    except OSError:
        return False


def _source_problem(cfg, fig):
    project = cfg["project"]
    src = project / fig["source"]
    if not _inside(src, project):
        return f"{fig['id']}: source {fig['source']!r} is outside the project"
    if fig["kind"] == "author-asset":
        return None
    if fig["kind"] == "raster.existing":
        roots = [project / r for r in cfg["template"]["paths"]["allowed_asset_roots"]]
        if not any(_inside(src, r) for r in roots) or _inside(src, figures.out_dir(cfg)):
            return f"{fig['id']}: an existing raster must lie under an allowed asset root (not {figures.out_dir(cfg).name}/)"
    elif not _inside(src, cfg.path("figures") / "src"):
        return f"{fig['id']}: a generated figure's source must lie under {cfg['template']['paths']['figures']}/src/"
    if not src.is_file():
        return f"{fig['id']}: source {fig['source']} missing"
    return None


def mode():
    return "offline" if os.environ.get(OFFLINE_ENV) else "live"


def check(project, cfg, out_dir=None, crosscheck_mode=None, rendered=True):
    """-> checker-report.v1 dict. `out_dir` holds the renders (default <figures>/out). `rendered=False` is the
    pre-render pass (render.render_all runs it first): manifest, references, fields, sources, packs and local
    chemistry validation, no resolution and no PubChem cross-check, so nothing unchecked is read or executed."""
    project = pathlib.Path(project)
    out_dir = out_dir or figures.out_dir(cfg)
    found = {i: [] for i in FIG_IDS + CHEM_IDS}   # id -> [(figure id or None, message)]
    found["_crosschecks"] = []   # the PubChem answer each structure was judged on (bound into build-report.json)
    man_path = figures.manifest_path(cfg)
    if not man_path.is_file():
        found["FIG-MANIFEST"].append((None, f"{man_path.relative_to(project).as_posix()} missing"))
        return _report(found, chem=False, crosschecks=None)
    try:
        man = json.loads(man_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        found["FIG-MANIFEST"].append((None, f"figures.json is not JSON: {e}"))
        return _report(found, chem=False, crosschecks=None)
    errs = schema.validate(man, _item_schema())
    if errs:
        found["FIG-MANIFEST"] += [(None, e) for e in errs]
        return _report(found, chem=False, crosschecks=None)
    figs = man["figures"]
    by_id = {}
    for f in figs:
        if f["id"] in by_id:
            found["FIG-MANIFEST"].append((f["id"], "duplicate id"))
        by_id[f["id"]] = f
    chapter_ids = {c["id"] for c, _ in cfg.chapters()}
    registry = packs.registry()
    allowed_packs = set(cfg["brief"]["figures"]["packs"])
    for f in figs:
        fid = f["id"]
        if f["chapter_id"] not in chapter_ids:
            found["FIG-MANIFEST"].append((fid, f"chapter_id {f['chapter_id']} is not in chapter-plan.json"))
        want = STATUS_OF.get(f["kind"], "generated")
        if f["status"] != want:
            found["FIG-MANIFEST"].append((fid, f"kind {f['kind']} needs status {want}, not {f['status']}"))
        p = _source_problem(cfg, f)
        if p:
            found["FIG-MANIFEST"].append((fid, p))
        if f["kind"] == annotated.KIND and not p:
            try:
                spec = annotated.load(cfg, f)
            except (json.JSONDecodeError, UnicodeDecodeError) as e:
                spec = f"not JSON: {e}"
            for msg in annotated.problems(cfg, spec):
                found["FIG-ANNOT"].append((fid, msg))
        if f["kind"] not in STATUS_OF and f["kind"] not in ("diagram.svg", annotated.KIND):
            name, mod = packs.pack_for(f["kind"], registry)
            if mod is None:
                found["FIG-MANIFEST"].append((fid, f"no registered pack renders kind {f['kind']}"))
            elif name not in allowed_packs:
                found["FIG-MANIFEST"].append((fid, f"pack {name} is not in brief.figures.packs"))
            elif hasattr(mod, "preflight") and mod.preflight():
                found["FIG-MANIFEST"].append((fid, f"pack {name} is not ready: " + "; ".join(mod.preflight())))
        for field, cid in OWN_FIELDS.items():
            v = f.get(field)
            if field == "licence":
                if v not in schema.load_schema("figures")["properties"]["figures"]["items"]["properties"]["licence"]["enum"]:
                    found[cid].append((fid, f"licence {v!r} is not in the allowed list"))
            elif not isinstance(v, str) or not v.strip():
                found[cid].append((fid, f"{field} is missing or blank"))
        if f["status"] == "needs-author-asset":
            found["FIG-AUTHOR-ASSET"].append((fid, f"needs an asset from the author ({f['source']})"))
    referenced = set()
    for entry, _, ids, direct in figures.references(cfg):
        for fid in ids:
            referenced.add(fid)
            if fid not in by_id:
                found["FIG-UNKNOWN"].append((fid, f"placed in {entry['id']}, not in figures.json"))
            elif by_id[fid]["chapter_id"] != entry["id"]:
                found["FIG-UNKNOWN"].append((fid, f"placed in {entry['id']}, but its chapter_id is {by_id[fid]['chapter_id']}"))
        for link in direct:
            found["FIG-UNKNOWN"].append((None, f"{entry['id']}: image {link} is placed without the manifest (use fig:<id>)"))
    for fid in by_id:
        if fid not in referenced:
            found["FIG-UNREFERENCED"].append((fid, "in figures.json, never placed in a chapter"))
    chem = [f for f in figs if f["kind"].startswith("chem.")]
    for f in chem:
        _chemistry(cfg, f, registry, crosscheck_mode or mode(), found, rendered)
    if not rendered:
        return _report(found, chem=bool(chem), crosschecks=None)
    width = cfg["theme"]["layout"]["text_width"]
    from harness.figures import render
    for f in figs:
        if found["FIG-MANIFEST"] or not render.renderable(cfg, f, registry):
            continue
        _, raster = figures.out_paths(cfg, f, out_dir)
        if not raster.is_file():
            found["FIG-RESOLUTION"].append((f["id"], f"not rendered ({raster.name} missing)"))
            continue
        from PIL import Image
        with Image.open(raster) as im:
            w, h = im.size
        placed = figures.placed_width_cm(w, h, width)
        dpi = w / (placed / 2.54)
        if dpi < MIN_DPI:
            found["FIG-RESOLUTION"].append((f["id"], f"{dpi:.0f} dpi at {placed:g} cm (needs 300)"))
    return _report(found, chem=bool(chem), crosschecks=found["_crosschecks"])


def _chemistry(cfg, f, registry, cmode, found, rendered):
    name, mod = packs.pack_for(f["kind"], registry)
    src = cfg["project"] / f["source"]
    if mod is None or mod.preflight() or _source_problem(cfg, f):
        return   # reported as FIG-MANIFEST
    try:
        spec = json.loads(src.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        found["FIG-MANIFEST"].append((f["id"], f"source {f['source']} is not JSON: {e}"))
        return
    if not isinstance(spec, dict) or spec.get("kind") != f["kind"]:
        got = spec.get("kind") if isinstance(spec, dict) else type(spec).__name__
        found["FIG-MANIFEST"].append((f["id"], f"manifest kind {f['kind']} but source kind {got!r}"))
        return
    findings = mod.validate(spec)
    for x in findings:
        found[x["id"]].append((f["id"], x["message"]))
    if findings or not rendered or f["kind"] not in getattr(mod, "CROSSCHECK_KINDS", mod.KINDS):
        return
    r = mod.crosscheck(spec, cmode, cfg.path("figures") / ".cache" / "pubchem")
    found["_crosschecks"].append({"figure": f["id"], **{k: r[k] for k in ("status", "url", "how", "response_sha256")
                                                          if k in r}})
    if r["status"] == "fail":
        found["CHEM-PUBCHEM-MISMATCH"].append((f["id"], r["detail"]))
    elif r["status"] == "unverified":
        found["CHEM-UNVERIFIED"].append((f["id"], r["detail"]))


def _report(found, chem, crosschecks):
    """One check per ID; `measured.figures` lists the figure ids it names (build-report reads CHEM-UNVERIFIED's).
    CHEM-PUBCHEM-MISMATCH also records `measured.crosschecks`: per structure the request URL, whether the answer
    was live or cached, and the SHA-256 of the answer used."""
    checks = []
    for cid in FIG_IDS + CHEM_IDS:
        if cid in CHEM_IDS and not chem:
            checks.append({"id": cid, "status": "not_applicable", "message": "no chemistry figures", "measured": {}})
            continue
        hits = found[cid]
        msgs = [f"{fid}: {m}" if fid else m for fid, m in hits]
        checks.append({"id": cid, "status": "fail" if hits else "pass", "message": "; ".join(msgs),
                       "measured": {"count": len(hits), "figures": sorted({fid for fid, _ in hits if fid})}})
        if cid == "CHEM-PUBCHEM-MISMATCH" and crosschecks is not None:
            checks[-1]["measured"]["crosschecks"] = crosschecks
    return {"schema_version": 1, "target": "figures", "checks": checks}


def ids_of(report, cid):
    return next(c["measured"].get("figures", []) for c in report["checks"] if c["id"] == cid)


def blocking(report):
    return [c for c in report["checks"] if c["status"] == "fail" and c["id"] not in NON_BLOCKING]


def main(project, argv):
    import argparse
    ap = argparse.ArgumentParser(prog="check_figures.py")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv[1:])
    from harness.figures import render
    try:
        cfg = config.load(project)
        with tempfile.TemporaryDirectory() as t:
            out = pathlib.Path(t) / "out"
            try:
                render.render_all(project, cfg, out)
                report = check(project, cfg, out)
            except render.FiguresBlocked:   # the pre-render pass failed: report it, render nothing
                report = check(project, cfg, rendered=False)
    except config.ConfigError as e:
        print(f"ERROR CONFIG: {e}", file=sys.stderr)
        return 2
    except render.RenderError as e:
        print(f"ERROR RENDER: {e}", file=sys.stderr)
        return 1
    if a.json:
        print(json.dumps(report, ensure_ascii=False, indent=1, sort_keys=True))
    else:
        for c in report["checks"]:
            if c["status"] == "fail":
                print(f"FAIL {c['id']}: {c['message']}")
        if not blocking(report):
            print("PASS")
    return 1 if blocking(report) else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    from harness.gate import enforce
    PROJECT = enforce("build", sys.argv)
    sys.exit(main(PROJECT, sys.argv))
