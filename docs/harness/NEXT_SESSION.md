# Kick-off prompt for the next execution session

Paste this into a new Claude Code session opened in `D:\yasser`:

```text
Continue the book-harness ticket, STEP 9b (absorb the Dr. Mo book-designer skill). Tasks 9b.1-9b.3 are committed; HEAD is 6ee44fe (c995741 is pushed to origin/master; 6ee44fe is not).

Read these first, in full:
- CLAUDE.md (root: Rules 7, 8, 11)
- docs/harness/TICKET.md ("STEP 9b"), docs/harness/LEDGER.md, docs/harness/DECISIONS.md (DEC-043..046; next is DEC-047)
- docs/superpowers/plans/2026-09-25-book-harness.md: "STEP 9b" Tasks 9b.1-9b.6
- docs/harness/references/dr-mo-food-analysis/README.md (the benchmark and the defects to avoid)

Done:
- 9b.1 harness/tools/blocks.py: one block grammar for DOCX and HTML; ~x~ subscript, ^x^ superscript. Medical golden matched.
- 9b.2 harness/tools/build_html.py: theme.build.pdf.engine "html" (Edge print, pypdf merge, contents page numbers from the outline, bookmarks, metadata); theme schema: build.pdf.engine, cover.design, layout.drop_cap, font_files. Fixture tests/fixtures/editorial-book.
- 9b.3 harness/tools/check_pdf.py: PDF-SIZE/BLANK/META/TYPE3/EMBED/FONTS/OUTLINE, run by `run build` for both engines; checkpoints in build/checkpoints (PyMuPDF, optional group evidence).

To do, in order:
1. Confirm tests.test_bypass_matrix and tests.test_build (medical golden, now with check_pdf in the build) pass on c995741; fix in a new commit if not.
2. 9b.4 annotated figures (diagram.annotated, FIG-ANNOT, key under the caption in both writers).
3. 9b.5 TYPO-LATEX, RHYTHM-PROSE (template.readability.max_prose_run_words), CHEM-FORMULA-PLAIN (chemistry pack check_text); mutations per ID.
4. 9b.6 editorial-book gains an annotated figure and a case table; tests/tools/make_step9b_evidence.py; evidence PNGs under docs/harness/reviews/step9b-evidence/; INTAKE_QUESTIONNAIRE topic L (palette, logos, PDF engine).
5. Deviations from the plan go in reviews/step9b-rulings.md: no ltr-editorial preset was needed (the HTML engine reads the theme's own preset); chapter opener pages keep the running head (Chromium has no per-named-page :first).
6. Full suite (background), one read-only Codex review of STEP 9b via codex-delegate (no --ignore-user-config), Fix Protocol into step9b-fixes.md, including every evidence PNG.
7. Refresh the medical intake receipt (config.py and theme.v1.json changed; precedent 30dfdfe), then `verify --through rework` exit 0; LEDGER row 9b done.

Rules: inline, at most 2 Claude subagents with a reason; commit after gates pass; push only when the user asks (DEC-028); stop at every approval point. Talk to me in simple Arabic, briefly.
```
