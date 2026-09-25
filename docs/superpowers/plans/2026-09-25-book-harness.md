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
- **Shell:** every command in this plan runs in **Git Bash** (the Bash tool; `cmp`, `grep`, `cut`, `sha256sum`, `cp` are the GNU tools shipped with Git for Windows), from `D:\yasser`. Temporary paths: `TMP=$(mktemp -d)` at the start of each command block that uses `$TMP`.
- **Commit boundary:** each task ends with `git add <explicit paths>`, `git commit`, then `git show --stat --format=%h HEAD` and `git status --porcelain` → empty. No task commits with a failing gate.
- **Real project vs temp repos:** tests and regression evidence (goldens, builds) run in temporary git repos (core §9.6), so they work before the task's commit. Commands on the real `projects/ai-in-medicine` run only on a clean tree (after the commit), because `tool_sha` refuses dirty tools; they produce no files that would need a second commit, except where a user approval writes `state.json` (Task 7.4, whose single commit comes after the approvals).
- Stop and ask the user at every user-approval point (DEC-028): manifest (STEP 6), medical onboarding intake + design + history import (STEP 7), outputs seen (STEP 11).

## Plan–spec notes (approved with this plan)

These resolve points the specs leave to the plan (core §13). None changes a spec decision.

- **N1 — Baseline capture before migration.** STEP 5 runs before `projects/` exists. The capture logic is a library (`harness/tools/capture_golden.py`: `capture(project_dir, layout) -> dict`). The shipped CLI always enforces the `projects/` rule (core §1.1); its optional `--layout FILE` only says which files **inside** that project to read (used in STEP 6, before project config exists; from STEP 8 the layout is derived from config). The one-time STEP 5 capture of the repo-root layout runs through a **test-side** script, `tests/fixtures/ai-in-medicine/capture_legacy.py`, which imports the library and passes `layout-legacy.json`. No shipped executable accepts a path outside `projects/`.
- **N2 — History import for the medical project.** The medical book was ingested, evaluated, designed and reworked before the harness existed. `require_gates` needs valid upstream receipts, which cannot honestly be produced by re-running agentic stages. `run_stage.py --project P import-history <stage> --dec DEC-NNN` writes a receipt with `status: ok`, `imported: true`, `imported_at_commit` (git `HEAD`), `dec_id`, `dec_row_sha256`, and input/output hashes of the files listed for that stage in the project's `history/import.json` (`{stage: {inputs: [...], outputs: [...]}}`, every path existing and inside the project). The historical artifacts are not in harness format (for example the old evaluation is `history/Review_Notes_AI_in_Medicine.pdf` and `rework/REVIEW_REPORT.md`, not `evaluation/findings.json`), so the import binds what really exists; `import.json` itself is an input of every imported receipt. The user sees and approves the full list and hashes (Task 7.4 Step 6). No file set is ever taken from command-line arguments. Its `tool_sha` is the literal `"imported"`: no harness tool produced these artifacts, so staleness for an imported receipt checks every input/output hash, the DEC row hash and the invalidation marker, but not tool SHA. Restrictions: only stages `ingest`, `evaluate`, `design`, `rework`; only in a project whose `new` receipt has `args.adopted = true` (created by `init-state`, Task 7.4); **one-shot** — refused if the stage already has any receipt or any later stage has a non-imported receipt; the DEC row must contain `import-history` and the stage name. `verify` prints `imported` beside such receipts. Used once, for `ai-in-medicine`, after the user approves it.
- **N3 — Finished outputs are preserved, not rebuilt over.** The manifest moves `AI_in_Health_Care_Interprofessional.{md,docx,pdf}` to `projects/ai-in-medicine/deliverables/`. Harness builds write to `projects/ai-in-medicine/build/` (core §1.1). The STEP 8 golden comparison is `deliverables` capture (STEP 6) vs `build` capture (STEP 8).
- **N4 — Legacy stage mapping for gates.** Legacy tools gate as: `convert_docx_to_md.py` → `ingest`; `check_book.py`, `verify_refs.py`, `renumber_refs.py`, `assemble.py` → `rework`; `build_book.py` → `build`.
- **N5 — Semantic DOCX hash.** `hashes.docx_parts` = `{part_name: sha256}` for **every** part in the package: each XML part is canonicalised (lxml C14N) after removing only the enumerated volatile nodes; each binary part (media) is hashed as raw bytes. Volatile removals, all listed in `volatile_excluded[]` (core §9.1) with reasons: `w:rsid*` attributes and `w:rsids` (save metadata); `w:lastRenderedPageBreak` and `w:proofErr` (layout/proofing); the **result** runs of the TOC field between `w:fldChar separate` and `end` (page numbers depend on Word pagination; the field instruction itself is kept); bookmarks named `_Toc*`; `docProps/core.xml` `created`, `modified`, `lastModifiedBy`, `revision`; `docProps/app.xml` `TotalTime`, `Application`, `AppVersion`. Table cells, headers, footers, styles, numbering, run formatting, relationships and image bytes are all inside the hash. `hashes.docx` = SHA-256 of the canonical JSON of `docx_parts`.
- **N6 — Legacy check IDs in the golden.** In STEPS 5–6 the golden is captured from the legacy checker by importing its functions per chapter. Each function maps to the core §9.3 IDs it covers, and each literal legacy message maps to one ID (table in Task 5.2, copied from `check_book.py`). A function returning `[]` marks its IDs `pass`; an unclassified message makes capture exit 2. Every message → ID mapping has its own mutation test. From STEP 8 the golden is built from `checker-report.v1` JSON.
- **N7 — New check IDs in STEP 8.** The generalised checker emits IDs the legacy checker never computed: `TPL-CALLOUT-COUNT`, `READ-NOPROSE`, `BUDGET-FRONT`, `ASSET-MISSING`, `ASSET-OUTSIDE-ROOT`. They cannot appear in the STEP 6 golden. The STEP 8 comparison therefore (a) compares `checks[]` restricted to the `(id, target)` pairs present in the STEP 6 golden (`compare_golden.py --checks-from A`), which must be identical, and (b) separately requires every extra `(id, target)` pair in the STEP 8 golden to be `pass` or `not_applicable`. All other keys are compared in full. The only allowed diff remains the `verify_refs` policy change (TICKET STEP 8).
- **N9 — What `tool_paths` covers.** Core §2.3 says `tool_paths` are "the harness files it executes". The plan reads that as the files that decide the stage's outputs and checks: the stage module, its tools, its completion-check module (one per stage) and the schemas it validates. The control plane (`state.py`, `paths.py`, `hashing.py`, `schema.py` except for intake) is excluded, so a control-plane fix does not stale every receipt of every project; its correctness is carried by the test suite and the bypass matrix. A stage with no tool yet lists its file-set definition (`harness/stages/contracts.py`) until its tool ships.
- **N8 — Provenance is not content.** `golden.v1` keeps `tool_sha` and capture paths under a top-level `provenance` object. `compare_golden.py` never compares `/provenance` (it is reported, not diffed). `project` is the slug (`ai-in-medicine`) in every capture, so project identity is compared and must be equal.

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
    __init__.py  contracts.py  new.py  ingest.py  build.py
    complete_checks/  __init__.py  common.py  intake.py  evaluate.py  design.py  rework.py  translate.py  audit.py
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
    {"source": "rework/ch01-what-ai-is.md", "destination": "projects/ai-in-medicine/rework/ch01-what-ai-is.md", "sha256": "<raw-bytes SHA-256 before the move>"}
  ],
  "path_fix_allowlist": ["projects/ai-in-medicine/rework/tools/check_book.py"],
  "expected_diff": []
}
```

Invariants (each has a test in Task 6.1): every `source` is tracked; no `destination` exists before the move; no duplicate destination; no `reserved` path moves; `sha256` equals the raw-bytes hash before and after; `images/` stays beside `rework/`; `expected_diff` items are `{pointer_glob, reason}` (core §9.2). Commit B scope is checked after the commit with `git diff-tree` against `path_fix_allowlist` plus named generated artifacts.

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
    import pywintypes, win32com.client
    word = None
    try:
        word = win32com.client.DispatchEx("Word.Application")
        return _c("word-com", "build", True, f"Word {word.Version}")
    except pywintypes.com_error as e:
        return _c("word-com", "build", False, f"Word COM unavailable: {e}")
    finally:
        if word is not None:
            word.Quit()


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
- Create: `harness/hashing.py`, `harness/tools/__init__.py`, `harness/tools/capture_golden.py`, `harness/tools/compare_golden.py`, `tests/fixtures/ai-in-medicine/layout-legacy.json`, `tests/fixtures/ai-in-medicine/capture_legacy.py` (test-side, N1), `tests/fixtures/ai-in-medicine/golden.json`, `tests/fixtures/ai-in-medicine/src/**` (copied), `tests/test_hashing.py`, `tests/test_golden.py`, `tests/test_legacy_classify.py`

**Interfaces:**
- `hashing.canonical_json(obj) -> bytes`; `hashing.hash_bytes(b) -> str`; `hashing.hash_file(path) -> str` (core §2.3).
- `capture_golden.capture(project_dir: Path, layout: dict, *, slug: str, run_refs=True) -> dict` (golden.v1 with N8 `provenance`); `capture_golden.docx_parts(path) -> dict[str, str]` (N5); `capture_golden.classify(fn: str, msg: str) -> str` raising `Unclassified`; `capture_golden.parse_refs_output(chapter, text) -> list[dict]` raising `NetworkError`; `capture_golden.dumps(obj) -> str`.
- Shipped CLI: `python harness/tools/capture_golden.py --project projects/<slug> --out FILE [--layout FILE] [--no-refs]` (projects rule enforced via `harness/paths.py` once it exists; in STEP 5 the CLI exists but is only exercised from STEP 6). Exit 0 ok; 2 on any `verify_refs` `ERROR` or unclassified legacy message.
- Test-side: `python tests/fixtures/ai-in-medicine/capture_legacy.py --out FILE [--copy-src DIR]` → `capture(REPO, layout-legacy.json, slug="ai-in-medicine")`.
- `compare_golden.diff(a, b, allow, *, checks_from=None) -> dict` (golden-diff.v1; ignores `/provenance`; with `checks_from` applies N7); CLI `python harness/tools/compare_golden.py A B --allow FILE [--checks-from A] [--out FILE]`, exit 0 iff every diff allowed and (with `--checks-from`) every extra check passes.

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

**Legacy message → ID table (N6), copied from `rework/tools/check_book.py`.** Regexes anchor on the literal f-string prefixes at the cited lines.

| Legacy function (line) | Literal message (f-string) | Regex | ID |
|---|---|---|---|
| `check_budget` (61) | `budget: {n} words, allowed {lo}–{hi}` | `^budget: ` | `BUDGET-CHAPTER` |
| `check_sentences` (94) | `sentences: mean length {mean} > {MAX_MEAN}` | `^sentences: mean length` | `READ-MEAN` |
| `check_sentences` (97) | `sentences: {share} over {LONG} words (…)` | `^sentences: \S+ over ` | `READ-LONG` |
| `check_template` (104) | `template: missing '# Chapter N: Title'` | `^template: missing '# Chapter` | `TPL-H1` |
| `check_template` (109) | `template: missing section '## {h}'` | `^template: missing section` | `TPL-SECTION-MISSING` |
| `check_template` (113) | `template: required sections out of order` | `^template: required sections out of order` | `TPL-SECTION-ORDER` |
| `check_template` (116) | `template: missing box '{b}'` | `^template: missing box` | `TPL-CALLOUT-MISSING` |
| `check_lenses` (125) | `lens missing: {lens}` | `^lens missing: ` | `PERSP-MISSING` |
| `check_lenses` (132) | `lens imbalance: …` | `^lens imbalance: ` | `PERSP-BALANCE` |
| `check_los` (143) | `LOs: {n} objectives, need 3–5` | `^LOs: \d+ objectives` | `LO-COUNT` |
| `check_los` (146) | `LOs: avoid 'understand': …` | `^LOs: avoid ` | `LO-VERB` |
| `check_mcqs` (164) | `Q{n}: option E present` | `^Q\d+: option E present` | `MCQ-EXTRA-OPTION` |
| `check_mcqs` (166) | `Q{n}: options must be exactly A–D, found …` | `^Q\d+: options must be` | `MCQ-OPTIONS` |
| `check_mcqs` (170) | `Q{n}: missing [LOn] tag` | `^Q\d+: missing \[LOn\] tag` | `MCQ-LO-TAG` |
| `check_mcqs` (172) | `MCQ count {k}, need 10` | `^MCQ count ` | `MCQ-COUNT` |
| `check_mcqs` (174) | `missing **Case Question.**` | `^missing \*\*Case Question` | `MCQ-CASE` |
| `check_mcqs` (178) | `Q{n}: tag LO{lo} not among objectives` | `^Q\d+: tag LO\d+ not among` | `MCQ-LO-UNKNOWN` |
| `check_mcqs` (181) | `LO{lo} has no question` | `^LO\d+ has no question` | `LO-UNASSESSED` |
| `check_mcqs` (186) | `Q{n}: empty rationale` | `^Q\d+: empty rationale` | `KEY-RATIONALE` |
| `check_mcqs` (189) | `Q{n}: no answer key` | `^Q\d+: no answer key` | `KEY-MISSING` |
| `check_mcqs` (194) | `key imbalance: …` | `^key imbalance: ` | `KEY-BALANCE` |
| `check_mcqs` (197) | `key run: …` | `^key run: ` | `KEY-RUN` |
| `check_citations` (220) | `missing reference {n}` | `^missing reference ` | `CIT-MISSING` |
| `check_citations` (221) | `uncited reference {n}` | `^uncited reference ` | `CIT-UNCITED` |
| `check_glossary` (249) | `glossary missing: {t}` | `^glossary missing: ` | `GLOSS-MISSING` |
| `check_banned` (252-253) | the function's literal message | copied at Step 1 from `check_book.py:252-253` | `BANNED-TERM` |
| `check_all` (274) | `book: {k} chapters, need 11` | `^book: \d+ chapters` | `BOOK-CHAPTER-COUNT` |
| `check_all` (281) | `book: missing 00-front-matter.md` | `^book: missing 00-front` | `BOOK-FRONT-MISSING` |
| `check_all` (283) | `book: total {t} words, need …` | `^book: total ` | `BUDGET-TOTAL` |
| `check_all` (286) | `book: errata ledger missing or has open rows` | `^book: errata ledger` | `ERRATA-OPEN` |
| `check_all` (288) | `book: glossary has {k} entries, need ≥ 120` | `^book: glossary has` | `GLOSS-MIN` |

Line numbers are those of `rework/tools/check_book.py` at `445dc0d`; Step 1 re-confirms each against the file. Each function's covered-ID set is the set of IDs in its rows.

`measured` per chapter: `words`, `mean_sentence`, `long_share`, `lo_count`, `mcq_count`, `key_counts {A..D}` (computed by calling the legacy helpers `words`, `clean_prose_lines`, `lo_ids` and the key regex of `check_mcqs`). Book: `total_words`, `glossary_terms`.

- [ ] **Step 1: Failing tests**

```python
# tests/test_hashing.py
import pathlib, tempfile, unittest
from harness import hashing

class HashingTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.tmp.cleanup()

    def _write(self, name, data):
        p = pathlib.Path(self.tmp.name) / name
        p.write_bytes(data)
        return p

    def test_json_canonical_ignores_key_order_and_spacing(self):
        a = self._write("a.json", b'{"b": 1, "a": [1, 2]}')
        b = self._write("b.json", b'{\n  "a": [1,2],\n  "b": 1\n}')
        self.assertEqual(hashing.hash_file(a), hashing.hash_file(b))

    def test_hash_crlf_equal_bom_differs(self):
        lf = self._write("lf.md", "# T\nx\n".encode())
        crlf = self._write("crlf.md", "# T\r\nx\r\n".encode())
        bom = self._write("bom.md", "﻿# T\nx\n".encode())
        self.assertEqual(hashing.hash_file(lf), hashing.hash_file(crlf))
        self.assertNotEqual(hashing.hash_file(lf), hashing.hash_file(bom))

    def test_binary_raw(self):
        a = self._write("a.png", b"\x89PNG\r\n")
        self.assertEqual(hashing.hash_file(a), hashing.hash_bytes(b"\x89PNG\r\n"))
```

```python
# tests/test_golden.py
import io, json, pathlib, tempfile, unittest, zipfile
from harness.tools import capture_golden, compare_golden

def docx_bytes(parts):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        for name, data in parts.items():
            z.writestr(name, data)
    return buf.getvalue()

W = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
DOC = f'<w:document {W}><w:body><w:tbl><w:tr><w:tc><w:p><w:r><w:t>cell</w:t></w:r></w:p></w:tc></w:tr></w:tbl>' \
      f'<w:p w:rsidR="00AB"><w:r><w:t>body</w:t></w:r></w:p></w:body></w:document>'
BASE = {"word/document.xml": DOC, "word/header1.xml": f'<w:hdr {W}><w:p><w:r><w:t>head</w:t></w:r></w:p></w:hdr>',
        "word/styles.xml": f'<w:styles {W}><w:style w:styleId="Normal"/></w:styles>', "word/media/image1.png": b"\x89PNG-A"}


class DocxHashTest(unittest.TestCase):
    def _hash(self, parts):
        with tempfile.TemporaryDirectory() as t:
            p = pathlib.Path(t, "x.docx"); p.write_bytes(docx_bytes(parts))
            return capture_golden.docx_parts(p)

    def test_rsid_is_volatile(self):
        other = dict(BASE, **{"word/document.xml": DOC.replace('w:rsidR="00AB"', 'w:rsidR="00CD"')})
        self.assertEqual(self._hash(BASE), self._hash(other))

    def test_content_changes_are_detected(self):
        base = self._hash(BASE)
        for part, old, new in [("word/document.xml", "cell", "CELL"), ("word/header1.xml", "head", "HEAD"),
                               ("word/styles.xml", "Normal", "Plain"), ("word/media/image1.png", b"-A", b"-B")]:
            with self.subTest(part):
                self.assertNotEqual(self._hash(dict(BASE, **{part: BASE[part].replace(old, new)})), base)


class CompareTest(unittest.TestCase):
    def test_allowed_and_disallowed(self):
        d = compare_golden.diff({"project": "x", "words": {"total": 1}}, {"project": "y", "words": {"total": 2}},
                                [{"pointer_glob": "/project", "reason": "rename"}])
        self.assertEqual({x["pointer"]: x["allowed"] for x in d["diffs"]}, {"/project": True, "/words/total": False})

    def test_provenance_ignored(self):
        self.assertEqual(compare_golden.diff({"provenance": {"tool_sha": "a"}}, {"provenance": {"tool_sha": "b"}}, [])["diffs"], [])

    def test_checks_from_projection(self):
        a = {"checks": [{"id": "CIT-MISSING", "target": "ch01", "status": "pass"}]}
        b = {"checks": [{"id": "CIT-MISSING", "target": "ch01", "status": "pass"},
                        {"id": "READ-NOPROSE", "target": "ch01", "status": "pass"}]}
        self.assertEqual(compare_golden.diff(a, b, [], checks_from=a)["diffs"], [])
        b["checks"][1]["status"] = "fail"
        self.assertTrue(compare_golden.diff(a, b, [], checks_from=a)["diffs"])


class CaptureTest(unittest.TestCase):
    def test_capture_refuses_network_error(self):
        with self.assertRaises(capture_golden.NetworkError):
            capture_golden.parse_refs_output("ch01", "OK 1\nERROR 2: timed out\n")

    def test_dumps_stable(self):
        g = {"b": 1, "a": {"d": 2, "c": [3]}}
        self.assertEqual(capture_golden.dumps(g), capture_golden.dumps(json.loads(capture_golden.dumps(g))))
```

```python
# tests/test_legacy_classify.py — every row of the N6 table, driven by a real legacy call on a mutated chapter
import importlib.util, pathlib, re, unittest
from harness.tools import capture_golden

REPO = pathlib.Path(__file__).resolve().parents[1]
SRC = REPO / "tests/fixtures/ai-in-medicine/src"          # immutable STEP 5 copy
CH = (SRC / "rework/ch01-what-ai-is.md").read_text(encoding="utf-8")

def legacy():
    spec = importlib.util.spec_from_file_location("legacy_check", SRC / "rework/tools/check_book.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod

MUTATIONS = [  # (legacy function, mutation of the chapter text, expected ID)
    ("check_template", lambda t: re.sub(r"^# Chapter \d+: .*$", "# Intro", t, count=1, flags=re.M), "TPL-H1"),
    ("check_template", lambda t: t.replace("\n## References", "\n## Refs", 1), "TPL-SECTION-MISSING"),
    ("check_lenses", lambda t: re.sub(r"\n> - \*\*[^*]+:\*\*[^\n]*", "", t, count=1), "PERSP-MISSING"),
    ("check_los", lambda t: re.sub(r"\[LO1\] \w+", "[LO1] Understand", t, count=1), "LO-VERB"),
    ("check_mcqs", lambda t: re.sub(r"(\*\*Q1\.) [A-D]\*\*", r"\1**", t, count=1), "KEY-MISSING"),
    ("check_citations", lambda t: t.replace(".\n", " [999].\n", 1), "CIT-MISSING"),
    # Step 1 extends this list until every row of the N6 table has one entry (31 rows).
]

class LegacyClassify(unittest.TestCase):
    def test_every_mapping_row(self):
        mod = legacy()
        for fn, mutate, expected in MUTATIONS:
            with self.subTest(fn=fn, expected=expected):
                msgs = getattr(mod, fn)(mutate(CH)) if fn not in ("check_budget", "check_glossary") else None
                self.assertTrue(msgs, "mutation produced no legacy message")
                self.assertIn(expected, {capture_golden.classify(fn, m) for m in msgs})

    def test_table_complete(self):
        ids = {row[2] for row in MUTATIONS}
        self.assertEqual(ids, set(capture_golden.ALL_LEGACY_IDS))

    def test_unknown_message_raises(self):
        with self.assertRaises(capture_golden.Unclassified):
            capture_golden.classify("check_template", "something the table does not know")
```

(`check_budget(text, budget)` and `check_glossary(text, path)` take a second argument; their `MUTATIONS` entries call them through a small `call(mod, fn, text)` helper in the test that supplies `budget=10` and the src glossary path.)

- [ ] **Step 2: Run** — `python -m unittest tests.test_hashing tests.test_golden tests.test_legacy_classify -v` → exit 1 (modules missing). `test_legacy_classify` needs `src/`; it is created in Step 7 by the first capture, so run it again after Step 7.

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
"""Walk two golden JSON trees and report every difference (core §9.2, plan N7/N8)."""
import argparse, fnmatch, json, sys

_MISSING = object()


def _walk(a, b, ptr, out):
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            _walk(a.get(k, _MISSING), b.get(k, _MISSING), f"{ptr}/{k}", out)
    elif isinstance(a, list) and isinstance(b, list):
        for i in range(max(len(a), len(b))):
            _walk(a[i] if i < len(a) else _MISSING, b[i] if i < len(b) else _MISSING, f"{ptr}/{i}", out)
    elif a != b:
        out.append((ptr or "/", None if a is _MISSING else a, None if b is _MISSING else b))


def _project_checks(b, checks_from):
    keep = {(c["id"], c["target"]) for c in checks_from.get("checks", [])}
    kept = [c for c in b.get("checks", []) if (c["id"], c["target"]) in keep]
    extra = [c for c in b.get("checks", []) if (c["id"], c["target"]) not in keep]
    return dict(b, checks=kept), extra


def diff(a, b, allow, *, checks_from=None):
    a = {k: v for k, v in a.items() if k != "provenance"}
    b = {k: v for k, v in b.items() if k != "provenance"}
    extra = []
    if checks_from is not None:
        b, extra = _project_checks(b, checks_from)
    found = []
    _walk(a, b, "", found)
    diffs = []
    for ptr, before, after in found:
        rule = next((r for r in allow if fnmatch.fnmatchcase(ptr, r["pointer_glob"])), None)
        diffs.append(dict(pointer=ptr, before=before, after=after,
                          allowed=rule is not None, reason=rule["reason"] if rule else ""))
    for c in extra:
        if c["status"] not in ("pass", "not_applicable"):
            diffs.append(dict(pointer=f"/checks/+{c['id']}@{c['target']}", before=None, after=c["status"],
                              allowed=False, reason="new check ID must pass (plan N7)"))
    return {"schema_version": 1, "diffs": diffs}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("a"); ap.add_argument("b")
    ap.add_argument("--allow", required=True)
    ap.add_argument("--checks-from")
    ap.add_argument("--out")
    x = ap.parse_args()
    load = lambda p: json.load(open(p, encoding="utf-8"))
    allow = load(x.allow)
    allow = allow.get("expected_diff", allow) if isinstance(allow, dict) else allow
    result = diff(load(x.a), load(x.b), allow, checks_from=load(x.checks_from) if x.checks_from else None)
    text = json.dumps(result, ensure_ascii=False, indent=1, sort_keys=True)
    if x.out:
        open(x.out, "w", encoding="utf-8", newline="\n").write(text + "\n")
    for d in result["diffs"]:
        print(("ALLOWED " if d["allowed"] else "DIFF ") + d["pointer"])
    sys.exit(0 if all(d["allowed"] for d in result["diffs"]) else 1)


if __name__ == "__main__":
    main()
```

- [ ] **Step 5: Implement `capture_golden.py`** (output via `dumps` = `json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=True) + "\n"`, written with `newline="\n"`):
  - `CLASSIFY = {function: [(regex, id), ...]}` from the N6 table; `ALL_LEGACY_IDS` = every ID in it; `classify(fn, msg)`.
  - `load_legacy_checker(project_dir, layout)`: `importlib.util.spec_from_file_location` on `<project_dir>/<legacy_tools>/check_book.py`; sets the module's `ROOT` to `<project_dir>/<chapters_dir>` (read-only).
  - `checks_for_chapter(mod, path)`: calls each legacy function in `check_chapter` order with its real arguments; each covered ID → `{"id", "target", "status", "measured": {}}`; classified failures → `fail` + `message`.
  - `book_checks(mod)`: `check_all()` with stdout captured; `book:` lines classified.
  - `parse_refs_output`, `refs(project_dir, layout)` (legacy `verify_refs.py` subprocess per chapter unless `--no-refs`), `images(...)` (Pillow, project-relative POSIX paths), `docx_parts(path)` (N5, lxml `etree.tostring(tree, method="c14n")` after removing the volatile nodes), `docx_facts(path)` (part list, paragraph count per style, `a:blip` count, TOC field present), `pdf_facts(path)` (pypdf pages + flattened outline titles).
  - `capture(project_dir, layout, slug, run_refs=True)` → keys `schema_version, project (= slug), checks, chapters, words, references, verify_refs, images, docx, pdf, hashes {assembled_md, docx, docx_parts, chapters}, volatile_excluded, provenance {tool_sha, captured_from}`.
  - CLI (shipped): resolves `--project` with the projects rule. Until `harness/paths.py` exists (Task 7.1), the CLI performs the same check inline: `path.resolve().parent == REPO / "projects"` and name regex; Task 7.1 replaces it with `paths.resolve_project`.
  - `tests/fixtures/ai-in-medicine/capture_legacy.py`: loads `layout-legacy.json`, calls `capture(REPO, layout, slug="ai-in-medicine")`, writes `--out`; `--copy-src DIR` copies `src_copy` paths, refusing if `DIR` exists with any differing file (compared by `hash_file`); identical → no-op.

- [ ] **Step 6: Run tests** — `python -m unittest tests.test_hashing tests.test_golden -v` → exit 0.

- [ ] **Step 7: Capture twice and compare bytes** (Git Bash):

```bash
TMP=$(mktemp -d)
python tests/fixtures/ai-in-medicine/capture_legacy.py --out tests/fixtures/ai-in-medicine/golden.json --copy-src tests/fixtures/ai-in-medicine/src; echo "exit=$?"
python tests/fixtures/ai-in-medicine/capture_legacy.py --out "$TMP/golden2.json"; echo "exit=$?"
cmp tests/fixtures/ai-in-medicine/golden.json "$TMP/golden2.json"; echo "cmp=$?"
python -m unittest tests.test_legacy_classify -v; echo "exit=$?"
git status --porcelain -- . ':!harness' ':!tests'
```

Expected: `exit=0`, `exit=0`, `cmp=0`, `exit=0`, and the last command prints nothing (no tracked file outside `harness/`, `tests/` changed; scope lock). A capture exit 2 on `ERROR` means network trouble: re-run later, never edit the golden by hand. The `verify_refs` no-DOI bug is captured as-is (`no_doi` statuses).

- [ ] **Step 8: Commit**

```bash
git add harness/hashing.py harness/tools/__init__.py harness/tools/capture_golden.py harness/tools/compare_golden.py tests/test_hashing.py tests/test_golden.py tests/test_legacy_classify.py tests/fixtures/ai-in-medicine
git commit -m "feat(harness): golden capture/compare and frozen medical baseline (STEP 5b)"
git status --porcelain   # expect empty
```

**STEP 5 exit:** `python harness/preflight.py` → 0; the two captures byte-identical; `python -m unittest discover -s tests -t . -v` → 0; Codex review done (protocol above).

---

## STEP 6 — Manifest-driven migration

### Task 6.1: Manifest and its validator

**Files:**
- Create: `docs/harness/migration-manifest.json`, `harness/tools/manifest.py`, `tests/test_manifest.py`, `tests/fixtures/ai-in-medicine/layout-projects.json`

**Interfaces:**
- `manifest.problems(repo: Path, m: dict, phase: "pre"|"post") -> list[str]`; `manifest.scope_problems(repo, m, changed: list[str], extra_allowed: list[str]) -> list[str]`; CLI `python harness/tools/manifest.py --phase pre|post` and `python harness/tools/manifest.py --scope-commit HEAD --extra <path>...` (checks `git diff-tree --no-commit-id --name-only -r <commit>` against `path_fix_allowlist` + `--extra`); exit 0 iff no problems.

Manifest content (every tracked file of the medical book; listed from `git ls-files` for the paths below):

| Source | Destination |
|---|---|
| `rework/**` (chapters, front matter, glossary, errata, `_template.md`, `REVIEW_REPORT.md`, `figures/**`, `tools/**`) | `projects/ai-in-medicine/rework/**` |
| `images/**` | `projects/ai-in-medicine/images/**` |
| `AI_in_Health_Care_Interprofessional.{md,docx,pdf}` | `projects/ai-in-medicine/deliverables/` (N3) |
| `AI_in_Medicine- Assistant Prof Dr Shereen Elkholy.{md,docx}` | `projects/ai-in-medicine/original/` |
| `convert_docx_to_md.py` | `projects/ai-in-medicine/tools/convert_docx_to_md.py` |
| `EVALUATION_RUBRIC.md`, `EVALUATION_GUIDE.md`, `Review_Notes_AI_in_Medicine.pdf`, `VERDICT.md`, `SESSION_SUMMARY.md`, `PRODUCT.md` | `projects/ai-in-medicine/history/` |
| `.claude/agents/medical-ai-reviewer.md` | `projects/ai-in-medicine/history/medical-ai-reviewer.md` (its text becomes the overlay in Task 7.4) |

Not moved: `CLAUDE.md` (reserved), `.claude/agents/academic-*.md`, `research-synthesist.md`, `.agents/skills/**` (they become shared personas in Task 7.1), `docs/**`, `.gitignore`, `tests/**`, `harness/**`.

`path_fix_allowlist`: `projects/ai-in-medicine/rework/tools/{check_book,build_book,assemble,verify_refs,renumber_refs,test_check_book,test_verify_refs}.py`, `projects/ai-in-medicine/tools/convert_docx_to_md.py`. `expected_diff`: `[]`. Captures record project-relative paths and the slug (N8), so moving the tree changes no compared field. If Task 6.3 finds a diff, the task stops and asks the user rather than widening the allowlist silently.

`layout-projects.json` = `layout-legacy.json` with `deliverables` under `deliverables/` and `legacy_tools` at `rework/tools`; all other paths unchanged (they were already relative to the book root, which is now `projects/ai-in-medicine`).

- [ ] **Step 1: Failing test** — one test per invariant:

```python
# tests/test_manifest.py
import copy, json, pathlib, unittest
from harness.tools import manifest

REPO = pathlib.Path(__file__).resolve().parents[1]
REAL = json.loads((REPO / "docs/harness/migration-manifest.json").read_text(encoding="utf-8"))

def one(src, dst, sha=None, **extra):
    m = {"schema_version": 1, "project": "p", "reserved": ["CLAUDE.md"], "path_fix_allowlist": [], "expected_diff": [],
         "moves": [{"source": src, "destination": dst, "sha256": sha or "0"}]}
    m.update(extra)
    return m

class ManifestInvariants(unittest.TestCase):
    def test_real_manifest_pre_ok(self):
        self.assertEqual(manifest.problems(REPO, REAL, "pre"), [])

    def test_reserved_never_moved(self):
        self.assertTrue(any("reserved" in p for p in manifest.problems(REPO, one("CLAUDE.md", "projects/p/CLAUDE.md"), "pre")))

    def test_untracked_source(self):
        self.assertTrue(any("not tracked" in p for p in manifest.problems(REPO, one("nope.md", "projects/p/nope.md"), "pre")))

    def test_existing_destination(self):
        self.assertTrue(any("exists" in p for p in manifest.problems(REPO, one(".gitignore", "CLAUDE.md"), "pre")))

    def test_wrong_hash(self):
        self.assertTrue(any("hash" in p for p in manifest.problems(REPO, one(".gitignore", "projects/p/.gitignore", sha="0" * 64), "pre")))

    def test_duplicate_destination(self):
        m = one(".gitignore", "projects/p/x")
        m["moves"].append({"source": "CLAUDE.md", "destination": "projects/p/x", "sha256": "0"})
        self.assertTrue(any("duplicate" in p for p in manifest.problems(REPO, m, "pre")))

    def test_post_requires_moved_state(self):
        self.assertTrue(any("missing" in p for p in manifest.problems(REPO, one(".gitignore", "projects/p/never.txt"), "post")))

    def test_expected_diff_format(self):
        m = one(".gitignore", "projects/p/y", expected_diff=[{"pointer": "/x"}])
        self.assertTrue(any("expected_diff" in p for p in manifest.problems(REPO, m, "pre")))

    def test_images_beside_rework(self):
        dests = {pathlib.PurePosixPath(e["destination"]).parts[2] for e in REAL["moves"]
                 if e["source"].startswith(("images/", "rework/"))}
        self.assertEqual(dests, {"images", "rework"})

    def test_scope(self):
        m = one(".gitignore", "projects/p/z", path_fix_allowlist=["a.py"])
        self.assertEqual(manifest.scope_problems(REPO, m, ["a.py", "rep.md"], ["rep.md"]), [])
        self.assertTrue(manifest.scope_problems(REPO, m, ["b.py"], []))
```

- [ ] **Step 2: Run** — `python -m unittest tests.test_manifest -v` → exit 1.
- [ ] **Step 3: Implement `manifest.py`**: `pre` → source tracked (`git ls-files --error-unmatch`), destination absent, `hash_bytes(read_bytes)` equals `sha256`, no reserved path in source or destination, no duplicate destination, every `expected_diff` item has exactly `pointer_glob` and `reason`; `post` → destination exists with the same raw hash, source absent. Generate the manifest `moves` with a short script (`git ls-files` over the listed paths → destination mapping per the table → raw hash), review the output by eye, save.
- [ ] **Step 4: Run** — `python -m unittest tests.test_manifest -v` → exit 0; `python harness/tools/manifest.py --phase pre` → exit 0.
- [ ] **Step 5: Commit**

```bash
git add docs/harness/migration-manifest.json harness/tools/manifest.py tests/test_manifest.py tests/fixtures/ai-in-medicine/layout-projects.json
git commit -m "docs(harness): migration manifest and validator (STEP 6a)"
git status --porcelain   # expect empty
```

- [ ] **Step 6: USER APPROVAL.** Show the user the moves table, `sha256sum docs/harness/migration-manifest.json` and `git rev-parse HEAD`. On explicit approval, add the DEC row (next free number) to `docs/harness/DECISIONS.md` naming both values and the user's words; `git add docs/harness/DECISIONS.md && git commit -m "docs(harness): record manifest approval"`. **Task 6.2 does not start before that DEC exists.**

### Task 6.2: Commit A — pure moves

- [ ] **Step 1:** `python harness/tools/manifest.py --phase pre` → exit 0; `git status --porcelain` → empty.
- [ ] **Step 2:** Moves:

```bash
python - <<'EOF'
import json, pathlib, subprocess
m = json.load(open("docs/harness/migration-manifest.json", encoding="utf-8"))
for e in m["moves"]:
    pathlib.Path(e["destination"]).parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "mv", e["source"], e["destination"]], check=True)
EOF
```

- [ ] **Step 3:** `python harness/tools/manifest.py --phase post` → exit 0.
- [ ] **Step 4:** `git status --porcelain | cut -c1-2 | sort -u` → only `R ` (`git mv` stages the renames; no `git add` is used, so nothing else can enter commit A). `git commit -m "chore(migrate): move medical book into projects/ai-in-medicine (STEP 6 commit A)"`; then `git show -M100% --name-status --format= HEAD | cut -f1 | sort -u` → exactly `R100`, and `git status --porcelain` → empty.

### Task 6.3: Commit B — path fixes, re-capture, golden diff

- [ ] **Step 1:** `grep -rn "parents\[\|ROOT /\|\"rework\"\|AI_in_Health_Care\|images/" projects/ai-in-medicine/rework/tools projects/ai-in-medicine/tools` — every path literal that now points to the wrong place.
- [ ] **Step 2:** Edit only those literals, only in allowlisted files. Typical: `OUT = ROOT / "AI_in_Health_Care_Interprofessional.docx"` → `ROOT / "deliverables" / …` (legacy `ROOT` stays `parents[2]` because the relative depth is unchanged); `DOCX_PATH` absolute path in `convert_docx_to_md.py:13-15` → path relative to the script (`pathlib.Path(__file__).resolve().parents[1] / "original" / …`).
- [ ] **Step 3:** `python -m pytest projects/ai-in-medicine/rework/tools -q` → all pass (legacy tests are pytest-style; pytest 9.1.1 is a dev tool here, not a runtime dependency).
- [ ] **Step 4:** Re-capture and diff (Git Bash):

```bash
TMP=$(mktemp -d)
python harness/tools/capture_golden.py --project projects/ai-in-medicine --layout tests/fixtures/ai-in-medicine/layout-projects.json --out tests/fixtures/ai-in-medicine/golden-step6.json; echo "exit=$?"
python harness/tools/compare_golden.py tests/fixtures/ai-in-medicine/golden.json tests/fixtures/ai-in-medicine/golden-step6.json --allow docs/harness/migration-manifest.json --out "$TMP/diff.json"; echo "exit=$?"
```

Expected: `exit=0` twice. Write `docs/harness/reviews/step6-golden-diff.md` with both commands, exit codes and the diff list (expected empty).
- [ ] **Step 5:** Scope check before commit: `git status --porcelain` lists only allowlisted files plus `tests/fixtures/ai-in-medicine/golden-step6.json` and `docs/harness/reviews/step6-golden-diff.md`.
- [ ] **Step 6: Commit and verify scope after commit**

```bash
git add projects/ai-in-medicine/rework/tools projects/ai-in-medicine/tools tests/fixtures/ai-in-medicine/golden-step6.json docs/harness/reviews/step6-golden-diff.md
git commit -m "fix(migrate): path constants only (STEP 6 commit B)"
python harness/tools/manifest.py --scope-commit HEAD --extra tests/fixtures/ai-in-medicine/golden-step6.json --extra docs/harness/reviews/step6-golden-diff.md; echo "exit=$?"   # expect 0
git status --porcelain   # expect empty
```

**STEP 6 exit:** manifest DEC names SHA-256 and commit; commit A is `R100` only; `manifest.py --scope-commit` on commit B → 0; golden diff → 0; Codex review done.

---

## STEP 7 — Control plane, gates everywhere, `CLAUDE.md` split

### Task 7.1: Paths, schema validator, schemas, state, rubric core, shared personas

**Files:**
- Create: `harness/paths.py`, `harness/schema.py`, `harness/state.py`, `harness/stages/__init__.py`, `harness/stages/contracts.py`, `harness/schemas/{brief,rubric,template,theme,chapter-plan,overlay,state,findings,scorecard,checker-report,source-manifest,conversion-report,figures,golden,golden-diff,units}.v1.json`, `harness/rubric_core.json`, `harness/defaults.json`, `harness/agents/{subject-reviewer,statistician,research-synthesist,psychologist,narratologist,anthropologist,historian,geographer,instructional-designer}.md`, `harness/locale/__init__.py`, `harness/locale/en.json`, `harness/presets/ltr-textbook.json`
- Test: `tests/helpers.py`, `tests/test_paths.py`, `tests/test_schema.py`, `tests/test_state.py`

**Interfaces:**
- `paths.REPO: Path` (git work tree containing `harness/`); `paths.resolve_project(arg: str, *, must_exist=True) -> Path` raising `state.GateError("PROJECT-OUTSIDE"|"PROJECT-NAME"|"PROJECT-MISSING")`.
- `schema.load_schema(name: str) -> dict` (reads `harness/schemas/<name>.v1.json`); `schema.validate(doc, sch, ptr="") -> list[str]` supporting exactly the core §4 subset `type, required, properties, additionalProperties, items, enum, pattern, minimum, maximum, minItems, maxItems, const` and nothing else (repeated shapes are written out inline; `unknown_keywords` rejects any other keyword, including `$ref`, `title`, `description`). String-length limits (overlay caps, core §6) are not in the subset and are enforced in code by `complete_checks.intake` (Task 7.2).
- `state.GateError(code: str, message: str)`; `state.STAGES: list[dict]` = `[{"id","kind","after","tool_paths","approvals"}]` in graph order (core §2.1); `state.APPROVAL_SETS: dict[str, Callable[[Path], list[str]]]`; `state.mandatory_stages(brief: dict) -> list[str]`; `state.load(project) -> dict`; `state.write(project, fn: Callable[[dict], None])` (holds `state.lock`); `state.tool_sha(tool_paths, repo=None) -> str` (raises `DIRTY-TOOL`, `TOOL-UNTRACKED`, `GIT-ERROR`); `state.receipt_problems(project, stage_id, st) -> list[str]`; `state.require_gates(project, stage_id, repo=None) -> dict`; `state.begin(project, stage_id, amend=False, author_model=None, repo=None) -> str` (nonce; `author_model` is stored in `active_run` and copied into the receipt, EXT-TR-4); `state.complete(project, stage_id, nonce, extras: dict, unit=None, final=False, repo=None) -> dict` (file sets come from `contracts.files(project, stage_id, unit)`, never from the caller); `state.run_auto(project, stage_id, fn)`; `state.abort(project, stage_id, reason)`; `state.approve(project, kind, dec)`; `state.import_history(project, stage_id, dec)`; `state.verify(project, through=None) -> list[str]`; `state.dec_row_hash(project, dec) -> str`.
- `locale.load_profile(tag: str) -> dict` (primary subtag → `harness/locale/<primary>.json`, then `template.locale_overrides` merged by the caller via `locale.with_overrides(profile, overrides)`).
- `tests/helpers.temp_repo(fixture: str|None, slug: str) -> ContextManager[Path]` and `helpers.run_cli(repo: Path, *args) -> CompletedProcess` (core §9.6).

Error codes (stderr line `ERROR <CODE>: <message>`, exit 1): `PROJECT-OUTSIDE`, `PROJECT-NAME`, `PROJECT-MISSING`, `NO-APPROVAL`, `APPROVAL-STALE`, `APPROVAL-SET-CHANGED`, `DEC-ROW-CHANGED`, `DEC-MISSING`, `UPSTREAM-MISSING`, `UPSTREAM-STALE`, `RUN-ACTIVE`, `NO-ACTIVE-RUN`, `NONCE-MISMATCH`, `DIRTY-TOOL`, `TOOL-UNTRACKED`, `GIT-ERROR`, `LOCKED`, `SCHEMA`, `NOT-MANDATORY`, `RESERVED-FIELD`, `UNIT-UNKNOWN`, `IMPORT-REFUSED`.
- `harness/stages/contracts.py` (created in this task): `files(project, stage_id, unit=None) -> tuple[list[str], list[str]]` returns the canonical input and output paths of a stage (or one unit) exactly as core §2.2 and TR §2 list them, resolved through `template.paths` and `chapter-plan.json`; `units(project, stage_id) -> list[str]` (chapter IDs for `rework`, `source_refs` unit IDs for `translate`). Every receipt's file maps come only from here.

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

    def test_tool_sha_rejects_untracked_and_empty(self):
        with temp_repo() as root:
            with self.assertRaises(state.GateError) as cm:
                state.tool_sha(["harness/does_not_exist.py"], repo=root)
            self.assertEqual(cm.exception.code, "TOOL-UNTRACKED")

    def test_extras_cannot_override_reserved_fields(self):
        with temp_repo("state-basic", stamp=True) as root:
            p = root / "projects" / "fixture-book"
            nonce = state.begin(p, "evaluate", repo=root)
            with self.assertRaises(state.GateError) as cm:
                state.complete(p, "evaluate", nonce, extras={"outputs": {}}, repo=root)
            self.assertEqual(cm.exception.code, "RESERVED-FIELD")

    def test_import_history_refused_unless_adopted_and_one_shot(self):
        with temp_repo("state-basic", stamp=True) as root:
            p = root / "projects" / "fixture-book"
            with self.assertRaises(state.GateError) as cm:
                state.import_history(p, "evaluate", "DEC-001")
            self.assertEqual(cm.exception.code, "IMPORT-REFUSED")   # not adopted
            state.write(p, lambda st: st["receipts"]["new"]["args"].update(adopted=True))
            with self.assertRaises(state.GateError) as cm:
                state.import_history(p, "ingest", "DEC-001")
            self.assertEqual(cm.exception.code, "IMPORT-REFUSED")   # ingest already has a receipt

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

`tests/fixtures/state-basic/` is a tiny valid project: brief, rubric, template, theme (each `schema_version: 1`, valid against its schema), `decisions.md` with a row `| DEC-001 | 2026-09-25 | user | approve intake | "ok" |`, `ingest/normalized.md`, and `state.json` with a `new` receipt (`args: {slug: fixture-book}`), an intake receipt, an intake approval and an ingest receipt. Its hashes and `tool_sha` are placeholders (`"0"`); `stamp_project` rewrites them inside the temp repo.

- [ ] **Step 2: Run** — `python -m unittest tests.test_paths tests.test_schema tests.test_state -v` → FAIL.

- [ ] **Step 3: Implement `harness/schema.py`**

```python
"""Stdlib validator for exactly the JSON Schema subset in core §4."""
import json, pathlib, re

SCHEMAS = pathlib.Path(__file__).resolve().parent / "schemas"
KEYWORDS = {"type", "required", "properties", "additionalProperties", "items", "enum", "pattern",
            "minimum", "maximum", "minItems", "maxItems", "const"}
TYPES = {"object": dict, "array": list, "string": str, "boolean": bool, "null": type(None)}


def load_schema(name):
    return json.loads((SCHEMAS / f"{name}.v1.json").read_text(encoding="utf-8"))


def unknown_keywords(sch, ptr=""):
    bad = [f"{ptr}/{k}" for k in sch if k not in KEYWORDS]
    for k, sub in (sch.get("properties") or {}).items():
        bad += unknown_keywords(sub, f"{ptr}/properties/{k}")
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


def validate(doc, sch, ptr=""):
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
                errs += validate(item, sch["items"], f"{ptr}/{i}")
    if isinstance(doc, dict):
        for k in sch.get("required", []):
            if k not in doc:
                errs.append(f"{ptr}/{k}: required")
        props = sch.get("properties", {})
        for k, v in doc.items():
            if k in props:
                errs += validate(v, props[k], f"{ptr}/{k}")
            elif sch.get("additionalProperties") is False:
                errs.append(f"{ptr}/{k}: not allowed")
            elif isinstance(sch.get("additionalProperties"), dict):
                errs += validate(v, sch["additionalProperties"], f"{ptr}/{k}")
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


# Tool provenance design (plan fix S4-01): a stage's tool_paths list only the code that decides that stage's
# outputs or checks. The control plane (state.py, paths.py, hashing.py) is not listed: it is covered by tests,
# and listing it would stale every receipt of every project on any control-plane fix. Stages that have no tool
# yet list harness/stages/contracts.py (their file-set definition); the task that ships a stage's tool replaces
# it (Tasks 8.x, 9.x, 11.x state their STAGES edit). tool_sha refuses untracked paths.
STAGES = [
    {"id": "new", "kind": "auto", "tool_paths": ["harness/stages/contracts.py"]},        # -> stages/new.py in 7.2
    {"id": "intake", "kind": "agentic", "tool_paths": ["harness/schema.py", "harness/schemas/brief.v1.json", "harness/schemas/rubric.v1.json",
                                                       "harness/schemas/template.v1.json", "harness/schemas/theme.v1.json",
                                                       "harness/schemas/overlay.v1.json"]},  # + complete_checks/intake.py in 7.2
    {"id": "ingest", "kind": "auto", "tool_paths": ["harness/stages/contracts.py"]},     # -> ingest.py, convert_docx.py in 8.4
    {"id": "evaluate", "kind": "agentic", "tool_paths": ["harness/stages/contracts.py"]},  # -> complete_checks/{common,evaluate}.py in 7.2
    {"id": "design", "kind": "agentic", "tool_paths": ["harness/stages/contracts.py"]},  # -> complete_checks/design.py in 7.2
    {"id": "translate", "kind": "agentic", "tool_paths": ["harness/stages/contracts.py"]},  # -> check_translation.py, complete_checks/translate.py in 11.x
    {"id": "rework", "kind": "agentic", "tool_paths": ["harness/stages/contracts.py"]},  # -> check_book.py (8.1), verify_refs.py + complete_checks/rework.py (8.3)
    {"id": "build", "kind": "auto", "tool_paths": ["harness/stages/contracts.py"]},      # -> assemble.py (8.1), build.py + build_book.py (8.2), figures (9.1)
    {"id": "audit", "kind": "agentic", "tool_paths": ["harness/stages/contracts.py"]},   # -> complete_checks/{common,audit}.py in 7.2
]
RESERVED = {"stage", "status", "args", "inputs", "outputs", "tool_sha", "time", "error", "invalidated_by",
            "units", "imported", "imported_at_commit", "dec_id", "dec_row_sha256"}
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


def _git(repo, *args):
    r = subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True)
    if r.returncode != 0:
        raise GateError("GIT-ERROR", f"git {' '.join(args)} failed: {r.stderr.strip()}")
    return r.stdout


def tool_sha(tool_paths, repo=None):
    repo = repo or paths.REPO
    for tp in tool_paths:
        if not _git(repo, "ls-files", "--", tp).strip():
            raise GateError("TOOL-UNTRACKED", f"{tp} is not a tracked file or directory")
    dirty = _git(repo, "status", "--porcelain", "--", *tool_paths)
    if dirty.strip():
        raise GateError("DIRTY-TOOL", f"uncommitted changes in {', '.join(tool_paths)}:\n{dirty}")
    sha = _git(repo, "log", "-1", "--format=%H", "--", *tool_paths).strip()
    if not sha:
        raise GateError("GIT-ERROR", f"no commit touches {tool_paths}")
    return sha


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
    if r.get("imported"):
        try:
            if dec_row_hash(project, r["dec_id"])[0] != r["dec_row_sha256"]:
                probs.append(f"{stage_id}: import DEC row changed")
        except GateError as e:
            probs.append(f"{stage_id}: {e}")
        return probs  # plan N2: imported artifacts are bound by content, not by a harness tool SHA
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
- `begin(project, stage_id, amend=False, author_model=None, repo=None)`: `require_gates`; refuses `RUN-ACTIVE` if `active_run` set (message names stage, unit, started_at); refuses `NOT-MANDATORY` if the stage is not in `mandatory_stages(brief)` (brief absent → only `new`/`intake` allowed); `amend` allowed only for `intake`; sets `active_run = {stage, nonce, pid, started_at, author_model}`, invalidates downstream unless `amend`; returns nonce `secrets.token_hex(8)`.
- `complete(project, stage_id, nonce, extras, unit=None, final=False)`: `require_gates` again; `NO-ACTIVE-RUN` / `NONCE-MISMATCH` checks; `RESERVED-FIELD` if any `extras` key is in `RESERVED`; file maps from `contracts.files(project, stage_id, unit)` (`hash_map` also fails `SCHEMA` if a listed output file is missing); computes `tool_sha` (may raise `DIRTY-TOOL`, `TOOL-UNTRACKED`).
  - **Unit lifecycle** (rework, translate; core §2.2, TR §2): one `begin <stage>` opens one stage lease. Inside it, `complete <stage> --unit U --nonce N` may be called for any unit in `contracts.units(...)` (else `UNIT-UNKNOWN`), in any order and repeatedly; each writes `receipts[stage]["units"][U] = {status, args: {unit: U}, inputs, outputs, tool_sha, time, **extras}` and **keeps** the lease. `complete <stage> --nonce N` (no unit, `final=True`) requires every unit receipt present and not stale, runs the stage-level checks, writes the stage receipt (whose `inputs`/`outputs` are the union of the unit maps plus stage-level files), and clears the lease. A new session resumes by reading the nonce from `verify` output (`active_run: rework nonce=… started=…`); `abort` is only for abandoning the run.
  - Non-unit agentic stages: `complete <stage> --nonce N` writes the receipt and clears the lease.
- `run_auto(project, stage_id, fn)`: `begin` + `fn(project) -> (inputs, outputs, extras)` + complete; on exception writes `{status: "failed", error: str(e)}` and clears the lease, then re-raises.
- `abort(project, stage_id, reason)`: requires `active_run.stage == stage_id`; appends `{stage, nonce, reason, time}` to `aborts`; clears lease.
- `approve(project, kind, dec)`: `dec_row_hash` must succeed and the row must contain `kind` (case-insensitive) — else `DEC-MISSING`; writes `{kind, files: hash_map(APPROVAL_SETS[kind]), dec_id, dec_row_sha256, approved_at, approved_by: "user"}`. For `design` also `require_gates(project, "design")` must pass except for the design approval itself.
- `import_history(project, stage_id, dec)`: `IMPORT-REFUSED` unless all hold: stage in `{"ingest","evaluate","design","rework"}`; `receipts["new"]["args"]["adopted"] is True`; the stage has no receipt; no later stage has a non-imported receipt; the DEC row contains `import-history` and `stage_id`; `history/import.json` lists the stage and every listed file exists inside the project. Writes `{stage, status: "ok", imported: True, imported_at_commit: <git HEAD>, dec_id, dec_row_sha256, tool_sha: "imported", inputs, outputs, time}`; for `rework` it also writes one imported unit receipt per chapter in `chapter-plan.json`.
- `verify(project, through=None)`: returns a list of failure lines: `require_gates(project, next stage after through or last mandatory)` errors, every mandatory receipt up to the boundary via `receipt_problems`, `active_run` if set; prints `imported` receipts as info, not failure.

Write `harness/schemas/state.v1.json` to match exactly (receipt object with `additionalProperties: true` for stage extras; approvals `additionalProperties: false`).

- [ ] **Step 6: Write the other schemas** — one file each, fields exactly as core §4.1–§4.5, §6, §7.1, §8, §9, `additionalProperties: false` at every object level except receipt extras. Every document requires `"schema_version": {"const": 1}`. `brief.v1.json` enforces `answers` with all 13 letters as `required`. `rubric.v1.json` enforces `pillars` items `{id, kind, name, description, weight, anchors, hard_caps, reviewer_ids, applicable}` and `hard_caps` items `{trigger: {severity, min_count, tag}, max_score, description}`. Numeric cross-constraints (weights sum to 100, 1–4 domain pillars of 5–40 summing to 40) are code in `harness/stages/complete_checks/intake.py` (Task 7.2), not schema.

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
- Create: `harness/run_stage.py`, `harness/stages/new.py`, `harness/stages/complete_checks/{__init__,common,intake,evaluate,design,audit}.py` (one module per stage so a change to one stage's checks stales only that stage; `__init__` re-exports `CHECKS`, `rubric_problems`, `score`, `fixes_rows`, `review_header`, `overlay_cap_problems`),
- Modify: `harness/state.py` (`STAGES`: `new` → `["harness/stages/new.py"]`; `intake` += `harness/stages/complete_checks/intake.py`; `evaluate` → `[common.py, evaluate.py]`; `design` → `[common.py, design.py]`; `audit` → `[common.py, audit.py]`, all under `harness/stages/complete_checks/`), `.claude/skills/book-{new,intake,ingest,evaluate,design,translate,rework,build,audit,verify}/SKILL.md`
- Test: `tests/test_run_stage.py`, `tests/test_complete_checks.py`

**Interfaces:**
- CLI: `python harness/run_stage.py --project P <command>`; commands `new`, `init-state` (Task 7.4), `begin STAGE [--amend] [--author-model NAME]`, `complete STAGE --nonce N [--unit U]`, `run STAGE`, `abort STAGE --reason TEXT`, `approve intake|design --dec DEC-NNN`, `import-history STAGE --dec DEC-NNN`, `terms resolve --dec DEC-NNN` (Task 11.2), `verify [--through STAGE]`. Exit 0 ok; 1 `GateError` or check failure (stderr `ERROR <CODE>: …`, one line per problem); 2 usage error or ingest `lost`.
- `complete_checks.CHECKS: dict[str, Callable[[Path, dict, str|None], tuple[dict, list[str]]]]` — `(project, active_run, unit) -> (extras, problems)` per agentic stage (file sets are not theirs to decide: `contracts.files`); `complete_checks.intake(project)`, `.evaluate(project)`, `.design(project)`, `.audit(project)`; `complete_checks.score(rubric, scorecard, findings, fixes) -> list[str]` (core §5.4); `complete_checks.fixes_rows(project, path) -> tuple[dict[str, str], list[str]]` (finding ID → status, problems) for the Fix Protocol table; `complete_checks.review_header(path) -> dict` (parses the `key: value` header lines of a saved review: `reviewed_commit`, `verdict`, `open_blocker_major`, `reviewer_model`).
- `new.run(project_arg) -> None`: creates `projects/<slug>/` with `agents/`, `source/`, `ingest/`, `evaluation/`, `design/`, `figures/src/`, `build/`, `audit/`, empty `decisions.md` (header row `| DEC | Date | Kind | Decision | User words |`), and `state.json` `{schema_version:1, project_id, receipts:{}, approvals:{}, active_run:null, aborts:[]}`; receipt `new` with `args: {slug}`, outputs = the directory markers (`.keep` files) and `decisions.md` excluded (control plane). On failure removes only what it created.

`complete_checks.intake` enforces: all five kinds validate; core §4.6 rules 1–8 (rule 2/3 by primary subtag via `locale.primary(tag)`); `TR-PAIR-UNSUPPORTED` when subtags differ and the pair is not `en-ar`/`ar-en` (message names the pair); rubric §5.2 (four fixed pillars with core weights, G3→G2 reallocation only when MCQs, cases and exercises are all disabled, 1–4 domain pillars each 5–40 summing to 40, total 100, unique IDs, ≥1 reviewer each); `brief.unresolved == []`. `evaluate`/`audit` enforce `findings.v1`, one pillar per finding, `score()` (weighted total, cap triggers vs `caps_applied`), `rubric_digest` equality (audit vs evaluate receipt), and the fixes gate: every blocker/major Codex finding has a row with status `fixed + verified`, `rejected` or `ruled by user`. **A `ruled by user` row must carry a `DEC` column value** whose row exists in `projects/<p>/decisions.md`; `fixes_rows` returns the problem `RULING-NO-DEC` otherwise, and the completer records `{finding_id: dec_row_sha256}` in the receipt extras as `rulings`, so a later edit of that DEC row makes the receipt stale (checked in `receipt_problems` alongside the file hashes). The fixes table columns are `ID | real/rejected | root cause | siblings found | fix | status | DEC | verification → result`. `audit` also refuses `CHEM-UNVERIFIED` unless a `ruled by user` row with a DEC covers it (core §7.5) and refuses `TB-PROPOSAL-OPEN` (TR §3.3). `evaluate` and `audit` record `author_model` (from `active_run`; `begin` defaults it to `claude` for every agentic stage except `translate`, where `--author-model` is required, Task 11.2) and `reviewer_model` (from `review_header`), both required non-empty; `begin` prints `nonce=<hex>` on stdout. `intake` also enforces the overlay caps of core §6 in code: `scope` ≤ 400 characters; `criteria` ≤ 12 items; `exclusions` and `evidence_expectations` ≤ 8 items; every list item ≤ 200 characters. `design` enforces `chapter-plan.v1`, budget sum within `template.budgets.total`, every evaluate blocker/major mapped to a chapter or `out-of-scope` with reason.

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
Additional tests in `tests/test_complete_checks.py` (same file, written in Step 1):

```python
class RulingTest(unittest.TestCase):
    def test_bare_ruled_by_user_does_not_close(self):
        with temp_repo("state-basic", stamp=True) as root:
            p = root / "projects" / "fixture-book"
            (p / "evaluation").mkdir(exist_ok=True)
            f = p / "evaluation" / "fixes.md"
            f.write_text("| ID | real/rejected | root cause | siblings found | fix | status | DEC | verification → result |
"
                         "|---|---|---|---|---|---|---|---|
| S-01 | real | x | none | y | ruled by user |  | n/a |
", encoding="utf-8")
            rows, probs = cc.fixes_rows(p, f)
            self.assertIn("RULING-NO-DEC", " ".join(probs))

class OverlayCapsTest(unittest.TestCase):
    def test_boundaries(self):
        ok = {"scope": "x" * 400, "criteria": ["c" * 200] * 12, "exclusions": ["e"] * 8, "evidence_expectations": ["v"] * 8}
        self.assertEqual(cc.overlay_cap_problems(ok), [])
        for key, bad in [("scope", "x" * 401), ("criteria", ["c"] * 13), ("criteria", ["c" * 201]),
                         ("exclusions", ["e"] * 9), ("evidence_expectations", ["v"] * 9)]:
            with self.subTest(key=key):
                self.assertTrue(cc.overlay_cap_problems(dict(ok, **{key: bad})))
```

(`from tests.helpers import temp_repo` is added to the file's imports.)

- [ ] **Step 3: Implement** `run_stage.py` (argparse subcommands; every command resolves `--project` via `paths.resolve_project(..., must_exist=command != "new")`; catches `GateError` → `print(f"ERROR {e.code}: {e}", file=sys.stderr); sys.exit(1)`), `new.py`, the `complete_checks/` package (functions above; `rubric_problems(rubric, assessment_enabled)`; `score(...)` computes `round(sum(score*weight)/10, 1)` over applicable pillars; `fixes_rows` parses the Markdown table in `fixes.md` by header names `ID` and `real/rejected` + the status column `fix`/`status`).
- [ ] **Step 4: Skills** — each `SKILL.md` is ≤ 30 lines: `name: book-<stage>`, description "Run the <stage> stage of the book harness through run_stage.py", body: the exact `run_stage.py` commands, the gate reminder (Rule 7: never edit `state.json`; approvals only after explicit user approval in chat with a DEC row), and for agentic stages the task brief the runner prints at `begin`. `book-intake` includes the questionnaire A–M from `docs/harness/INTAKE_QUESTIONNAIRE.md` by reference.
- [ ] **Step 5: Run** — `python -m unittest tests.test_run_stage tests.test_complete_checks -v` → PASS.
- [ ] **Step 6: Commit**

```bash
git add harness/run_stage.py harness/stages/new.py harness/stages/complete_checks harness/state.py .claude/skills tests/test_run_stage.py tests/test_complete_checks.py
git commit -m "feat(harness): stage runner, completion checks, book-* skills (STEP 7 task 2)"
git status --porcelain   # expect empty
```

### Task 7.3: Executable registry, legacy gate shims and the bypass matrix

**Files:**
- Create: `harness/gate.py`, `harness/registry.py`, `tests/fixtures/bypass/` (a minimal gated project: intake + design approvals, receipts `new` … `design` valid, `goal.mode evaluate_and_rework`)
- Modify: `projects/ai-in-medicine/rework/tools/{check_book,build_book,assemble,verify_refs,renumber_refs}.py`, `projects/ai-in-medicine/tools/convert_docx_to_md.py` (entry lines only); `projects/ai-in-medicine/rework/tools/{test_check_book,test_verify_refs}.py` (run the tools inside a temp repo with the bypass project, so they pass in this task)
- Test: `tests/test_bypass_matrix.py`

**Interfaces:**
- `registry.EXECUTABLES: list[dict]` — one row per script in the repo that has a `__main__` block (outside `tests/`), `{path, gate: <stage id> | None, why_ungated: str | None}`. Gated rows: the six legacy tools (N4) and every `harness/tools/*.py` / `harness/figures/*.py` that takes `--project` (rows are added by the task that creates the tool). Ungated rows need a reason: `harness/preflight.py` ("environment probe, reads no project"), `harness/tools/compare_golden.py` ("compares two JSON files"), `harness/tools/manifest.py` ("repo migration validator"), `harness/tools/leak_scan.py` ("scans shared code"), `harness/tools/capture_golden.py` ("read-only regression capture; still enforces the projects rule"), `harness/tools/calibrate.py` (STEP 10, "reads the test corpus only"). Scripts under `tests/` (e.g. `capture_legacy.py`, `make_forbidden.py`) are excluded. `harness/run_stage.py` has `gate: "per-command"`.
- `registry.RUNNER_COMMANDS: list[dict]` — every runner command form with the stage it gates: `run <auto stage>`, `begin <stage>`, `complete <stage>` (with `--nonce`), `complete <unit stage> --unit U`, `approve design` (gates as `design`, needs intake approval), `import-history <stage>`, `terms resolve` (gates as `rework`, Task 11.2 adds it), `verify`. Generated from `state.STAGES` so a new stage adds rows automatically.
- `gate.enforce(stage_id, argv) -> Path`: parses and removes `--project P`; missing → `ERROR PROJECT-REQUIRED`, exit 1; resolves via `paths.resolve_project`; `state.require_gates(project, stage_id)`; on `GateError` prints `ERROR <CODE>: …` and exits 1.
- Legacy shim (first statements of each legacy script body):

```python
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4]))  # repo root; parents[3] for projects/<p>/tools/*.py
from harness.gate import enforce
PROJECT = enforce("rework", sys.argv)  # stage per N4
```

**Matrix.** For each gated executable and each runner command, every case below is run **independently** in a fresh `temp_repo("bypass", slug="bypass-book", stamp=True, with_legacy=True)`:

| Case | Setup | Expected when the case applies to the gate stage | When it does not apply |
|---|---|---|---|
| no approval | delete `approvals.intake` | `ERROR NO-APPROVAL` | — (applies to every stage after intake) |
| edit after approval | append a space to `brief.json` `identity.title` | `ERROR APPROVAL-STALE` | — |
| DEC row edited | change the intake DEC row text | `ERROR DEC-ROW-CHANGED` | — |
| stale upstream receipt | edit `ingest/normalized.md` | `ERROR UPSTREAM-STALE` for stages after ingest | ingest-gated: stderr must **not** contain `UPSTREAM-STALE` |
| missing design approval | delete `approvals.design` | `ERROR NO-APPROVAL` for translate/rework/build/audit gates | ingest/evaluate/design gates: stderr must **not** contain `NO-APPROVAL` |
| outside `projects/` | `--project harness` | `ERROR PROJECT-OUTSIDE` | — |
| missing `--project` (scripts only) | omit it | `ERROR PROJECT-REQUIRED` | — |
| staleness during agentic work (runner, agentic stages only) | `begin S` succeeds, then edit `brief.json`, then `complete S --nonce N` | `ERROR APPROVAL-STALE` from `complete` | — |

"Does not apply" cases are asserted, not skipped: the command runs and its stderr lacks the named code (it may fail later for unrelated reasons, e.g. missing inputs, which is fine).

- [ ] **Step 1: Failing test**

```python
# tests/test_bypass_matrix.py
import json, pathlib, subprocess, sys, unittest
from harness import registry, state
from tests.helpers import temp_repo, REPO

AFTER_INGEST = set(state.ORDER[state.ORDER.index("ingest") + 1:])
DESIGN_GATED = set(state.ORDER[state.ORDER.index("translate"):])


def edit_json(path, fn):
    d = json.loads(path.read_text(encoding="utf-8")); fn(d); path.write_text(json.dumps(d), encoding="utf-8")


SETUPS = {
    "no-approval": lambda p: edit_json(p / "state.json", lambda st: st["approvals"].pop("intake")),
    "edit-after-approval": lambda p: edit_json(p / "brief.json", lambda b: b["identity"].update(title=b["identity"]["title"] + " ")),
    "dec-row-edited": lambda p: (p / "decisions.md").write_text((p / "decisions.md").read_text(encoding="utf-8").replace("approve intake", "approve intake (edited)"), encoding="utf-8"),
    "stale-upstream": lambda p: (p / "ingest" / "normalized.md").write_text("tampered\n", encoding="utf-8"),
    "no-design": lambda p: edit_json(p / "state.json", lambda st: st["approvals"].pop("design")),
}
CODE = {"no-approval": "NO-APPROVAL", "edit-after-approval": "APPROVAL-STALE", "dec-row-edited": "DEC-ROW-CHANGED",
        "stale-upstream": "UPSTREAM-STALE", "no-design": "NO-APPROVAL"}


def applies(case, stage):
    if case == "stale-upstream":
        return stage in AFTER_INGEST
    if case == "no-design":
        return stage in DESIGN_GATED
    return True


def invocations():
    for row in registry.EXECUTABLES:
        if row["gate"] not in (None, "per-command"):
            yield row["path"], row["gate"], lambda proj, t=row["path"]: [sys.executable, t] + (["--project", proj] if proj else [])
    for cmd in registry.RUNNER_COMMANDS:
        yield f"run_stage {cmd['argv']}", cmd["gate"], lambda proj, c=cmd: [sys.executable, "harness/run_stage.py", "--project", proj, *c["argv"].split()]


def run(root, argv):
    return subprocess.run(argv, cwd=root, capture_output=True, text=True, encoding="utf-8")


class BypassMatrix(unittest.TestCase):
    def test_cases(self):
        for name, stage, argv in invocations():
            for case, code in CODE.items():
                with self.subTest(exe=name, case=case), temp_repo("bypass", slug="bypass-book", stamp=True, with_legacy=True) as root:
                    SETUPS[case](root / "projects" / "bypass-book")
                    r = run(root, argv("projects/bypass-book"))
                    if applies(case, stage):
                        self.assertNotEqual(r.returncode, 0, r.stdout)
                        self.assertIn(f"ERROR {code}", r.stderr)
                    else:
                        self.assertNotIn(f"ERROR {code}", r.stderr)
            with self.subTest(exe=name, case="outside"), temp_repo("bypass", slug="bypass-book", stamp=True, with_legacy=True) as root:
                r = run(root, argv("harness"))
                self.assertIn("ERROR PROJECT-OUTSIDE", r.stderr)

    def test_missing_project_flag(self):
        for row in registry.EXECUTABLES:
            if row["gate"] in (None, "per-command"):
                continue
            with self.subTest(exe=row["path"]), temp_repo("bypass", slug="bypass-book", stamp=True, with_legacy=True) as root:
                self.assertIn("ERROR PROJECT-REQUIRED", run(root, [sys.executable, row["path"]]).stderr)

    def test_staleness_during_agentic_work(self):
        for sid in [s["id"] for s in state.STAGES if s["kind"] == "agentic" and s["id"] in ("evaluate", "design")]:
            with self.subTest(stage=sid), temp_repo("bypass", slug="bypass-book", stamp=True, with_legacy=True) as root:
                p = ["--project", "projects/bypass-book"]
                b = run(root, [sys.executable, "harness/run_stage.py", *p, "begin", sid])
                self.assertEqual(b.returncode, 0, b.stderr)
                nonce = b.stdout.split("nonce=")[1].split()[0]
                SETUPS["edit-after-approval"](root / "projects" / "bypass-book")
                c = run(root, [sys.executable, "harness/run_stage.py", *p, "complete", sid, "--nonce", nonce])
                self.assertIn("ERROR APPROVAL-STALE", c.stderr)

    def test_registry_covers_every_script(self):
        mains = {str(p.relative_to(REPO)).replace("\\", "/") for p in REPO.rglob("*.py")
                 if "__main__" in p.read_text(encoding="utf-8", errors="replace")
                 and not str(p.relative_to(REPO)).startswith(("tests", ".git"))
                 and not p.name.startswith("test_")}
        self.assertEqual(mains, {r["path"] for r in registry.EXECUTABLES})
        for r in registry.EXECUTABLES:
            self.assertTrue(r["gate"] or r["why_ungated"], r["path"])

    def test_runner_commands_cover_every_stage(self):
        gated = {c["gate"] for c in registry.RUNNER_COMMANDS}
        self.assertEqual(gated - {None}, set(state.ORDER) - {"new"})
```

`begin` prints `nonce=<hex>` on stdout (Task 7.2 runner contract; add `test_begin_prints_nonce` to `tests/test_run_stage.py` in this task if Task 7.2 did not assert it).

- [ ] **Step 2: Run** — `python -m unittest tests.test_bypass_matrix -v` → exit 1 (no registry, legacy tools ungated).
- [ ] **Step 3: Implement** `registry.py`, `gate.py`; insert the shim into the six tools; update the two legacy pytest files so each test creates `temp_repo("bypass", slug="bypass-book", stamp=True, with_legacy=True)` and calls the tool with `--project projects/bypass-book` plus its original file arguments (the tools still read the files they are given).
- [ ] **Step 4: Run**

```bash
python -m unittest tests.test_bypass_matrix -v; echo "exit=$?"            # expect 0
python -m pytest projects/ai-in-medicine/rework/tools -q; echo "exit=$?"  # expect 0
python -m unittest discover -s tests -t . -v; echo "exit=$?"              # expect 0
```

- [ ] **Step 5: Commit**

```bash
git add harness/gate.py harness/registry.py tests/test_bypass_matrix.py tests/fixtures/bypass projects/ai-in-medicine/rework/tools projects/ai-in-medicine/tools
git commit -m "feat(harness): executable registry, gate every legacy tool, bypass matrix (STEP 7 task 3)"
git status --porcelain   # expect empty
```


### Task 7.4: Medical project onboarding (USER APPROVALS, one commit)

**Files:**
- Create: `projects/ai-in-medicine/{brief,rubric,template,theme}.json`, `projects/ai-in-medicine/agents/clinical-accuracy.json` (overlay from `history/medical-ai-reviewer.md`), `projects/ai-in-medicine/design/{design.md,chapter-plan.json,errata-seed.md}`, `projects/ai-in-medicine/decisions.md`, `projects/ai-in-medicine/state.json` (written only by the runner)
- Modify: `harness/run_stage.py`, `harness/stages/new.py` — add `init-state`: `run_stage.py --project P init-state` refuses if `state.json` exists, otherwise writes the empty state and a `new` receipt with `args: {slug, adopted: true}`; `harness/stages/contracts.py` — medical paths resolve through `template.paths` (no special case)
- Test: `tests/test_medical_config.py`, `tests/test_run_stage.py::test_init_state_refuses_existing`

**Content rules (reproduce the old hardcoded behaviour, INV mapping core §10):**
- `template.json`: section, callout and perspective labels from `check_book.py:18-22`; `budgets.total {17000, 21000}`, `front_matter 500`; readability from `check_book.py:14-17`; LO `id_pattern "^LO\\d+$"`, `min 3`, `max 5`, `discouraged_verbs ["understand"]`; MCQ `count 10`, `option_labels ["A","B","C","D"]`, `key_balance {2,3}`, `max_run 2`; numeric-bracket citations; `references.no_doi_policy` as the user decides at Step 3 (the STEP 5 golden records the old pass-everything behaviour; the fix is Task 8.3); `banned_terms` from `check_book.py:252-253`; errata open value `open`; glossary `minimum_terms 120`, `term_syntax bold`, `excluded_callout_ids [<perspective callout id>]`; `paths.chapters "rework"`, `chapter_glob "ch*.md"`, `allowed_asset_roots ["images","rework/figures"]`.
- `theme.json`: preset `ltr-textbook`, `lang_tag en-GB`, fonts, palette, page, callout colours, boxed and TOC-excluded sections from `build_book.py:30-51, 204-237, 569-573`; `title_page.notices` = the fictional-patient notice; `output.basename "AI_in_Health_Care_Interprofessional"`.
- `brief.json`: A–M from `history/SESSION_SUMMARY.md`, `history/PRODUCT.md` and the interprofessional design spec; `answers.*.provenance "default-confirmed"`; `goal.mode evaluate_and_rework`; `language {source: en, output: en-GB, translation_required: false}`.
- `rubric.json`: the four core pillars plus domain pillars proposed from the old rubric's non-correctness pillars, summing to 40.
- `chapter-plan.json`: 11 chapters, `word_budget` from `check_book.py:14-16`, `parts[]` from `build_book.py:45-51`, `source_refs []`, `dropped []`.

- [ ] **Step 1: Failing tests** — `tests/test_medical_config.py`: every file validates against its schema; `complete_checks.intake` returns no problems; `chapter-plan.json` budgets equal the legacy `BUDGETS` imported from `projects/ai-in-medicine/rework/tools/check_book.py`; template callout labels equal legacy `BOXES`; perspective labels equal legacy `LENSES`. `test_init_state_refuses_existing`: in a temp repo, `init-state` twice → second exits 1 with `ERROR PROJECT-EXISTS`.
- [ ] **Step 2: Run** — `python -m unittest tests.test_medical_config tests.test_run_stage -v` → exit 1.
- [ ] **Step 3: Write the files and the `init-state` code.** Run → exit 0. Commit the **code** part only if the tree must be clean for the runner (it must: `tool_sha` refuses dirty tools):

```bash
git add harness/run_stage.py harness/stages/new.py harness/stages/contracts.py tests/test_medical_config.py tests/test_run_stage.py
git commit -m "feat(harness): init-state for adopting an existing project (STEP 7 task 4, code)"
```

This is the task's code commit; the config and approvals below form its data commit. Both are one reviewable task with one gate set (Step 9); the split exists only because approvals require committed tools. (Plan note: TICKET STEP 4 "one commit boundary per task" is kept as one boundary **per gate**, and this task has two gates — tests, then user approvals.)

- [ ] **Step 4: Create state.** `python harness/run_stage.py --project projects/ai-in-medicine init-state` → exit 0.
- [ ] **Step 5: USER APPROVAL — intake.** Show the user, in chat, the **full content** of `brief.json`, `rubric.json`, `template.json`, `theme.json` and `agents/clinical-accuracy.json` (each in a fenced block; long files may be sent as files with `SendUserFile` in addition), followed by a table `file | SHA-256` computed with `python -c "from harness.hashing import hash_file; …"`. Ask: "Do you approve these five files at these hashes?" On explicit approval: add the DEC row (user's words and the five hashes) to `projects/ai-in-medicine/decisions.md` and `docs/harness/DECISIONS.md`; then:

```bash
python harness/run_stage.py --project projects/ai-in-medicine begin intake            # prints nonce=…
python harness/run_stage.py --project projects/ai-in-medicine complete intake --nonce <n>; echo "exit=$?"   # 0
python harness/run_stage.py --project projects/ai-in-medicine approve intake --dec DEC-NNN; echo "exit=$?"  # 0
```

`approve` re-hashes the files; if any differs from the table shown, it is not the approved set: stop and re-ask.
- [ ] **Step 6: USER APPROVAL — history import.** Write `projects/ai-in-medicine/history/import.json` (stage → historical input/output files: ingest = original DOCX → `original/*.md`, `images/*`; evaluate = original MD → `history/Review_Notes_AI_in_Medicine.pdf`, `history/VERDICT.md`, `history/EVALUATION_RUBRIC.md`; design = those → `docs/superpowers/specs/2026-09-24-interprofessional-rework-design.md` copied to `history/`, `design/*`; rework = design → chapters, glossary, errata, `rework/figures/**`). Show it with every file's SHA-256, and explain N2 (content-bound, one-shot, marked `imported`). On explicit approval: DEC row naming `import-history`, the four stages and the user's words; then `import-history ingest|evaluate|design|rework --dec DEC-NNN` (four calls, each exit 0).
- [ ] **Step 7: USER APPROVAL — design.** Show the full `design.md`, `chapter-plan.json`, `errata-seed.md` with SHA-256s. On explicit approval: DEC row; `approve design --dec DEC-NNN` → exit 0.
- [ ] **Step 8: Gates**

```bash
python harness/run_stage.py --project projects/ai-in-medicine verify --through intake; echo "exit=$?"   # 0
python harness/run_stage.py --project projects/ai-in-medicine verify --through rework; echo "exit=$?"   # 0, imported receipts listed as imported
python -m unittest discover -s tests -t . -v; echo "exit=$?"                                            # 0
```

- [ ] **Step 9: Commit (data)**

```bash
git add projects/ai-in-medicine/brief.json projects/ai-in-medicine/rubric.json projects/ai-in-medicine/template.json projects/ai-in-medicine/theme.json projects/ai-in-medicine/agents projects/ai-in-medicine/design projects/ai-in-medicine/history/import.json projects/ai-in-medicine/history/2026-09-24-interprofessional-rework-design.md projects/ai-in-medicine/decisions.md projects/ai-in-medicine/state.json docs/harness/DECISIONS.md
git commit -m "feat(ai-in-medicine): approved intake, history import and design (STEP 7 task 4, data)"
python harness/run_stage.py --project projects/ai-in-medicine verify --through rework; echo "exit=$?"   # still 0 after commit
git status --porcelain   # expect empty
```

### Task 7.5: `CLAUDE.md` split (own commit)

- [ ] **Step 1:** `cp CLAUDE.md projects/ai-in-medicine/CLAUDE.md && cmp CLAUDE.md projects/ai-in-medicine/CLAUDE.md; echo "cmp=$?"` → `cmp=0`.
- [ ] **Step 2:** Rewrite root `CLAUDE.md` (≤ 80 lines): what the harness is (the vision's six phases); layout pointer (core §1); how to run (`book-*` skills → `run_stage.py`); **Rule 7** (intake gate, design gate, never edit `state.json`, approvals only after explicit user approval with a DEC row); **Rule 8** (no domain literals in `harness/`); **Rule 11** (inline default, ≤ 2 Claude subagents with reasons, Codex excluded); per-project instructions live in `projects/<book>/CLAUDE.md`.
- [ ] **Step 3:** `git status --porcelain` → exactly ` M CLAUDE.md` and `?? projects/ai-in-medicine/CLAUDE.md`. Show the user `git diff CLAUDE.md` in chat (TICKET STEP 7 exit: diff reviewed).
- [ ] **Step 4: Commit**

```bash
git add CLAUDE.md projects/ai-in-medicine/CLAUDE.md
git commit -m "docs: split CLAUDE.md into harness root and ai-in-medicine project (STEP 7 task 5)"
git status --porcelain   # expect empty
```


**STEP 7 exit:** `python -m unittest tests.test_bypass_matrix -v` → 0; `CLAUDE.md` diff shown; onboarding DECs exist; `verify --through intake` → 0; Codex review (one pass over tasks 7.1–7.5, after all tests pass).

---

## STEP 8 — Generalise the tools and implement ingest

Common interfaces for STEP 8 (defined in Task 8.1, used by 8.2–8.4):
- `harness/tools/config.py`: `load(project: Path) -> Config` where `Config` is a `dict` with keys `brief, template, theme, chapter_plan, profile_out, profile_src` (profiles from `locale.load_profile` with `template.locale_overrides` merged); `Config.path(key) -> Path` resolves `template.paths.<key>` against the project.
- `harness/text.py`: `words(text, profile) -> int`; `tokens(text, profile) -> list[str]`; `sentences(text, profile) -> list[str]`; `normalise(text, profile, purpose: "compare"|"count") -> str`; `digits_value(s: str) -> int` (either system); `mixed_digits(s) -> bool`.
- `harness/tools/check_book.py`: `parse(text, cfg) -> Parsed` (`Parsed = {"h1": {num, title}, "sections": [{id, role, label, line, body}], "callouts": [{id, line, parts}], "objectives": [...], "mcqs": [...], "key": {...}, "citations": [...], "references": [...], "glossary_terms": [{term, gloss}]}`); `check_chapter(path, cfg, chapter) -> list[Check]`; `check_book(cfg) -> Report`; CLI `python harness/tools/check_book.py --project P [--chapter ID] [--json]` exit 0 iff no `fail`. `Check = {"id","status","message","measured"}`; `Report` is `checker-report.v1`.

### Task 8.1: Checker and assembler generalisation, positive-config fixtures, mutations, leak scan

**Files:**
- Create: `harness/text.py`, `harness/tools/config.py`, `harness/tools/check_book.py`, `harness/tools/assemble.py`, `harness/tools/leak_scan.py`, `tests/fixtures/positive-config/{no-mcq,no-glossary,no-cases,no-perspectives,no-errata}/`, `tests/fixtures/mutations/mutations.json`, `tests/fixtures/leak/clinical.txt` (the fixed clinical term list), `tests/fixtures/leak/forbidden.txt` (generated), `tests/tools/make_forbidden.py` (test-side, so the list never sits inside scanned code), `tests/fixtures/ai-in-medicine/allow-step8.json` (content `[]` in this task)
- Modify: `harness/tools/capture_golden.py` (harness mode, below), `harness/state.py` (`STAGES`: `rework` → `["harness/tools/check_book.py"]`; `build` → `["harness/tools/assemble.py"]`), `harness/registry.py` (rows: `check_book.py` gate `rework`, `assemble.py` gate `build`, `leak_scan.py` ungated)
- Test: `tests/test_text.py`, `tests/test_checker.py`, `tests/test_mutations.py`, `tests/test_positive_config.py`, `tests/test_assemble.py`, `tests/test_leak_scan.py`, `tests/test_golden.py` (harness-mode additions)

**Capture harness mode** (N1, N7, N8): without `--layout`, `capture_golden.py --project projects/<slug>` derives the layout from project config. Its sources are: `checks` from `harness/tools/check_book.py --json`; `verify_refs` from `harness/tools/verify_refs.py --json` when that file exists (Task 8.3), otherwise from the project's legacy `verify_refs.py`; `docx`/`pdf`/`hashes.docx*` from `--docx-from build|deliverables` (default `build`). Test `test_harness_mode_layout_from_config` asserts the derived layout for the medical config equals `layout-projects.json` except `deliverables`.

Port rule: each legacy function becomes a config-driven function with the same algorithm, replacing each literal by its INV target (core §10): `check_template` ← INV-10/12/13 (`template.sections[]`, `callouts[]`, `chapter_heading_pattern`); `check_lenses` ← INV-14 (`perspectives`); `check_los` ← INV-15; `check_mcqs` ← INV-16 (marker grammar constant, core §4.3); `check_citations` ← INV-17; `check_glossary` ← INV-18; `check_banned` ← INV-19 (+ `profile.banned_terms`); `check_budget` ← INV-09 (`chapter_plan.chapters[].word_budget`, `template.budgets.tolerance`); `check_sentences` ← INV-11 via `text.sentences(profile)`; `check_all` ← INV-20. Every disabled feature returns its IDs as `not_applicable`. `LO-UNASSESSED` and `MCQ-LO-UNKNOWN` port the legacy messages at `check_book.py:178,181`. IDs the legacy checker never computed (`TPL-CALLOUT-COUNT`, `READ-NOPROSE`, `BUDGET-FRONT`, `ASSET-*`) are new and handled by N7. `ASSET-MISSING`/`ASSET-OUTSIDE-ROOT` come from the path-relative resolver shared with `assemble.py` (`assemble.resolve_asset(chapter_file, link, cfg) -> Path`, core §1.1 asset model; fixes INV-40).

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
- [ ] **Step 3: Implement** `text.py`, `config.py`, `check_book.py` (port rule above; `--project` via `gate.enforce("rework", argv)` as its first call), `assemble.py` (same gate; output `build/<basename>.md`; path-relative asset rewrite via `os.path.relpath`), `tests/tools/make_forbidden.py` (reads `projects/ai-in-medicine/{template,theme,brief}.json` labels, title, subtitle, author names, plus `tests/fixtures/leak/clinical.txt`: `patient, clinical, clinician, physician, pharmacist, physiotherapy, radiology, pathology, diagnosis, medicine, medical, hospital, nurse`; writes `forbidden.txt`) and `leak_scan.py` (scope and patterns core §9.5; case-insensitive whole-word match; prints `path:line: literal`).
- [ ] **Step 4: Positive-config fixtures** — each is a complete small project (one 400-word chapter, template/theme/brief/rubric/chapter-plan, approvals and receipts stamped by `temp_repo`) with exactly one feature disabled.
- [ ] **Step 5: Run and golden check (checker fields, deliverables DOCX)** — `test_golden.py::test_checker_matches_step6` does this inside `temp_repo(project_from="projects/ai-in-medicine", stamp=True)`; the manual equivalent:

```bash
python -m unittest tests.test_text tests.test_checker tests.test_mutations tests.test_positive_config tests.test_assemble tests.test_leak_scan tests.test_golden -v; echo "exit=$?"   # 0
python tests/tools/make_forbidden.py && python harness/tools/leak_scan.py; echo "exit=$?"                                                                                   # 0
python -m unittest discover -s tests -t . -v; echo "exit=$?"                                                                                                                 # 0
```

The golden test captures with `--docx-from deliverables` and runs `compare_golden.diff(golden_step6, g, allow=[], checks_from=golden_step6)` → no diffs (N7: extra IDs must pass).
- [ ] **Step 6: Commit**

```bash
git add harness/text.py harness/tools/config.py harness/tools/check_book.py harness/tools/assemble.py harness/tools/leak_scan.py harness/tools/capture_golden.py harness/state.py harness/registry.py tests/tools tests/fixtures/positive-config tests/fixtures/mutations tests/fixtures/leak tests/fixtures/ai-in-medicine/allow-step8.json tests/test_text.py tests/test_checker.py tests/test_mutations.py tests/test_positive_config.py tests/test_assemble.py tests/test_leak_scan.py tests/test_golden.py
git commit -m "feat(harness): config-driven checker and assembler, positive-config, mutations, leak scan (STEP 8 task 1)"
git status --porcelain   # expect empty
```

### Task 8.2: Build generalisation

**Files:**
- Create: `harness/tools/build_book.py`, `harness/stages/build.py`, `tests/fixtures/ai-in-medicine/golden-step8.json` (generated in a temp repo, Step 5)
- Modify: `harness/state.py` (`STAGES`: `build` → `[assemble.py, build.py, build_book.py]`), `harness/stages/contracts.py` (build file sets), `harness/registry.py` (`build_book.py` gate `build`)
- Test: `tests/test_build.py`

Port rule: `build_book.py` consumes the checker's `Parsed` representation (INV-30) and `theme.json`; every literal replaced per INV-21…38; the DOCX element factory is **one** function `make_paragraph(doc, text_runs, style, theme)` / `make_run(p, text, theme, *, bold, italic)` / `make_table(...)` (EXT-LOC-2) that applies direction/lang from the theme (LTR only in this step). Output to `build/<basename>.docx|.pdf` (N3). Word COM backend kept (`DispatchEx`, hidden, TOC update, `ExportAsFixedFormat` with the current arguments `build_book.py:959`). `stages/build.py` = `run build`: render figures (placeholder call into `harness/figures/render.py` from STEP 9; until then it copies existing PNGs and records `figures: legacy`), assemble, build DOCX, PDF, write `build-report.json`.

- [ ] **Step 1: Failing test** — `tests/test_build.py::test_medical_build_matches_golden` (skipped unless `preflight.check_word()["ok"]`): inside `temp_repo(project_from="projects/ai-in-medicine", stamp=True)` (tests never touch the real project state, core §3) it runs `run_stage.py --project projects/ai-in-medicine run build`, captures, and compares with `golden-step6.json` under `allow-step8.json` → exit 0. Plus unit tests: `make_run` sets `w:lang` from `theme.lang_tag`; callout layouts come from `theme.callouts`.
- [ ] **Step 2: Run** — `python -m unittest tests.test_build -v` → exit 1.
- [ ] **Step 3: Implement** the port and `stages/build.py`.
- [ ] **Step 4: Run** — `python -m unittest tests.test_build -v` → exit 0 (the Word test is not skipped on this machine: `python harness/preflight.py --group build` → 0 first).
- [ ] **Step 5: Regression evidence, in a temp repo (no real-project state changes in STEP 8):** `tests/test_build.py::test_medical_build_matches_golden` writes its capture to `$HARNESS_EVIDENCE_OUT` when that variable is set:

```bash
HARNESS_EVIDENCE_OUT=tests/fixtures/ai-in-medicine/golden-step8.json python -m unittest tests.test_build.BuildTest.test_medical_build_matches_golden -v; echo "exit=$?"   # 0
python harness/tools/compare_golden.py tests/fixtures/ai-in-medicine/golden-step6.json tests/fixtures/ai-in-medicine/golden-step8.json --allow tests/fixtures/ai-in-medicine/allow-step8.json --checks-from tests/fixtures/ai-in-medicine/golden-step6.json; echo "exit=$?"   # 0, allowlist still []
python -m unittest discover -s tests -t . -v; echo "exit=$?"   # 0
```

If the DOCX part hashes differ, the port is not faithful: fix the builder (the diff names the part), never widen the allowlist.
- [ ] **Step 6: Commit**

```bash
git add harness/tools/build_book.py harness/stages/build.py harness/stages/contracts.py harness/state.py harness/registry.py tests/test_build.py tests/fixtures/ai-in-medicine/golden-step8.json
git commit -m "feat(harness): config-driven build (STEP 8 task 2)"
git status --porcelain   # expect empty
```

### Task 8.3: `verify_refs` policy fix

**Files:** Create `harness/tools/verify_refs.py`, `harness/tools/renumber_refs.py`; Create `harness/stages/complete_checks/rework.py` (`rework` completer; `rework` tool_paths → `[harness/tools/check_book.py, harness/tools/verify_refs.py, harness/stages/complete_checks/rework.py]`), `harness/stages/contracts.py` (rework unit file sets), `harness/state.py` (`STAGES`: `rework` as above), `harness/registry.py` (`verify_refs.py`, `renumber_refs.py` gate `rework`), `tests/fixtures/ai-in-medicine/allow-step8.json`, `tests/fixtures/ai-in-medicine/golden-step8.json`; Test `tests/test_verify_refs.py`, `tests/test_rework_complete.py`

**Rework completer** (core §2.2 rework row; now possible because the checker and `verify_refs` exist): `complete_checks.rework(project, active_run, unit)` — with `unit`: runs `check_book.check_chapter` for that chapter (zero `fail`) and `verify_refs.check_chapter` (zero blocking `check_id`); extras `{checker_report_sha256, verify_refs_summary {ok, no_doi_allowed, …}}`. Without `unit` (final): every chapter in `chapter-plan.json` has a valid unit receipt; book-level checks pass (`BOOK-*`, `BUDGET-TOTAL`, `ERRATA-OPEN` where enabled, `GLOSS-MIN`); when translation applies, TR §4.3 `TR-TARGET-UNMAPPED` via `check_translation` (Task 11.1 wires it; until then translation projects cannot complete rework, which is correct because STEP 11 does not exist yet). Tests (`tests/test_rework_complete.py`, positive-config project in a temp repo): unit completion with a failing chapter → exit 1 naming the check ID; all units then final → exit 0 and one stage receipt whose `units` has every chapter; final with one unit missing → exit 1 `UNIT-MISSING`; a second unit completion inside the same lease works (lease kept).

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

- [ ] **Step 2: Run** — `python -m unittest tests.test_verify_refs tests.test_rework_complete -v` → exit 1.
- [ ] **Step 3: Implement** the ports (config-driven, gated `rework`) and the rework completer.
- [ ] **Step 4: Run** — same command → exit 0.
- [ ] **Step 5: Regression evidence (temp repo, network):** re-run the Task 8.2 evidence command so `golden-step8.json` now carries the harness `verify_refs` results. The medical no-DOI references now pass by policy (the `allowed_types` the user approved in Task 7.4) or report `REF-NO-DOI-DISALLOWED`. Set `allow-step8.json` to exactly:

```json
[{"pointer_glob": "/verify_refs/*/status", "reason": "verify_refs no-DOI policy fix (TICKET STEP 8)"}]
```

```bash
HARNESS_EVIDENCE_OUT=tests/fixtures/ai-in-medicine/golden-step8.json python -m unittest tests.test_build.BuildTest.test_medical_build_matches_golden -v; echo "exit=$?"   # 0
python harness/tools/compare_golden.py tests/fixtures/ai-in-medicine/golden-step6.json tests/fixtures/ai-in-medicine/golden-step8.json --allow tests/fixtures/ai-in-medicine/allow-step8.json --checks-from tests/fixtures/ai-in-medicine/golden-step6.json --out "$(mktemp -d)/d.json"; echo "exit=$?"   # 0
```

Every allowed diff must be a `no_doi` entry (check the printed `ALLOWED` pointers against the STEP 6 golden's `no_doi` list). If any reference becomes `REF-NO-DOI-DISALLOWED`, record it for the user in `projects/ai-in-medicine/decisions.md` as a finding (chapters are not edited: scope lock).
- [ ] **Step 6: Commit**

```bash
git add harness/tools/verify_refs.py harness/tools/renumber_refs.py harness/stages/complete_checks harness/stages/contracts.py harness/state.py harness/registry.py tests/test_verify_refs.py tests/test_rework_complete.py tests/fixtures/ai-in-medicine/allow-step8.json tests/fixtures/ai-in-medicine/golden-step8.json projects/ai-in-medicine/decisions.md
git commit -m "fix(harness): verify_refs enforces the no-DOI policy; rework completer (STEP 8 task 3)"
git status --porcelain   # expect empty
```

### Task 8.4: Ingest and fidelity

**Files:** Create `harness/tools/convert_docx.py`, `harness/stages/ingest.py`, `tests/fixtures/ingest/*.docx` + `*.expected.json`, `tests/fixtures/ingest/make_fixtures.py`; Modify `harness/state.py` (`STAGES`: `ingest` → `["harness/stages/ingest.py", "harness/tools/convert_docx.py"]`), `harness/stages/contracts.py` (ingest file sets), `harness/registry.py` (`convert_docx.py` gate `ingest`); Test `tests/test_ingest.py`

**Interfaces:** `convert_docx.convert(docx: Path, cfg) -> (markdown: str, assets: dict[str, bytes], report: dict)`; `ingest.run(project) -> (inputs, outputs, extras)` used by `run_stage.py run ingest`: copies `brief.source.files[]` into `source/` (custody; hashes must equal `brief.source.files[].sha256`), writes `source-manifest.json`, converts (DOCX native; other formats via `markitdown` if importable, else exit 1 naming it), writes `ingest/normalized.md`, `ingest/units.json` (TR §4.1: `src-chNN`, `src-chNN-sMM` by document order, line spans, sha256 of the span text), `ingest/assets/*`, `ingest/conversion-report.json` (core §2.4 incl. `omitted[]`); exit 2 if any structure `lost`.

**Atomic commit of outputs** (core §2.2 ingest row): everything is written to a complete sibling staging tree `.ingest-stage/` (`source/`, `source-manifest.json`, `ingest/`), validated (schemas, custody hashes, no `lost`), then swapped with `swap_dirs(project, pairs)`: for each pair it renames the live item to `.ingest-old/<name>` and the staged item into place; if any rename fails it renames every already-moved item back (rollback) and re-raises; on success it deletes `.ingest-old/`. A leftover `.ingest-old/` at the next run means a crash mid-swap: `run ingest` refuses with `ERROR INGEST-RECOVERY` naming it, and the user decides (never silently deleted).

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

- [ ] **Step 1: Failing tests** — one test per fixture asserting the literal expected report; `test_units_ids_in_document_order`; `test_lost_structure_keeps_previous_outputs` (exit 2, live tree byte-identical to before); `test_failure_during_swap_rolls_back` (patch `os.replace` to raise on its second call → live tree identical to before, no `.ingest-stage` promoted); `test_leftover_old_dir_refuses` (`ERROR INGEST-RECOVERY`); `test_medical_ingest_has_no_lost` (in `temp_repo(project_from="projects/ai-in-medicine", stamp=True)`: `verify --through intake` exits 0 first, then a fresh ingest into a **copy** of the project with its downstream receipts removed → exit 0, no `lost`).
- [ ] **Step 2: Run** — `python -m unittest tests.test_ingest -v` → exit 1.
- [ ] **Step 3: Implement** (port `convert_docx_to_md.py`, replacing INV-01…07 literals by `template.ingest.*`/`paths.*`; INV-05/07 removed).
- [ ] **Step 4: Run** — `python -m unittest tests.test_ingest -v; echo "exit=$?"` → 0; `python -m unittest discover -s tests -t . -v; echo "exit=$?"` → 0; `python harness/tools/leak_scan.py; echo "exit=$?"` → 0.
- [ ] **Step 5: Commit**

```bash
git add harness/tools/convert_docx.py harness/stages/ingest.py harness/stages/contracts.py harness/state.py harness/registry.py tests/fixtures/ingest tests/test_ingest.py
git commit -m "feat(harness): ingest stage with fidelity report, units and atomic swap (STEP 8 task 4)"
git status --porcelain   # expect empty
```

**STEP 8 exit:** `python -m unittest discover -s tests -t . -v` → 0 (mutations yield their IDs with non-zero checker exit); `compare_golden.py golden-step6.json golden-step8.json --allow allow-step8.json --checks-from golden-step6.json` → 0 with the allowlist containing **only** the `verify_refs` glob (provenance is never compared, N8; new IDs must pass, N7); positive-config pass; `python harness/tools/leak_scan.py` → 0; `python harness/run_stage.py --project projects/ai-in-medicine verify --through rework` → 0 after the last commit; Codex review.

---

## STEP 9 — Figure system and chemistry pack

### Task 9.1: Manifest, renderer, charts, checker

**Files:**
- Create: `harness/figures/{__init__,render,charts,check_figures,png}.py`, `harness/figures/packs/__init__.py`, `tests/fixtures/figures-book/` (a small valid project with the figures listed in Task 9.3 minus chemistry), `tests/test_figures.py`
- Modify: `harness/schemas/figures.v1.json` (final fields, core §7.1), `harness/stages/build.py` (render + check before assembling), `harness/stages/contracts.py` (build outputs `figures/out/*`), `harness/state.py` (`STAGES`: `build` += `harness/figures`), `harness/registry.py` (`render.py`, `check_figures.py` gate `build`)

**Interfaces:**
- `packs.registry() -> dict[str, module]`: the built-in `charts` plus each package directory under `harness/figures/packs/`.
- `png.write_canonical(image: PIL.Image.Image, path, dpi: int) -> None`: saves with Pillow using fixed parameters (`optimize=False`, `compress_level=9`, `pnginfo` containing only `dpi`), and no time or text chunks, so identical pixels produce **identical bytes**. Every PNG the harness writes goes through it.
- `charts.render(spec_path, out_svg, out_png, width_cm, dpi=300)`: runs the figure's Python source in a subprocess with `MPLBACKEND=Agg`, `rcParams["svg.hashsalt"] = "harness"`, `svg.fonttype = "none"`, `savefig(metadata={"Date": None, "Creator": None})`; the PNG is rasterised by matplotlib then re-encoded through `png.write_canonical`.
- `render.render_all(project, cfg) -> list[dict]` (`{id, svg, png, status, versions}`, where `versions` holds matplotlib, Pillow, RDKit and browser versions, recorded in `build-report.json`). Hand SVGs are rasterised by the headless browser (`--headless --disable-gpu --hide-scrollbars --screenshot=<png> --window-size=<w>,<h> --force-device-scale-factor=<dpi/96> <svg>`), then re-encoded through `png.write_canonical`.
- `check_figures.check(project, cfg) -> Report` (checker-report.v1) with `FIG-UNREFERENCED, FIG-UNKNOWN, FIG-CAPTION, FIG-ALT, FIG-LICENCE, FIG-RESOLUTION, FIG-AUTHOR-ASSET` (core §7.3) and, from Task 9.2, the chemistry IDs with the core §7.5 effects. Numbering is computed by order of first reference.
- CLI: `python harness/figures/render.py --project P` and `python harness/figures/check_figures.py --project P [--json]` (gate `build`); exit 0 iff no blocking ID.

- [ ] **Step 1: Failing tests** (`tests/test_figures.py`, all in `temp_repo("figures-book", slug="figures-book", stamp=True)`):
  - `test_chart_bytes_identical`: render twice; SVG bytes equal **and** PNG bytes equal.
  - `test_svg_raster_bytes_identical`: hand SVG through the browser twice; PNG bytes equal.
  - `test_each_fig_id`: one fixture defect per ID (7 subtests) → that ID `fail`, exit 1.
  - `test_numbering_by_first_reference`: `Figure 2.1` goes to the first figure referenced in chapter 2, not the first one in the manifest.
  - `test_needs_author_asset_blocks_build`: `run build` → exit 1 naming `FIG-AUTHOR-ASSET`.
  - `test_png_300dpi_at_text_width`: PNG `dpi == (300, 300)` and width in pixels equals `round(theme.layout.text_width / 2.54 * 300)`.
- [ ] **Step 2: Run** — `python -m unittest tests.test_figures -v; echo "exit=$?"` → 1.
- [ ] **Step 3: Implement.**
- [ ] **Step 4: Run** — `python -m unittest tests.test_figures -v; echo "exit=$?"` → 0; `python -m unittest discover -s tests -t . -v; echo "exit=$?"` → 0 (the Task 8.2 golden test still passes: the medical figures are `raster.existing`, whose bytes are copied unchanged).
- [ ] **Step 5: Commit**

```bash
git add harness/figures harness/schemas/figures.v1.json harness/stages/build.py harness/stages/contracts.py harness/state.py harness/registry.py tests/fixtures/figures-book tests/test_figures.py
git commit -m "feat(harness): figure manifest, deterministic rendering, figure checker (STEP 9 task 1)"
git status --porcelain   # expect empty
```


### Task 9.2: Chemistry pack

**Files:** Create `harness/figures/packs/chemistry/{__init__,pubchem}.py`, `requirements-chemistry.txt` (`rdkit==<the version installed in Step 1>`); Modify `harness/figures/check_figures.py` (chemistry IDs and their core §7.5 effects), `harness/stages/complete_checks/audit.py` (`CHEM-UNVERIFIED` gate); Test `tests/test_chemistry.py`

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
            spec = {"kind": "chem.structure", "smiles": "CC(=O)Oc1ccccc1C(=O)O", "name": "aspirin"}
            chem.render(spec, svg, png)
            first = (svg.read_bytes(), png.read_bytes())
            chem.render(spec, svg, png)
            self.assertEqual((svg.read_bytes(), png.read_bytes()), first)   # byte-identical re-render
            self.assertTrue(first[0].startswith(b"<?xml"))

    def test_reaction_render_bytes_identical(self):
        import tempfile, pathlib
        with tempfile.TemporaryDirectory() as t:
            svg, png = pathlib.Path(t, "r.svg"), pathlib.Path(t, "r.png")
            spec = {"kind": "chem.reaction", "smarts": "CCO>>CC=O", "name": "oxidation"}
            chem.render(spec, svg, png); first = (svg.read_bytes(), png.read_bytes())
            chem.render(spec, svg, png)
            self.assertEqual((svg.read_bytes(), png.read_bytes()), first)

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

- [ ] **Step 3: Run** — `python -m unittest tests.test_chemistry -v; echo "exit=$?"` → 1 (module missing).
- [ ] **Step 4: Implement** (`KINDS`, `preflight`, `validate` with `Chem.MolFromSmiles(sanitize=False)` then `Chem.SanitizeMol` → `CHEM-SANITIZE`; `render` via `rdMolDraw2D.MolDraw2DSVG` (fixed size from the theme text width, `drawOptions().fixedFontSize`, no timestamps) and `MolDraw2DCairo` for the PNG, re-encoded through `png.write_canonical` at 300 dpi; reactions via `AllChem.ReactionFromSmarts` + `Draw.ReactionToImage`/`MolDraw2D.DrawReaction`; `crosscheck` compares canonical SMILES from PubChem `.../compound/name/<name>/property/CanonicalSMILES/JSON` (timeout 10 s, cache `figures/.cache/pubchem/<sha256(name)>.json`); stage effects per core §7.5 wired into `check_figures` and the audit completer).
- [ ] **Step 5: Run** — `python -m unittest tests.test_chemistry -v; echo "exit=$?"` → 0 with **no skips** (`chem.preflight() == []` after Step 1); `python -m unittest discover -s tests -t . -v; echo "exit=$?"` → 0.
- [ ] **Step 6: Commit**

```bash
git add harness/figures/packs/chemistry requirements-chemistry.txt harness/figures/check_figures.py harness/stages/complete_checks/audit.py tests/test_chemistry.py
git commit -m "feat(harness): chemistry pack with RDKit and PubChem cross-check (STEP 9 task 2)"
git status --porcelain   # expect empty
```

### Task 9.3: Visual evidence

**Files:** Create `docs/harness/reviews/step9-evidence/{bar-chart,line-chart,diagram,aspirin,caffeine,ethanol-oxidation}.png`, `tests/fixtures/figures-book/figures/src/*` (the chemistry specs are added to the Task 9.1 fixture), `tests/tools/make_step9_evidence.py`

- [ ] **Step 1:** Add to `figures-book`: one bar chart, one line chart, one hand SVG diagram, two `chem.structure` (aspirin `CC(=O)Oc1ccccc1C(=O)O`, caffeine `Cn1cnc2c1c(=O)n(C)c(=O)n2C`), one `chem.reaction` (`CCO>>CC=O`).
- [ ] **Step 2:** `python tests/tools/make_step9_evidence.py; echo "exit=$?"` → 0. The script renders the fixture in a temp repo and copies the six PNGs to `docs/harness/reviews/step9-evidence/`.
- [ ] **Step 3:** Open each PNG with the Read tool and check it: legible labels, correct structures, nothing clipped. Fix defects, then repeat Step 2.
- [ ] **Step 4:** `python -m unittest discover -s tests -t . -v; echo "exit=$?"` → 0.
- [ ] **Step 5: Commit**

```bash
git add docs/harness/reviews/step9-evidence tests/fixtures/figures-book tests/tools/make_step9_evidence.py
git commit -m "docs(harness): STEP 9 visual evidence"
git status --porcelain   # expect empty
```

The STEP 9 Codex brief lists all six PNG paths and requires a per-file verdict from Codex.

**STEP 9 exit:** all tests pass, including the invalid SMILES; evidence committed; Codex review done and every PNG inspected.

---

## STEP 10 — Arabic locale

### Task 10.1: `ar.json`, tokenizer, sentences, digits, calibration

**Files:**
- Create: `harness/locale/ar.json`, `harness/tools/calibrate.py`, `tests/fixtures/locale/ar/{tokenize,sentences,digits}/*.json`, `tests/fixtures/locale/ar/parallel/{pairs.tsv,SOURCE.md}`, `tests/test_locale_ar.py`
- Modify: `harness/text.py` (`unicode-word` tokenizer, Arabic sentence rules, digits), `harness/tools/check_book.py` (`AR-DIGIT-MIXED`, `AR-DIGIT-INCONSISTENT`, citation parsing with both digit systems and the `،` separator), `harness/registry.py` (`calibrate.py` ungated)

Corpus: at least 500 human-authored EN–AR aligned pairs from an openly licensed source (a UN Parallel Corpus sample or OPUS Tatoeba). Fetch it once with WebFetch, store it as `pairs.tsv`, and record the licence, URL and date in `SOURCE.md` (AR §2.1). If no openly licensed source is reachable, stop and ask the user.

Case-file format (every corpus directory): `{"cases": [{"name": str, "input": str, "expect": <int | list[str] | {"present": [ids], "absent": [ids]}>}]}`.

- [ ] **Step 1: Failing tests**

```python
# tests/test_locale_ar.py
import json, pathlib, unittest
from harness import text
from harness.locale import load_profile
from harness.tools import calibrate, check_book

CORPUS = pathlib.Path(__file__).resolve().parent / "fixtures/locale/ar"
AR, EN = load_profile("ar"), load_profile("en")
CFG_AR = {"profile_out": AR, "template": {"citations": {"style": "numeric-bracket"}}}


def cases(kind):
    for f in sorted((CORPUS / kind).glob("*.json")):
        yield from json.loads(f.read_text(encoding="utf-8"))["cases"]


class ArabicText(unittest.TestCase):
    def test_tokenize_corpus(self):
        for c in cases("tokenize"):
            with self.subTest(c["name"]):
                self.assertEqual(text.words(c["input"], AR), c["expect"])

    def test_sentence_corpus(self):
        for c in cases("sentences"):
            with self.subTest(c["name"]):
                self.assertEqual(text.sentences(c["input"], AR), c["expect"])

    def test_digit_corpus(self):
        for c in cases("digits"):
            with self.subTest(c["name"]):
                ids = {x["id"] for x in check_book.check_digits(c["input"], CFG_AR) if x["status"] == "fail"}
                self.assertTrue(set(c["expect"]["present"]) <= ids)
                self.assertFalse(set(c["expect"]["absent"]) & ids)

    def test_arabic_citation_digits(self):
        self.assertEqual(check_book.cited_numbers("كما ذكر [١، ٣-٥].", CFG_AR), [1, 3, 4, 5])

    def test_mixed_number_fails(self):
        ids = {c["id"] for c in check_book.check_digits("القيمة 1٢ مرتفعة.", CFG_AR) if c["status"] == "fail"}
        self.assertIn("AR-DIGIT-MIXED", ids)

    def test_calibration_reproducible(self):
        pairs = calibrate.load_pairs(CORPUS / "parallel/pairs.tsv")
        self.assertGreaterEqual(len(pairs), 500)
        out = calibrate.compute(EN, AR, pairs)
        for k in ("mean_sentence_max", "long_sentence_words", "long_share_max"):
            self.assertEqual(out[k], AR["readability"][k], k)

    def test_primary_subtag_selects_profile(self):
        self.assertEqual(load_profile("ar-EG")["tag"], "ar")
```

- [ ] **Step 2: Run** — `python -m unittest tests.test_locale_ar -v; echo "exit=$?"` → 1.
- [ ] **Step 3: Implement** AR §2 exactly (tokenizer categories, clitics kept, terminators, abbreviations, decimals, digits via `unicodedata.digit`). Write the corpus cases, then run `python harness/tools/calibrate.py --en harness/locale/en.json --pairs tests/fixtures/locale/ar/parallel/pairs.tsv` and paste its output (`r`, the three values, `provenance`) into `ar.json` `readability`.
- [ ] **Step 4: Run** — `python -m unittest tests.test_locale_ar -v; echo "exit=$?"` → 0; `python -m unittest discover -s tests -t . -v; echo "exit=$?"` → 0 (English behaviour unchanged: `test_text.py` still equals the legacy counts).
- [ ] **Step 5: Commit**

```bash
git add harness/locale/ar.json harness/tools/calibrate.py harness/text.py harness/tools/check_book.py harness/registry.py tests/fixtures/locale/ar tests/test_locale_ar.py
git commit -m "feat(harness): Arabic locale profile, tokenizer, sentences, digits, calibration (STEP 10 task 1)"
git status --porcelain   # expect empty
```

### Task 10.2: Labels, objectives, glossary, headings, reference policy

**Files:**
- Create: `harness/schemas/references-manual.v1.json`, `tests/fixtures/locale/ar/{labels,objectives,glossary,references}/`, `tests/test_locale_ar_book.py`
- Modify: `harness/tools/check_book.py`, `harness/tools/verify_refs.py`, `harness/locale/__init__.py` (heading-pattern expansion), `harness/stages/contracts.py` (`references-manual.json` as a rework input)

- [ ] **Step 1: Failing tests** (`tests/test_locale_ar_book.py`):
  - `test_heading_expansion`: the five AR §2.2 headings parse to `num` 3, 3, 3, 3, 11. `# الفصل: …` (no number) does not match.
  - `test_labels_book_passes`: in `temp_repo("locale/ar/labels", slug="ar-labels", stamp=True)`, `check_book.py --project projects/ar-labels --json` → exit 0; parsed section IDs equal the literal list in `labels/expected.json`.
  - `test_discouraged_verbs`: every line listed in `objectives/cases.json` gets `LO-VERB`, and the clean line does not.
  - `test_glossary_gloss`: `**التعلم الآلي** (machine learning)` → `{term: "التعلم الآلي", gloss: "machine learning"}`; a term with harakat matches the glossary entry without them.
  - `test_reference_pairs`: each `references/cases.json` case gives its literal `(doi_status, title_status)` pair (mocked fetch), including `manual_pending` when the marker is missing and `manual_ok` when a `references-manual.json` entry exists with a valid `dec_row_sha256`.
  - `test_manual_record_edit_stales_rework`: editing a `references-manual.json` entry makes `verify --through rework` report the file as changed.
- [ ] **Step 2: Run** — `python -m unittest tests.test_locale_ar_book -v; echo "exit=$?"` → 1.
- [ ] **Step 3: Implement** AR §2.2, §4 and §5.
- [ ] **Step 4: Run** — `python -m unittest tests.test_locale_ar_book -v; echo "exit=$?"` → 0; the full suite → 0.
- [ ] **Step 5: Commit**

```bash
git add harness/schemas/references-manual.v1.json harness/tools/check_book.py harness/tools/verify_refs.py harness/locale/__init__.py harness/stages/contracts.py tests/fixtures/locale/ar tests/test_locale_ar_book.py
git commit -m "feat(harness): Arabic labels, headings, glossary gloss, reference policy (STEP 10 task 2)"
git status --porcelain   # expect empty
```

### Task 10.3: RTL rendering, preset, DOCX assertions, evidence

**Files:**
- Create: `harness/presets/rtl-textbook.json` (`required_font_files: ["majalla.ttf","majallab.ttf","segoeui.ttf"]`), `tests/fixtures/locale/ar/book/` (the `labels/` book as a full project, including a table, a bulleted list, a numbered list, header/footer text, a mixed-script paragraph with an English term, a DOI, a URL, an inline formula, a percentage, a parenthesised citation, and one display equation), `tests/fixtures/locale/ar/docx/assertions.json`, `tests/test_rtl_docx.py`, `tests/tools/make_step10_evidence.py`, `docs/harness/reviews/step10-evidence/{toc,table,list,mixed-script}.png`
- Modify: `harness/tools/build_book.py` (the single element factory gains RTL: AR §3 row by row)

`assertions.json` items are `{"part": <zip path or glob>, "xpath": str, "expect": "present" | "absent" | {"equals": str} | {"count_min": int}}`. The test loads **every** part the glob names: `word/document.xml`, `word/styles.xml`, `word/settings.xml`, `word/numbering.xml`, `word/header*.xml`, `word/footer*.xml`, `docProps/core.xml`. There is at least one item per AR §3 row: docDefaults `w:lang/@w:bidi`; `w:themeFontLang/@w:bidi`; `w:bidi` on body paragraphs; `w:rtl` on Arabic runs and its absence on Latin runs; `w:szCs`; `w:rFonts/@w:cs` equal to `complex_script` in docDefaults and to `complex_script_heading` in heading, caption, header/footer and TOC styles; `w:bCs`; `w:bidiVisual`; `w:sectPr/w:bidi`; `w:pgNumType/@w:fmt`; `w:numFmt` in `numbering.xml`; `w:bidi` in every header and footer paragraph; the TOC field instruction; the display-equation paragraph with no `w:bidi` and `m:jc` centred; LRM (U+200E) beside the DOI run; `dc:language`.

- [ ] **Step 1: Failing test** — `tests/test_rtl_docx.py::test_assertions`: builds the fixture book in `temp_repo("locale/ar/book", slug="ar-book", stamp=True)` with `run build`, then evaluates each assertion (lxml, namespaces `w`, `m`, `dc`) and reports each failure as `part xpath`. `test_ltr_unchanged`: the medical golden test (Task 8.2) still passes.
- [ ] **Step 2: Run** — `python -m unittest tests.test_rtl_docx -v; echo "exit=$?"` → 1.
- [ ] **Step 3: Implement** AR §3 inside `make_paragraph` / `make_run` / `make_table` / section, style, numbering and header/footer setup. Split bidi runs with `unicodedata.bidirectional`.
- [ ] **Step 4: Run** — `python -m unittest tests.test_rtl_docx -v; echo "exit=$?"` → 0; `python harness/preflight.py --group build; echo "exit=$?"` → 0 (Arabic fonts present); the full suite → 0.
- [ ] **Step 5: Evidence** — `python tests/tools/make_step10_evidence.py; echo "exit=$?"` → 0. The script builds the fixture's PDF in a temp repo, renders the pages that hold the TOC, the table, the lists and the mixed-script paragraph to PNG with PyMuPDF (`fitz`, installed; used only for evidence) at 150 dpi, and saves the four files. Open each with the Read tool and check the reading order, the right-side list markers, the right-to-left table columns and the DOI/formula order.
- [ ] **Step 6: Commit**

```bash
git add harness/presets/rtl-textbook.json harness/tools/build_book.py tests/fixtures/locale/ar tests/test_rtl_docx.py tests/tools/make_step10_evidence.py docs/harness/reviews/step10-evidence
git commit -m "feat(harness): RTL DOCX rendering, rtl-textbook preset, Arabic evidence (STEP 10 task 3)"
git status --porcelain   # expect empty
```

**STEP 10 exit:** the Arabic fixture passes the checker (`test_labels_book_passes`); it builds DOCX and PDF (`test_rtl_docx`); the four evidence pages are committed; the Codex review inspected them.

---

## STEP 11 — Translation, both directions

### Task 11.1: Schemas and `check_translation.py`

**Files:**
- Create: `harness/schemas/{termbase,termbase-proposals,termbase-additions,trace}.v1.json` (the three termbase forms are separate files because the schema subset has no `$ref`), `harness/tools/check_translation.py`, `tests/test_translation_checks.py`
- Modify: `harness/state.py` (`STAGES`: `translate` → `["harness/tools/check_translation.py"]`), `harness/registry.py` (gate `translate`), `harness/stages/complete_checks/rework.py` (final rework runs `TR-TARGET-UNMAPPED` and `TB-REJECTED-PRESENT` when translation applies; `rework` tool_paths += `check_translation.py`)

**Interfaces:** `check_translation.check(project, cfg, unit=None) -> Report` with IDs `TB-TERM-MISSING, TB-FORBIDDEN-VARIANT, TB-DNT-ALTERED, TB-GLOSS-MISSING, TB-REJECTED-PRESENT, PRES-CITATION, PRES-IDENTIFIER, PRES-PROTECTED, PRES-FIGURE, PRES-LATIN-TERM, TR-UNIT-MISSING, TR-UNIT-STALE, TR-ORPHAN, TR-TARGET-UNMAPPED` (TR §4.3, §5). Source text uses `profile_src` and target text `profile_out`; unprotected numbers go to `notes[]`. `check_translation.trace_problems(map: dict) -> list[str]` enforces the TR §4.2 `kind` rules in code (the subset has no conditionals). CLI `python harness/tools/check_translation.py --project P [--unit ID] [--json]`, exit 0 iff no `fail`.

- [ ] **Step 1: Failing tests** — one synthetic en-ar unit pair per ID, each asserting that exact ID fails (14 subtests) plus a clean pair with zero failures; `trace_problems` cases: a translation-kind entry carrying `relation` fails; a final-kind `dropped` entry without target fields passes; a final-kind `translated` entry without `translation_sha256` fails.
- [ ] **Step 2: Run** — `python -m unittest tests.test_translation_checks -v; echo "exit=$?"` → 1.
- [ ] **Step 3: Implement.**
- [ ] **Step 4: Run** — same → 0; the full suite → 0.
- [ ] **Step 5: Commit**

```bash
git add harness/schemas/termbase.v1.json harness/schemas/termbase-proposals.v1.json harness/schemas/termbase-additions.v1.json harness/schemas/trace.v1.json harness/tools/check_translation.py harness/state.py harness/registry.py harness/stages/complete_checks/rework.py tests/test_translation_checks.py
git commit -m "feat(harness): termbase/trace schemas and translation checks (STEP 11 task 1)"
git status --porcelain   # expect empty
```

### Task 11.2: Translate stage, `terms resolve`, review gate

**Files:**
- Create: `harness/stages/complete_checks/translate.py`, `tests/test_translate_stage.py`
- Modify: `harness/stages/contracts.py` (translate unit and stage file sets per TR §2; rework and audit conditional inputs per core §2.2), `harness/run_stage.py` (`terms resolve`), `harness/stages/complete_checks/audit.py` (`TB-PROPOSAL-OPEN`, translation evidence in `codex_audited_inputs`), `harness/state.py` (`STAGES`: `translate` += `complete_checks/translate.py`), `harness/registry.py` (`terms resolve` runner row)

**Interfaces:**
- `begin translate --author-model NAME` (required for translate; `ERROR AUTHOR-MODEL-REQUIRED` if missing). It is stored in `active_run.author_model` and copied into every translate receipt.
- `complete translate --unit U --nonce N`: runs `check_translation --unit U`; zero `fail` → unit receipt (lease kept).
- `complete translate --nonce N` (final): every unit in `contracts.units(project, "translate")` is valid; `translation/codex-review.md` exists (else `TR-REVIEW-MISSING`); `review_header(...)["reviewer_model"]` is non-empty (else `TR-REVIEW-MISSING`, message "reviewer_model missing") and differs from `active_run.author_model` (else `TR-REVIEW-SAME-MODEL`, via `state.check_independent(author, reviewer)`, EXT-TR-4); every blocker/major row is closed, with rulings carrying a DEC (else `TR-REVIEW-OPEN` / `RULING-NO-DEC`).
- `terms resolve --dec DEC-NNN` (gate `rework`): reads `terms/resolve-request.json` (`[{proposal_id, status, entry}]`, which Claude writes from the user's chat answer); every `proposal_id` must exist in a proposals file (else `ERROR PROPOSAL-UNKNOWN`); appends the resolutions with `dec_id` and `dec_row_sha256` to `termbase-additions.json`; deletes the request file.

- [ ] **Step 1: Failing tests** (`tests/test_translate_stage.py`, in temp repos over a small en-ar project): `TR-REVIEW-SAME-MODEL` (author `claude`, header `reviewer_model: claude`); `TR-REVIEW-MISSING` for a missing file and for a missing `reviewer_model` line; `AUTHOR-MODEL-REQUIRED`; `TR-REVIEW-OPEN` for an open major row; `RULING-NO-DEC` for a bare ruling; `complete audit` → `TB-PROPOSAL-OPEN` with one unresolved proposal; resolving it makes `verify --through rework` report `termbase-additions.json` changed, and after re-completing rework it reports nothing (convergence); TR §9 criterion 6 (`ar-EG → en-GB` accepted as `ar-en`, `en-GB → en-US` not translation, `fr → ar` refused with `TR-PAIR-UNSUPPORTED`).
- [ ] **Step 2: Run** — `python -m unittest tests.test_translate_stage -v; echo "exit=$?"` → 1.
- [ ] **Step 3: Implement.**
- [ ] **Step 4: Run** — same → 0; `python -m unittest tests.test_bypass_matrix -v; echo "exit=$?"` → 0 (the new runner rows are covered); the full suite → 0.
- [ ] **Step 5: Commit**

```bash
git add harness/stages/complete_checks harness/stages/contracts.py harness/run_stage.py harness/state.py harness/registry.py tests/test_translate_stage.py
git commit -m "feat(harness): translate stage, terms resolve, review gate (STEP 11 task 2)"
git status --porcelain   # expect empty
```

### Task 11.3: EN→AR and AR→EN fixtures with real reviews (USER SEES OUTPUTS)

**Files:** Create `tests/fixtures/translation/{en-ar,ar-en}/`, as specified in TR §9: two chapters, at least four H2 units, a table, a figure reference, a DOI reference, a formula or SMILES string, one `dnt` term, one `gloss_first_use` term, both trace maps, a proposals file with one accepted and one rejected proposal plus its resolution record, and `translation/codex-review.md` and `translation/fixes.md`. Also create `tests/test_translation_fixtures.py` and `tests/tools/build_translation_fixtures.py`.

- [ ] **Step 1: Failing test** — `tests/test_translation_fixtures.py` runs, for **both** directions in temp repos, TR §9 criteria 1–4 and 6: the good fixture passes, and each listed mutation yields its named ID with a non-zero checker exit. Run `python -m unittest tests.test_translation_fixtures -v; echo "exit=$?"` → 1 (fixtures missing).
- [ ] **Step 2:** Write the source units and termbases. Claude translates the units (Claude is `author_model: claude`). Write both trace maps and the proposals.
- [ ] **Step 3: One real Codex review per fixture translation** (read-only, `codex-delegate`, without `--ignore-user-config`). The brief lists every unit pair and asks for findings citing `unit-id:line` under a header that includes `reviewer_model: codex`. Save each verbatim to the fixture's `translation/codex-review.md`. Resolve the findings through the Fix Protocol into `translation/fixes.md`.
- [ ] **Step 4: Run** — `python -m unittest tests.test_translation_fixtures -v; echo "exit=$?"` → 0; the full suite → 0.
- [ ] **Step 5: USER SEES OUTPUTS** — `python tests/tools/build_translation_fixtures.py --out "$(mktemp -d)"; echo "exit=$?"` → 0. It builds both fixtures to DOCX and PDF in temp repos and prints the four paths. Send the two PDFs to the user with `SendUserFile` and wait until they confirm they have seen both (TICKET STEP 11 exit). Record the confirmation as a DEC row with their words.
- [ ] **Step 6: Commit**

```bash
git add tests/fixtures/translation tests/test_translation_fixtures.py tests/tools/build_translation_fixtures.py docs/harness/DECISIONS.md
git commit -m "feat(harness): EN<->AR translation fixtures with independent reviews (STEP 11 task 3)"
git status --porcelain   # expect empty
```

**STEP 11 exit:** both fixtures pass termbase consistency, traceability, preservation and different-model review (`test_translation_fixtures` → 0); the STEP 11 Codex review is done; the user has seen both outputs (DEC row).

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
- Deliberate size limits: STEPS 9–11 give interfaces, tests, literal expectations and every command with its expected exit code, but not full implementation listings, because that code depends on RDKit/python-docx/Word behaviour that the first failing test pins down.
- Codex plan review (`docs/harness/reviews/step4-review.md`) and its Fix Protocol record (`step4-fixes.md`) explain every change made after the first draft.
