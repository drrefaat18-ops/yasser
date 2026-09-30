# Design items Codex review (NEXT_DESIGN_ITEMS.md, Items 1-2, with the 2026-09-28 editorial options)

reviewed: uncommitted working tree on b8774ee (read-only `codex exec`)

| ID | Severity (blocker/major/minor) | File:line | Problem | Concrete fix |
|---|---|---|---|---|
| D-01 | major | `harness/tools/build_html.py:283` | Old presets no longer produce byte-identical output. `stylesheet()` always emits rewritten running-head rules and all new editorial CSS, even when no new keys are set; `Writer.inline()` at line 107 also always inserts NBSPs. The added test only compares editorial CSS against the newly generated plain CSS, never against the previous output. | Preserve the legacy rendering path verbatim when the resolved design uses built-in defaults and no new content options are configured, including the old stylesheet and inline-text behavior. Add a golden assertion comparing the complete HTML/stylesheet for an unchanged old-preset fixture with the pre-change bytes. |
| D-02 | major | `harness/tools/check_pdf.py:128` | PDF-BLEED uses a non-paper top-left pixel to decide whether a page is full bleed. A bleed failure that exposes paper at the top-left is therefore classified as an ordinary page and passes without any edge checks—the gate bypasses the exact defect it should catch. | Identify expected bleed pages from document structure/config or explicit page evidence rather than from the pixel being validated. At minimum, evaluate all edge samples before classification and add a regression test where only the top-left edge leaks. |
| D-03 | major | `harness/tools/check_pdf.py:128` | The `continue` after bleed processing prevents PDF-DASH from inspecting every page classified as full bleed. Thus a chapter opener, part page, cover, or ending page whose text begins with an em/en dash passes PDF-DASH. | Extract and test text lines for PDF-DASH on every page; limit only PDF-HEAD to non-bleed pages. Add a full-bleed-page test containing a leading dash. |

verdict: fail