# Review of the finished book, round 8 — marketing-book

reviewed_commit: 173e24d

Read-only review by claude-sonnet-5-5 as a fresh-context subagent (DEC-003); same request as `audit/codex-prompt.md`. The book was written by claude-opus-5-5. Saved verbatim from the verdict line on. Kept as a record: its findings were fixed in the next commit.

verdict: pass
open_blocker_major: 0
reviewer_model: claude-sonnet-5-5

| ID | severity | location | finding | why it matters | suggested fix |
|---|---|---|---|---|---|
| C-001 | minor | Glossary, "societal marketing orientation" | The entry ends "the only acceptable one for health services". Ch1 §1.6, the takeaway and Q9 say "most appropriate". Round 7 C-004 softened the same absolute wording in the chapters, but this glossary entry was missed. | The glossary contradicts the chapter text and overstates the point, since the book never argues the other orientations are unacceptable. | Change to "the most appropriate orientation for health services". |
| C-002 | minor | Ch5 §5.1 "No transfer of ownership" and E1 answer | The text says "The patient owns the report but not the scan." A scan is a performance, and patients normally receive the images and the report, so the sentence blurs the point being made. | A student could read it as a rule about who owns the images. The point is that the buyer receives a performance. | Reword to "The patient receives the performance and its report, not ownership of the service itself." |

Notes:
- All worked examples and numeric MCQs were recomputed, and every one reproduced.
  - Ch2: elasticity −0.4 (midpoint −0.474); revenue 120,000 to 135,000 EGP.
  - Ch3: cost per booking 40 and 80 EGP.
  - Ch5: customer value 25 and 30; Q8 = 20.
  - Ch7: 240, 300 and 20% margin; break-even 333.3 so 334; Q3 = 240; Q4 = 200; E1 = 150 and 100.
  - Ch10: pathway totals 1,600 and 1,800, incremental 200, hospital-only difference 600; Q6 = 600.
  - Ch11: QALYs 1.5 and 1.2; PV 8,626 (8,628 with the rounded factor), about 16% overstatement; Q2 = 2; Q6 = 3,000.
  - Ch12: micro-costing USD 437.35 with the stay at 80%; ICER −0.9; B/C 0.50, 0.43 and 0.23; net benefit −30 and −47; cost per case detected 3,333, 3,750, ICER 5,000 and sensitivity 3,000; cost per QALY 6,000 ÷ 0.20 = 30,000, with average ratios 2,500 and about 3,171.
- Decision rules are correct: dominance is read from the quadrant, incremental B/C has the ordering condition, and the baseline of no treatment is stated.
- No wrong MCQ key and no distractor that is also defensible was found.
- No endorsement of inducement or misleading promotion was found. The ethics boxes consistently reject referral payments, fear-based targeting and staff sales bonuses.
- Reference details (editions, DOIs, pages, years) match what is known of these works. The items rejected in rounds 6 and 7 were not re-raised: Decree 816 and the Rice & Unruh year.
- The "54.9% in 2022, down from 62.7% in 2018–2019" out-of-pocket figures could not be verified: the WHO PDF did not return readable text through the fetch tool. Earlier rounds recorded that 54.9% was read from the source, but the 62.7% figure has no recorded check, so the author may want to confirm it.
- Cross-references between chapters are consistent, and ledger items E-001 to E-018 are all reflected in the current text.
