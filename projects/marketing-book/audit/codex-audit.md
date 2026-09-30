# Audit review of the finished book — marketing-book

reviewed_commit: 4d7ae39

This is a read-only review by claude-sonnet-5-5 as a fresh-context subagent, recorded under DEC-003 (a Claude reviewer in place of Codex). The book was written by claude-opus-5-5.

The full audit chain ends in `audit/review-r10-final.md`, which passed at 2ba249a and scored the book 89.5.

Commit 4d7ae39 then recorded the user's design approval (DEC-004). It updated three passages of design/design.md and rebuilt the book, so the PDF and DOCX changed byte for byte. This review confirms that the book's content is unchanged, so the audit and its scores carry forward.

Saved verbatim from the verdict line on.

verdict: pass
open_blocker_major: 0
reviewer_model: claude-sonnet-5-5

| ID | severity | location | finding | why it matters | suggested fix |
|---|---|---|---|---|---|
| none | none | n/a | Book content did not change between 2ba249a and 4d7ae39. | n/a | none |

Notes

**1. Git diff 2ba249a to 4d7ae39**
- The diff of `rework/` and `build/Healthcare_Marketing.md` is empty: every chapter and the built markdown are unchanged.
- The design.md diff has three changes, each checked against the book:
  - **ch11 row in §4.** It now reads "four comparative methods, with cost-of-illness as a descriptive study". This matches `rework/ch11.md`, which names four methods (CMA, CEA, CUA, CBA) and treats cost-of-illness as a related descriptive study. Table 11.1's caption says the same, and the COI section says it is not a full economic evaluation.
  - **§7 figures.** The new text lists 22 figures: 15 diagrams, 3 illustrations and 4 photographs. `rework/figures/figures.json` has 22 entries and `rework/ch*.md` contain 22 image references. `photo-sources.md` lists the 4 photographs, all public-domain works from Wikimedia Commons: the ch04 imaging room, the ch05 microbiology laboratory, the ch06 MRI installation and the ch08 pharmacy counter.
  - **§8 NARS.** Only the wording changed ("start without" became "finish without"), and the rule for a later mapping is kept. There is no factual conflict.

**2. PDF comparison** (old file from `git show 2ba249a:...`, new file from 4d7ae39, both read with pymupdf)
- Both files have 136 pages.
- The extracted text is identical on all 136 pages.
- The image lists (xref and size) match on all 136 pages.
- Pages rendered at 50 dpi are pixel-identical on all 136 pages.
- The metadata is identical: same title and author, creator "book harness (HTML engine)", producer pypdf, and empty creation and modification dates.
- The file sizes differ (5,491,472 bytes against 5,437,305). Since text, images and rendered pixels all match, the byte difference is not visible content.

**3. DOCX comparison**
- Both files contain the same 124 zip members.
- All 22 `word/media/*` files are byte-identical.
- The extracted `<w:t>` text of `document.xml` is identical: 250,732 characters.
- With the volatile ids stripped (paraId, textId, rsid, durableId), `document.xml` has the same length and the same set of tags. The only remaining differences are the `_Toc` bookmark numbers.
- The other members that differ hold only volatile data: the timestamp in `core.xml`; the rsid, paraId and durableId values; and the obfuscation GUID header of the embedded fonts.
- The DOCX was regenerated with new random ids, a new timestamp and new font obfuscation keys; its content is identical.
