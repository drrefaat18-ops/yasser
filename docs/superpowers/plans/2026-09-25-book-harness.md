# Book Harness Implementation Plan (STEPS 5–11)

> **For agentic workers:** Execution is **Claude inline** (DEC-017), using superpowers:executing-plans. Steps use checkbox (`- [ ]`) syntax. Subagents: default 0, at most 2 at a time, each with a stated reason logged in the ledger row (DEC-014, DEC-015, Rule 11). Codex dispatches do not count.

**Goal:** Turn the one-book medical workspace into a generic, gated book harness (control plane, config-driven tools, ingest, figures with a chemistry pack, Arabic locale, EN↔AR translation) without changing the medical book's verified output.

**Architecture:** One stdlib Python control plane (`harness/state.py`, `harness/run_stage.py`) owns receipts, approvals, gates and the run lease. Every executable calls `state.require_gates`. Tools under `harness/tools/` are driven by per-project JSON config (`brief`, `rubric`, `template`, `theme`, `chapter-plan`) and a locale profile passed as a parameter. Rendering (python-docx + Word COM) and figures (matplotlib, headless Edge/Chrome, optional RDKit) sit behind preflight-checked dependency groups.

**Tech Stack:** Python 3.11 stdlib (`unittest`, `json`, `hashlib`, `re`, `unicodedata`, `subprocess`, `urllib`); python-docx, lxml, Pillow, pywin32 + Microsoft Word, pypdf; matplotlib; RDKit (optional group, STEP 9); markitdown (optional, non-DOCX ingest).

**Specs (approved at `fcfee40`, DEC-032):**
- `docs/superpowers/specs/2026-09-25-book-harness-core-design.md` (cited *core §N*)
- `docs/superpowers/specs/2026-09-25-arabic-locale-contract.md` (cited *AR §N*)
- `docs/superpowers/specs/2026-09-25-translation-contract.md` (cited *TR §N*)
- Ticket: `docs/harness/TICKET.md` (approved `23d819f`, DEC-026). Vision: `docs/harness/VISION.md`.

## Global Constraints

- Control plane, checker, assembler, `verify_refs`, comparator, leak scan: **Python 3.11 stdlib only** (Rule 10, core §12).
- Runtime code **never installs** anything; missing dependencies are named by preflight and the tool exits non-zero (core §12).
- Every executable requires `--project <path>`; the path must be a direct child of `<repo>/projects/` with name `^[a-z0-9][a-z0-9-]{1,62}$`; no bypass flag (core §1.1). Sole exception: plan note N1.
- No stage after `intake` runs without a hash-matching intake approval; `translate`, `rework`, `build`, `audit` also need the design approval; enforced by `state.require_gates` in every executable, including legacy tools (Rule 7, core §2.3).
- Shared code under `harness/` carries no profession names, box labels, clinical terms, book titles, author names or absolute paths (Rule 8, core §9.5).
- JSON hashed canonically (`sort_keys=True, separators=(",", ":"), ensure_ascii=False`, UTF-8); `.md .txt .svg .py` hashed after CRLF→LF; others raw bytes (core §2.3).
- Never modify `AI_in_Medicine- Assistant Prof Dr Shereen Elkholy.{md,docx}` or the finished interprofessional outputs; the only exception is the manifest `git mv` in STEP 6 (Rule 5).
- One commit per task, after its gates pass; **never push** (DEC-028).
- One Codex review per STEP (the STEP's tasks are one artifact batch), read-only via `codex-delegate`, **without** `--ignore-user-config`; findings resolved through the Fix Protocol into `docs/harness/reviews/step<N>-fixes.md` (DEC-030).
- Tests: `python -m unittest discover -s tests -t . -v` from the repo root; every test file is stdlib `unittest`.
- Stop and ask the user at every user-approval point (DEC-028): manifest (STEP 6), medical onboarding intake + design + history import (STEP 7), outputs seen (STEP 11).

## Plan–spec notes (approved with this plan)

These resolve points the specs leave to the plan (core §13). None changes a spec decision.

- **N1 — Baseline capture before migration.** STEP 5 runs before `projects/` exists, so `capture_golden.py` takes `--project <dir>` plus `--layout <json>` naming where chapters, glossary, errata, figures, images and deliverables live. It is **read-only** (writes only `--out` and, with `--copy-src`, the fixture `src/`), is not a stage, and is therefore exempt from the `projects/` rule only while `--layout tests/fixtures/ai-in-medicine/layout-legacy.json` is used. From STEP 6 on it runs with `--project projects/ai-in-medicine` and the projects rule applies.
- **N2 — History import for the medical project.** The medical book was ingested, evaluated, designed and reworked before the harness existed. `require_gates` needs valid upstream receipts, which cannot honestly be produced by re-running agentic stages. `run_stage.py --project P import-history <stage> --dec DEC-NNN` writes a receipt with `status: ok`, `imported: true`, `dec_id`, `dec_row_sha256`, current input/output hashes and the stage's `tool_sha`. It is allowed only for `ingest`, `evaluate`, `design`, `rework`, only when the DEC row names "import-history" and the stage, and `verify` prints `imported` next to such receipts. It is used once, for `ai-in-medicine`, after the user approves it (STEP 7, Task 7.4).
- **N3 — Finished outputs are preserved, not rebuilt over.** The manifest moves `AI_in_Health_Care_Interprofessional.{md,docx,pdf}` to `projects/ai-in-medicine/deliverables/`. Harness builds write to `projects/ai-in-medicine/build/` (core §1.1). The STEP 8 golden comparison is `deliverables` capture (STEP 6) vs `build` capture (STEP 8).
- **N4 — Legacy stage mapping for gates.** Legacy tools gate as: `convert_docx_to_md.py` → `ingest`; `check_book.py`, `verify_refs.py`, `renumber_refs.py`, `assemble.py` → `rework`; `build_book.py` → `build`.
- **N5 — Semantic DOCX hash.** `hashes.docx_document` = SHA-256 of the canonical JSON list of `[style_id, text]` per body paragraph plus `["tbl", rows, cols]` per table and `["img", rel_target_basename]` per drawing, **excluding** paragraphs inside the TOC field result and ignoring `w:rsid*`, `w:lastRenderedPageBreak`, `_Toc*` bookmarks and proofing marks. These exclusions are listed in `volatile_excluded[]` (core §9.1) with the reason "Word COM TOC refresh and save metadata".
- **N6 — Legacy check IDs in the golden.** In STEP 5–6 the golden is captured from the legacy checker by importing its functions per chapter; each function maps to the core §9.3 IDs it covers (table in Task 5.2). A function returning `[]` marks its IDs `pass`; a returned message is classified by the regex table; an unclassified message makes capture exit 2. From STEP 8 the golden is built from `checker-report.v1` JSON. Both produce identical `checks[]` for an unchanged book.

## Review Focus

Inputs the specs imply that no single happy-path test hits, most likely first. Each has a pinned test in the named task.

1. **A covered file edited by a text editor that adds CRLF or a BOM** — must not flip an approval stale for CRLF alone, but a BOM or content change must. Pinned: Task 7.1 `test_hash_crlf_equal_bom_differs`.
2. **A project path given as a symlink, `..` segment or trailing slash that resolves outside `projects/`** — must fail `PROJECT-OUTSIDE`. Pinned: Task 7.1 `test_resolve_project_rejects_escape`.
3. **A crashed agentic stage leaving `active_run` set** — the next `begin` must fail `RUN-ACTIVE` naming stage and time, and `abort` must recover. Pinned: Task 7.2 `test_crashed_run_needs_abort`.
4. **Offline network during `verify_refs` or PubChem** — must report `error`/`unverified`, never `ok`/`pass`, and capture must refuse to freeze. Pinned: Task 5.2 `test_capture_refuses_network_error`, Task 8.3 `test_network_error_is_ref_error`, Task 9.2 `test_offline_is_unverified`.
5. **An Arabic chapter using Arabic-Indic digits in citations `[١، ٣]` and a mixed-system number `1٢`** — citations must parse; the mixed number must fail `AR-DIGIT-MIXED`. Pinned: Task 10.1 `test_arabic_citation_digits`, `test_mixed_number_fails`.

---

## Execution protocol per STEP

For every STEP 5–11:
1. Update `docs/harness/LEDGER.md` row to `In progress`.
2. Execute its tasks in order; each task ends with its gate commands passing and one commit.
3. After the last task: `python -m unittest discover -s tests -t . -v` → exit 0.
4. One Codex review (read-only, `codex-delegate`, brief lists the STEP's commits, the tasks from this plan, the specs, and asks for the S<N>-NN findings table used in STEP 3). Save verbatim to `docs/harness/reviews/step<N>-review.md`.
5. Fix Protocol into `docs/harness/reviews/step<N>-fixes.md`; re-run the STEP gates; commit.
6. Ledger row `Done` with commit SHAs, subagent count and reasons.

Codex brief skeleton (copied into each STEP's brief):

```text
You are a read-only reviewer. Do NOT edit files or commit.
<context>Repo D:\yasser. STEP <N> of the book-harness ticket. Commits: <sha list>.</context>
<review_targets>files changed in those commits</review_targets>
<review_against>plan tasks <N.x> in docs/superpowers/plans/2026-09-25-book-harness.md; core/AR/TR specs; TICKET STEP <N>; VISION.md</review_against>
<gates>python -m unittest discover -s tests -t . -v  (expect exit 0) ; <STEP-specific commands></gates>
<report_contract>reviewed_commit / verdict / open_blocker_major; findings table | ID | Severity | File:line | Problem | Concrete fix |; Top 5; "No files were modified."</report_contract>
```

---

## File structure

```text
harness/
  __init__.py
  paths.py            # REPO, resolve_project(), project-relative path helpers
  hashing.py          # hash_file(), canonical_json()
  schema.py           # stdlib validator for the core §4 JSON Schema subset; load_schema()
  state.py            # STAGES, APPROVAL_SETS, receipts, require_gates, lease, approve, verify, import_history
  run_stage.py        # CLI over state.py and stage implementations
  stages/             # one module per auto stage + agentic completers
    __init__.py  new.py  ingest.py  build.py  complete_checks.py
  preflight.py
  defaults.json  rubric_core.json
  schemas/*.v1.json
  agents/*.md
  locale/en.json  locale/ar.json  locale/__init__.py (load_profile)
  text.py             # tokenizer, sentence splitter, digits, normalisation — profile-parameterised
  presets/ltr-textbook.json  presets/rtl-textbook.json
  tools/  config.py check_book.py assemble.py build_book.py verify_refs.py renumber_refs.py
          convert_docx.py capture_golden.py compare_golden.py leak_scan.py check_translation.py
  figures/ render.py check_figures.py charts.py packs/__init__.py packs/chemistry/__init__.py
tests/
  helpers.py          # temp_repo() per core §9.6, run_cli()
  test_*.py
  fixtures/ai-in-medicine/  positive-config/<5>/  mutations/  ingest/  locale/ar/  translation/{en-ar,ar-en}/  leak/
projects/ai-in-medicine/   # after STEP 6
.claude/skills/book-{new,intake,ingest,evaluate,design,translate,rework,build,audit,verify}/SKILL.md
```

Responsibility boundaries: `paths`/`hashing`/`schema` have no knowledge of stages; `state` knows stages but not tool internals; tools know config but not state files (the runner passes them config and paths); `text.py` knows locale profiles but not templates.

---

## Migration manifest format (STEP 6)

`docs/harness/migration-manifest.json`:

```json
{
  "schema_version": 1,
  "project": "ai-in-medicine",
  "reserved": ["CLAUDE.md"],
  "moves": [
    {"source": "rework/ch01-what-ai-is.md", "destination": "projects/ai-in-medicine/rework/ch01-what-ai-is.md", "sha256": "<pre-move hash>"}
  ],
  "path_fix_allowlist": ["projects/ai-in-medicine/rework/tools/check_book.py"],
  "expected_diff": [
    {"pointer_glob": "/project", "reason": "capture now names projects/ai-in-medicine"},
    {"pointer_glob": "/images/*/path", "reason": "paths are now under projects/ai-in-medicine/"}
  ]
}
```

Rules checked by `tests/test_manifest.py`: every `source` exists and is tracked; no `destination` exists; no entry touches a `reserved` path; `sha256` equals the current hash (raw bytes, since moves are byte-identical); destinations keep `images/` beside `rework/`; `expected_diff` uses the `golden-diff.v1` allowlist form (core §9.2).

---

## STEP 5 — Preflight and medical baseline freeze

### Task 5.1: `harness/preflight.py`

**Files:**
- Create: `harness/__init__.py` (empty), `harness/preflight.py`
- Test: `tests/__init__.py` (empty), `tests/test_preflight.py`

**Interfaces:**
- Produces: `preflight.run(groups: list[str]) -> list[Check]` where `Check = dict(name=str, group=str, ok=bool, detail=str, required=bool)`; CLI `python harness/preflight.py [--group core|build|ingest|figures|chemistry|golden ...] [--json]`, exit 0 iff every **required** check is ok. Groups `core, build, ingest, figures, golden` are required by default; `chemistry` and `markitdown` are optional (reported, never fail unless requested with `--group chemistry`).

Checks (name → how):

| Name | Group | How |
|---|---|---|
| `python>=3.11` | core | `sys.version_info >= (3, 11)` |
| `git` | core | `git --version` exit 0 |
| `write-lock` | core | create then delete `projects/.preflight-<pid>` with `open(..., "x")`; report any existing `projects/*/state.lock` with its content |
| `python-docx`, `lxml` | ingest, build | `importlib.util.find_spec` |
| `markitdown` | ingest (optional) | `find_spec("markitdown")` |
| `Pillow`, `pywin32` | build | `find_spec("PIL")`, `find_spec("win32com")` |
| `word-com` | build | `win32com.client.DispatchEx("Word.Application")` then `.Quit()`; detail is Word `.Version` |
| `browser` | build, figures | first existing of `%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe`, `%ProgramFiles%\Microsoft\Edge\Application\msedge.exe`, `%ProgramFiles%\Google\Chrome\Application\chrome.exe` |
| `fonts` | build | files present in `%WINDIR%\Fonts`: `Sitka.ttc`, `segoeui.ttf`, `majalla.ttf`, `majallab.ttf` (font list read from `harness/presets/*.json` `required_font_files` once presets exist; until STEP 7 the list is a module constant, then moved) |
| `matplotlib` | figures | `find_spec` |
| `pypdf` | golden | `find_spec` |
| `rdkit` | chemistry (optional) | `find_spec("rdkit")` and, if present, `Chem.MolFromSmiles("CCO")` not None |

- [ ] **Step 1: Write the failing test**

```python
# tests/test_preflight.py
import json, subprocess, sys, unittest
from harness import preflight

class PreflightTest(unittest.TestCase):
    def test_missing_module_is_named(self):
        checks = preflight.check_module("definitely_not_a_module_xyz", group="core", required=True)
        self.assertFalse(checks["ok"])
        self.assertIn("definitely_not_a_module_xyz", checks["detail"])

    def test_optional_group_does_not_fail_default_run(self):
        checks = preflight.run(["core"]) + [dict(name="rdkit", group="chemistry", ok=False, detail="missing", required=False)]
        self.assertEqual(preflight.exit_code(checks), 0 if all(c["ok"] for c in checks if c["required"]) else 1)

    def test_cli_json_lists_every_check(self):
        out = subprocess.run([sys.executable, "harness/preflight.py", "--group", "core", "--json"],
                             capture_output=True, text=True)
        names = {c["name"] for c in json.loads(out.stdout)}
        self.assertTrue({"python>=3.11", "git", "write-lock"} <= names)

if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run to verify it fails** — `python -m unittest tests.test_preflight -v` → FAIL (`ModuleNotFoundError: harness.preflight`).

- [ ] **Step 3: Implement**

```python
# harness/preflight.py
"""Dependency and environment probe. Never installs anything (Rule 10)."""
import argparse, importlib.util, json, os, pathlib, subprocess, sys

REPO = pathlib.Path(__file__).resolve().parents[1]
DEFAULT_GROUPS = ["core", "ingest", "build", "figures", "golden"]
FONT_FILES = ["Sitka.ttc", "segoeui.ttf", "majalla.ttf", "majallab.ttf"]  # ponytail: moves to presets in STEP 7
BROWSERS = [r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe",
            r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe",
            r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"]


def _c(name, group, ok, detail, required=True):
    return dict(name=name, group=group, ok=bool(ok), detail=detail, required=required)


def check_module(module, group, required=True, label=None):
    found = importlib.util.find_spec(module) is not None
    return _c(label or module, group, found, "present" if found else f"missing Python package: {module}", required)


def check_python():
    return _c("python>=3.11", "core", sys.version_info >= (3, 11), sys.version.split()[0])


def check_git():
    try:
        r = subprocess.run(["git", "--version"], capture_output=True, text=True)
        return _c("git", "core", r.returncode == 0, r.stdout.strip() or r.stderr.strip())
    except FileNotFoundError:
        return _c("git", "core", False, "git not on PATH")


def check_write_lock():
    projects = REPO / "projects"
    projects.mkdir(exist_ok=True)
    probe = projects / f".preflight-{os.getpid()}"
    try:
        with open(probe, "x", encoding="utf-8") as f:
            f.write("probe")
        probe.unlink()
    except OSError as e:
        return _c("write-lock", "core", False, f"cannot exclusive-create in projects/: {e}")
    stale = [f"{p}: {p.read_text(encoding='utf-8', errors='replace').strip()}" for p in projects.glob("*/state.lock")]
    return _c("write-lock", "core", not stale, "; ".join(stale) or "exclusive-create works, no leftover locks")


def check_word():
    if importlib.util.find_spec("win32com") is None:
        return _c("word-com", "build", False, "pywin32 missing")
    try:
        import win32com.client
        word = win32com.client.DispatchEx("Word.Application")
        version = word.Version
        word.Quit()
        return _c("word-com", "build", True, f"Word {version}")
    except Exception as e:  # COM failure names itself
        return _c("word-com", "build", False, f"Word COM unavailable: {e}")


def check_browser(group):
    for raw in BROWSERS:
        path = pathlib.Path(os.path.expandvars(raw))
        if path.exists():
            return _c("browser", group, True, str(path))
    return _c("browser", group, False, "no Edge or Chrome found for SVG rasterising")


def check_fonts():
    fonts = pathlib.Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts"
    missing = [f for f in FONT_FILES if not (fonts / f).exists()]
    return _c("fonts", "build", not missing, "missing: " + ", ".join(missing) if missing else "all present")


def check_rdkit():
    if importlib.util.find_spec("rdkit") is None:
        return _c("rdkit", "chemistry", False, "missing Python package: rdkit", required=False)
    from rdkit import Chem
    return _c("rdkit", "chemistry", Chem.MolFromSmiles("CCO") is not None, "smoke test CCO", required=False)


def run(groups):
    checks = []
    if "core" in groups:
        checks += [check_python(), check_git(), check_write_lock()]
    if "ingest" in groups:
        checks += [check_module("docx", "ingest", label="python-docx"), check_module("lxml", "ingest"),
                   check_module("markitdown", "ingest", required=False)]
    if "build" in groups:
        checks += [check_module("PIL", "build", label="Pillow"), check_module("win32com", "build", label="pywin32"),
                   check_word(), check_browser("build"), check_fonts()]
    if "figures" in groups:
        checks += [check_module("matplotlib", "figures")]
    if "golden" in groups:
        checks += [check_module("pypdf", "golden")]
    if "chemistry" in groups:
        c = check_rdkit()
        c["required"] = True  # explicitly requested
        checks.append(c)
    elif groups == DEFAULT_GROUPS:
        checks.append(check_rdkit())
    return checks


def exit_code(checks):
    return 0 if all(c["ok"] for c in checks if c["required"]) else 1


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--group", action="append")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    checks = run(a.group or DEFAULT_GROUPS)
    if a.json:
        print(json.dumps(checks, ensure_ascii=False, indent=1))
    else:
        for c in checks:
            tag = "OK" if c["ok"] else ("MISSING" if c["required"] else "OPTIONAL-MISSING")
            print(f"{tag} {c['name']}: {c['detail']}")
    sys.exit(exit_code(checks))


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run tests** — `python -m unittest tests.test_preflight -v` → PASS.
- [ ] **Step 5: Gate** — `python harness/preflight.py` → exit 0 (rdkit and markitdown print `OPTIONAL-MISSING`). **If exit ≠ 0, stop the ticket and tell the user what is missing (TICKET STEP 5).**
- [ ] **Step 6: Commit** — `git add harness/__init__.py harness/preflight.py tests/__init__.py tests/test_preflight.py && git commit -m "feat(harness): preflight probe (STEP 5a)"`

### Task 5.2: `capture_golden.py`, `compare_golden.py` and the frozen baseline

**Files:**
- Create: `harness/hashing.py`, `harness/tools/__init__.py`, `harness/tools/capture_golden.py`, `harness/tools/compare_golden.py`, `tests/fixtures/ai-in-medicine/layout-legacy.json`, `tests/fixtures/ai-in-medicine/golden.json`, `tests/fixtures/ai-in-medicine/src/**` (copied), `tests/test_hashing.py`, `tests/test_golden.py`

**Interfaces:**
- Produces: `hashing.canonical_json(obj) -> bytes`; `hashing.hash_bytes(b) -> str`; `hashing.hash_file(path) -> str` (core §2.3 rules). `capture_golden.capture(project: Path, layout: dict, *, run_refs=True) -> dict` (golden.v1); CLI `python harness/tools/capture_golden.py --project DIR --layout FILE --out FILE [--copy-src DIR] [--no-refs]`, exit 0 ok, 2 on any `verify_refs` `ERROR` or unclassified legacy message. `compare_golden.diff(a: dict, b: dict, allow: list[dict]) -> dict` (golden-diff.v1); CLI `python harness/tools/compare_golden.py A B --allow FILE [--out FILE]`, exit 0 iff every diff allowed.

`layout-legacy.json`:

```json
{
  "schema_version": 1,
  "chapters_dir": "rework",
  "chapter_glob": "ch*.md",
  "front_matter": "rework/00-front-matter.md",
  "glossary": "rework/glossary.md",
  "errata": "rework/errata-ledger.md",
  "images": ["images", "rework/figures"],
  "legacy_tools": "rework/tools",
  "deliverables": {"md": "AI_in_Health_Care_Interprofessional.md",
                   "docx": "AI_in_Health_Care_Interprofessional.docx",
                   "pdf": "AI_in_Health_Care_Interprofessional.pdf"},
  "src_copy": ["rework", "images", "AI_in_Health_Care_Interprofessional.md"]
}
```

Legacy function → check ID map (N6). Messages are classified by the first matching regex:

| Legacy function | IDs it covers | Message regex → ID |
|---|---|---|
| `check_template` | `TPL-H1`, `TPL-SECTION-MISSING`, `TPL-SECTION-ORDER`, `TPL-CALLOUT-MISSING` | `H1` → `TPL-H1`; `missing section` → `TPL-SECTION-MISSING`; `order` → `TPL-SECTION-ORDER`; `missing box` → `TPL-CALLOUT-MISSING` |
| `check_lenses` | `PERSP-MISSING`, `PERSP-BALANCE` | `lens .* missing` → `PERSP-MISSING`; `balance` → `PERSP-BALANCE` |
| `check_los` | `LO-COUNT`, `LO-VERB` | `objectives` → `LO-COUNT`; `understand` → `LO-VERB` |
| `check_mcqs` | `MCQ-COUNT`, `MCQ-OPTIONS`, `MCQ-EXTRA-OPTION`, `MCQ-LO-TAG`, `MCQ-CASE`, `KEY-MISSING`, `KEY-RATIONALE`, `KEY-BALANCE`, `KEY-RUN` | classified by the literal phrases the function emits (Step 3 copies them from `check_book.py:150-199`) |
| `check_citations` | `CIT-MISSING`, `CIT-UNCITED` | `no reference` → `CIT-MISSING`; `never cited` → `CIT-UNCITED` |
| `check_sentences` | `READ-MEAN`, `READ-LONG` | `mean` → `READ-MEAN`; `long` → `READ-LONG` |
| `check_banned` | `BANNED-TERM` | any → `BANNED-TERM` |
| `check_budget` | `BUDGET-CHAPTER` | any → `BUDGET-CHAPTER` |
| `check_glossary` | `GLOSS-MISSING` | any → `GLOSS-MISSING` |
| `check_all` book lines | `BOOK-CHAPTER-COUNT`, `BOOK-FRONT-MISSING`, `BUDGET-TOTAL`, `ERRATA-OPEN`, `GLOSS-MIN` | `chapters, need` / `missing 00-front` / `total .* words` / `errata` / `glossary has` |

`measured` per chapter: `words` (`words(prose)`), `mean_sentence`, `long_share` (from `clean_prose_lines` + the function's split), `lo_count`, `mcq_count`, `key_counts {A..D}`. Book: `total_words`, `glossary_terms`.

- [ ] **Step 1: Failing tests**

```python
# tests/test_hashing.py
import json, pathlib, tempfile, unittest
from harness import hashing

class HashingTest(unittest.TestCase):
    def _write(self, name, data):
        p = pathlib.Path(self.tmp.name) / name
        p.write_bytes(data)
        return p

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.tmp.cleanup()

    def test_json_canonical_ignores_key_order_and_spacing(self):
        a = self._write("a.json", b'{"b": 1, "a": [1, 2]}')
        b = self._write("b.json", b'{\n  "a": [1,2],\n  "b": 1\n}')
        self.assertEqual(hashing.hash_file(a), hashing.hash_file(b))

    def test_hash_crlf_equal_bom_differs(self):
        lf = self._write("lf.md", "# T\nx\n".encode())
        crlf = self._write("crlf.md", "# T\r\nx\r\n".encode())
        bom = self._write("bom.md", "\ufeff# T\nx\n".encode())
        self.assertEqual(hashing.hash_file(lf), hashing.hash_file(crlf))
        self.assertNotEqual(hashing.hash_file(lf), hashing.hash_file(bom))

    def test_binary_raw(self):
        a = self._write("a.png", b"\x89PNG\r\n")
        self.assertEqual(hashing.hash_file(a), hashing.hash_bytes(b"\x89PNG\r\n"))
```

```python
# tests/test_golden.py
import json, pathlib, subprocess, sys, tempfile, unittest
from harness.tools import capture_golden, compare_golden

class CompareTest(unittest.TestCase):
    def test_allowed_and_disallowed(self):
        a = {"project": "x", "words": {"total": 1}}
        b = {"project": "y", "words": {"total": 2}}
        d = compare_golden.diff(a, b, [{"pointer_glob": "/project", "reason": "rename"}])
        self.assertEqual({x["pointer"]: x["allowed"] for x in d["diffs"]}, {"/project": True, "/words/total": False})

    def test_wildcard_pointer(self):
        d = compare_golden.diff({"images": [{"path": "a"}]}, {"images": [{"path": "b"}]},
                                [{"pointer_glob": "/images/*/path", "reason": "moved"}])
        self.assertTrue(all(x["allowed"] for x in d["diffs"]))

class CaptureTest(unittest.TestCase):
    def test_classify_legacy_message(self):
        self.assertEqual(capture_golden.classify("check_banned", "banned term 'master-slave'"), "BANNED-TERM")
        with self.assertRaises(capture_golden.Unclassified):
            capture_golden.classify("check_template", "something the table does not know")

    def test_capture_refuses_network_error(self):
        with self.assertRaises(capture_golden.NetworkError):
            capture_golden.parse_refs_output("ch01", "OK 1\nERROR 2: timed out\n")

    def test_output_is_sorted_and_stable(self):
        g = {"b": 1, "a": {"d": 2, "c": [3]}}
        self.assertEqual(capture_golden.dumps(g), capture_golden.dumps(json.loads(capture_golden.dumps(g))))
```

- [ ] **Step 2: Run** — `python -m unittest tests.test_hashing tests.test_golden -v` → FAIL (modules missing).

- [ ] **Step 3: Implement `harness/hashing.py`**

```python
"""Receipt hashing rules (core §2.3)."""
import hashlib, json, pathlib

TEXT_SUFFIXES = {".md", ".txt", ".svg", ".py"}


def canonical_json(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def hash_bytes(data):
    return hashlib.sha256(data).hexdigest()


def hash_file(path):
    path = pathlib.Path(path)
    data = path.read_bytes()
    if path.suffix == ".json":
        return hash_bytes(canonical_json(json.loads(data.decode("utf-8"))))
    if path.suffix in TEXT_SUFFIXES:
        return hash_bytes(data.replace(b"\r\n", b"\n"))
    return hash_bytes(data)
```

- [ ] **Step 4: Implement `compare_golden.py`**

```python
"""Walk two golden JSON trees and report every difference (core §9.2)."""
import argparse, fnmatch, json, sys


def _walk(a, b, ptr, out):
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            _walk(a.get(k, _MISSING), b.get(k, _MISSING), f"{ptr}/{k}", out)
    elif isinstance(a, list) and isinstance(b, list):
        for i in range(max(len(a), len(b))):
            _walk(a[i] if i < len(a) else _MISSING, b[i] if i < len(b) else _MISSING, f"{ptr}/{i}", out)
    elif a != b:
        out.append((ptr or "/", None if a is _MISSING else a, None if b is _MISSING else b))


_MISSING = object()


def diff(a, b, allow):
    found = []
    _walk(a, b, "", found)
    diffs = []
    for ptr, before, after in found:
        rule = next((r for r in allow if fnmatch.fnmatchcase(ptr, r["pointer_glob"])), None)
        diffs.append(dict(pointer=ptr, before=before, after=after,
                          allowed=rule is not None, reason=rule["reason"] if rule else ""))
    return {"schema_version": 1, "diffs": diffs}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("a"); ap.add_argument("b")
    ap.add_argument("--allow", required=True)
    ap.add_argument("--out")
    x = ap.parse_args()
    load = lambda p: json.load(open(p, encoding="utf-8"))
    allow = load(x.allow)
    allow = allow.get("expected_diff", allow) if isinstance(allow, dict) else allow
    result = diff(load(x.a), load(x.b), allow)
    text = json.dumps(result, ensure_ascii=False, indent=1, sort_keys=True)
    if x.out:
        open(x.out, "w", encoding="utf-8", newline="\n").write(text + "\n")
    for d in result["diffs"]:
        print(("ALLOWED " if d["allowed"] else "DIFF ") + d["pointer"])
    sys.exit(0 if all(d["allowed"] for d in result["diffs"]) else 1)


if __name__ == "__main__":
    main()
```

Note `fnmatch` `*` also matches `/`; allowlist globs are written with that in mind (`/images/*/path` matches only paths ending in `/path`).

- [ ] **Step 5: Implement `capture_golden.py`** with these functions (all output via `dumps` = `json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=True) + "\n"`, written with `newline="\n"`):
  - `load_legacy_checker(layout, project)`: `importlib.util.spec_from_file_location` on `<project>/<legacy_tools>/check_book.py`; sets the module's `ROOT` to `<project>/<chapters_dir>` before use (read-only; no file writes).
  - `CLASSIFY = {function: [(regex, id), ...]}` from the table above, the `check_mcqs` phrases copied literally from `check_book.py:150-199`; `classify(fn, msg)` returns the ID or raises `Unclassified(fn, msg)`.
  - `checks_for_chapter(mod, path)`: calls each legacy function in the `check_chapter` order with the same arguments `check_chapter` uses (`check_budget(text, BUDGETS[n])`, `check_glossary(text, glossary)`); every ID the function covers gets `{"id", "target": chapter file name, "status": "pass"|"fail", "measured": {}}`; IDs with a classified failure are `fail` with `message`.
  - `book_checks(mod)`: runs `check_all()` with stdout captured, classifies each `book:` line; book IDs without a failure are `pass`.
  - `parse_refs_output(chapter, text)`: parses `OK n`, `NO DOI n`, `NOT FOUND n: …`, `TITLE MISMATCH n: …`; any `ERROR` line raises `NetworkError`.
  - `refs(project, layout)`: runs the **legacy** `verify_refs.py` as a subprocess per chapter (network) unless `--no-refs`; records `[{chapter, n, status}]` sorted by `(chapter, n)`.
  - `images(project, layout)`: every `.png/.jpg/.jpeg` under `layout["images"]` → `{path (posix, project-relative), width_px, height_px, dpi}` via Pillow (`img.info.get("dpi", (0, 0))[0]` rounded).
  - `docx_facts(path)`: with `zipfile` + `lxml`: sorted part list; paragraph count per `w:pStyle/@w:val` (`Normal` when absent); count of `a:blip`; `toc_field` = any `w:instrText` starting with ` TOC`; `core` = `docProps/core.xml` children minus `created`, `modified`, `lastModifiedBy`, `revision`; semantic hash per N5.
  - `pdf_facts(path)`: `pypdf.PdfReader`: `pages`, `bookmarks` = flattened outline titles in order.
  - `hashes`: `assembled_md` (`hash_file` of deliverables md), `docx_document` (N5), `chapters {name: hash_file}`.
  - `capture(project, layout)`: assembles golden.v1 with keys `schema_version, project, tool_sha, checks, chapters, words, references, verify_refs, images, docx, pdf, hashes, volatile_excluded`. `tool_sha` = `git log -1 --format=%H -- <legacy_tools>`. `references` per chapter: count, with DOI, without (from the legacy `references()` + DOI regexes). `volatile_excluded` lists core §9.1 fields plus the N5 exclusions.
  - `--copy-src DIR`: copies each `layout["src_copy"]` path with `shutil.copytree`/`copy2`, refusing if `DIR` already exists and differs (immutability): compare by `hash_file` per file; if identical, do nothing.

- [ ] **Step 6: Run tests** — `python -m unittest tests.test_hashing tests.test_golden -v` → PASS.

- [ ] **Step 7: Capture twice and compare bytes**

```bash
python harness/tools/capture_golden.py --project . --layout tests/fixtures/ai-in-medicine/layout-legacy.json --out tests/fixtures/ai-in-medicine/golden.json --copy-src tests/fixtures/ai-in-medicine/src
python harness/tools/capture_golden.py --project . --layout tests/fixtures/ai-in-medicine/layout-legacy.json --out "$TMP/golden2.json"
cmp tests/fixtures/ai-in-medicine/golden.json "$TMP/golden2.json"
```

Expected: both captures exit 0; `cmp` exit 0 (byte-identical). If a capture exits 2 on `ERROR`, re-run later (network); never edit the file by hand. Confirm `git status` shows no change to any tracked file outside `harness/`, `tests/` (scope lock: no tool behaviour changed; the `verify_refs` no-DOI bug is captured as-is, visible as `NO DOI` → status `no_doi` lines).

- [ ] **Step 8: Commit** — `git add harness/hashing.py harness/tools tests && git commit -m "feat(harness): golden capture/compare and frozen medical baseline (STEP 5b)"`

**STEP 5 exit:** `python harness/preflight.py` → 0; the two captures byte-identical; `python -m unittest discover -s tests -t . -v` → 0; Codex review done (protocol above).

---

## STEP 6 — Manifest-driven migration

### Task 6.1: Manifest and its validator

**Files:**
- Create: `docs/harness/migration-manifest.json`, `harness/tools/manifest.py`, `tests/test_manifest.py`, `tests/fixtures/ai-in-medicine/layout-projects.json`

**Interfaces:**
- Produces: `manifest.problems(repo: Path, m: dict, phase: "pre"|"post") -> list[str]`; CLI `python harness/tools/manifest.py --phase pre|post` exit 0 iff no problems.

Manifest content (every tracked file of the medical book; generated once by listing `git ls-files` for the paths below, then reviewed by hand):

| Source | Destination |
|---|---|
| `rework/**` (chapters, front matter, glossary, errata, `_template.md`, `REVIEW_REPORT.md`, `figures/**`, `tools/**`) | `projects/ai-in-medicine/rework/**` |
| `images/**` | `projects/ai-in-medicine/images/**` |
| `AI_in_Health_Care_Interprofessional.{md,docx,pdf}` | `projects/ai-in-medicine/deliverables/` (N3) |
| `AI_in_Medicine- Assistant Prof Dr Shereen Elkholy.{md,docx}` | `projects/ai-in-medicine/original/` |
| `convert_docx_to_md.py` | `projects/ai-in-medicine/tools/convert_docx_to_md.py` |
| `EVALUATION_RUBRIC.md`, `EVALUATION_GUIDE.md`, `Review_Notes_AI_in_Medicine.pdf`, `VERDICT.md`, `SESSION_SUMMARY.md`, `PRODUCT.md` | `projects/ai-in-medicine/history/` |
| `.claude/agents/medical-ai-reviewer.md` | `projects/ai-in-medicine/history/medical-ai-reviewer.md` (its text becomes the overlay in Task 7.4) |

Not moved: `CLAUDE.md` (reserved), `.claude/agents/academic-*.md` and `research-synthesist.md` and `.agents/skills/**` (they become shared personas in Task 7.1), `docs/**`, `.gitignore`.

`path_fix_allowlist`: the files whose hardcoded paths break after the move — `projects/ai-in-medicine/rework/tools/{check_book,build_book,assemble,verify_refs,renumber_refs}.py`, `projects/ai-in-medicine/tools/convert_docx_to_md.py`, `projects/ai-in-medicine/rework/tools/test_check_book.py`, `projects/ai-in-medicine/rework/tools/test_verify_refs.py`. Each fix is a path constant only (e.g. `ROOT … parents[2]` stays correct because the relative depth is unchanged; the root-level `OUT` becomes `ROOT / "deliverables" / …`). The actual edits are found by Step 5's grep, not guessed.

`layout-projects.json` = `layout-legacy.json` with every path prefixed by nothing (the project root is now `projects/ai-in-medicine`) and `deliverables` under `deliverables/`.

- [ ] **Step 1: Failing test**

```python
# tests/test_manifest.py
import json, pathlib, unittest
from harness.tools import manifest

REPO = pathlib.Path(__file__).resolve().parents[1]

class ManifestTest(unittest.TestCase):
    def setUp(self):
        self.m = json.load(open(REPO / "docs/harness/migration-manifest.json", encoding="utf-8"))

    def test_reserved_never_moved(self):
        self.assertFalse([e for e in self.m["moves"] if e["source"] in self.m["reserved"]])

    def test_images_beside_rework(self):
        dests = {pathlib.PurePosixPath(e["destination"]).parts[2] for e in self.m["moves"]
                 if e["source"].startswith(("images/", "rework/"))}
        self.assertEqual(dests, {"images", "rework"})

    def test_rejects_existing_destination(self):
        bad = {"moves": [{"source": "CLAUDE.md", "destination": "CLAUDE.md", "sha256": "0"}], "reserved": []}
        self.assertTrue(any("exists" in p for p in manifest.problems(REPO, bad, "pre")))
```

- [ ] **Step 2: Run** → FAIL (module/manifest missing).
- [ ] **Step 3: Implement `manifest.py`**: `pre` checks each source is tracked (`git ls-files --error-unmatch`), each destination absent, hash equals `hashing.hash_bytes(Path.read_bytes())`, no reserved path, no duplicate destination; `post` checks each destination exists with the same raw hash and each source is gone. Write the manifest (hashes computed by a one-off `python -c` over the listed files; paste the output).
- [ ] **Step 4: Run** — `python -m unittest tests.test_manifest -v` → PASS; `python harness/tools/manifest.py --phase pre` → exit 0.
- [ ] **Step 5: Commit** — `git add docs/harness/migration-manifest.json harness/tools/manifest.py tests/test_manifest.py tests/fixtures/ai-in-medicine/layout-projects.json && git commit -m "docs(harness): migration manifest (STEP 6a)"`
- [ ] **Step 6: USER APPROVAL.** Show the user the manifest table and `sha256sum docs/harness/migration-manifest.json` plus the commit SHA. On explicit approval, add a DEC row (next free number) naming both, commit it. **Do not start Task 6.2 before that DEC exists.**

### Task 6.2: Commit A — pure moves

- [ ] **Step 1:** `python harness/tools/manifest.py --phase pre` → 0.
- [ ] **Step 2:** For each entry: `git mv "<source>" "<destination>"` (a short Python loop over the manifest calling `subprocess.run(["git","mv",s,d], check=True)` after `mkdir -p` of the parent).
- [ ] **Step 3:** `python harness/tools/manifest.py --phase post` → 0.
- [ ] **Step 4:** `git commit -m "chore(migrate): move medical book into projects/ai-in-medicine (STEP 6 commit A)"`; then `git show --stat --format= HEAD | grep -v " => " | grep -v "files changed"` → empty (renames only), and `git show -M100% --name-status HEAD | cut -c1` all `R`.

### Task 6.3: Commit B — path fixes, re-capture, golden diff

- [ ] **Step 1:** `grep -rn "parents\[\|ROOT /\|\"rework\"\|AI_in_Health_Care\|images/" projects/ai-in-medicine/rework/tools projects/ai-in-medicine/tools` — list every path literal that now points to the wrong place.
- [ ] **Step 2:** Edit only those literals, only in allowlisted files.
- [ ] **Step 3:** `git diff --name-only | python -c "import json,sys; a=set(json.load(open('docs/harness/migration-manifest.json'))['path_fix_allowlist']); bad=[l.strip() for l in sys.stdin if l.strip() not in a]; print(bad); sys.exit(1 if bad else 0)"` → exit 0.
- [ ] **Step 4:** `python -m pytest projects/ai-in-medicine/rework/tools -q` → all pass (legacy tests still pytest-style; pytest 9.1.1 is installed as a dev tool, not a runtime dependency).
- [ ] **Step 5:** Re-capture and diff:

```bash
python harness/tools/capture_golden.py --project projects/ai-in-medicine --layout tests/fixtures/ai-in-medicine/layout-projects.json --out tests/fixtures/ai-in-medicine/golden-step6.json
python harness/tools/compare_golden.py tests/fixtures/ai-in-medicine/golden.json tests/fixtures/ai-in-medicine/golden-step6.json --allow docs/harness/migration-manifest.json --out "$TMP/diff.json"
```

Expected: exit 0 (every diff is in `expected_diff`). Write `docs/harness/reviews/step6-golden-diff.md`: the command, exit code, and the diff list as a table `pointer | before | after | reason`.
- [ ] **Step 6: Commit** — `git add -A projects/ai-in-medicine tests/fixtures/ai-in-medicine/golden-step6.json docs/harness/reviews/step6-golden-diff.md && git commit -m "fix(migrate): path constants only (STEP 6 commit B)"`

**STEP 6 exit:** manifest DEC exists naming SHA-256 and commit; commit A renames only; commit B touches only allowlisted files (plus the new golden and diff report, which are outside the moved tree); golden diff all allowed; Codex review done.

---

## STEP 7 — Control plane, gates everywhere, `CLAUDE.md` split

### Task 7.1: Paths, schema validator, schemas, state, rubric core, shared personas

**Files:**
- Create: `harness/paths.py`, `harness/schema.py`, `harness/state.py`, `harness/schemas/{brief,rubric,template,theme,chapter-plan,overlay,state,findings,scorecard,checker-report,source-manifest,conversion-report,figures,golden,golden-diff,units}.v1.json`, `harness/rubric_core.json`, `harness/defaults.json`, `harness/agents/{subject-reviewer,statistician,research-synthesist,psychologist,narratologist,anthropologist,historian,geographer,instructional-designer}.md`, `harness/locale/__init__.py`, `harness/locale/en.json`, `harness/presets/ltr-textbook.json`
- Test: `tests/helpers.py`, `tests/test_paths.py`, `tests/test_schema.py`, `tests/test_state.py`

**Interfaces:**
- `paths.REPO: Path` (git work tree containing `harness/`); `paths.resolve_project(arg: str, *, must_exist=True) -> Path` raising `state.GateError("PROJECT-OUTSIDE"|"PROJECT-NAME"|"PROJECT-MISSING")`.
- `schema.load_schema(name: str) -> dict` (reads `harness/schemas/<name>.v1.json`); `schema.validate(doc, sch, ptr="") -> list[str]` supporting exactly `type, required, properties, additionalProperties, items, enum, pattern, minimum, maximum, minItems, maxItems, const` plus local `$ref: "#/$defs/<name>"` (needed for recursion-free reuse; listed here as the one addition to the core §4 subset — a plan note, no semantic change).
- `state.GateError(code: str, message: str)`; `state.STAGES: list[dict]` = `[{"id","kind","after","tool_paths","approvals"}]` in graph order (core §2.1); `state.APPROVAL_SETS: dict[str, Callable[[Path], list[str]]]`; `state.mandatory_stages(brief: dict) -> list[str]`; `state.load(project) -> dict`; `state.write(project, fn: Callable[[dict], None])` (holds `state.lock`); `state.tool_sha(tool_paths) -> str` (raises `GateError("DIRTY-TOOL")`); `state.receipt_problems(project, stage_id, st) -> list[str]`; `state.require_gates(project, stage_id) -> None`; `state.begin(project, stage_id, unit=None, amend=False) -> str` (nonce); `state.complete(project, stage_id, nonce, inputs: list[str], outputs: list[str], extras: dict, args: dict) -> dict`; `state.run_auto(project, stage_id, fn)`; `state.abort(project, stage_id, reason)`; `state.approve(project, kind, dec)`; `state.import_history(project, stage_id, dec, inputs, outputs)`; `state.verify(project, through=None) -> list[str]`; `state.dec_row_hash(project, dec) -> str`.
- `locale.load_profile(tag: str) -> dict` (primary subtag → `harness/locale/<primary>.json`, then `template.locale_overrides` merged by the caller via `locale.with_overrides(profile, overrides)`).
- `tests/helpers.temp_repo(fixture: str|None, slug: str) -> ContextManager[Path]` and `helpers.run_cli(repo: Path, *args) -> CompletedProcess` (core §9.6).

Error codes (stderr line `ERROR <CODE>: <message>`, exit 1): `PROJECT-OUTSIDE`, `PROJECT-NAME`, `PROJECT-MISSING`, `NO-APPROVAL`, `APPROVAL-STALE`, `APPROVAL-SET-CHANGED`, `DEC-ROW-CHANGED`, `DEC-MISSING`, `UPSTREAM-MISSING`, `UPSTREAM-STALE`, `RUN-ACTIVE`, `NO-ACTIVE-RUN`, `NONCE-MISMATCH`, `DIRTY-TOOL`, `LOCKED`, `SCHEMA`, `NOT-MANDATORY`.

- [ ] **Step 1: Failing tests**

```python
# tests/helpers.py
import contextlib, pathlib, shutil, subprocess, sys, tempfile

REPO = pathlib.Path(__file__).resolve().parents[1]


LEGACY_TOOL_DIRS = ["projects/ai-in-medicine/rework/tools", "projects/ai-in-medicine/tools"]


@contextlib.contextmanager
def temp_repo(fixture=None, slug="fixture-book", *, stamp=False, with_legacy=False, project_from=None):
    """Core §9.6: a throwaway git repo with a committed copy of harness/ and one project under projects/.

    fixture      -- directory under tests/fixtures/ copied to projects/<slug>
    project_from -- instead, a real project path (e.g. "projects/ai-in-medicine") copied read-only
    with_legacy  -- also copy and commit the legacy tool dirs at the same relative paths
    stamp        -- recompute receipt/approval hashes, tool_sha and dec_row_sha256 inside the temp repo
    """
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        shutil.copytree(REPO / "harness", root / "harness", ignore=shutil.ignore_patterns("__pycache__"))
        (root / "projects").mkdir()
        run = lambda *a: subprocess.run(a, cwd=root, check=True, capture_output=True)
        run("git", "init", "-q")
        run("git", "config", "user.email", "t@t"); run("git", "config", "user.name", "t")
        tracked = ["harness"]
        if with_legacy:
            for d in LEGACY_TOOL_DIRS:
                shutil.copytree(REPO / d, root / d, ignore=shutil.ignore_patterns("__pycache__"))
            tracked += LEGACY_TOOL_DIRS
        run("git", "add", *tracked); run("git", "commit", "-qm", "tools")
        if project_from:
            slug = pathlib.PurePosixPath(project_from).name
            shutil.copytree(REPO / project_from, root / "projects" / slug, dirs_exist_ok=True,
                            ignore=shutil.ignore_patterns("__pycache__", "state.lock", "tools"))
        elif fixture:
            shutil.copytree(REPO / "tests" / "fixtures" / fixture, root / "projects" / slug)
        if stamp:
            stamp_project(root, root / "projects" / slug)
        yield root


def stamp_project(root, project):
    """Rewrite hashes inside state.json so a copied fixture is valid in this temp repo (test-only)."""
    import json
    sys.path.insert(0, str(root))
    from harness import hashing, state
    st = json.loads((project / "state.json").read_text(encoding="utf-8"))
    for sid, r in st["receipts"].items():
        for kind in ("inputs", "outputs"):
            r[kind] = {rel: hashing.hash_file(project / rel) for rel in r[kind]}
        r["tool_sha"] = state.tool_sha(state.BY_ID[sid]["tool_paths"], repo=root)
        if r.get("dec_id"):
            r["dec_row_sha256"] = state.dec_row_hash(project, r["dec_id"])[0]
    for a in st["approvals"].values():
        a["files"] = {rel: hashing.hash_file(project / rel) for rel in a["files"]}
        a["dec_row_sha256"] = state.dec_row_hash(project, a["dec_id"])[0]
    (project / "state.json").write_text(json.dumps(st, ensure_ascii=False, indent=1, sort_keys=True) + "\n",
                                        encoding="utf-8", newline="\n")
    sys.path.remove(str(root))


def run_cli(root, *args):
    return subprocess.run([sys.executable, "harness/run_stage.py", *args], cwd=root,
                          capture_output=True, text=True, encoding="utf-8")
```

```python
# tests/test_paths.py
import os, pathlib, unittest
from harness import paths, state
from tests.helpers import temp_repo

class ResolveProjectTest(unittest.TestCase):
    def test_resolve_project_rejects_escape(self):
        for bad in ["projects/../harness", "projects/a/b", "harness", "projects/../projects/../x"]:
            with self.assertRaises(state.GateError) as cm:
                paths.resolve_project(bad, must_exist=False)
            self.assertIn(cm.exception.code, {"PROJECT-OUTSIDE", "PROJECT-NAME"})

    def test_rejects_bad_name(self):
        with self.assertRaises(state.GateError) as cm:
            paths.resolve_project("projects/Bad_Name", must_exist=False)
        self.assertEqual(cm.exception.code, "PROJECT-NAME")

    def test_trailing_slash_ok(self):
        p = paths.resolve_project("projects/good-name/", must_exist=False)
        self.assertEqual(p.name, "good-name")

    def test_symlink_out_rejected(self):
        with temp_repo() as root:
            link = root / "projects" / "linked"
            try:
                os.symlink(root / "harness", link, target_is_directory=True)
            except OSError:
                self.skipTest("symlinks need developer mode on Windows")
            with self.assertRaises(state.GateError):
                paths.resolve_project(str(link), must_exist=True, repo=root)
```

```python
# tests/test_schema.py
import unittest
from harness import schema

S = {"type": "object", "required": ["a"], "additionalProperties": False,
     "properties": {"a": {"type": "integer", "minimum": 1}, "b": {"enum": ["x", "y"]},
                    "c": {"type": "array", "items": {"type": "string", "pattern": "^[a-z]+$"}, "maxItems": 2}}}

class SchemaTest(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(schema.validate({"a": 2, "b": "x", "c": ["ab"]}, S), [])

    def test_each_keyword_reports_pointer(self):
        errs = schema.validate({"a": 0, "b": "z", "c": ["A", "b", "c"], "d": 1}, S)
        joined = "\n".join(errs)
        for frag in ["/a", "/b", "/c/0", "/c", "/d"]:
            self.assertIn(frag, joined)

    def test_bool_is_not_integer(self):
        self.assertTrue(schema.validate({"a": True}, S))

    def test_every_shipped_schema_is_valid_subset(self):
        for name in ["brief", "rubric", "template", "theme", "chapter-plan", "overlay", "state", "findings",
                     "scorecard", "checker-report", "source-manifest", "conversion-report", "figures",
                     "golden", "golden-diff", "units"]:
            self.assertEqual(schema.unknown_keywords(schema.load_schema(name)), [], name)
```

```python
# tests/test_state.py
import json, pathlib, subprocess, unittest
from harness import state
from tests.helpers import temp_repo

class StateTest(unittest.TestCase):
    def test_graph_order_and_mandatory_sets(self):
        ids = [s["id"] for s in state.STAGES]
        self.assertEqual(ids, ["new", "intake", "ingest", "evaluate", "design", "translate", "rework", "build", "audit"])
        self.assertEqual(state.mandatory_stages({"goal": {"mode": "evaluate_only"}, "language": {"translation_required": False}}),
                         ["new", "intake", "ingest", "evaluate"])
        self.assertIn("translate", state.mandatory_stages({"goal": {"mode": "evaluate_and_rework"},
                                                           "language": {"translation_required": True}}))

    def test_required_approvals_derived_from_graph(self):
        self.assertEqual(state.required_approvals("ingest"), ["intake"])
        self.assertEqual(state.required_approvals("rework"), ["intake", "design"])
        self.assertEqual(state.required_approvals("intake"), [])

    def test_output_edit_makes_receipt_stale(self):
        with temp_repo("state-basic", stamp=True) as root:
            p = root / "projects" / "fixture-book"
            (p / "ingest" / "normalized.md").write_text("tampered\n", encoding="utf-8")
            probs = state.receipt_problems(p, "ingest", state.load(p), repo=root)
            self.assertTrue(any("output" in x for x in probs))

    def test_missing_approval_fails_not_skips(self):
        with temp_repo("state-basic", stamp=True) as root:
            p = root / "projects" / "fixture-book"
            state.write(p, lambda st: st["approvals"].pop("intake"))
            with self.assertRaises(state.GateError) as cm:
                state.require_gates(p, "evaluate", repo=root)
            self.assertEqual(cm.exception.code, "NO-APPROVAL")

    def test_dec_row_edit_makes_approval_stale(self):
        with temp_repo("state-basic", stamp=True) as root:
            p = root / "projects" / "fixture-book"
            d = p / "decisions.md"
            d.write_text(d.read_text(encoding="utf-8").replace("approve", "approve (edited)"), encoding="utf-8")
            with self.assertRaises(state.GateError) as cm:
                state.require_gates(p, "evaluate", repo=root)
            self.assertEqual(cm.exception.code, "DEC-ROW-CHANGED")

    def test_dirty_tool_refuses_receipt(self):
        with temp_repo("state-basic", stamp=True) as root:
            (root / "harness" / "state.py").write_text("# dirty\n" + (root / "harness" / "state.py").read_text(encoding="utf-8"), encoding="utf-8")
            with self.assertRaises(state.GateError) as cm:
                state.tool_sha(["harness/state.py"], repo=root)
            self.assertEqual(cm.exception.code, "DIRTY-TOOL")

    def test_leftover_lock_is_named_not_removed(self):
        with temp_repo("state-basic", stamp=True) as root:
            p = root / "projects" / "fixture-book"
            (p / "state.lock").write_text("pid=1 time=2026-09-25T00:00:00Z", encoding="utf-8")
            with self.assertRaises(state.GateError) as cm:
                state.write(p, lambda st: None)
            self.assertEqual(cm.exception.code, "LOCKED")
            self.assertIn("pid=1", str(cm.exception))
            self.assertTrue((p / "state.lock").exists())
```

`tests/fixtures/state-basic/` is a tiny valid project: brief, rubric, template, theme (each `schema_version: 1`, valid against its schema), `decisions.md` with a row `| DEC-001 | 2026-09-25 | user | approve intake | "ok" |`, `ingest/normalized.md`, and `state.json` with an intake approval and an ingest receipt. Its hashes and `tool_sha` are placeholders (`"0"`); `stamp_project` rewrites them inside the temp repo.

- [ ] **Step 2: Run** — `python -m unittest tests.test_paths tests.test_schema tests.test_state -v` → FAIL.

- [ ] **Step 3: Implement `harness/schema.py`**

```python
"""Stdlib validator for the JSON Schema subset in core §4 (plus local $ref)."""
import json, pathlib, re

SCHEMAS = pathlib.Path(__file__).resolve().parent / "schemas"
KEYWORDS = {"type", "required", "properties", "additionalProperties", "items", "enum", "pattern",
            "minimum", "maximum", "minItems", "maxItems", "const", "$ref", "$defs", "$id", "title", "description"}
TYPES = {"object": dict, "array": list, "string": str, "boolean": bool, "null": type(None)}


def load_schema(name):
    return json.loads((SCHEMAS / f"{name}.v1.json").read_text(encoding="utf-8"))


def unknown_keywords(sch, ptr=""):
    bad = [f"{ptr}/{k}" for k in sch if k not in KEYWORDS]
    for k, sub in (sch.get("properties") or {}).items():
        bad += unknown_keywords(sub, f"{ptr}/properties/{k}")
    for k, sub in (sch.get("$defs") or {}).items():
        bad += unknown_keywords(sub, f"{ptr}/$defs/{k}")
    if isinstance(sch.get("items"), dict):
        bad += unknown_keywords(sch["items"], f"{ptr}/items")
    if isinstance(sch.get("additionalProperties"), dict):
        bad += unknown_keywords(sch["additionalProperties"], f"{ptr}/additionalProperties")
    return bad


def _type_ok(value, t):
    if t == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if t == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    return isinstance(value, TYPES[t])


def validate(doc, sch, ptr="", root=None):
    root = root or sch
    if "$ref" in sch:
        sch = root["$defs"][sch["$ref"].rsplit("/", 1)[1]]
    errs = []
    loc = ptr or "/"
    if "type" in sch:
        types = sch["type"] if isinstance(sch["type"], list) else [sch["type"]]
        if not any(_type_ok(doc, t) for t in types):
            return [f"{loc}: expected {'|'.join(types)}"]
    if "const" in sch and doc != sch["const"]:
        errs.append(f"{loc}: must equal {sch['const']!r}")
    if "enum" in sch and doc not in sch["enum"]:
        errs.append(f"{loc}: {doc!r} not in {sch['enum']}")
    if isinstance(doc, str) and "pattern" in sch and not re.search(sch["pattern"], doc):
        errs.append(f"{loc}: does not match {sch['pattern']}")
    if isinstance(doc, (int, float)) and not isinstance(doc, bool):
        if "minimum" in sch and doc < sch["minimum"]:
            errs.append(f"{loc}: below minimum {sch['minimum']}")
        if "maximum" in sch and doc > sch["maximum"]:
            errs.append(f"{loc}: above maximum {sch['maximum']}")
    if isinstance(doc, list):
        if "minItems" in sch and len(doc) < sch["minItems"]:
            errs.append(f"{loc}: fewer than {sch['minItems']} items")
        if "maxItems" in sch and len(doc) > sch["maxItems"]:
            errs.append(f"{loc}: more than {sch['maxItems']} items")
        if isinstance(sch.get("items"), dict):
            for i, item in enumerate(doc):
                errs += validate(item, sch["items"], f"{ptr}/{i}", root)
    if isinstance(doc, dict):
        for k in sch.get("required", []):
            if k not in doc:
                errs.append(f"{ptr}/{k}: required")
        props = sch.get("properties", {})
        for k, v in doc.items():
            if k in props:
                errs += validate(v, props[k], f"{ptr}/{k}", root)
            elif sch.get("additionalProperties") is False:
                errs.append(f"{ptr}/{k}: not allowed")
            elif isinstance(sch.get("additionalProperties"), dict):
                errs += validate(v, sch["additionalProperties"], f"{ptr}/{k}", root)
    return errs
```

- [ ] **Step 4: Implement `harness/paths.py`**

```python
"""Repository root and project selection (core §1.1)."""
import pathlib, re, subprocess

NAME = re.compile(r"^[a-z0-9][a-z0-9-]{1,62}$")


def repo_root(start=None):
    here = pathlib.Path(start or __file__).resolve()
    out = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=here if here.is_dir() else here.parent,
                         capture_output=True, text=True)
    return pathlib.Path(out.stdout.strip()).resolve()


REPO = repo_root()


def resolve_project(arg, *, must_exist=True, repo=None):
    from harness.state import GateError  # ponytail: late import avoids a cycle; state owns the error type
    repo = pathlib.Path(repo or REPO).resolve()
    raw = pathlib.Path(arg)
    path = (raw if raw.is_absolute() else repo / raw).resolve()
    if path.parent != repo / "projects":
        raise GateError("PROJECT-OUTSIDE", f"{arg} resolves to {path}, not a direct child of {repo / 'projects'}")
    if not NAME.match(path.name):
        raise GateError("PROJECT-NAME", f"project name {path.name!r} must match {NAME.pattern}")
    if must_exist and not path.is_dir():
        raise GateError("PROJECT-MISSING", f"{path} does not exist")
    return path
```

`Path.resolve()` follows symlinks, so a link under `projects/` pointing elsewhere fails `PROJECT-OUTSIDE`.

- [ ] **Step 5: Implement `harness/state.py`** — the full module. Key parts, verbatim:

```python
"""Receipts, approvals, gates, lease (core §2.3, §3)."""
import datetime, json, os, pathlib, re, secrets, subprocess
from harness import hashing, paths, schema

CONTROL_PLANE = {"state.json", "state.lock", "decisions.md"}


class GateError(Exception):
    def __init__(self, code, message):
        super().__init__(f"{code}: {message}")
        self.code = code


STAGES = [
    {"id": "new", "kind": "auto", "tool_paths": ["harness/state.py", "harness/stages/new.py"]},
    {"id": "intake", "kind": "agentic", "tool_paths": ["harness/state.py", "harness/schema.py", "harness/schemas", "harness/stages/complete_checks.py"]},
    {"id": "ingest", "kind": "auto", "tool_paths": ["harness/stages/ingest.py", "harness/tools/convert_docx.py"]},
    {"id": "evaluate", "kind": "agentic", "tool_paths": ["harness/stages/complete_checks.py", "harness/tools/check_book.py"]},
    {"id": "design", "kind": "agentic", "tool_paths": ["harness/stages/complete_checks.py"]},
    {"id": "translate", "kind": "agentic", "tool_paths": ["harness/tools/check_translation.py"]},
    {"id": "rework", "kind": "agentic", "tool_paths": ["harness/tools/check_book.py", "harness/tools/verify_refs.py"]},
    {"id": "build", "kind": "auto", "tool_paths": ["harness/stages/build.py", "harness/tools/build_book.py", "harness/tools/assemble.py", "harness/figures"]},
    {"id": "audit", "kind": "agentic", "tool_paths": ["harness/stages/complete_checks.py"]},
]
ORDER = [s["id"] for s in STAGES]
BY_ID = {s["id"]: s for s in STAGES}
DESIGN_GATED_FROM = "translate"


def required_approvals(stage_id):
    i = ORDER.index(stage_id)
    if i <= ORDER.index("intake"):
        return []
    return ["intake"] + (["design"] if i >= ORDER.index(DESIGN_GATED_FROM) else [])


def _translation_applies(project):
    brief = _read_json(project / "brief.json") or {}
    return brief.get("language", {}).get("translation_required") is True


APPROVAL_SETS = {
    "intake": lambda p: ["brief.json", "rubric.json", "template.json", "theme.json"]
                        + sorted(f"agents/{f.name}" for f in (p / "agents").glob("*.json")),
    "design": lambda p: ["design/design.md", "design/chapter-plan.json", "design/errata-seed.md"]
                        + (["termbase.json"] if _translation_applies(p) else []),
}


def mandatory_stages(brief):
    if brief["goal"]["mode"] == "evaluate_only":
        return ["new", "intake", "ingest", "evaluate"]
    base = ["new", "intake", "ingest", "evaluate", "design", "rework", "build", "audit"]
    if brief["language"]["translation_required"]:
        base.insert(base.index("rework"), "translate")
    return base


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _read_json(path):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def load(project):
    st = _read_json(project / "state.json")
    if st is None:
        raise GateError("PROJECT-MISSING", f"{project / 'state.json'} missing; run `new` first")
    errs = schema.validate(st, schema.load_schema("state"))
    if errs:
        raise GateError("SCHEMA", "state.json: " + "; ".join(errs))
    return st


def write(project, mutate):
    lock = project / "state.lock"
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        raise GateError("LOCKED", f"{lock} exists ({lock.read_text(encoding='utf-8', errors='replace').strip()}); "
                                  "another process holds it or crashed; remove it by hand after checking")
    try:
        os.write(fd, f"pid={os.getpid()} time={now()}".encode())
        os.close(fd)
        st = load(project)
        mutate(st)
        tmp = project / "state.json.tmp"
        tmp.write_text(json.dumps(st, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
        os.replace(tmp, project / "state.json")
        return st
    finally:
        lock.unlink(missing_ok=True)


def tool_sha(tool_paths, repo=None):
    repo = repo or paths.REPO
    dirty = subprocess.run(["git", "status", "--porcelain", "--", *tool_paths], cwd=repo, capture_output=True, text=True).stdout
    if dirty.strip():
        raise GateError("DIRTY-TOOL", f"uncommitted changes in {', '.join(tool_paths)}:\n{dirty}")
    return subprocess.run(["git", "log", "-1", "--format=%H", "--", *tool_paths], cwd=repo,
                          capture_output=True, text=True).stdout.strip()


def hash_map(project, rels):
    out = {}
    for rel in rels:
        if pathlib.PurePosixPath(rel).name in CONTROL_PLANE:
            continue
        out[rel] = hashing.hash_file(project / rel)
    return out


def dec_row_hash(project, dec):
    text = (project / "decisions.md").read_text(encoding="utf-8").replace("\r\n", "\n")
    rows = [l.rstrip() for l in text.split("\n") if l.startswith(f"| {dec} |")]
    if len(rows) != 1:
        raise GateError("DEC-MISSING", f"{dec}: expected exactly one row in decisions.md, found {len(rows)}")
    return hashing.hash_bytes(rows[0].encode("utf-8")), rows[0]


def receipt_problems(project, stage_id, st, repo=None):
    r = st["receipts"].get(stage_id)
    if r is None:
        return [f"{stage_id}: no receipt"]
    probs = []
    if r["status"] != "ok":
        probs.append(f"{stage_id}: status {r['status']}")
    if r.get("invalidated_by"):
        probs.append(f"{stage_id}: invalidated by {r['invalidated_by']}")
    for kind in ("inputs", "outputs"):
        for rel, h in r[kind].items():
            f = project / rel
            if not f.exists():
                probs.append(f"{stage_id}: {kind[:-1]} missing {rel}")
            elif hashing.hash_file(f) != h:
                probs.append(f"{stage_id}: {kind[:-1]} changed {rel}")
    try:
        if tool_sha(BY_ID[stage_id]["tool_paths"], repo) != r["tool_sha"]:
            probs.append(f"{stage_id}: tool changed since receipt")
    except GateError as e:
        probs.append(f"{stage_id}: {e}")
    return probs


def approval_problems(project, kind, st):
    a = st["approvals"].get(kind)
    if a is None:
        return [("NO-APPROVAL", f"{kind} approval missing")]
    probs = []
    expected = sorted(APPROVAL_SETS[kind](project))
    if sorted(a["files"]) != expected:
        probs.append(("APPROVAL-SET-CHANGED", f"{kind} approval covers {sorted(a['files'])}, current set is {expected}"))
    for rel, h in a["files"].items():
        f = project / rel
        if not f.exists() or hashing.hash_file(f) != h:
            probs.append(("APPROVAL-STALE", f"{kind} approval: {rel} changed or missing; the user must re-approve"))
    try:
        if dec_row_hash(project, a["dec_id"])[0] != a["dec_row_sha256"]:
            probs.append(("DEC-ROW-CHANGED", f"{a['dec_id']} row in decisions.md changed after approval"))
    except GateError as e:
        probs.append((e.code, str(e)))
    return probs


def upstream(stage_id, brief):
    mand = mandatory_stages(brief) if brief else ORDER[: ORDER.index("intake") + 1]
    return [s for s in ORDER[: ORDER.index(stage_id)] if s in mand]


def require_gates(project, stage_id, repo=None):
    st = load(project)
    for kind in required_approvals(stage_id):
        probs = approval_problems(project, kind, st)
        if probs:
            raise GateError(probs[0][0], "; ".join(m for _, m in probs))
    brief = _read_json(project / "brief.json")
    for up in upstream(stage_id, brief):
        if up not in st["receipts"]:
            raise GateError("UPSTREAM-MISSING", f"{stage_id} needs a valid {up} receipt; none exists")
        probs = receipt_problems(project, up, st, repo)
        if probs:
            raise GateError("UPSTREAM-STALE", "; ".join(probs))
    return st
```

The rest of `state.py` (same file) implements, with these exact behaviours:
- `invalidate_downstream(st, stage_id)`: for every receipt of a stage after `stage_id` in `ORDER`, set `invalidated_by = f"{stage_id}@{now()}"`.
- `begin(project, stage_id, unit=None, amend=False)`: `require_gates`; refuses `RUN-ACTIVE` if `active_run` set (message names stage, unit, started_at); refuses `NOT-MANDATORY` if the stage is not in `mandatory_stages(brief)` (brief absent → only `new`/`intake` allowed); `amend` allowed only for `intake`; sets `active_run`, invalidates downstream unless `amend`; returns nonce `secrets.token_hex(8)`.
- `complete(project, stage_id, nonce, inputs, outputs, extras, args)`: `require_gates` again; `NO-ACTIVE-RUN` / `NONCE-MISMATCH` checks; computes `tool_sha` (may raise `DIRTY-TOOL`); writes receipt `{stage, status: "ok", args, inputs: hash_map, outputs: hash_map, tool_sha, time, **extras}`; unit receipts go to `receipts[stage]["units"][unit]` and do not clear the lease unless `extras.get("final")`; clears `active_run` on stage completion.
- `run_auto(project, stage_id, fn)`: `begin` + `fn(project) -> (inputs, outputs, extras)` + complete; on exception writes `{status: "failed", error: str(e)}` and clears the lease, then re-raises.
- `abort(project, stage_id, reason)`: requires `active_run.stage == stage_id`; appends `{stage, nonce, reason, time}` to `aborts`; clears lease.
- `approve(project, kind, dec)`: `dec_row_hash` must succeed and the row must contain `kind` (case-insensitive) — else `DEC-MISSING`; writes `{kind, files: hash_map(APPROVAL_SETS[kind]), dec_id, dec_row_sha256, approved_at, approved_by: "user"}`. For `design` also `require_gates(project, "design")` must pass except for the design approval itself.
- `import_history(project, stage_id, dec, inputs, outputs)`: allowed stages `{"ingest","evaluate","design","rework"}`; DEC row must contain `import-history` and `stage_id`; writes receipt with `imported: true`, `dec_id`, `dec_row_sha256`.
- `verify(project, through=None)`: returns a list of failure lines: `require_gates(project, next stage after through or last mandatory)` errors, every mandatory receipt up to the boundary via `receipt_problems`, `active_run` if set; prints `imported` receipts as info, not failure.

Write `harness/schemas/state.v1.json` to match exactly (receipt object with `additionalProperties: true` for stage extras; approvals `additionalProperties: false`).

- [ ] **Step 6: Write the other schemas** — one file each, fields exactly as core §4.1–§4.5, §6, §7.1, §8, §9, `additionalProperties: false` at every object level except receipt extras. Every document requires `"schema_version": {"const": 1}`. `brief.v1.json` enforces `answers` with all 13 letters as `required`. `rubric.v1.json` enforces `pillars` items `{id, kind, name, description, weight, anchors, hard_caps, reviewer_ids, applicable}` and `hard_caps` items `{trigger: {severity, min_count, tag}, max_score, description}`. Numeric cross-constraints (weights sum to 100, 1–4 domain pillars of 5–40 summing to 40) are code in `harness/stages/complete_checks.py` (Task 7.2), not schema.

- [ ] **Step 7: `rubric_core.json`, `defaults.json`, `locale/en.json`, `presets/ltr-textbook.json`**
  - `rubric_core.json`: `{"schema_version":1,"core_version":1,"pillars":[G1 20, G2 20, G3 10, G4 10]}` with names, `owns` text and anchors copied from core §5.1 and the four-band anchor scheme of core §4.2.
  - `defaults.json`: `{"schema_version":1,"references":{"providers":{"crossref":{"endpoint":"https://api.crossref.org/works/","user_agent":"rework-verify/1.0","retries":5,"timeout_s":15,"backoff_s":3}}}}` (values from `verify_refs.py:27-40`).
  - `locale/en.json`: `tag: en`, `script: Latn`, `direction: ltr`, `normalisation.compare: ["NFC","casefold"]`, `normalisation.count: ["NFC"]`, `tokenizer: {"kind":"ascii-word","pattern":"[A-Za-z0-9][A-Za-z0-9'’\\-–./%]*"}` (today's `check_book.py:23`), `sentence_terminators: [".","!","?"]`, `discouraged_objective_verbs: ["understand"]`, `banned_terms: []` (the medical banned term becomes template data in Task 7.4), `readability: {mean_sentence_max: 16, long_sentence_words: <from check_book.py:15-16>, long_share_max: <same>}`, `chapter_heading_pattern: "^# Chapter (?P<num>\\d+): (?P<title>.+)$"`, `figure_caption_pattern: "Figure {chapter}.{n}"`, `default_labels` (`Contents`, `Chapter`, `Part`, `Glossary`, `Figure`, `Table`, `Q`, `LO`, the section-role defaults `Learning Objectives`, `References`, `Self-Assessment`, `Answers and Rationales`, `How to Use This Book`, …), `digits: {"accepted":["western"],"output":"western"}`.
  - `presets/ltr-textbook.json`: fonts, page, palette defaults = today's `build_book.py:30-32, 569-573` values; `title_page_layout`; `required_font_files: ["Sitka.ttc","segoeui.ttf"]`. `preflight.FONT_FILES` is replaced by the union of `required_font_files` over presets (edit preflight in this task; its test still passes).

- [ ] **Step 8: Shared personas** — `harness/agents/*.md`: copy each `.claude/agents/academic-*.md` / `research-synthesist.md` body, strip domain wording, rename to the core §6 IDs (`subject-reviewer` is written new from the generic parts of `projects/ai-in-medicine/history/medical-ai-reviewer.md`; `instructional-designer` is written new: objectives, progression, cognitive load, assessment alignment). `git rm` the moved `.claude/agents/academic-*.md` and `research-synthesist.md` and `.agents/skills/**` only after the new files exist (they are superseded; the ledger records it).

- [ ] **Step 9: Run** — `python -m unittest tests.test_paths tests.test_schema tests.test_state -v` → PASS; `python harness/tools/leak_scan.py` does not exist yet (Task 8.1), so run `grep -rniE "medic|clinic|patient|pharmac|physio|elkholy|shereen" harness/` → no output.
- [ ] **Step 10: Commit** — `git add -A harness tests .claude/agents .agents && git commit -m "feat(harness): state, schemas, validator, rubric core, shared personas (STEP 7 task 1)"`

### Task 7.2: Runner, completion checks and skills

**Files:**
- Create: `harness/run_stage.py`, `harness/stages/__init__.py`, `harness/stages/new.py`, `harness/stages/complete_checks.py`, `.claude/skills/book-{new,intake,ingest,evaluate,design,translate,rework,build,audit,verify}/SKILL.md`
- Test: `tests/test_run_stage.py`, `tests/test_complete_checks.py`

**Interfaces:**
- CLI: `python harness/run_stage.py --project P <command>`; commands `new`, `init-state` (Task 7.4), `begin STAGE [--unit U] [--amend]`, `complete STAGE --nonce N [--unit U]`, `run STAGE`, `abort STAGE --reason TEXT`, `approve intake|design --dec DEC-NNN`, `import-history STAGE --dec DEC-NNN`, `terms resolve --dec DEC-NNN` (Task 11.2), `verify [--through STAGE]`. Exit 0 ok; 1 `GateError` or check failure (stderr `ERROR <CODE>: …`, one line per problem); 2 usage error or ingest `lost`.
- `complete_checks.CHECKS: dict[str, Callable[[Path], tuple[list[str], list[str], dict, list[str]]]]` returning `(inputs, outputs, extras, problems)` per agentic stage; `complete_checks.intake(project)`, `.evaluate(project)`, `.design(project)`, `.audit(project)`; `complete_checks.score(rubric, scorecard, findings, fixes) -> list[str]` (core §5.4); `complete_checks.fixes_rows(path) -> dict[str, str]` (finding ID → status) for the Fix Protocol table.
- `new.run(project_arg) -> None`: creates `projects/<slug>/` with `agents/`, `source/`, `ingest/`, `evaluation/`, `design/`, `figures/src/`, `build/`, `audit/`, empty `decisions.md` (header row `| DEC | Date | Kind | Decision | User words |`), and `state.json` `{schema_version:1, project_id, receipts:{}, approvals:{}, active_run:null, aborts:[]}`; receipt `new` with `args: {slug}`, outputs = the directory markers (`.keep` files) and `decisions.md` excluded (control plane). On failure removes only what it created.

`complete_checks.intake` enforces: all five kinds validate; core §4.6 rules 1–8 (rule 2/3 by primary subtag via `locale.primary(tag)`); `TR-PAIR-UNSUPPORTED` when subtags differ and the pair is not `en-ar`/`ar-en` (message names the pair); rubric §5.2 (four fixed pillars with core weights, G3→G2 reallocation only when MCQs, cases and exercises are all disabled, 1–4 domain pillars each 5–40 summing to 40, total 100, unique IDs, ≥1 reviewer each); `brief.unresolved == []`. `evaluate`/`audit` enforce `findings.v1`, one pillar per finding, `score()` (weighted total, cap triggers vs `caps_applied`), `rubric_digest` equality (audit vs evaluate receipt), and the fixes gate: every blocker/major Codex finding has a row with status `fixed + verified`, `rejected` or `ruled by user`. `audit` also refuses `CHEM-UNVERIFIED` without a `ruled by user` row (core §7.5) and `TB-PROPOSAL-OPEN` (TR §3.3). `design` enforces `chapter-plan.v1`, budget sum within `template.budgets.total`, every evaluate blocker/major mapped to a chapter or `out-of-scope` with reason.

- [ ] **Step 1: Failing tests**

```python
# tests/test_run_stage.py
import json, unittest
from tests.helpers import temp_repo, run_cli

class RunnerTest(unittest.TestCase):
    def test_new_then_verify_through_new(self):
        with temp_repo() as root:
            r = run_cli(root, "--project", "projects/book-one", "new")
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual(run_cli(root, "--project", "projects/book-one", "verify", "--through", "new").returncode, 0)

    def test_begin_ingest_without_intake_approval(self):
        with temp_repo() as root:
            run_cli(root, "--project", "projects/book-one", "new")
            r = run_cli(root, "--project", "projects/book-one", "run", "ingest")
            self.assertEqual(r.returncode, 1)
            self.assertIn("ERROR NO-APPROVAL", r.stderr)

    def test_crashed_run_needs_abort(self):
        with temp_repo("state-basic", stamp=True) as root:
            p = ["--project", "projects/fixture-book"]
            r = run_cli(root, *p, "begin", "evaluate")
            self.assertEqual(r.returncode, 0, r.stderr)
            r2 = run_cli(root, *p, "begin", "evaluate")
            self.assertEqual(r2.returncode, 1)
            self.assertIn("ERROR RUN-ACTIVE", r2.stderr)
            self.assertIn("evaluate", r2.stderr)
            self.assertEqual(run_cli(root, *p, "abort", "evaluate", "--reason", "crash test").returncode, 0)
            self.assertEqual(run_cli(root, *p, "begin", "evaluate").returncode, 0)

    def test_complete_needs_matching_nonce(self):
        with temp_repo("state-basic", stamp=True) as root:
            p = ["--project", "projects/fixture-book"]
            run_cli(root, *p, "begin", "evaluate")
            r = run_cli(root, *p, "complete", "evaluate", "--nonce", "0000")
            self.assertIn("ERROR NONCE-MISMATCH", r.stderr)

    def test_approve_needs_dec_row(self):
        with temp_repo("state-basic", stamp=True) as root:
            r = run_cli(root, "--project", "projects/fixture-book", "approve", "intake", "--dec", "DEC-999")
            self.assertIn("ERROR DEC-MISSING", r.stderr)
```

```python
# tests/test_complete_checks.py
import unittest
from harness.stages import complete_checks as cc

def rubric(domain):
    fixed = [dict(id=i, kind="fixed", weight=w, reviewer_ids=["r"], applicable=True, hard_caps=[])
             for i, w in (("G1", 20), ("G2", 20), ("G3", 10), ("G4", 10))]
    return {"pillars": fixed + [dict(id=f"D{n}", kind="domain", weight=w, reviewer_ids=["r"], applicable=True, hard_caps=[])
                                 for n, w in enumerate(domain)]}

class RubricRulesTest(unittest.TestCase):
    def test_single_domain_pillar_of_40_is_valid(self):
        self.assertEqual(cc.rubric_problems(rubric([40]), assessment_enabled=True), [])

    def test_five_domain_pillars_rejected(self):
        self.assertTrue(cc.rubric_problems(rubric([8, 8, 8, 8, 8]), assessment_enabled=True))

    def test_g3_moves_to_g2_only_when_all_assessment_disabled(self):
        r = rubric([40]); r["pillars"][2]["applicable"] = False; r["pillars"][1]["weight"] = 30
        self.assertEqual(cc.rubric_problems(r, assessment_enabled=False), [])
        self.assertTrue(cc.rubric_problems(r, assessment_enabled=True))

class ScoreTest(unittest.TestCase):
    def test_total_computed_and_cap_enforced(self):
        rub = rubric([40]); rub["pillars"][0]["hard_caps"] = [
            {"trigger": {"severity": "blocker", "min_count": 1, "tag": None}, "max_score": 4, "description": "x"}]
        findings = [{"id": "F-001", "pillar_id": "G1", "severity": "blocker", "tags": []}]
        card = {"pillars": [{"id": p["id"], "score": 8, "applicable": True} for p in rub["pillars"]],
                "caps_applied": [], "total": 80.0}
        probs = cc.score(rub, card, findings, fixes={})
        self.assertTrue(any("cap" in p for p in probs))
        card["pillars"][0]["score"] = 4
        card["caps_applied"] = [{"pillar_id": "G1", "cap_index": 0, "finding_ids": ["F-001"]}]
        card["total"] = round((4 * 20 + 8 * 20 + 8 * 10 + 8 * 10 + 8 * 40) / 10, 1)
        self.assertEqual(cc.score(rub, card, findings, fixes={}), [])

    def test_fixed_finding_does_not_trigger_cap(self):
        rub = rubric([40]); rub["pillars"][0]["hard_caps"] = [
            {"trigger": {"severity": "blocker", "min_count": 1, "tag": None}, "max_score": 4, "description": "x"}]
        findings = [{"id": "F-001", "pillar_id": "G1", "severity": "blocker", "tags": []}]
        card = {"pillars": [{"id": p["id"], "score": 8, "applicable": True} for p in rub["pillars"]],
                "caps_applied": [], "total": 80.0}
        self.assertEqual(cc.score(rub, card, findings, fixes={"F-001": "fixed + verified"}), [])
```

- [ ] **Step 2: Run** → FAIL.
- [ ] **Step 3: Implement** `run_stage.py` (argparse subcommands; every command resolves `--project` via `paths.resolve_project(..., must_exist=command != "new")`; catches `GateError` → `print(f"ERROR {e.code}: {e}", file=sys.stderr); sys.exit(1)`), `new.py`, `complete_checks.py` (functions above; `rubric_problems(rubric, assessment_enabled)`; `score(...)` computes `round(sum(score*weight)/10, 1)` over applicable pillars; `fixes_rows` parses the Markdown table in `fixes.md` by header names `ID` and `real/rejected` + the status column `fix`/`status`).
- [ ] **Step 4: Skills** — each `SKILL.md` is ≤ 30 lines: `name: book-<stage>`, description "Run the <stage> stage of the book harness through run_stage.py", body: the exact `run_stage.py` commands, the gate reminder (Rule 7: never edit `state.json`; approvals only after explicit user approval in chat with a DEC row), and for agentic stages the task brief the runner prints at `begin`. `book-intake` includes the questionnaire A–M from `docs/harness/INTAKE_QUESTIONNAIRE.md` by reference.
- [ ] **Step 5: Run** — `python -m unittest tests.test_run_stage tests.test_complete_checks -v` → PASS.
- [ ] **Step 6: Commit** — `git add -A harness .claude/skills tests && git commit -m "feat(harness): stage runner, completion checks, book-* skills (STEP 7 task 2)"`

### Task 7.3: Legacy gate shims and the bypass matrix

**Files:**
- Modify: `projects/ai-in-medicine/rework/tools/{check_book,build_book,assemble,verify_refs,renumber_refs}.py`, `projects/ai-in-medicine/tools/convert_docx_to_md.py` — top of `main()` / module entry only
- Create: `harness/gate.py`
- Test: `tests/test_bypass_matrix.py`, `tests/fixtures/bypass/` (a minimal gated project with intake + design approvals and receipts through `rework`)

**Interfaces:**
- `gate.enforce(stage_id: str, argv: list[str]) -> Path`: parses and removes `--project P` from `argv`, resolves it, calls `state.require_gates(project, stage_id)`, prints `ERROR <CODE>: …` and `sys.exit(1)` on failure, returns the project path. Missing `--project` → `ERROR PROJECT-REQUIRED` exit 1.
- Legacy tool change (each file, N4 mapping), inserted as the first statements of the script body:

```python
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4]))  # repo root; depth fixed by the manifest layout
from harness.gate import enforce
PROJECT = enforce("rework", sys.argv)  # stage per N4
```

(`parents[4]` for `projects/ai-in-medicine/rework/tools/x.py`; `parents[3]` for `projects/ai-in-medicine/tools/convert_docx_to_md.py`.) The tools' internal `ROOT` logic is unchanged (scope lock: no internals generalised).

Executable inventory (the matrix enumerates it from this list, and a guard test asserts the list equals every `*.py` with a `__main__` block under `harness/` and `projects/*/**/tools/` excluding tests): `harness/run_stage.py` (per stage command), `harness/tools/*.py` that take `--project` (from STEP 8 on they join automatically), and the six legacy tools.

Cases per executable (core/TICKET STEP 7 exit):

| Case | Setup in the temp repo | Expected |
|---|---|---|
| no approval | delete `approvals.intake` | exit ≠ 0, `ERROR NO-APPROVAL` |
| edit after approval | append a space to `brief.json`'s `identity.title` | `ERROR APPROVAL-STALE` |
| stale upstream receipt | edit `ingest/normalized.md` | `ERROR UPSTREAM-STALE` |
| missing design approval before rework | delete `approvals.design` | `ERROR NO-APPROVAL` for rework/build-gated tools; ingest-gated tools unaffected (they are asserted to pass this case) |
| path outside `projects/` | `--project harness` | `ERROR PROJECT-OUTSIDE` |

- [ ] **Step 1: Failing test**

```python
# tests/test_bypass_matrix.py
import json, pathlib, re, subprocess, sys, unittest
from tests.helpers import temp_repo, REPO

LEGACY = {  # N4
    "projects/ai-in-medicine/rework/tools/check_book.py": "rework",
    "projects/ai-in-medicine/rework/tools/verify_refs.py": "rework",
    "projects/ai-in-medicine/rework/tools/renumber_refs.py": "rework",
    "projects/ai-in-medicine/rework/tools/assemble.py": "rework",
    "projects/ai-in-medicine/rework/tools/build_book.py": "build",
    "projects/ai-in-medicine/tools/convert_docx_to_md.py": "ingest",
}
RUNNER = {"run ingest": "ingest", "begin evaluate": "evaluate", "begin design": "design",
          "begin rework": "rework", "run build": "build", "begin audit": "audit"}


def mutate(p, case):
    st = json.loads((p / "state.json").read_text(encoding="utf-8"))
    if case == "no-approval":
        st["approvals"].pop("intake")
    elif case == "no-design":
        st["approvals"].pop("design")
    (p / "state.json").write_text(json.dumps(st), encoding="utf-8")
    if case == "edit-after-approval":
        b = json.loads((p / "brief.json").read_text(encoding="utf-8"))
        b["identity"]["title"] += " "
        (p / "brief.json").write_text(json.dumps(b), encoding="utf-8")
    if case == "stale-upstream":
        (p / "ingest" / "normalized.md").write_text("tampered\n", encoding="utf-8")


EXPECT = {"no-approval": "NO-APPROVAL", "edit-after-approval": "APPROVAL-STALE",
          "stale-upstream": "UPSTREAM-STALE", "no-design": "NO-APPROVAL", "outside": "PROJECT-OUTSIDE"}


class BypassMatrix(unittest.TestCase):
    def _cmds(self, root):
        for tool, stage in LEGACY.items():
            yield f"{tool}", stage, lambda proj, t=tool: [sys.executable, t, "--project", proj]
        for cmd, stage in RUNNER.items():
            yield f"run_stage {cmd}", stage, lambda proj, c=cmd: [sys.executable, "harness/run_stage.py", "--project", proj, *c.split()]

    def test_matrix(self):
        for case, code in EXPECT.items():
            with temp_repo("bypass", slug="bypass-book", stamp=True, with_legacy=True) as root:
                p = root / "projects" / "bypass-book"
                if case != "outside":
                    mutate(p, case)
                for name, stage, argv in self._cmds(root):
                    if case == "no-design" and stage in ("ingest", "evaluate", "design"):
                        continue
                    if case == "stale-upstream" and stage == "ingest":
                        continue  # ingest has no upstream receipt to go stale
                    with self.subTest(case=case, exe=name):
                        proj = "harness" if case == "outside" else "projects/bypass-book"
                        r = subprocess.run(argv(proj), cwd=root, capture_output=True, text=True, encoding="utf-8")
                        self.assertNotEqual(r.returncode, 0, r.stdout)
                        self.assertIn(f"ERROR {code}", r.stderr)

    def test_inventory_is_complete(self):
        mains = {str(p.relative_to(REPO)).replace("\\", "/") for p in REPO.glob("projects/*/**/tools/*.py")
                 if "__main__" in p.read_text(encoding="utf-8") and not p.name.startswith("test_")}
        self.assertEqual(mains, set(LEGACY))
```

`temp_repo(..., with_legacy=True)` (defined in Task 7.1) copies and commits the legacy tool dirs at the same relative paths, so `parents[4]` resolves to the temp root.

- [ ] **Step 2: Run** — `python -m unittest tests.test_bypass_matrix -v` → FAIL (legacy tools do not gate).
- [ ] **Step 3: Implement `harness/gate.py`** and insert the shim lines into the six tools.
- [ ] **Step 4: Run** → PASS. Also `python -m pytest projects/ai-in-medicine/rework/tools -q` — the legacy tests call the tools without `--project`; update them to pass `--project projects/ai-in-medicine` **only after** Task 7.4 approvals exist; until then mark this command expected-fail and record it in the task commit message.
- [ ] **Step 5: Commit** — `git add harness/gate.py projects/ai-in-medicine/rework/tools projects/ai-in-medicine/tools tests && git commit -m "feat(harness): gate every legacy tool; bypass matrix (STEP 7 task 3)"`

### Task 7.4: Medical project onboarding (USER APPROVAL)

**Files:**
- Create: `projects/ai-in-medicine/{brief,rubric,template,theme}.json`, `projects/ai-in-medicine/agents/clinical-accuracy.json` (overlay from `history/medical-ai-reviewer.md`), `projects/ai-in-medicine/design/{design.md,chapter-plan.json,errata-seed.md}`, `projects/ai-in-medicine/decisions.md`, `projects/ai-in-medicine/state.json`
- Modify: `harness/run_stage.py`, `harness/stages/new.py` — add `init-state` (the project directory already exists, so `new` refuses): `run_stage.py --project P init-state` refuses if `state.json` exists, otherwise writes the empty state and a `new` receipt with `args: {slug, adopted: true}`; test `tests/test_run_stage.py::test_init_state_refuses_existing`
- Test: `tests/test_medical_config.py`

**Content rules (reproduce old hardcoded behaviour, INV mapping core §10):**
- `template.json`: sections/callouts/perspectives labels from `check_book.py:18-22`; budgets `total {17000, 21000}`, `front_matter 500`; readability from `check_book.py:14-17`; LO `id_pattern "^LO\\d+$"`, `min 3`, `max 5`, `discouraged_verbs ["understand"]`; MCQ `count 10`, `option_labels ["A","B","C","D"]`, `key_balance {2,3}`, `max_run 2`; citations numeric-bracket; references `no_doi_policy` = today's effective behaviour (the no-DOI bug is recorded in STEP 5 golden and fixed in STEP 8 Task 8.3, not here); `banned_terms` from `check_book.py:252-253`; errata open value `open`; glossary `minimum_terms 120`, `term_syntax bold`, `excluded_callout_ids [<the perspective callout id>]`; `paths.chapters "rework"`, `chapter_glob "ch*.md"`, `allowed_asset_roots ["images","rework/figures"]`.
- `theme.json`: preset `ltr-textbook`, `lang_tag en-GB`, fonts/palette/page/callout colours/boxed and TOC-excluded sections from `build_book.py:30-51, 204-237, 569-573`; `title_page.notices` = the fictional-patient notice text; `output.basename "AI_in_Health_Care_Interprofessional"`.
- `brief.json`: A–M answered from `history/SESSION_SUMMARY.md`, `PRODUCT.md`, the interprofessional design spec; `answers.*.provenance` `default-confirmed` until the user confirms; `goal.mode evaluate_and_rework`; `language {source: en, output: en-GB, translation_required: false}`.
- `rubric.json`: core pillars + domain pillars proposed from the old rubric's non-correctness pillars (e.g. AI & computational rigour, ethics/regulatory depth), summing to 40.
- `chapter-plan.json`: 11 chapters with `word_budget` from `check_book.py:14-16`, `parts[]` from `build_book.py:45-51`, `source_refs` empty lists with `dropped []` (history import; the source-unit mapping did not exist).

- [ ] **Step 1: Failing test** — `tests/test_medical_config.py` asserts: all files validate against their schemas; `complete_checks.intake(project)` returns no problems; `chapter-plan.json` budgets equal the legacy `BUDGETS` dict imported from the legacy `check_book.py`; the template's callout labels equal the legacy `BOXES`; the perspective labels equal legacy `LENSES`.
- [ ] **Step 2: Run** → FAIL. **Step 3:** write the files. **Step 4:** Run → PASS.
- [ ] **Step 5: Commit** the config files (no approvals yet): `git commit -m "feat(ai-in-medicine): project config reproducing legacy behaviour (STEP 7 task 4a)"`.
- [ ] **Step 6: USER APPROVAL — intake.** Present brief, rubric, template, theme and the overlay in chat (tables, not raw JSON dumps; offer raw on request). On explicit approval: add the DEC row to `projects/ai-in-medicine/decisions.md` **and** `docs/harness/DECISIONS.md` with the user's words; `run_stage.py --project projects/ai-in-medicine begin intake`, `complete intake --nonce N`, `approve intake --dec DEC-NNN`.
- [ ] **Step 7: USER APPROVAL — history import.** Ask the user to approve importing the historical `ingest`, `evaluate`, `design`, `rework` outputs (N2), listing each stage's files. On approval: DEC row naming `import-history` and the four stages; run `import-history` for each.
- [ ] **Step 8: USER APPROVAL — design.** Present `design.md`, `chapter-plan.json`, `errata-seed.md`. On approval: DEC row; `approve design --dec DEC-NNN`.
- [ ] **Step 9: Gates** — `python harness/run_stage.py --project projects/ai-in-medicine verify --through intake` → exit 0; `verify --through rework` → exit 0 (imported receipts listed as `imported`). Update the legacy pytest tests to pass `--project projects/ai-in-medicine`; `python -m pytest projects/ai-in-medicine/rework/tools -q` → pass.
- [ ] **Step 10: Commit** — `git add projects/ai-in-medicine docs/harness/DECISIONS.md && git commit -m "feat(ai-in-medicine): approved intake, design and history import (STEP 7 task 4b)"`

### Task 7.5: `CLAUDE.md` split (own commit)

- [ ] **Step 1:** `cp CLAUDE.md projects/ai-in-medicine/CLAUDE.md`; `cmp CLAUDE.md projects/ai-in-medicine/CLAUDE.md` → exit 0.
- [ ] **Step 2:** Rewrite root `CLAUDE.md` (≤ 80 lines): what the harness is (vision's six phases); layout pointer (core §1); how to run (`book-*` skills → `run_stage.py`); **Rule 7** verbatim intent (intake gate, design gate, never edit `state.json`, approvals only after explicit user approval with a DEC row); **Rule 8** (no domain literals in `harness/`); **Rule 11** (inline default, ≤ 2 Claude subagents with reasons, Codex excluded); per-project instructions live in `projects/<book>/CLAUDE.md`.
- [ ] **Step 3:** `git diff --stat` shows exactly `CLAUDE.md` modified and `projects/ai-in-medicine/CLAUDE.md` added. Show the user the root `CLAUDE.md` diff in chat (TICKET STEP 7 exit: diff reviewed).
- [ ] **Step 4: Commit** — `git commit -m "docs: split CLAUDE.md into harness root and ai-in-medicine project (STEP 7 task 5)"`

**STEP 7 exit:** `python -m unittest tests.test_bypass_matrix -v` → 0; `CLAUDE.md` diff shown; onboarding DECs exist; `verify --through intake` → 0; Codex review (one pass over tasks 7.1–7.5, after all tests pass).

---

## STEP 8 — Generalise the tools and implement ingest

Common interfaces for STEP 8 (defined in Task 8.1, used by 8.2–8.4):
- `harness/tools/config.py`: `load(project: Path) -> Config` where `Config` is a `dict` with keys `brief, template, theme, chapter_plan, profile_out, profile_src` (profiles from `locale.load_profile` with `template.locale_overrides` merged); `Config.path(key) -> Path` resolves `template.paths.<key>` against the project.
- `harness/text.py`: `words(text, profile) -> int`; `tokens(text, profile) -> list[str]`; `sentences(text, profile) -> list[str]`; `normalise(text, profile, purpose: "compare"|"count") -> str`; `digits_value(s: str) -> int` (either system); `mixed_digits(s) -> bool`.
- `harness/tools/check_book.py`: `parse(text, cfg) -> Parsed` (`Parsed = {"h1": {num, title}, "sections": [{id, role, label, line, body}], "callouts": [{id, line, parts}], "objectives": [...], "mcqs": [...], "key": {...}, "citations": [...], "references": [...], "glossary_terms": [{term, gloss}]}`); `check_chapter(path, cfg, chapter) -> list[Check]`; `check_book(cfg) -> Report`; CLI `python harness/tools/check_book.py --project P [--chapter ID] [--json]` exit 0 iff no `fail`. `Check = {"id","status","message","measured"}`; `Report` is `checker-report.v1`.

### Task 8.1: Checker and assembler generalisation, positive-config fixtures, mutations, leak scan

**Files:**
- Create: `harness/text.py`, `harness/tools/config.py`, `harness/tools/check_book.py`, `harness/tools/assemble.py`, `harness/tools/leak_scan.py`, `tests/fixtures/positive-config/{no-mcq,no-glossary,no-cases,no-perspectives,no-errata}/`, `tests/fixtures/mutations/mutations.json`, `tests/fixtures/leak/forbidden.txt` (generated), `harness/tools/make_forbidden.py`
- Test: `tests/test_text.py`, `tests/test_checker.py`, `tests/test_mutations.py`, `tests/test_positive_config.py`, `tests/test_assemble.py`, `tests/test_leak_scan.py`

Port rule: each legacy function becomes a config-driven function with the same algorithm, replacing each literal by its INV target (core §10): `check_template` ← INV-10/12/13 (`template.sections[]`, `callouts[]`, `chapter_heading_pattern`); `check_lenses` ← INV-14 (`perspectives`); `check_los` ← INV-15; `check_mcqs` ← INV-16 (marker grammar constant, core §4.3); `check_citations` ← INV-17; `check_glossary` ← INV-18; `check_banned` ← INV-19 (+ `profile.banned_terms`); `check_budget` ← INV-09 (`chapter_plan.chapters[].word_budget`, `template.budgets.tolerance`); `check_sentences` ← INV-11 via `text.sentences(profile)`; `check_all` ← INV-20. Every disabled feature returns its IDs as `not_applicable`. `LO-UNASSESSED` and `MCQ-LO-UNKNOWN` are new IDs (core §9.3): an objective with no MCQ tagging it; an MCQ tag naming no objective. `ASSET-MISSING`/`ASSET-OUTSIDE-ROOT` come from the path-relative resolver shared with `assemble.py` (`assemble.resolve_asset(chapter_file, link, cfg) -> Path`, core §1.1 asset model; fixes INV-40).

`mutations.json`:

```json
[
  {"name": "remove-required-callout", "fixture": "ai-in-medicine", "file": "rework/ch01-what-ai-is.md", "op": "delete_line_matching", "arg": "^> \\*\\*Safety Alert:", "expect": "TPL-CALLOUT-MISSING"},
  {"name": "break-image-path", "fixture": "ai-in-medicine", "file": "rework/ch06-seeing-disease.md", "op": "replace_first", "arg": ["](../images/", "](../images/missing-"], "expect": "ASSET-MISSING"},
  {"name": "skew-answer-key", "fixture": "ai-in-medicine", "file": "rework/ch02-health-data.md", "op": "set_all_keys", "arg": "A", "expect": "KEY-BALANCE"},
  {"name": "reopen-erratum", "fixture": "ai-in-medicine", "file": "rework/errata-ledger.md", "op": "replace_first", "arg": ["| closed |", "| open |"], "expect": "ERRATA-OPEN"},
  {"name": "break-citation", "fixture": "ai-in-medicine", "file": "rework/ch03-how-models-learn.md", "op": "append_to_first_prose", "arg": " [999]", "expect": "CIT-MISSING"},
  {"name": "drop-perspective", "fixture": "ai-in-medicine", "file": "rework/ch04-reading-performance-claims.md", "op": "delete_first_perspective_item", "arg": null, "expect": "PERSP-MISSING"},
  {"name": "exceed-word-budget", "fixture": "ai-in-medicine", "file": "rework/ch05-generative-ai-llms.md", "op": "append_prose_words", "arg": 900, "expect": "BUDGET-CHAPTER"}
]
```

(The exact line markers are confirmed against the chapter files in Step 1; each `op` is a small function in the test.)

- [ ] **Step 1: Failing tests** (excerpts; each file holds the full set):

```python
# tests/test_mutations.py
import json, pathlib, re, shutil, subprocess, sys, unittest
from tests.helpers import temp_repo, REPO

MUT = json.loads((REPO / "tests/fixtures/mutations/mutations.json").read_text(encoding="utf-8"))
OPS = {
    "delete_line_matching": lambda t, a: "\n".join(l for l in t.split("\n") if not re.search(a, l)),
    "replace_first": lambda t, a: t.replace(a[0], a[1], 1),
    "set_all_keys": lambda t, a: re.sub(r"(\*\*Q\d+\.) [A-D]\*\*", rf"\1 {a}**", t),
    "append_to_first_prose": lambda t, a: re.sub(r"(\n[A-Z][^\n>#|*-][^\n]*?\.)(\n)", rf"\1{a}\2", t, count=1),
    "delete_first_perspective_item": lambda t, a: re.sub(r"\n> - \*\*[^*]+:\*\*[^\n]*", "", t, count=1),
    "append_prose_words": lambda t, a: t.replace("\n## ", "\n" + " ".join(["word"] * a) + ".\n\n## ", 1),
}

class Mutations(unittest.TestCase):
    def test_each_mutation_yields_named_id(self):
        for m in MUT:
            with self.subTest(m["name"]), temp_repo(project_from="projects/ai-in-medicine", stamp=True) as root:
                f = root / "projects/ai-in-medicine" / m["file"]
                f.write_text(OPS[m["op"]](f.read_text(encoding="utf-8"), m["arg"]), encoding="utf-8")
                r = subprocess.run([sys.executable, "harness/tools/check_book.py", "--project", "projects/ai-in-medicine",
                                    "--json"], cwd=root, capture_output=True, text=True, encoding="utf-8")
                self.assertNotEqual(r.returncode, 0)
                ids = {c["id"] for t in json.loads(r.stdout)["targets"] for c in t["checks"] if c["status"] == "fail"}
                self.assertIn(m["expect"], ids)
```

**Gate note for mutations:** the checker gates as `rework` (N4), and `require_gates(project, "rework")` checks the approvals and the receipts **upstream** of rework (ingest … design, translate), not the rework receipt itself. Editing a chapter therefore does not block the checker, and no bypass flag exists or is needed.

```python
# tests/test_positive_config.py
import json, subprocess, sys, unittest
from tests.helpers import temp_repo

CASES = {"no-mcq": ["MCQ-COUNT", "KEY-BALANCE"], "no-glossary": ["GLOSS-MISSING", "GLOSS-MIN"],
         "no-cases": ["MCQ-CASE"], "no-perspectives": ["PERSP-MISSING", "PERSP-BALANCE"], "no-errata": ["ERRATA-OPEN"]}

class PositiveConfig(unittest.TestCase):
    def test_disabled_checks_not_applicable_and_book_passes(self):
        for name, disabled in CASES.items():
            with self.subTest(name), temp_repo(f"positive-config/{name}", slug=name, stamp=True) as root:
                r = subprocess.run([sys.executable, "harness/tools/check_book.py", "--project", f"projects/{name}", "--json"],
                                   cwd=root, capture_output=True, text=True, encoding="utf-8")
                self.assertEqual(r.returncode, 0, r.stdout[-2000:])
                checks = [c for t in json.loads(r.stdout)["targets"] for c in t["checks"]]
                for cid in disabled:
                    self.assertTrue(all(c["status"] == "not_applicable" for c in checks if c["id"] == cid), cid)
```

```python
# tests/test_leak_scan.py
import pathlib, shutil, subprocess, sys, tempfile, unittest
from tests.helpers import REPO

class LeakScan(unittest.TestCase):
    def test_clean_tree_passes(self):
        r = subprocess.run([sys.executable, "harness/tools/leak_scan.py"], cwd=REPO, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_planted_literal_fails(self):
        forbidden = (REPO / "tests/fixtures/leak/forbidden.txt").read_text(encoding="utf-8").split("\n")[0]
        with tempfile.TemporaryDirectory() as tmp:
            shutil.copytree(REPO / "harness", pathlib.Path(tmp) / "harness")
            shutil.copytree(REPO / "tests/fixtures/leak", pathlib.Path(tmp) / "tests/fixtures/leak")
            (pathlib.Path(tmp) / "harness" / "planted.py").write_text(f"X = {forbidden!r}\n", encoding="utf-8")
            r = subprocess.run([sys.executable, "harness/tools/leak_scan.py", "--root", tmp], capture_output=True, text=True)
            self.assertEqual(r.returncode, 1)
            self.assertIn("planted.py", r.stdout)

    def test_absolute_path_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            shutil.copytree(REPO / "harness", pathlib.Path(tmp) / "harness")
            shutil.copytree(REPO / "tests/fixtures/leak", pathlib.Path(tmp) / "tests/fixtures/leak")
            (pathlib.Path(tmp) / "harness" / "abs.py").write_text("P = r'D:\\\\data'\n", encoding="utf-8")
            r = subprocess.run([sys.executable, "harness/tools/leak_scan.py", "--root", tmp], capture_output=True, text=True)
            self.assertEqual(r.returncode, 1)
```

`--root` is a scan-root argument for the read-only scanner (it has no `--project` because it scans shared code, not a project; core §9.5). `harness/preflight.py`'s `%ProgramFiles%` browser paths use environment variables, not absolute drive paths, so they pass the `[A-Za-z]:\\` pattern.

`tests/test_text.py` covers: English tokenizer equals legacy counts on every medical chapter (`words(text, en) == legacy.words(text)`), sentence split equals legacy on the same chapters, `normalise` compare vs count purposes.

- [ ] **Step 2: Run** → FAIL.
- [ ] **Step 3: Implement** `text.py`, `config.py`, `check_book.py` (port rule above; `--project` via `gate.enforce("rework", argv)` as its first call), `assemble.py` (same gate; output `build/<basename>.md`; path-relative asset rewrite via `os.path.relpath`), `make_forbidden.py` (reads `projects/ai-in-medicine/{template,theme,brief}.json` labels, title, subtitle, author names + a fixed clinical list: `patient, clinical, clinician, physician, pharmacist, physiotherapy, radiology, pathology, diagnosis, medicine, medical, hospital, nurse`) and `leak_scan.py` (scope and patterns core §9.5; case-insensitive whole-word match; prints `path:line: literal`).
- [ ] **Step 4: Positive-config fixtures** — each is a complete small project (one 400-word chapter, template/theme/brief/rubric/chapter-plan, approvals and receipts stamped by `temp_repo`) with exactly one feature disabled.
- [ ] **Step 5: Run** all STEP 8.1 tests → PASS. Golden check (partial, checker fields): `python harness/tools/capture_golden.py --project projects/ai-in-medicine --out $TMP/g8.json` (harness mode: no `--layout`; reads config) then `python harness/tools/compare_golden.py tests/fixtures/ai-in-medicine/golden-step6.json $TMP/g8.json --allow tests/fixtures/ai-in-medicine/allow-step8.json` → the only diffs are under `/docx`, `/pdf`, `/hashes/docx_document` (not rebuilt yet) and `/project`/`/tool_sha`. `allow-step8.json` lists exactly those plus the verify_refs change added in 8.3.
- [ ] **Step 6: Commit** — `git commit -m "feat(harness): config-driven checker and assembler, positive-config, mutations, leak scan (STEP 8 task 1)"`

### Task 8.2: Build generalisation

**Files:**
- Create: `harness/tools/build_book.py`, `harness/stages/build.py`
- Test: `tests/test_build.py`

Port rule: `build_book.py` consumes the checker's `Parsed` representation (INV-30) and `theme.json`; every literal replaced per INV-21…38; the DOCX element factory is **one** function `make_paragraph(doc, text_runs, style, theme)` / `make_run(p, text, theme, *, bold, italic)` / `make_table(...)` (EXT-LOC-2) that applies direction/lang from the theme (LTR only in this step). Output to `build/<basename>.docx|.pdf` (N3). Word COM backend kept (`DispatchEx`, hidden, TOC update, `ExportAsFixedFormat` with the current arguments `build_book.py:959`). `stages/build.py` = `run build`: render figures (placeholder call into `harness/figures/render.py` from STEP 9; until then it copies existing PNGs and records `figures: legacy`), assemble, build DOCX, PDF, write `build-report.json`.

- [ ] **Step 1: Failing test** — `tests/test_build.py::test_medical_build_matches_golden` (skipped unless `preflight.check_word()["ok"]`): inside `temp_repo(project_from="projects/ai-in-medicine", stamp=True)` (tests never touch the real project state, core §3) it runs `run_stage.py --project projects/ai-in-medicine run build`, captures, and compares with `golden-step6.json` under `allow-step8.json` → exit 0. Plus unit tests: `make_run` sets `w:lang` from `theme.lang_tag`; callout layouts come from `theme.callouts`.
- [ ] **Step 2: Run** → FAIL. **Step 3: Implement.** **Step 4: Run** → PASS.
- [ ] **Step 5: Real build (gated, real project):** `python harness/run_stage.py --project projects/ai-in-medicine run build` → exit 0 (writes a build receipt; the design approval and imported rework receipt allow it). Capture + compare as in 8.1 Step 5, now with `/docx`, `/pdf`, `/hashes` **removed** from the allowlist → exit 0.
- [ ] **Step 6: Commit** — `git commit -m "feat(harness): config-driven build (STEP 8 task 2)"`

### Task 8.3: `verify_refs` policy fix

**Files:** Create `harness/tools/verify_refs.py`, `harness/tools/renumber_refs.py`; Test `tests/test_verify_refs.py`

**Interfaces:** `verify_refs.check_chapter(path, cfg, fetch=crossref_title) -> list[Ref]` with `Ref = {"n", "doi", "doi_status": exists|not_found|error|no_doi, "title_status": match|mismatch|manual_pending|manual_ok|not_applicable, "check_id": str|None}`; CLI `--project P [--chapter ID] [--json]`, exit 1 iff any ref has a blocking `check_id` (`REF-NOT-FOUND`, `REF-ERROR`, `REF-TITLE-MISMATCH`, `REF-NO-DOI-DISALLOWED`; `REF-MANUAL-PENDING` from STEP 10). Provider settings from `defaults.json` overridden by `template.references.providers`. The **fix**: a no-DOI reference passes only if its type is in `no_doi_policy.allowed_types` (type detected by `template.references` entry pattern groups; `requires_url` enforced) — otherwise `REF-NO-DOI-DISALLOWED` (fixes INV-46; the legacy tool printed `NO DOI` and passed).

- [ ] **Step 1: Failing tests**

```python
# tests/test_verify_refs.py
import unittest
from harness.tools import verify_refs as vr

CFG = {"template": {"references": {"entry_pattern": r"^(?P<n>\d+)\. (?P<body>.+)$",
                                   "identifier_patterns": [r"DOI:\s*(10\.\S+?)\.?\s*$", r"doi\.org/(10\.\S+?)\.?\s*$"],
                                   "no_doi_policy": {"allowed_types": ["web"], "requires_url": True},
                                   "title_match": {"mode": "heuristic", "words": 6, "threshold": 0.6}}},
       "profile_out": {"tag": "en", "normalisation": {"compare": ["NFC", "casefold"]}}}

class VerifyRefs(unittest.TestCase):
    def test_no_doi_without_allowed_type_fails(self):
        r = vr.classify_line(1, "Smith J. A book about things. Publisher; 2020.", CFG, fetch=lambda d: None)
        self.assertEqual(r["check_id"], "REF-NO-DOI-DISALLOWED")

    def test_network_error_is_ref_error(self):
        def boom(doi): raise OSError("timed out")
        r = vr.classify_line(2, "Doe A. Title words here now. J. 2021. DOI: 10.1/x", CFG, fetch=boom)
        self.assertEqual((r["doi_status"], r["check_id"]), ("error", "REF-ERROR"))

    def test_title_match(self):
        r = vr.classify_line(3, "Doe A. Deep learning for images of cells. J. 2021. DOI: 10.1/y", CFG,
                             fetch=lambda d: "Deep learning for images of cells")
        self.assertEqual((r["doi_status"], r["title_status"], r["check_id"]), ("exists", "match", None))
```

- [ ] **Step 2–4:** fail → implement (port of `verify_refs.py` + `renumber_refs.py` config-driven, gated `rework`) → pass.
- [ ] **Step 5:** Real run `python harness/tools/verify_refs.py --project projects/ai-in-medicine --json` (network). The medical book's no-DOI references now either pass by policy (template sets `allowed_types` for the kinds it has, which the user approved in Task 7.4) or report `REF-NO-DOI-DISALLOWED`. Re-capture golden; compare; the **only** new diff vs STEP 6 is under `/verify_refs/*/status` for no-DOI entries (`no_doi` → `no_doi_allowed` or `no_doi_disallowed`). Add exactly that glob to `allow-step8.json` with reason "verify_refs no-DOI policy fix (TICKET STEP 8)". If any reference becomes `REF-NO-DOI-DISALLOWED`, record it as a medical-project finding in `projects/ai-in-medicine/decisions.md` for the user (do not edit chapters — scope lock).
- [ ] **Step 6: Commit** — `git commit -m "fix(harness): verify_refs enforces the no-DOI policy (STEP 8 task 3)"`

### Task 8.4: Ingest and fidelity

**Files:** Create `harness/tools/convert_docx.py`, `harness/stages/ingest.py`, `tests/fixtures/ingest/*.docx` + `*.expected.json`, `tests/fixtures/ingest/make_fixtures.py`; Test `tests/test_ingest.py`

**Interfaces:** `convert_docx.convert(docx: Path, cfg) -> (markdown: str, assets: dict[str, bytes], report: dict)`; `ingest.run(project) -> (inputs, outputs, extras)` used by `run_stage.py run ingest`: copies `brief.source.files[]` into `source/` (custody; hashes must equal `brief.source.files[].sha256`), writes `source-manifest.json`, converts (DOCX native; other formats via `markitdown` if importable, else exit 1 naming it), writes `ingest/normalized.md`, `ingest/units.json` (TR §4.1: `src-chNN`, `src-chNN-sMM` by document order, line spans, sha256 of the span text), `ingest/assets/*`, `ingest/conversion-report.json` (core §2.4 incl. `omitted[]`), all via `ingest/.tmp/` then `os.replace` per file; exit 2 if any structure `lost`.

Fixtures (generated by `make_fixtures.py` with python-docx, committed as `.docx` + expected JSON):

| Fixture | Contains | Expected |
|---|---|---|
| `headings.docx` | Heading 1/2/3 + a bold-paragraph heading matched by `heading_rules` | headings `ok`, counts literal |
| `tables.docx` | 2 tables + one 1×1 callout table | tables `ok` (2), callouts counted separately (1) |
| `figures.docx` | 2 inline images | figures `ok` (2), 2 assets written |
| `equations.docx` | one OMML equation (inserted as raw XML) | equations `lossy` (1), exit 0, a `lossy` finding recorded |
| `footnotes.docx` | 2 footnote references | footnotes `lossy` (2) |
| `toc.docx` | a source TOC block + body | text `ok` with `omitted[0].reason == "source_toc"`; TOC lines absent from `normalized.md` |
| `dropped-table.docx` | a table inside a text box (converter cannot reach it) | tables `lost`, exit 2, previous outputs untouched |

- [ ] **Step 1: Failing tests** — one test per fixture asserting the literal expected report, plus `test_failed_ingest_keeps_previous_outputs` and `test_units_ids_in_document_order`.
- [ ] **Step 2–4:** fail → implement (port `convert_docx_to_md.py` logic, replacing INV-01…07 literals by `template.ingest.*`/`paths.*`; INV-05/07 removed) → pass.
- [ ] **Step 5:** Medical ingest dry check: in a `temp_repo(project_from="projects/ai-in-medicine")`, `run ingest` on the original DOCX → exit 0 and `conversion-report.json` has no `lost` (the real project keeps its imported ingest receipt; re-running ingest there would invalidate downstream, which is not wanted).
- [ ] **Step 6: Commit** — `git commit -m "feat(harness): ingest stage with fidelity report and units (STEP 8 task 4)"`

**STEP 8 exit:** `python -m unittest discover -s tests -t . -v` → 0 (mutations yield their IDs with non-zero checker exit); golden vs STEP 6 differs only by the listed `verify_refs` change (`compare_golden.py … --allow allow-step8.json` → 0 with the allowlist containing only `/project`, `/tool_sha` and the `verify_refs` glob); positive-config pass; `python harness/tools/leak_scan.py` → 0; Codex review.

---

## STEP 9 — Figure system and chemistry pack

### Task 9.1: Manifest, renderer, charts, checker

**Files:** Create `harness/schemas/figures.v1.json` (exists from 7.1; finalise), `harness/figures/{__init__,render,charts,check_figures}.py`, `harness/figures/packs/__init__.py`; modify `harness/stages/build.py` (call render + check); Test `tests/test_figures.py`, fixture `tests/fixtures/figures-book/`

**Interfaces:** `packs.registry() -> dict[str, module]` (package dirs under `packs/`, plus the built-in `charts`); `render.render_all(project, cfg) -> list[dict]` (one result per figure `{id, svg, png, status}`); `charts.render(spec_path, out_svg, out_png, width_cm)` executes the figure's Python source in a subprocess with `MPLBACKEND=Agg`, fixed `svg.hashsalt`, `svg.fonttype: none`, `metadata={"Date": None}`; hand SVG → PNG via headless browser `--headless --screenshot --window-size=<px> --force-device-scale-factor=<dpi/96>`; `check_figures.check(project, cfg) -> Report` with IDs `FIG-UNREFERENCED, FIG-UNKNOWN, FIG-CAPTION, FIG-ALT, FIG-LICENCE, FIG-RESOLUTION, FIG-AUTHOR-ASSET` (core §7.3); numbering computed by first reference order.

- [ ] **Step 1: Failing tests** — `test_render_is_deterministic` (render twice → identical SVG bytes and identical PNG pixel hash), `test_each_fig_id` (one fixture defect per ID → that ID fails), `test_numbering_by_first_reference`, `test_needs_author_asset_blocks_build` (build exit ≠ 0 with `FIG-AUTHOR-ASSET`), `test_png_300dpi_at_text_width`.
- [ ] **Step 2–4:** fail → implement → pass.
- [ ] **Step 5: Commit** — `git commit -m "feat(harness): figure manifest, deterministic rendering, figure checker (STEP 9 task 1)"`

### Task 9.2: Chemistry pack

**Files:** Create `harness/figures/packs/chemistry/{__init__,pubchem}.py`, `requirements-chemistry.txt` (`rdkit==<version>`); Test `tests/test_chemistry.py`

- [ ] **Step 1: Install the optional group (environment setup, not runtime):** `uv pip install --python "$(python -c 'import sys;print(sys.executable)')" rdkit` → note the installed version; pin it in `requirements-chemistry.txt`; `python harness/preflight.py --group chemistry` → exit 0 (Windows smoke test `CCO`). If the install fails on Windows, stop and ask the user (RDKit is DEC-009 scope, not droppable).
- [ ] **Step 2: Failing tests**

```python
# tests/test_chemistry.py
import json, unittest
from unittest import mock
from harness.figures.packs import chemistry as chem

@unittest.skipUnless(chem.preflight() == [], "rdkit missing")
class Chemistry(unittest.TestCase):
    def test_invalid_smiles_fails(self):
        ids = [f["id"] for f in chem.validate({"kind": "chem.structure", "smiles": "C1CC(", "name": "bad"})]
        self.assertIn("CHEM-SMILES-INVALID", ids)

    def test_valid_structure_renders(self):
        import tempfile, pathlib
        with tempfile.TemporaryDirectory() as t:
            svg, png = pathlib.Path(t, "a.svg"), pathlib.Path(t, "a.png")
            chem.render({"kind": "chem.structure", "smiles": "CC(=O)Oc1ccccc1C(=O)O", "name": "aspirin"}, svg, png)
            self.assertTrue(svg.read_text(encoding="utf-8").startswith("<?xml"))
            self.assertGreater(png.stat().st_size, 1000)

    def test_reaction_smarts(self):
        self.assertEqual(chem.validate({"kind": "chem.reaction", "smarts": "CCO>>CC=O", "name": "oxidation"}), [])
        self.assertIn("CHEM-SMARTS-INVALID",
                      [f["id"] for f in chem.validate({"kind": "chem.reaction", "smarts": "CC(>>", "name": "bad"})])

    def test_offline_is_unverified(self):
        with mock.patch("urllib.request.urlopen", side_effect=OSError("offline")):
            r = chem.crosscheck({"name": "aspirin", "smiles": "CC(=O)Oc1ccccc1C(=O)O"}, "live", self._cache())
        self.assertEqual(r["status"], "unverified")
        self.assertEqual(chem.crosscheck({"name": "aspirin"}, "offline", self._cache())["status"], "unverified")

    def test_mocked_mismatch(self):
        body = json.dumps({"PropertyTable": {"Properties": [{"CanonicalSMILES": "CCO"}]}}).encode()
        with mock.patch("urllib.request.urlopen", return_value=mock.MagicMock(__enter__=lambda s: s, __exit__=lambda *a: False, read=lambda: body)):
            r = chem.crosscheck({"name": "aspirin", "smiles": "CC(=O)Oc1ccccc1C(=O)O"}, "live", self._cache())
        self.assertEqual(r["status"], "fail")

    def _cache(self):
        import tempfile
        self._t = tempfile.TemporaryDirectory()
        return self._t.name
```

- [ ] **Step 3–4:** fail → implement (`KINDS`, `preflight`, `validate` with `Chem.MolFromSmiles(sanitize=False)` then `Chem.SanitizeMol` → `CHEM-SANITIZE`; `render` via `rdMolDraw2D.MolDraw2DSVG` and `MolDraw2DCairo`/Pillow for PNG at 300 dpi; reactions via `AllChem.ReactionFromSmarts` + `Draw.ReactionToImage`/`MolDraw2D.DrawReaction`; `crosscheck` compares canonical SMILES from PubChem `.../compound/name/<name>/property/CanonicalSMILES/JSON` (timeout 10 s, cache `figures/.cache/pubchem/<sha256(name)>.json`); stage effects per core §7.5 wired into `check_figures`) → pass.
- [ ] **Step 5: Commit** — `git commit -m "feat(harness): chemistry pack with RDKit and PubChem cross-check (STEP 9 task 2)"`

### Task 9.3: Visual evidence

- [ ] **Step 1:** `tests/fixtures/figures-book/` includes: one bar chart, one line chart, one hand SVG diagram, two `chem.structure` (aspirin, caffeine), one `chem.reaction` (ethanol oxidation). Render in a temp repo; copy the six PNGs to `docs/harness/reviews/step9-evidence/`.
- [ ] **Step 2:** View each PNG yourself (Read tool) and note any defect; fix before committing.
- [ ] **Step 3: Commit** — `git commit -m "docs(harness): STEP 9 visual evidence"`. The STEP 9 Codex brief lists every PNG path and requires Codex to open each and report per file.

**STEP 9 exit:** all tests pass including the invalid SMILES; evidence committed; Codex review done and inspected every PNG.

---

## STEP 10 — Arabic locale

### Task 10.1: `ar.json`, tokenizer, sentences, digits, calibration

**Files:** Create `harness/locale/ar.json`, `tests/fixtures/locale/ar/{tokenize,sentences,digits}/*.json`, `tests/fixtures/locale/ar/parallel/{pairs.tsv,SOURCE.md}`, `harness/tools/calibrate.py`; modify `harness/text.py`; Test `tests/test_locale_ar.py`

- Corpus: 500+ human-authored EN–AR aligned pairs from an openly licensed source (UN Parallel Corpus sample or OPUS Tatoeba); download once by hand (WebFetch), store `pairs.tsv`, record licence and URL in `SOURCE.md` (AR §2.1). If no openly licensed source is reachable, stop and ask the user.
- `calibrate.py --profile en --corpus tests/fixtures/locale/ar/parallel/pairs.tsv` prints `r` and the three values; they are written into `ar.json` `readability` with `provenance`.

- [ ] **Step 1: Failing tests** — corpus-driven: every case file `{input, expect}` in `tokenize/` (exact word count), `sentences/` (exact list), `digits/` (IDs present/absent). Plus:

```python
def test_arabic_citation_digits(self):
    self.assertEqual(check_book.cited_numbers("كما ذكر [١، ٣-٥].", CFG_AR), [1, 3, 4, 5])

def test_mixed_number_fails(self):
    ids = {c["id"] for c in check_book.check_digits("القيمة 1٢ مرتفعة.", CFG_AR) if c["status"] == "fail"}
    self.assertIn("AR-DIGIT-MIXED", ids)

def test_calibration_reproducible(self):
    out = calibrate.compute(load_profile("en"), load_profile("ar"), PAIRS)
    self.assertEqual({k: out[k] for k in ("mean_sentence_max", "long_sentence_words", "long_share_max")},
                     {k: load_profile("ar")["readability"][k] for k in ("mean_sentence_max", "long_sentence_words", "long_share_max")})
```

- [ ] **Step 2–4:** fail → implement (`text.py` `unicode-word` tokenizer and sentence rules exactly AR §2; digits via `unicodedata.digit`) → pass.
- [ ] **Step 5: Commit** — `git commit -m "feat(harness): Arabic locale profile, tokenizer, sentences, digits, calibration (STEP 10 task 1)"`

### Task 10.2: Labels, objectives, glossary, headings, reference policy

**Files:** modify `harness/tools/check_book.py`, `harness/tools/verify_refs.py`; create `harness/schemas/references-manual.v1.json`, `tests/fixtures/locale/ar/{labels,objectives,glossary,references}/`; Test `tests/test_locale_ar_book.py`

- Chapter heading pattern: implement AR §2.2 expansion (`re.escape`, longest first, both genders, normalised match, `num` → int). Tests: the five literal headings in AR §2.2 parse to 3, 3, 3, 3, 11.
- Labels by ID (AR §4), objectives discouraged-verb patterns (AR §2 `discouraged_objective_verbs`), glossary `gloss` capture, reference `doi_status`/`title_status` modes and `references-manual.json` with `dec_row_sha256` (AR §5), `REF-MANUAL-PENDING`.
- [ ] Steps: failing corpus tests → implement → pass → commit `feat(harness): Arabic labels, headings, glossary gloss, reference policy (STEP 10 task 2)`.

### Task 10.3: RTL rendering, preset, DOCX assertions, evidence

**Files:** create `harness/presets/rtl-textbook.json`, `tests/fixtures/locale/ar/book/` (the `labels/` fixture book as a full project), `tests/fixtures/locale/ar/docx/assertions.json`; modify `harness/tools/build_book.py` (the single element factory gains RTL); Test `tests/test_rtl_docx.py`

- Implement AR §3 row by row inside `make_paragraph`/`make_run`/`make_table`/section setup: bidi run splitting by `unicodedata.bidirectional`, LRM insertion, `w:bidi`, `w:rtl`, `w:cs` fonts (`complex_script` body, `complex_script_heading` for heading/caption/header/footer/TOC styles), `w:szCs`, `w:bCs`/`w:iCs`, `w:bidiVisual`, `sectPr/w:bidi`, `pgNumType hindiNumbers|decimal`, list `numFmt`, display-equation paragraph without `w:bidi`, `dc:language`.
- `assertions.json`: ≥ one `{xpath, expect}` per AR §3 row (AR §6.2 list); `test_rtl_docx.py` builds the fixture book in a temp repo and evaluates each XPath with lxml over `word/document.xml`, `word/styles.xml`, `word/settings.xml`, `docProps/core.xml`.
- Evidence: build the fixture's PDF; render pages to PNG with PyMuPDF (`fitz`, installed; evidence-only, not a runtime dependency) at 150 dpi; save `toc.png`, `table.png`, `list.png`, `mixed-script.png` under `docs/harness/reviews/step10-evidence/`; view each yourself before committing.
- [ ] Steps: failing assertion test → implement → pass → evidence → commit `feat(harness): RTL DOCX rendering, rtl-textbook preset, Arabic evidence (STEP 10 task 3)`.

**STEP 10 exit:** Arabic fixture passes the checker (`check_book.py --project` in temp repo → 0); builds DOCX and PDF; four evidence pages committed; Codex review inspected them.

---

## STEP 11 — Translation, both directions

### Task 11.1: Schemas and `check_translation.py`

**Files:** create `harness/schemas/{termbase,trace}.v1.json`, `harness/tools/check_translation.py`; Test `tests/test_translation_checks.py`

**Interfaces:** `check_translation.check(project, cfg, unit=None) -> Report` with IDs `TB-TERM-MISSING, TB-FORBIDDEN-VARIANT, TB-DNT-ALTERED, TB-GLOSS-MISSING, TB-REJECTED-PRESENT, PRES-CITATION, PRES-IDENTIFIER, PRES-PROTECTED, PRES-FIGURE, PRES-LATIN-TERM, TR-UNIT-MISSING, TR-UNIT-STALE, TR-ORPHAN, TR-TARGET-UNMAPPED` (TR §4.3, §5); source text with `profile_src`, target with `profile_out`; `notes[]` for unprotected numbers. `termbase.v1` has three `$defs` forms (entry, proposal, resolution file); `trace.v1` enforces the `kind: translation|final` field rules of TR §4.2 (the conditional required/forbidden sets are checked in code, `check_translation.trace_problems(map)`, since the schema subset has no `if/then`).

- [ ] Steps: failing tests (one per ID, synthetic en-ar units) → implement → pass → commit `feat(harness): termbase/trace schemas and translation checks (STEP 11 task 1)`.

### Task 11.2: Translate stage, `terms resolve`, review gate

**Files:** modify `harness/state.py` (translate inputs/outputs; audit conditional inputs), `harness/run_stage.py` (`terms resolve`), `harness/stages/complete_checks.py` (`translate`, TR §6 gates, `TB-PROPOSAL-OPEN` in audit, `TR-PAIR-UNSUPPORTED` in intake already from 7.2); Test `tests/test_translate_stage.py`

- `complete translate --unit U`: runs `check_translation --unit U`; unit receipt. `complete translate` (final): every unit in `chapter-plan.chapters[].source_refs` valid; `translation/codex-review.md` exists (`TR-REVIEW-MISSING`), header `reviewer_model` ≠ receipt `author_model` (`TR-REVIEW-SAME-MODEL`, via `state.check_independent(receipt)` — EXT-TR-4), blocker/major rows closed (`TR-REVIEW-OPEN`).
- `terms resolve --dec DEC-NNN`: reads a resolution batch from `terms/resolve-request.json` (Claude writes it from the user's chat answer), validates each `proposal_id` exists in a proposals file, writes/extends `termbase-additions.json` with `dec_id` + `dec_row_sha256`, deletes the request file.
- [ ] Steps: failing tests (`TR-REVIEW-SAME-MODEL`, `TR-REVIEW-MISSING`, `TR-REVIEW-OPEN`, `TB-PROPOSAL-OPEN` on `complete audit`, resolve-then-rework-stale convergence, language-tag criterion 6) → implement → pass → commit `feat(harness): translate stage, terms resolve, review gate (STEP 11 task 2)`.

### Task 11.3: EN→AR and AR→EN fixtures with real reviews (USER SEES OUTPUTS)

**Files:** create `tests/fixtures/translation/{en-ar,ar-en}/` per TR §9 (two chapters, ≥ 4 H2 units, table, figure ref, DOI ref, formula or SMILES, one `dnt`, one `gloss_first_use`, both maps, proposals with one accepted + one rejected + resolution); Test `tests/test_translation_fixtures.py` (TR §9 criteria 1–6 for both directions, each mutation → named ID).

- Claude translates the units (it is the author model); one real Codex review per fixture translation, saved as the fixture's `translation/codex-review.md` with `reviewer_model: codex`; Fix Protocol into the fixture's `translation/fixes.md`.
- Build both fixtures to DOCX/PDF in a temp repo; show the user both outputs (send the PDFs) and wait for them to confirm they have seen them (TICKET STEP 11 exit).
- [ ] Steps: failing fixture tests → build fixtures → reviews → pass → user sees outputs → commit `feat(harness): EN↔AR translation fixtures with independent reviews (STEP 11 task 3)`.

**STEP 11 exit:** both fixtures pass termbase, traceability, preservation, different-model review; Codex review of STEP 11; the user has seen both outputs.

---

## Spec coverage map

| Spec section | Task(s) |
|---|---|
| core §1 layout, project selection, asset model, build location | 7.1 (`paths`), 8.1 (`resolve_asset`), 8.2 (`build/`) |
| core §2.1 graph, phase map, mandatory sets | 7.1 `STAGES`, `mandatory_stages` |
| core §2.2 stage rows | 7.2 (`new`, agentic completers), 8.2 (build), 8.4 (ingest), 11.2 (translate) |
| core §2.3 receipts, control plane, staleness incl. outputs, `require_gates`, invalidation, lock, lease, verify | 7.1, 7.2 |
| core §2.4 ingest fidelity incl. omissions | 8.4 |
| core §3 approvals, `dec_row_sha256`, intake amend | 7.1 (`approve`, `dec_row_hash`), 7.2 (`begin --amend`) |
| core §4 schemas, validator, cross-rules | 7.1, 7.2 |
| core §5 rubric, overlap, caps, digest | 7.1 (`rubric_core.json`), 7.2 (`rubric_problems`, `score`) |
| core §6 overlays and personas | 7.1 (personas), 7.4 (overlay) |
| core §7 figures and chemistry | 9.1, 9.2, 9.3 |
| core §8 evaluate procedure | 7.2 (`complete_checks.evaluate`), skill `book-evaluate` |
| core §9 golden, comparator, check IDs, mutations, positive-config, leak scan, test isolation | 5.2, 8.1, 7.1 (`temp_repo`) |
| core §10 inventory | 7.4 (config values), 8.1–8.4 (port rules) |
| core §11 EXT points | 7.1 (profiles as parameters, `APPROVAL_SETS`), 8.1 (`text.py`), 8.2 (element factory), 8.3 (two-field refs), 10.x, 11.x |
| core §12 dependencies | 5.1 preflight, 9.2 optional group |
| AR §1–§7 | 10.1, 10.2, 10.3 |
| TR §1–§9 | 7.2 (pair rule), 11.1, 11.2, 11.3 |

## Self-review notes

- Placeholder scan: no TBD/TODO; literal values that depend on files (legacy message phrases, exact chapter markers, font file names) are pinned to exact file:line sources and confirmed in the first step of their task.
- Type consistency: `GateError.code` strings are the single list in Task 7.1; `Check`/`Report` shapes defined once (STEP 8 common interfaces) and reused by figures, Arabic and translation checkers.
- Deliberate size limits: STEPS 9–11 give interfaces, tests and literal expectations rather than full implementation listings, because their code depends on RDKit/python-docx behaviour verified at the first failing test; each task still names every function, file, ID and command.
