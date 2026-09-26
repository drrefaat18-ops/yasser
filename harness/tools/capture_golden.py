"""Golden regression capture (core §9.1; plan N1, N5, N6, N8). Read-only: it writes only --out.

Usage: python harness/tools/capture_golden.py --project projects/<slug> --out FILE [--layout FILE | --docx-from build|deliverables] [--no-refs]
Without --layout (harness mode, STEP 8) the layout comes from project config and the checks from harness/tools/check_book.py.
Exit 0 ok; 1 bad project path or missing dependency; 2 on any verify_refs ERROR (network) or unclassified message.
"""
import argparse, contextlib, importlib.util, io, json, os, pathlib, re, subprocess, sys, zipfile

REPO = pathlib.Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))
from harness import hashing  # noqa: E402

SLUG = re.compile(r"^[a-z0-9][a-z0-9-]{1,62}$")


class Unclassified(Exception):
    """A legacy message or verify_refs line that the N6 table does not know."""


class LayoutError(Exception):
    """A layout path that escapes the project (core §1.1, plan N1)."""


LAYOUT_PATH_KEYS = ["chapters_dir", "front_matter", "glossary", "errata", "legacy_tools"]


def layout_problems(project_dir, layout):
    """Every layout path must be relative and resolve inside the project; the chapter glob is one file pattern."""
    root = pathlib.Path(project_dir).resolve()
    found = [(k, layout.get(k)) for k in LAYOUT_PATH_KEYS]
    found += [("images", v) for v in layout.get("images", [])]
    found += [(f"deliverables.{k}", v) for k, v in layout.get("deliverables", {}).items()]
    probs = []
    for key, value in found:
        if not isinstance(value, str) or not value:
            probs.append(f"{key}: missing or not a string")
            continue
        path = pathlib.PurePosixPath(value.replace("\\", "/"))
        if path.is_absolute() or re.match(r"^[A-Za-z]:", value) or ".." in path.parts:
            probs.append(f"{key}: {value!r} must be a relative path inside the project")
        elif not (root / path).resolve().is_relative_to(root):
            probs.append(f"{key}: {value!r} resolves outside the project")
    glob = layout.get("chapter_glob")
    if not isinstance(glob, str) or not glob or re.search(r"[/\\]|\.\.", glob):
        probs.append(f"chapter_glob: {glob!r} must be a single file-name pattern")
    return probs


class NetworkError(Exception):
    """verify_refs printed ERROR: a flaky result is never frozen (core §9.1)."""


class GateRefused(Exception):
    """A gated legacy tool refused to run (Rule 7): the project's approvals or receipts are not valid."""


# N6: legacy message -> check ID. Line numbers: rework/tools/check_book.py at d557120.
CLASSIFY = {
    "check_template": [(r"^template: missing '# Chapter", "TPL-H1"),                 # 104
                       (r"^template: missing section", "TPL-SECTION-MISSING"),       # 109
                       (r"^template: required sections out of order", "TPL-SECTION-ORDER"),  # 113
                       (r"^template: missing box", "TPL-CALLOUT-MISSING")],          # 116
    "check_lenses": [(r"^lens missing: ", "PERSP-MISSING"),                          # 125
                     (r"^lens imbalance: ", "PERSP-BALANCE")],                       # 132
    "check_los": [(r"^LOs: \d+ objectives", "LO-COUNT"),                             # 143
                  (r"^LOs: avoid ", "LO-VERB")],                                     # 146
    "check_mcqs": [(r"^Q\d+: option E present", "MCQ-EXTRA-OPTION"),                 # 164
                   (r"^Q\d+: options must be", "MCQ-OPTIONS"),                       # 166
                   (r"^Q\d+: missing \[LOn\] tag", "MCQ-LO-TAG"),                    # 170
                   (r"^MCQ count ", "MCQ-COUNT"),                                    # 172
                   (r"^missing \*\*Case Question", "MCQ-CASE"),                      # 174
                   (r"^Q\d+: tag LO\d+ not among", "MCQ-LO-UNKNOWN"),                # 178
                   (r"^LO\d+ has no question", "LO-UNASSESSED"),                     # 181
                   (r"^Q\d+: empty rationale", "KEY-RATIONALE"),                     # 186
                   (r"^Q\d+: no answer key", "KEY-MISSING"),                         # 189
                   (r"^key imbalance: ", "KEY-BALANCE"),                             # 194
                   (r"^key run: ", "KEY-RUN")],                                      # 197
    "check_citations": [(r"^missing reference ", "CIT-MISSING"),                     # 220
                        (r"^uncited reference ", "CIT-UNCITED")],                    # 221
    "check_sentences": [(r"^sentences: mean length", "READ-MEAN"),                   # 94
                        (r"^sentences: \S+ over ", "READ-LONG"),                     # 97
                        (r"^sentences: no prose found$", "READ-NOPROSE")],           # 88
    "check_banned": [(r"^banned term: ", "BANNED-TERM")],                            # 253
    "check_budget": [(r"^budget: ", "BUDGET-CHAPTER")],                              # 61
    "check_glossary": [(r"^glossary missing: ", "GLOSS-MISSING")],                   # 249
    "check_all": [(r"^book: \d+ chapters", "BOOK-CHAPTER-COUNT"),                    # 274
                  (r"^book: missing 00-front", "BOOK-FRONT-MISSING"),                # 282
                  (r"^book: total ", "BUDGET-TOTAL"),                                # 284
                  (r"^book: errata ledger", "ERRATA-OPEN"),                          # 287
                  (r"^book: glossary has", "GLOSS-MIN")],                            # 289
}
ALL_LEGACY_IDS = sorted({i for rows in CLASSIFY.values() for _, i in rows})
CHAPTER_FNS = ["check_template", "check_lenses", "check_los", "check_mcqs", "check_citations",
               "check_sentences", "check_banned", "check_budget", "check_glossary"]  # check_chapter order

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
CP = "http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
DCTERMS = "http://purl.org/dc/terms/"
EP = "http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"
W14 = "http://schemas.microsoft.com/office/word/2010/wordml"
W15 = "http://schemas.microsoft.com/office/word/2012/wordml"
WP14 = "http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing"
W16CID = "http://schemas.microsoft.com/office/word/2016/wordml/cid"
# Per-save random IDs, found by diffing two builds of identical sources (STEP 5 ruling on N5)
VOLATILE_ATTRS = {f"{{{W14}}}paraId", f"{{{W14}}}textId", f"{{{WP14}}}anchorId", f"{{{WP14}}}editId",
                  f"{{{W16CID}}}durableId", f"{{{W}}}fontKey"}
VOLATILE_TAGS = {f"{{{W}}}rsids", f"{{{W}}}rsid", f"{{{W}}}lastRenderedPageBreak", f"{{{W}}}proofErr",
                 f"{{{W14}}}docId", f"{{{W15}}}docId", f"{{{W}}}zoom"}
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL = "http://schemas.openxmlformats.org/package/2006/relationships"
VOLATILE_CORE = {f"{{{CP}}}lastModifiedBy", f"{{{CP}}}revision", f"{{{DCTERMS}}}created", f"{{{DCTERMS}}}modified"}
VOLATILE_APP = {f"{{{EP}}}TotalTime", f"{{{EP}}}Application", f"{{{EP}}}AppVersion"}
VOLATILE_EXCLUDED = [  # N5 / core §9.1: every field the semantic hashes and facts leave out, with its reason
    {"field": "docx: w:rsid* attributes, w:rsids and w:rsid elements", "reason": "save-session metadata"},
    {"field": "docx: w14:paraId, w14:textId, wp14:anchorId, wp14:editId, w16cid:durableId attributes; w14:docId, w15:docId",
     "reason": "random IDs Word writes on every save"},
    {"field": "docx: w:zoom in settings.xml", "reason": "view zoom of the last Word window, not content"},
    {"field": "docx: w:fontKey, and the bytes of embedded fonts (word/fonts/*)",
     "reason": "Word re-obfuscates and rewrites embedded fonts on every save (random key, head checksum, timestamps);"
               " each font part is hashed by its fontTable name, embed slot and byte length"},
    {"field": "docx: w:lastRenderedPageBreak, w:proofErr", "reason": "layout and proofing state"},
    {"field": "docx: result runs of the TOC field (between fldChar separate and end)",
     "reason": "page numbers depend on Word pagination; the field instruction is kept"},
    {"field": "docx: bookmarks named _Toc*", "reason": "Word regenerates them on every TOC update"},
    {"field": "docProps/core.xml created, modified, lastModifiedBy, revision", "reason": "save metadata"},
    {"field": "docProps/app.xml TotalTime, Application, AppVersion", "reason": "save metadata"},
    {"field": "pdf: CreationDate, ModDate, document ID", "reason": "export metadata; only page count and bookmarks are captured"},
]
# legacy verify_refs.py:53, but "[ \t]" after the colon so the §9.5 leak scan sees no drive-letter pattern
DOI_REF = re.compile(r"DOI:[ \t]*(10\.\S+?)\.?\s*$|doi\.org/(10\.\S+?)\.?\s*$")


def _w(tag):
    return f"{{{W}}}{tag}"


def classify(fn, msg):
    for rx, cid in CLASSIFY.get(fn, []):
        if re.search(rx, msg):
            return cid
    raise Unclassified(f"{fn}: {msg}")


def dumps(obj):
    return json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=True) + "\n"


def _rel(path, root):
    return pathlib.Path(os.path.relpath(path, root)).as_posix()


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_legacy_checker(project_dir, layout):
    mod = _load(pathlib.Path(project_dir) / layout["legacy_tools"] / "check_book.py", "legacy_check_book")
    mod.ROOT = pathlib.Path(project_dir) / layout["chapters_dir"]
    return mod


def chapter_id(path):
    return re.match(r"[^-.]+", pathlib.Path(path).name).group(0)


def chapter_paths(project_dir, layout):
    return sorted((pathlib.Path(project_dir) / layout["chapters_dir"]).glob(layout["chapter_glob"]))


def _sentence_lengths(mod, text):
    sents = []
    for line in mod.clean_prose_lines(text):
        sents += [s for s in re.split(r"(?<=[.!?])\s+", line) if mod.WORD.search(s)]
    return [len(mod.WORD.findall(s)) for s in sents]


def _measured(mod, text, budget, labels):
    lens = _sentence_lengths(mod, text)
    sa = mod.sections(text).get(labels["assessment"], "")
    qs = {int(m.group(1)) for m in re.finditer(r"^\*\*Q(\d+)\.\*\*", sa, re.M)}
    ans = mod.sections(text).get(labels["answers"], "")
    keys = [m.group(1) for m in re.finditer(r"^\*\*Q\d+\. ([A-D])\*\*", ans, re.M)]
    return {
        "BUDGET-CHAPTER": {"words": mod.words(text), "budget": budget},
        "READ-MEAN": {"mean_sentence": round(sum(lens) / len(lens), 3)} if lens else {},
        "READ-LONG": {"long_share": round(sum(1 for n in lens if n > mod.LONG) / len(lens), 4)} if lens else {},
        "LO-COUNT": {"lo_count": len(mod.lo_ids(text))},
        "MCQ-COUNT": {"mcq_count": len(qs)},
        "KEY-BALANCE": {"key_counts": {k: keys.count(k) for k in "ABCD"}},
    }


def _entries(fn, target, msgs, measured):
    by_id = {}
    for m in msgs:
        by_id.setdefault(classify(fn, m), []).append(m)
    out = []
    for _, cid in CLASSIFY[fn]:
        e = {"id": cid, "target": target, "status": "fail" if cid in by_id else "pass", "measured": measured.get(cid, {})}
        if cid in by_id:
            e["message"] = "; ".join(by_id[cid])
        out.append(e)
    return out


def checks_for_chapter(mod, path, glossary, labels):
    text = pathlib.Path(path).read_text(encoding="utf-8")
    m = re.search(r"ch(\d+)", pathlib.Path(path).name)          # same budget rule as legacy check_chapter
    budget = mod.BUDGETS.get(int(m.group(1)), 0) if m else 0
    msgs = {fn: (getattr(mod, fn)(text, budget) if fn == "check_budget" else
                 getattr(mod, fn)(text, glossary) if fn == "check_glossary" else getattr(mod, fn)(text))
            for fn in CHAPTER_FNS}
    if sum(msgs.values(), []) != mod.check_chapter(path, budget, glossary):
        raise Unclassified(f"{path}: per-function messages differ from legacy check_chapter")
    measured = _measured(mod, text, budget, labels)
    return [e for fn in CHAPTER_FNS for e in _entries(fn, chapter_id(path), msgs[fn], measured)]


def book_checks(mod, layout, project_dir):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        fails = mod.check_all()
    total = int(re.search(r"^total words: (\d+)$", buf.getvalue(), re.M).group(1))
    names = {p.name for p in mod.ROOT.glob("*.md")}
    book = []
    for f in fails:
        if f.startswith("book:"):
            book.append(f)
        elif f.split(": ", 1)[0] not in names:  # chapter lines are captured per chapter
            raise Unclassified(f"check_all: {f}")
    measured = {"BOOK-CHAPTER-COUNT": {"chapters": len(chapter_paths(project_dir, layout))},
                "BUDGET-TOTAL": {"total_words": total},
                "GLOSS-MIN": {"glossary_terms": len(mod.load_glossary(pathlib.Path(project_dir) / layout["glossary"]))}}
    return _entries("check_all", "book", book, measured), total


def parse_refs_output(chapter, text):
    rows = []
    for line in text.splitlines():
        if not line.strip():
            continue
        for rx, status in [(r"^OK (\d+)$", "ok"), (r"^NO DOI (\d+)$", "no_doi"),
                           (r"^NOT FOUND (\d+): ", "not_found"), (r"^TITLE MISMATCH (\d+): ", "title_mismatch")]:
            m = re.match(rx, line)
            if m:
                rows.append({"chapter": chapter, "n": int(m.group(1)), "status": status})
                break
        else:
            if line.startswith("ERROR "):
                raise NetworkError(f"{chapter}: {line}")
            raise Unclassified(f"verify_refs {chapter}: {line}")
    return rows


def refs(project_dir, layout, paths):
    tool = pathlib.Path(project_dir) / layout["legacy_tools"] / "verify_refs.py"
    # a gated copy (Task 7.3 shim) needs --project; the frozen STEP 5 fixture copy has no shim
    gate = ["--project", str(project_dir)] if "harness.gate" in tool.read_text(encoding="utf-8") else []
    rows = []
    for p in paths:
        r = subprocess.run([sys.executable, str(tool), *gate, str(p)], capture_output=True, text=True, encoding="utf-8")
        if r.stderr.lstrip().startswith("ERROR "):   # a refused gate exits 1 like a failing check: never freeze it
            raise GateRefused(f"{chapter_id(p)}: {r.stderr.strip()[-300:]}")
        if r.returncode not in (0, 1):
            raise NetworkError(f"{chapter_id(p)}: verify_refs exit {r.returncode}: {r.stderr.strip()[-300:]}")
        rows += parse_refs_output(chapter_id(p), r.stdout)
    return rows


def reference_counts(project_dir, layout, paths):
    mod = _load(pathlib.Path(project_dir) / layout["legacy_tools"] / "verify_refs.py", "legacy_verify_refs")
    out = {}
    for p in paths:
        lines = [line for _, line in mod.references(p.read_text(encoding="utf-8"))]
        doi = sum(1 for line in lines if DOI_REF.search(line))
        out[chapter_id(p)] = {"count": len(lines), "with_doi": doi, "without_doi": len(lines) - doi}
    return out


def images(project_dir, layout):
    from PIL import Image
    out = []
    for d in layout["images"]:
        for p in sorted((pathlib.Path(project_dir) / d).rglob("*")):
            if p.suffix.lower() in {".png", ".jpg", ".jpeg"}:
                with Image.open(p) as im:
                    dpi = im.info.get("dpi")
                    out.append({"path": _rel(p, project_dir), "width_px": im.width, "height_px": im.height,
                                "dpi": [round(float(x), 2) for x in dpi] if dpi else None})
    return out


def _strip_volatile(name, root):
    """N5: remove only the enumerated volatile nodes, in place."""
    for el in root.iter():
        for k in [k for k in el.attrib if k.startswith(_w("rsid")) or k in VOLATILE_ATTRS]:
            del el.attrib[k]
    drop = [el for el in root.iter(*VOLATILE_TAGS)]
    toc_ids = set()
    for el in root.iter(_w("bookmarkStart")):
        if el.get(_w("name"), "").startswith("_Toc"):
            toc_ids.add(el.get(_w("id")))
            drop.append(el)
    drop += [el for el in root.iter(_w("bookmarkEnd")) if el.get(_w("id")) in toc_ids]
    # TOC field result, per run child: text/tabs inside the result are dropped; a fldChar is dropped only when it
    # is inside the result both before and after it, so the TOC's own begin/instr/separate/end always stay.
    stack, touched = [], set()
    in_result = lambda: any(f["toc"] and f["result"] for f in stack)
    for run in root.iter(_w("r")):
        if in_result():
            touched.add(run)
        for child in run:
            if child.tag == _w("rPr"):
                continue
            before = in_result()
            if child.tag == _w("fldChar"):
                kind = child.get(_w("fldCharType"))
                if kind == "begin":
                    stack.append({"instr": "", "toc": False, "result": False})
                elif kind == "separate" and stack:
                    stack[-1]["result"] = True
                    stack[-1]["toc"] = stack[-1]["instr"].strip().startswith("TOC")
                elif kind == "end" and stack:
                    stack.pop()
                gone = before and in_result()
            else:
                if child.tag == _w("instrText") and stack:
                    stack[-1]["instr"] += child.text or ""
                gone = before
            if gone:
                drop.append(child)
                touched.add(run)
    if name == "docProps/core.xml":
        drop += [el for el in root if el.tag in VOLATILE_CORE]
    if name == "docProps/app.xml":
        drop += [el for el in root if el.tag in VOLATILE_APP]
    for el in drop:
        if el.getparent() is not None:
            el.getparent().remove(el)
    emptied = set()
    for run in touched:  # a run left with only formatting was pure result
        if run.getparent() is not None and all(c.tag == _w("rPr") for c in run):
            if run.getparent().tag == _w("hyperlink"):
                emptied.add(run.getparent())
            run.getparent().remove(run)
    for h in emptied:
        if h.getparent() is not None and not h.findall(_w("r")):
            h.getparent().remove(h)


def embedded_fonts(z):
    """{part name: {font, embed}} for every embedded font declared in word/fontTable.xml."""
    from lxml import etree
    names = set(z.namelist())
    if not {"word/fontTable.xml", "word/_rels/fontTable.xml.rels"} <= names:
        return {}
    targets = {r.get("Id"): r.get("Target") for r in etree.fromstring(z.read("word/_rels/fontTable.xml.rels"))
               .iter(f"{{{PKG_REL}}}Relationship")}
    fonts = {}
    for font in etree.fromstring(z.read("word/fontTable.xml")).iter(_w("font")):
        for el in font:
            rid = el.get(f"{{{R}}}id")
            if rid in targets:
                part = "word/" + targets[rid].lstrip("/").removeprefix("word/")
                fonts[part] = {"font": font.get(_w("name")), "embed": etree.QName(el).localname}
    return fonts


def docx_parts(path):
    from lxml import etree
    out = {}
    with zipfile.ZipFile(path) as z:
        fonts = embedded_fonts(z)
        for name in sorted(z.namelist()):
            data = z.read(name)
            if name in fonts:  # ponytail: identity, not bytes; Word rewrites font bytes per save (same-length edits unseen)
                out[name] = hashing.hash_bytes(hashing.canonical_json(dict(fonts[name], length=len(data))))
                continue
            if name.endswith((".xml", ".rels")):
                root = etree.fromstring(data)
                _strip_volatile(name, root)
                data = etree.tostring(root, method="c14n")
            out[name] = hashing.hash_bytes(data)
    return out


def docx_facts(path):
    from lxml import etree
    with zipfile.ZipFile(path) as z:
        parts = sorted(z.namelist())
        doc = etree.fromstring(z.read("word/document.xml"))
        core = etree.fromstring(z.read("docProps/core.xml"))
    styles = {}
    for p in doc.iter(_w("p")):
        s = p.find(f"{_w('pPr')}/{_w('pStyle')}")
        k = s.get(_w("val")) if s is not None else "(none)"
        styles[k] = styles.get(k, 0) + 1
    instr = "".join(t.text or "" for t in doc.iter(_w("instrText")))
    return {"parts": parts, "paragraph_styles": styles, "images": sum(1 for _ in doc.iter(f"{{{A}}}blip")),
            "toc_field": bool(re.search(r"(^|\s)TOC\s", instr)),
            "core_properties": {etree.QName(el).localname: el.text or "" for el in core if el.tag not in VOLATILE_CORE}}


def pdf_facts(path):
    from pypdf import PdfReader
    reader = PdfReader(str(path))
    titles = []

    def walk(items, level):
        for it in items:
            if isinstance(it, list):
                walk(it, level + 1)
            else:
                titles.append({"level": level, "title": it.title})
    walk(reader.outline, 0)
    return {"pages": len(reader.pages), "bookmarks": titles}


def _tool_sha(project_dir, layout):
    r = subprocess.run(["git", "log", "-1", "--format=%H", "--", layout["legacy_tools"]],
                       cwd=project_dir, capture_output=True, text=True)
    if r.returncode != 0 or not r.stdout.strip():
        raise RuntimeError(f"git log failed for {layout['legacy_tools']}: {r.stderr.strip()}")
    return r.stdout.strip()


def _tail(project_dir, layout, paths, tool_sha):
    """The keys every capture mode computes the same way: images, DOCX/PDF facts, hashes, provenance."""
    deliv = {k: project_dir / v for k, v in layout["deliverables"].items()}
    parts = docx_parts(deliv["docx"])
    return {
        "images": images(project_dir, layout),
        "docx": docx_facts(deliv["docx"]),
        "pdf": pdf_facts(deliv["pdf"]),
        "hashes": {"assembled_md": hashing.hash_file(deliv["md"]),
                   "docx": hashing.hash_bytes(hashing.canonical_json(parts)),
                   "docx_parts": parts,
                   "chapters": {chapter_id(p): hashing.hash_file(p) for p in paths}},
        "volatile_excluded": VOLATILE_EXCLUDED,
        "provenance": {"tool_sha": tool_sha,
                       "captured_from": _rel(project_dir, REPO) if project_dir.is_relative_to(REPO) else project_dir.name},
    }


def _chapter_list(project_dir, paths):
    out = []
    for p in paths:
        h1 = re.search(r"^# (.+?)\s*$", p.read_text(encoding="utf-8"), re.M)
        out.append({"id": chapter_id(p), "file": _rel(p, project_dir), "title": h1.group(1) if h1 else None})
    return out


def capture(project_dir, layout, *, slug, run_refs=True):
    """Legacy mode (STEPS 5-6, plan N6): checks from the project's legacy checker, per function."""
    project_dir = pathlib.Path(project_dir)
    probs = layout_problems(project_dir, layout)
    if probs:
        raise LayoutError("; ".join(probs))
    mod = load_legacy_checker(project_dir, layout)
    paths = chapter_paths(project_dir, layout)
    glossary = project_dir / layout["glossary"]
    checks = [e for p in paths for e in checks_for_chapter(mod, p, glossary, layout["legacy_sections"])]
    book, total = book_checks(mod, layout, project_dir)
    checks = sorted(checks + book, key=lambda e: (e["target"], e["id"]))
    front = project_dir / layout["front_matter"]
    return {
        "schema_version": 1,
        "project": slug,
        "checks": checks,
        "chapters": _chapter_list(project_dir, paths),
        "words": {"chapters": {chapter_id(p): mod.words(p.read_text(encoding="utf-8")) for p in paths},
                  "front_matter": mod.words(front.read_text(encoding="utf-8")) if front.exists() else None,
                  "total": total},
        "references": reference_counts(project_dir, layout, paths),
        "verify_refs": refs(project_dir, layout, paths) if run_refs else None,
        **_tail(project_dir, layout, paths, _tool_sha(project_dir, layout)),
    }


# ---------- harness mode (STEP 8, plan Task 8.1): layout and checks from project config ----------

DELIVERABLES = ("build", "deliverables")


def derive_layout(project_dir, docx_from="build"):
    """The capture layout implied by template.json / theme.json (same keys as layout-projects.json)."""
    from harness.tools import config
    if docx_from not in DELIVERABLES:
        raise LayoutError(f"--docx-from must be one of {DELIVERABLES}")
    cfg = config.load(project_dir)
    p = cfg["template"]["paths"]
    ch = p["chapters"]
    roles = {s["role"]: s["label"] for s in cfg["template"]["sections"]}
    base = f"{docx_from}/{cfg['theme']['output']['basename']}"
    roots = list(p["allowed_asset_roots"])
    return {"schema_version": 1, "chapters_dir": ch, "chapter_glob": p["chapter_glob"],
            "front_matter": f"{ch}/{p['front_matter']}" if p.get("front_matter") else None,
            "glossary": f"{ch}/{p['glossary']}" if p.get("glossary") else None,
            "errata": f"{ch}/{p['errata']}" if p.get("errata") else None,
            "images": roots, "legacy_tools": f"{ch}/tools",
            "legacy_sections": {"assessment": roles.get("assessment"), "answers": roles.get("answers")},
            "deliverables": {ext: f"{base}.{ext}" for ext in ("md", "docx", "pdf")},
            "src_copy": [ch] + [r for r in roots if not r.startswith(ch + "/")] + [f"{base}.md"]}


def harness_report(project_dir):
    """checker JSON from the gated harness checker of the repo that holds the project."""
    repo = pathlib.Path(project_dir).resolve().parents[1]
    r = subprocess.run([sys.executable, str(repo / "harness/tools/check_book.py"), "--project", str(project_dir), "--json"],
                       cwd=repo, capture_output=True, text=True, encoding="utf-8")
    if r.returncode == 1 and r.stderr.lstrip().startswith("ERROR "):   # a refused gate: never freeze it
        raise GateRefused(r.stderr.strip()[-300:])
    if r.returncode not in (0, 1):
        raise LayoutError(f"check_book exit {r.returncode}: {r.stderr.strip()[-300:]}")
    return json.loads(r.stdout)


def harness_checks(report):
    """checker-report targets -> golden checks[] (message kept only on fail, as in the legacy capture)."""
    out = []
    for t in report["targets"]:
        for c in t["checks"]:
            e = {"id": c["id"], "target": t["target"], "status": c["status"], "measured": c["measured"]}
            if c["status"] == "fail":
                e["message"] = c["message"]
            out.append(e)
    return sorted(out, key=lambda e: (e["target"], e["id"]))


def harness_reference_counts(cfg):
    from harness.tools import check_book
    ids = [re.compile(x) for x in cfg["template"]["references"]["identifier_patterns"]]
    out = {}
    for c, path in cfg.chapters():
        lines = [line for _, line in check_book.reference_entries(path.read_text(encoding="utf-8"), cfg)]
        doi = sum(1 for line in lines if any(x.search(line) for x in ids))
        out[c["id"]] = {"count": len(lines), "with_doi": doi, "without_doi": len(lines) - doi}
    return out


REF_STATUS = {None: "ok", "REF-NOT-FOUND": "not_found", "REF-TITLE-MISMATCH": "title_mismatch",
              "REF-NO-DOI-DISALLOWED": "no_doi_disallowed"}


def harness_refs(project_dir, layout, paths):
    """verify_refs rows from the gated harness tool (Task 8.3) when the repo has it, else the legacy project tool."""
    repo = pathlib.Path(project_dir).resolve().parents[1]
    tool = repo / "harness/tools/verify_refs.py"
    if not tool.is_file():
        return refs(project_dir, layout, paths)
    r = subprocess.run([sys.executable, str(tool), "--project", str(project_dir), "--json"], cwd=repo,
                       capture_output=True, text=True, encoding="utf-8")
    if r.returncode == 1 and not r.stdout.strip():
        raise GateRefused(r.stderr.strip()[-300:])
    if r.returncode not in (0, 1):
        raise LayoutError(f"verify_refs exit {r.returncode}: {r.stderr.strip()[-300:]}")
    rows = []
    for chapter, found in json.loads(r.stdout)["chapters"].items():
        for x in found:
            if x["check_id"] == "REF-ERROR":   # a flaky result is never frozen (core §9.1)
                raise NetworkError(f"{chapter}: reference {x['n']}: {x.get('error')}")
            status = "no_doi_allowed" if x["doi_status"] == "no_doi" and x["check_id"] is None else REF_STATUS[x["check_id"]]
            rows.append({"chapter": chapter, "n": x["n"], "status": status})
    return rows


def _git_sha(repo, rel):
    r = subprocess.run(["git", "log", "-1", "--format=%H", "--", rel], cwd=repo, capture_output=True, text=True)
    if r.returncode != 0 or not r.stdout.strip():
        raise RuntimeError(f"git log failed for {rel}: {r.stderr.strip()}")
    return r.stdout.strip()


def capture_harness(project_dir, *, slug, run_refs=True, docx_from="build"):
    from harness.tools import config
    project_dir = pathlib.Path(project_dir)
    layout = derive_layout(project_dir, docx_from)
    cfg = config.load(project_dir)
    paths = [p for _, p in cfg.chapters()]
    report = harness_report(project_dir)
    by = {(t["target"], c["id"]): c["measured"] for t in report["targets"] for c in t["checks"]}
    words = {"chapters": {c["id"]: by[(c["id"], "BUDGET-CHAPTER")]["words"] for c, _ in cfg.chapters()},
             "front_matter": by.get(("book", "BUDGET-FRONT"), {}).get("words"),
             "total": report["total_words"]}
    return {
        "schema_version": 1,
        "project": slug,
        "checks": harness_checks(report),
        "chapters": _chapter_list(project_dir, paths),
        "words": words,
        "references": harness_reference_counts(cfg),
        "verify_refs": harness_refs(project_dir, layout, paths) if run_refs else None,
        **_tail(project_dir, layout, paths, _git_sha(project_dir.resolve().parents[1], "harness/tools")),
    }


def write(obj, out):
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(dumps(obj))


def resolve_project(arg):
    """Core §1.1 projects rule, inline until harness/paths.py exists (Task 7.1 replaces this)."""
    p = pathlib.Path(arg).resolve()
    if p.parent != (REPO / "projects").resolve():
        raise ValueError(f"PROJECT-OUTSIDE: {arg} is not a direct child of {REPO / 'projects'}")
    if not SLUG.match(p.name):
        raise ValueError(f"PROJECT-NAME: {p.name!r} does not match {SLUG.pattern}")
    if not p.is_dir():
        raise ValueError(f"PROJECT-MISSING: {arg}")
    return p


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--layout", help="legacy mode: which files inside the project to read (N1); omit for harness mode")
    ap.add_argument("--docx-from", choices=DELIVERABLES, default="build", help="harness mode: where md/docx/pdf are read")
    ap.add_argument("--no-refs", action="store_true")
    a = ap.parse_args()
    try:
        project = resolve_project(a.project)
    except ValueError as e:
        print(f"ERROR {e}", file=sys.stderr)
        sys.exit(1)
    try:
        if a.layout:
            layout = json.loads(pathlib.Path(a.layout).read_text(encoding="utf-8"))
            golden = capture(project, layout, slug=project.name, run_refs=not a.no_refs)
        else:
            golden = capture_harness(project, slug=project.name, run_refs=not a.no_refs, docx_from=a.docx_from)
        write(golden, a.out)
    except ImportError as e:
        print(f"ERROR DEPENDENCY: {e}", file=sys.stderr)
        sys.exit(1)
    except LayoutError as e:
        print(f"ERROR LAYOUT: {e}", file=sys.stderr)
        sys.exit(1)
    except GateRefused as e:
        print(f"ERROR GATE: {e}", file=sys.stderr)
        sys.exit(1)
    except (NetworkError, Unclassified) as e:
        print(f"ERROR {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
