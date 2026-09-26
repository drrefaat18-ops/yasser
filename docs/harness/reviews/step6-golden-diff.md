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

`check_book.py`, `verify_refs.py`, `renumber_refs.py` and the two legacy tests needed no change (their `ROOT` depth is unchanged). `python -m pytest projects/ai-in-medicine/rework/tools -q` → 15 passed.

## Known limitation (not fixed: scope lock)

`assemble.py` still rewrites image links to `images/…` and `rework/figures/…`, which are relative to the book root. The assembled Markdown now lives in `deliverables/`, so those links are broken when it is viewed on its own. The same is true of the moved deliverable `AI_in_Health_Care_Interprofessional.md`. The DOCX and PDF are unaffected (images are embedded). Harness builds write to `build/` from STEP 8 (N3), which is where this should be settled.
