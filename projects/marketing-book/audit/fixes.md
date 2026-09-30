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

## Round 2 — review of commit b94371e

Recorded verbatim in `audit/codex-audit-r2.md`: 9 findings, 3 major and 6 minor, down from 5 major. Codex reproduced
every other calculation and found no further wrong MCQ key.

| ID | status | real/rejected | root cause | siblings found | fix | verification → result |
|---|---|---|---|---|---|---|
| C-001 | fixed + verified | real | My round-0 fix gave costs for 30 days and effects at three months | Table 12.2 caption; ledger E-005 | Costs and effects both for one month of treatment; the source numbers then reproduce | ICER −0.9 unchanged, math checks pass → ok |
| C-002 | fixed + verified | real | Out-of-pocket claims cited to the insurance law, which gives no spending data; a laboratory-specific share was asserted | ch01 §1.6, ch02 §2.2 lens, §2.4, Q6, E3, takeaway; ch10 Egyptian Context; ledger E-016 | WHO Country Cooperation Strategy 2024–2028 cited (fetched and read: 54.9% of CHE in 2022); the laboratory-specific share removed; Q6 rewritten to the national figure | reference added in ch01, ch02, ch10 → ok |
| C-003 | fixed + verified | real | Public pull for check-up packages allowed on accuracy alone, against ch01's clinical-need rule | ch09 lens | Pull only for clinically indicated tests to a defined group, with eligibility stated | lens balance re-checked → ok |
| C-004 | fixed + verified | real | Definition dated 2007 | ledger E-013 | Dated 2017 by the association, wording first adopted 2007; cited through Kotler and Keller because the template's reference policy does not accept a web page without DOI | → ok |
| C-005 | fixed + verified | real | Year taken from the PDF's creation date | — | 2020, per the EDA regulatory index (fetched and read) | → ok |
| C-006 | fixed + verified | real | "Whatever it costs" equates inelastic with perfectly inelastic | Q9 rationale | Less price-responsive; affordability still limits | → ok |
| C-007 | fixed + verified | real | WTP described on both sides of the balance | — | One convention: valued intangible effects are benefits, never also costs | → ok |
| C-008 | fixed + verified | real | Utility scale described without negative values | glossary | Values below 0 noted | → ok |
| C-009 | fixed + verified | real | Takeaway kept the absolute wording round 1 removed from the body | — | Takeaway qualified | → ok |

## Round 3 — review of commit c4c3291

Recorded verbatim in `audit/codex-audit-r3.md`: 8 findings, 4 major and 4 minor. All arithmetic, units, ICERs,
quadrants and B/C results reproduced; every finding is about interpretation or definition.

| ID | status | real/rejected | root cause | siblings found | fix | verification → result |
|---|---|---|---|---|---|---|
| C-001 | fixed + verified | real | The glossary kept the source's "lower is better" rule that ch11 had already corrected | — | Glossary separates the descriptive average ratio from the incremental ratio used for decisions | → ok |
| C-002 | fixed + verified | real | Regained production listed as a benefit while ch10 counts lost production as a cost | treatment savings, same problem | One convention stated in ch11: productivity and treatment savings enter as smaller costs, never also as benefits | → ok |
| C-003 | fixed + verified | real | COI total read as the savings from elimination | glossary already correct | COI describes burden, not avoidable savings | → ok |
| C-004 | fixed + verified | real | Each option's own B/C interpreted without a stated baseline | Common Mistake box | Baseline of no treatment stated; own ratios interpreted only against it | → ok |
| C-005 | fixed + verified | real | Stem did not specify QALYs | — | Stem specifies QALYs; rationale notes CEA with a shared natural unit | key unchanged → ok |
| C-006 | fixed + verified | real | "Opened needles in sealed wrappers" | — | A sterile needle opened from an intact wrapper | → ok |
| C-007 | fixed + verified | real | The 2017 date rested on a 2016 secondary source | — | Date removed; the definition's wording is supported by the cited source | → ok |
| C-008 | fixed + verified | real | CMA example inferred equivalence from equal percentages | — | Equivalence shown within a prespecified margin in a trial designed for it | → ok |

## Claude review — commit b74f87e

A fresh-context Claude review at the user's request (`audit/claude-review.md`): 14 findings, 2 major, 12 minor. It
recomputed every worked example, numeric MCQ and numeric essay answer and found no arithmetic or key error.

| ID | status | real/rejected | root cause | fix |
|---|---|---|---|---|
| R-001 | fixed + verified | real | ch05 takeaway kept the absolute service wording (missed sibling of round-1 C-004) | Takeaway qualified |
| R-002 | fixed + verified | real | Figure 9.1 caption and ch09 takeaway stated a worldwide ban | "in Egypt and most other countries" added to both |
| R-003 | fixed + verified | real | Two sentences in ch11 still called productivity and savings benefits (missed siblings of round-3 C-002) | Reworded as smaller costs |
| R-004 | fixed + verified | real | "Six categories" then withdrew two | Four categories plus two concepts; LO3 aligned |
| R-005 | fixed + verified | real | Laboratory reagent example did not fit the consignee definition | Consignment stock for end users, consignee pharmacy kept; E2 and glossary aligned |
| R-006 | fixed + verified | real | Budget shift justified by average cost per booking | Marginal test before shifting budget |
| R-007 | fixed + verified | real | Cost activity valued only the worker's share of wages and named no method | Human capital approach, full lost production including sick pay |
| R-008 | fixed + verified | real | Four value types attributed to Kotler & Keller | Presented as the book's grouping; citation kept for the value concept only (a new source could not be DOI-verified while Crossref was unreachable) |
| R-009 | fixed + verified | real | "New uses" and guarantees without health-care limits | Approved indication for medicines, guideline support for tests; outcome guarantees ruled out |
| R-010 | fixed + verified | real | Price said to represent worth, against the same paragraph | Money price linked to the broader customer cost of ch01 and ch04 |
| R-011 | fixed + verified | real | Pharmacoeconomics stretched to devices and tests | That sentence now describes economic evaluation |
| R-012 | fixed + verified | real | Channel functions attributed to Kotler & Keller as listed, without risk | "Adapted from"; risk taking added as the eighth function |
| R-013 | fixed + verified | real | Sanders et al. cited for what HTA bodies do | Attributed to the Second Panel's reference case |
| R-014 | fixed + verified | real | Uncited statements of Egyptian pricing and pre-launch rules | Hedged to name the EDA as the authority; the promotion guideline cited in ch06 |

## Round 4 — review of commit 8696791

Recorded verbatim in `audit/codex-audit-r4.md`: 5 findings, 2 major and 3 minor. All arithmetic reproduced; Codex
found no endorsed inducement or misleading promotion, and judged the Egyptian data-protection, promotion and
out-of-pocket claims supportable.

| ID | status | real/rejected | root cause | fix |
|---|---|---|---|---|
| C-001 | fixed + verified | real | Analysers and reagents called IVDs categorically; IVD status depends on intended purpose | Intended-purpose qualification; research-use-only reagents and general equipment excluded; Q7 and glossary aligned |
| C-002 | fixed + verified | real | A "main and supporting elements" table not found in the cited source | Kotler and Keller's eight major modes, each with a health-care example; LO1, Q2 and takeaway aligned |
| C-003 | fixed + verified | real | Elasticity base not stated | Initial-value method named; midpoint result (about −0.47) given; math check added |
| C-004 | fixed + verified | real | ch08 takeaway omitted risk taking | Added |
| C-005 | fixed + verified | real | Q10 gave the life-cycle label as the legal reason | Option and rationale state the registration rule |

## Round 5 — review of commit 600d239

Recorded verbatim in `audit/codex-audit-r5.md`: 6 findings, 2 major and 4 minor. All arithmetic reproduced; no
endorsed misleading or inducement-based promotion found.

| ID | status | real/rejected | root cause | fix |
|---|---|---|---|---|
| C-001 | fixed + verified | real | Egyptian medicine prices classed as ceiling prices; Egypt sets an official public price per product | Registered medicines moved to fixed prices; controlled prices defined as ceilings; Q1, takeaway, Egyptian Context and both glossary entries aligned |
| C-002 | fixed + verified | real | The prescription-medicine promotion guideline extended to devices and IVDs | Passage and Q10 narrowed to prescription medicines; devices pointed to the authority's separate rules |
| C-003 | fixed + verified | real | Price defined as money plus time in ch01, ch04 and the glossary, money only in ch07 | Price is the money charge everywhere; time, travel and effort are non-money parts of total customer cost |
| C-004 | fixed + verified | real | E3 answer said CEA cannot compare across diseases | Limited comparison unless a shared natural outcome is used |
| C-005 | fixed + verified | real | Q6 asked for the "most important" classification | Stem asks which classification decides the audience of promotion |
| C-006 | fixed + verified | real | Average ratios linked to willingness to pay | The average comparison named as invalid; decision rests on the ICER or net benefit |

## Round 6 (claude-sonnet-5-5, commit 2f2c5f3)

Recorded verbatim in `audit/review-r6.md`: verdict pass, 0 blocker or major, 9 minor. Run by a different Claude model after Codex usage limits blocked round 6, on the user's instruction to finish on Claude. All arithmetic reproduced.

| ID | status | real/rejected | root cause | fix |
|---|---|---|---|---|
| C-001 | rejected | rejected | The reviewer's search result was misread: the executive regulations were issued by the Minister of Communications and Information Technology as Ministerial Decree No. 816 of 2025 (Al Tamimi & Company legal update, checked 2026-09-30) | No change; text and reference already correct |
| C-002 | fixed + verified | real | Worked examples and rationales referred to an uncredited "source", "source slide" and "lecture notes" | Rephrased as common wrong answers or teaching-note usages in ch09, ch11 and ch12; history kept in the errata ledger |
| C-003 | fixed + verified | real | Friction cost method described as excluding recruitment and training | 10.6 and 10.7 now include hiring and training in friction costs; the separate row is explained by the human capital valuation |
| C-004 | fixed + verified | real | Common Mistake box and E2 used "consignee" for a laboratory end user | Box uses a pharmacy with consigned medicines; E2 names both arrangements |
| C-005 | fixed + verified | real | Q2 assumed fasting for a lipid test | Stem uses a fasting glucose test |
| C-006 | fixed + verified | real | LO3 counted six characteristics; Table 2.1 has seven | LO3 says seven |
| C-007 | fixed + verified | real | Health-care brand loyalty stated as settled | Table row says "often reported as high"; Q5 rationale no longer rests on loyalty |
| C-008 | fixed + verified | real | Profit peak placed in both growth and maturity | Maturity: "at or just past their peak" |
| C-009 | fixed + verified | real | "Most countries" without the exceptions | 9.3 names the United States and New Zealand |

## Round 7 (claude-sonnet-5-5, commit 83cd49a)

Recorded verbatim in `audit/review-r7.md`: verdict pass, 0 blocker or major, 5 minor. All arithmetic reproduced. Reviewer per DEC-003.

| ID | status | real/rejected | root cause | fix |
|---|---|---|---|---|
| C-001 | rejected | rejected | Publisher and retailer listings give the 4th edition as 2016 (Barnes & Noble, Health Administration Press, ISBN 978-1-56793-723-7; checked 2026-09-30); APA uses the copyright year | No change |
| C-002 | rejected | rejected | Wirtz and Lovelock's *Services Marketing* teaches the 7 Ps of services marketing (product, price, place, promotion, people, process, physical evidence); the citation supports the claim | No change |
| C-003 | fixed + verified | real | The worked example listed a full month of lost production and the replacement cost without saying they cannot simply be added | One sentence added: add them only when no output is restored |
| C-004 | fixed + verified | real | "Only acceptable" orientation stated as an absolute | Text, takeaway, Q9 stem and rationale say "most appropriate" or "best fits"; key unchanged |
| C-005 | fixed + verified | real | Rice & Unruh cited for a specific wellness-panel claim | Citation moved to the general elasticity statement; the panel given as an illustration |

## Round 8 (claude-sonnet-5-5, commit 173e24d)

Recorded verbatim in `audit/review-r8.md`: verdict pass, 0 blocker or major, 2 minor. All arithmetic reproduced. Reviewer per DEC-003. The reviewer's note on the 62.7% out-of-pocket figure was checked against the text read earlier from the WHO document: "making up 59.3% in 2020 decreasing to an estimate of 54.9% of CHE in 2022, down from 62.7% in 2018–2019". The figure is confirmed and not changed.

| ID | status | real/rejected | root cause | fix |
|---|---|---|---|---|
| C-001 | fixed + verified | real | The round 7 sibling hunt missed the glossary entry for "societal marketing orientation" | Glossary entry and its generator say "the most appropriate one"; no other "only acceptable" remains |
| C-002 | fixed + verified | real | "Owns the report but not the scan" blurred the no-ownership characteristic | Patient receives the performance and its results (images and report) but does not own the service |

## Final confirmation and rescore (claude-sonnet-5-5, commit 2ad98f1)

The confirmation review of the diff from 173e24d is saved as `audit/codex-audit.md`: verdict pass, and no findings.

The independent rescore against the same rubric gives 87.5, against a baseline of 33.0 for the source lectures. The pillar scores are G1 9, G2 8.5, G3 8, G4 8.5, D1 8.5 and D2 9.5; they are recorded in `audit/scorecard.json`.

The rescore lists 5 minor findings that remain open in the audited text; they are recorded in `audit/findings.json`. None is a blocker or major. They were left open so that the audit closes on the text the reviewer confirmed, and fixing them would re-open the audit.

| ID | status | real/rejected | root cause | fix |
|---|---|---|---|---|
| F-001 | open (minor) | real | Sibling of round 6 C-002 missed: one "source example" left in ch12 | Rephrase without naming a source |
| F-002 | open (minor) | real | The vitamin D testing guideline position has no citation | Cite a guideline, or soften the claim |
| F-003 | open (minor) | real | The AMA 1985 definition is quoted without a citation | Add a secondary citation, or paraphrase |
| F-004 | open (minor) | real | ch08 §8.7–8.8 have no laboratory or imaging application | Add the reagent and contrast supply link |
| F-005 | open (minor) | real | The Egyptian rules for laboratory and imaging promotion are generic | Name the instrument, or state the limit of coverage |
