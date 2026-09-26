---
name: book-rework
description: Run the rework stage of the book harness through run_stage.py
---

# book-rework

Rewrite one chapter at a time; each `--unit` completion writes a unit receipt and keeps the run open. The last call without `--unit` closes the stage once every chapter is valid. Checks arrive in STEP 8.

```bash
python harness/run_stage.py --project projects/<book> begin rework      # lists units missing or stale
python harness/run_stage.py --project projects/<book> complete rework --nonce <hex> --unit <chapter-id>
python harness/run_stage.py --project projects/<book> complete rework --nonce <hex>
```

A crashed or abandoned run: `abort <stage> --reason "..."` (keeps the files). Resume a unit stage with the nonce shown by `verify`.

**Gate rules (Rule 7).** Never edit `state.json` by hand. Approvals are written only right after the user approves the exact files in chat, and only after a row with their words exists in `projects/<book>/decisions.md`. If a command prints `ERROR <CODE>`, stop and report it; there is no bypass flag.
