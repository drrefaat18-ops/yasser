# Reference: Dr. Mo's *Principles of Food Analysis* (2026)

A finished book, kept as a **reference for future work** (DEC-046). It is not a harness project: no stage runs on it and the files here are never edited.

| File | What it is |
|---|---|
| `food-analysis-2026.pdf` | The finished book: 208 pages, 570 × 810 pt, 11 chapters and a case-studies appendix, 85 images. Author: Assoc. Prof. Dr. Mahmoud Elkhoudary, Faculty of Pharmacy, East Port Said National University. |
| `SKILL.md` | The `dr-mo-book-designer` skill that produced it. |

## What the harness takes from it (the benchmark)

Match these in the HTML PDF engine (`theme.build.pdf.engine: "html"`), from project config only (Rule 8):

- Full-bleed designed cover and closing page in the primary colour, with logos, an eyebrow label, title, subtitle and author block.
- Chapter opener: summary box, objectives, drop cap on the first paragraph.
- Running heads (chapter left, institution right) and page number in the footer.
- Tables with a dark header row and striped body rows; callout boxes with a coloured edge.
- Apparatus figures with numbered badges, leader lines and a component key under the caption (`diagram.annotated`).
- Chemical formulas with real subscripts and superscripts (`CO~2~`, `Ca^2+^`), structures from SMILES.
- A visual every 400–500 words of prose (`RHYTHM-PROSE`).
- Case studies with data tables and worked answers.

## What the harness must not repeat (measured 2026-09-28)

`check_pdf.py` fails this PDF on every one of these; our books must pass them:

- `PDF-META`: title metadata empty; author is `DrMO87`, not the author's name.
- `PDF-TYPE3`: Type 3 fonts on 26 pages (the skill's own "Type 3 audit" did not catch them).
- `PDF-EMBED`: Helvetica, Playfair Display and Segoe UI not embedded on some pages.
- `PDF-FONTS`: 16 font families instead of the 4 the skill declares (Arial, Cambria Math, Consolas, Georgia, Helvetica, KaTeX ×3, Times New Roman, Segoe UI Black, …).
- `PDF-OUTLINE`: bookmarks are file names (`chapter1` … `chapter11`, `appendix` twice), not chapter titles.
- Page numbers restart in every chapter, so the contents page (1, 21, 41, 59, 79, …) points nowhere.
- Content errors a subject review must catch: bullets that also carry "1.", "2." numbers; in appendix Case 6 the answer calls chlorine 0.6 ppm a risk while the table's own limit is 0.2–0.8.
