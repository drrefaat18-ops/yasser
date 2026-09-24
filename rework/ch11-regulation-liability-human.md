# Chapter 11: Regulation, Liability and the Human in the Loop

## Opening Case
Two weeks after her hospital stay, Amal is readmitted with a fever. The hospital's sepsis model gives her a "low risk" score. It is a busy night. A junior doctor sees the score, notes that her vital signs are "borderline" and plans to review her in the morning. By morning, Amal has septic shock and needs intensive care. She survives.

Her family asks hard questions. The model was approved and bought by the hospital. The doctor followed its score. The vendor says the tool is "decision support only". Who is responsible when care guided by AI goes wrong? Who checked the tool before it reached the ward? And why did a trained doctor accept a number that did not fit what she saw? This chapter answers these questions.

## Learning Objectives
By the end of this chapter you will be able to:
1. [LO1] Explain software as a medical device and risk-based classification.
2. [LO2] Distinguish FDA 510(k), De Novo, premarket approval and predetermined change control plans.
3. [LO3] Describe the EU AI Act's obligations for high-risk medical AI and how they relate to the MDR and IVDR.
4. [LO4] Apply the elements of negligence to an AI-assisted case and explain the learned intermediary doctrine correctly.
5. [LO5] Explain automation bias, de-skilling and the limits of explainable AI, and propose countermeasures.

## 11.1 When Software Is a Medical Device
Software that is intended to diagnose, prevent, monitor or treat disease can be a medical device, even without any hardware. This is called **software as a medical device** (SaMD). A retinal screening system, a sepsis prediction model and a dosing calculator can all be SaMD. A hospital rota app is not.

Regulators classify SaMD by risk. An international framework considers two questions [1]. How important is the software's information: does it treat or diagnose, drive clinical management, or only inform it? And how serious is the patient's condition: critical, serious or non-serious? Software that diagnoses a critical condition carries the highest risk and faces the strictest review.

> **Medical Background in 60 Seconds:** A **medical device** is any instrument, machine, implant or software used for a medical purpose, from a thermometer to an MRI scanner. Regulators check that its benefits outweigh its risks before it is sold, and keep monitoring it afterwards. **Septic shock** is the most severe stage of sepsis, when blood pressure stays dangerously low despite fluids, and drugs are needed to support it.

## 11.2 The United States: FDA Pathways
The US Food and Drug Administration (FDA) uses three main routes to market.

- **510(k) clearance.** The maker shows that the device is "substantially equivalent" to one already on the market, called a predicate. Most AI devices reach the market this way.
- **De Novo classification.** For new, low-to-moderate-risk devices with no predicate. The autonomous retinal screening system took this route (Chapter 6).
- **Premarket approval** (PMA). For high-risk devices. It requires the strongest evidence, usually clinical studies.

Clearance does not always mean strong evidence. An analysis of FDA-cleared AI devices found that most were evaluated only on retrospective data, and many at only one or two sites [15]. Approvals in the USA and Europe rose sharply between 2015 and 2020, often with limited public detail on the evidence [14].

AI models can be updated. A traditional approval covers one fixed version. The FDA now allows a **predetermined change control plan** (PCCP). The maker states in advance what changes it plans, how it will develop and test them, and how it will assess their impact. Changes made within an authorised plan do not need a new submission. The FDA issued final guidance on PCCPs for AI-enabled devices in December 2024 [2]. Earlier, the FDA and the UK and Canadian regulators agreed ten principles of **good machine learning practice**, covering data quality, testing, human factors and monitoring [3].

## 11.3 Europe: The MDR, IVDR and the AI Act
In the European Union, medical devices are regulated by the **Medical Device Regulation** (MDR) [5]. Laboratory tests, including software that analyses samples, fall under the **In Vitro Diagnostic Regulation** (IVDR) [6]. Most diagnostic or monitoring software is classed at least as moderate risk and needs review by an independent **notified body** before it can carry the CE mark.

The **EU AI Act** (Regulation 2024/1689) is the first broad law on AI [4]. It entered into force in August 2024 and applies in stages. AI systems that are medical devices needing notified-body review count as **high-risk AI**. Obligations for these systems are scheduled to apply from August 2027. They include:

- a risk-management system across the product's life;
- data governance, including checks for bias in training data;
- technical documentation and automatic logging of use;
- transparency and clear instructions for users;
- human oversight built into the design;
- accuracy, robustness and cybersecurity.

The AI Act adds to the MDR and IVDR; it does not replace them. Makers can cover both in one assessment.

The World Health Organization's guidance sets six principles for AI in health: protect autonomy, promote well-being and safety, ensure transparency, foster responsibility and accountability, ensure inclusiveness and equity, and promote AI that is responsive and sustainable [7].

> **Local Context:** In Egypt, medical devices are regulated by the **Egyptian Drug Authority**, established by Law No. 151 of 2019. The law's definition of a medical device includes software intended for diagnosis, prevention, monitoring or treatment [16]. AI tools used in Egyptian care therefore fall within device regulation, alongside the data-protection rules in Chapter 10.

![Figure 11.1 — Lifecycle governance for AI medical software](figures/orig-image24.png)
*Figure 11.1 — AI medical software moves from development and validation, through regulatory review, to deployment and post-market monitoring. Planned updates can be managed through a predetermined change control plan. Illustrative.*

## 11.4 Liability: Who Is Responsible?
**Negligence** is the legal basis of most malpractice claims. A patient must show four elements:

1. **Duty.** The professional owed the patient care.
2. **Breach.** The care fell below the accepted **standard of care**.
3. **Causation.** The breach caused the harm.
4. **Damages.** Real harm occurred.

AI complicates the second element. What is the standard of care when an AI tool is available? Legal scholars suggest that, today, clinicians are generally safest when they follow standard care [8]. Risk rises when a clinician follows an AI recommendation that departs from standard care and harm results. As AI becomes standard, the reverse may also become true: ignoring a well-validated tool could one day be a breach.

Responsibility is usually shared (Figure 11.2). The clinician is responsible for clinical judgment. The hospital is responsible for choosing, validating, training staff on and monitoring the tool. The maker is responsible for the product's design, testing and warnings.

![Figure 11.2 — Shared responsibility for AI-assisted care](figures/orig-image21.png)
*Figure 11.2 — Responsibility for AI-assisted care is shared between the licensed clinician, the developer or manufacturer, and the healthcare institution. Illustrative.*

The **learned intermediary doctrine** is often misunderstood. It comes from product-liability law for medicines and devices. A manufacturer usually meets its duty to warn about risks by warning the prescribing clinician, rather than each patient. The clinician, as a trained intermediary, then advises the patient. The doctrine limits the manufacturer's duty to warn patients directly. It is not a shield for clinicians, and it does not make the clinician automatically liable for every product defect.

## 11.5 The Human in the Loop
Amal's doctor was not careless by nature. She showed **automation bias** (Chapter 1). A systematic review found that automation bias is common, and that errors happen both when people follow a wrong suggestion and when they miss a problem because the system did not flag it [9]. Busy shifts, high trust in the system and low experience make it worse.

**De-skilling** is a longer-term risk. In a multicentre study of colonoscopy, doctors who had become used to AI support detected fewer precancerous growths when they later worked without it [10]. Skills that are not practised can fade.

Many people hope that **explainable AI** (XAI) will solve these problems. XAI methods, such as heatmaps, show which parts of an input influenced a model's output. But a heatmap shows where the model looked, not whether its reasoning was sound. Tests have shown that some heatmap methods produce similar maps even from models with random parameters [11]. Explanations can make people trust a wrong answer more [12]. For high-stakes decisions, some experts argue for models that are interpretable by design [13].

Countermeasures work at several levels:

- **Design.** Show uncertainty, not just a single score. Avoid labels like "low risk" that invite people to stop thinking.
- **Workflow.** Make the clinician record their own assessment before seeing the AI output, where possible.
- **Training.** Teach staff each tool's known failure modes and its PPV at the local threshold.
- **Culture.** Make it normal to override AI when the patient does not fit, and to report every mismatch.
- **Monitoring.** Track performance after deployment, because models drift as data change (Chapter 3).

## 11.6 Looking Ahead: Roles Change, Professions Remain
AI will change the daily work of every health profession. Physicians will spend less time on documentation and more on judgment. Pharmacists will manage smarter alerts and lead precision dosing. Physiotherapists will supervise home programmes with objective movement data. Laboratory, imaging and public-health professionals will run the quality systems that keep AI honest.

What AI cannot do is sit with a frightened patient, weigh values that data do not capture, or take responsibility. These remain human tasks, and they are the core of every health profession.

> **Through Four Lenses**
> - **Medicine:** Physicians remain responsible for clinical judgment. When a score conflicts with the examination, document the conflict, act on the patient's condition and report the case for review.
> - **Pharmacy:** Pharmacists should check whether a dosing or interaction tool is a regulated device, and whether it has been validated locally. Unregulated calculators used for patient decisions carry extra risk.
> - **Physical Therapy:** Physiotherapists using movement apps should know whether the app is a medical device or a wellness product. Wellness apps may not meet clinical standards for assessment.
> - **Health Sciences:** Laboratory and imaging professionals often run post-market monitoring in practice. Logging errors, drift and equipment changes provides the evidence regulators and institutions need.

> **Myth vs Evidence:** Myth: "If a tool is FDA-cleared, it has been proven in clinical trials." Evidence: Most AI devices are cleared through 510(k), and most cleared AI devices were evaluated on retrospective data only, often at few sites [15].

> **Safety Alert:** A "low risk" score never overrides your assessment of a patient who looks unwell. Act on the patient, record your reasoning and report the mismatch.

## Key Takeaways
- Software that diagnoses, monitors or treats can be a medical device, classified by risk.
- FDA routes include 510(k), De Novo and PMA; PCCPs allow planned updates to AI devices.
- The EU AI Act adds high-risk AI obligations to the MDR and IVDR, including human oversight and data governance.
- Liability is usually shared; the learned intermediary doctrine limits manufacturers' duty to warn patients directly and is not a clinician shield.
- Automation bias, de-skilling and over-trust in explanations are human risks that need design, training and culture to manage.

## Self-Assessment
**Q1.** Which of these is most likely to be software as a medical device? [LO1]
A) A hospital staff-rota app
B) Software that analyses ECGs to detect atrial fibrillation
C) A spreadsheet of canteen menus
D) A library catalogue

**Q2.** A company develops a new AI tool with no similar device on the US market. It carries low-to-moderate risk. Which FDA route fits best? [LO2]
A) 510(k) clearance
B) Premarket approval only
C) No review is needed
D) De Novo classification

**Q3.** What does a predetermined change control plan allow? [LO2]
A) Planned, pre-specified model updates without a new submission for each change
B) Unlimited changes without any testing
C) Skipping clinical validation for the first version
D) Selling the device without a label

**Q4.** Under the EU AI Act, how is an AI system that is a medical device needing notified-body review classified? [LO3]
A) Minimal-risk AI
B) Banned AI
C) High-risk AI
D) General-purpose AI only

**Q5.** Which is an obligation for high-risk AI under the EU AI Act? [LO3]
A) Human oversight built into the design
B) Removing all documentation
C) Using only unsupervised learning
D) Avoiding logging of use

**Q6.** A clinician follows an AI recommendation that departs from standard care, and the patient is harmed. According to legal scholars, how does this compare with following standard care? [LO4]
A) It lowers the clinician's legal risk.
B) It raises the clinician's legal risk.
C) It has no legal effect.
D) It transfers all responsibility to the patient.

**Q7.** What does the learned intermediary doctrine say? [LO4]
A) Clinicians are always liable for product defects.
B) AI developers can never be sued.
C) Patients must read all device manuals themselves.
D) A manufacturer usually meets its duty to warn by warning the prescribing clinician.

**Q8.** Amal's doctor accepted a "low risk" sepsis score despite borderline vital signs. What is this an example of? [LO5]
A) De-skilling
B) Differential privacy
C) Automation bias
D) Federated learning

**Q9.** A saliency heatmap highlights part of a chest X-ray. What can it reliably tell the clinician? [LO5]
A) That the model's reasoning is correct
B) Which image regions influenced the output, not whether the reasoning was valid
C) The patient's diagnosis
D) That the model is calibrated

**Q10.** Doctors who became used to AI in colonoscopy later detected fewer precancerous growths without it. What does this show? [LO5]
A) De-skilling
B) Data leakage
C) Distribution shift in the model
D) Better training

**Case Question.** Using the four elements of negligence, analyse Amal's case in the opening. Then suggest two changes the hospital could make to reduce the chance of the same event happening again.

## Answers and Rationales
**Q1. B** — ECG analysis for diagnosis has a medical purpose [1]. A, C and D do not.

**Q2. D** — De Novo is for new low-to-moderate-risk devices without a predicate. A needs a predicate. B is for high risk. C is wrong.

**Q3. A** — A PCCP pre-specifies changes and their testing [2]. B, C and D are false.

**Q4. C** — Medical-device AI needing notified-body review is high-risk under the AI Act [4]. A, B and D are wrong.

**Q5. A** — Human oversight is a core high-risk obligation [4]. B, C and D contradict the Act.

**Q6. B** — Following AI away from standard care into harm raises risk [8]. A, C and D are wrong.

**Q7. D** — The doctrine concerns the manufacturer's duty to warn through the clinician. A and B misstate it. C is the opposite.

**Q8. C** — Accepting an automated output despite conflicting evidence is automation bias [9]. A is long-term skill loss. B and D are privacy methods.

**Q9. B** — Heatmaps show influence, not correctness [11, 12]. A, C and D overstate them.

**Q10. A** — Skill declined after reliance on AI [10]. B, C and D are unrelated.

**Case Question — model answer.** Duty: the doctor and hospital owed Amal care. Breach: accepting a "low risk" score despite borderline signs, and delaying review, may fall below the standard of care, which requires assessing the patient. Causation: the delay plausibly contributed to septic shock. Damages: she needed intensive care. Responsibility may be shared: the hospital chose and deployed the tool, and should have trained staff on its limits. Two changes: display the model's uncertainty and remove the reassuring "low risk" label, and require a bedside review for any patient with abnormal vital signs regardless of the score.

## References
1. International Medical Device Regulators Forum. "Software as a Medical Device": possible framework for risk categorization and corresponding considerations. IMDRF/SaMD WG/N12FINAL. 2014. https://www.imdrf.org/documents/software-medical-device-possible-framework-risk-categorization-and-corresponding-considerations
2. US Food and Drug Administration. Marketing submission recommendations for a predetermined change control plan for artificial intelligence-enabled device software functions: final guidance. December 2024. https://www.fda.gov/regulatory-information/search-fda-guidance-documents/marketing-submission-recommendations-predetermined-change-control-plan-artificial-intelligence
3. US Food and Drug Administration, Health Canada, UK Medicines and Healthcare products Regulatory Agency. Good machine learning practice for medical device development: guiding principles. 2021. https://www.fda.gov/medical-devices/software-medical-device-samd/good-machine-learning-practice-medical-device-development-guiding-principles
4. European Parliament and Council. Regulation (EU) 2024/1689 laying down harmonised rules on artificial intelligence (Artificial Intelligence Act). Off J Eur Union. 2024. https://eur-lex.europa.eu/eli/reg/2024/1689/oj
5. European Parliament and Council. Regulation (EU) 2017/745 on medical devices. Off J Eur Union. 2017;L117:1-175. https://eur-lex.europa.eu/eli/reg/2017/745/oj
6. European Parliament and Council. Regulation (EU) 2017/746 on in vitro diagnostic medical devices. Off J Eur Union. 2017;L117:176-332. https://eur-lex.europa.eu/eli/reg/2017/746/oj
7. World Health Organization. Ethics and governance of artificial intelligence for health: WHO guidance. Geneva: WHO; 2021. https://www.who.int/publications/i/item/9789240029200
8. Price WN, Gerke S, Cohen IG. Potential liability for physicians using artificial intelligence. JAMA. 2019;322(18):1765-1766. DOI: 10.1001/jama.2019.15064
9. Goddard K, Roudsari A, Wyatt JC. Automation bias: a systematic review of frequency, effect mediators, and mitigators. J Am Med Inform Assoc. 2012;19(1):121-127. DOI: 10.1136/amiajnl-2011-000089
10. Budzyń K, Romańczyk M, Kitala D, et al. Endoscopist deskilling risk after exposure to artificial intelligence in colonoscopy: a multicentre, observational study. Lancet Gastroenterol Hepatol. 2025;10(10):896-903. DOI: 10.1016/S2468-1253(25)00133-5
11. Adebayo J, Gilmer J, Muelly M, et al. Sanity checks for saliency maps. In: Advances in Neural Information Processing Systems 31. 2018. https://arxiv.org/abs/1810.03292
12. Ghassemi M, Oakden-Rayner L, Beam AL. The false hope of current approaches to explainable artificial intelligence in health care. Lancet Digit Health. 2021;3(11):e745-e750. DOI: 10.1016/S2589-7500(21)00208-9
13. Rudin C. Stop explaining black box machine learning models for high stakes decisions and use interpretable models instead. Nat Mach Intell. 2019;1(5):206-215. DOI: 10.1038/s42256-019-0048-x
14. Muehlematter UJ, Daniore P, Vokinger KN. Approval of artificial intelligence and machine learning-based medical devices in the USA and Europe (2015-20): a comparative analysis. Lancet Digit Health. 2021;3(3):e195-e203. DOI: 10.1016/S2589-7500(20)30292-2
15. Wu E, Wu K, Daneshjou R, et al. How medical AI devices are evaluated: limitations and recommendations from an analysis of FDA approvals. Nat Med. 2021;27(4):582-584. DOI: 10.1038/s41591-021-01312-x
16. Arab Republic of Egypt. Law No. 151 of 2019 on the establishment of the Egyptian Drug Authority. Official Gazette No. 34 bis (A); 2019. https://www.eastlaws.com/legislation-full-text/en/egypt/law/25-08-2019/no-151?type=1&id=4747464
