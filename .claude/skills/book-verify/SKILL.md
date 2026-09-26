---
name: book-verify
description: Run the verify stage of the book harness through run_stage.py
---

# book-verify

Checks approvals, every receipt up to the boundary, and any active run. Exit 0 only when all pass.

```bash
python harness/run_stage.py --project projects/<book> verify [--through <stage>]
```

**Gate rules (Rule 7).** Never edit `state.json` by hand. Approvals are written only right after the user approves the exact files in chat, and only after a row with their words exists in `projects/<book>/decisions.md`. If a command prints `ERROR <CODE>`, stop and report it; there is no bypass flag.
