---
name: book-audit
description: Run the audit stage of the book harness through run_stage.py
---

# book-audit

One Codex audit saved to `audit/codex-audit.md` (with `reviewed_commit:`), independent scores on the same rubric, Fix Protocol in `audit/fixes.md`.

```bash
python harness/run_stage.py --project projects/<book> begin audit
python harness/run_stage.py --project projects/<book> complete audit --nonce <hex>
```

A crashed or abandoned run: `abort <stage> --reason "..."` (keeps the files). Resume a unit stage with the nonce shown by `verify`.

**Gate rules (Rule 7).** Never edit `state.json` by hand. Approvals are written only right after the user approves the exact files in chat, and only after a row with their words exists in `projects/<book>/decisions.md`. If a command prints `ERROR <CODE>`, stop and report it; there is no bypass flag.
