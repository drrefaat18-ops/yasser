# STEP 9b fixes (Fix Protocol on `step9b-review.md`, reviewed commit 1ef9bd9)

| ID | Real / rejected | Root cause | Siblings found | Fix | Verification → result |
|---|---|---|---|---|---|
| S9b-01 | real | The DOCX writer passed heading text to Word as a raw string, while every other block went through the inline grammar. | Chapter titles (`heading1`) and the chapter running head had the same raw path. | H3 through `Renderer.inline`; chapter titles with markup through it too (a plain title keeps its single bare run, so the medical DOCX is unchanged); running head uses `blocks.plain`. | `tests.test_step9b_fixes.test_s9b01_*` → OK; medical DOCX parts byte-identical (snapshot diff empty) |
| S9b-02 | real | Logo and font paths were checked for containment only, and the build receipt listed only files that a directory glob found. | Same for `font_files`. | `config.path_problems` requires each configured logo and font to be an existing file under an asset root (paths normalised first); `contracts.files(build)` always lists them as inputs. | `test_s9b02_*` → OK |
| S9b-03 | real | `PDF-OUTLINE` tested a substring anywhere in the outline. | None. | `outline_problems`: exactly one bookmark `<n> <title>` per chapter, in plan order, whose page shows the title (line-end hyphenation rejoined). | `test_s9b03_outline_is_exact` (wrong page, duplicate, swapped order, superstring) → OK; medical deliverable and editorial PDF pass |
| S9b-04 | real | `TYPO-LATEX` used a short allowlist of commands. | None. | Any control word, display delimiters, and `$…$` that contains a TeX sign (prices pass); inline code spans are skipped. | `test_s9b04_general_tex` → OK; medical and both fixtures raise none |
| S9b-05 | accepted-minor | A vector-only page counts as blank. | — | Ruling R6 (documented; no such page is placed today). | — |
| S9b-06 | real | `annotated.problems` opened the base image without catching an unreadable file. | `to_svg` opens it only after `problems` passes. | Unreadable base → `FIG-ANNOT` message. | `test_s9b06_corrupt_base_is_reported` → OK |
| S9b-C01 | found-by-claude | `css_string` did not escape `<`, so a config string (title, chapter title, label) could close the `<style>` element. | `@font-face` URLs were quoted with `'` by hand. | `<` escaped as `\3c`; font URLs through `css_string`. | `test_s9b_c01_css_string_cannot_close_style` → OK |

Evidence PNGs: Codex passed all seven (`step9b-review.md`, "Evidence PNGs").
