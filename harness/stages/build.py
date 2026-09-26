"""`run build` (core §2.2 build row; plan Task 8.2): figures, assemble, DOCX, PDF, build-report.json.

Figures: until the figure system ships (STEP 9) the builder reads the existing PNG mirrors and the receipt records
`figures: legacy`. A failing step raises; the runner then writes a `failed` receipt naming it.
"""
import json
from harness import preflight
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
    report = {"schema_version": 1, "backend": cfg["theme"]["build"]["backend"], "figures": "legacy",
              "docx": {k: facts["docx"][k] for k in ("parts", "images", "toc_field")},
              "pdf": {"pages": facts["pdf"]["pages"], "bookmarks": len(facts["pdf"]["bookmarks"])}}
    (project / "build" / "build-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=1, sort_keys=True) + "\n",
                                                        encoding="utf-8", newline="\n")
    if not report["docx"]["toc_field"]:
        raise BuildStepFailed("report: the DOCX has no TOC field")
    return {"backend": report["backend"], "figures": "legacy", "page_count": pages,
            "bookmarks_count": report["pdf"]["bookmarks"]}
