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
  PDF-HEAD     a running head or foot leaves the text block's width, or two of its lines collide (a wrapped head)
  PDF-BLEED    a full-bleed page (cover, opener, ending) shows the paper colour at an edge
  PDF-DASH     a text line starts with an em or en dash (a bad break)
PDF-HEAD, PDF-BLEED and PDF-DASH read the page layout with PyMuPDF; without it they are not_applicable.
`checkpoints()` saves the cover, first chapter page, first figure page and last page as PNGs (PyMuPDF, optional).
Exit 0 iff every check passes; 1 otherwise or on a refused gate; 2 on a config error.
"""
import json, pathlib, re, sys

REPO = pathlib.Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))
from harness.tools import blocks, build_book, build_html, config  # noqa: E402

IDS = ["PDF-SIZE", "PDF-BLANK", "PDF-META", "PDF-TYPE3", "PDF-EMBED", "PDF-FONTS", "PDF-OUTLINE", "PDF-HEAD", "PDF-BLEED",
       "PDF-DASH"]
LAYOUT_IDS = ("PDF-HEAD", "PDF-BLEED", "PDF-DASH")
LEADING_DASH = re.compile(r"^[—–]\s*\S")
PT_PER_CM = 72 / 2.54
# fonts each engine adds on its own: Word's list bullets (Symbol), its default theme fonts and table fallbacks
ENGINE_FALLBACKS = {"word_com": {"symbol", "symbolmt", "calibri", "cambria", "arial", "arialmt"}, "html": set()}
# OMML carries no font of its own: the reader lays an equation out in the document's math font, and Word's
# default is Cambria Math. A book with `template.math` on therefore prints it wherever it has an equation.
MATH_FONTS = {"cambriamath"}
STYLE_SUFFIX = re.compile(r"[-,](bold|italic|oblique|regular|semibold|light|black|boldmt|italicmt|bolditalic|bolditalicmt|mt|it)+$", re.I)


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


def _squash(s):
    """Whitespace removed and words rejoined where the layout hyphenated them at a line end."""
    return re.sub(r"\s+", "", re.sub(r"[-­]\s*\n", "", s))


def outline_problems(cfg, reader):
    """Each chapter has exactly one bookmark `<n> <title>`, in plan order, pointing at a page that shows the title
    (step9b fix S9b-03: a substring anywhere was not enough)."""
    marks = [(re.sub(r"\s+", " ", t).strip(), p) for t, p in outline_titles(reader)]
    out, last = [], -1
    for _, path in cfg.chapters():
        n, chapter = build_book.chapter_heading(path.read_text(encoding="utf-8"), cfg)
        title = re.sub(r"\s+", " ", blocks.plain(chapter)).strip()
        want = f"{n} {title}"
        hits = [k for k, (t, _) in enumerate(marks) if t == want]
        if len(hits) != 1:
            out.append(f"{len(hits)} bookmarks titled {want!r} (need exactly 1)")
            continue
        k = hits[0]
        if k < last:
            out.append(f"bookmark {want!r} is out of chapter order")
        last = k
        if _squash(blocks.plain(chapter)) not in _squash(reader.pages[marks[k][1]].extract_text()):
            out.append(f"bookmark {want!r} points at page {marks[k][1] + 1}, which does not show the chapter title")
    return out


def _near(a, b, tol=14):
    return all(abs(x - y) <= tol for x, y in zip(a, b))


EDGES = {"top-left": (0, 0), "top-right": (1, 0), "bottom-left": (0, 1), "bottom-right": (1, 1), "top": (0.5, 0),
         "bottom": (0.5, 1), "left": (0, 0.5), "right": (1, 0.5)}


def layout_problems(cfg, pdf):
    """-> {id: [problem]} for LAYOUT_IDS, or None without PyMuPDF.
    A page is full-bleed when any of its four corners and four edge midpoints is not the paper colour; all eight must
    then be off the paper colour (PDF-BLEED). Every other page: lines in the top or bottom margin stay inside the text
    block's width and never overlap one another (PDF-HEAD). No line on any page starts with a dash (PDF-DASH)."""
    try:
        import fitz
    except ImportError:
        return None
    th = cfg["theme"]
    m = {k: v * PT_PER_CM for k, v in th["page"]["margins"].items()}
    paper = tuple(int((th["palette"].get("paper") or "FFFFFF").lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
    found = {i: [] for i in LAYOUT_IDS}
    doc = fitz.open(str(pdf))
    try:
        for n, page in enumerate(doc, 1):
            W, H = page.rect.width, page.rect.height
            pix = page.get_pixmap(dpi=24)
            inset = lambda f, size: max(1, min(size - 2, round(f * (size - 1))))   # 1 px in from the edge
            px = lambda fx, fy: pix.pixel(inset(fx, pix.width), inset(fy, pix.height))[:3]
            leaks = [name for name, (fx, fy) in EDGES.items() if _near(px(fx, fy), paper)]
            bleed = len(leaks) < len(EDGES)   # a text page is paper at every edge; any colour there means full bleed
            if bleed and leaks:
                found["PDF-BLEED"].append(f"page {n}: paper shows at {', '.join(leaks)}")
            lines = {}   # words, not line boxes: Word ends a line box with a space glyph past the margin
            for x0, y0, x1, y1, word, blk, ln, _ in page.get_text("words"):
                lines.setdefault((blk, ln), []).append((x0, y0, x1, y1, word))
            band = []
            for ws in lines.values():
                text = " ".join(w[4] for w in ws)
                x0, y0, x1, y1 = min(w[0] for w in ws), min(w[1] for w in ws), max(w[2] for w in ws), max(w[3] for w in ws)
                if not bleed and (y1 <= m["top"] or y0 >= H - m["bottom"]):
                    band.append((x0, y0, x1, y1, text))
                    if x0 < m["left"] - 1 or x1 > W - m["right"] + 1:
                        found["PDF-HEAD"].append(f"page {n}: {text[:40]!r} runs outside the text block")
                elif LEADING_DASH.match(text):
                    found["PDF-DASH"].append(f"page {n}: {text[:40]!r}")
            for i, a in enumerate(band):
                for c in band[i + 1:]:
                    same_band = (a[1] < m["top"]) == (c[1] < m["top"])
                    if same_band and a[0] < c[2] - 0.5 and c[0] < a[2] - 0.5:   # stacked lines share their x range
                        found["PDF-HEAD"].append(f"page {n}: {a[4][:30]!r} and {c[4][:30]!r} collide (a wrapped head?)")
    finally:
        doc.close()
    return found


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
    if (cfg["template"].get("math") or {}).get("enabled"):
        allowed |= MATH_FONTS
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
        found["PDF-OUTLINE"] = outline_problems(cfg, r)
    lay = layout_problems(cfg, pdf)
    for i in LAYOUT_IDS:
        found[i] = lay[i] if lay is not None else None
    checks = [{"id": i, "status": "not_applicable", "message": "pymupdf missing (optional group evidence)",
               "measured": {"count": 0}} if found[i] is None else
              {"id": i, "status": "fail" if found[i] else "pass", "message": "; ".join(found[i]),
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
