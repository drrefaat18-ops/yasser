# Audit review, round 1, of commit f114486 — healthcare-entrepreneurship

reviewed_commit: f114486

Read-only full-book review by claude-sonnet-5-5 as a fresh-context subagent (DEC-002, in place of Codex), with the
request in `audit/codex-prompt.md`. The book was written by claude-opus-5-5. The reviewer fetched the cited sources
for the named Egyptian examples. Saved from the verdict line on; typography normalised.

verdict: fail
open_blocker_major: 3
reviewer_model: claude-sonnet-5-5

| ID | severity | location | finding | why it matters | suggested fix |
|---|---|---|---|---|---|
| C-001 | major | Ch. 4, Egyptian Entrepreneur: Cairo Scan, "it added laboratory testing in 2012 ... By that year it had 20 centres" | The Mediterrania profile (2023) says it "expanded into laboratory testing in 2012" and, separately, "With 20 centres, Cairo Scan has the largest branch network in Giza and Cairo". The 20-centre count is the 2023 figure, not 2012; the book back-dates a current figure. | The brief's strictest rule: every figure about a named company is dated and source-supported. | "As of the 2023 profile it had 20 centres"; drop "By that year". |
| C-002 | major | Ch. 12.2 Licensing; Ch. 12 Q1 and Q2 and rationales; Key Takeaways | Law 51 of 1981 is presented as the licensing law for laboratories and radiology clinics. Laboratories are licensed under the separate Law 367 of 1954, which the cited WHO annex lists as covering the organisation of diagnostic laboratories; the book mentions it only in passing. It then gives "a licensed doctor as director" as a general rule, and Q2 keys it with no laboratory-specific qualification. | The audience is laboratory students; the framing could mislead a founder planning a laboratory. | Say that laboratories are also governed by Law 367 of 1954, which sets who may direct or own one; scope Q1 and Q2 to clinics and centres, or rewrite them. |
| C-003 | major | Ch. 11, Egyptian Entrepreneur: Alfa Medical Group, "An established, profitable group sold a minority share, keeping control" | The source supports the 100-million-dollar minority investment, the date and the uses, but gives no profit or financial figures; "profitable" is not in the source, and "keeping control" is an inference. | An unsupported claim about a named company. | Remove "profitable"; say only "sold a minority stake". |
| C-004 | minor | Ch. 4.4, "Egyptian platforms such as Rology now offer this service across the region (Wamda, 2022b)" | Wamda says the funds will go towards expansion in the MEA region: a plan, not a present service. | Claim–support mismatch. | "plans to expand across the Middle East and Africa". |
| C-005 | minor | Ch. 9, Rology box, "connected existing scanners with radiologists who had spare reading time"; "did not need to buy scanners" | Not in the source; the book's own inference presented as story. | Unsupported detail about a named company. | Label as interpretation, or delete. |
| C-006 | minor | Ch. 12.6, Hend El Sherbini box, "became chief executive ... after Al Mokhtabar ... merged with Al Borg in 2012" | The IFC case study gives no date for her becoming CEO. | The book ties her appointment to the merger without support. | "is the chief executive"; drop the sequence. |
| C-007 | minor | Ch. 10, IDH box, spike centres "register patients, collect samples and send most of them to the hub" | The IFC text: spikes "complete some rapid, basic tests and send the rest back to the hub or spokes"; spokes are collection centres that process some routine tests on site. | Paraphrase drift on a named company's model. | Follow the IFC wording. |
| C-008 | minor | Ch. 6, Baheya box, "women with breast cancer were diagnosed late and could not afford treatment" | The source supports the family founding, the early-detection focus, the services and the soft opening; it does not say "diagnosed late", and it says treatment costs were covered by the charity Resala, which the book omits. | Unsupported causal claim about a named institution. | Mark the late-diagnosis point as the book's reading; state the funding source. |
| C-009 | minor | Ch. 14.1, "The Baheya hospital described in Chapter 6 had a soft opening" | Chapter 6 does not say so. | Internal consistency. | Add the fact to Chapter 6, or drop the cross-reference. |
| C-010 | minor | Ch. 13, EVA Pharma box, "the partnership expanded access to an essential medicine"; "the partner a global patent holder trusts" | Forbes supports an announced collaboration, not a result; it does not describe Lilly as a patent holder or EVA as trusted for production. Mildly promotional. | Unchecked and promotional claims are forbidden by the brief. | "announced a collaboration aimed at improving access"; remove the production inference. |
| C-011 | minor | Ch. 3.3, the five measure groups "(Isenberg, 2010)" | Isenberg describes ecosystem domains (policy, finance, culture, supports, human capital, markets); the five groups listed are not his (from the reviewer's knowledge of the article). | Citation does not support the claim as stated. | Cite Isenberg only for the ecosystem idea; present the groups as the book's own. |
| C-012 | minor | Ch. 12.2, "Price lists are regulated ... prices are not purely a marketing decision" | The WHO review says a licence needs "an approved, clear price list" but also that "the lack of pricing regulation allows each provider to set their own price list". | Overstated claim about Egyptian regulation from the book's own source. | Say a clear price list is a licensing condition, and the review found prices themselves largely unregulated. |
| C-013 | minor | Ch. 12.2, "The law was amended in 2026" (Law 7 of 2010) | True (Law No. 10 of 2026) but uncited. | Citation coverage. | Cite the amending law. |
| C-014 | minor | Ch. 11.4 runway example vs Table 11.1 and In Practice | Working capital is 72,000 EGP, yet in month 3 the venture has 96,000 EGP left with no further funding described. | The running example contradicts itself. | Use 72,000 EGP or less, or state an extra round. |
| C-015 | minor | Ch. 8.3 SOM vs Ch. 11.3 | Ch. 8's year-3 SOM (500 patients, about 167 visits a month) disagrees with Ch. 11's expected 220 visits a month at the end of year 1. | Undercuts the margin-of-safety lesson. | Align the SOM and the forecast. |
| C-016 | minor | Ch. 7.3 In Practice, "46 ideas ... discard 19 ... combine 12 ... into four concepts" | 46 − 19 = 27; merging 12 into 4 leaves 19, yet only four concepts are scored. | A printed count that does not reconcile. | Fix the counts or drop them. |
| C-017 | minor | Consolidated References, Hébert & Link (2009), "(Chapter 1.)" | Not cited anywhere; missing from Ch. 1's list. | Orphan reference with a false back-reference. | Remove it. |
| C-018 | minor | Ch. 10 Table 10.1 vs Q3 | The accredited partner laboratory appears under both Key resources and Key partnerships; Q3 keys it to Key resources. | Weak consistency in teaching the canvas. | Keep it only under Key partnerships; change Q3's stem. |
| C-019 | minor | Ch. 6 LO4 vs 6.5 and Q8 | LO4 lists market size, severity, technology gap and who pays; the matrix uses market and severity combined, technology gap, who pays and fit. | Objective does not match the content tested. | Align LO4 with the matrix. |

Scores
- G1 Content accuracy: 6 — several claim–support mismatches (C-001 to C-007, C-011, C-012) and one legal framing that could mislead (C-002); arithmetic sound, no calculation cap.
- G2 Pedagogical design and clarity: 8 — consistent objectives, boxes, worked steps and progression; minor slips C-015, C-016, C-019.
- G3 Assessment quality: 8 — every numeric MCQ and every key recomputed and correct, full rationales; slips C-002 (Q1, Q2 framing), C-018.
- G4 Sources and currency: 7 — metadata accurate where recognised; slips C-011, C-013, C-017.
- D1 Health-sector applicability and Egyptian examples: 6 — concepts applied well throughout; unsupported or mis-dated facts in named examples (C-001, C-003 to C-008, C-010) and an Egyptian law overstatement (C-002, C-012).
- D2 Business-tool and calculation accuracy: 8 — all printed numbers reproduce; slips are consistency only (C-014, C-015, C-016).

Notes (summary)
- Fetched and supported without discrepancy: The National (Shezlong); Ahram Online (Startup Charter); Wamda (Chefaa, Rology, Vezeeta); StartupScene (Chefaa); Daily News Egypt (Vezeeta); TechCrunch (Yodawy; the "insurers, hospitals and employers fund the service" sentence not specifically confirmed); Egyptian Streets (Magdi Yacoub); Chambers (data protection regulations); EGAC (El Shifa, Port Said); Rouse (Law 163 of 2023); Forbes Middle East (EVA Pharma, except C-010).
- IFC case study read from the PDF text: supports 1979 and the Moamena Kamel details, the 2012 merger, the hub, spoke and spike model, CAP accreditation, the quote, quality advisory services, EPiHC and the 2015 IPO, except C-006 and C-007.
- Mediterrania profile and WHO EMRO review read from the PDF text: C-001, C-002, C-012.
- Not fully verified: GAHAR handbook (exists), Law 206 of 2017, the official texts of Laws 51, 82 and 151; Chanda and Gupta (2025) exists. Danhof's "adoptive" label not verified.
- No blocker, ethics or MCQ-key defect found; all math checks spot-recomputed; errata claims E-003, E-005, E-008, E-013 and E-015 carried out.
