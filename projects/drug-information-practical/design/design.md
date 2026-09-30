# Design — Drug Information: A Practical Section Guide

Book: `drug-information-practical`. Inputs: approved intake (DEC-002), evaluation (30.0/100; 46 findings, 20 major).

## 1. What the new edition is

A short, easy guide for the Drug Information practical sections (Faculty of Pharmacy, Port Said University). One chapter per 45-minute section. Priority (user): an easy subject with valuable content. The students are near graduation and this is a secondary course, so each chapter teaches only what a working pharmacist uses: how to answer a drug question, which source to open, how to read a trial, and how to recognise, assess and report an ADR. No padding, no advanced statistics.

## 2. Chapters (chapter-plan.json)

| # | ID | Title | Words | Source |
|---|---|---|---|---|
| 1 | ch01 | The Drug Information Centre | 1400 | Sec 1 |
| 2 | ch02 | Drug Information Sources | 1500 | Sec 2 (primary literature added) |
| 3 | ch03 | Study Designs and Levels of Evidence | 1400 | added (Sec 3 missing) |
| 4 | ch04 | Randomisation and Blinding | 1300 | Sec 4 |
| 5 | ch05 | The Research Protocol, Hypothesis Testing and Ethics | 1500 | Sec 5 (first part) |
| 6 | ch06 | Critical Appraisal of a Clinical Trial | 1400 | Sec 5 (RCT evaluation) + added |
| 7 | ch07 | Adverse Drug Reactions | 1400 | Sec 6 |
| 8 | ch08 | ADR Causality and Management | 1400 | Sec 6 (management) + Sec 7 (causality) |
| 9 | ch09 | Pharmacovigilance, ADR Reporting and Medication Errors | 1500 | Sec 6 (PV, DTC) + Sec 7 (errors) + added reporting |
| 10 | ch10 | Applied Case: Answering a Real Drug Question | 1200 | Sec 8 rebuilt |

Total 14000 words (template 11,000-17,000), about 4-6 A4 pages per chapter. No parts. Nothing dropped: every source topic is kept; the physiotherapy detail of the Section 8 case (stretching grades, mobilisation) is replaced by the pharmacy questions it raises.

Chapter content in one line each:
1. What drug information is, the DIC, who asks, and the 7-step systematic approach to a request (flowchart + one worked request).
2. Tertiary, secondary, primary: what each is, pros/cons, named resources by question type (table), PubMed vs PMC, a search-order box.
3. (Added) Case report to meta-analysis: one table (design, question, strength, weakness, example) and the evidence pyramid.
4. Randomisation methods table (simple, block, stratified, unequal), allocation concealment, blinding levels; efficacy vs effectiveness.
5. Protocol contents, H0/H1, the 2x2 error table, alpha, power, p-value, 95% CI in plain words; IRB, informed consent, eligibility, outcomes, drop-outs.
6. (Added, uses the Sec 5 RCT slides) A 10-question appraisal checklist (title to conflicts of interest), CONSORT 2025, ITT, NNT; publication bias.
7. WHO definition, side effect vs ADR, burden, types A-F (one table), patient and drug risk factors.
8. Causality: WHO-UMC table and the Naranjo 10-question table with a worked score; severity vs seriousness; management steps starting with patient care.
9. Pharmacovigilance (WHO definition), pre- vs post-marketing, spontaneous reporting, how to report to the EDA (form fields, what to report), DTC role; medication errors: definition, types, causes, prevention, LASA and the regulator's role.
10. (Rebuilt) The frozen-shoulder patient becomes a pharmacy case: an NSAID question (choice, GI and CV risk), sources searched, one trial appraised, a suspected ADR scored with Naranjo and reported. Each step points back to its chapter.

## 3. Chapter pattern

Every chapter uses the same order (template.json):

1. `# Chapter N: Title`
2. `## In This Section` — 3-5 objectives `[LO1]…`, action verbs.
3. Core sections `## N.1 …` — short paragraphs, tables over prose (at least two tables per chapter), one flowchart where it helps.
4. `> **At the Pharmacy:**` — at least one real-practice example per chapter.
5. `> **Caution:**` and `> **Exam Tip:**` only where useful.
6. `## Key Takeaways` — 4-6 bullets.
7. `## Self-Assessment` — 5 single-best-answer MCQs (A-D), each tagged `[LOn]`, key balance 1-2 per letter; then `**Practice Case.**` (one short case).
8. `## Answers and Rationales` — one line per question; model answer for the case.
9. `## References` — Vancouver, 3-5 per chapter. Core: Malone et al. Drug Information: A Guide for Pharmacists 7th ed.; WHO and WHO-UMC guidance; ICH E6(R3) and E2A; CONSORT 2025 and SPIRIT 2025; EDA pharmacovigilance guidance.

Added content (chapters 3, 6, 9 reporting part, 10, and the primary-literature part of chapter 2) is marked in the front matter's How to Use note. Style: en-GB, short sentences (mean ≤16 words), no slide fragments.

## 4. Front matter (`chapters/00-front-matter.md`)

Title, the four co-authors in the approved order, `## How to Use This Book` (the chapter pattern, the boxes, which parts were added), educational-purpose note. Cover and title page from theme.json (both logos, Terracotta & Petrol palette).

## 5. Figures (`figures/figures.json`, kind `diagram.svg`, licence original)

| ID | Chapter | Shows |
|---|---|---|
| di-request-steps | ch01 | The 7-step systematic approach to a drug information request |
| evidence-pyramid | ch03 | Evidence pyramid from case reports to systematic reviews |
| adr-management | ch08 | ADR management: patient care, causality, severity/seriousness, report, prevent |

Three simple flowcharts only (low-effort book); everything else is tables.

## 6. Errors and gaps (evaluation findings)

Every finding maps to one chapter. G1 findings are seeded as errata (`errata-seed.md`).

| Finding | Chapter | Reason |
|---|---|---|
| F-001 | ch01 | minor: Drug information centre and requests. |
| F-002 | ch01 | minor: Drug information centre and requests. |
| F-003 | ch01 | minor: Drug information centre and requests. |
| F-004 | ch02 | major: Source tiers. |
| F-005 | ch04 | minor: Randomisation and blinding. |
| F-006 | ch04 | minor: Randomisation and blinding. |
| F-007 | ch05 | major: Protocol, hypothesis testing, ethics. |
| F-008 | ch05 | major: Protocol, hypothesis testing, ethics. |
| F-009 | ch05 | major: Protocol, hypothesis testing, ethics. |
| F-010 | ch05 | major: Protocol, hypothesis testing, ethics. |
| F-011 | ch05 | major: Protocol, hypothesis testing, ethics. |
| F-012 | ch05 | minor: Protocol, hypothesis testing, ethics. |
| F-013 | ch06 | minor: Appraisal of a trial report. |
| F-014 | ch07 | major: ADR definitions, types and risk factors. |
| F-015 | ch09 | minor: Pharmacovigilance, reporting and medication errors. |
| F-016 | ch08 | minor: Causality and ADR management. |
| F-017 | ch09 | minor: Pharmacovigilance, reporting and medication errors. |
| F-018 | ch09 | minor: Pharmacovigilance, reporting and medication errors. |
| F-019 | ch01 | major: Applies to every chapter; fixed by the chapter pattern (section 3). |
| F-020 | ch07 | minor: ADR definitions, types and risk factors. |
| F-021 | ch06 | minor: Appraisal of a trial report. |
| F-022 | ch09 | minor: Pharmacovigilance, reporting and medication errors. |
| F-023 | ch09 | minor: Pharmacovigilance, reporting and medication errors. |
| F-024 | ch01 | major: Applies to every chapter; fixed by the chapter pattern (section 3). |
| F-025 | ch01 | major: Applies to every chapter; fixed by the chapter pattern (section 3). |
| F-026 | ch02 | minor: Source tiers. |
| F-027 | ch01 | major: Drug information centre and requests. |
| F-028 | ch02 | major: Source tiers. |
| F-029 | ch02 | minor: Source tiers. |
| F-030 | ch02 | minor: Source tiers. |
| F-031 | ch10 | major: Section 8 rebuilt as a pharmacy application case. |
| F-032 | ch03 | major: Added chapter on study designs. |
| F-033 | ch04 | minor: Randomisation and blinding. |
| F-034 | ch04 | minor: Randomisation and blinding. |
| F-035 | ch05 | minor: Protocol, hypothesis testing, ethics. |
| F-036 | ch06 | minor: Appraisal of a trial report. |
| F-037 | ch07 | minor: ADR definitions, types and risk factors. |
| F-038 | ch08 | major: Causality and ADR management. |
| F-039 | ch09 | major: Pharmacovigilance, reporting and medication errors. |
| F-040 | ch07 | major: ADR definitions, types and risk factors. |
| F-041 | ch05 | minor: Protocol, hypothesis testing, ethics. |
| F-042 | ch02 | major: Source tiers. |
| F-043 | ch02 | minor: Source tiers. |
| F-044 | ch08 | major: Causality and ADR management. |
| F-045 | ch08 | major: Causality and ADR management. |
| F-046 | ch09 | minor: Pharmacovigilance, reporting and medication errors. |

## 7. Decisions for the user

1. Ten chapters as above, including the three added chapters and the rebuilt case (chapter 10).
2. Chapter 10 keeps the patient from Section 8 but changes the questions from physiotherapy to pharmacy.
