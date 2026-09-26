# Design Spec — Interprofessional Rework of "Artificial Intelligence in Medicine"

**Date:** 2026-09-24
**Source manuscript:** `AI_in_Medicine- Assistant Prof Dr Shereen Elkholy.md` (26,394 words, 7 chapters, 135 MCQs, 23 refs, 24 figures)
**Inputs:** `VERDICT.md`, `SESSION_SUMMARY.md` (score 46/100), `EVALUATION_RUBRIC.md`, `EVALUATION_GUIDE.md`
**Approach:** A — organised by AI concept + running patient cases (approved in chat 2026-09-24)

---

## 1. Agreed Brief

| Decision | Value | Source |
|---|---|---|
| Use | One shared interprofessional course, same content for all faculties | User |
| Audiences | Medicine, Pharmacy, Physical Therapy, Health Sciences (lab, imaging technology, nutrition, public health) | User |
| Level | Years 1–2, pre-clinical | User |
| Language | English throughout | User |
| Length | Same as original: ~26,500 words total | User |
| Regulatory frame | International (WHO, FDA, EU) + one short "Local Context" box per regulation chapter for Egypt | **Assumption** — user did not specify region |
| Authorship | Dr. Shereen Elkholy remains author | **Assumption** — see §11 |

**Core shift:** the original is "a physician learning AI". The rework is "any health-profession student learning AI". AI literacy is the content; medicine is the context. A year-1 pharmacy or PT student must be able to read every chapter without prior clinical training.

**Success criteria:**
1. Re-score against `EVALUATION_RUBRIC.md` ≥ 75/100 (from 46).
2. Every chapter usable by all four professions — no chapter whose examples serve only physicians.
3. All errors listed in `SESSION_SUMMARY.md` §3 are either fixed or removed with the content they lived in (tracked in errata ledger).
4. MCQ answer key balanced (each letter 20–30% per chapter); zero joke distractors.
5. Every performance number, trial, dataset and regulation cited in-text and verifiable.

---

## 2. Book Architecture

Working title: **Artificial Intelligence in Health Care: An Interprofessional Introduction**

| # | Chapter | Words (prose + MCQ) | Main source material |
|---|---|:---:|---|
| 0 | Front matter: How to use this book (pathways per profession), meet the three patients | 500 | New |
| **Part I — Foundations** | | | |
| 1 | What AI Is — and Isn't (definitions, brief history, rules vs learning) | 2,000 | Ch1 §1.1, §1.3 (condensed) |
| 2 | Health Data: EHR, images, signals, text, omics | 2,000 | New; fragments of Ch2 overview, Ch3 §3.5 |
| 3 | How Models Learn — and How They Fail (splits, overfitting, leakage, shortcut learning, distribution shift, class imbalance) | 2,400 | New; Ch2 §2.4.1, §2.4.3 (corrected) |
| 4 | Reading an AI Performance Claim (confusion matrix, sens/spec, PPV/NPV + prevalence, ROC/AUROC vs AUPRC, calibration, Dice/IoU, internal vs external validation, evidence ladder, TRIPOD+AI / CONSORT-AI) | 2,700 | New (VERDICT priority #5) |
| 5 | Generative AI & Large Language Models (tokens, next-token prediction, hallucination, RAG, ambient scribes, patient chatbots, safe prompting, PHI, academic integrity) | 2,400 | New; Ch1 §1.3.2, Ch7 §7.6.1 |
| **Part II — AI Across the Care Pathway** | | | |
| 6 | Seeing Disease: Imaging, Laboratory & Pathology (CXR triage, CADe/CADx/CADt, mammography, fast MRI concept, retina, dermatology, WSI, lab automation, HIL, delta checks) | 2,800 | Ch2 (heavily condensed), Ch3 (completed + condensed), Ch6 §6.1, §6.3.2 |
| 7 | Medicines: Discovery, Dosing & Safety (AlphaFold, de novo design, pharmacovigilance NLP, drug-interaction alerts & alert fatigue, model-informed precision dosing, pharmacogenomics, automated dispensing) | 2,400 | New; Ch1 §1.2.3 |
| 8 | AI in Motion: Robotics, Rehabilitation & Wearables (surgical robots & autonomy levels, pose estimation, gait analysis, wearables & IMUs, tele-rehab, exoskeletons, skill metrics) | 2,400 | Ch4 §4.1, §4.3.1, §4.6 (condensed); rest new |
| 9 | Monitoring, Prediction & Population Health (early-warning scores, sepsis/AKI prediction with alarm burden, AI-ECG, closed-loop insulin, public-health surveillance) | 2,300 | Ch5 §5.5, §5.6; Ch6 §6.3.1, §6.4; new |
| **Part III — Responsible AI** | | | |
| 10 | Bias, Fairness & Privacy (sources of bias, Obermeyer case, Fitzpatrick, de-identification, HIPAA/GDPR, consent) | 2,200 | Ch7 §7.2, §7.4 (corrected §7.4.3) |
| 11 | Regulation, Liability & the Human in the Loop (SaMD, IMDRF risk, FDA 510(k)/De Novo/PMA, PCCP final guidance Dec 2024, EU AI Act 2024/1689, MDR/IVDR, WHO LMM guidance; liability & learned-intermediary (corrected); automation bias, de-skilling, XAI limits; future horizons) | 2,400 | Ch7 §7.1, §7.3, §7.5, §7.6 |
| — | Glossary (~150 terms), consolidated references, answer keys | outside budget | New |
| | **Total** | **~26,500** | |

**Dropped from original** (too specialised for year 1–2; errors disappear with them): TAVR/LAA planning, IVUS/OCT, FFR-CT, EVAR/endoleak, CT-perfusion detail, CVS/lap-chole segmentation, AR neurosurgery detail, bone-marrow/M:E ratios, AST kinetics, Gleason detail. Any retained one-line mention must be correct (e.g., stroke core = rCBF < 30%).

---

## 3. Chapter Template (every chapter)

1. **Opening case** (~150 words) — one of the three running patients, ends on a question the chapter answers.
2. **Learning objectives** — 3–5, observable verbs (explain, distinguish, calculate, interpret, evaluate). No "understand".
3. **Medical background in 60 seconds** — box defining any clinical concept a year-1 student lacks (e.g., "What is a mammogram?"). Mandatory wherever a clinical term appears.
4. **Core sections** — max 3 heading levels; mean sentence ≤ 22 words; every technical term defined on first use and in glossary.
5. **Through Four Lenses** — box with one concrete paragraph each: Medicine · Pharmacy · Physical Therapy · Health Sciences. Equal length (±20%).
6. **Myth vs Evidence** — one common misconception, corrected with a citation.
7. **Safety Alert** — one patient-safety point.
8. **Deeper Dive** (optional box) — maths or technical detail; skippable without losing the thread.
9. **Key takeaways** — 5 bullets.
10. **Self-assessment** — 10 MCQs + 1 short-answer case question; answers and rationales at chapter end.
11. **References** — numbered Vancouver, cited in-text `[n]`.

Callout names from original ("Clinical Pearl", "Radiology Alert") are replaced by the neutral set above.

---

## 4. Running Patients (narratologist + anthropologist personas)

Three patients recur across chapters so students see AI as a pathway, not a list of tools. Names and settings are regionally neutral; ages, genders and skin tones differ deliberately.

| Patient | Profile | Chapters |
|---|---|---|
| **Mrs. Amal Hassan**, 61 | Type 2 diabetes, hypertension, 7 medications | 2 (her EHR as data), 6 (retinal screening), 7 (interaction alert, dosing), 9 (deterioration score), 11 (who is liable) |
| **Mr. Karim Adel**, 34 | Construction worker, knee ligament injury | 3 (a model trained on athletes fails him), 6 (knee MRI AI), 7 (analgesic choice), 8 (pose-estimation rehab, wearable), 10 (wearable data privacy) |
| **Ms. Lina Osei**, 20 | University student, dark skin, changing mole, anxious | 1 (asks a chatbot first), 4 (what "95% accurate" means for her), 5 (LLM symptom advice), 6 (dermatology AI), 10 (skin-tone bias) |

Each opening case is written so the professional actor rotates: physician, pharmacist, physiotherapist, lab/imaging technologist, public-health officer.

---

## 5. Instructional Design Rules (master-instructional-design lenses)

**Performance lens.** Target behaviour: a graduate from any of the four professions can (a) judge whether an AI claim is trustworthy, (b) use an AI tool safely inside their scope, (c) recognise when to override or escalate. Every LO traces to one of these three.

**Cognitive load.** Year 1–2 students: open with case, not formulas. One new AI concept per section. Maths lives in Deeper Dive boxes. Ch3 and Ch4 are the conceptual spine; Part II chapters reuse their vocabulary instead of introducing new metrics.

**Emotional design.** Anticipated feelings: maths/CS anxiety; non-medicine students feeling like guests; fear of being replaced. Mitigations: plain-language first, worked examples before practice; lens boxes of equal weight; "clinician/health professional" as default noun, never "physician" unless specific; an explicit section in Ch11 on how roles change, not disappear.

**Inclusive design.** Patients and professionals varied by gender, age, skin tone, occupation. Examples not centred on US hospitals only. No idioms that assume native English.

**Assessment.** Bloom mix per chapter: ≤ 40% remember/understand; ≥ 30% apply/analyse (calculations, case interpretation); ≥ 1 evaluate item.

---

## 6. MCQ Specification

- 4 options (A–D). Option E removed.
- Key distribution per chapter: each letter 20–30%; no letter correct 3× in a row.
- Stem: ≥ 60% of items are vignettes (2–4 sentences, a patient or a tool deployment).
- Distractors: plausible misconceptions (e.g., confusing sensitivity with PPV). Zero joke options.
- Rationale: why the key is right + one line per distractor on why it is wrong.
- Each item tagged to one LO; each LO has ≥ 1 item.
- No item tests content absent from the chapter.
- Answers at chapter end, never under the question.
- Total: 110 MCQs + 11 short-answer cases.

---

## 7. Content Reuse & Correction Rules

**Keep and adapt (author's strongest material):** §2.4 risk/failure modes, §2.5 governance, §5.6 technical safety, §7.4 bias + Obermeyer case, Ch6 teaching style and §6.1.1 explanation, Figure 6.6 disclosure practice, CADe/CADx distinction, autonomy levels 0–5.

**Rewrite rule:** any reused paragraph is rewritten to the sentence-length and term-definition rules; clinical depth reduced to year-1 level.

**Mandatory corrections** if the topic survives (from `SESSION_SUMMARY.md`):

| Topic | Correct statement |
|---|---|
| k-space undersampling | Undersampling produces aliasing; networks suppress it using incoherent sampling + a learned prior; missing data is inferred, not recovered (link to hallucination risk) |
| MRI time saving | 25→5 / 40→10 min = 75–80% reduction |
| MASAI screening trial | Cite Lång 2023; 44% screen-reading workload reduction; +20% cancer detection; recall not reduced |
| Softmax output | Not a calibrated probability or statistical confidence |
| Stroke core | rCBF < 30% (not CBV) |
| Delta check | IV contamination dilutes (lowers) analytes; false rise = wrong patient/mislabel/interference |
| ICG | Hepatic/biliary excretion; does not show ureters |
| AML blasts | WHO 5th ed. (2022) removed 20% threshold for defining genetic abnormalities; ICC uses ≥10% |
| Physiological tremor | 8–12 Hz |
| ML vs logistic regression | Cite Christodoulou 2019: no average benefit in clinical prediction |
| AKI prediction (Tomašev 2019) | Report 93.6% male cohort and ~2 false alerts per true alert |
| STAR robot | Pre-clinical, animal study, small n |
| Data leakage | Train/test contamination, not a privacy issue |
| Learned intermediary | Product-liability doctrine: manufacturer discharges duty to warn by warning the clinician; not a shield for clinicians |
| §7.4.3 lesson | Obermeyer algorithm was race-blind; bias came from cost proxy → fix the label, not "blindness" |
| Differential privacy | Bounded, tunable guarantee (ε), not absolute |
| XAI | Saliency shows where, not whether reasoning is valid (Adebayo 2018) |
| Terminology | "leader–follower", not "master–slave" |

All tracked in `rework/errata-ledger.md` with status: fixed / removed-with-content.

---

## 8. Sourcing (research-synthesist persona)

- Target ~200 references across the book (~18 per chapter), median year ≥ 2021, ≥ 25% from 2023–2026.
- Must include: MASAI, CheXpert, MIMIC, HAM10000, IDx-DR (Abràmoff 2018), Obermeyer 2019, Tomašev 2019, Christodoulou 2019, Gichoya 2022, Daneshjou 2022, EchoNet-RCT (He 2023), TRIPOD+AI 2024, CONSORT-AI/SPIRIT-AI 2020, DECIDE-AI 2022, FDA PCCP final guidance 2024, EU AI Act (Reg. 2024/1689), EU MDR 2017/745, WHO LMM guidance 2024, AlphaFold (Jumper 2021), Med-PaLM (Singhal 2023), plus pharmacy (pharmacovigilance, MIPD, DDI alert fatigue) and PT (pose estimation, gait, wearables, tele-rehab) primary studies.
- Every added reference verified for existence (CrossRef/DOI lookup where web access allows); unverifiable references are not used. DOI included where available.
- Original 23 references retained (all verified correct); McKinney 2020 cited with Haibe-Kains 2020 caveat.
- No performance number without an in-text citation.

---

## 9. Figures

| Action | Figures |
|---|---|
| Keep, re-caption to match image | image2 (AI hierarchy), image3 (triage pipeline), image4 (radiomics), image5 (WSI), image15 (dermoscopy), image17 (digital pathology), image18 (closed-loop insulin), image19 (oculomics), image20 (maturity, with disclosure), image21 (liability), image22 (anonymisation), image23 (XAI), image24 (SaMD lifecycle) |
| Visual check before deciding | image7 (AR navigation — needs brain-shift caveat), image11 (stroke — may encode CBV error), image14 (hemodynamic), image16 (oncology workflow) |
| Drop | image1 (cover: hallucinated text), image6 (CVS — unsafe), image8 (orphan, mislabelled), image9, image10, image12, image13 (content removed) |
| New (briefs only; production method decided in plan) | Confusion matrix + PPV-vs-prevalence; train/validation/test split and leakage; LLM next-token; pose-estimation skeleton; pharmacovigilance pipeline; three-patient journey map; new cover |

Every figure referenced from the prose ("see Figure 4.2"); illustrative figures labelled "illustrative".

---

## 10. Personas (used inline, from `.agents/skills/`)

| Persona | Role | When |
|---|---|---|
| statistician | Author Ch4, co-author Ch3; audit every number in the book | Drafting Ch3–4; final numeric audit |
| research-synthesist | Reference search, verification, citation linking | Every chapter; final reference audit |
| psychologist | Cognitive load, emotional design, automation-bias content (Ch11), MCQ fairness | Review pass per chapter |
| narratologist | Three running patients, opening cases, continuity | Front matter + every opening case |
| anthropologist | Professional cultures of the four lenses, inclusive examples, Local Context boxes | Lens boxes review |
| historian | Brief history in Ch1; flags anachronism/myth claims | Ch1 |
| geographer | Not used | — |

Master-instructional-design audit framework (A–I) applied as the final pass on each chapter.

---

## 11. Deliverables & Layout

```
rework/
  00-front-matter.md
  ch01-what-ai-is.md … ch11-regulation-liability-human.md
  glossary.md
  references.md
  errata-ledger.md
  figures/            (kept + new figures)
AI_in_Health_Care_Interprofessional.md   (assembled book)
```

Original manuscript is not modified.

## 12. Verification (acceptance checks)

1. Script: word count per chapter within ±15% of budget; total 24–29k.
2. Script: mean sentence length ≤ 22; share of sentences > 40 words < 5%.
3. Script: MCQ key distribution per chapter (20–30% per letter); no E options.
4. Script: every `[n]` resolves to a reference; every reference cited ≥ 1×.
5. Script: every bolded first-use term appears in glossary.
6. Checklist: each chapter has all 11 template elements; lens boxes within ±20% length.
7. Errata ledger: every row closed.
8. Persona audits (statistician, research-synthesist, psychologist) + rubric re-score ≥ 75.

## 13. Out of Scope

- Changing the original `.md`/`.docx`.
- `.docx`/PDF typesetting (can follow later).
- Slides, lecture plans, LMS packaging.
- Arabic translation/glossary.

## 14. Open Items (need user input, do not block drafting)

1. Region confirmation — Egypt Local Context boxes assumed.
2. Authorship/credit for the reworked edition — assumed Dr. Elkholy as author; confirm whether she has approved the rework.
3. Live literature access: PubMed connector needs authorization in claude.ai connector settings; otherwise verification relies on CrossRef via web fetch.
