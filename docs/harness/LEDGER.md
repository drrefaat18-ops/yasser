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
| 6 | Claude | In progress: Task 6.1 done (manifest + validator, 9aa3430); manifest approved (DEC-034). Paused by user; next is Task 6.2 (commit A) | migration manifest + golden diff | 9aa3430 | 2026-09-25 |
| 7 | Claude | Not started | control plane + bypass matrix | — | — |
| 8 | Claude | Not started | `harness/tools/*` + ingest | — | — |
| 9 | Claude | Not started | `harness/figures/*` + evidence | — | — |
| 10 | Claude | Not started | Arabic fixture + evidence | — | — |
| 11 | Claude | Not started | EN↔AR fixtures | — | — |
| 12 | Claude + user | Not started | `reviews/step12-e2e-report.md` | — | — |
| 13 | Codex | Not started | `reviews/step13-final-audit.md` | — | — |

