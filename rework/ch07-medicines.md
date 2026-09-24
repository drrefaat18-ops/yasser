# Chapter 7: Medicines — Discovery, Dosing and Safety

## Opening Case
Amal's knee has been painful for weeks. Her family physician prescribes ibuprofen, an anti-inflammatory painkiller. At the community pharmacy, the dispensing system shows four alerts on her screen at once. One says "Ibuprofen + lisinopril + furosemide: risk of acute kidney injury". The others warn about minor issues the pharmacist sees dozens of times a day.

The pharmacist knows that most alerts are overridden. She also knows Amal's kidney function is already reduced, with an eGFR of 52. She stops, reads the kidney alert carefully and calls the physician. They agree on paracetamol and a physiotherapy referral instead.

A single alert among many prevented harm. Why do so many alerts get ignored, how could AI make them better, and where else is AI changing how medicines are discovered, dosed and monitored?

## Learning Objectives
By the end of this chapter you will be able to:
1. [LO1] Describe how AI contributes at different stages of drug discovery, and its limits.
2. [LO2] Explain alert fatigue and how machine learning could make medication alerts more useful.
3. [LO3] Describe model-informed precision dosing using the example of vancomycin.
4. [LO4] Explain how AI supports pharmacovigilance and pharmacogenomics.
5. [LO5] Identify risks of using AI tools for drug information.

> **Medical Background in 60 Seconds:** A new medicine usually takes 10 to 15 years to develop. Scientists first find a **drug target**, usually a protein involved in disease. They then search for molecules that act on it. Promising molecules are tested in cells and animals, then in human trials: phase I for safety, phase II for dose and early effect, and phase III for effectiveness in large groups. After approval, safety monitoring continues for as long as the drug is used. This last step is **pharmacovigilance**.

## 7.1 Discovery: Finding Targets and Molecules
**Protein structure.** A protein's shape decides how drugs can bind to it. For decades, finding a shape took months of laboratory work. AlphaFold predicts protein structures from their amino-acid sequence, often with accuracy close to experimental methods [1]. It has made structures available for almost every known protein.

A structure is not a drug. It shows where a molecule might bind. It does not show whether a molecule will be safe, reach the right tissue or help patients.

**Searching for molecules.** Deep-learning models can screen huge libraries of molecules on a computer. One team trained a model to predict antibacterial activity and screened more than 100 million molecules [2]. It found halicin, a compound that killed resistant bacteria in laboratory tests and in mice.

**Designing new molecules.** Generative models can propose molecules that have never been made. In one study, a generative model designed candidate inhibitors of a kinase target. The team synthesised and tested them in cells and mice within weeks [3].

These are real advances in speed. But all three examples stopped at laboratory or animal stages when they were published. Most drug candidates fail in human trials. AI can shorten the early search; it cannot skip clinical testing.

## 7.2 Medication Alerts and Alert Fatigue
**Clinical decision support** (Chapter 1) is built into most prescribing and dispensing systems. It checks for interactions, allergies, duplicate therapy and doses that do not suit kidney function.

The problem is volume. A systematic review found that clinicians overrode between 49% and 96% of drug-safety alerts [4]. Many alerts are about minor or theoretical risks. When people see the same alert again and again, they stop reading it. This is **alert fatigue**. A study in primary care found that clinicians were less likely to accept an alert the more often they had seen it before [5].

In Chapter 4 terms, most rule-based alerts have a low PPV. Only a small share lead to a change that matters. Experts have long advised that alerts should be fewer, faster and more specific [6].

Machine learning offers one route. Instead of firing on every drug pair, a model can learn which prescriptions, in which patients, are truly high-risk. In a French hospital, a machine-learning system trained on past pharmacist reviews identified prescriptions at high risk of medication error. Its alerts were more often relevant than those of the hospital's existing rule-based system [7].

Amal's case shows what matters. Ibuprofen with an ACE inhibitor (lisinopril) and a diuretic (furosemide) can reduce blood flow to the kidneys. With her existing kidney impairment, the risk is real. A good system would show that alert prominently and hide the trivial ones.

## 7.3 Precision Dosing
Many drugs have a narrow range between an effective and a toxic level. Vancomycin, an antibiotic for serious infections, is one. Its effect depends on the total drug exposure over 24 hours, measured as the **area under the concentration–time curve** (AUC).

Traditional dosing uses fixed doses and a single trough level. **Model-informed precision dosing** (MIPD) uses a pharmacokinetic model of how the drug moves through the body. The model starts with average patient values. As each blood level arrives, it updates its estimate for that patient, using Bayesian methods (Chapter 4). It then recommends the dose most likely to reach the target.

Current guidelines for serious MRSA infections recommend AUC-guided vancomycin dosing, preferably with Bayesian software [9]. MIPD is not new, but it is still used less than it could be. Barriers include software integration, staff training and validation of models in local patients [8].

Some newer dosing tools add machine learning to the pharmacokinetic model. They still need the same checks: tested in patients like yours, calibrated and supervised by a pharmacist.

## 7.4 Pharmacogenomics and Pharmacovigilance
**Pharmacogenomics** studies how genes affect drug response. Some variants change how quickly the liver breaks down a drug. Others raise the risk of severe reactions. For example, people carrying HLA-B*57:01 have a high risk of a dangerous reaction to the HIV drug abacavir, so testing is done before prescribing [10]. AI helps by linking genetic results to prescribing systems, so that a warning appears at the right moment.

**Pharmacovigilance** looks for harms that trials missed. Trials involve thousands of people; after approval, millions take the drug. Rare reactions appear only then. Sources include spontaneous reports from clinicians and patients, health records and even social media. Data-mining and natural language processing can scan these sources and flag possible signals, such as a drug reported with liver injury more often than expected [11].

A signal is a question, not an answer. Many signals are caused by chance, by confounding or by the disease the drug treats. Experts must review each one.

> **Deeper Dive:** A common signal method compares proportions. Suppose 2% of all reports in a database mention liver injury, but 10% of reports for Drug X do. The reporting ratio is 10 ÷ 2 = 5. A high ratio flags Drug X for review. It does not prove the drug causes liver injury. For example, Drug X might be used mainly by patients who already have liver disease.

## 7.5 Dispensing, Supply and Drug Information
Hospitals and pharmacies use automation for dispensing cabinets, robot packing and stock control. Forecasting models predict demand, which helps prevent shortages of critical medicines.

LLMs are increasingly used to answer drug questions (Chapter 5). They can explain mechanisms well. But they can state wrong doses, miss interactions or ignore kidney function, all in fluent language. Amal's case would have gone wrong if a chatbot had simply said "ibuprofen is a safe painkiller". Doses and interactions must always be checked against official product information or a trusted drug database.

> **Through Four Lenses**
> - **Medicine:** Physicians should not override kidney or bleeding alerts by habit. Reading the one alert that matters, as Amal's physician did after the pharmacist's call, is a core safety skill.
> - **Pharmacy:** Pharmacists sit at the final check before a medicine reaches the patient. They can help tune alerts, lead precision-dosing services and report adverse reactions that feed pharmacovigilance.
> - **Physical Therapy:** Physiotherapists see how medicines affect movement and pain. Dizziness, falls or muscle pain after a new drug should be reported. Non-drug pain options, such as exercise, reduce reliance on risky analgesics.
> - **Health Sciences:** Laboratory scientists provide the drug levels, kidney results and genetic tests that dosing models use. Timing of samples, units and assay changes affect every Bayesian dose calculation.

> **Myth vs Evidence:** Myth: "AI can now design drugs without the need for long trials." Evidence: AI has sped up target structure prediction and molecule screening [1, 2, 3]. Candidates still need animal studies and phased human trials, where most fail.

> **Safety Alert:** Never dismiss a kidney, bleeding or allergy alert without reading it, even when you see many alerts a day. Check doses and interactions against authoritative sources, not chatbots.

## Key Takeaways
- AI speeds up protein structure prediction, molecule screening and design, but clinical trials remain essential.
- Most rule-based medication alerts are overridden; low PPV causes alert fatigue.
- Machine learning can make alerts more specific by learning which prescriptions are truly high-risk.
- Model-informed precision dosing uses Bayesian updating with each drug level, as recommended for vancomycin.
- Pharmacovigilance signals from AI are questions for experts, not proof of harm.

## Self-Assessment
**Q1.** AlphaFold predicts a protein's structure with high accuracy. What does this achieve for drug development? [LO1]
A) It proves a drug will be safe.
B) It replaces phase III trials.
C) It shows which patients will respond.
D) It helps identify where a molecule might bind to the target.

**Q2.** A study reports that clinicians override 90% of drug-interaction alerts. What is the most likely underlying problem? [LO2]
A) Clinicians do not care about safety.
B) Many alerts are low-value, so their PPV is low and fatigue develops.
C) The alerts use machine learning.
D) The alerts are too rare.

**Q3.** Amal takes lisinopril and furosemide and has an eGFR of 52. She is prescribed ibuprofen. What is the main risk the pharmacist identifies? [LO2]
A) Acute kidney injury
B) Low blood sugar
C) Liver failure
D) Loss of vision

**Q4.** How does model-informed precision dosing for vancomycin work? [LO3]
A) It gives every patient the same fixed dose.
B) It uses a chatbot to choose the dose.
C) It combines a pharmacokinetic model with the patient's drug levels to update and recommend doses.
D) It measures vancomycin in urine only.

**Q5.** Why is Bayesian updating useful in precision dosing? [LO3]
A) It refines the estimate for the individual patient as each new blood level arrives.
B) It removes the need for blood levels.
C) It guarantees no side effects.
D) It works only for children.

**Q6.** A pharmacovigilance system finds that liver injury is reported five times more often for Drug X than for other drugs. What is the correct next step? [LO4]
A) Withdraw Drug X immediately from all markets.
B) Ignore the signal because reports are unreliable.
C) Conclude that Drug X causes liver injury.
D) Have experts review the signal, looking for chance, confounding and biological plausibility.

**Q7.** Before prescribing abacavir, a clinician orders an HLA-B*57:01 test. Which field does this belong to? [LO4]
A) Radiomics
B) Pharmacogenomics
C) Oculomics
D) Reinforcement learning

**Q8.** A patient's relative says, "The chatbot told me the dose is fine." What should the pharmacist do? [LO5]
A) Accept it, because chatbots are trained on medical texts
B) Double the dose to be safe
C) Check the dose against the product information or a trusted drug database
D) Ask the chatbot again

**Q9.** A machine-learning alert system learns from past pharmacist reviews which prescriptions were truly risky. Compared with a rule-based system, what is its main aim? [LO2]
A) To raise the proportion of alerts that are clinically relevant
B) To show every possible interaction
C) To remove pharmacists from review
D) To make alerts appear more often

**Q10.** A generative model designs a molecule that works in mice. What can be concluded? [LO1]
A) It is ready for approval.
B) It will be safe in humans.
C) It is a candidate that still needs human trials, where many candidates fail.
D) It does not need pharmacovigilance.

**Case Question.** You are the pharmacist in the opening case. Write a short message to the physician explaining the risk of the ibuprofen prescription for Amal and proposing an alternative plan.

## Answers and Rationales
**Q1. D** — A structure shows possible binding sites [1]. A, B and C need other evidence.

**Q2. B** — Frequent low-value alerts lower PPV and drive overrides [4, 5]. A blames people for a design problem. C and D are not the cause.

**Q3. A** — An NSAID with an ACE inhibitor and a diuretic reduces kidney blood flow, and her kidney function is already reduced. B, C and D are not the main risk.

**Q4. C** — MIPD combines a pharmacokinetic model with measured levels [8, 9]. A is traditional fixed dosing. B and D are wrong.

**Q5. A** — Each new level updates the patient-specific estimate. B, C and D are false.

**Q6. D** — A signal needs expert review before conclusions [11]. A and C act too early. B ignores a possible harm.

**Q7. B** — Genetic testing to guide drug choice is pharmacogenomics [10]. A, C and D are unrelated.

**Q8. C** — Dose advice must be checked against authoritative sources. A trusts fluent output. B is dangerous. D is not verification.

**Q9. A** — The aim is fewer, more relevant alerts [7]. B worsens fatigue. C is not the aim. D reverses the aim.

**Q10. C** — Animal results do not predict human safety or benefit. A, B and D are wrong.

**Case Question — model answer.** "Dear Doctor, Amal Hassan has been prescribed ibuprofen while taking lisinopril and furosemide, and her eGFR is 52. This combination can reduce kidney blood flow and cause acute kidney injury. I suggest paracetamol at a standard dose for her knee pain instead, with a physiotherapy referral for exercise-based management. If an anti-inflammatory is essential, a topical form for a short period with a kidney check would be safer. Please let me know if you agree, and I will explain the change to her."

## References
1. Jumper J, Evans R, Pritzel A, et al. Highly accurate protein structure prediction with AlphaFold. Nature. 2021;596(7873):583-589. DOI: 10.1038/s41586-021-03819-2
2. Stokes JM, Yang K, Swanson K, et al. A deep learning approach to antibiotic discovery. Cell. 2020;180(4):688-702. DOI: 10.1016/j.cell.2020.01.021
3. Zhavoronkov A, Ivanenkov YA, Aliper A, et al. Deep learning enables rapid identification of potent DDR1 kinase inhibitors. Nat Biotechnol. 2019;37(9):1038-1040. DOI: 10.1038/s41587-019-0224-x
4. van der Sijs H, Aarts J, Vulto A, Berg M. Overriding of drug safety alerts in computerized physician order entry. J Am Med Inform Assoc. 2006;13(2):138-147. DOI: 10.1197/jamia.M1809
5. Ancker JS, Edwards A, Nosal S, et al. Effects of workload, work complexity, and repeated alerts on alert fatigue in a clinical decision support system. BMC Med Inform Decis Mak. 2017;17:36. DOI: 10.1186/s12911-017-0430-8
6. Bates DW, Kuperman GJ, Wang S, et al. Ten commandments for effective clinical decision support: making the practice of evidence-based medicine a reality. J Am Med Inform Assoc. 2003;10(6):523-530. DOI: 10.1197/jamia.M1370
7. Corny J, Rajkumar A, Martin O, et al. A machine learning-based clinical decision support system to identify prescriptions with a high risk of medication error. J Am Med Inform Assoc. 2020;27(11):1688-1694. DOI: 10.1093/jamia/ocaa154
8. Darwich AS, Ogungbenro K, Vinks AA, et al. Why has model-informed precision dosing not yet become common clinical reality? Lessons from the past and a roadmap for the future. Clin Pharmacol Ther. 2017;101(5):646-656. DOI: 10.1002/cpt.659
9. Rybak MJ, Le J, Lodise TP, et al. Therapeutic monitoring of vancomycin for serious methicillin-resistant Staphylococcus aureus infections: a revised consensus guideline and review. Am J Health Syst Pharm. 2020;77(11):835-864. DOI: 10.1093/ajhp/zxaa036
10. Relling MV, Evans WE. Pharmacogenomics in the clinic. Nature. 2015;526(7573):343-350. DOI: 10.1038/nature15817
11. Harpaz R, DuMouchel W, Shah NH, et al. Novel data-mining methodologies for adverse drug event discovery and analysis. Clin Pharmacol Ther. 2012;91(6):1010-1021. DOI: 10.1038/clpt.2012.50
