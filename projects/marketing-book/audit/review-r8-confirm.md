# Confirmation review of commit 2ad98f1 — marketing-book

reviewed_commit: 2ad98f1

Final read-only review by claude-sonnet-5-5 as a fresh-context subagent, recorded under DEC-003 (Claude reviewer in place of Codex). The book was written by claude-opus-5-5.

This review completes a two-part process:
- Round 8, saved in `audit/review-r8.md`, was a full-book review of commit 173e24d. Its verdict was pass, with 0 blocker or major findings and 2 minor ones.
- Commit 2ad98f1 fixed those 2 minors, changing two sentences, in rework/ch05.md and rework/glossary.md and in the built book.
- This review read that diff against round 8, checked the changed passages in context, and searched the whole build for other instances of the same two problems.
- For every text that was not changed, the round 8 full-book verdict stands.

Saved verbatim from the verdict line on. Kept as a record: the audit closed on it once (7828cc7), then the five rescore minors were fixed and the audit re-run.

verdict: pass
open_blocker_major: 0
reviewer_model: claude-sonnet-5-5

| ID | severity | location | finding | why it matters | suggested fix |
|---|---|---|---|---|---|
| none | - | - | Both r8 findings are resolved and commit 2ad98f1 introduced nothing wrong. | - | - |

Notes:
- **Diff scope.** The diff of `rework` and `build/Healthcare_Marketing.md` between 173e24d and 2ad98f1 contains exactly three substantive changes, each mirrored between the source file and the build.
  - The glossary entry "societal marketing orientation" now reads "the most appropriate one for health services". This resolves C-001. It matches Ch1 §1.6 (line 175), the takeaway (line 190), Q9 (line 242) and the Q9 key (line 280), which all say "most appropriate" or "best fits".
  - Ch5 §5.1 "No transfer of ownership" now reads "The patient receives the performance and its results, such as the images and the report, but does not come to own the service itself." This resolves C-002. It fits the services table row at line 1066 ("No: the buyer receives a performance") and the closing sentence of the paragraph.
  - `rework/ch05.md` and `rework/glossary.md` carry the same edits as the build.
- **E1.** The model answer at line 1300 already says "the patient receives a performance and a report". It was left unchanged and is consistent with the new §5.1 wording.
- **Remaining instances.** A grep of the build found no "only acceptable" or similar exclusivity claim about orientations, and no remaining "patient owns the report/scan" wording. The other "owns" and "ownership" hits are the distribution-channel and consignment passages in Ch8, which are accurate and unrelated.
- **Other files in the commit.** The commit also touched `audit/fixes.md`, `audit/review-r8.md`, `state.json` and the rebuilt docx and pdf. The docx and pdf contents were not examined. `state.json` is written only by `run_stage.py`, so it was treated as consistent and not inspected.
