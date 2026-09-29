"""`run build` (core §2.2 build row; plan Tasks 8.2, 9b.2-9b.3): figures, assemble, DOCX, PDF, PDF gates, build-report.json.

Figures (core §7): with a manifest, the checker's pre-render pass runs, every figure is rendered into
<paths.figures>/out/ and the full figure check runs before anything is assembled; a blocking check ID fails the build. Without a manifest, only a book whose rework
was history-imported (plan N2) may build, reading its existing PNG mirrors (`figures: legacy`); any other book
fails with FIG-MANIFEST. A failing step raises; the runner then writes a `failed` receipt naming it.
"""
import json, os, pathlib
from harness import figures, preflight, state
from harness.figures import check_figures, render
from harness.tools import assemble, build_book, build_html, capture_golden, check_pdf, config


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
    cfg = config.load(project)
    missing = [c for c in preflight.run(["build"], cfg["theme"]["preset"]) if c["required"] and not c["ok"]]
    if missing:
        raise BuildStepFailed("preflight: " + "; ".join(f"{c['name']}: {c['detail']}" for c in missing))
    _contained(project, [project / "build", figures.out_dir(cfg), cfg.path("figures") / ".cache"])
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
    engine = build_html.engine(cfg)
    if engine == "html":   # DEC-043: Word writes the DOCX, headless Edge prints the PDF from the same blocks
        _step("docx (word_com)", lambda: build_book.word_finish(cfg, docx, export_pdf=False))
        pdf, pages = _step("pdf (html)", lambda: build_html.build_pdf(cfg, docx.with_suffix(".pdf")))
    else:
        pdf, pages = _step("pdf (word_com)", lambda: build_book.word_finish(cfg, docx))
    pdf_report = _step("pdf checks", lambda: check_pdf.check(cfg, pdf))
    shots = _step("checkpoints", lambda: check_pdf.checkpoints(cfg, pdf, project / "build" / "checkpoints"))
    facts = _step("report", lambda: {"docx": capture_golden.docx_facts(docx), "pdf": capture_golden.pdf_facts(pdf)})
    report = {"schema_version": 1, "backend": cfg["theme"]["build"]["backend"], "pdf_engine": engine, "figures": fig_mode,
              "docx": {k: facts["docx"][k] for k in ("parts", "images", "toc_field")},
              "pdf": {"pages": facts["pdf"]["pages"], "bookmarks": len(facts["pdf"]["bookmarks"])}}
    report.update({"pdf_checks": pdf_report["checks"], "checkpoints": shots})
    if fig_report is not None:
        report.update(fig_report)
    (project / "build" / "build-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=1, sort_keys=True) + "\n",
                                                        encoding="utf-8", newline="\n")
    if not report["docx"]["toc_field"]:
        raise BuildStepFailed("report: the DOCX has no TOC field")
    bad = check_pdf.failures(pdf_report)
    if bad:
        raise BuildStepFailed("pdf checks: " + "; ".join(f"{c['id']}: {c['message'][:300]}" for c in bad))
    return {"backend": report["backend"], "pdf_engine": engine, "figures": fig_mode, "page_count": pages,
            "bookmarks_count": report["pdf"]["bookmarks"]}


def _contained(project, dirs):
    """Each folder the build writes must resolve to itself inside the project: a symlink or junction anywhere on its
    path would carry the writes (and the clearing of <figures>/out) outside it (step9 fix S9-01)."""
    root = pathlib.Path(os.path.realpath(project))
    for d in dirs:
        rel = os.path.relpath(os.path.abspath(d), os.path.abspath(project))
        if os.path.normcase(os.path.realpath(d)) != os.path.normcase(str(root / rel)):
            raise BuildStepFailed(f"output: {pathlib.Path(rel).as_posix()} resolves to {os.path.realpath(d)}, "
                                  "not inside the project (a link or junction)")


def _figures(project, cfg):
    """-> (mode, build-report additions). Renders, then checks; raises BuildStepFailed on a blocking check ID."""
    if not figures.manifest_path(cfg).is_file():   # a malformed manifest is FIG-MANIFEST in the pre-render check
        rework = state.load(project)["receipts"].get("rework", {})
        if rework.get("imported"):
            return "legacy", None
        raise BuildStepFailed(f"figures: FIG-MANIFEST: {figures.manifest_path(cfg).relative_to(project).as_posix()} "
                              "missing (only a history-imported book may build without one)")
    try:   # render_all runs the checker's pre-render pass first; a blocking ID stops before any source is read
        results = render.render_all(project, cfg)
    except render.FiguresBlocked as e:
        raise BuildStepFailed(f"figures: {e}") from e
    except Exception as e:
        raise BuildStepFailed(f"figures (render): {type(e).__name__}: {e}") from e
    report = check_figures.check(project, cfg)
    bad = check_figures.blocking(report)
    if bad:
        raise BuildStepFailed("figures: " + "; ".join(f"{c['id']}: {c['message']}" for c in bad))
    man = figures.load(cfg)
    return "manifest", {"figure_checks": report["checks"], "figure_renders": results,
                        "figure_versions": render.versions(man["figures"]),
                        "chem_unverified": check_figures.ids_of(report, "CHEM-UNVERIFIED")}
