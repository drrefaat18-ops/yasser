# Chapter 4: Reading an AI Performance Claim

## Opening Case
Lina is still worried about her mole. A friend sends her a skin-check app. Its website says, "Our AI detects melanoma with 95% accuracy." Lina takes a photo. The app says "High risk — see a doctor urgently." She cannot sleep.

The next day, a public-health officer running a skin-cancer campaign at her university explains that the number on the website does not mean what Lina thinks. She asks three questions. Ninety-five percent of what? Tested on whom? And how common is melanoma in people like Lina? By the end of this chapter, you will be able to ask these questions yourself and answer them.

## Learning Objectives
By the end of this chapter you will be able to:
1. [LO1] Calculate sensitivity, specificity, positive and negative predictive value from a 2 × 2 table.
2. [LO2] Explain why positive predictive value depends on how common a condition is.
3. [LO3] Interpret a ROC curve and AUROC, and explain when AUPRC is more informative.
4. [LO4] Distinguish discrimination from calibration.
5. [LO5] Rank study designs from retrospective testing to randomised trials and use reporting guidelines to judge a study.

## 4.1 The 2 × 2 Table
Most performance numbers come from one simple table, the **confusion matrix**. It compares the model's answer with the truth for every case.

|  | Truly has disease | Truly healthy |
|---|---|---|
| Model says positive | True positive (TP) | False positive (FP) |
| Model says negative | False negative (FN) | True negative (TN) |

From this table come four key measures:

- **Sensitivity** = TP ÷ (TP + FN). Of the people who have the disease, what share does the model catch?
- **Specificity** = TN ÷ (TN + FP). Of the healthy people, what share does the model correctly clear?
- **Positive predictive value** (PPV) = TP ÷ (TP + FP). If the model says positive, how likely is disease?
- **Negative predictive value** (NPV) = TN ÷ (TN + FN). If the model says negative, how likely is health?

Sensitivity and specificity describe the test. PPV and NPV describe what a result means for the person in front of you. Lina needs PPV.

**Accuracy** is (TP + TN) ÷ all cases. It sounds useful but hides a trap. When a disease is rare, a model that always says "healthy" has high accuracy and catches nobody (Chapter 3).

## 4.2 Why a "95%" Test Can Be Wrong Most of the Time
Suppose the skin app truly has 95% sensitivity and 95% specificity. Suppose melanoma is present in 5 of every 1,000 moles checked by young people. What does a positive result mean?

Picture 100,000 moles (Figure 4.1).

- 500 are melanoma (5 per 1,000). The app catches 95%: 475 true positives and 25 false negatives.
- 99,500 are harmless. The app clears 95%: 94,525 true negatives. The other 5%, or 4,975, are false positives.
- In total, 475 + 4,975 = 5,450 moles are flagged.

PPV = 475 ÷ 5,450 = 8.7%.

So when the app says "high risk", the mole is melanoma less than 1 time in 10. The other 9 alarms are false. This is not because the app is bad. It is because melanoma is rare in this group. NPV, by contrast, is 94,525 ÷ 94,550 = 99.97%. A negative result is very reassuring.

![Figure 4.1 — How prevalence changes PPV](figures/confusion-ppv.svg)
*Figure 4.1 — The same test (95% sensitivity, 95% specificity) gives a PPV of 8.7% at 5 per 1,000 prevalence, and a much higher PPV when the condition is common. Illustrative.*

How common a condition is in the tested group is called **prevalence**. PPV rises with prevalence. If the same app were used in a dermatology clinic where 1 in 10 referred moles is melanoma, its PPV would be about 68%. The model did not change. The population did.

> **Deeper Dive:** This is Bayes' theorem. PPV = (sensitivity × prevalence) ÷ [(sensitivity × prevalence) + (1 − specificity) × (1 − prevalence)]. With 0.95, 0.005 and 0.95: 0.00475 ÷ (0.00475 + 0.04975) = 0.087. Try prevalence 0.10: 0.095 ÷ (0.095 + 0.045) = 0.68.

> **Medical Background in 60 Seconds:** **Screening** tests people without symptoms to find disease early, such as mammography or retinal photos in diabetes. In screening, prevalence is low, so false positives are common. A **diagnostic test** is used when symptoms already raise suspicion, so prevalence is higher. The same AI can perform very differently in these two settings.

## 4.3 Thresholds, ROC Curves and AUROC
Most models give a score, not a yes or no. Someone chooses a **threshold**. Scores above it count as positive. A low threshold catches more disease (higher sensitivity) but raises more false alarms (lower specificity). A high threshold does the opposite.

A **ROC curve** plots sensitivity against 1 − specificity for every possible threshold. The **area under the ROC curve** (AUROC, also called the C-statistic) summarises the curve in one number between 0.5 and 1.0. An AUROC of 0.5 is a coin toss. An AUROC of 1.0 is perfect.

AUROC has a simple meaning. It is the probability that the model gives a randomly chosen patient with the disease a higher score than a randomly chosen patient without it.

AUROC has two limits. First, it says nothing about any single threshold, and clinicians use one threshold. Second, when a condition is rare, AUROC can look excellent while PPV is poor. For rare conditions, the **area under the precision–recall curve** (AUPRC) is more informative [2]. Precision is another name for PPV, and recall is another name for sensitivity. AUPRC shows directly how many alarms will be real.

## 4.4 Discrimination Versus Calibration
**Discrimination** is the ability to rank patients: do sicker patients get higher scores? AUROC measures discrimination.

**Calibration** asks a different question: do the numbers mean what they say? If a model gives 100 patients a 20% risk, about 20 of them should have the event. A model can rank well but be badly calibrated. It might say 60% when the true risk is 20%. Poor calibration misleads decisions about treatment [3].

Many deep-learning models output a number between 0 and 1 from a final "softmax" step. This number is often presented as a probability or a "confidence". It is neither, unless the model has been calibrated and checked. Modern neural networks tend to be overconfident [12]. When an app shows "Malignant: 92%", ask whether that number has been calibrated in patients like yours.

## 4.5 Measuring Outlines: Dice and IoU
Some models draw outlines, for example around a tumour or a joint. Two overlap measures are common. The **Dice coefficient** is twice the overlap divided by the total size of both outlines. **Intersection over union** (IoU) is the overlap divided by the combined area. Both range from 0 (no overlap) to 1 (perfect). They can hide clinically important errors, such as missing a small lesion completely, so experts recommend choosing metrics to fit the clinical question [4].

## 4.6 How Strong Is the Evidence?
A performance number is only as good as the study that produced it. From weakest to strongest:

1. **Retrospective internal testing.** The model is tested on old data from the same source. Often optimistic.
2. **Retrospective external validation.** Old data from other hospitals or populations. Shows generalisation.
3. **Prospective silent testing.** The model runs on new patients, but clinicians do not see its output.
4. **Prospective clinical studies.** Clinicians use the output; outcomes and workflow are measured.
5. **Randomised controlled trial**s (RCTs). Patients or sites are randomly assigned to care with or without AI.

Real examples show why this ladder matters. A widely used sepsis prediction model was reported by its developer to perform well. Independent external validation in 27,697 patients found an AUROC of 0.63. The model missed two-thirds of sepsis cases and alerted on 18% of all admitted patients [5]. In contrast, a blinded RCT of AI for measuring heart pumping function on ultrasound found that cardiologists changed the AI's initial assessment less often than sonographers' assessments [6]. The MASAI breast-screening trial is another RCT with clear results [1].

A review of studies comparing deep learning with clinicians found few randomised trials. Many non-randomised studies claimed that AI matched or beat experts despite a high risk of bias [7].

**Reporting guideline**s help readers judge a study. TRIPOD+AI covers prediction models [8]. CONSORT-AI covers trials of AI interventions [9], and SPIRIT-AI covers their protocols [10]. DECIDE-AI covers early clinical evaluation [11]. If a study does not report the items these guidelines list, be cautious.

## 4.7 Ten Questions to Ask About Any AI Claim
1. What exactly was measured: sensitivity, specificity, PPV, AUROC or "accuracy"?
2. What was the reference standard, and who decided the truth?
3. What was the prevalence in the test group, and is it like my setting?
4. Was the test set external, from other sites or times?
5. Was the study prospective or retrospective?
6. Which threshold will be used in practice, and what are sensitivity and PPV at that threshold?
7. Is the model calibrated, and was calibration checked in a population like mine?
8. How did performance vary across age, sex, skin tone and other groups?
9. How many false alarms per true alarm should staff expect?
10. Did any trial show better patient outcomes, not just better scores?

> **Through Four Lenses**
> - **Medicine:** Physicians must translate sensitivity and specificity into PPV for the patient in front of them. A screening-level PPV of 9% means a positive result needs confirmation, not immediate treatment.
> - **Pharmacy:** Pharmacists receive drug-safety alerts with their own PPV. If only 1 in 20 interaction alerts matters, staff learn to ignore them. Measuring alert PPV is as important as measuring sensitivity.
> - **Physical Therapy:** Physiotherapists using fall-risk or re-injury scores should ask about calibration. A score of "30% risk" should mean roughly 30 of 100 similar patients fall, or goals will be set wrongly.
> - **Health Sciences:** Public-health officers plan screening programmes and must model prevalence. The same AI can overload clinics with false positives in a low-risk population and work well in a high-risk one.

> **Myth vs Evidence:** Myth: "A high AUROC means the model is ready for the clinic." Evidence: A sepsis model deployed in hundreds of hospitals had an AUROC of only 0.63 on independent testing and generated many false alerts [5]. Discrimination, calibration, PPV at the chosen threshold and external validation all matter.

> **Safety Alert:** A positive AI result in a low-prevalence group is more likely to be false than true. Confirm before acting, and explain this to anxious patients like Lina.

## Key Takeaways
- Sensitivity and specificity describe a test; PPV and NPV describe what a result means for a patient.
- PPV depends on prevalence: a "95% accurate" test can have a PPV below 10% in screening.
- AUROC measures ranking, not usefulness at a threshold; AUPRC is better for rare conditions.
- Discrimination and calibration are different; a model's "92%" is not a probability unless calibrated.
- Evidence strength rises from retrospective internal tests to external, prospective and randomised studies.

## Self-Assessment
**Q1.** A model is tested on 200 patients with pneumonia and 800 without. It flags 160 of the patients with pneumonia and 80 of those without. What is its sensitivity? [LO1]
A) 80%
B) 67%
C) 90%
D) 20%

**Q2.** Using the same data as Q1, what is the PPV? [LO1]
A) 80%
B) 90%
C) 67%
D) 33%

**Q3.** An AI test for a rare eye disease has 90% sensitivity and 90% specificity. It is moved from a specialist clinic, where prevalence is 20%, to community screening, where prevalence is 1%. What happens to its PPV? [LO2]
A) It stays the same because sensitivity and specificity are unchanged.
B) It falls sharply because the disease is much rarer.
C) It rises because more people are tested.
D) It becomes equal to the NPV.

**Q4.** What does an AUROC of 0.85 mean? [LO3]
A) The model is correct in 85% of cases.
B) 85% of positive results are true.
C) The model is calibrated.
D) There is an 85% chance that a random patient with the condition scores higher than a random patient without it.

**Q5.** A hospital compares two sepsis models for a condition present in 2% of admissions. Which measure best shows how many alerts will be real across thresholds? [LO3]
A) AUPRC
B) Accuracy
C) AUROC alone
D) Specificity alone

**Q6.** A fall-risk model ranks patients well (AUROC 0.82). But among patients given "40% risk", only 10% fall. What is the problem? [LO4]
A) Poor discrimination
B) Data leakage
C) Poor calibration
D) Class imbalance in the training set only

**Q7.** Lina's app shows "Malignant: 92%". What is the most accurate interpretation? [LO4]
A) There is a 92% chance the mole is melanoma.
B) The app is 92% accurate.
C) 92% of dermatologists agree.
D) It is a model score that is not a reliable probability unless the model was calibrated for people like her.

**Q8.** Which study design gives the strongest evidence that an AI tool improves patient care? [LO5]
A) Retrospective internal testing
B) A randomised controlled trial
C) A developer's press release
D) Retrospective external validation

**Q9.** A screening test has 95% sensitivity and 95% specificity. Prevalence is 5 per 1,000. Out of 100,000 people, how many false positives are there? [LO2]
A) 25
B) 475
C) 4,975
D) 94,525

**Q10.** A research team reports a new AI prediction model. Which reporting guideline should they follow? [LO5]
A) TRIPOD+AI
B) CONSORT-AI
C) SPIRIT-AI
D) DECIDE-AI

**Case Question.** Lina asks you, "The app said high risk and it is 95% accurate, so I probably have cancer, right?" Using the numbers from Section 4.2, write a short, kind explanation she can understand, and tell her what to do next.

## Answers and Rationales
**Q1. A** — Sensitivity = 160 ÷ 200 = 80%. B is the PPV. C and D are wrong calculations.

**Q2. C** — PPV = 160 ÷ (160 + 80) = 67%. A is sensitivity. B is specificity (720 ÷ 800). D is the false share of positive results.

**Q3. B** — PPV falls with prevalence: about 69% at 20% prevalence and about 8% at 1%. A ignores prevalence. C and D are false.

**Q4. D** — This is the ranking meaning of AUROC. A describes accuracy. B describes PPV. C concerns calibration.

**Q5. A** — AUPRC shows precision (PPV) across recall levels and suits rare outcomes [2]. B is misleading under imbalance. C can look good while PPV is poor. D ignores missed cases.

**Q6. C** — Ranking is good but the stated risks are too high, which is miscalibration [3]. A is contradicted by the AUROC. B and D do not explain the mismatch.

**Q7. D** — Softmax scores are often overconfident and are not probabilities without calibration [12]. A, B and C misread the number.

**Q8. B** — Randomisation best isolates the effect of the AI on care. A and D are weaker. C is not evidence.

**Q9. C** — 5% of 99,500 healthy people = 4,975 false positives. A is the false negatives. B is the true positives. D is the true negatives.

**Q10. A** — TRIPOD+AI covers prediction models [8]. B and C cover trials and trial protocols. D covers early clinical evaluation.

**Case Question — model answer.** "I understand why you are scared. The 95% describes how the app performs overall, not your personal chance. Melanoma is rare in young people, so most 'high risk' results are false alarms. With these numbers, fewer than 1 in 10 flagged moles is actually melanoma. That still means your mole should be checked, because it has changed, so please book a dermatology appointment this week. The app cannot give you a diagnosis; a skin examination can."

## References
1. Lång K, Josefsson V, Larsson AM, et al. Artificial intelligence-supported screen reading versus standard double reading in the Mammography Screening with Artificial Intelligence trial (MASAI): a clinical safety analysis of a randomised, controlled, non-inferiority, single-blinded, screening accuracy study. Lancet Oncol. 2023;24(8):936-944. DOI: 10.1016/s1470-2045(23)00298-x
2. Saito T, Rehmsmeier M. The precision-recall plot is more informative than the ROC plot when evaluating binary classifiers on imbalanced datasets. PLoS One. 2015;10(3):e0118432. DOI: 10.1371/journal.pone.0118432
3. Van Calster B, McLernon DJ, van Smeden M, et al. Calibration: the Achilles heel of predictive analytics. BMC Med. 2019;17:230. DOI: 10.1186/s12916-019-1466-7
4. Maier-Hein L, Reinke A, Godau P, et al. Metrics reloaded: recommendations for image analysis validation. Nat Methods. 2024;21(2):195-212. DOI: 10.1038/s41592-023-02151-z
5. Wong A, Otles E, Donnelly JP, et al. External validation of a widely implemented proprietary sepsis prediction model in hospitalized patients. JAMA Intern Med. 2021;181(8):1065-1070. DOI: 10.1001/jamainternmed.2021.2626
6. He B, Kwan AC, Cho JH, et al. Blinded, randomized trial of sonographer versus AI cardiac function assessment. Nature. 2023;616(7957):520-524. DOI: 10.1038/s41586-023-05947-3
7. Nagendran M, Chen Y, Lovejoy CA, et al. Artificial intelligence versus clinicians: systematic review of design, reporting standards, and claims of deep learning studies. BMJ. 2020;368:m689. DOI: 10.1136/bmj.m689
8. Collins GS, Moons KGM, Dhiman P, et al. TRIPOD+AI statement: updated guidance for reporting clinical prediction models that use regression or machine learning methods. BMJ. 2024;385:e078378. DOI: 10.1136/bmj-2023-078378
9. Liu X, Cruz Rivera S, Moher D, et al. Reporting guidelines for clinical trial reports for interventions involving artificial intelligence: the CONSORT-AI extension. BMJ. 2020;370:m3164. DOI: 10.1136/bmj.m3164
10. Cruz Rivera S, Liu X, Chan AW, et al. Guidelines for clinical trial protocols for interventions involving artificial intelligence: the SPIRIT-AI extension. BMJ. 2020;370:m3210. DOI: 10.1136/bmj.m3210
11. Vasey B, Nagendran M, Campbell B, et al. Reporting guideline for the early stage clinical evaluation of decision support systems driven by artificial intelligence: DECIDE-AI. BMJ. 2022;377:e070904. DOI: 10.1136/bmj-2022-070904
12. Guo C, Pleiss G, Sun Y, Weinberger KQ. On calibration of modern neural networks. In: Proceedings of the 34th International Conference on Machine Learning. PMLR 70; 2017:1321-1330. https://proceedings.mlr.press/v70/guo17a.html
