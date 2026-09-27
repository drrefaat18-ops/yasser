"""`run build` (core §2.2 build row; plan Task 8.2): figures, assemble, DOCX, PDF, build-report.json.

Figures (core §7): with a manifest, every figure is rendered into <paths.figures>/out/ and the figure checker runs
before anything is assembled; a blocking check ID fails the build. Without a manifest, only a book whose rework
was history-imported (plan N2) may build, reading its existing PNG mirrors (`figures: legacy`); any other book
fails with FIG-MANIFEST. A failing step raises; the runner then writes a `failed` receipt naming it.
"""
import json
from harness import figures, preflight, state
from harness.figures import check_figures, render
from harness.tools import assemble, build_book, capture_golden, config


class BuildStepFailed(Exception):
    exit_code = 1

    def __init__(self, message):
        super().__init__(f"BUILD: {message}")


def _step(name, fn):
    try:
        return fn()
    except Exception as e:
        raise BuildStepFailed(f"{name}: {type(e).__name__}: {e}") from e


def run(project):
    missing = [c for c in preflight.run(["build"]) if c["required"] and not c["ok"]]
    if missing:
        raise BuildStepFailed("preflight: " + "; ".join(f"{c['name']}: {c['detail']}" for c in missing))
    cfg = config.load(project)
    fig_mode, fig_report = _figures(project, cfg)

    def do_assemble():
        book, probs = assemble.assemble(cfg)
        if probs:
            raise build_book.BuildError("; ".join(probs))
        out = assemble.output_path(cfg)
        out.parent.mkdir(exist_ok=True)
        out.write_text(book, encoding="utf-8", newline="\n")
    _step("assemble", do_assemble)
    docx = _step("docx", lambda: build_book.build(cfg))
    pdf, pages = _step("pdf (word_com)", lambda: build_book.word_finish(cfg, docx))
    facts = _step("report", lambda: {"docx": capture_golden.docx_facts(docx), "pdf": capture_golden.pdf_facts(pdf)})
    report = {"schema_version": 1, "backend": cfg["theme"]["build"]["backend"], "figures": fig_mode,
              "docx": {k: facts["docx"][k] for k in ("parts", "images", "toc_field")},
              "pdf": {"pages": facts["pdf"]["pages"], "bookmarks": len(facts["pdf"]["bookmarks"])}}
    if fig_report is not None:
        report.update(fig_report)
    (project / "build" / "build-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=1, sort_keys=True) + "\n",
                                                        encoding="utf-8", newline="\n")
    if not report["docx"]["toc_field"]:
        raise BuildStepFailed("report: the DOCX has no TOC field")
    return {"backend": report["backend"], "figures": fig_mode, "page_count": pages,
            "bookmarks_count": report["pdf"]["bookmarks"]}


def _figures(project, cfg):
    """-> (mode, build-report additions). Renders, then checks; raises BuildStepFailed on a blocking check ID."""
    if figures.load(cfg) is None:
        rework = state.load(project)["receipts"].get("rework", {})
        if rework.get("imported"):
            return "legacy", None
        raise BuildStepFailed(f"figures: FIG-MANIFEST: {figures.manifest_path(cfg).relative_to(project).as_posix()} "
                              "missing (only a history-imported book may build without one)")
    results = _step("figures (render)", lambda: render.render_all(project, cfg))
    report = check_figures.check(project, cfg)
    bad = check_figures.blocking(report)
    if bad:
        raise BuildStepFailed("figures: " + "; ".join(f"{c['id']}: {c['message']}" for c in bad))
    man = figures.load(cfg)
    return "manifest", {"figure_checks": report["checks"], "figure_renders": results,
                        "figure_versions": render.versions(man["figures"]),
                        "chem_unverified": check_figures.ids_of(report, "CHEM-UNVERIFIED")}
