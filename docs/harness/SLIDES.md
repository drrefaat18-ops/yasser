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
