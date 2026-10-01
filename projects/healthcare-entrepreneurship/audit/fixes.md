# Fix Protocol — audit of healthcare-entrepreneurship

## Round 1 (review of f114486 by claude-sonnet-5-5 per DEC-002)

Review: `audit/review-r1.md` (verdict fail, 3 major, 16 minor). Protocol: confirm each finding against the cited
source, find the root cause, hunt siblings, fix, verify. Every finding was checked against the source text (the IFC
and Mediterrania PDFs and the WHO EMRO review read locally, the web articles as fetched) before any edit.

| ID | status | real/rejected | root cause | siblings found | fix | verification → result |
|---|---|---|---|---|---|---|
| C-001 | fixed + verified | real | A current figure (20 centres, 2023) was written into a sentence about 2012. | Checked every dated figure in the 14 Egyptian Entrepreneur boxes against its source; none other back-dated. | "The same profile reports 20 centres in 2023". | Profile text: "With 20 centres, Cairo Scan has the largest branch network" → ok |
| C-002 | fixed + verified | real | Law 51 of 1981 was treated as the whole licensing framework; the WHO annex also lists Law 367 of 1954 for laboratories. | The director rule in the bullet list, Key Takeaways, Q2 and its rationale. | §12.2 adds Law 367 of 1954 for laboratories and its role in who may practise in and direct a laboratory; the director bullet distinguishes centres from laboratories; Q2 is scoped to a specialised medical centre; the takeaway names both laws. Reference added. | WHO EMRO 2014 annex, laws list (367/1954) and descriptor → ok |
| C-003 | fixed + verified | real | "Profitable" and "keeping control" were inferences, not source facts. | Hunted interpretive adjectives in every box (C-005, C-008, C-010 are the same class). | "An established group sold a minority stake to an investor with a development mission." | Hospital Management (2021) text → ok |
| C-004 | fixed + verified | real | A stated plan was written as a present fact. | — | "offer this service and plan to expand it across the Middle East and Africa". | Wamda (2022b) → ok |
| C-005 | fixed + verified | real | Interpretation told as story. | — | The lesson is labelled as the book's reading; the "spare reading time" and "did not buy scanners" details are removed. | — → ok |
| C-006 | fixed + verified | real | A sequence of events was implied that the source does not give. | — | "is the chief executive ... the group formed in 2012 ... listed ... in 2015 under her leadership". | IFC (2022): CEO, 2012 merger, 2015 IPO in her words → ok |
| C-007 | fixed + verified | real | Paraphrase drift. | — | Spokes and spikes described in the IFC's terms. | IFC (2022) "hub, spoke, and spike" paragraph → ok |
| C-008 | fixed + verified | real | Causal claim not in the source; funding omitted. | C-009. | The box states the soft opening and the source's report that Resala covered treatment costs; the lesson is labelled as the book's reading. The source conflicts with Baheya's own website on the building, so the box says nothing about premises. | Egyptian Streets (2015) → ok |
| C-009 | fixed + verified | real | Cross-reference to a fact Chapter 6 did not state. | — | Chapter 6 now states the soft opening, so the Chapter 14 cross-reference holds. | Both chapters re-read → ok |
| C-010 | fixed + verified | real | An announced collaboration was described as an achieved result. | — | "announced a collaboration aimed at improving access"; the production inference is removed and the lesson labelled. | Forbes Middle East (2023) → ok |
| C-011 | fixed + verified | real | The book's own grouping was attributed to Isenberg. | Danhof sibling: "Danhof also called them adoptive" was also unverified; now "Some textbooks also call them adoptive entrepreneurs". | The grouping is presented as the book's own; Isenberg is cited for the ecosystem idea and his domains. | — → ok |
| C-012 | fixed + verified | real | "Regulated" overstated the source. | — | A clear price list is a licensing condition; the WHO review found prices largely unregulated. | WHO EMRO 2014: "The lack of pricing regulation allows each provider to set their own price list" → ok |
| C-013 | fixed + verified | real | Uncited fact. | — | "amended in 2026 by Law 10 of 2026", with a reference to the law. | Law of 2026 confirmed by the reviewer's search and by the Law Library of Congress listing found at rework → ok |
| C-014 | fixed + verified | real | The runway cash figure was chosen for clean arithmetic, not derived from Table 11.1. | — | The example now starts from the 72,000 EGP working capital: two months of 18,000 EGP losses leave 36,000 EGP; runway = 36,000 ÷ 12,000 = 3 months. | Math checks added (18,000; 36,000; 3) → ok |
| C-015 | fixed + verified | real | The two chapters of the running example used unrelated volume assumptions. | Ch. 8 figure, Ch. 8 Q8 rationale, Ch. 11 Q4 (it duplicated the new example). | Ch. 8 SOM set to 6% (600 patients, 960,000 EGP, 200 visits a month), and Ch. 11 uses that target: profit 6,000 EGP and margin of safety 20%. Q4 now uses 150 and 250 (40%). The figure and math checks were updated. | 47 math checks pass in the build → ok |
| C-016 | fixed + verified | real | Counts did not reconcile. | — | "group all 27 into four concepts". | 46 − 19 = 27 → ok |
| C-017 | fixed + verified | real | `references.md` was generated before Hébert and Link was removed from Chapter 1. | — | `references.md` regenerated from the chapters. | No orphan entries → ok |
| C-018 | fixed + verified | real | The partner laboratory was listed in two blocks. | Canvas figure checked: lists only collectors, cooled boxes and booking system as resources. | Removed from Key resources; Q3's stem now names collectors and cooled boxes. | — → ok |
| C-019 | fixed + verified | real | LO4 written before the matrix. | — | LO4 now lists the four criteria the matrix uses. | — → ok |

After the fixes: book check PASS (38,928 words), references verified (no disallowed or mismatched entry), build 139
pages with all PDF, figure and math gates green (47 math checks).

## Confirmation (review of 43a7c9c by claude-sonnet-5-5 per DEC-002)

| ID | status | real/rejected | root cause | fix |
|---|---|---|---|---|
| R-none | no action | — | The confirmation found no new problem; all of C-001 to C-019 resolved. | — |

The final review (`audit/codex-audit.md`, 43a7c9c) passed. Three optional minor points are recorded as audit findings
F-001 to F-003 and left open. The independent rescore is G1 8, G2 8, G3 8, G4 8, D1 8, D2 9, a total of 82.0 against the
source's 24.5.
