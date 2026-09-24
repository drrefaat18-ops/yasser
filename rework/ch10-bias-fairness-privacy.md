# Chapter 10: Bias, Fairness and Privacy

## Opening Case
The university's public-health team is planning a skin-cancer awareness campaign. The team leader proposes recommending a free skin-check app to all students. A team member mentions Lina's experience. The app flagged her mole, but its website shows almost no photos of dark skin. Would it work as well for her as for her lighter-skinned classmates?

Across town, Karim's employer offers workers a free fitness wristband "to support wellbeing". Karim's physiotherapist reads the terms. Step counts, heart rate and sleep data will be shared with the employer's insurance partner. Karim worries that his slower recovery could affect his job.

Both stories raise one question: who is protected by health AI, and who might be harmed by it? This chapter looks at bias, fairness and privacy.

## Learning Objectives
By the end of this chapter you will be able to:
1. [LO1] Identify where bias can enter the AI pipeline, from problem choice to deployment.
2. [LO2] Analyse the Obermeyer case and explain why the choice of label caused the bias.
3. [LO3] Distinguish anonymisation, pseudonymisation and de-identification, and explain re-identification risk.
4. [LO4] Describe privacy-preserving methods, including differential privacy and federated learning, and their limits.
5. [LO5] Compare the core principles of major data-protection laws, including Egypt's.

## 10.1 Where Bias Comes From
**Algorithmic bias** means that a model performs systematically worse, or makes systematically worse recommendations, for some groups. Bias can enter at every step.

- **Problem choice.** Which conditions get AI tools, and which communities are they designed for?
- **Data collection.** Who is in the dataset? Chapter 2 showed that famous datasets come from a few wealthy settings.
- **Labels.** What counts as the "right answer"? A proxy label can carry past inequality.
- **Model development.** Is performance reported for each group, or only on average?
- **Deployment.** Is the tool used in a population like the one it was tested in?
- **Feedback.** Do the tool's decisions shape the data used to train its next version?

Skin tone is a clear example. Dermatology datasets contain mostly light skin [4]. When models were tested on images balanced across skin tones, performance fell on darker skin [5]. For Lina, this is not abstract.

Bias can also hide inside images. A study of chest X-rays found that AI models underdiagnosed disease more often in female, Black, Hispanic and younger patients, and in patients with public insurance for low income [3]. Patients who already face barriers in care were more likely to be told they were healthy when they were not.

## 10.2 The Obermeyer Case: When the Label Is the Problem
A widely used US commercial algorithm selected patients for an extra-care programme [1]. It predicted which patients would need the most care. The developers used health-care cost as the label for health need. The algorithm did not use race as an input.

The researchers found that at the same risk score, Black patients were considerably sicker than white patients. The reason was the label. Because of unequal access to care, less money had been spent on Black patients with the same level of illness. The model learned correctly that they would cost less, and wrongly treated that as meaning they needed less.

When the researchers changed the label to direct measures of health, such as the number of active chronic conditions, the share of Black patients selected for extra help rose from 17.7% to 46.5% [1].

The lesson is often stated wrongly. Removing race from the inputs did not prevent bias here, because the model was already race-blind. The bias came from a label that reflected unequal access. The fix was to change what the model predicted.

Removing sensitive variables also fails for another reason. AI models can detect a patient's self-reported race from chest X-rays with high accuracy, even when images are blurred or cropped, and even though experts cannot see how [2]. A model can use information that no one intended it to use. "Fairness through blindness" is not a reliable strategy. Fairness needs measurement: report performance for each group, choose labels carefully and monitor after deployment.

> **Medical Background in 60 Seconds:** The **Fitzpatrick scale** classifies skin by how it reacts to sun, from type I (always burns, never tans) to type VI (deeply pigmented, rarely burns). Melanoma is less common in darker skin but is often diagnosed later, when outcomes are worse. It may also appear in less expected places, such as the palms, soles or nails.

## 10.3 Privacy: Identifiers and Re-Identification
Health data are among the most sensitive personal data. Removing names is not enough to protect them.

Three terms are often confused:

- **De-identification** removes or changes details that could identify a person. In the United States, the HIPAA "Safe Harbor" method lists 18 identifiers to remove, such as names, full dates and record numbers [11].
- **Pseudonymisation** replaces identifiers with a code. Someone who holds the key can re-link the data. Under European law, pseudonymised data are still personal data [10].
- **Anonymisation** makes re-identification impossible by reasonable means. True anonymisation is hard to achieve for rich health data.

The problem is **re-identification**. Combining a few ordinary facts can single a person out. Early work showed that ZIP code, birth date and sex together identify most US residents [8]. A later study estimated that 99.98% of Americans could be correctly re-identified in any dataset using 15 demographic attributes [6]. Wearable data are especially risky, because movement and sleep patterns are almost unique to each person.

![Figure 10.1 — A privacy pipeline for AI training](figures/privacy-pipeline.svg)
*Figure 10.1 — Raw records are de-identified, protected with privacy methods and stored securely. Each step reduces, but does not remove, re-identification risk. Illustrative.*

## 10.4 Privacy-Preserving Methods
**Differential privacy** adds carefully measured random noise to data or results. It gives a mathematical limit on how much anyone can learn about one individual [7]. The limit is controlled by a setting called epsilon (ε). A smaller ε means stronger privacy but less accurate results. Differential privacy is a tunable, bounded guarantee. It is not absolute protection.

**Federated learning** trains a model across several hospitals without moving patient data. Each hospital trains on its own data and shares only model updates. A central server combines the updates [9]. This reduces data transfer. But model updates can still leak some information, so federated learning is often combined with other protections.

## 10.5 The Law: Principles Across Countries
Laws differ, but share core principles: a lawful basis for processing, purpose limitation, data minimisation, security and rights for individuals.

- **GDPR** in the European Union treats health data as a special category needing extra protection [10]. It gives rights about automated decisions. Whether it creates a full "right to explanation" of AI decisions is debated among legal scholars [12].
- **HIPAA** in the United States sets rules for health providers and insurers, including the Safe Harbor de-identification standard [11].

> **Local Context:** Egypt's **Personal Data Protection Law** (Law No. 151 of 2020) treats health data as sensitive personal data. Processing it generally requires explicit written consent and stronger security. Executive regulations issued in 2025 set out detailed technical and procedural requirements [13].

For Karim, these principles matter directly. Wellness-programme data shared with an insurer may fall outside health-privacy rules that cover clinicians. He has the right to know how his data will be used before he agrees.

> **Through Four Lenses**
> - **Medicine:** Physicians should ask vendors for performance by sex, age, ethnicity and skin tone. An average accuracy figure can hide poor performance in exactly the patients who already face worse care.
> - **Pharmacy:** Pharmacists handle prescription and dispensing data that reveal diagnoses. Sharing them with apps or loyalty schemes needs clear consent, because a medicine list can identify a condition.
> - **Physical Therapy:** Physiotherapists should explain to patients like Karim what wearables record and who sees it. Movement and sleep data are highly personal and are hard to anonymise.
> - **Health Sciences:** Public-health officers should test tools in the community they serve before recommending them. A campaign app that fails on darker skin would widen, not narrow, health gaps.

> **Myth vs Evidence:** Myth: "If a model does not use race as an input, it cannot be racially biased." Evidence: The Obermeyer algorithm did not use race, yet it under-selected Black patients because its cost label reflected unequal access [1]. Models can also infer race from images [2].

> **Safety Alert:** Before recommending any AI tool to a group of patients, check whether it was tested in people like them. If there is no evidence, say so.

## Key Takeaways
- Bias can enter at problem choice, data, labels, development, deployment and feedback.
- In the Obermeyer case, a cost label carried unequal access into the model; changing the label fixed much of the bias.
- Removing sensitive variables does not guarantee fairness; measuring performance by group does.
- Re-identification is easy with combined details; pseudonymised data remain personal data.
- Differential privacy and federated learning reduce, but do not remove, privacy risk.

## Self-Assessment
**Q1.** A skin-check app was trained mostly on images of light skin. At which step did bias most likely enter? [LO1]
A) Deployment feedback
B) Legal review
C) Data collection
D) Model compression

**Q2.** In the Obermeyer case, why did Black patients with the same risk score have more illness than white patients? [LO2]
A) The label was health-care cost, which reflected unequal access to care.
B) Race was used as an input variable.
C) The dataset was too small.
D) The algorithm was a large language model.

**Q3.** A developer says, "We removed race from the inputs, so our imaging model is fair." What is the best reply? [LO2]
A) Correct; removing race guarantees fairness.
B) Fairness is not relevant in imaging.
C) Images cannot contain information about race.
D) Models can infer race from images, so fairness must be measured by group.

**Q4.** A research team replaces patient names with codes but keeps a key file linking codes to names. What is this called? [LO3]
A) Anonymisation
B) Pseudonymisation
C) Differential privacy
D) Federated learning

**Q5.** Why is wearable movement data difficult to anonymise? [LO3]
A) It is always stored on paper.
B) It contains no personal information.
C) Movement and sleep patterns are almost unique to each person.
D) It is protected by default.

**Q6.** A hospital adds random noise to a dataset release, with a setting ε that controls privacy strength. What is true of this method? [LO4]
A) It gives a bounded, tunable guarantee; smaller ε gives stronger privacy but less accuracy.
B) It guarantees that no information about anyone can ever be learned.
C) It removes the need for consent.
D) It is the same as pseudonymisation.

**Q7.** Five hospitals train a shared model, each on its own data, sending only model updates to a central server. What is this approach? [LO4]
A) Retrieval-augmented generation
B) Pseudonymisation
C) Reinforcement learning
D) Federated learning

**Q8.** Under Egypt's Personal Data Protection Law, how is health data treated? [LO5]
A) As public data that anyone may use
B) As sensitive data, generally requiring explicit written consent and stronger security
C) As exempt from any protection
D) As data only employers can process

**Q9.** Under GDPR, what is the status of pseudonymised health data? [LO5]
A) It is still personal data.
B) It is fully anonymous.
C) It is not covered by the law.
D) It can be sold freely.

**Q10.** In a chest X-ray study, AI underdiagnosed disease more often in which patients? [LO1]
A) Only in older white men
B) Equally in all groups
C) In female, Black, Hispanic and younger patients, and those with low-income public insurance
D) Only in patients with rare diseases

**Case Question.** Karim asks you whether he should accept the employer's free wristband. Write a short, balanced answer that explains the privacy risks, the questions he should ask, and what he can do if he is unsure.

## Answers and Rationales
**Q1. C** — The training images under-represented dark skin, so bias entered during data collection [4, 5]. A, B and D are not where this bias began.

**Q2. A** — Cost reflected unequal access, so equally sick Black patients looked less needy [1]. B is false; race was not an input. C and D are wrong.

**Q3. D** — Race can be detected from images [2], so removing it does not prevent bias. A, B and C are false.

**Q4. B** — Codes with a linking key are pseudonymisation. A makes re-linking impossible. C adds noise. D trains across sites.

**Q5. C** — Unique behavioural patterns allow re-identification [6]. A, B and D are false.

**Q6. A** — Differential privacy is a tunable, bounded guarantee [7]. B overstates it. C and D are wrong.

**Q7. D** — Training locally and sharing updates is federated learning [9]. A, B and C are different methods.

**Q8. B** — Health data are sensitive under Law No. 151 of 2020, generally requiring explicit written consent [13]. A, C and D are wrong.

**Q9. A** — Pseudonymised data remain personal data under GDPR [10]. B, C and D are wrong.

**Q10. C** — Underdiagnosis was greater in these groups [3]. A, B and D do not match the findings.

**Case Question — model answer.** "A free wristband can help you track your activity, but the terms say your steps, heart rate and sleep will be shared with an insurance partner. That data can reveal a lot about your health and recovery, and it is hard to make anonymous. Before agreeing, ask who will see the data, what it will be used for, how long it is kept and whether you can withdraw. You can also ask whether saying no affects your job or benefits. If the answers are unclear, you can decline, or use a device that keeps data only on your own phone."

## References
1. Obermeyer Z, Powers B, Vogeli C, Mullainathan S. Dissecting racial bias in an algorithm used to manage the health of populations. Science. 2019;366(6464):447-453. DOI: 10.1126/science.aax2342
2. Gichoya JW, Banerjee I, Bhimireddy AR, et al. AI recognition of patient race in medical imaging: a modelling study. Lancet Digit Health. 2022;4(6):e406-e414. DOI: 10.1016/s2589-7500(22)00063-2
3. Seyyed-Kalantari L, Zhang H, McDermott MBA, Chen IY, Ghassemi M. Underdiagnosis bias of artificial intelligence algorithms applied to chest radiographs in under-served patient populations. Nat Med. 2021;27(12):2176-2182. DOI: 10.1038/s41591-021-01595-0
4. Adamson AS, Smith A. Machine learning and health care disparities in dermatology. JAMA Dermatol. 2018;154(11):1247-1248. DOI: 10.1001/jamadermatol.2018.2348
5. Daneshjou R, Vodrahalli K, Novoa RA, et al. Disparities in dermatology AI performance on a diverse, curated clinical image set. Sci Adv. 2022;8(32):eabq6147. DOI: 10.1126/sciadv.abq6147
6. Rocher L, Hendrickx JM, de Montjoye YA. Estimating the success of re-identifications in incomplete datasets using generative models. Nat Commun. 2019;10:3069. DOI: 10.1038/s41467-019-10933-3
7. Dwork C, McSherry F, Nissim K, Smith A. Calibrating noise to sensitivity in private data analysis. In: Theory of Cryptography. Lecture Notes in Computer Science. Springer; 2006:265-284. DOI: 10.1007/11681878_14
8. Sweeney L. k-anonymity: a model for protecting privacy. Int J Uncertain Fuzziness Knowl Based Syst. 2002;10(05):557-570. DOI: 10.1142/s0218488502001648
9. Rieke N, Hancox J, Li W, et al. The future of digital health with federated learning. NPJ Digit Med. 2020;3:119. DOI: 10.1038/s41746-020-00323-1
10. European Parliament and Council. Regulation (EU) 2016/679 (General Data Protection Regulation). Off J Eur Union. 2016;L119:1-88. https://eur-lex.europa.eu/eli/reg/2016/679/oj
11. US Department of Health and Human Services. Guidance regarding methods for de-identification of protected health information in accordance with the HIPAA Privacy Rule (45 CFR 164.514). 2012. https://www.hhs.gov/hipaa/for-professionals/special-topics/de-identification/index.html
12. Wachter S, Mittelstadt B, Floridi L. Why a right to explanation of automated decision-making does not exist in the General Data Protection Regulation. Int Data Priv Law. 2017;7(2):76-99. DOI: 10.1093/idpl/ipx005
13. Arab Republic of Egypt. Law No. 151 of 2020 promulgating the Personal Data Protection Law. Official Gazette; 2020. https://mcit.gov.eg/Upcont/Documents/Reports%20and%20Documents_1232021000_Law_No_151_2020_Personal_Data_Protection.pdf
