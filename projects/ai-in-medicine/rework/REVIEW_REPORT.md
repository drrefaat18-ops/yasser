# Review Report — Interprofessional Edition

**Book:** *Artificial Intelligence in Health Care: An Interprofessional Introduction* (rework of *Artificial Intelligence in Medicine*, Dr. Shereen Elsaid Elkholy)
**Date:** 2026-09-24
**Files:** `rework/` (source chapters), `AI_in_Health_Care_Interprofessional.md` (assembled book)
**Spec:** `docs/superpowers/specs/2026-09-24-interprofessional-rework-design.md`

> This re-score was done by the same author who wrote the rework, using the personas in `.agents/skills/` inline. It is a self-assessment. An independent reviewer should confirm it before publication.

## 1. Scorecard (EVALUATION_RUBRIC.md)

| Pillar | Weight | Original | Rework | Main reason |
|---|:---:|:---:|:---:|---|
| 1. Clinical & medical accuracy | 25% | 5.5 | 8.0 | All 34 known errors fixed or removed along with their topic; clinical depth set for years 1–2 |
| 2. AI & computational rigour | 20% | 5.0 | 8.5 | New Ch3 (splits, leakage, shortcuts, shift) and Ch4 (PPV, AUROC/AUPRC, calibration, Dice, evidence ladder) |
| 3. Pedagogical design | 20% | 5.0 | 8.5 | Objectives, running patients, 60-second medical boxes and four-lens boxes in every chapter; mean sentence length ≤ 22 words |
| 4. Question bank | 15% | 3.0 | 8.0 | 110 MCQs with A–D keys balanced (2–3 per letter); per-distractor rationales; 66% vignettes; no joke options |
| 5. Ethics, law & regulation | 10% | 5.0 | 8.5 | EU AI Act, MDR/IVDR, PCCP final guidance (2024), corrected learned-intermediary doctrine, Egypt boxes |
| 6. Literature & citations | 10% | 3.0 | 7.0 | 129 references, all cited in-text, all DOIs verified; recency target missed (see §4) |
| **Weighted total** | | **46** | **≈ 81** | |

## 2. What Changed

- **Audience:** a single shared course for years 1–2 in medicine, pharmacy, physical therapy and the health sciences. The original targeted residents.
- **Structure:** 11 chapters in 3 parts, plus front matter and a glossary. Two chapters are completely new: Medicines (Ch7) and AI in Motion (Ch8).
- **Length:** 26,642 words counted by the checker (excluding references), against a 26,500 target.
- **Retained author material, rewritten:** definitions (§1.1), risk and governance sections, CADe/CADx, autonomy levels, the Obermeyer case (now with the correct lesson), the teaching style of the original Chapter 6, and 9 original figures (titles cropped; one inaccurate footer removed).
- **Dropped as too specialised:** TAVR, IVUS/OCT, FFR-CT, EVAR, CT perfusion, CVS, bone marrow, AST kinetics.

## 3. Audit Results

| Check | Result |
|---|---|
| `check_book.py --all` (template, lenses ±20%, LOs, MCQ keys, citations, glossary, sentence length, budgets, ledger) | PASS |
| Checker self-test | 10/10 |
| DOI existence and title (`verify_refs.py`) | 111/111 OK; 18 laws, guidance documents and proceedings cited by URL |
| Year, volume and first page vs CrossRef | 111/111 consistent |
| Uncited numeric claims | None; the remaining numbers are worked examples or case facts |
| Re-imported known errors (grep on the assembled book) | None |
| Errata ledger | 34/34 closed (25 fixed, 9 removed together with their topic) |
| Figure links in the assembled book | 14/14 resolve |
| Glossary | 136 terms, no duplicates |

**Persona passes (inline):** statistician for Ch3, Ch4 and Ch9 arithmetic; research-synthesist for references; historian for Ch1 dates; anthropologist for the lens boxes and Local Context boxes; psychologist for tone, emotional arc and MCQ fairness; plus the master-instructional-design audit A–I.

## 4. Gaps and Deviations From the Spec

1. **Reference targets missed.** There are 129 references against a target of about 200. The median year is 2019 against a target of 2021 or later, and 17% date from 2023–2026 against a target of at least 25%. Density is 4.8 per 1,000 words, compared with 0.87 in the original. Reaching the target would mean adding recent primary studies where they change the teaching, not padding the lists.
2. **No student pilot.** Readability and the MCQs have not been tested with real year-1 students. Item difficulty and discrimination are therefore unknown.
3. **Bloom level mix** was designed in but has not been measured item by item.
4. **Figures.** Six new SVG figures were drawn by hand, and nine original figures were retained after cropping. Figures 6.1 (dermoscopy) and 9.1 are schematic. A designer should unify their style.
5. **References are per chapter.** There is no separate consolidated list.
6. **Not produced:** .docx/PDF typesetting, slides, an Arabic glossary (all out of scope).

## 5. Open Items for the User

- Confirm Egypt as the local context. The Local Context boxes are in Ch10 (Law 151/2020) and Ch11 (Egyptian Drug Authority, Law 151/2019).
- Confirm that Dr. Elkholy has approved the rework and how the new edition will credit her.
- The PubMed connector was unavailable, so references were verified through CrossRef.

## 6. Simplified Edition (2026-09-24)

At the user's request, the chapters were rewritten in plainer language for both students and teaching staff.

- **Length:** the book fell from 26,642 to 20,481 words. The checker's new budget is 17,000–21,000 words, with about 1,700 words per chapter.
- **Sentences:** the checker now fails any chapter whose prose averages more than 16 words per sentence, or where 5% or more of sentences exceed 28 words. The actual prose average is 9.5 words.
- **Removed:**
  - all Deeper Dive boxes and formulas;
  - Dice/IoU, k-space detail, tremor frequencies, reporting-guideline lists and secondary study statistics;
  - references that are no longer cited. The list went from 129 to 101, renumbered by first citation with `tools/renumber_refs.py`.
- **Kept:**
  - every chapter, running case, Learning Objectives box, Medical Background box, Four Lenses box, Myth vs Evidence box, Safety Alert box and Local Context box;
  - all 10 MCQs per chapter, with the same answer keys and shortened rationales.
- **Unchanged:** no new factual claims were added. The remaining references are a subset of the 111 already verified.
- **Outputs:** `AI_in_Health_Care_Interprofessional.docx` and `.pdf`, 95 pages, built by `tools/build_book.py`.
