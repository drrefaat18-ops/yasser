---
name: book-slides
description: Make PowerPoint decks from a built book in projects/ — teaching decks (build_slides.py) or source-faithful study-summary decks with a PDF (build_study.py). Use when the user asks for slides, a deck, PowerPoint, a presentation, a summary deck or revision slides for a book chapter.
---

# book-slides

Two kinds of deck, both after `build` (gate: build), both styled from the project's own files. The rules and the
lessons behind them are in `docs/harness/SLIDES.md` — read it first.

| User asks for | Mode | Tool |
|---|---|---|
| slides to teach / present a lecture | **teaching** (§1–3 below) | `build_slides.py`, every chapter |
| a summary deck to study or revise from | **study** (§4 below) | `build_study.py`, chapter by chapter |

## 4. Study mode (summary deck, content fixed to the book)

Defaults the user chose (see SLIDES.md, Study decks): shortened but traceable points, English as in the book,
for the lecturer and the student together (on-slide text plus speaker notes), PPTX and PDF.

1. **Ask only what is not yet settled** (the defaults above stand; ask about new needs, one round, recommended first).
2. **Read the whole chapter**, then write `projects/<book>/slides/study/<chapter stem>.json` (format in the tool's
   docstring): per core section, `points` slides (≤6 points, each a shortening of one chapter sentence quoted
   verbatim in `src`; a figure beside short points) and `table` slides for comparisons between related concepts,
   with their `src` quotes. Use only the chapter's own words; bold the key term in a point.
   **Prefer a diagram whenever the content has a shape** (user, 2026-10-01: "more figures, so the information is
   summarised better"): a sequence → `flow`; parts of a whole or a list of 4-10 → `cards`; two contrasted ideas →
   `versus`; a definition that is a difference or sum → `equation`; a scale with a best end → `spectrum`. Put the
   one-line key message in `caption`. Keep a table only where the reader compares several attributes across rows,
   and keep the book's own figures beside short points. Aim for at least one diagram per section. Keep node texts
   short and of similar length: one long text shrinks the whole row.
3. Build: `python harness/tools/build_study.py --project projects/<book> --chapter chNN --pdf`.
   The fidelity check stops the build on any non-verbatim `src`, any word not in the chapter, a point that shares
   less than half its words with its `src`, or a section without a slide. **Fix the outline, never the checker's
   limits.** The tool adds the objectives, the callout boxes, key terms (glossary), the MCQs (question, then answer
   with the reason) and a one-page revision slide, all verbatim.
4. QA as in §3: export to PNG with PowerPoint COM, look at every slide on contact sheets (only `Slide*.PNG`), fix
   in the outline or the tool, rebuild, look again. Lint warnings for the revision slide's density are expected.
5. Send the PPTX and PDF, ask the user what to change, and record each new preference in `docs/harness/SLIDES.md`
   (Study decks section) so the next chapter starts from it.

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
