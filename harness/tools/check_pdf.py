"""PDF quality gates (plan Task 9b.3; DEC-045). Emits one checker-report.v1 document, target `pdf`.

Usage: python harness/tools/check_pdf.py --project projects/<slug> [--pdf FILE] [--json]
Checks build/<basename>.pdf (or FILE) against the book's own config, for either PDF engine:
  PDF-SIZE     every page is the preset page size (within 1 pt)
  PDF-BLANK    a page has no text and no image
  PDF-META     the title or author metadata is not the brief's
  PDF-TYPE3    a Type 3 (bitmap-like) font is used
  PDF-EMBED    a font is not embedded
  PDF-FONTS    a font family outside the theme fonts, its font files and the engine's own fallbacks
  PDF-OUTLINE  bookmarks are `headings` but a chapter title is missing from them
`checkpoints()` saves the cover, first chapter page, first figure page and last page as PNGs (PyMuPDF, optional).
Exit 0 iff every check passes; 1 otherwise or on a refused gate; 2 on a config error.
"""
import json, pathlib, re, sys

REPO = pathlib.Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))
from harness.tools import blocks, build_book, build_html, config  # noqa: E402

IDS = ["PDF-SIZE", "PDF-BLANK", "PDF-META", "PDF-TYPE3", "PDF-EMBED", "PDF-FONTS", "PDF-OUTLINE"]
PT_PER_CM = 72 / 2.54
# fonts each engine adds on its own: Word's list bullets (Symbol), its default theme fonts and table fallbacks
ENGINE_FALLBACKS = {"word_com": {"symbol", "symbolmt", "calibri", "cambria", "arial", "arialmt"}, "html": set()}
STYLE_SUFFIX = re.compile(r"[-,](bold|italic|oblique|regular|semibold|light|black|boldmt|italicmt|bolditalic|bolditalicmt|mt)+$", re.I)


def family(base_font):
    """'ABCDEF+SitkaHeading-Bold' -> 'sitkaheading'; 'Sitka Heading' -> 'sitkaheading'."""
    name = str(base_font).lstrip("/").split("+", 1)[-1]
    name = STYLE_SUFFIX.sub("", name)
    return re.sub(r"[\s_-]", "", name).lower()


def _fonts(resources, seen):
    """(font dict) for every font in a resources dict, including those of form XObjects."""
    if not resources:
        return
    res = resources.get_object()
    for f in (res.get("/Font") or {}).values():
        f = f.get_object()
        if id(f) not in seen:
            seen.add(id(f))
            yield f
    for x in (res.get("/XObject") or {}).values():
        x = x.get_object()
        if x.get("/Subtype") == "/Form" and "/Resources" in x:
            yield from _fonts(x["/Resources"], seen)


def _embedded(font):
    desc = font.get("/FontDescriptor")
    if font.get("/Subtype") == "/Type0":
        desc = font["/DescendantFonts"][0].get_object().get("/FontDescriptor")
    desc = desc.get_object() if desc is not None else {}
    return any(k in desc for k in ("/FontFile", "/FontFile2", "/FontFile3"))


def outline_titles(reader):
    out = []

    def walk(items):
        for it in items:
            walk(it) if isinstance(it, list) else out.append((it.title, reader.get_destination_page_number(it)))
    walk(reader.outline)
    return out


def check(cfg, pdf):
    from pypdf import PdfReader
    bk = build_book.Book(cfg)
    r = PdfReader(str(pdf))
    found = {i: [] for i in IDS}
    pg = bk.preset["page"]
    want = (pg["width_cm"] * PT_PER_CM, pg["height_cm"] * PT_PER_CM)
    allowed = {family(bk.fonts[k]) for k in ("serif", "serif_heading", "sans", "complex_script", "complex_script_heading")
               if bk.fonts.get(k)}
    allowed |= {family(f) for f in (cfg["theme"].get("font_files") or {})}
    allowed |= ENGINE_FALLBACKS[build_html.engine(cfg)]
    seen, bad_fonts = set(), {}
    for n, page in enumerate(r.pages, 1):
        w, h = float(page.mediabox.width), float(page.mediabox.height)
        if abs(w - want[0]) > 1 or abs(h - want[1]) > 1:
            found["PDF-SIZE"].append(f"page {n}: {w:.1f} x {h:.1f} pt, not {want[0]:.1f} x {want[1]:.1f}")
        if not page.extract_text().strip() and not page.images:
            found["PDF-BLANK"].append(f"page {n}")   # ponytail: a vector-only page counts as blank; none is placed today
        for f in _fonts(page.get("/Resources"), seen):
            name = str(f.get("/BaseFont", f.get("/Name", "?")))
            if f.get("/Subtype") == "/Type3":
                found["PDF-TYPE3"].append(f"page {n}: {name}")
                continue
            if not _embedded(f):
                found["PDF-EMBED"].append(f"page {n}: {name}")
            if family(name) not in allowed:
                bad_fonts.setdefault(name.lstrip("/").split("+", 1)[-1], n)
    found["PDF-FONTS"] = [f"{name} (first on page {n})" for name, n in sorted(bad_fonts.items())]
    meta = r.metadata or {}
    title = f"{bk.title}: {bk.subtitle}" if bk.subtitle else bk.title
    for key, value in (("/Title", title), ("/Author", bk.credits)):
        if (meta.get(key) or "") != value:
            found["PDF-META"].append(f"{key} is {meta.get(key)!r}, not {value!r}")
    if cfg["theme"]["build"]["pdf"]["bookmarks"] == "headings":
        titles = [re.sub(r"\s+", " ", t) for t, _ in outline_titles(r)]
        for _, path in cfg.chapters():
            _, chapter = build_book.chapter_heading(path.read_text(encoding="utf-8"), cfg)
            if not any(blocks.plain(chapter) in t for t in titles):
                found["PDF-OUTLINE"].append(f"no bookmark for {blocks.plain(chapter)!r}")
    checks = [{"id": i, "status": "fail" if found[i] else "pass", "message": "; ".join(found[i]),
               "measured": {"count": len(found[i])}} for i in IDS]
    checks[0]["measured"]["pages"] = len(r.pages)
    return {"schema_version": 1, "target": "pdf", "checks": checks}


def failures(report):
    return [c for c in report["checks"] if c["status"] == "fail"]


def checkpoints(cfg, pdf, out_dir, dpi=100):
    """-> {name: project-relative PNG path} for cover, first-chapter, first-figure, last; {"skipped": why} without
    PyMuPDF (optional group `evidence`)."""
    try:
        import fitz
    except ImportError:
        return {"skipped": "pymupdf missing (optional group evidence)"}
    from pypdf import PdfReader
    marks = outline_titles(PdfReader(str(pdf)))
    _, first = build_book.chapter_heading(cfg.chapters()[0][1].read_text(encoding="utf-8"), cfg)
    chapter = next((p for t, p in marks if blocks.plain(first) in t), None)
    doc = fitz.open(str(pdf))
    try:
        start = chapter or 0
        figure = next((i for i in range(start, doc.page_count) if doc[i].get_images()), None)
        pages = {"cover": 0, "first-chapter": chapter, "first-figure": figure, "last": doc.page_count - 1}
        out_dir.mkdir(parents=True, exist_ok=True)
        for old in out_dir.glob("*.png"):
            old.unlink()
        done = {}
        for name, i in pages.items():
            if i is None:
                continue
            path = out_dir / f"{name}.png"
            doc[i].get_pixmap(dpi=dpi).save(str(path))
            done[name] = path.relative_to(cfg["project"]).as_posix() if path.is_relative_to(cfg["project"]) else str(path)
        return done
    finally:
        doc.close()


def main(project, argv):
    import argparse
    ap = argparse.ArgumentParser(prog="check_pdf.py")
    ap.add_argument("--pdf")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv[1:])
    try:
        cfg = config.load(project)
        pdf = pathlib.Path(a.pdf) if a.pdf else cfg["project"] / "build" / f"{cfg['theme']['output']['basename']}.pdf"
        if not pdf.is_file():
            raise FileNotFoundError(f"{pdf} missing (run build first)")
        report = check(cfg, pdf)
    except (config.ConfigError, KeyError, FileNotFoundError) as e:
        print(f"ERROR CONFIG: {e}", file=sys.stderr)
        return 2
    if a.json:
        print(json.dumps(report, ensure_ascii=False, indent=1))
    else:
        for c in report["checks"]:
            print(f"{c['status']:4} {c['id']}" + (f": {c['message']}" if c["message"] else ""))
    return 1 if failures(report) else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    from harness.gate import enforce
    PROJECT = enforce("build", sys.argv)
    sys.exit(main(PROJECT, sys.argv))
