---
name: book-intake
description: Run the intake stage of the book harness through run_stage.py
---

# book-intake

Ask the questionnaire in `docs/harness/INTAKE_QUESTIONNAIRE.md` (A–M), one topic at a time. Write `brief.json`, `rubric.json`, `template.json`, `theme.json` and `agents/*.json`. Show the user every file and its SHA-256; approve only on an explicit yes. To change an intake file later: `abort <stage>`, `begin intake --amend`, edit, `complete intake`, re-approve.

```bash
python harness/run_stage.py --project projects/<book> begin intake      # prints nonce=<hex> and the required outputs
python harness/run_stage.py --project projects/<book> complete intake --nonce <hex>
python harness/run_stage.py --project projects/<book> approve intake --dec DEC-NNN   # only after explicit user approval
```

A crashed or abandoned run: `abort <stage> --reason "..."` (keeps the files). Resume a unit stage with the nonce shown by `verify`.

**Gate rules (Rule 7).** Never edit `state.json` by hand. Approvals are written only right after the user approves the exact files in chat, and only after a row with their words exists in `projects/<book>/decisions.md`. If a command prints `ERROR <CODE>`, stop and report it; there is no bypass flag.
