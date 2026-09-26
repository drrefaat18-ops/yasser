---
name: book-translate
description: Run the translate stage of the book harness through run_stage.py
---

# book-translate

Faithful translation, one source unit at a time (translation contract). Implemented in STEP 11.

```bash
python harness/run_stage.py --project projects/<book> begin translate --author-model <model>
python harness/run_stage.py --project projects/<book> complete translate --nonce <hex> --unit <unit-id>
python harness/run_stage.py --project projects/<book> complete translate --nonce <hex>
```

A crashed or abandoned run: `abort <stage> --reason "..."` (keeps the files). Resume a unit stage with the nonce shown by `verify`.

**Gate rules (Rule 7).** Never edit `state.json` by hand. Approvals are written only right after the user approves the exact files in chat, and only after a row with their words exists in `projects/<book>/decisions.md`. If a command prints `ERROR <CODE>`, stop and report it; there is no bypass flag.
