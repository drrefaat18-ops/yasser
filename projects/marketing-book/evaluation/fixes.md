# Fix Protocol — Codex review of the evaluate stage

Review: `evaluation/codex-review.md` (GPT-5 Codex, verdict fail, 12 blocker/major, 5 minor).
Protocol: confirm each finding at its cited location, find the root cause, hunt siblings, fix, verify. All 17 were
confirmed against `ingest/normalized.md` before any edit; none was accepted on the reviewer's word alone.

| ID | status | real/rejected | root cause | siblings found | fix | verification → result |
|---|---|---|---|---|---|---|
| C-001 | fixed + verified | real | I read "the extra cost required to purchase an additional unit of effect" as a definition of incremental cost. It is the definition of an incremental ratio. | F-003 uses the same concept; it was already correct. | F-002 now says the definition itself is wrong (it describes ΔC ÷ ΔE), and its location spans the whole section. | Re-read lines 1131–1136 → ok |
| C-002 | fixed + verified | real | I missed that the lecture notes already carry the corrected −0.9 beside the slide's −15.36. The remaining error is the dominance rule, which belongs under D2. | — | F-005 rewritten around the negative-ICER rule, moved to D2, location 1426–1432. | Lines 1426–1432 contain both statements → ok |
| C-003 | fixed + verified | real | I wrote "never finish it" about the mix without checking lectures 3–6, which do develop each P. | — | F-015 now describes duplicated definitions and missing signposting; downgraded to minor. | Lectures 3–6 cover product, price, place and promotion → ok |
| C-004 | fixed + verified | real | Severity overstated: the arithmetic is right and the conclusion follows. | — | F-029 downgraded to minor; its claim now states that the arithmetic is correct and the defect is labelling. | 60, 82, 5 ÷ 22 = 0.227 reproduce → ok |
| C-005 | fixed + verified | real | Missed: I read the importance list as motivation, not as a decision rule. | The same rule was in my own Chapter 10 draft, §10.1. | Added F-032 (G1, major). Chapter 10 §10.1 rewritten (see the rework commit). | Line 1045 carries the phrase → ok |
| C-006 | fixed + verified | real | Missed: I accepted the lecture's grouping of WTP with the productivity methods. | My Chapter 10 draft §10.6 repeated the grouping. | Added F-033 (G1, major). Chapter 10 §10.6 separates productivity valuation from WTP and defines the friction period. | Lines 1154–1169 → ok |
| C-007 | fixed + verified | real | Missed. | Chapter 10 §10.3 listed fees, transport and lost earnings but not time and caregiving. | Added F-034 (G1, major). Chapter 10 §10.3 extended. | Line 1247 → ok |
| C-008 | fixed + verified | real | Missed; worse, my Chapter 11 draft copied the lecture's ACER as "net cost ÷ net health benefit". | Chapter 11 §11.4. | Added F-035 (D2, major). Chapter 11 now gives ACER = total cost ÷ total effect of one option. | Line 1324 → ok |
| C-009 | fixed + verified | real | Missed; my Chapter 11 draft also said "lower is better" for the cost-utility ratio. | Chapter 11 §11.4 and its takeaways. | Added F-036 (D2, major). Chapter 11 now teaches the incremental cost per QALY against a threshold, with the average ratio as descriptive. | Line 1360 → ok |
| C-010 | fixed + verified | real | Missed the condition on the CMA examples. | Chapter 11 and 12 drafts already required demonstrated equivalence; checked that both say it covers safety too. | Added F-037 (D2, major). Chapters 11 and 12 now say "equivalence in all relevant outcomes, including safety". | Lines 1336–1339 and 1424 → ok |
| C-011 | fixed + verified | real | Missed: I checked the arithmetic of Example 2 but not its basis. | Chapter 12's version of the example. | Added F-038 (D2, major). Chapter 12 states the cost as a 30-day supply per patient and the effect at three months. | Lines 1413–1417 → ok |
| C-012 | fixed + verified | real | I flagged the first function of advertising medicines but not the second. | Chapter 9 §9.4 already restricts advertising to approved use; it now cites the Egyptian guidance. | Added F-039 (D1, major). Chapter 9 cites the Egyptian Drug Authority's Prescription Medicine Promotion Guidelines (version 01), which were fetched and read: promotional material for prescription medicines is pre-cleared and directed to health professionals only. | Line 1002; the EDA PDF text → ok |
| C-013 | fixed + verified | real | Missed the conflict with lecture 1's definition. | Chapter 7 §7.1 defines price correctly; a sentence distinguishing cost was added. | Added F-040 (G1, major). | Line 553 → ok |
| C-014 | fixed + verified | real | Line spans were set to the first quoted line only. | F-001, F-004, F-005, F-024 corrected; the others quote a single line. | Spans widened; F-001 names line 252 for its second quote. | Each span re-read → ok |
| C-015 | fixed + verified | real | Terminology placed under a calculation pillar. | — | F-031 moved to G1. | — → ok |
| C-016 | fixed + verified | real | My fix hint repeated the lecture's equation of friction cost with replacement cost. | Chapter 10's activity table used the same label. | F-004's fix hint and Chapter 10's activity now record a replacement cost under the employer's perspective, with friction-cost valuation described separately. | — → ok |
| C-017 | fixed + verified | real | Missed the second QALY definition. | Chapter 11 already defines QALY as years × utility; checked it names the utility source. | Added F-041 (G1, major). | Line 1362 → ok |

## Rescoring

G1 4.5 → 4 (six more content errors in definitions and decision rules). D2 6 → 4.5 (F-005 moved in; ACER, cost-utility
rule, CMA condition and Example 2's basis added; F-029 and F-031 lighter or moved out). Total recomputed:
(4×20 + 3×20 + 2×10 + 2×10 + 3×20 + 4.5×20) / 10 = 33.0, matching `scorecard.json`. Counts from `findings.json`:
41 findings, 1 blocker, 27 major, 13 minor, matching `report.md`.

## What the review taught the rework

Five of the missed findings (C-005 to C-009) were errors I had carried from the lectures into my own chapter drafts.
The chapters are corrected in the rework, and the sibling column above names each place.
