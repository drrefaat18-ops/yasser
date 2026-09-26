# STEP 6 — Codex review (manifest-driven migration)

Source: codex-delegate relay, read-only, run yasser-2026-09-26T13-47-25-242Z, thread 01a0ddf8-80b7-76a0-957c-a495690912c8, touchedFiles: []. An earlier dispatch (run yasser-2026-09-26T13-46-22-803Z, `--ignore-user-config`) could not execute any command in its sandbox and produced no review; it is not counted. Report below is verbatim.

reviewed_commit: 783fdd4ad1a7f80c4c10b2fe54df72f852d567eb
verdict: fail
open_blocker_major: 5

## Findings

| ID | Severity (blocker/major/minor) | File:line | Problem | Concrete fix |
|---|---|---|---|---|
| S6-01 | major | `tests/test_manifest.py:15` | The committed suite is red after migration: `test_real_manifest_pre_ok` runs the pre-phase validator against the post-migration tree, producing 162 problems. Any full test run now fails. | Exercise pre-phase success in an isolated temporary Git fixture representing the pre-migration state; keep current-tree assertions phase-appropriate. |
| S6-02 | major | `harness/tools/manifest.py:25` | `problems()` never enforces that `images/` remains beside `rework/`. The test at `tests/test_manifest.py:42` inspects the approved JSON directly, so an implementation with this invariant entirely absent still passes. A newly approved malformed manifest could place images elsewhere while validation succeeds. | Enforce the destination layout inside `problems()` and mutate a manifest in the test to prove the validator rejects the wrong layout. |
| S6-03 | major | `tests/test_manifest.py:35` | Post-phase coverage proves only that a missing destination is rejected. Removing the post-move hash check or the “source still present” check from `manifest.py:54-57` would leave every test passing, allowing modified bytes or copied-not-moved sources through. | Add independent post-phase tests for a valid move, changed destination bytes, and a surviving source. |
| S6-04 | major | `projects/ai-in-medicine/rework/tools/assemble.py:21` | The assembler still rewrites links to `images/...` and `rework/figures/...` while writing into `deliverables/`. Those links resolve beneath `deliverables/`, but its validation checks them beneath the project root, so it can exit successfully with a broken Markdown file. Deferring correction of the already-frozen deliverable is consistent with Rule 5; deferring this allowlisted live-tool path fix is not. | Preserve `../images/...`, rewrite chapter-local `figures/...` to `../rework/figures/...`, and validate links relative to `OUT.parent`. Do not edit the frozen deliverable. |
| S6-05 | major | `projects/ai-in-medicine/tools/convert_docx_to_md.py:42` | The converter now writes Markdown under `original/` but continues emitting `images/<file>`, which resolves to nonexistent `original/images/`. Running it after migration creates broken image links. | Emit `../images/<file>` when `MD_PATH` is under `original/`, preferably with a focused path-resolution test. |
| S6-06 | minor | `projects/ai-in-medicine/rework/tools/assemble.py:3` | The live usage example still says `python rework/tools/assemble.py`; equivalent stale examples remain in `build_book.py`, `check_book.py`, `verify_refs.py`, and `renumber_refs.py`. From the repository root required by the plan, these commands address paths that no longer exist. | Use repository-root paths beginning `projects/ai-in-medicine/...`, or explicitly document changing into the project directory first. |

## Gates run

- `python -m unittest tests.test_manifest -v` -> exit 1: 9 passed, `test_real_manifest_pre_ok` failed with 162 pre-state errors.
- `python harness/tools/manifest.py --phase post` -> exit 1: expected post-Commit-B hash mismatches for the three intentionally edited allowlisted files (`convert_docx_to_md.py`, `assemble.py`, `build_book.py`).
- `python -m pytest projects/ai-in-medicine/rework/tools -q -p no:cacheprovider` -> not runnable in sandbox: pytest requires a writable temporary directory; none is available in the read-only environment.
- `git show -M100% --name-status --format= c9de6e3` -> exactly 81 entries, all `R100`, matching the manifest source/destination pairs exactly.
- `git show --stat 783fdd4` -> five files: three allowlisted tools plus `golden-step6.json` and `step6-golden-diff.md`.
- `python harness/tools/manifest.py --scope-commit 783fdd4 --extra tests/fixtures/ai-in-medicine/golden-step6.json --extra docs/harness/reviews/step6-golden-diff.md` -> exit 0, 0 problems.
- Manifest/plan inventory audit -> 81 expected and 81 declared; no missing, extra, reserved, or wrongly mapped moves. All current destination raw hashes match except the three intentional Commit-B edits.
- Golden audit -> all non-provenance fields are identical and non-vacuous: 302 checks, 11 chapters, 38 images, and 101 reference rows.