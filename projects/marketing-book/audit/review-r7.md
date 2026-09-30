# Review of the finished book, round 7 — marketing-book

reviewed_commit: 83cd49a

Final read-only review by claude-sonnet-5-5 as a fresh-context subagent; same request as `audit/codex-prompt.md`. The book was written by claude-opus-5-5. Saved verbatim from the verdict line on. Kept as a record: its findings were fixed in the next commit.

verdict: pass
open_blocker_major: 0
reviewer_model: claude-sonnet-5-5

| ID | severity | location | finding | why it matters | suggested fix |
|---|---|---|---|---|---|
| C-001 | minor | Chapters 2, 7 and 10, reference lists and in-text "Rice & Unruh, 2016" | Rice and Unruh, *The Economics of Health Reconsidered*, 4th ed., Health Administration Press, was published in June 2015 according to publisher and retailer listings found by web search; the book prints 2016 everywhere | A wrong year in a cited reference, where the book's own audit trail treats reference accuracy as a pass criterion | Change to 2015 in the three chapter lists, the consolidated list and the in-text citations |
| C-002 | minor | Ch4 §4.3: "The result is the **7 Ps of services marketing** (Wirtz & Lovelock, 2021)" | The seven-P services mix (adding people, process and physical evidence) comes from Booms and Bitner (1981); Wirtz and Lovelock's own integrated framework has eight elements. This is from recall of the 9th edition and could not be checked against the book; the search confirmed only the Booms and Bitner origin | The citation may not support the claim, and the original source is missing from the references | Attribute the seven Ps to Booms & Bitner (1981) and cite Wirtz & Lovelock only for service characteristics; if Booms & Bitner cannot be added with a DOI, write "the widely taught seven Ps" and keep Wirtz & Lovelock for the service characteristics |
| C-003 | minor | Ch10 §10.7 worked example and Table 10.2: one month of lost production at full wage by the human capital approach, plus a separate "replacement cost to the employer" row | The scenario has the employer bring in a replacement for the month. Valuing the whole month as lost output and also listing the recruiting and training of a replacement describe the same absence twice: if the replacement restores output, the month is not fully lost. The box calls the replacement cost "separate" but does not warn that the two cannot simply be summed | A student who sums the rows double-counts, close to the double-counting rule the chapter teaches elsewhere | Add one sentence saying the replacement cost is listed to show where it belongs and is not added to a full month of lost production unless no output is restored, or move the row to a note |
| C-004 | minor | Ch1 §1.6 "For health services, only the last is acceptable"; Q9 and its answer ("Only the societal marketing orientation…"); Key Takeaways | An absolute normative claim is stated as settled and, through the surrounding paragraph, attributed to Kotler and Keller, who describe the orientations but do not say only one is acceptable for health services. A marketing orientation that respects the ethics and legal limits taught in this book is defensible, and the other chapters are careful to state tendencies, not absolutes | The claim overstates its source and invites a defensible alternative answer in class | Write "the societal orientation is the most appropriate" or "best fits"; reword Q9 to "most appropriate" and keep the key |
| C-005 | minor | Ch2 §2.5: "A general 'wellness' panel loses many buyers when its price rises (Rice & Unruh, 2016)" | Rice and Unruh is a general health-economics text: it discusses the price responsiveness of demand for care, but not the behaviour of wellness panels at laboratories. It could not be confirmed that it supports this specific claim | A specific claim is pinned to a source that probably does not make it | Drop the citation and present the sentence as an illustration ("demand for elective, self-paid services tends to be more elastic"), or cite an elasticity source that covers elective services |

## Notes

- **Arithmetic.** Every worked example, numeric MCQ and numeric essay answer was recomputed, and all reproduce.
  - Ch2: elasticity −0.4, midpoint −0.47; Q8 0.5.
  - Ch3: cost per booking 40 and 80 EGP.
  - Ch5: customer value 25 and 30; Q8 20.
  - Ch7: markup 300 EGP with a 20% margin; break-even 333.3, so 334; Q3 240; Q4 200; E1 150 and 100.
  - Ch10: totals 1,600 and 1,800, incremental cost 200; Q6 600.
  - Ch11: QALYs 1.5, 1.2, 2 and 2.1; discount factor 1.1593, 8,626 EGP and about 16%; Q6 ICER 3,000.
  - Ch12: micro-costing USD 437.35 with the stay at 80%; CERs 0.72 and 1.8; ICER −0.9; CBA 0.50, 0.43 and 0.23, net benefits −30 and −47; screening CERs 3,333 and 3,750, ICER 5,000 (3,000 in the sensitivity case); imaging ICER 30,000, average ratios 2,500 and about 3,171.
  - The dominance, B/C, ICER and quadrant decision rules are all stated correctly.
- **MCQ keys.** No wrong key and no second defensible option. In Ch2 Q10 the stem ("does not reliably diagnose") would fit the book's Principle 1 better than Principle 4, but Principle 1 is not offered, so the key stands.
- **Ethics.** No endorsement of inducement or misleading promotion; the Ethics Check boxes, pricing limits and promotion principles are consistent.
- **Earlier rejection.** The rejection of round 6 C-001 is correct: Decree No. 816 of 2025 is rightly described as a Ministry of Communications and IT decree. Its content was not re-verified.
- **Not verified, so not in the table.**
  - Ch7 §7.6, the "seven stages" of price setting attributed to Nagle & Müller. The sequence may be closer to Kotler and Keller's pricing steps, but this could not be checked.
  - Ch1 §1.2 and ledger E-013 call the 1985 AMA wording the "predecessor" of the current definition. The body text says only that older books still quote it, which is accurate. If "predecessor" is meant literally, the intervening 2004 AMA definition makes it inexact.
  - Ch2 Key Takeaways: "A price change that leaves revenue unchanged can still reduce access". The worked example and E2 say revenue rises or does not fall; consider "does not reduce revenue".
  - Ch12 §12.1 lists three uses of economic evaluation and Ch10 §10.1 lists four. The lists are compatible, so this is presentation only.
