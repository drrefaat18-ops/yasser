---
name: book-build
description: Run the build stage of the book harness through run_stage.py
---

# book-build

Renders figures, assembles Markdown, builds DOCX and PDF into `build/`. Implemented in STEP 8.

```bash
python harness/run_stage.py --project projects/<book> run build
```

**Gate rules (Rule 7).** Never edit `state.json` by hand. Approvals are written only right after the user approves the exact files in chat, and only after a row with their words exists in `projects/<book>/decisions.md`. If a command prints `ERROR <CODE>`, stop and report it; there is no bypass flag.
