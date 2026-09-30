# Audit review of the finished book — biopharmaceutics-pharmacokinetics

reviewed_commit: 0e07287

This is a read-only review by claude-sonnet-5-5 as a fresh-context subagent, recorded under DEC-010: Claude only, in place of Codex, on the user's instruction ("خلص كتاب الكاينتكس بكلود بس"). The book was written by claude-opus-5-5.

The audit chain ends in `audit/review-r5-final.md`, which passed at 9cf8529 with a score of 86.5. Commit c96c149 then merged new shared tooling from origin: three new PDF gates, a dash-binding rule and cover-accent changes. Commit 0e07287 re-recorded the stages and rebuilt the book with that tooling. This review confirms that the book's content did not change, so the audit and its scores carry forward.

Saved verbatim from the verdict line on.

verdict: pass
open_blocker_major: 0
reviewer_model: claude-sonnet-5-5

| ID | severity | location | finding | why it matters | suggested fix |
|---|---|---|---|---|---|
| R1 | minor | PDF pages 10-40 and 42-52 (42 pages, all of Chapter 1 except page 41) | The running head changed. It used to be one line: "Biopharmaceutics and Pharmacokinetics **Chapter 1 · Introduction to Biopharmaceutics and Pharmacokinetics**". It is now split into a left cell and a right cell, and both are cut with an ellipsis: "Biopharmaceutics and…" on the left and "Chapter 1 · Introduction to Biopharmaceutics and…" on the right. Chapters 2-14 still show the full head in two cells. | The word "Pharmacokinetics" is cut from the running head on these pages. This is a cosmetic loss in the header, not in the body content; the full title remains on the cover, the chapter opener and the other headers. | Optional: shorten the Chapter 1 head text, or let the head wrap so the ellipsis is not needed. No action is required for acceptance. |

## Notes

**Step 1: git diff, 9cf8529 to 0e07287, for this book (14 files)**
- `rework/` has no diff at all, and neither does `build/Biopharmaceutics_and_Pharmacokinetics_PT312.md`.
- The files that changed are:
  - `audit/*`: codex-audit, codex-audit-r1, findings, fixes, review-r5-confirm, review-r5-confirm2 and scorecard.
  - `build/*`: the PDF, the DOCX, build-report.json, and the three checkpoint PNGs (cover, first-chapter, first-figure).
  - `state.json`.

**Step 2: PDF comparison (the old PDF from 9cf8529 against the current one)**
- The page count is 177 in both.
- After normalising whitespace (with U+00A0 treated as a space), 42 of the 177 pages have different text. Every difference is the running head on those pages (R1). No other word differs on any page, and pages 53-177 are identical in text.
- The images are unchanged: every page has the same images at the same sizes, 16 in total in each file, and no figure changed.
- Rendered at 30 dpi, 45 pages differ:
  - Page 1, the cover: the accent rules, the "PT-312" pill outline and the "Theoretical Notes" subtitle were gold in the old file and are now a muted or white tone. The title, the text and the layout are the same.
  - Pages 10-40 and 42-52: the running-head change described in R1.
  - Pages 162 and 173: small sub-pixel shifts confined to a thin band. On page 162 this is around the apparatus table and the "Apparatus 1 to 4 — basket" line. The text is identical; the shifts come from dash binding and line breaks. Page 162 was rendered at 50 dpi in both versions: the table and paragraphs are intact, with no overlap or breakage.
- No word, number, equation, figure or table changed. The only visible differences are layout and colour: the cover accents, the Chapter 1 running head, and minor dash and line-break placement on pages 162 and 173.

**Step 3: DOCX**
- The extracted text of `word/document.xml` is identical after NBSP normalisation: 345,637 characters in both.
- Both files contain 16 media files, with identical names and MD5 hashes.
- The new `document.xml` is about 2.5 KB shorter, which is markup only, and the DOCX is 5 KB smaller overall because of zip or style differences.

**Step 4: check_pdf.py**
- All 10 gates pass: PDF-SIZE, PDF-BLANK, PDF-META, PDF-TYPE3, PDF-EMBED, PDF-FONTS, PDF-OUTLINE, PDF-HEAD, PDF-BLEED and PDF-DASH. PDF-HEAD passes because it accepts the head truncated with an ellipsis.

**Method**
- git diff; git show to a temporary copy of the old PDF and DOCX; pymupdf text and image extraction; zipfile for the DOCX; and difflib at word level. Nothing in the repository was changed.
