"""`complete rework` (core §2.2 rework row; plan Task 8.3). Unit form checks one chapter; final form the book.

Unit: the checker reports zero `fail` for the chapter and verify_refs reports no blocking check ID.
Final: every unit receipt is valid (state.complete, UNIT-INCOMPLETE) and the book-level checks pass. Translation
projects cannot complete rework until STEP 11 wires TR-TARGET-UNMAPPED.
"""
from harness import hashing
from harness.tools import check_book, config, verify_refs


def _translation(cfg):
    return cfg["brief"]["language"]["translation_required"] is True


def rework(project, active_run, unit, fetch=None):
    cfg = config.load(project)
    probs = []
    if unit is not None:
        entry = next((c for c, _ in cfg.chapters() if c["id"] == unit), None)
        if entry is None:
            return {}, [f"UNIT-UNKNOWN {unit}: not in chapter-plan.json"]
        path = cfg.path("chapters") / entry["file"]
        if not path.is_file():
            return {}, [f"UNIT-FILE-MISSING {unit}: {entry['file']} (named in chapter-plan.json) is not in chapters/"]
        report = check_book.check_chapter(path, cfg, entry)
        probs += [f"{c['id']} {unit}: {c['message']}" for c in report["checks"] if c["status"] == "fail"]
        refs = verify_refs.check_chapter(path, cfg, fetch)
        probs += [f"{r['check_id']} {unit} reference {r['n']}" + (f" ({r['doi']})" if r["doi"] else "")
                  for r in verify_refs.blocking(refs)]
        return {"checker_report_sha256": hashing.hash_bytes(hashing.canonical_json(report)),
                "verify_refs_summary": verify_refs.summary(refs)}, probs
    words = [check_book.words(p.read_text(encoding="utf-8"), cfg) for _, p in cfg.chapters()]
    book, total = check_book.check_book_level(cfg, words)
    probs += [f"{c['id']} book: {c['message']}" for c in book["checks"] if c["status"] == "fail"]
    if _translation(cfg):
        probs.append("TR-TARGET-UNMAPPED: the translation trace check ships in STEP 11 (translation contract §4.3)")
    return {"checker_report_sha256": hashing.hash_bytes(hashing.canonical_json(book)), "total_words": total}, probs
