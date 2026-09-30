# Audit review of the finished book — biopharmaceutics-pharmacokinetics

reviewed_commit: 9cf8529

This is the final read-only review by claude-sonnet-5-5 as a fresh-context subagent, recorded under DEC-010 (a Claude reviewer in place of Codex, which is at its usage limit until 2026-10-05). The book was written by claude-opus-5-5.

The review chain:
- Round 5 (`audit/review-r5.md`) was a full-book review of 10215fb: 16 findings, 3 of them major, all fixed in 2dbaa01.
- The confirmation of 2dbaa01, with the rescore (`audit/review-r5-confirm.md`), passed with 4 minor findings; 3 were fixed in 918fc28.
- The confirmation of 918fc28 (`audit/review-r5-confirm2.md`) passed with 2 minor findings, fixed in 9cf8529.
- This review confirms 9cf8529. For all text not changed since each earlier review, that review's verdict stands.

Saved verbatim from the verdict line on.

verdict: pass
open_blocker_major: 0
reviewer_model: claude-sonnet-5-5

| ID | severity | location | finding | why it matters | suggested fix |
|---|---|---|---|---|---|
| R-003 | minor (optional) | rework/ch03.md line 144, Example 3.1 (mirrored in the build .md) | The intercept check is only weakly independent. The ARE column was built by subtracting from 1000 mg (840 = 1000 − 160), so extrapolating that line back to t = 0 returns about 1000 mg almost by construction. The text says it "reproduces the estimate of Step 3", which is slightly stronger than the evidence. | It is a self-consistency check, not a second estimate of Du∞. The arithmetic is correct and LO3 is now met, so a careful reader would find it only mildly generous. | Optional wording change, such as "confirms that the ARE line is consistent with Du∞ = 1000 mg". No fix is required. |

Notes:

1. **Diff scope (items 1 and 6).**
   - `rework/ch03.md` and the build .md carry the same 8-line text change.
   - `rework/math-checks.md` gains 21 lines.
   - `build-report.json`, the .docx, the .pdf and `state.json` are regenerated build and state outputs.
   - No other rework chapter changed.

2. **Circularity (item 2): resolved.**
   - Step 3 now states that 984 mg is not Du∞, because collection stopped at 6 h.
   - K = 0.682 h⁻¹ comes from the rate method of Step 4, which needs no Du∞. Recomputed: ln 640 − ln 23 over 4.875 h = 0.6823.
   - The fraction collected by 6 h is 0.983, so Du∞ = 984 ÷ 0.983 ≈ 1000 mg. The text labels this an estimate, not an assumption.
   - fe = Du∞/dose = 1.00 is then a result, and Step 7 says so.
   - Step 3 cites Step 4's K before Step 4 appears, but says so explicitly, which is acceptable.

3. **Numbers (item 3).** All were recomputed in python and all match the text.

   | Quantity | Recomputed | Text |
   |---|---|---|
   | 1 − e^(−0.682×6) | 0.98329 | 0.983 |
   | 984 ÷ 0.98329 | 1000.72 | ≈ 1000 mg, "to the nearest 10 mg" |
   | 840·e^(0.695×0.25) | 999.40 | ≈ 999 mg |
   | K, Step 4 (rate method) | 0.68225 | 0.682 |
   | K, Step 5 (sigma-minus) | 0.69500 | 0.695 |

   The Step 5 logs (ln 840 = 6.7334, ln 62 = 4.1271) also match.

4. **Final sentence (item 4).** "Both give the overall elimination rate constant K, whatever the value of fe" is correct pharmacokinetics. Both the excretion-rate and sigma-minus plots have slope −K/2.303, and fe affects only the intercepts, through Ke·D and Du∞. The earlier wording, "as they must when fe = 1", was misleading, and this change corrects it.

5. **Math-check blocks (item 5).** The three new blocks match the text. The values (0.983 ± 0.001, 1000 ± 5, 999 ± 1) agree with the recomputation, the inputs match the text (K = 0.682, t = 6, Du6 = 984, ARE = 840, K = 0.695, t = 0.25), and the tolerances pass.

6. **Consistency with the surrounding text.** LO3 ("check Du∞ against the intercept") is now served by Example 3.1. The Common Mistake paragraph's "about 98% at six half-lives" agrees with the 0.983 fraction.
