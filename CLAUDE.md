# CLAUDE.md — Book Harness

This repository is a **book harness**: one pipeline that takes any university textbook, in any science, in Arabic or English, and runs it through the same six phases:

1. Ingest the book.
2. Evaluate it to find gaps and problems.
3. Design a stronger, simpler edition for university teachers and students.
4. Rewrite it (translation between Arabic and English is the first step of this phase when needed).
5. Build Word and PDF.
6. Re-score it.

The binding vision is `docs/harness/VISION.md`; the ticket is `docs/harness/TICKET.md`; decisions are in `docs/harness/DECISIONS.md`.

## Layout

- `harness/` — shared, domain-free code and data: `state.py` (receipts, approvals, gates), `run_stage.py` (the one runner), `schemas/`, `agents/` (shared reviewer personas), `locale/`, `presets/`, `tools/`.
- `projects/<book>/` — one folder per book: its intake files, `state.json`, `decisions.md`, sources, chapters and outputs. Each book's own instructions are in `projects/<book>/CLAUDE.md`.
- `.claude/skills/book-*/` — thin skills, one per stage, that call `run_stage.py`.
- `tests/` — stdlib `unittest`; fixtures are immutable and run in temporary git repos.
- Full layout: `docs/superpowers/specs/2026-09-25-book-harness-core-design.md` §1.

## How to run

Use the `book-*` skills. Each one calls:

```bash
python harness/run_stage.py --project projects/<book> <command>
```

Stages in order: `new`, `intake`, `ingest`, `evaluate`, `design`, `[translate]`, `rework`, `build`, `audit`. Agentic stages are bracketed by `begin <stage>` and `complete <stage> --nonce N`; auto stages use `run <stage>`. `verify [--through <stage>]` checks the whole chain. Run the tests with `python -m unittest discover -s tests -t .`.

## Rule 7 — gates cannot be waived

- **Intake first.** No stage after `intake` runs on a book until the user has approved its `brief.json`, `rubric.json`, `template.json`, `theme.json` and `agents/*.json` at matching hashes.
- **Design gate.** `translate`, `rework`, `build` and `audit` also need the user's design approval.
- **Never edit `state.json` by hand.** Only `run_stage.py` writes it.
- **Approvals only after explicit user approval in chat.** Show the exact files and their SHA-256s, get a clear yes, add a DEC row with the user's words to `projects/<book>/decisions.md`, then run `approve <kind> --dec DEC-NNN`.
- Every executable that reads or writes a book, including legacy tools under `projects/`, calls the gate and needs `--project projects/<book>`. There is no bypass flag. The only ungated scripts are the four listed with their reasons in `harness/registry.py` (environment probe, golden compare, migration validator, golden capture). If a command prints `ERROR <CODE>`, stop and report it.

## Rule 8 — no domain in shared code

Nothing under `harness/` or `.claude/skills/book-*` may contain profession names, box or callout labels, clinical or other domain vocabulary, book titles, author names or absolute paths. All of these come from the project's config. "It already works for one book" is not a reason.

## Rule 11 — cheapest execution at highest quality

- Work inline by default.
- Spawn a Claude subagent only for a real reason: isolating a very large read whose conclusion alone is needed, or genuinely independent parallel work. At most 2, each logged with its reason (`complete ... --subagent "<reason>"`). "One agent per chapter" or "one per persona" is not a reason.
- Codex reviews do not count toward the cap. Each artifact gets **one** read-only Codex review; Claude then applies the Fix Protocol (confirm each finding, find the root cause, hunt siblings, fix, verify) and records it in a `fixes.md`.

## Working rules

- Commit after a task passes its gates; never push.
- Stop and ask the user at every approval point. Do not guess a genuine fork; log it in the ticket's Blocker Register.
