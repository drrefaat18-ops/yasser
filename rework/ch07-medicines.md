# Chapter 7: Medicines — Discovery, Dosing and Safety

## Opening Case
Amal's knee has hurt for weeks. Her doctor prescribes ibuprofen, a painkiller. At the pharmacy, four alerts appear on screen at once. One says: "Ibuprofen + lisinopril + furosemide: risk of acute kidney injury". The others are minor warnings the pharmacist sees many times a day.

The pharmacist knows most alerts are ignored. She also knows Amal's kidney function is already low. She reads the kidney alert and calls the doctor. They agree on paracetamol and a physiotherapy referral instead.

One alert among many prevented harm. Why are so many alerts ignored, and where else is AI changing how medicines are found, dosed and watched?

## Learning Objectives
By the end of this chapter you will be able to:
1. [LO1] Describe how AI helps drug discovery, and its limits.
2. [LO2] Explain alert fatigue and how AI could make alerts more useful.
3. [LO3] Describe precision dosing using the example of vancomycin.
4. [LO4] Explain how AI supports pharmacovigilance and pharmacogenomics.
5. [LO5] Identify risks of using AI tools for drug information.

> **Medical Background in 60 Seconds:** A new medicine usually takes 10 to 15 years to develop. Scientists find a **drug target**, usually a protein linked to disease. They search for molecules that act on it. Then come tests in cells and animals, and three phases of human trials. After approval, safety is watched for as long as the drug is used. This is **pharmacovigilance**.

## 7.1 Discovery: Finding Targets and Molecules
**Protein shapes.** A protein's shape decides how a drug can bind to it. Finding a shape used to take months. AlphaFold predicts protein shapes from their building blocks, often almost as well as laboratory methods [1]. But a shape is not a drug. It shows where a molecule might bind, not whether it will be safe.

**Searching for molecules.** AI can screen huge libraries of molecules on a computer. One team screened over 100 million molecules and found halicin, which killed resistant bacteria in laboratory tests and mice [2].

**Designing molecules.** Generative AI can suggest brand-new molecules. One team designed and tested new candidates in cells and mice within weeks [3].

These are real gains in speed. But all these examples stopped at laboratory or animal stages. Most drug candidates fail in human trials. AI can speed up the early search; it cannot skip clinical testing.

## 7.2 Medication Alerts and Alert Fatigue
**Clinical decision support** (Chapter 1) is built into most prescribing and pharmacy systems. It checks for interactions, allergies, duplicates and doses that do not suit the kidneys.

The problem is volume. A review found that clinicians override 49% to 96% of drug-safety alerts [4]. Many alerts are about minor risks. When people see the same alert again and again, they stop reading it. This is **alert fatigue** [5].

In Chapter 4 terms, most alerts have a low PPV. Only a few lead to an important change. Machine learning can help. Instead of firing on every drug pair, a model learns which prescriptions, in which patients, are truly risky. In a French hospital, such a system gave more relevant alerts than the old rule-based one [6].

Amal's case shows why. Ibuprofen with lisinopril and furosemide can reduce blood flow to the kidneys. With her low kidney function, the risk is real. A good system would show this alert clearly and hide the trivial ones.

## 7.3 Precision Dosing
Some drugs have a narrow gap between a helpful and a toxic level. Vancomycin, an antibiotic for serious infections, is one.

**Model-informed precision dosing** (MIPD) uses a model of how the drug moves through the body. It starts with average values. With each new blood level, it updates its estimate for this patient. Then it suggests the dose most likely to hit the target. Current guidelines recommend this approach for vancomycin in serious infections [7].

MIPD is still used less than it could be. Barriers include software, training and testing in local patients [8].

## 7.4 Genes and Drug Safety
**Pharmacogenomics** studies how genes affect drug response. Some gene variants change how fast the liver breaks down a drug. Others raise the risk of severe reactions. For example, people with the gene variant HLA-B*57:01 are tested before receiving the HIV drug abacavir [9]. AI helps link gene results to prescribing systems, so a warning appears at the right moment.

**Pharmacovigilance** looks for harms that trials missed. Trials include thousands of people; after approval, millions take the drug. AI can scan reports and health records for possible signals, such as a drug linked to liver injury more often than expected [10].

A signal is a question, not an answer. It may be due to chance or to the disease the drug treats. Experts must review each one.

## 7.5 Chatbots and Drug Information
Chatbots are often used for drug questions (Chapter 5). They explain how drugs work quite well. But they can give wrong doses or miss interactions, in fluent language. Amal would have been harmed if a chatbot had said "ibuprofen is a safe painkiller". Always check doses and interactions in official product information or a trusted drug database.

> **Through Four Lenses**
> - **Medicine:** Doctors should not override kidney or bleeding alerts by habit. Reading the one alert that matters, as happened for Amal, is a core safety skill.
> - **Pharmacy:** Pharmacists are the last check before a medicine reaches the patient. They can help tune alerts, lead dosing services and report side effects to pharmacovigilance.
> - **Physical Therapy:** Physiotherapists see how medicines affect movement. Dizziness, falls or muscle pain after a new drug should be reported. Exercise can reduce the need for risky painkillers.
> - **Health Sciences:** Laboratory scientists provide the drug levels, kidney results and gene tests that dosing models use. Sample timing and units affect every dose calculation.

> **Myth vs Evidence:** Myth: "AI can now design drugs without long trials." Evidence: AI has sped up protein-shape prediction and molecule screening [1, 2]. Candidates still need animal studies and human trials, where most fail.

> **Safety Alert:** Never dismiss a kidney, bleeding or allergy alert without reading it. Check doses and interactions in trusted sources, not chatbots.

## Key Takeaways
- AI speeds up early drug discovery, but human trials remain essential.
- Most medication alerts are ignored because too many are low-value.
- Machine learning can make alerts fewer and more relevant.
- Precision dosing updates the dose with each blood level, as advised for vancomycin.
- AI safety signals are questions for experts, not proof of harm.

## Self-Assessment
**Q1.** AlphaFold predicts a protein's shape. What does this achieve for drug development? [LO1]
A) It proves a drug will be safe.
B) It replaces human trials.
C) It shows which patients will respond.
D) It helps show where a molecule might bind.

**Q2.** Clinicians override 90% of drug-interaction alerts. What is the most likely problem? [LO2]
A) Clinicians do not care about safety.
B) Many alerts are low-value, so people stop reading them.
C) The alerts use machine learning.
D) The alerts are too rare.

**Q3.** Amal takes lisinopril and furosemide and has low kidney function. She is prescribed ibuprofen. What is the main risk? [LO2]
A) Acute kidney injury
B) Low blood sugar
C) Liver failure
D) Loss of vision

**Q4.** How does precision dosing for vancomycin work? [LO3]
A) Every patient gets the same fixed dose.
B) A chatbot chooses the dose.
C) A drug model is combined with the patient's blood levels to suggest doses.
D) The drug is measured in urine only.

**Q5.** Why is updating the model with each blood level useful? [LO3]
A) It makes the estimate fit the individual patient better each time.
B) It removes the need for blood tests.
C) It guarantees no side effects.
D) It works only in children.

**Q6.** A system finds liver injury reported five times more often for Drug X. What is the right next step? [LO4]
A) Withdraw Drug X everywhere today.
B) Ignore the signal.
C) Conclude that Drug X causes liver injury.
D) Have experts review the signal for chance and other causes.

**Q7.** Before giving abacavir, a doctor orders an HLA-B*57:01 test. Which field is this? [LO4]
A) Radiology
B) Pharmacogenomics
C) Oculomics
D) Reinforcement learning

**Q8.** A relative says, "The chatbot said the dose is fine." What should the pharmacist do? [LO5]
A) Accept it
B) Double the dose to be safe
C) Check the dose in the product information or a trusted drug database
D) Ask the chatbot again

**Q9.** An AI alert system learns from past pharmacist reviews. What is its main aim compared with a rule-based system? [LO2]
A) To make a larger share of alerts truly relevant
B) To show every possible interaction
C) To remove pharmacists
D) To show alerts more often

**Q10.** A new AI-designed molecule works in mice. What can we conclude? [LO1]
A) It is ready for approval.
B) It will be safe in humans.
C) It is a candidate that still needs human trials, where many fail.
D) It needs no safety monitoring.

**Case Question.** You are the pharmacist in the opening case. Write a short message to the doctor explaining the risk and proposing another plan.

## Answers and Rationales
**Q1. D** — A shape shows possible binding sites [1]. A, B and C need other evidence.

**Q2. B** — Frequent low-value alerts cause fatigue [4, 5]. A blames people for a design problem. C and D are wrong.

**Q3. A** — This combination reduces kidney blood flow, and her kidneys are already weak. B, C and D are not the main risk.

**Q4. C** — Precision dosing combines a drug model with measured levels [7]. A is fixed dosing. B and D are wrong.

**Q5. A** — Each new level refines the estimate for this patient. B, C and D are false.

**Q6. D** — A signal needs expert review [10]. A and C act too early. B ignores possible harm.

**Q7. B** — Gene tests that guide drug choice are pharmacogenomics [9]. A, C and D are unrelated.

**Q8. C** — Doses must be checked in trusted sources. A and D are not checking. B is dangerous.

**Q9. A** — The aim is fewer, more relevant alerts [6]. B worsens fatigue. C and D are wrong.

**Q10. C** — Results in mice do not predict safety in humans. A, B and D are wrong.

**Case Question — model answer.** "Dear Doctor, Amal Hassan was prescribed ibuprofen while taking lisinopril and furosemide, and her eGFR is 52. This combination can cause acute kidney injury. I suggest paracetamol for her knee pain and a physiotherapy referral for exercise. Please let me know if you agree, and I will explain the change to her."

## References
1. Jumper J, Evans R, Pritzel A, et al. Highly accurate protein structure prediction with AlphaFold. Nature. 2021;596(7873):583-589. DOI: 10.1038/s41586-021-03819-2
2. Stokes JM, Yang K, Swanson K, et al. A deep learning approach to antibiotic discovery. Cell. 2020;180(4):688-702. DOI: 10.1016/j.cell.2020.01.021
3. Zhavoronkov A, Ivanenkov YA, Aliper A, et al. Deep learning enables rapid identification of potent DDR1 kinase inhibitors. Nat Biotechnol. 2019;37(9):1038-1040. DOI: 10.1038/s41587-019-0224-x
4. van der Sijs H, Aarts J, Vulto A, Berg M. Overriding of drug safety alerts in computerized physician order entry. J Am Med Inform Assoc. 2006;13(2):138-147. DOI: 10.1197/jamia.M1809
5. Ancker JS, Edwards A, Nosal S, et al. Effects of workload, work complexity, and repeated alerts on alert fatigue in a clinical decision support system. BMC Med Inform Decis Mak. 2017;17:36. DOI: 10.1186/s12911-017-0430-8
6. Corny J, Rajkumar A, Martin O, et al. A machine learning-based clinical decision support system to identify prescriptions with a high risk of medication error. J Am Med Inform Assoc. 2020;27(11):1688-1694. DOI: 10.1093/jamia/ocaa154
7. Rybak MJ, Le J, Lodise TP, et al. Therapeutic monitoring of vancomycin for serious methicillin-resistant Staphylococcus aureus infections: a revised consensus guideline and review. Am J Health Syst Pharm. 2020;77(11):835-864. DOI: 10.1093/ajhp/zxaa036
8. Darwich AS, Ogungbenro K, Vinks AA, et al. Why has model-informed precision dosing not yet become common clinical reality? Lessons from the past and a roadmap for the future. Clin Pharmacol Ther. 2017;101(5):646-656. DOI: 10.1002/cpt.659
9. Relling MV, Evans WE. Pharmacogenomics in the clinic. Nature. 2015;526(7573):343-350. DOI: 10.1038/nature15817
10. Harpaz R, DuMouchel W, Shah NH, et al. Novel data-mining methodologies for adverse drug event discovery and analysis. Clin Pharmacol Ther. 2012;91(6):1010-1021. DOI: 10.1038/clpt.2012.50
