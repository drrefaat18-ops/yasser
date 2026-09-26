"""Canonical input/output file sets per stage (core §2.2, translation contract §2). Every receipt's file maps come from here.

Paths are project-relative POSIX strings. Harness files that a stage reads (intake) are given relative to the project
as `../../harness/...`, so they hash like any other input. Fixed names are always listed (a missing required output
fails `complete`); globs and optional files list only what exists.
"""
import json, pathlib

HARNESS = "../../harness"
UNIT_STAGES = {"rework", "translate"}


def _json(project, rel):
    p = project / rel
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def _glob(project, rel_dir, pattern="*"):
    d = project / rel_dir
    return sorted(p.relative_to(project).as_posix() for p in d.rglob(pattern) if p.is_file()) if d.is_dir() else []


def _optional(project, *rels):
    return [r for r in rels if (project / r).exists()]


def _translation(project):
    brief = _json(project, "brief.json") or {}
    return (brief.get("language", {}).get("translation_required") is True
            and brief.get("goal", {}).get("mode") == "evaluate_and_rework")


def _paths(project):
    return (_json(project, "template.json") or {}).get("paths", {})


def _plan(project):
    return _json(project, "design/chapter-plan.json") or {"chapters": []}


def _chapter_file(project, chapter_id):
    for c in _plan(project)["chapters"]:
        if c["id"] == chapter_id:
            return f"{_paths(project)['chapters']}/{c['file']}"
    raise KeyError(chapter_id)


def _chapter_files(project):
    return [f"{_paths(project)['chapters']}/{c['file']}" for c in _plan(project)["chapters"]]


def _book_files(project):
    """Rework-owned files beyond the chapters: front matter, glossary, errata ledger (each if configured)."""
    p = _paths(project)
    return [f"{p['chapters']}/{p[k]}" for k in ("front_matter", "glossary", "errata") if p.get(k)]


INTAKE_OUT = ["brief.json", "rubric.json", "template.json", "theme.json"]
EVAL_OUT = [f"evaluation/{f}" for f in ("findings.json", "scorecard.json", "report.md", "codex-review.md", "fixes.md")]
DESIGN_OUT = ["design/design.md", "design/chapter-plan.json", "design/errata-seed.md"]
TRANSLATE_STAGE_OUT = ["translation/check-report.json", "translation/codex-review.md", "translation/fixes.md",
                       "trace/translation-map.json", "terms/translate-proposals.json"]
AUDIT_OUT = [f"audit/{f}" for f in ("findings.json", "scorecard.json", "codex-audit.md", "fixes.md")]


def units(project, stage_id):
    project = pathlib.Path(project)
    if stage_id == "rework":
        return [c["id"] for c in _plan(project)["chapters"]]
    if stage_id == "translate":
        return sorted({ref for c in _plan(project)["chapters"] for ref in c["source_refs"]})
    return []


def files(project, stage_id, unit=None):
    """-> (inputs, outputs) for the stage, or for one unit of a unit-based stage."""
    project = pathlib.Path(project)
    p = _paths(project)
    agents = _glob(project, "agents", "*.json")
    tr = _translation(project)
    normalized = p.get("normalized_source", "ingest/normalized.md")

    if stage_id == "new":
        return [], _glob(project, ".", ".keep")
    if stage_id == "intake":
        brief, theme = _json(project, "brief.json") or {}, _json(project, "theme.json") or {}
        tag = brief.get("language", {}).get("output", "en").split("-")[0].lower()
        ins = [f"{HARNESS}/rubric_core.json", f"{HARNESS}/locale/{tag}.json"]
        if theme.get("preset"):
            ins.append(f"{HARNESS}/presets/{theme['preset']}.json")
        return ins, INTAKE_OUT + agents
    if stage_id == "ingest":
        brief = _json(project, "brief.json") or {}
        ins = [f["path"] for f in brief.get("source", {}).get("files", [])] + ["template.json"]
        outs = (_glob(project, "source") + ["source-manifest.json", normalized, "ingest/units.json",
                                             "ingest/conversion-report.json"] + _glob(project, p.get("assets", "ingest/assets")))
        return ins, outs
    if stage_id == "evaluate":
        return ["brief.json", "rubric.json", *agents, normalized, "ingest/conversion-report.json"], list(EVAL_OUT)
    if stage_id == "design":
        return EVAL_OUT + ["brief.json", "template.json", "theme.json"], DESIGN_OUT + (["termbase.json"] if tr else [])
    if stage_id == "translate":
        common = DESIGN_OUT + ["termbase.json", normalized, "ingest/units.json", "brief.json"]
        if unit is not None:
            return common, [f"translation/{unit}.md"]
        return common, [f"translation/{u}.md" for u in units(project, "translate")] + TRANSLATE_STAGE_OUT
    if stage_id == "rework":
        common = DESIGN_OUT + INTAKE_OUT + agents + [normalized] + _optional(project, "references-manual.json")
        if tr:
            common += (_glob(project, "translation", "*.md") + ["trace/translation-map.json", "termbase.json"]
                       + _optional(project, "termbase-additions.json"))
        if unit is not None:   # a unit is checked against the glossary too (GLOSS-MISSING), so it is an input
            gl = [f"{p['chapters']}/{p['glossary']}"] if p.get("glossary") else []
            return common + gl, [_chapter_file(project, unit)]
        outs = _chapter_files(project) + _book_files(project) + _glob(project, f"{p['figures']}/src")
        outs += _optional(project, f"{p['figures']}/figures.json")   # required once the figure system ships (STEP 9)
        if tr:
            outs += ["trace/source-target-map.json", "terms/rework-proposals.json"]
        return common, outs
    if stage_id == "build":
        theme = _json(project, "theme.json") or {}
        base = theme.get("output", {}).get("basename", "book")
        # every file under the asset roots and the figures dir is read (images, legacy PNG mirrors, cover); figures.json
        # joins when the figure system ships (STEP 9)
        assets = sorted({f for root in p.get("allowed_asset_roots", []) + [p["figures"]] for f in _glob(project, root)}
                        - {f for f in _glob(project, f"{p['figures']}/out")})
        ins = (_chapter_files(project) + _book_files(project) + ["brief.json", "template.json", "theme.json",
               "design/chapter-plan.json"] + assets)
        outs = _glob(project, f"{p['figures']}/out") + [f"build/{base}.{ext}" for ext in ("md", "docx", "pdf")]
        return ins, outs + ["build/build-report.json"]
    if stage_id == "audit":
        _, build_outs = files(project, "build")
        ins = (build_outs + _chapter_files(project) + _book_files(project)
               + ["brief.json", "rubric.json", "evaluation/scorecard.json", normalized])
        if tr:
            ins += (["ingest/units.json"] + _glob(project, "translation", "*.md") + ["translation/check-report.json",
                    "trace/source-target-map.json", "termbase.json"] + _optional(project, "termbase-additions.json"))
        return ins, list(AUDIT_OUT)
    raise KeyError(stage_id)
