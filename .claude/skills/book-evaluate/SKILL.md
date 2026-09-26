---
name: book-evaluate
description: Run the evaluate stage of the book harness through run_stage.py
---

# book-evaluate

Inline persona passes (one per rubric reviewer), findings with one pillar each, the scorecard, then one read-only Codex review saved verbatim to `evaluation/codex-review.md` and the Fix Protocol in `evaluation/fixes.md`. Subagents: default 0, at most 2, each logged with `--subagent` (Rule 11).

```bash
python harness/run_stage.py --project projects/<book> begin evaluate
python harness/run_stage.py --project projects/<book> complete evaluate --nonce <hex> [--subagent "<reason>"]
```

A crashed or abandoned run: `abort <stage> --reason "..."` (keeps the files). Resume a unit stage with the nonce shown by `verify`.

**Gate rules (Rule 7).** Never edit `state.json` by hand. Approvals are written only right after the user approves the exact files in chat, and only after a row with their words exists in `projects/<book>/decisions.md`. If a command prints `ERROR <CODE>`, stop and report it; there is no bypass flag.
