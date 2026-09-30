# Evaluation report — drug-information-practical

Source: `ingest/source.md` (text of `original/drug-info-sections-combined.pdf`: section decks 1, 2 (incomplete), 4, 5, 6, 7 and 8; Section 3 is missing).
Review kind: self (Claude, inline persona passes: subject-reviewer, drug-information-reviewer, instructional-designer). Codex review: `codex-review.md`; fixes in `fixes.md`. Scores use the rubric anchor bands.

## Score

Total **30.0 / 100**. No hard cap fires (no safety blocker).

| Pillar | Name | Weight | Score | Findings |
|---|---|---|---|---|
| G1 | Content accuracy | 20 | 3 | 20 |
| G2 | Pedagogical design and clarity | 20 | 3 | 5 |
| G3 | Assessment quality | 10 | 1 | 1 |
| G4 | Sources and currency | 10 | 2 | 2 |
| D1 | Drug information practice | 15 | 4 | 7 |
| D2 | Research methods | 15 | 4 | 5 |
| D3 | Pharmacovigilance | 10 | 3 | 6 |

Findings: 46 (0 blocker, 20 major, 26 minor).

## What the source does well

- Covers the core topics of a drug information course: the DIC, source tiers, randomisation, protocol and ethics, ADR types, causality and medication errors.
- The tertiary-source pros/cons and the evaluation questions for tertiary literature are clear and usable.
- The type I / type II error explanation uses a concrete 'current vs new drug' example that students can follow.

## Main problems

1. **Accuracy (G1, D3).** ADR severity confused with seriousness and no immediate patient care in ADR management; wrong definitions borrowed from other contexts (IRB from science fairs, informed consent from data protection), 'proving' H0, alpha called precision, and a confused ADR type C.
2. **Missing content (D1, D2, D3).** No systematic approach to a drug information request; primary literature, Section 3 (study designs), Type D ADRs, the Naranjo algorithm and ADR reporting are missing. Section 8 is a physiotherapy case with no drug-information content.
3. **Form (G2).** Slide fragments and garbled tables; no objectives or summaries.
4. **Assessment and sources (G3, G4).** No questions and no references.

## Blocker and major findings

| ID | Pillar | Lines | Claim |
|---|---|---|---|
| F-004 | G1 | 199-207 | The online-source examples are misclassified or out of date: MEDLINE is a secondary (indexing) database, TOXNET was retired in 2019, and the FDA site and DailyMed hold official labelling, not summaries. |
| F-007 | G1 | 363-369 | A trial never proves the null hypothesis; it tests H0 and either rejects it or fails to reject it. |
| F-008 | G1 | 371-381 | Alpha is the significance level (false-positive risk), not 'precision'; 1 - alpha is the confidence level. Alpha 5% and beta 20% are conventional choices set by the investigator, not fixed facts. |
| F-009 | G1 | 395-401 | The IRB definition is taken from a science-fair context ('fair, high school'); it does not describe the ethics committee of a clinical trial. |
| F-010 | G1 | 403-408 | Informed consent is defined as permission to process personal data (a data-protection definition), not the voluntary agreement of a trial participant after full disclosure. |
| F-011 | G1 | 467-474 | A secondary outcome is also pre-specified in the protocol; it is not any additional outcome that 'occurs' during the study. |
| F-014 | G1 | 625-669 | The ADR type names are inconsistent and Type C is wrong: B is called 'Nonpharmacologic' then 'Bizarre'; C is called 'Continuous' then 'Chemical', with paracetamol hepatotoxicity as the example. In the standard scheme C is Chronic (dose- and time-related), e.g. HPA-axis suppression with corticosteroids. |
| F-019 | G2 | 1-1062 | The source is slide fragments with no learning objectives, summaries or connected explanation; text is broken into bullets and garbled tables (e.g. lines 837-948). |
| F-024 | G3 | 1-1062 | There are no MCQs, cases, exercises or answers in any section. |
| F-025 | G4 | 1-1062 | The source cites no references; statistics (ADR burden, PMC size, FDA names) have no source. |
| F-027 | D1 | 80-124 | There is no systematic approach to answering a drug information request (the core practical skill): get requester details, background, the real question, categorise, search, answer, follow up, document. |
| F-028 | D1 | 209-246 | Section 2 stops after secondary sources; primary literature (definition, types, pros and cons) is missing. |
| F-031 | D1 | 951-1050 | Section 8 ('Trauma') is a physiotherapy case of non-traumatic frozen shoulder; it has no drug-information question, source search or ADR content. |
| F-032 | D2 | 246-252 | Section 3 is missing: there is no content on study designs or the hierarchy of evidence between sources (Section 2) and randomisation (Section 4). |
| F-038 | D3 | 775-780 | The Naranjo algorithm is named but not taught: its 10 questions, scores and categories are absent. |
| F-039 | D3 | 727-831 | The practical steps of reporting an ADR are missing: what to report, who reports, which form, and where (the EDA Egyptian Pharmaceutical Vigilance Center). |
| F-040 | G1 | 692-698 | Patient, prescriber and pharmacist are given as 'causes' of ADRs, mixing non-preventable ADR susceptibility with preventable medication errors. |
| F-042 | D1 | 209-238 | PubMed Central is placed under secondary resources; it is a free full-text archive, not an indexing or abstracting database. |
| F-044 | D3 | 757-773 | Severity (intensity) is confused with seriousness (regulatory outcome): 'severe' is defined as fatal or life-threatening and 'moderate' as needing hospitalisation. This can lead to wrong reporting decisions. |
| F-045 | D3 | 786-800 | ADR management jumps to education, formulary change and notification; immediate patient care (assess, stop or withhold the suspected drug, treat, monitor, escalate) is missing. |

## Direction for the design

Ten short chapters (45 minutes each), tables over prose, one 'At the Pharmacy' example per chapter, 5 MCQs and one case each. Added chapters: 3 (study designs), 6 (critical appraisal), 9 (ADR reporting and medication errors). Chapter 10 rebuilds Section 8 as a pharmacy application case.
