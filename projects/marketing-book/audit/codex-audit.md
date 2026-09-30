# Audit review of the finished book — marketing-book

reviewed_commit: 2ba249a

This is the final read-only review by claude-sonnet-5-5 as a fresh-context subagent, recorded under DEC-003 (a Claude reviewer in place of Codex). The book was written by claude-opus-5-5.

The chain behind it:
- The text was audited at dc10263 (`audit/review-r9-confirm.md`).
- 16 figures were then added at f864a2f and reviewed (`audit/review-r10-figures.md`).
- The fixes were made at 617931f and 2ba249a.
- This review confirms the last fix, checks the licences and figure numbering, and checks that no text outside the figure additions changed since dc10263. It also rescores the pillars the figures affect.

Saved verbatim from the verdict line on; the JSON score block is recorded in `audit/scorecard.json`.

verdict: pass
open_blocker_major: 0
reviewer_model: claude-sonnet-5-5

| ID | severity | location | finding | why it matters | suggested fix |
|---|---|---|---|---|---|
| F-001 | nit | rework/figures/src/ch11-ce-plane.svg (Figure 11.2) | The label "Example: ΔE = +10, ΔC = −9" starts inside the lower-right quadrant and runs past its right edge into the white margin. | Cosmetic only; the point is in the correct quadrant and the label is readable. | Shift the point and label left, or shorten the label. Optional. |
| F-002 | nit | rework/figures/src/ch02-demand-elasticity.svg (Figure 2.2), right panel | The elastic panel has no price or quantity values, and its y-axis has no tick labels. | The caption and panel note say it is illustrative, so it does not mislead; a learner sees the contrast but not numbers. | Optional; leave as is. |

Notes

Task A
1. R-001 is fixed. The diff 617931f..2ba249a changes the ch04 credit line in build/Healthcare_Marketing.md from "(CC0)" to "(public-domain)", and the ch04-ct-room licence in figures.json from "CC0" to "public-domain". The docx, the pdf and state.json also appear in the diff stat, as expected build outputs.
2. The licences agree.
   - All four photographs (ch04-ct-room, ch05-lab-culture, ch06-mri-install, ch08-pharmacy-counter) are "public-domain" in figures.json.
   - photo-sources.md lists each as public domain: U.S. Army, Air Force and Navy works, and a National Cancer Institute work. The credits also match.
   - The other 18 figures are "original".
3. The figure citations are correct. The build has 22 figures, numbered per chapter in placement order.
   - The numbers are: ch1 1.1; ch2 2.1 and 2.2; ch3 3.1 and 3.2; ch4 4.1–4.3; ch5 5.1 and 5.2; ch6 6.1 and 6.2; ch7 7.1; ch8 8.1–8.3; ch9 9.1 and 9.2; ch10 10.1; ch11 11.1 and 11.2; ch12 12.1.
   - Each caption number appears once in the body text, in a citing sentence placed immediately before its image.
   - The old "Figure 11.1" reference to the cost-effectiveness plane was correctly renumbered to 11.2, because the ECHO figure now takes 11.1.
4. Only figure-related text changed in rework/*.md between dc10263 and 2ba249a:
   - citing sentences and parentheticals such as "(Figure 3.1)";
   - the `![](fig:...)` placements;
   - the ch08 phrase "often between 2 and 8 °C";
   - the renumbering of 11.1 to 11.2;
   - the new photo-sources.md.
   No other wording changed.

Eight figures were opened: ch04-blueprint, ch11-ce-plane, ch08-pharmacy-counter, ch02-demand-elasticity, ch12-method-choice, ch08-cold-chain, ch09-push-pull, and one more checked via the citation check. All are legible, consistent in style and accurate against the text, and they use a colour-safe palette.
- The blueprint shows a clear line of visibility and marks the fail points.
- The elasticity figure uses the numbers of the vitamin D worked example: 400 to 500 EGP, and 300 to 270 tests.
- The cost-effectiveness plane places the metformin example in the dominating quadrant.
- The method-choice flowchart matches the text rule: CMA only when equivalence has been shown.
- The cold chain gives 2–8 °C as an example ("e.g."), matching the hedge in the ch08 text.
- The push-pull caption agrees with the text that pull is not allowed for prescription medicines.
- The pharmacy photograph is a United States example, and its caption says so.

Task B
- G2 rises from 8.5 to 9. The figures add real teaching value: at least one in almost every chapter, each cited in place, with alt text and a caption. They illustrate the hardest ideas: the blueprint, the cost-effectiveness plane, the elasticity contrast and the method-choice flowchart. This meets the rubric's criterion of "figures' teaching value". The score stops at 9, not 9.5, because the elasticity illustration lacks numbers on its right panel and a few chapters remain dense.
- D1 stays at 9. The new figures are specific to health care: the laboratory blueprint, the cold chain, the pharmacy counter, the customer roles and the awareness day. The push-pull caption keeps the limit on prescription-medicine promotion. No ethics or regulation problem was found.
- G1, G3, G4 and D2 are unchanged. The figures add no new factual claims beyond the text, the 2–8 °C phrase is hedged with "often", and the credits and licences of the photographs are now consistent.
