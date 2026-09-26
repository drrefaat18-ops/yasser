# Book Harness Step Ledger

This file is kept separate from `TICKET.md` so that progress updates never touch the ticket itself (DEC-023, DEC-030).


| Step | Owner | Status | Handoff artifact | Commit | Date |
|---|---|---|---|---|---|
| 0 | Claude | Done: approved at 23d819f (DEC-026) | `TICKET.md`, `VISION.md`, `DECISIONS.md` | — | 2026-09-25 |
| 1 | Claude | Done: spec approved by user (DEC-031). Exit checks pass (A–M covered, 48/48 INV rows, TBD grep empty). Subagents spawned: 0 | `docs/superpowers/specs/2026-09-25-book-harness-core-design.md` | 0284376 | 2026-09-25 |
| 2 | Claude | Done: both contracts committed; every map row names a core extension point; TBD grep empty on all three specs; core spec amended in same commit. Subagents spawned: 0 | `2026-09-25-arabic-locale-contract.md`, `2026-09-25-translation-contract.md` | 20f4efe | 2026-09-25 |
| 3 | Codex / user | Review done (verdict fail, 15 blocker/major + 2 minor); all 17 resolved via Fix Protocol, verifier exit 0. Final specs approved by user (DEC-032). Subagents spawned: 0 | `reviews/step3-review.md`, `reviews/step3-fixes.md` | fcfee40 | 2026-09-25 |
| 4 | Claude | Plan written; Codex review (fail, 21 blocker/major + 1 minor) resolved via Fix Protocol, verifier exit 0. Plan approved by user (DEC-033). Subagents spawned: 0 | `docs/superpowers/plans/2026-09-25-book-harness.md`, `reviews/step4-review.md`, `reviews/step4-fixes.md` | 0cd77e4 | 2026-09-25 |
| 5 | Claude | Done: preflight exit 0; double capture byte-identical (cmp 0); suite 28/28. Codex review (fail, 6 major) resolved via Fix Protocol + 2 found-by-claude, gates re-run. Rulings R1–R8 in `reviews/step5-fixes.md`. Subagents spawned: 0 | `harness/preflight.py`, `tests/fixtures/ai-in-medicine/golden.json`, `reviews/step5-review.md`, `reviews/step5-fixes.md` | d557120, c2fe5b3, d341132 | 2026-09-25 |
| 6 | Claude | Done: manifest approved (DEC-034); commit A all R100 (81 moves); commit B scope check exit 0; golden diff empty (exit 0). Codex review (fail, 5 major + 1 minor) resolved via Fix Protocol + 2 found-by-claude (S6-07 manifest hashes are working-tree bytes: 2 files CRLF-checked-out over LF blobs; approved manifest left unchanged). Suite 42/42, legacy 15/15. Subagents spawned: 0 | `migration-manifest.json`, `reviews/step6-golden-diff.md`, `reviews/step6-review.md`, `reviews/step6-fixes.md` | 9aa3430, c9de6e3, 783fdd4, 60b9c51, 3574263 | 2026-09-26 |
| 7 | Claude | Done: bypass matrix exit 0; `verify --through intake` and `--through rework` exit 0 on ai-in-medicine; intake (DEC-036), history import (DEC-039, replacing DEC-037) and design (DEC-040, replacing DEC-038) approved by the user; CLAUDE.md split (projects copy byte-identical). Codex review (fail, 10 major + 1 minor) resolved via Fix Protocol; rulings R1–R26. Suite 101/101 (1 skipped). Subagents spawned: 0 | `harness/{state,run_stage,gate,registry,schema,paths,locales}.py`, `harness/schemas/`, `harness/stages/`, `.claude/skills/book-*`, `reviews/step7-rulings.md`, `reviews/step7-review.md`, `reviews/step7-fixes.md` | d9ef9a3, 1c25490, 26164e8, 3673389, 2b9a998, 5aed84e, d6ab289, ceb6336 | 2026-09-26 |
| 8 | Claude | In progress: reading done (ticket, plan 8.1–8.4, core spec §2.4, §9, §10, state/contracts/capture_golden, legacy check_book); no code yet. Resume at Task 8.1 Step 1 (failing tests) | `harness/tools/*` + ingest | — | — |
| 9 | Claude | Not started | `harness/figures/*` + evidence | — | — |
| 10 | Claude | Not started | Arabic fixture + evidence | — | — |
| 11 | Claude | Not started | EN↔AR fixtures | — | — |
| 12 | Claude + user | Not started | `reviews/step12-e2e-report.md` | — | — |
| 13 | Codex | Not started | `reviews/step13-final-audit.md` | — | — |

