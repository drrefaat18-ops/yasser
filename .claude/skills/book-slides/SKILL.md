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
   short and of similar length: one long text shrinks the whole row. **Few words per slide** (user, round 3): more
   slides are fine; labels alone are enough when they say it all.
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

## 5. Decks-only projects (source decks, no book)

When the user wants decks straight from course sources (sections, labs, quizzes) without a book:

1. `new`, then a short intake (brief goal mode `evaluate_only`, direction `other`; glossary and perspectives off;
   `paths.chapters: ingest`; chapter heading pattern for topics). The source is a faithful transcription of the
   pages used, in their wording, one `# Topic N: <title>` part per deck, with `## N.n` sections; keep the originals
   in `intake/original/`. Show the files and SHA-256s; approve on an explicit yes; then `run ingest`.
2. Contradictions or typos in the sources: ask the user; never resolve by guessing. Mark open ones "to be
   confirmed" in the transcription and on the slide.
3. Outline `slides/study/<deck>.json` with `"topic": N`; add `mcq` (q, opts, key, why, src) from the course
   quizzes, `takeaways` (text, src), `case` slides (verbatim case text beside the points that answer it) and
   pictures (`image` on points slides and on diagram nodes). Pictures live in `slides/study/images/` (outside every
   stage contract) with a `photo-sources.md`.
4. Build: `python harness/tools/build_source_deck.py --project projects/<p> [--chapter <deck>] --pdf`
   (gate: evaluate, i.e. intake approved and a fresh ingest). Then QA as in §3.

## 6. Design workflow for good-looking study decks (both modes)

Ideas taken from the slide skills surveyed on 2026-10-01 (academic-pptx-skill, siril9/presentation-skill,
danny0926/ppt-skills, mpuig/agent-slides, bergside glassmorphism, claude-office-skills ppt-visual), rebuilt inside
build_study.py; none of their code is installed or run.

1. **Plan the story with action titles**: every title states the slide's message in the source's own words
   ("Viral in 70–90% of cases; bacterial ~10–30%"), not a topic label. Read the titles alone (the review's ghost
   deck): they must tell the whole topic.
2. **Pick the layout from the content's shape**, and vary it (no layout twice in a row): `stats` for numbers
   (percentages, ages, durations, counts), `flow` for a sequence, `cards` for parts of a whole, `versus` for a
   contrast, `equation` for a definition that is a sum or difference, `spectrum` for a scale, `table` only for
   several attributes compared across rows, `points` + `image` for a definition with a picture, `case` for a case.
3. **One icon per node** (`"icon"`: one colour emoji, e.g. 🦠 bacterial, 🤧 viral, 💊 drug, 🌡️ fever, 👶 child,
   🤰 pregnancy, ✂️ surgery, 📅 episodes): same style throughout, meaning first, never decoration only.
4. **Few words**: labels alone when they say it all; one key message per slide in `caption`.
5. Build with `--review`: the tool exports every slide, writes contact sheets and a review note (ghost deck, layout
   repeats, densest slides) beside the deck. Look at every sheet; fix in the outline or the tool; rebuild; look again.
6. Send the PPTX and PDF; record the user's new preferences in docs/harness/SLIDES.md.
