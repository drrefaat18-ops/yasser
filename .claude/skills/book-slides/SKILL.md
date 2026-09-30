---
name: book-slides
description: Make PowerPoint teaching decks (one .pptx per chapter) from a built book through harness/tools/build_slides.py. Use when the user asks for slides, a slide deck, PowerPoint or a presentation for a book in projects/.
---

# book-slides

Turns the reworked chapters of a book into one teaching deck per chapter. Runs after `build` (gate: build). All
wording, colours, logos and labels come from the project's own files; the rules and the lessons behind them are in
`docs/harness/SLIDES.md` — read it first.

## 1. Questionnaire first (always, before any deck is built)

Ask with `AskUserQuestion` (checkboxes where more than one answer fits), one round, recommended option first:

| Question | Options (recommended first) | Goes to `slides.json` |
|---|---|---|
| Files | One deck per chapter / one deck for the whole book | per-chapter only today; if "one deck", say so and stop |
| Slides per session | 12-15 teaching slides / 8-10 / 20+ | guides review; `minutes` holds the session length |
| What goes on the slides (multi) | tables and figures / the feature callout on a panel / MCQs: question slide then answer slide / speaker notes / the explanation printed on the slides | `feature_callout`, `mcq_slides`, `speaker_notes`, `explain_on_slide` |
| Look | the book's palette and logos / a preset (academic-defense, indigo-porcelain, forest-ink, executive, strategy-consulting, light-corporate, data-forward, academic-royal, warm-editorial, swiss-ikb) | `preset` (null = book palette) |
| Roadmap slide | yes / no | `agenda` |
| Unit name and session length | ask in plain words (e.g. "Section", 45 min) | `unit_label`, `minutes` |
| Feature callout glyph | one character that suits the subject, or none | `feature_glyph`, `case_glyph` |

Write the answers to `projects/<book>/slides.json` and show it to the user.

## 2. Build

```bash
python harness/tools/build_slides.py --project projects/<book>
```

Output: `projects/<book>/slides/*.pptx`. A deck that is open in PowerPoint is skipped (exit 1); ask the user to
close it and run again.

## 3. QA (one batched round, fix, one confirm round, stop)

1. Read `slides/qa-report.json` (the tool's own lint) and fix what it lists.
2. Validate every deck: `python <pptx skill>/scripts/office/validate.py <deck>.pptx`.
3. Export two or three decks to PNG with PowerPoint (PowerShell COM: `Presentations.Open(...).Export(dir, "PNG",
   1280, 720)`) and look at a contact sheet: text overflow, overlapping rows, empty halves, logo edges.
4. Fix in `build_slides.py` or in `slides.json`, never by hand in a deck. Re-run the tests:
   `python -m unittest tests.test_build_slides`.

**Gate rules (Rule 7).** The tool calls the build gate; if it prints `ERROR <CODE>`, stop and report it. No bypass.
