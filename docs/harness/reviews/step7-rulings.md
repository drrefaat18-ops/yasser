# STEP 7: rulings made during execution

Decisions Claude took where the plan was silent, contradictory or wrong. The STEP 7 Codex review sees this file.

| ID | Task | Ruling | Why | Cost if wrong |
|---|---|---|---|---|
| R1 | 7.1 | Locale code lives in `harness/locales.py`; `harness/locale/` holds only the `<primary>.json` profiles. The plan put the code in `harness/locale/__init__.py`. | A package named `locale` shadows the stdlib `locale` module for every script run from `harness/` (sys.path[0]); `python harness/preflight.py` crashed inside argparse/gettext. A data folder without `__init__.py` never wins over the stdlib module. | None; callers import `harness.locales`. |
| R2 | 7.1 | Extra schema `locale.v1.json` (the EXT-LOC-1 fields), used to validate shipped profiles and `template.locale_overrides`. | The plan's 16 schemas left the profile unvalidated. | One more file. |
| R3 | 7.1 | New error code `UNIT-INCOMPLETE`: the final `complete` of a unit stage refuses while any unit receipt is missing or stale. | None of the plan's codes names this case (`UPSTREAM-*` is about other stages). | Callers matching codes must know it. |
| R4 | 7.1 | `approve <kind>` also requires the `<kind>` stage's own receipt to be valid (`complete intake` / `complete design` passed). | Otherwise files that never passed their completion checks could be approved. | An approval cannot be written before `complete`; that is the intended order. |
| R5 | 7.1 | `run_auto(project, stage, fn)`: `fn(project) -> extras`. The plan also had it return inputs and outputs. | The plan says in the same task that file sets come only from `contracts.files`; returned maps would be ignored. | None. |
| R6 | 7.1 | Harness files that `intake` hashes (`rubric_core.json`, locale, preset) are listed project-relative as `../../harness/...`. | Receipt maps are project-relative; this keeps one path form and one hash routine. | A project moved outside `projects/<slug>/` would break it; §1.1 forbids that anyway. |
| R7 | 7.1 | `harness/agents/narratologist.md`: "comedic" → "comic". | The plan's leak grep (`medic`) matches "comedic"; the meaning is unchanged. | None. |
| R8 | 7.1 | `history/import.json` shape: `{"schema_version": 1, "stages": {"<stage>": {"inputs": [...], "outputs": [...]}}}`; rework import writes one unit receipt per `chapter-plan.json` chapter with that chapter file as output. | The plan names the file and its checks but not its shape. | Task 7.4 writes the medical `import.json` to this shape. |
| R9 | 7.1 | A unit stage keeps a placeholder stage receipt (`status: failed`, `error: units in progress`) holding `units{}` until the final `complete`. | The plan stores units under `receipts[stage].units` but a stage receipt does not exist yet; `failed` blocks downstream until the stage is really complete. | None. |
| R10 | 7.1 | `preflight.FONT_FILES` is the union of `required_font_files` over `harness/presets/*.json`; the Arabic fonts drop out until the RTL preset (STEP 10). | Plan Step 7. | Arabic font absence is not reported until STEP 10. |
