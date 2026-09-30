# Next design items: editorial preset and visual-rhythm gate

Two proposed items for the HTML/PDF engine. They continue the design work of 2026-09-28, which adopted the lessons of `dr mo skill/SKILL.md`. Nothing here has been started. Read this file, then `harness/tools/build_html.py` and `harness/tools/check_pdf.py`, before starting.

## Background: what was done on 2026-09-28

The user's priority is the **PDF** and the **design of the HTML that renders it**. The following was added to the harness as **optional** `theme.json` keys (schema: `harness/schemas/theme.v1.json`). A book without these keys builds exactly as before.

| Key | Effect | Code |
|---|---|---|
| `layout.chapter_opener: "page"` | A full-bleed opener page for each chapter. It holds the chapter's h1, a part line, and an "In this chapter" list when `labels.in_this_chapter` is set. Part pages also go full-bleed. | `opener_html`, `body_parts` |
| `section_eyebrows: {section_id: text}` | A small uppercase accent kicker above that template section's h2. | `Writer.render` |
| `running: {style, head_left, footer_left, footer_center, page_number}` | `style` is `plain` or `caps`. Footer boxes on the left and in the centre; page number `center` or `right`. Heads are cut to a character budget, because Edge ignores `text-overflow` in margin boxes. | `stylesheet`, `clip`, `fit_heads`, `HEAD_EM` |
| `toc.style: "chapters"` | One row per chapter: the label, the title, the level-2 headings as a muted line, and the page. Parts appear as bands. | `toc_html` |
| `title_page.layout: "centered"` | A centred title page. The notices sit at its foot, so there is no near-empty notices page. | `title_page_centered` |
| `ending: {quote, attribution}` | A full-bleed closing page, printed as its own piece after the body. | `ending_html`, `build_pdf` |

The HTML writer also binds a spaced dash to the word before it (NBSP), so no line can start with "—" or "–".

Three new PDF gates were added in `check_pdf.py`. They use PyMuPDF and report `not_applicable` without it.

- **PDF-HEAD:** a running head or foot leaves the text width, or two of its lines collide (a wrapped head).
- **PDF-BLEED:** a full-bleed page shows the paper colour at an edge.
- **PDF-DASH:** a line starts with a dash. The frozen Word deliverable `projects/ai-in-medicine` has one real case (page 90); the tests subtract it as a `BASELINE`.

Tests: `tests/test_build_html.py` (WriterTest) and `tests/test_check_pdf.py`. For a gated full-book trial, use the preview pattern: copy a project into `temp_repo`, override its theme, stamp the state (unit receipts too) and `run build`. The real project is never touched. The CNS book is closed and out of scope (user, 2026-09-28).

---

## Item 1: an editorial preset

**Problem.** Every option above has to be switched on by hand in each book's `theme.json`. Until someone does that, a new book is built in the old, plain look.

**Proposal.** Add a preset that turns on the full editorial design, for example `harness/presets/ltr-textbook-editorial.json`. It follows the format of the existing `ltr-textbook-alexandria.json` (fonts, page, palette, `title_page_layout`, `required_font_files`) and adds default design values:

- `chapter_opener: "page"`
- `toc.style: "chapters"`
- `title_page.layout: "centered"`
- `running.style: "caps"`, `running.page_number: "right"`

**Decisions for the next session:**

1. **How theme and preset merge.** Today the preset supplies page geometry, fonts and the title-page layout, and the design keys are read only from `theme.json`. The rule to add: *theme value, else preset default, else built-in default.* Put it in one place, for example a `design(bk, key)` helper in `build_html.py`. Callers must not each read `th.get(...)` separately.
2. **Where the defaults go.** Either in the preset, or in the intake template that writes `theme.json`. The preset is simpler, and existing books can opt in by changing `"preset"`.

**Stays in the book's config (Rule 8: no domain in shared code):** footer text (author, course code), the ending quote and its attribution, section eyebrow words, and `labels.in_this_chapter`. These are content, not design. The preset holds none of them.

**Done when:**

- A fixture using the new preset builds with the HTML engine and passes all ten PDF gates.
- A book on an old preset builds byte-identically to the current output: the same stylesheet string for the same config.
- Unit tests cover the merge order.

---

## Item 2: a visual-rhythm gate

**Rule, from Dr Mo:** no more than about **400–500 words** of running prose without a visual break. A dense wall of text loses students.

**Proposal.** Add a check that runs over the chapter Markdown (rework output) before the PDF is built. For each chapter, it counts the words of consecutive `para` and `bullet` blocks, using the same parser as the renderer, `blocks.parse`.

- **Breaks that reset the count:** `table`, `image`, `callout`, `grid`, a boxed section, and `question`.
- **Report:** chapter, section heading, word count, and the first words of the run. Example: `ch03 · 3.2 Levodopa: 620 words (starts "Levodopa is…")`.
- **ID:** for example `RHYTHM-PROSE`, in the existing checker-report format (`harness/schemas/checker-report.v1.json`).

**Decisions for the next session (the user was asked and has not answered yet):**

1. **The threshold.** Proposed default: 450 words. It is set per book, in `rubric.json` or `template.json`.
2. **Warning or blocking.** Recommended: a **warning**. It is written to `build-report.json` and to the rework checker report, but does not fail the build. Some sections are legitimately prose-only (introductions, clinical cases).
3. **Where it lives.** Either in `check_book.py`, so it runs during rework and the author fixes it there, or in `check_pdf.py`, so it runs at build. Recommended: rework, because that is where the fix happens.
4. **Which blocks count as prose.** Should a numbered list count as prose or as a break?

**Done when:**

- A fixture chapter with a 600-word run triggers the check.
- The same chapter with a table inserted in the middle does not.
- The threshold is read from config, and no domain words are in the code.

---

## Order

Item 1 first: it is smaller and has an immediate visual effect on every new book. Item 2 second.

Rules still apply:

- **Rule 11:** work inline, one Codex review per artifact, then the Fix Protocol.
- **Commits:** commit after the gates pass; never push.

---

## Status at the stop (2026-09-28, nothing committed)

Items 1 and 2 are written, and so are the fixes from the review. Nothing new has to be written. What is left is to verify the work, then commit it.

### Done

- **Item 1: the editorial preset.**
  - Code: `DESIGN` and `design(bk, key)` in `harness/tools/build_html.py`. The order is: theme value, else the preset's `design`, else the built-in default. A bad preset value raises `BuildError`.
  - Callers: running style, page number, title page, contents style and chapter opener all read through `design()`.
  - New preset: `harness/presets/ltr-textbook-editorial.json`. It is the Alexandria preset plus a `design` block, and it uses the same CRLF line endings.
  - Tests in `tests/test_build_html.py`:
    - `test_design_merge_order`.
    - `test_preset_without_design_keeps_the_old_look`: an old preset gives the same output.
    - `test_editorial_preset_turns_the_design_on`.
    - `EditorialPresetBuildTest`: a full `run build` passes all 10 PDF gates. It passed.
- **Item 2: RHYTHM-PROSE.**
  - `check_book.check_rhythm` reads `blocks.parse`. A table, image, callout, grid, question or boxed section resets the count. Paragraphs, bullets and numbered items count as prose.
  - The message starts with the section heading.
  - It is a warning (DEC-047): `check_book.NON_BLOCKING`, `blocking()`, and `failures(report, warnings=False)`. `complete_checks/rework.py` uses `check_book.blocking`, and the CLI prints `WARN`.
  - Tests in `tests/test_text_checks.py`: a 600-word run fails and names the section; a table in the middle passes; the warning does not block.
- **Codex review: done once.** The user said not to send another. The review is `docs/harness/reviews/design-items-review.md`; the fixes are `design-items-fixes.md`.
  - D-01: a test only.
  - D-02: PDF-BLEED now reads all 8 edge samples.
  - D-03: PDF-DASH now runs on full-bleed pages too.
- **Two Word defects found by the stricter gates (DEC-048).**
  - `blocks.bind_dash` (NBSP before a spaced dash) is now used by both writers (`Factory.make_run` and `Writer.inline`).
  - The Word cover section's top margin is now `-635` EMU (-1 twip, an exact margin). Word no longer pushes the cover 13 pt below the empty header. This was tested directly with Word.
  - `tests/fixtures/ai-in-medicine/allow-step8.json` now allows `/hashes/docx` and `/hashes/docx_parts/word/document.xml`.
  - `BASELINE` in `tests/test_check_pdf.py` is now `{"PDF-DASH", "PDF-BLEED"}`: the frozen deliverable's page 90 dash and page 1 strip. They are pinned in `test_medical_deliverable_dash_is_found`.

### Left to do, in order

1. `python -m unittest tests.test_build.BuildTest tests.test_check_pdf` (about 6 minutes).
   - The last `test_build` run was before DEC-048. Its only diff then was the DOCX hash, which is now allowed.
   - If PDF-DASH or PDF-BLEED still fail on the fresh Word PDF, open page 1 and the glossary page of `build/*.pdf` in the temp repo.
2. Run the full suite in the background: `python -m unittest discover -s tests -t .` (about 25 minutes). The last full run had one F, most likely `test_build`. Confirm it.
3. Add two rows to `docs/harness/reviews/design-items-fixes.md`:
   - W-01: the Word cover strip.
   - W-02: the Word NBSP dash.
   - Give the root cause, the fix and the test for each, as in the table above.
4. Commit. Suggested: two commits.
   - (a) The 2026-09-28 editorial options and PDF gates.
   - (b) Items 1-2, the review fixes, DEC-047/048 and the Word fixes.
   - If splitting the files is hard, one commit is fine. Never push.
5. `verify` on `projects/ai-in-medicine` may now report stale build and rework receipts, because the harness tools changed. That is normal. Do not edit `state.json`. The ai-in-medicine and CNS books are frozen or closed.
