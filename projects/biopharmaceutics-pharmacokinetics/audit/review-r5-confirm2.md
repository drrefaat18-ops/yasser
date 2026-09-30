# Confirmation of commit 918fc28 — biopharmaceutics-pharmacokinetics

reviewed_commit: 918fc28

This is a read-only review by claude-sonnet-5-5 (DEC-010), saved here in summary. Findings R-001 and R-002 were fixed in 9cf8529.

verdict: pass
open_blocker_major: 0
reviewer_model: claude-sonnet-5-5

| ID | severity | location | finding | why it matters | suggested fix |
|---|---|---|---|---|---|
| R-001 | minor | ch03 Example 3.1, Step 3 against Step 7 and the Answer | Step 3 took fe = 1 as known so that Du∞ = dose, and Step 7 then reported fe = 1.00 as a result. The argument was still circular. | The example never determined fe. | Reword the step, or estimate Du∞ without assuming fe. |
| R-002 | minor | ch03 LO3 against Example 3.1 | The new LO3 says "check Du∞ against the intercept", but the example had no such step. | The objective went further than the example demonstrated. | Add the intercept check. |

Notes (summary):
- F-001 is resolved. ch09 now starts D B C A, unique across the 14 chapters, and the keyed options and rationale letters are correct.
- F-002 is resolved.
