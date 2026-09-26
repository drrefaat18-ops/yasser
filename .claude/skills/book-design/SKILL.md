---
name: book-design
description: Run the design stage of the book harness through run_stage.py
---

# book-design

Write `design/design.md` (with a `| Finding | Chapter | Reason |` table mapping every blocker/major finding), `design/chapter-plan.json` and `design/errata-seed.md`. Show them to the user with SHA-256s before approving.

```bash
python harness/run_stage.py --project projects/<book> begin design
python harness/run_stage.py --project projects/<book> complete design --nonce <hex>
python harness/run_stage.py --project projects/<book> approve design --dec DEC-NNN   # after explicit user approval
```

A crashed or abandoned run: `abort <stage> --reason "..."` (keeps the files). Resume a unit stage with the nonce shown by `verify`.

**Gate rules (Rule 7).** Never edit `state.json` by hand. Approvals are written only right after the user approves the exact files in chat, and only after a row with their words exists in `projects/<book>/decisions.md`. If a command prints `ERROR <CODE>`, stop and report it; there is no bypass flag.
