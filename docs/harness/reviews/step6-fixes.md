# STEP 6: Fix Protocol record (DEC-030)

Review: `docs/harness/reviews/step6-review.md`. Codex reviewed commits `9aa3430`, `c9de6e3` and `783fdd4` read-only (run `yasser-2026-09-26T13-47-25-242Z`, `touchedFiles: []`). Verdict `fail`: 5 major, 1 minor. This is STEP 6's only review; there is no second round. An earlier dispatch with `--ignore-user-config` could not run any command in its sandbox (the user config's `[windows] sandbox = "elevated"` was skipped) and produced no review.

## Findings

| ID | Real / rejected | Root cause | Siblings found (same class) | Fix | Verification → result |
|---|---|---|---|---|---|
| S6-01 | Real (also found-by-claude before the report arrived) | `test_real_manifest_pre_ok` asserted the pre-move state against the live tree; the migration is one-way. | S6-07 | Replaced by `test_real_manifest_pre_then_post_on_approved_tree`: a detached worktree of the approval commit `b732b46`, `pre` → the moves (`git mv`) → `post`. Plus `test_real_manifest_is_the_approved_one` (manifest SHA-256 equals DEC-034). | `python -m unittest discover -s tests -t .` → 42 OK; worktree removed afterwards (`git worktree list` shows only the main tree). |
| S6-02 | Real | The invariant was asserted on the JSON only, not in `problems()`. | none | `problems()` requires `images/**` and `rework/**` to keep their relative path under `projects/<slug>/`. `test_images_beside_rework` mutates destinations (`assets/`, `src/`) and checks the correct one passes. | Test OK. |
| S6-03 | Real | Post phase had one negative test only. | none | `test_post_valid_move`, `test_post_changed_bytes`, `test_post_source_survives` on temp git repos. | Tests OK. |
| S6-04 | Real | `fix_paths` and the missing-image check kept book-root-relative links after `OUT` moved to `deliverables/`. | S6-05 | `../images/…` kept as authored; `figures/…` → `../rework/figures/…`; check resolves against `OUT.parent`. Frozen deliverable not edited. | `assemble.main()` with `OUT` redirected to a scratch folder beside `rework/`: 13 image links, 0 unresolved, exit 0 (scratch removed). Mutation: `../images/nope.png` and `../rework/figures/nope.svg` reported missing; `../images/image1.jpeg` not. The 14th link in the sources is in `_template.md`, which is not assembled. |
| S6-05 | Real | Converter output moved to `original/` but its links stayed `images/…`. | — | `../images/{filename}`; docstring. Not run (it would overwrite the frozen original). | Static: `normpath(dirname(MD_PATH)/../images) == IMAGES_DIR` → True. |
| S6-06 | Real (minor) | Usage lines were relative to the old repo root. | Same in 5 files | `python projects/ai-in-medicine/rework/tools/…` and chapter-path examples. | `grep "python rework/" projects/ai-in-medicine` → none. |
| S6-07 | Real, found-by-claude | The manifest hashes the working-tree bytes at approval time. Two sources, the original manuscript `.md` and `convert_docx_to_md.py`, were checked out CRLF while their committed blobs are LF (`core.autocrlf=false`; the stat cache kept `git status` clean). A clean checkout of `b732b46` therefore fails `pre` on exactly those two. The committed blobs moved `R100`; no content was altered. | `harness/tools/manifest.py` itself was CRLF over an LF blob; normalized to LF in this commit so the diff is 4 lines. | The approved manifest is **not** changed (it would need re-approval). The replay test pins the two known exceptions (`EOL_DIVERGENT`), so any other drift fails. | Replay test OK; `git show b732b46:<src>` hashed for all 81 → exactly these 2 differ. |
| S6-08 | Real, found-by-claude (Codex gate note) | `--phase post` is only valid between commits A and B, undocumented. | none | One line in the `manifest.py` docstring. | — |

## Gates after the fixes

| Command | Result |
|---|---|
| `python -m unittest discover -s tests -t .` | 42 tests OK |
| `python -m pytest projects/ai-in-medicine/rework/tools -q -p no:cacheprovider` | 15 passed |
| `capture_golden.py … --layout layout-projects.json` → temp; `compare_golden.py golden.json <temp> --allow migration-manifest.json` | exit 0, exit 0, `diffs: []` |
| `manifest.py --scope-commit 60b9c51 --extra docs/harness/reviews/step6-golden-diff.md` | exit 0, 0 problems |
