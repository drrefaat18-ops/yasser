# Chapter 4: Reading an AI Performance Claim

## Opening Case
Lina is still worried about her mole. A friend sends her a skin-check app. Its website says, "Our AI detects melanoma with 95% accuracy." Lina takes a photo. The app says "High risk — see a doctor urgently." She cannot sleep.

The next day, a public-health officer at her university explains that the number does not mean what Lina thinks. She asks three questions. Ninety-five percent of what? Tested on whom? And how common is melanoma in people like Lina? This chapter teaches you to ask these questions.

## Learning Objectives
By the end of this chapter you will be able to:
1. [LO1] Calculate sensitivity, specificity and positive predictive value from a 2 × 2 table.
2. [LO2] Explain why positive predictive value depends on how common a condition is.
3. [LO3] Interpret AUROC and explain when AUPRC is more useful.
4. [LO4] Distinguish discrimination from calibration.
5. [LO5] Rank study designs from weakest to strongest evidence.

## 4.1 The 2 × 2 Table
Most performance numbers come from one simple table, the **confusion matrix**. It compares the model's answer with the truth.

|  | Has disease | Healthy |
|---|---|---|
| Model says positive | True positive (TP) | False positive (FP) |
| Model says negative | False negative (FN) | True negative (TN) |

Four key measures come from this table:

- **Sensitivity** = TP ÷ (TP + FN). Of the sick people, how many does the model catch?
- **Specificity** = TN ÷ (TN + FP). Of the healthy people, how many does it clear?
- **Positive predictive value** (PPV) = TP ÷ (TP + FP). If the result is positive, how likely is disease?
- **Negative predictive value** (NPV) = TN ÷ (TN + FN). If the result is negative, how likely is health?

Sensitivity and specificity describe the test. PPV and NPV tell the patient what a result means. Lina needs PPV.

**Accuracy** is the share of all cases the model gets right. It can mislead. When a disease is rare, a model that always says "healthy" has high accuracy but catches no one.

## 4.2 Why a "95%" Test Can Be Wrong Most of the Time
Suppose the app has 95% sensitivity and 95% specificity. Suppose 5 in every 1,000 moles checked by young people are melanoma. Picture 100,000 moles (Figure 4.1).

- 500 are melanoma. The app catches 95%: 475 true positives.
- 99,500 are harmless. The app wrongly flags 5% of them: 4,975 false positives.
- So 475 + 4,975 = 5,450 moles are flagged.

PPV = 475 ÷ 5,450 = 8.7%.

When the app says "high risk", the mole is melanoma less than 1 time in 10. This is not because the app is bad. It is because melanoma is rare in this group. A negative result, however, is very reassuring.

![Figure 4.1 — How prevalence changes PPV](figures/confusion-ppv.svg)
*Figure 4.1 — The same test gives a PPV of 8.7% when the disease is rare and 68% when it is common. Illustrative.*

How common a condition is in the tested group is called **prevalence**. PPV rises with prevalence. In a skin clinic where 1 in 10 moles is melanoma, the same app has a PPV of about 68%. The model did not change. The population did.

> **Medical Background in 60 Seconds:** **Screening** tests people without symptoms, such as mammography. Prevalence is low, so false alarms are common. A **diagnostic test** is used when symptoms already raise concern, so prevalence is higher. The same AI can behave very differently in these two settings.

## 4.3 Thresholds and AUROC
Most models give a score, not a yes or no. Someone sets a **threshold**. Scores above it count as positive. A low threshold catches more disease but gives more false alarms. A high threshold does the opposite.

The **area under the ROC curve** (AUROC) sums up performance across all thresholds. It runs from 0.5 (a coin toss) to 1.0 (perfect). In plain words, it is the chance that a sick patient gets a higher score than a healthy one.

AUROC has limits. It says nothing about the one threshold used in practice. And for rare conditions it can look excellent while PPV is poor. For rare conditions, the **area under the precision–recall curve** (AUPRC) is more useful [1]. It shows how many alarms will be real.

## 4.4 Ranking Versus Honest Numbers
**Discrimination** means ranking patients well: do sicker patients get higher scores? AUROC measures this.

**Calibration** asks: do the numbers mean what they say? If a model gives 100 patients a 20% risk, about 20 should have the event. A model can rank well but still say 60% when the true risk is 20% [2].

Apps often show a number such as "Malignant: 92%". This is a model score. It is not a true probability unless the model has been calibrated and checked. Modern AI models are often overconfident [3].

## 4.5 How Strong Is the Evidence?
A number is only as good as the study behind it. From weakest to strongest:

1. **Old data, same hospital.** Often too optimistic.
2. **Old data, other hospitals.** Shows whether the model travels.
3. **New patients, output hidden.** The model runs quietly in the background.
4. **New patients, output used.** Clinicians act on it, and results are measured.
5. **Randomised controlled trial**s (RCTs). Patients or sites are randomly assigned to care with or without AI.

Examples show why this matters. A widely used sepsis model looked good in its developer's reports. An independent test in 27,697 patients found an AUROC of only 0.63. It missed two-thirds of sepsis cases [4]. In contrast, a randomised trial tested AI for measuring heart function on ultrasound. Cardiologists needed to correct the AI's readings less often than the sonographers' readings [5].

A **reporting guideline** lists what a good study must report. TRIPOD+AI is the guideline for prediction models [6]. CONSORT-AI is for trials of AI [7].

## 4.6 Five Questions to Ask About Any AI Claim
1. What was measured: sensitivity, PPV, AUROC or just "accuracy"?
2. Who was tested, and how common was the disease in them?
3. Was it tested at other hospitals?
4. Were the patients like mine, by age, sex and skin tone?
5. Did a trial show better patient outcomes, not just better scores?

> **Through Four Lenses**
> - **Medicine:** Doctors must turn sensitivity into PPV for their patient. A screening PPV of 9% means a positive result needs checking, not immediate treatment.
> - **Pharmacy:** Drug-safety alerts have a PPV too. If only 1 alert in 20 matters, staff learn to ignore them. Measuring alert PPV is essential.
> - **Physical Therapy:** Fall-risk scores need good calibration. "30% risk" should mean about 30 in 100 similar patients fall, or goals will be wrong.
> - **Health Sciences:** Public-health officers must plan for prevalence. The same AI can flood clinics with false alarms in a low-risk group.

> **Myth vs Evidence:** Myth: "A high AUROC means the model is ready for the clinic." Evidence: A sepsis model used in hundreds of hospitals had an AUROC of only 0.63 on independent testing [4]. Calibration, PPV and outside testing all matter.

> **Safety Alert:** In a group where the disease is rare, a positive AI result is more likely false than true. Confirm before acting, and explain this kindly to anxious patients.

## Key Takeaways
- Sensitivity and specificity describe a test; PPV tells the patient what a result means.
- PPV depends on prevalence: a "95%" test can have a PPV below 10% in screening.
- AUROC measures ranking; AUPRC is better for rare conditions.
- A score such as "92%" is not a true probability unless the model is calibrated.
- Evidence gets stronger from old data to outside testing to randomised trials.

## Self-Assessment
**Q1.** A model is tested on 200 patients with pneumonia and 800 without. It flags 160 of the sick and 80 of the healthy. What is its sensitivity? [LO1]
A) 80%
B) 67%
C) 90%
D) 20%

**Q2.** Using the same data, what is the PPV? [LO1]
A) 80%
B) 90%
C) 67%
D) 33%

**Q3.** An eye-disease AI moves from a specialist clinic (20% prevalence) to community screening (1% prevalence). What happens to its PPV? [LO2]
A) It stays the same.
B) It falls sharply because the disease is rarer.
C) It rises because more people are tested.
D) It becomes equal to the NPV.

**Q4.** What does an AUROC of 0.85 mean? [LO3]
A) The model is right in 85% of cases.
B) 85% of positive results are true.
C) The model is calibrated.
D) There is an 85% chance a sick patient scores higher than a healthy one.

**Q5.** A condition affects 2% of admissions. Which measure best shows how many alerts will be real? [LO3]
A) AUPRC
B) Accuracy
C) AUROC alone
D) Specificity alone

**Q6.** A fall-risk model ranks patients well. But of patients given "40% risk", only 10% fall. What is the problem? [LO4]
A) Poor ranking
B) Data leakage
C) Poor calibration
D) Too few patients

**Q7.** Lina's app shows "Malignant: 92%". What is the best interpretation? [LO4]
A) There is a 92% chance of melanoma.
B) The app is 92% accurate.
C) 92% of doctors agree.
D) It is a model score, not a reliable probability unless calibrated for people like her.

**Q8.** Which design gives the strongest evidence that an AI tool helps patients? [LO5]
A) Testing on old data from the same hospital
B) A randomised controlled trial
C) A company press release
D) Testing on old data from other hospitals

**Q9.** A test has 95% sensitivity and 95% specificity. Prevalence is 5 per 1,000. Out of 100,000 people, how many false positives are there? [LO2]
A) 25
B) 475
C) 4,975
D) 94,525

**Q10.** A team reports a new AI prediction model. Which reporting guideline should they follow? [LO5]
A) TRIPOD+AI
B) CONSORT-AI
C) A press-release template
D) No guideline exists

**Case Question.** Lina says, "The app said high risk and it is 95% accurate, so I probably have cancer." Using Section 4.2, write a short, kind reply and tell her what to do next.

## Answers and Rationales
**Q1. A** — 160 ÷ 200 = 80%. B is the PPV. C and D are wrong.

**Q2. C** — 160 ÷ (160 + 80) = 67%. A is sensitivity. B is specificity. D is the false share.

**Q3. B** — PPV falls as the disease gets rarer. A ignores prevalence. C and D are false.

**Q4. D** — This is the plain meaning of AUROC. A is accuracy. B is PPV. C is calibration.

**Q5. A** — AUPRC suits rare outcomes and shows real alarms [1]. B and C can look good while PPV is poor. D ignores missed cases.

**Q6. C** — Ranking is good, but the stated risks are too high [2]. A, B and D do not explain it.

**Q7. D** — Model scores are often overconfident and need calibration [3]. A, B and C misread the number.

**Q8. B** — Randomisation best shows the true effect of AI on care. A and D are weaker. C is not evidence.

**Q9. C** — 5% of 99,500 healthy people = 4,975. A is missed cases. B is true positives. D is true negatives.

**Q10. A** — TRIPOD+AI is for prediction models [6]. B is for trials. C and D are wrong.

**Case Question — model answer.** "I understand why you are scared. The 95% describes the app overall, not your personal chance. Melanoma is rare at your age, so most 'high risk' results are false alarms; fewer than 1 in 10 flagged moles is melanoma. Your mole has changed, so it still needs checking. Please book a skin clinic visit this week."

## References
1. Saito T, Rehmsmeier M. The precision-recall plot is more informative than the ROC plot when evaluating binary classifiers on imbalanced datasets. PLoS One. 2015;10(3):e0118432. DOI: 10.1371/journal.pone.0118432
2. Van Calster B, McLernon DJ, van Smeden M, et al. Calibration: the Achilles heel of predictive analytics. BMC Med. 2019;17:230. DOI: 10.1186/s12916-019-1466-7
3. Guo C, Pleiss G, Sun Y, Weinberger KQ. On calibration of modern neural networks. In: Proceedings of the 34th International Conference on Machine Learning. PMLR 70; 2017:1321-1330. https://proceedings.mlr.press/v70/guo17a.html
4. Wong A, Otles E, Donnelly JP, et al. External validation of a widely implemented proprietary sepsis prediction model in hospitalized patients. JAMA Intern Med. 2021;181(8):1065-1070. DOI: 10.1001/jamainternmed.2021.2626
5. He B, Kwan AC, Cho JH, et al. Blinded, randomized trial of sonographer versus AI cardiac function assessment. Nature. 2023;616(7957):520-524. DOI: 10.1038/s41586-023-05947-3
6. Collins GS, Moons KGM, Dhiman P, et al. TRIPOD+AI statement: updated guidance for reporting clinical prediction models that use regression or machine learning methods. BMJ. 2024;385:e078378. DOI: 10.1136/bmj-2023-078378
7. Liu X, Cruz Rivera S, Moher D, et al. Reporting guidelines for clinical trial reports for interventions involving artificial intelligence: the CONSORT-AI extension. BMJ. 2020;370:m3164. DOI: 10.1136/bmj.m3164
