# STEP 5: Fix Protocol record (DEC-030)

Review: `docs/harness/reviews/step5-review.md`. Codex reviewed commits `d557120` and `c2fe5b3` read-only (run `yasser-2026-09-25T17-24-35-870Z`, `touchedFiles: []`). Verdict `fail`: 6 major, 0 blocker, 0 minor. This is STEP 5's only review; there is no second round.

Codex could not run the gates in its sandbox (no writable temp dir, no Word COM in its logon session). Claude re-ran every gate after the fixes (bottom of this file).

## Rulings made during execution (before the review)

| ID | Ruling | Why | Cost if wrong | Codex |
|---|---|---|---|---|
| R1 | N5 volatile list extended with the per-save IDs Word writes. | Two legacy builds of identical sources (scratch copies, Word COM) differed in 94 parts under N5 as written; the STEP 8 golden compare could never pass. | A random-ID attribute that carried content would go unseen (none do). | Rejected the font part of it; fixed as S5-01 |
| R2 | N6 gains `sentences: no prose found` (`check_book.py:88`) → `READ-NOPROSE`. | The legacy checker emits it; plan N7 wrongly lists it as new. | None: STEP 8 compares it by projection. | Accept |
| R3 | N6 `check_all` line numbers corrected to 274/282/284/287/289. | Plan Step 1 asked for re-confirmation. | None. | Accept |
| R4 | `layout-legacy.json` gains `legacy_sections {assessment, answers}`. | Keeps section labels out of shared code (Rule 8). | `layout-projects.json` (STEP 6) must carry the key too. | Accept |
| R5 | Target = chapter file name up to the first `-` (`ch01`), book-level `book`; `measured` inside the matching check; repeated failures joined with `; `. | Plan fixed the keys but not these shapes. | STEP 8 checker must emit the same targets. | Accept |
| R6 | An unknown `verify_refs` line raises `Unclassified` (exit 2). | Never freeze an uninterpreted result. | None. | Accept |
| R7 | `capture_legacy.py` validates the src copy before writing the golden; `__pycache__` is ignored in the comparison. | Immutable copy; see also S5-08. | None. | Accept |
| R8 | Book-level IDs tested by `BOOK_MUTATIONS` on a temp chapters copy. | The plan's `MUTATIONS` shape takes one chapter text only. | None. | Accept |

## Findings

| ID | Real / rejected | Root cause | Siblings found (same class) | Fix | Verification → result |
|---|---|---|---|---|---|
| S5-01 | Real, partly. Replacing font bytes with `"volatile"` hid every font change. Codex's exact fix (hash de-obfuscated bytes) is not stable: after de-obfuscation Word still rewrites the `head` checksum/timestamp and other bytes on every save (13–19 differing bytes per font between two builds of identical sources). | A volatile source was excluded wholesale instead of narrowing to what is volatile. | none | Each `word/fonts/*` part is hashed by identity: its `fontTable.xml` font name, embed slot (`embedRegular`, …) and byte length. `ponytail:` comment and `volatile_excluded` entry name the ceiling (same-length glyph edits are unseen). | `test_embedded_font_hash_ignores_key_but_sees_payload` (key change equal; length change and font rename differ) → OK. Two scratch rebuilds and the deliverable: 0 differing parts. |
| S5-02 | Real | The TOC walk decided per run, but result text can share a run with the `separate`/`end` fldChar. | A pre-existing run holding only `rPr` inside the result survived, keeping its hyperlink and the random `_Toc` anchor (found-by-claude while re-verifying on the two builds). | The walk works per run child: children inside the result are dropped; a fldChar only when it is inside the result both before and after it; any run that starts inside the result and ends with only `rPr` is removed, then emptied hyperlinks. | `test_toc_result_sharing_delimiter_runs_is_volatile` (text in the separate and end runs, nested PAGEREF) → OK; `test_toc_result_and_toc_bookmarks_are_volatile` now includes an `rPr`-only run → OK; rebuild diff → 0 parts. |
| S5-03 | Real | Checks were attached to the first group in `run()` instead of every group of the Task 5.1 table; `--group` accepted any string. | none | One `CHECKS` registry of `(groups, probe)`; a check runs once when any of its groups is requested; `--group` has `choices`; `run()` raises on unknown groups. | `test_group_matrix`, `test_unknown_group_is_refused` → OK |
| S5-04 | Real | Plan code carried a `C:\Windows` fallback literal. | `capture_golden.py` regex `DOI:\s` matches the §9.5 leak pattern `[A-Za-z]:\\` (found-by-claude); changed to `DOI:[ \t]` (same match on a single line). | Fonts check reads `WINDIR` or `SystemRoot`, else fails naming them. | `test_fonts_without_windir_fails_named` → OK; `grep -rnE '[A-Za-z]:\\\\|/Users/|/home/' harness/ --include=*.py --include=*.json` → no match |
| S5-05 | Real | The layout was trusted because only the test-side caller existed. | `chapter_glob` could contain `/` or `..`. | `layout_problems()` checks every path key (relative, no `..`, no drive, resolves inside the project) and the glob; `capture()` itself raises `LayoutError`, so every caller routes through it; the CLI exits 1 `ERROR LAYOUT`. | `test_layout_paths_must_stay_inside_project` (7 escape cases) → OK |
| S5-06 | Real | Two rows shared one mutation that emits both IDs, so a swapped mapping passed. | Book-level rows had the same unguarded shape. | Isolated prose for `READ-MEAN` (mean 21, none > 28) and `READ-LONG` (19 short, 1 long). New `test_swapped_mappings_would_be_caught` over every same-function pair; the same guard in the book-level test. | Suite OK. Mutation proof: restoring the shared mutation makes the guard fail with "READ-LONG and READ-MEAN mutations each emit both IDs". |
| S5-07 | Real, found-by-claude | `compare_golden.py` took any JSON as an allowlist. | none | `--allow` must be a list, or a dict with `expected_diff`, of exactly `{pointer_glob, reason}`; otherwise exit 2 `ERROR ALLOWLIST`. | `test_bad_allowlist_is_a_named_error` (3 cases) → OK |
| S5-08 | Real, found-by-claude | Loading the legacy checker from the immutable src copy wrote `__pycache__` into it. | none | `test_legacy_classify.legacy()` sets `sys.dont_write_bytecode`. | `ls tests/fixtures/ai-in-medicine/src/rework/tools` → no `__pycache__` after the suite |

## Gates after all fixes

- `python -m unittest discover -s tests -t . -v` → 28 tests, OK, exit 0.
- `python harness/preflight.py` → exit 0 (`rdkit`, `markitdown` OPTIONAL-MISSING).
- Golden re-frozen: `capture_legacy.py --out golden.json --copy-src src` → exit 0; second capture → exit 0; `cmp` → 0. The golden diff against `c2fe5b3` is only the 15 font-part hashes, `hashes.docx` and the font `volatile_excluded` entry.
- Scope lock: `git diff --stat e77d0b9 -- rework AI_in_Health_Care_Interprofessional.{md,docx,pdf}` → empty.
