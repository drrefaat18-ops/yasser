# Fix Protocol — Codex review of the finished book

Every finding was confirmed against the chapter text before any edit; nothing was removed to make room.

## Round 1 — review of commit 41553df

Recorded verbatim in `audit/codex-audit-r1.md`: 11 findings, 5 major and 6 minor. Codex recomputed all 13 worked
examples and every numeric MCQ; apart from C-001 and C-006 the arithmetic reproduced.

| ID | status | real/rejected | root cause | siblings found | fix | verification → result |
|---|---|---|---|---|---|---|
| C-001 | fixed + verified | real | "Margin" used for a percentage of cost, which is a markup | Q3, takeaway, glossary | Markup throughout; markup and margin distinguished, with P = C ÷ (1 − g) for a target margin; margin on the example price stated (20%) | math checks added; checker pass → ok |
| C-002 | fixed + verified | real | COI listed as one of five evaluation methods although it compares no options | Table 11.1 caption, step 6, E3, glossary | Four comparative methods; COI a related descriptive study | re-read §11.4 → ok |
| C-003 | fixed + verified | real | The chapter was written from the 2020 law alone; the 2025 executive regulations were not checked | — | Decree No. 816 of 2025 cited (confirmed by search: issued 1 November 2025, one-year transition); licensing, electronic marketing and DPO questions added | reference added to ch03 and the consolidated list → ok |
| C-004 | fixed + verified | real | Service characteristics stated as absolutes, contradicting the batching example in ch05 | ch04 §4.3 and Q3, ch05 Table 5.1, glossary | Stated as tendencies; perishability defined as unused capacity; samples can be stored | re-read ch04, ch05 → ok |
| C-005 | fixed + verified | real | ICER per case detected compared with the cost of one complication | — | Decision needs an explicit willingness to pay per case detected, or modelling of downstream outcomes | re-read → ok |
| C-006 | fixed + verified | real | Rounded factor printed, unrounded factor used | — | Factor 1.1593 printed; the rounded-factor result shown | math check added → ok |
| C-007 | fixed + verified | real | UHIA wording implied no patient choice | — | Insurer contracts accredited providers; beneficiaries choose among them | → ok |
| C-008 | fixed + verified | real | Q3 stem gave equivalence in effect only | ch11 already correct | Stem states equivalence in all relevant outcomes | → ok |
| C-009 | fixed + verified | real | Incremental B/C rule without the ordering condition | — | Order by cost, remove dominated options, prefer net benefit when signs are awkward | → ok |
| C-010 | fixed + verified | real | Final user changed between zero- and one-level examples | — | Levels counted to the final user, with both hospital cases explained | → ok |
| C-011 | fixed + verified | real | Positive customer value stated as guaranteeing satisfaction | — | "More likely to be", with expectations as the basis of satisfaction | → ok |
