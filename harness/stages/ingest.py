"""`run ingest` (core §2.2 ingest row, §2.4; plan Task 8.4).

Copies brief.source.files into source/ (custody: hashes must equal the brief), writes source-manifest.json, converts
(DOCX natively; other formats through markitdown when it is importable), and writes the normalized Markdown, its
units, its assets and the conversion report. Everything is built in a complete sibling staging tree `.ingest-stage/`,
validated, then swapped into place; a failure at any point leaves the previous outputs as they were.
"""
import json, os, pathlib, shutil
from harness import hashing, schema
from harness.tools import config, convert_docx

STAGE_DIR, OLD_DIR = ".ingest-stage", ".ingest-old"


class IngestError(Exception):
    def __init__(self, code, message, exit_code=1):
        super().__init__(f"{code}: {message}")
        self.code, self.exit_code = code, exit_code


def swap_dirs(project, pairs):
    """For each project-relative path: live item -> .ingest-old/<rel>, staged item -> live. Any failure moves every
    already-moved item back (rollback) and re-raises; on success .ingest-old/ is deleted."""
    project = pathlib.Path(project)
    stage, old = project / STAGE_DIR, project / OLD_DIR
    done = []   # (kind, src, dst) in the order they happened
    try:
        for rel in pairs:
            live, staged, stash = project / rel, stage / rel, old / rel
            if live.exists():
                stash.parent.mkdir(parents=True, exist_ok=True)
                os.replace(live, stash)
                done.append((stash, live))
            live.parent.mkdir(parents=True, exist_ok=True)
            os.replace(staged, live)
            done.append((live, staged))
    except BaseException:
        for src, dst in reversed(done):
            dst.parent.mkdir(parents=True, exist_ok=True)
            os.replace(src, dst)
        raise
    shutil.rmtree(old, ignore_errors=True)
    shutil.rmtree(stage, ignore_errors=True)


def _write_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def _markitdown(path):
    try:
        from markitdown import MarkItDown
    except ImportError:
        raise IngestError("DEPENDENCY", f"{path.name}: non-DOCX input needs the Python package `markitdown`; it is not installed")
    return MarkItDown().convert(str(path)).text_content


def not_measurable_report(fmt, md):
    na = {"source_count": None, "output_count": None, "status": "not_measurable"}
    out = convert_docx.output_counts(md)
    s = {k: dict(na, output_count=out.get(k)) for k in convert_docx.STRUCTURES if k != "callouts"}
    return {"schema_version": 1, "converter": "markitdown", "source_formats": [fmt], "structures": s}


def run(project):
    project = pathlib.Path(project)
    if (project / OLD_DIR).exists():
        raise IngestError("INGEST-RECOVERY", f"{OLD_DIR}/ exists: an earlier ingest crashed while swapping outputs. It holds "
                                             "the previous outputs; restore or delete it by hand, then re-run")
    cfg = config.load(project)
    paths = cfg["template"]["paths"]
    stage = project / STAGE_DIR
    shutil.rmtree(stage, ignore_errors=True)
    try:
        files = cfg["brief"]["source"]["files"]
        manifest = []
        for f in files:
            orig = (project / f["path"]).resolve()
            if not orig.is_relative_to(project.resolve()) or not orig.is_file():
                raise IngestError("SOURCE-MISSING", f"{f['path']} is missing or outside the project")
            if hashing.hash_file(orig) != f["sha256"]:
                raise IngestError("CUSTODY", f"{f['path']}: SHA-256 differs from brief.source.files (the approved source)")
            dest = stage / "source" / orig.name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(orig, dest)
            if hashing.hash_file(dest) != f["sha256"]:
                raise IngestError("CUSTODY", f"{dest.name}: the custody copy does not match the original")
            manifest.append({"path": f"source/{orig.name}", "original": f["path"], "format": f["format"], "sha256": f["sha256"]})
        if len(files) != 1:
            raise IngestError("SOURCE-COUNT", f"one source file is supported, brief lists {len(files)}")
        src = stage / manifest[0]["path"]
        if manifest[0]["format"] == "docx":
            md, assets, report = convert_docx.convert(src, cfg)
        else:
            md, assets = _markitdown(src), {}
            report = not_measurable_report(manifest[0]["format"], md)
        outputs = {"source-manifest.json": {"schema_version": 1, "files": manifest}, "ingest/conversion-report.json": report,
                   "ingest/units.json": convert_docx.units(md)}
        for rel, doc in outputs.items():
            _write_json(stage / rel, doc)
        norm = stage / paths["normalized_source"]
        norm.parent.mkdir(parents=True, exist_ok=True)
        norm.write_text(md, encoding="utf-8", newline="\n")
        adir = stage / paths["assets"]
        adir.mkdir(parents=True, exist_ok=True)
        for name, data in assets.items():
            (adir / name).write_bytes(data)
        for rel, name in (("source-manifest.json", "source-manifest"), ("ingest/conversion-report.json", "conversion-report"),
                          ("ingest/units.json", "units")):
            errs = schema.validate(json.loads((stage / rel).read_text(encoding="utf-8")), schema.load_schema(name))
            if errs:
                raise IngestError("SCHEMA", f"{rel}: {'; '.join(errs)}")
        lost = convert_docx.lost(report)
        if lost:
            raise IngestError("INGEST-LOST", f"structures lost in conversion: {', '.join(lost)} (see the report; previous "
                                             "outputs are unchanged)", exit_code=2)
        swap_dirs(project, ["source", "source-manifest.json", paths["normalized_source"], "ingest/units.json",
                            "ingest/conversion-report.json", paths["assets"]])
    finally:
        shutil.rmtree(stage, ignore_errors=True)
    return {"converter": report["converter"], "source_formats": report["source_formats"]}
