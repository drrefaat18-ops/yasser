# Slide decks from a book (build_slides)

Tool: `harness/tools/build_slides.py` (gate: build). Skill: `.claude/skills/book-slides`. Test:
`tests/test_build_slides.py`. First used on `drug-information-practical` (2026-09-30).

## What the user asked for (keep these as defaults)

1. **Questionnaire first.** Every new deck starts with checkbox questions (files, slides per session, contents,
   look, unit name and length). Answers go into `projects/<book>/slides.json`.
2. **One deck per chapter**, one chapter per teaching session; about 12-15 teaching slides plus the MCQ slides.
3. **Contents:** the book's tables and figures; the feature callout (the practice example) on its own slide;
   MCQs as a question slide followed by an answer slide that highlights the key and gives the reason; the practice
   case; key takeaways.
4. **Speaker notes** under every content slide (the section's prose; the case's model answer).
5. **The explanation must also be on the slides**, not only in the notes (user, after seeing notes-only slides).
6. **Professional design** with the book's palette and **both logos**; the logos must look right.
7. **Save the method in the harness** so any future book gets the same result.

## Design rules (from the pptx and impeccable skills, applied)

- Dark (primary colour) title and closing slides; white content slides.
- One motif repeated: a round accent-colour chip with the chapter number beside every title. No accent line under
  titles, no decorative bars or edge stripes.
- Fonts that ship with Office: Cambria headings, Calibri body. Never Aptos; Georgia is unreliable in previews.
- Title 32 pt (27 when long); body 18-24 pt; nothing under 15 pt in rows.
- Numbered discs instead of plain bullets; cards with a small label pill for callouts; a half-bleed panel with a
  large glyph for the feature callout and the case.
- Table colours: primary header, zebra rows from a 94% tint of the primary; first column bold.
- Callout card colours come from `theme.callouts.<id>` (fill, label colour).

## Problems met and how the tool handles them

| Problem | Fix in the tool |
|---|---|
| Square logo on a white square showed its corners on the round badge; logos looked mismatched | `badge()`: clip each logo to its inscribed circle, centre it on a white disc |
| Two tables next to each other merged into one | A table caption line (`*Table ...*`) ends the table |
| A list next to a table was dropped | Every figure, table and list becomes its own slide (`chunks()`) |
| Lists from different subheadings merged | A `###` subheading titles the visuals under it |
| Long points overlapped in numbered rows | `rows()` estimates wrapped lines and shrinks the font (min 15 pt) until it fits |
| Tiny text in tables, large empty space | Table font scales with the amount of text; row height up to 0.7" |
| Explanation only in the notes | `explain_on_slide`: short text above the visual, long text in a column beside it, or on its own slide before a wide table |
| Huge section numeral collided with the title | Numeral box moved right and shrunk; title box narrowed |
| A deck open in PowerPoint could not be written (PermissionError) | The deck is skipped with a message; exit 1 |
| Cover subtitle unreadable (accent on primary) | Light text is a tint of the primary, not the accent (same rule as the PDF cover, `cover_accent`) |

## QA that worked

PowerPoint COM export to PNG (LibreOffice is not installed here), then a contact sheet of 9-12 slides from two
decks. One batched fix round, one confirm round, stop.

## Rules taken from open-source slide skills (2026-09-30)

Surveyed: knowledge-cat-ppt-skill, slide-skill, slide-maestro, AgentBuff, powerpoint-fancy-design, html2pptx,
image-to-editable-ppt-skill, guizang-ppt-skill, starrykit, frontend-slides, slide-writer, slide-creator, openclaw
pptx-creator (list from kimi.ai/resources/ppt-skills-for-agents). Their code is kept for reference only in
`vendor/ppt-skills-ref/` (git-ignored, outside `.claude/skills` so none of it loads or runs). What was built into
`build_slides.py`:

| Rule | Source skills |
|---|---|
| 10 palette presets (`slides.json` `preset`), each with Office-safe fonts | slide-skill themes, guizang, slide-creator, openclaw |
| WCAG contrast guard: colours darkened until white text reaches 4.5:1 | slide-skill svg_qa, slide-creator |
| Density caps: 6 points / 8 table rows per slide, split into "(1/2)" slides; font floors (rows 16 pt, tables 12 pt, chrome 12 pt); split rather than shrink | fancy-design, slide-writer, maestro |
| Explanation moves to its own slide when a slide would pass ~850 characters | fancy-design presentation_quality |
| Roadmap (agenda) slide after the objectives | slide-writer, slide-skill academic |
| Page numbers "05 / 24" | guizang, slide-skill academic |
| Notes end with a timing estimate (140 words/min) and the next slide's title | slide-skill rehearse, guizang notes |
| Alt text on every picture | maestro, knowledge-cat |
| Lint pass to `qa-report.json`: overflow >15%, font <12 pt, contrast, placeholders, density >900 characters, 3 dense slides in a row | slide-skill, fancy-design, knowledge-cat, slide-creator |

Not taken: HTML/WebGL decks, CDN scripts, auto-updates (`git pull`), public deploys (Vercel), remote OCR or MCP
uploads, reuse of stored login tokens. image-to-editable-ppt-skill's SKILL.md tells agents to pre-justify permission
prompts (prompt injection); slide-writer ships settings that pre-allow `git push`. Both stay disabled.

## Timed decks (CNS book, 2026-09-30)

User: "every section exactly 40 minutes; fit the content to it; review every slide visually before handing over".

| Problem | Fix in the tool |
|---|---|
| Full decks ran 39-54 slides for a 40-minute section | `fit_to_minutes`: each slide group has a priority and a time cost; greedy fill of the session; the first slide of every section and the first 3 MCQs always stay; `callout_priority` in slides.json ranks callouts |
| Timing must add up exactly | Notes end "Time m:ss (at mm:ss of 40:00)"; per-slide seconds in 15 s steps, the last slide absorbs rounding |
| A split table kept "(1/2)" after its second half was dropped | Kept parts are renumbered; a lone part loses its suffix |
| A callout with a list inside (`> - ...`) lost its list to the previous slide as "> -" rows | The parser joins `>` lines to the callout; card and panel draw several paragraphs |
| Narrow first column broke words ("Thiopenta/l") | Each column is widened to its longest word, taken from the widest column |
| Long cards shrank to small text | Card shrinks only to 22 pt, then grows to the content band, then shrinks to 18 |
| Accent tint on the accent was 4.3:1 | `acc_l` picks the first tint reaching 4.5:1 |
| Tool commits after a finished book staled its gate | `build_slides` uses the content-only gate (DEC-009 in the CNS project): approvals and every hash checked, tool SHA not |

## Study decks (build_study, marketing-book ch01, 2026-10-01)

User: "a clear, summarised PowerPoint that also works for studying; the content fixed to the source; build it step
by step, one chapter at a time, and improve the skill as we go".

Answers to the first questionnaire (the defaults for every study deck until the user changes them):

| Question | Answer |
|---|---|
| Fidelity | Shortened but traceable: every point shortens one chapter sentence; section number on every slide |
| Audience | Lecturer and student together: explanation on the slide and the section's prose in the notes |
| Contents | Section summaries; definitions and comparison tables; MCQs (question, then answer); one-page revision |
| Language | English, as in the book |

How the tool keeps the content fixed to the source: the agent writes only the condensed outline
(`slides/study/<stem>.json`), each point with a verbatim `src`; `build_study.py` refuses to build if a `src` is not
in the chapter, if any word or number on a slide is not in the chapter, if a point shares less than half its words
with its `src`, or if a section has no slide. Callouts, glossary definitions, MCQs and takeaways are copied, not
written. Deck: title, objectives, roadmap, per section points/table slides then its callouts, key terms, MCQs,
"Chapter N on one page".

| Problem | Fix |
|---|---|
| python-pptx missing from the system Python | `python -m pip install --user python-pptx` |
| Figures not found for books whose figures live under `rework/figures` | `build_slides.figures()` reads `template.paths.figures` |
| Faded MCQ options at 4.2:1 | `Style.mut_f`: darkened until 4.6:1 on the faded disc |
| Long figure caption overflowed its 0.4" box | Caption box grows with its text; the picture shrinks to make room |
| Revision slide ran into the footer; key terms as run-on text | Compact numbered list sized to fit; key terms in two columns on a card |
| Stop-words passing the vocabulary check as stems ("mostly" → "most") | Stems are filtered against the stop list too |
| Contact sheet showed each slide twice | Windows globs are case-insensitive: glob `Slide*.PNG` only |

Second round (same day). User: "more figures in the slides, so the information is summarised better for the
lecturer and for the student while studying; the title bold and inside a clear frame".

| Request or problem | Fix |
|---|---|
| More figures | Five native diagram kinds (flow, cards, versus, equation, spectrum) with a key-message caption bar; ch01 went from 1 figure to 14 diagram slides |
| Title bold in a clear frame | Framed title band (primary border, tint fill) on every content slide; `slides.json` `study.title_frame: false` turns it off |
| Kicker at 4.3:1 on the band tint | Accent darkened until 4.6:1 on the band |
| Boxes half empty, text small | One label size, header height and text size per row; boxes shrink to their text and are centred |
| Text 13 pt in narrow boxes | Width estimate measured on exports: body 0.43 em, bold heading font 0.56 em per character; text capped at 20 pt |
| One long node shrank a 10-card grid to 13 pt | Keep node texts short and alike (outline rule in the skill) |
| Faint caption bar | Primary tint with an accent stripe |

Third round (same day). User: "fewer words on each slide even if there are more slides; two questions per slide;
all the answers together at the end; a 3D glassmorphism design".

| Request or problem | Fix |
|---|---|
| Fewer words per slide | Caps: 4 points, 6 cards (a larger grid splits), 4 key terms, 300 characters per callout slide (split at sentence ends, every word kept); outline texts shortened; pages split evenly |
| Two questions per slide | `mcq_pairs`: two glass blocks per slide, options as 2 × 2 pills, no answer shown |
| Answers at the end | `answer_key`: 3 per slide (Q number, key letter, the right option, the book's reason) after the takeaways |
| 3D glassmorphism | Blurred colour-field backgrounds from the palette (light and dark); frosted panels (white at 58-80% opacity, white border, soft shadow); headers, discs, chips and arrows solid with a soft-round bevel |
| "01" and "vs" wrapped inside discs | Small shapes: no inner margin, no wrap |
| Label-only cards left an empty body | A label-only node is one 3D block |
| Words broken mid-word in narrow cards ("mammograph-y") | Text shrinks until the longest word fits a line (0.57 em for the longest word; hyphenated parts counted apart) |
| Long options in one column came out tiny | Options always 2 × 2; long ones wrap inside their pill |

## Source decks (community-pharmacy, tonsillitis, 2026-10-01)

User: a new project "community pharmacy" from 16 course files (Port Said University and East Port Said National
University), decks made with the study-deck skill, first deck on tonsillitis, "make graphics that make studying
easier, and use the pictures where there are pictures"; chose a light deck project (no book), no author name, the
sore-throat treatments and the quiz and lab cases included, the sources' pictures used.

| Need or problem | Fix |
|---|---|
| A deck without a book | `build_source_deck.py` (gate: evaluate) runs `build_study.main(source=True)`: one deck per outline, built from the `# Topic N` part of `ingest/normalized.md` |
| Questions and takeaways are not in the source text | Outline `mcq` and `takeaways`, each checked against the source (words, verbatim src, reason share) |
| Pictures | `image` on points slides and diagram nodes; files in `slides/study/images/` (inside `images/` they broke the ingest contract: UPSTREAM-STALE) |
| A case from a lab sheet | `case` slide: the case verbatim beside the points that answer it |
| No glossary or objectives in the sources | Key-terms and objectives slides are skipped; title facts drop zero counts |
| Slashes do not break lines in PowerPoint ("antipyr-etics") | Space the slash in the outline ("Analgesics / antipyretics") |
| The source contradicts itself (Benzydamine spray >12 years and >6 yrs) | Asked the user; marked "to be confirmed" on the slide |

## Design round from the GitHub survey (2026-10-01)

User: "install all of them in the harness and make a workflow to create good-looking slides". Cloning the
skills was blocked by the auto-mode safety classifier (untrusted code integration), so nothing was installed; their
published ideas were rebuilt in build_study.py instead, and the workflow is the skill's section 6.

| Idea (source skill) | In the tool |
|---|---|
| Action titles, ghost-deck test (academic-pptx-skill, agent-slides critique) | Titles written as messages; the review note lists the titles alone |
| Big-number layout, layout variety (siril9 presentation-skill, danny0926 ppt-skills) | `stats` kind; `variety()` warns when a layout repeats on the next slide |
| One consistent icon style (claude-office-skills ppt-visual) | `"icon"` per node: colour emoji (Segoe UI Emoji) on a white glass disc above the card; no downloads |
| Luminous borders, one metaphor, contrast first (bergside glassmorphism) | A light highlight line along the top of every large panel; contrast lint unchanged |
| Rendered visual QA (siril9, agent-slides audit) | `--review`: PNG of every slide, contact sheets, review note |

| Problem | Fix |
|---|---|
| Icons on the card edge covered the header text | Icons sit above the card; diagrams with icons start 0.8" lower |
| Long action titles wrapped out of the band | Title size fits one line (30 down to 20 pt) |

## Glass look for teaching decks (CNS, 2026-10-01)

User: "re-design the CNS decks, visually only". The glass primitives moved from build_study.py into build_slides.py
(`Glass` mixin, `backgrounds()`); study decks use them unchanged. `slides.json` `"look": "glass"` builds the same
teaching slides (same count, same content) on blurred colour fields, with the framed title band, frosted callout,
stat and option panels, and bevelled pills and the right answer.

| Problem | Fix |
|---|---|
| "Why:" accent at 4.1:1 on the glass background | Uses the darkened kicker colour (4.6:1) |
| Explanations and figures as bare text on the blurred field: hard to read, not professional (user) | Content band on one frosted sheet (84%); explanations with an accent bar; figures on a white card with a soft shadow; the feature-callout text on its own sheet |
