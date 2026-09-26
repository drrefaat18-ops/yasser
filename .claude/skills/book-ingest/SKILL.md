---
name: book-ingest
description: Run the ingest stage of the book harness through run_stage.py
---

# book-ingest

Copies the source into `source/`, converts it to `ingest/normalized.md` and reports fidelity. Exit 2 means a structure was lost.

```bash
python harness/run_stage.py --project projects/<book> run ingest
```

**Gate rules (Rule 7).** Never edit `state.json` by hand. Approvals are written only right after the user approves the exact files in chat, and only after a row with their words exists in `projects/<book>/decisions.md`. If a command prints `ERROR <CODE>`, stop and report it; there is no bypass flag.
