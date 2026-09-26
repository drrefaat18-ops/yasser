# STEP 6: golden diff after migration (Task 6.3)

Baseline: `tests/fixtures/ai-in-medicine/golden.json` (STEP 5, repo-root layout).
Re-capture: `tests/fixtures/ai-in-medicine/golden-step6.json` (after commit A `c9de6e3` and the commit B path fixes, `projects/ai-in-medicine` layout).

## Commands

```bash
TMP=$(mktemp -d)
python harness/tools/capture_golden.py --project projects/ai-in-medicine --layout tests/fixtures/ai-in-medicine/layout-projects.json --out tests/fixtures/ai-in-medicine/golden-step6.json; echo "exit=$?"
python harness/tools/compare_golden.py tests/fixtures/ai-in-medicine/golden.json tests/fixtures/ai-in-medicine/golden-step6.json --allow docs/harness/migration-manifest.json --out "$TMP/diff.json"; echo "exit=$?"
```

## Results

| Command | Exit |
|---|---|
| `capture_golden.py` | 0 |
| `compare_golden.py` | 0 |

Diff list (`diff.json`): `{"diffs": [], "schema_version": 1}`. Empty, as the manifest's `expected_diff: []` requires.

Raw `diff` of the two files differs only in `provenance` (`captured_from` `.` → `projects/ai-in-medicine`, `tool_sha` → `c9de6e3`), which the comparison does not compare.

## Path fixes in commit B

Only allowlisted files changed; line endings preserved.

| File | Change |
|---|---|
| `projects/ai-in-medicine/rework/tools/assemble.py` | `OUT` → `ROOT / "deliverables" / …md`; docstring |
| `projects/ai-in-medicine/rework/tools/build_book.py` | `OUT` → `ROOT / "deliverables" / …docx` (PDF follows `OUT`); docstring |
| `projects/ai-in-medicine/tools/convert_docx_to_md.py` | absolute `D:\yasser\…` paths → relative to the script (`original/`, `images/`) |

`check_book.py`, `verify_refs.py`, `renumber_refs.py` and the two legacy tests needed no path-constant change (their `ROOT` depth is unchanged); the Fix Protocol later corrected their usage lines only (S6-06). `python -m pytest projects/ai-in-medicine/rework/tools -q` → 15 passed.

## Image links after the move (updated by the Fix Protocol, `step6-fixes.md` S6-04, S6-05)

The live tools now write links relative to where their output lives: `assemble.py` keeps `../images/…` and writes `../rework/figures/…` into `deliverables/`, and validates them relative to `OUT.parent`; `convert_docx_to_md.py` emits `../images/…` into `original/`. Re-running the capture and comparison after these fixes: both exit 0, diff list empty.

The two frozen files, `deliverables/AI_in_Health_Care_Interprofessional.md` and `original/AI_in_Medicine- Assistant Prof Dr Shereen Elkholy.md`, still carry root-relative `images/…` links, so their images do not resolve when the Markdown is viewed on its own. They are not edited (Rule 5). The DOCX and PDF embed their images and are unaffected.
