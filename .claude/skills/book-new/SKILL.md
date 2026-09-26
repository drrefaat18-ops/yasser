---
name: book-new
description: Run the new stage of the book harness through run_stage.py
---

# book-new

Creates `projects/<book>/` with its skeleton, an empty `decisions.md` and `state.json`. The slug must match `^[a-z0-9][a-z0-9-]{1,62}$`.

```bash
python harness/run_stage.py --project projects/<book> new
python harness/run_stage.py --project projects/<book> init-state   # adopt an existing folder instead
```

**Gate rules (Rule 7).** Never edit `state.json` by hand. Approvals are written only right after the user approves the exact files in chat, and only after a row with their words exists in `projects/<book>/decisions.md`. If a command prints `ERROR <CODE>`, stop and report it; there is no bypass flag.
