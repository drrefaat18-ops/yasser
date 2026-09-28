# STEP 9b Codex review

reviewed_commit: 1ef9bd911187094427e60f84d264c51f0e59aeb8  
verdict: fail  
open_blocker_major: 4

## Findings

| ID | Severity (blocker/major/minor) | File:line | Problem | Concrete fix |
|---|---|---|---|---|
| S9b-01 | major | `harness/tools/build_book.py:605` | H3 content drifts between writers. DOCX writes `b["text"]` literally, including inline Markdown such as `CO~2~` or `**bold**`; HTML processes the same block through `inline()` at `build_html.py:159`. | Render H3 DOCX text through `Renderer.inline()` into an empty Heading 3 paragraph. Add a parity test covering bold, italic, subscript, superscript, and links in H3 blocks. |
| S9b-02 | major | `harness/tools/config.py:64` | Logo and font paths are checked for containment but not existence or regular-file status. A missing logo can silently disappear in the HTML PDF, while a missing font can fall back to an installed font. Because `contracts.py:125` hashes only existing glob results, the absent configured input is also omitted from the receipt. | Require every configured logo and font file to be an existing regular file during config validation. Add each configured path explicitly to build inputs rather than relying only on directory globs. Test missing logo and missing font cases. |
| S9b-03 | major | `harness/tools/check_pdf.py:103` | `PDF-OUTLINE` checks only whether each chapter title is a substring of any bookmark title. It does not verify exact normalized titles, uniqueness, hierarchy, order, or destination pages. A bookmark with the right words but pointing to the wrong page passes. | Derive the expected ordered outline and expected chapter-start pages, then compare normalized titles and destinations exactly. Add mutations for wrong destination, reordered bookmarks, misleading superstrings, and duplicate titles. |
| S9b-04 | major | `harness/tools/check_book.py:408` | `TYPO-LATEX` recognizes only a short command allowlist. Raw TeX such as `\sqrt{x}`, `\alpha`, `\begin{equation}`, `\[x\]`, or an unknown command passes even though the writers print it literally. | Detect general TeX constructs outside code fences, including control words, control symbols, display delimiters, and environments. Preserve explicit exclusions for ordinary backslashes if required, and add negative controls plus representative missed constructs. |
| S9b-05 | minor | `harness/tools/check_pdf.py:86` | `PDF-BLANK` treats a page containing only vector drawing operators as blank because it checks extracted text and raster images only. This can reject legitimate vector-only pages. | Inspect the page content stream for painting operators or rendered bounds, or rasterize at low resolution and test whether the page differs materially from its background. Add a vector-only-page test. |
| S9b-06 | minor | `harness/figures/annotated.py:41` | An existing but invalid/corrupt base image raises from `PIL.Image.open()` instead of producing `FIG-ANNOT`. The checker can therefore crash rather than return its promised report. | Catch `UnidentifiedImageError`/relevant image I/O errors in `problems()` and return a `FIG-ANNOT` message. Add corrupt and unsupported-image fixtures. |

## Evidence PNGs

| File | Verdict | Notes |
|---|---|---|
| `annotated-figure.png` | Pass | Diagram, badges, leader lines, caption, and numbered key are legible. Nothing is clipped. Green/gold/blue palette is coherent and the key wraps cleanly. |
| `contents.png` | Pass | Fully legible with no clipping. Dotted leaders align properly. Roman `iii` and body pages 1–9 are plausible relative to the other evidence pages. |
| `cover.png` | Pass | All text and the logo are sharp and inside the frame. Green, white, and gold match the configured visual scheme; no edge clipping is visible. |
| `first-chapter.png` | Pass | Heading, callouts, objectives, drop cap, citations, running head, and page number are clear. No clipping or overlap. |
| `first-figure.png` | Pass | Both figures and captions are legible, with no clipping. Chart labels remain readable and the page numbering is plausible. |
| `last.png` | Pass | Glossary columns and running head are legible. Nothing is clipped; page 9 agrees with the contents page. |
| `table.png` | Pass | Graph, table, and viewpoint grid are legible and use the configured green/blue/orange palette. The final paragraph continues naturally onto the next page rather than being visibly clipped. |

## Notes

- Gate enforcement and executable registry coverage are present for both new command-line tools.
- The STEP 9b tool paths are included in the build/rework provenance sets, and no Rule 8 vocabulary or absolute-path leak was found under `harness/`.
- `check_book.py` and the modules loaded by `text_packs()` remain standard-library-only at import time.
- The existing tests do not exercise H3 writer parity, configured-but-missing logo/font inputs, wrong bookmark destinations, general TeX syntax, or vector-only PDF pages.
- Review was static and read-only as requested; the test suite was not run.
