# STEP 9b rulings (deviations from the plan and judgement calls)

| # | Ruling | Why |
|---|---|---|
| R1 | No `ltr-editorial` preset. The HTML engine reads the theme's own preset (page size, title-page layout) and the theme tokens. | The look is theme config; a second preset would duplicate `ltr-textbook` with no new value (YAGNI). |
| R2 | Chapter opener pages keep the running head in the HTML engine; Word drops it there. | Chromium has no per-named-page `:first`; Dr. Mo's reference also keeps it. |
| R3 | The body, front and cover are separate Edge prints merged by pypdf. | Arabic page numbers must start at 1 on the first body page and roman numbers on the title page; Chromium cannot reset the page counter. |
| R4 | Contents page numbers come from Edge's own outline (`--generate-pdf-document-outline`), matched heading by heading against what the writer placed; a mismatch fails the build. | One source of truth; no text search in the PDF. |
| R5 | `PDF-FONTS` allows, beyond the theme fonts, only the engine's own fallbacks: Word adds Symbol (bullets), Calibri, Cambria and Arial; the HTML engine adds none. | The medical Word PDF uses them; changing its output would break the golden. |
| R6 | `PDF-BLANK` treats a page with no text and no image as blank; a vector-only page would be flagged. | None is placed today (marked `ponytail:` in the code). |
| R7 | Checkpoint PNGs need PyMuPDF (optional group `evidence`); without it the build report says `skipped`. | Rule 10: diagnose, never install. |
| R8 | Annotated-figure labels are printed as the key under the caption, not drawn on the image. | Crisp, searchable and translatable (STEP 11); Dr. Mo's figures do the same with a key banner. |
| R9 | `CHEM-FORMULA-PLAIN` flags two or more element symbols with a bare digit, or a common diatomic (`O2`); a single element with a number (`B12`, `Ca2+`) is not flagged. | Avoids false hits on vitamin and code names. |
| R10 | Pack text checks are discovered (`packs.text_packs()`), so `check_book.py` names no pack; the chemistry pack owns its element list. | Rule 8. |
| R11 | `logos` and `font_files` must lie under an allowed asset root. | They are then build inputs the receipt hashes (contracts.py). |
| R12 | `theme.palette.paper` (the page colour) is applied by the HTML engine only; Word pages stay white. | The user asked for the cream page of the reference PDF; Word page colours do not export to PDF reliably. |
| R13 | AI-made images are accepted as author-supplied figures with no AI label (DEC-044); the harness still calls no image generator. | User ruling. |
