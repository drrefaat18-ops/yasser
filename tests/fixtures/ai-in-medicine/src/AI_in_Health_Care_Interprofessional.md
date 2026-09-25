# Artificial Intelligence in Health Care: An Interprofessional Introduction

***Assistant Prof. Dr. Shereen Elsaid Elkholy***

![Cover — Artificial Intelligence in Health Care](rework/figures/cover.svg)

## Contents

- [Chapter 1: What AI Is — and Isn't](#chapter-1-what-ai-is--and-isnt)
- [Chapter 2: Health Data — What AI Learns From](#chapter-2-health-data--what-ai-learns-from)
- [Chapter 3: How Models Learn — and How They Fail](#chapter-3-how-models-learn--and-how-they-fail)
- [Chapter 4: Reading an AI Performance Claim](#chapter-4-reading-an-ai-performance-claim)
- [Chapter 5: Generative AI and Large Language Models](#chapter-5-generative-ai-and-large-language-models)
- [Chapter 6: Seeing Disease — Imaging, Laboratory and Pathology](#chapter-6-seeing-disease--imaging-laboratory-and-pathology)
- [Chapter 7: Medicines — Discovery, Dosing and Safety](#chapter-7-medicines--discovery-dosing-and-safety)
- [Chapter 8: AI in Motion — Rehabilitation, Wearables and Robotics](#chapter-8-ai-in-motion--rehabilitation-wearables-and-robotics)
- [Chapter 9: Monitoring, Prediction and Population Health](#chapter-9-monitoring-prediction-and-population-health)
- [Chapter 10: Bias, Fairness and Privacy](#chapter-10-bias-fairness-and-privacy)
- [Chapter 11: Regulation, Liability and the Human in the Loop](#chapter-11-regulation-liability-and-the-human-in-the-loop)
- [Glossary](#glossary)

## How to Use This Book

This book is for students of medicine, pharmacy, physical therapy and the health sciences. You do not need clinical experience. You do not need to write code. You need curiosity and a willingness to ask, "How do we know this works?"

The book has three parts.

- **Part I — Foundations (Chapters 1–5)** explains what AI is, how it learns from health data, how it fails, and how to judge a performance claim. Every student should read all of Part I.
- **Part II — AI Across the Care Pathway (Chapters 6–9)** shows AI at work: seeing disease, managing medicines, supporting movement and rehabilitation, and predicting deterioration.
- **Part III — Responsible AI (Chapters 10–11)** covers bias, privacy, regulation, liability and the human in the loop.

Every chapter is for every profession. Some chapters sit closer to your future work:

| Profession | Chapters to read most closely |
|---|---|
| Medicine | 6, 9, 11 |
| Pharmacy | 7, 9, 5 |
| Physical Therapy | 8, 6, 10 |
| Health Sciences (laboratory, imaging, nutrition, public health) | 2, 6, 9 |

## Boxes You Will Meet

- **Opening Case** — a patient story that raises the chapter's question.
- **Medical Background in 60 Seconds** — the clinical idea you need, in plain words.
- **Through Four Lenses** — what the chapter means for each of the four professions.
- **Myth vs Evidence** — a common belief, checked against research.
- **Safety Alert** — one point that protects patients.
- **Local Context** — how the topic applies in Egypt.

Numbers in square brackets, such as [3], point to the numbered references at the end of each chapter. Words in **bold** are defined in the Glossary.

## Meet the Patients

Three patients return throughout the book. Their details stay the same in every chapter.

**Mrs. Amal Hassan, 61.** Amal is a retired schoolteacher. She has type 2 diabetes and high blood pressure. She takes seven medicines every day. Her kidney function is mildly reduced (eGFR 52). She worries about losing her sight, like her mother did. She meets a family physician, a community pharmacist, a laboratory technologist and, later, a hospital team.

**Mr. Karim Adel, 34.** Karim is a construction worker and the main earner for his family. He twisted his left knee on site and tore a ligament. He needs to return to heavy physical work. He is worried about time off and about pain medicines. He meets an emergency physician, a radiographer, a pharmacist and a physiotherapist.

**Ms. Lina Osei, 20.** Lina is a biology student. She has dark skin (Fitzpatrick type V). A mole on her forearm has changed shape. She feels anxious about health and often searches online before she sees anyone. She meets a chatbot first, then a pharmacist, a dermatologist and a public-health team running a skin-cancer awareness campaign.

## Who Is in the Care Team

Each chapter's case shows a different professional making the key decision: a physician, a pharmacist, a physiotherapist, a laboratory or imaging technologist, or a public-health officer. AI supports each of them. It does not replace any of them.


---

# Chapter 1: What AI Is — and Isn't

## Opening Case
It is late at night. Lina Osei, a 20-year-old student, sees that a mole on her arm looks bigger. She opens a chatbot on her phone. She uploads a photo and asks, "Is this cancer?"

The reply comes in two seconds. It is calm and kind. It says the mole "shows some features of concern" and tells her to see a doctor.

The next morning, Lina shows the reply to a pharmacist. The pharmacist asks: "What looked at your photo, and how does it know?" This chapter answers that question.

## Learning Objectives
By the end of this chapter you will be able to:
1. [LO1] Distinguish artificial intelligence, machine learning, deep learning and generative AI.
2. [LO2] Contrast a rule-based system with a learned model.
3. [LO3] Describe three milestones in the history of AI in health care.
4. [LO4] Name one benefit and one risk of AI for each health profession.

## 1.1 Four Words You Will Hear Every Day
**Artificial intelligence** (AI) means computer systems that do tasks we link with human thinking. Examples are reading images, understanding language and making predictions.

**Machine learning** (ML) is one way to build AI. The computer is not given rules. It learns patterns from examples. The examples are called **training data**. The result is a **model**: a tool that turns an input into an output.

**Deep learning** is a type of machine learning. It uses a **neural network** with many layers. It works well with images, sound and text.

**Generative AI** makes new content, such as text or images. A **large language model** (LLM) is generative AI trained on huge amounts of text. Lina's chatbot is an LLM.

![Figure 1.1 — Nested fields of AI](rework/figures/orig-image2.png)
*Figure 1.1 — AI contains machine learning, which contains deep learning. Generative AI is built with deep learning.*

Think of the terms as boxes inside boxes (Figure 1.1). Every LLM uses deep learning. Not every AI system does.

## 1.2 Rules Versus Learning
Older health software used a **rule-based system**. A person writes every rule. For example: "If a patient takes warfarin and aspirin is added, show a bleeding warning." You can read the logic. But rules break when real life is messier than the rule.

A learned model works differently. It studies thousands of past prescriptions and what happened next. Then it gives a risk score for a new prescription. It can find patterns no one wrote down. It can also learn wrong or unfair patterns. And you cannot read its logic line by line.

Neither is always better. For many clinical predictions, simple statistics work as well as complex machine learning [1].

> **Medical Background in 60 Seconds:** **Clinical decision support** is software that gives a health professional advice at the moment of a decision. Examples are drug-interaction warnings, vaccine reminders and alerts for abnormal laboratory results. Some use rules. Some use machine learning.

## 1.3 A Short History
**1956 — the name.** A workshop at Dartmouth College in the United States named the field "artificial intelligence" [2]. Hopes were high. Progress was slow.

**1970s — expert systems.** MYCIN, at Stanford, used about 600 written rules to suggest antibiotics [3]. In tests, it did well. But it was never used in routine care. The lesson still matters: doing well in a study does not mean a tool will be used safely in practice.

**2012 — deep learning takes off.** A deep neural network won a big image-recognition contest [4]. Soon it was used in medicine. In 2016, a model graded diabetic eye disease from retinal photos with high accuracy [5].

**2018 — AI makes a decision.** The US Food and Drug Administration authorised an AI system that screens eye photos for diabetic eye disease without a specialist [6].

**2020s — generative AI.** From 2022, chatbots such as ChatGPT reached the public. Health workers now use them to draft notes and explain conditions [7].

## 1.4 What AI Can and Cannot Do
AI is good at narrow tasks with many examples. It can sort, detect, measure and predict. In a large Swedish breast-screening trial, AI help cut the reading work by 44%. It also found about 20% more cancers [8].

AI is weak at new situations. It has no common sense. A model trained in one hospital may fail in another. A chatbot can write a confident answer that is false. It cannot examine a patient or take responsibility.

In short, AI is a strong tool with a narrow view [9]. It works best as part of a team.

> **Through Four Lenses**
> - **Medicine:** Doctors meet AI in image reading and risk scores. The benefit is faster detection. The risk is trusting a score without checking the patient.
> - **Pharmacy:** Pharmacists meet AI in interaction checks and drug chatbots. The benefit is catching dangerous combinations. The risk is too many alerts and fluent wrong answers.
> - **Physical Therapy:** Physiotherapists meet AI in movement videos and wearables. The benefit is objective progress. The risk is a model trained on athletes misjudging older bodies.
> - **Health Sciences:** Laboratory and imaging staff meet AI in analysers and scanners. The benefit is speed and consistency. The risk is silent failure after equipment changes.

## 1.5 Three Risks to Watch
Three risks appear again and again in this book.

**Bias.** A model learns from past data. If some groups are missing, it may work worse for them (Chapter 10).

**Hallucination.** A chatbot predicts likely words. It does not check facts. It can invent a dose or a reference (Chapter 5).

**Automation bias.** People tend to accept a computer's answer, even when their own judgment disagrees (Chapter 11).

Lina's chatbot shows all three. It may have seen few photos of dark skin. It wrote fluent text, not a checked diagnosis. And its calm tone made her trust it.

> **Myth vs Evidence:** Myth: "AI will soon replace clinicians." Evidence: AI does well on narrow tasks, but people still make the final decisions. Even in the largest screening trial, radiologists made the final calls [8].

> **Safety Alert:** A chatbot's answer is not a diagnosis. A changing mole, a new symptom or a medicine question needs a qualified health professional.

## Key Takeaways
- AI is the broad idea. Machine learning learns from data. Deep learning uses layered networks. Generative AI makes new content.
- Rules are easy to read but break easily. Learned models are flexible but hard to inspect.
- Good study results do not guarantee safe use in practice.
- AI is strong at narrow tasks and weak outside what it learned.
- Bias, hallucination and automation bias affect every profession.

## Self-Assessment
**Q1.** A pharmacy system warns whenever warfarin and aspirin are prescribed together. A programmer wrote this rule by hand. What kind of system is it? [LO2]
A) A deep-learning model
B) A rule-based system
C) A large language model
D) A clustering model

**Q2.** Which statement about AI terms is correct? [LO1]
A) Machine learning includes AI as a subtype.
B) Every AI system uses a neural network.
C) Generative AI is unrelated to deep learning.
D) Deep learning is a type of machine learning.

**Q3.** MYCIN did well in tests but was never used in routine care. What is the lesson for today? [LO3]
A) Good study results do not guarantee safe real-world use.
B) Rule-based systems are always less accurate.
C) Computers cannot support antibiotic choice.
D) Expert systems were banned.

**Q4.** A clinic's knee app was trained only on young athletes. Karim is a 34-year-old builder with an injured knee. What is the main risk? [LO4]
A) The app invents a drug dose.
B) The pharmacy system leaks his data.
C) The app works poorly for people unlike its training data.
D) The app refuses to open.

**Q5.** A student says, "The chatbot checks medical facts before it answers." What is wrong? [LO1]
A) Chatbots cannot write text.
B) Chatbots predict likely words and do not check facts.
C) Chatbots only work with images.
D) Chatbots always refuse medical questions.

**Q6.** Why is 2018 called a turning point? [LO3]
A) An AI system that screens eye photos without a specialist was authorised in the United States.
B) The term "artificial intelligence" was first used.
C) ChatGPT reached the public.
D) MYCIN entered routine use.

**Q7.** In the Swedish breast-screening trial, what did AI help achieve? [LO4]
A) It replaced radiologists.
B) It found fewer cancers but saved time.
C) It halved the number of women screened.
D) It cut reading work by 44% and found more cancers.

**Q8.** What is one advantage of a learned model over a rule-based system? [LO2]
A) Its logic can be read line by line.
B) It never makes errors.
C) It can find patterns no one wrote down.
D) It needs no data.

**Q9.** A laboratory analyser's AI works well for months. Then the reagent supplier changes and errors rise without warning. What does this show? [LO4]
A) Silent failure when conditions change
B) Invented references
C) Automation bias in patients
D) A badly written rule

**Q10.** What helped deep learning take off around 2012? [LO3]
A) New laws requiring AI
B) Faster computer chips and large sets of labelled images
C) The invention of rules
D) The end of the Dartmouth workshop

**Case Question.** Lina shows you the chatbot's answer. In four sentences, tell her what made the answer, why it might be wrong for her, and what to do next.

## Answers and Rationales
**Q1. B** — A rule written by a person makes a rule-based system. A, C and D learn from data.

**Q2. D** — Deep learning sits inside machine learning. A reverses the order. B and C are false.

**Q3. A** — MYCIN failed for practical reasons, not poor accuracy. B, C and D are false.

**Q4. C** — A model can fail for people who differ from its training data. A, B and D are not the main risk.

**Q5. B** — Chatbots predict likely words; they do not check facts. A, C and D are false.

**Q6. A** — In 2018 the FDA authorised an eye-screening AI that works without a specialist [6]. B was 1956. C was 2022. D never happened.

**Q7. D** — Reading work fell by 44% and more cancers were found [8]. A, B and C are false.

**Q8. C** — Learned models find patterns in examples. A describes rules. B and D are false.

**Q9. A** — A change in inputs caused a silent drop in performance. B, C and D do not fit.

**Q10. B** — Better chips and large labelled image sets made deep learning practical [4]. A, C and D are wrong.

**Case Question — model answer.** The answer came from a chatbot that predicts likely words; it did not examine your skin. It may have learned mostly from light skin, so it may misjudge a mole on dark skin. Its calm tone can sound more certain than it is. Please have the mole checked by a doctor soon.

## References
1. Christodoulou E, Ma J, Collins GS, et al. A systematic review shows no performance benefit of machine learning over logistic regression for clinical prediction models. J Clin Epidemiol. 2019;110:12-22. DOI: 10.1016/j.jclinepi.2019.02.004
2. McCarthy J, Minsky ML, Rochester N, Shannon CE. A proposal for the Dartmouth summer research project on artificial intelligence. 1955. http://jmc.stanford.edu/articles/dartmouth/dartmouth.pdf
3. Shortliffe EH. Design considerations for MYCIN. In: Computer-Based Medical Consultations: MYCIN. Elsevier; 1976:63-78. DOI: 10.1016/b978-0-444-00179-5.50008-1
4. Krizhevsky A, Sutskever I, Hinton GE. ImageNet classification with deep convolutional neural networks. Commun ACM. 2017;60(6):84-90. DOI: 10.1145/3065386
5. Gulshan V, Peng L, Coram M, et al. Development and validation of a deep learning algorithm for detection of diabetic retinopathy in retinal fundus photographs. JAMA. 2016;316(22):2402-2410. DOI: 10.1001/jama.2016.17216
6. Abràmoff MD, Lavin PT, Birch M, et al. Pivotal trial of an autonomous AI-based diagnostic system for detection of diabetic retinopathy in primary care offices. NPJ Digit Med. 2018;1:39. DOI: 10.1038/s41746-018-0040-6
7. Thirunavukarasu AJ, Ting DSJ, Elangovan K, et al. Large language models in medicine. Nat Med. 2023;29(8):1930-1940. DOI: 10.1038/s41591-023-02448-8
8. Lång K, Josefsson V, Larsson AM, et al. Artificial intelligence-supported screen reading versus standard double reading in the Mammography Screening with Artificial Intelligence trial (MASAI): a clinical safety analysis of a randomised, controlled, non-inferiority, single-blinded, screening accuracy study. Lancet Oncol. 2023;24(8):936-944. DOI: 10.1016/s1470-2045(23)00298-x
9. Topol EJ. High-performance medicine: the convergence of human and artificial intelligence. Nat Med. 2019;25(1):44-56. DOI: 10.1038/s41591-018-0300-7


---

# Chapter 2: Health Data — What AI Learns From

## Opening Case
Amal Hassan, 61, has had type 2 diabetes for twelve years. Her story is spread across many computers. The clinic holds her blood pressure and diagnoses. The laboratory holds ten years of results. The pharmacy holds every refill of her seven medicines.

A laboratory technologist is asked to help build a model. It should predict which patients like Amal will lose kidney function. She opens the data. Some results are missing. The two clinics code diagnoses differently. The pharmacy uses a different patient number. What does a model learn from, and what can go wrong before learning starts?

## Learning Objectives
By the end of this chapter you will be able to:
1. [LO1] Classify health data into structured data, images, signals, text and omics.
2. [LO2] Explain what a label is and why labels contain errors.
3. [LO3] Identify common data-quality problems, such as missing data.
4. [LO4] Recognise the main data standards and famous datasets, and who they leave out.

## 2.1 Five Kinds of Health Data
**Structured data** fit into rows and columns. Examples are age, blood pressure, laboratory values, diagnosis codes and prescriptions.

*Images* include X-rays, scans, eye photos, skin photos and pathology slides. A video of a patient walking is also image data.

*Signals* are measurements over time. An ECG and a glucose monitor both produce signals.

*Text* is written language, such as clinic notes and discharge letters. Text is rich but messy.

**Omics** data describe molecules. Genomics reads DNA. Pharmacogenomics studies genes that change how a person handles a drug.

Images, signals and text are called **unstructured data**. They need more work before a model can use them. Image files also carry **metadata**, such as the scanner model and hospital name.

> **Medical Background in 60 Seconds:** An **electronic health record** (EHR) is the digital version of a patient's chart. Creatinine is a waste product cleared by the kidneys. When blood creatinine rises, kidney function is falling. Doctors use it to estimate eGFR. Amal's eGFR is 52, which is mildly low.

## 2.2 Labels: The Answers a Model Learns From
Most medical AI learns from examples with the right answer attached. That answer is called a **label**. For Amal's model, the label might be: "Did kidney function fall by 30% within two years? Yes or no."

Labels come from four main places:

- *Experts* mark each case. This is accurate but slow and costly.
- *Codes* entered for billing or records. Cheap, but often wrong or missing.
- *Outcomes* that happened later, such as death or admission.
- *Software* that reads reports and pulls out a label. Several famous chest X-ray datasets were labelled this way [1, 2].

Every source has errors. Wrong labels are called **label noise**. A model trained on noisy labels learns the noise too.

## 2.3 Data Quality: Problems Before Learning Starts
Health data are collected for care and billing, not for AI. This causes common problems.

**Missing data.** Many values are empty, and often for a reason. A test is ordered because a clinician is worried. One study found that *whether* a test was ordered predicted survival, often more than the result itself [3]. So a model may learn doctors' habits, not disease.

**Who gets tested.** People who cannot reach a clinic leave fewer records. Their disease may look rarer than it is.

**Different codes.** The same condition or drug may be recorded differently in different places.

**Linking errors.** Joining records wrongly could attach another patient's medicines to Amal.

**Change over time.** Laboratory methods and guidelines change. Old data may mean something different today.

## 2.4 Speaking the Same Language: Standards
Data from different systems can be combined only if they share rules. This is called **interoperability**.

| Standard | What it covers | Example |
|---|---|---|
| DICOM | Medical images | A CT scan sent to a viewing screen |
| HL7 FHIR | Sharing health records | An app requesting Amal's results |
| ICD | Diagnosis codes | E11 for type 2 diabetes |
| LOINC | Laboratory tests | A code for serum creatinine |
| ATC | Drug classes | A10BA02 for metformin |

You do not need to memorise these codes. But when an AI tool fails in a new place, a coding mismatch is a common reason.

## 2.5 Famous Datasets and Who They Leave Out
A few large public datasets trained much of today's medical AI.

- MIMIC-IV holds records of intensive-care and emergency patients from one Boston hospital [4]. MIMIC-CXR adds chest X-rays from the same hospital [5].
- CheXpert holds 224,316 chest X-rays from Stanford [1].
- The Cancer Genome Atlas (TCGA) links tumour genes, slides and outcomes [6].
- UK Biobank follows about half a million UK adults [7]. Its volunteers are healthier and less diverse than the general population [8].

These datasets are valuable. But most come from a few rich countries and large hospitals. A model built on them may not fit a clinic in Cairo or a rural area.

> **Through Four Lenses**
> - **Medicine:** Doctors write much of the record. Clear diagnoses become good labels. Vague or copied notes become label noise that future models learn.
> - **Pharmacy:** Pharmacists hold dispensing data. Refill gaps show missed doses that prescriptions hide. This makes pharmacy data very useful for prediction.
> - **Physical Therapy:** Physiotherapists record movement, pain and progress. Free-text notes are hard for models to use. Structured outcome measures make rehabilitation visible.
> - **Health Sciences:** Laboratory and imaging staff control how samples and images are made. Analyser and scanner changes explain many problems that later confuse models.

> **Myth vs Evidence:** Myth: "More data always means a better model." Evidence: Big datasets can still be biased or noisy. Test-ordering patterns alone predict outcomes, so a big dataset may teach doctors' habits, not disease [3].

> **Safety Alert:** Never copy patient data to a personal device or public website to "try" an AI tool. Health data are sensitive (Chapter 10).

## Key Takeaways
- Health data include structured data, images, signals, text and omics.
- Models learn from labels, and every label source has errors.
- Missing data are rarely random; who gets tested carries information.
- Standards such as DICOM, FHIR and ICD let systems share data.
- Famous datasets come from a few settings and may not fit yours.

## Self-Assessment
**Q1.** Amal's glucose monitor records a value every five minutes. What data type is this? [LO1]
A) Omics
B) Free text
C) Signal
D) Image

**Q2.** A pneumonia model's labels were taken by software reading X-ray reports. What is the main weakness? [LO2]
A) Some labels will be wrong because reports can be unclear or misread.
B) The labels will be perfect.
C) The labels cannot be stored.
D) The labels contain genomes.

**Q3.** Patients who had a blood culture are more likely to die than those who did not. What is the best explanation? [LO3]
A) Blood cultures cause death.
B) The laboratory made errors.
C) The dataset is too small.
D) Blood cultures are ordered when doctors already suspect serious illness.

**Q4.** Which standard is mainly for medical images? [LO4]
A) ICD
B) DICOM
C) ATC
D) LOINC

**Q5.** Amal collects a 30-day pack of metformin every 60 days. Which data show this, and what does it suggest? [LO1]
A) Dispensing data; missed doses
B) Genomic data; a gene variant
C) Imaging data; kidney damage
D) Laboratory data; an analyser error

**Q6.** A team trains a model on UK Biobank and wants to use it in Egypt. What is the main concern? [LO4]
A) UK Biobank cannot be read by computers.
B) UK Biobank contains only children.
C) Its participants differ in health, ethnicity and setting from Egyptian patients.
D) UK Biobank has no outcomes.

**Q7.** Half of the patients with kidney disease were never given a code. What will a model trained on these codes learn? [LO2]
A) A perfect definition of kidney disease
B) An incomplete picture, because the labels are wrong in a pattern
C) Nothing at all
D) Only kidney genetics

**Q8.** A physiotherapy clinic records knee movement only in free-text notes. Why does this limit AI? [LO3]
A) Free text is illegal.
B) Knee movement cannot be measured.
C) Physiotherapy data are never useful.
D) Models struggle with free text unless measures are also recorded in a structured way.

**Q9.** An X-ray model learns which hospital's scanner made each image, not the disease. What made this easy? [LO1]
A) The image metadata, such as scanner model and hospital
B) The prescription history
C) The diagnosis code
D) The drug class

**Q10.** What does interoperability mean? [LO4]
A) Keeping data on paper
B) Deleting old records
C) The ability of different systems to share and use data
D) Training AI without labels

**Case Question.** You are the technologist in the opening case. Name three data problems to check before the model is trained, with one sentence on why each matters.

## Answers and Rationales
**Q1. C** — Values over time form a signal. A is molecules. B is written language. D is pictures.

**Q2. A** — Report-reading software makes mistakes, and reports can be unclear [1]. B, C and D are false.

**Q3. D** — Tests are ordered for sicker patients, so the test itself carries information [3]. A confuses link with cause. B and C do not explain it.

**Q4. B** — DICOM is for images. A is diagnoses. C is drugs. D is laboratory tests.

**Q5. A** — Refill timing shows missed doses. B, C and D do not show refills.

**Q6. C** — UK Biobank volunteers are healthier and less diverse than many populations [8]. A, B and D are false.

**Q7. B** — Labels that are missing in a pattern teach an incomplete picture. A, C and D are false.

**Q8. D** — Structured measures make data usable. A, B and C are false.

**Q9. A** — Metadata can reveal the scanner and hospital. B, C and D are not in the image file.

**Q10. C** — Interoperability means systems can share and use data. A, B and D are unrelated.

**Case Question — model answer.** First, check missing values and why they are missing, because tests ordered only for worrying cases can mislead the model. Second, check that clinic, laboratory and pharmacy records are linked correctly, so no one gets another patient's data. Third, check whether laboratory methods changed over the years, because a new method could look like a change in kidney function.

## References
1. Irvin J, Rajpurkar P, Ko M, et al. CheXpert: a large chest radiograph dataset with uncertainty labels and expert comparison. Proc AAAI Conf Artif Intell. 2019;33(01):590-597. DOI: 10.1609/aaai.v33i01.3301590
2. Wang X, Peng Y, Lu L, et al. ChestX-ray8: hospital-scale chest X-ray database and benchmarks on weakly-supervised classification and localization of common thorax diseases. In: 2017 IEEE Conference on Computer Vision and Pattern Recognition (CVPR). 2017:3462-3471. DOI: 10.1109/cvpr.2017.369
3. Agniel D, Kohane IS, Weber GM. Biases in electronic health record data due to processes within the healthcare system: retrospective observational study. BMJ. 2018;361:k1479. DOI: 10.1136/bmj.k1479
4. Johnson AEW, Bulgarelli L, Shen L, et al. MIMIC-IV, a freely accessible electronic health record dataset. Sci Data. 2023;10:1. DOI: 10.1038/s41597-022-01899-x
5. Johnson AEW, Pollard TJ, Berkowitz SJ, et al. MIMIC-CXR, a de-identified publicly available database of chest radiographs with free-text reports. Sci Data. 2019;6:317. DOI: 10.1038/s41597-019-0322-0
6. Cancer Genome Atlas Research Network, Weinstein JN, Collisson EA, et al. The Cancer Genome Atlas Pan-Cancer analysis project. Nat Genet. 2013;45(10):1113-1120. DOI: 10.1038/ng.2764
7. Bycroft C, Freeman C, Petkova D, et al. The UK Biobank resource with deep phenotyping and genomic data. Nature. 2018;562(7726):203-209. DOI: 10.1038/s41586-018-0579-z
8. Fry A, Littlejohns TJ, Sudlow C, et al. Comparison of sociodemographic and health-related characteristics of UK Biobank participants with those of the general population. Am J Epidemiol. 2017;186(9):1026-1034. DOI: 10.1093/aje/kwx246


---

# Chapter 3: How Models Learn — and How They Fail

## Opening Case
Karim Adel, 34, is a builder. He twisted his left knee at work and felt a pop. At the physiotherapy clinic, an app studies a video of him doing a squat. It gives a "knee stability score" of 82 and says "low risk".

The physiotherapist is surprised. Karim's knee gives way when he turns. She reads the app's leaflet. The model was trained on videos of young athletes, filmed in a bright sports laboratory. Its accuracy was 94%.

Karim is older, heavier and in pain. He was filmed in a small, dark room. Why would a model with 94% accuracy fail for him?

## Learning Objectives
By the end of this chapter you will be able to:
1. [LO1] Distinguish supervised, unsupervised and reinforcement learning.
2. [LO2] Explain in plain words how a model is trained.
3. [LO3] Describe the purpose of training, validation and test sets.
4. [LO4] Distinguish overfitting, data leakage, shortcut learning and distribution shift.
5. [LO5] Explain class imbalance and why complex models are not always better.

## 3.1 Three Ways to Learn
**Supervised learning** uses labelled examples (Chapter 2). The model sees an input and the right answer many times. Example: X-rays labelled "fracture" or "no fracture".

**Unsupervised learning** has no labels. The model finds groups by itself. A clinic might discover three recovery patterns after knee surgery.

**Reinforcement learning** learns by trial and reward. Researchers have tested it to suggest drug doses in intensive care [1]. It is still experimental.

## 3.2 How Training Works
A model holds millions of adjustable numbers called **parameter**s. At the start they are random, so the model guesses badly.

Training repeats three steps:

1. The model makes a guess.
2. A **loss function** measures how wrong the guess was.
3. The numbers are adjusted a little to reduce the error.

After millions of small steps, the model fits the training data well. This method is called **gradient descent**. Picture a walker in fog, always stepping downhill.

A **convolutional neural network** (CNN) is the classic model for images. Early layers see edges. Later layers see shapes, such as a bone or a mole's border.

## 3.3 Splitting the Data
A model always looks good on the data it trained on. The real question is how it does on new patients. So the data are split into three sets (Figure 3.1).

- The **training set** teaches the model.
- The **validation set** helps tune the design and decide when to stop.
- The **test set** is kept locked and used once, at the end.

![Figure 3.1 — Training, validation and test sets](rework/figures/split-leakage.svg)
*Figure 3.1 — The test set must stay unseen. Leakage happens when test information reaches training.*

Testing on part of the same dataset is **internal validation**. Testing on data from another hospital or time is **external validation**. External validation tells you much more.

## 3.4 Four Ways Models Fail
**Overfitting.** The model memorises the training data instead of learning general patterns. It is like a student who memorises last year's answers. It does well in training and badly on new data.

**Data leakage.** Information that would not exist in real use slips into training or testing [2]. The model then looks better than it is. Two common examples:

- *Same patient in both sets.* The model recognises the patient, not the disease.
- *Information from the future.* A sepsis model that uses "antibiotics started" is reading the doctor's decision.

**Shortcut learning.** The model finds an easy clue that has nothing to do with the disease [3]. One pneumonia model learned features of the hospital and the X-ray machine [4]. It failed at other hospitals.

**Distribution shift.** The world changes after training. New scanners, new patients or new habits make today's data different [5]. Karim's case is a shift: older age, a different body, pain and poor light.

> **Medical Background in 60 Seconds:** The **anterior cruciate ligament** (ACL) is a strong band inside the knee. It stops the shin bone sliding forward and helps the knee resist twisting. It often tears during a sudden turn. Patients feel a "pop" and later say the knee "gives way".

## 3.5 Rare Conditions and Simple Models
Many conditions are rare. Only a few mammograms in a thousand show cancer. This is called **class imbalance**. A model can be 99% accurate by always saying "no cancer". That model is useless. Chapter 4 shows better measures.

More complex is not always better. A review of 71 studies compared machine learning with simple statistics [6]. In good studies, machine learning had no average advantage. For tables of numbers, such as vital signs, simple models often work as well. Deep learning is strongest with images, signals and text.

> **Through Four Lenses**
> - **Medicine:** Doctors should ask where a model was trained and tested. A model tested in one teaching hospital may fail in a district clinic.
> - **Pharmacy:** Pharmacists should watch for future leakage. A model that uses "drug stopped" or "antidote given" is reading the response, not predicting the event.
> - **Physical Therapy:** Physiotherapists should compare the training group with their own patients. Age, body size, pain and lighting can all cause shift.
> - **Health Sciences:** Technologists should report changes in analysers, reagents and scanners. These changes shift data silently and can mislead a model.

> **Myth vs Evidence:** Myth: "Machine learning always beats traditional statistics." Evidence: Across 71 clinical studies, machine learning showed no average benefit over simple statistics [6].

> **Safety Alert:** When an AI result does not match the patient in front of you, trust the patient. Record the mismatch and report it.

## Key Takeaways
- Supervised learning uses labels. Unsupervised learning finds groups. Reinforcement learning learns from rewards.
- Training adjusts the model step by step to reduce its errors.
- Only an unseen test set, ideally from another site, shows real performance.
- Overfitting, leakage, shortcuts and shift make good-looking models fail.
- With rare conditions, accuracy misleads, and simple models are often enough.

## Self-Assessment
**Q1.** A hospital groups diabetes patients by glucose patterns, without labels. What type of learning is this? [LO1]
A) Supervised learning
B) Reinforcement learning
C) Transfer learning
D) Unsupervised learning

**Q2.** What does the loss function do during training? [LO2]
A) It deletes patient records.
B) It measures how wrong the model's guesses are.
C) It picks patients for the test set.
D) It explains the model to doctors.

**Q3.** A team uses its test set again and again to choose a design. What is the problem? [LO3]
A) The test set no longer gives a fair estimate for new patients.
B) The model trains faster.
C) The validation set gets too big.
D) There is no problem.

**Q4.** Karim's knee app did well on athletes in a laboratory but fails in a small clinic. What best explains this? [LO4]
A) Future leakage
B) A deliberate attack
C) Distribution shift
D) Reinforcement learning

**Q5.** Photos of the same patients appear in both training and test sets. What is the likely effect? [LO4]
A) Performance will look worse than it is.
B) The model becomes unsupervised.
C) Class imbalance disappears.
D) Performance will look better than it is.

**Q6.** A pneumonia model learned features of the X-ray machine and failed at other hospitals. What is this called? [LO4]
A) Shortcut learning
B) Underfitting
C) Gradient descent
D) Calibration

**Q7.** Cancer is present in 3 of every 1,000 images. A model says "no cancer" for all of them. What is its accuracy, and is it useful? [LO5]
A) 3%; useful
B) 50%; not useful
C) 99.7%; not useful
D) 100%; useful

**Q8.** A sepsis model uses "IV antibiotics started" as an input. Why is this a concern? [LO4]
A) Antibiotics are never recorded.
B) It is future leakage: the input shows the doctor already suspects sepsis.
C) It makes the model unsupervised.
D) It is a deliberate attack.

**Q9.** A team compares simple statistics with complex machine learning to predict readmission from 20 laboratory values. What is the most likely result? [LO5]
A) Similar performance, with the simple model easier to check
B) Machine learning wins by far
C) Simple statistics cannot use laboratory values
D) Neither can be tested

**Q10.** What is the validation set for? [LO3]
A) To replace the test set
B) To tune the design and decide when to stop training
C) To store the model
D) To collect new patients

**Case Question.** Karim's physiotherapist wants to explain the problem to her manager. Write four sentences using at least two terms from this chapter, and suggest one test before the app is used again.

## Answers and Rationales
**Q1. D** — Finding groups without labels is unsupervised learning. A needs labels. B needs rewards. C reuses another model.

**Q2. B** — The loss function measures error, which training reduces. A, C and D are not its job.

**Q3. A** — Using the test set many times makes its result too optimistic. B and C are unrelated. D is wrong.

**Q4. C** — Karim and the room differ from the training data. A, B and D do not fit.

**Q5. D** — The model recognises the same patients, so results look too good [2]. A reverses it. B and C are unrelated.

**Q6. A** — The model used a clue linked to the hospital, not the disease [4]. B, C and D do not fit.

**Q7. C** — It is right 997 times in 1,000 but misses every cancer. A, B and D are wrong.

**Q8. B** — Starting antibiotics shows the doctor already suspects sepsis. A, C and D are wrong.

**Q9. A** — For tables of numbers, machine learning has no average advantage [6]. B overstates. C and D are false.

**Q10. B** — The validation set guides tuning; the test set stays unseen. A, C and D are wrong.

**Case Question — model answer.** The app was trained on young athletes in a bright laboratory, but Karim is older, injured and was filmed in a dark room. This is distribution shift, so the 94% accuracy does not apply to him. The app may also use shortcuts, such as lighting. Its result disagreed with the clinical finding that his knee gives way. Before using it again, the clinic should test it on its own patients against a physiotherapist's assessment.

## References
1. Komorowski M, Celi LA, Badawi O, et al. The Artificial Intelligence Clinician learns optimal treatment strategies for sepsis in intensive care. Nat Med. 2018;24(11):1716-1720. DOI: 10.1038/s41591-018-0213-5
2. Kapoor S, Narayanan A. Leakage and the reproducibility crisis in machine-learning-based science. Patterns. 2023;4(9):100804. DOI: 10.1016/j.patter.2023.100804
3. Geirhos R, Jacobsen JH, Michaelis C, et al. Shortcut learning in deep neural networks. Nat Mach Intell. 2020;2(11):665-673. DOI: 10.1038/s42256-020-00257-z
4. Zech JR, Badgeley MA, Liu M, et al. Variable generalization performance of a deep learning model to detect pneumonia in chest radiographs: a cross-sectional study. PLoS Med. 2018;15(11):e1002683. DOI: 10.1371/journal.pmed.1002683
5. Finlayson SG, Subbaswamy A, Singh K, et al. The clinician and dataset shift in artificial intelligence. N Engl J Med. 2021;385(3):283-286. DOI: 10.1056/nejmc2104626
6. Christodoulou E, Ma J, Collins GS, et al. A systematic review shows no performance benefit of machine learning over logistic regression for clinical prediction models. J Clin Epidemiol. 2019;110:12-22. DOI: 10.1016/j.jclinepi.2019.02.004


---

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

![Figure 4.1 — How prevalence changes PPV](rework/figures/confusion-ppv.svg)
*Figure 4.1 — The same test gives a PPV of 8.7% when the disease is rare and 68% when it is common.*

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


---

# Chapter 5: Generative AI and Large Language Models

## Opening Case
Lina is waiting for her skin appointment. She is anxious. She asks a free chatbot: "I'm 20, my mole changed, and I have headaches. Has my cancer spread?" The chatbot gives a long, warm answer. It says melanoma "can spread to the brain". It suggests two supplements and cites a journal article.

Lina shows the answer to a pharmacist. The pharmacist checks the article. It does not exist. One supplement weakens the contraceptive pill Lina takes.

That afternoon, the same pharmacist uses an approved hospital chatbot to draft a leaflet on sun protection. It saves her an hour. She checks every sentence before printing. Why was the tool harmful in one case and helpful in the other?

## Learning Objectives
By the end of this chapter you will be able to:
1. [LO1] Explain next-token prediction and why it causes hallucinations.
2. [LO2] Identify safe and unsafe uses of chatbots in health care.
3. [LO3] Apply a safe-use checklist, including protecting patient data.
4. [LO4] Describe retrieval-augmented generation and ambient scribes.
5. [LO5] Judge a chatbot answer for accuracy, gaps and bias.

## 5.1 How a Large Language Model Works
A **large language model** (LLM) has one basic job: predict the next piece of text. Text is split into small pieces called **token**s. A token is a word or part of a word.

During training, the model reads billions of sentences. Again and again, it guesses the next token and corrects itself (Chapter 3). The design behind modern LLMs is called the **transformer** [1].

When you ask a question, the model writes the answer one token at a time (Figure 5.1). Each token is the one that seems most likely to come next.

![Figure 5.1 — Next-token prediction](rework/figures/next-token.svg)
*Figure 5.1 — An LLM writes by choosing a likely next token, again and again. It predicts likely text; it does not look up facts.*

## 5.2 Why Chatbots Make Things Up
An LLM predicts what text usually looks like. It does not check whether the text is true. When it does not know, it still writes fluent, confident text. This is called a **hallucination** [2].

Hallucinations are dangerous because they look exactly like correct answers. In one study, a chatbot wrote medical articles with references. Only 7% of the references were both real and correct [3]. The article cited to Lina was one of the fake ones.

Chatbots also copy problems from their training text. In one study, four major chatbots repeated some old, disproved race-based medical ideas [4].

## 5.3 Exam Scores Are Not Patient Safety
Chatbots have passed medical exam questions. Google's Med-PaLM 2 scored 86.5% on exam-style questions [5].

This shows strong medical knowledge. It does not show safety with real patients. Exam questions are tidy and have one right answer. Real patients bring missing facts, mixed symptoms and fear. An exam does not test whether a chatbot notices what is missing or spots an emergency.

> **Medical Background in 60 Seconds:** A **drug interaction** happens when one medicine, food or supplement changes the effect of another. Some supplements, such as St John's wort, make hormonal contraceptives less effective. Pharmacists check for interactions whenever a new product is added.

## 5.4 Useful Applications
**Writing notes.** An **ambient scribe** listens, with consent, to a consultation and drafts the note. In one large health system, doctors using scribes reported less time on paperwork and more attention to patients [6]. The clinician must still check and sign every note.

**Answering patients.** In one study, health professionals preferred chatbot replies to doctors' replies to online questions [7]. But the questions came from a public forum, not real care.

**Teaching.** Chatbots can explain a concept or write practice questions. They are good tutors. They are poor sources for doses and interactions unless linked to a trusted source.

**Answering from trusted sources.** In **retrieval-augmented generation** (RAG), the system first searches trusted documents, such as a hospital drug list or national guideline. Then the chatbot answers from those pages and shows its sources [8]. This reduces mistakes but does not remove them.

## 5.5 Using Chatbots Safely: A Checklist
1. **Protect patient data.** Never paste names, record numbers, photos or other identifying details into a public chatbot.
2. **Use it for drafts, not decisions.** A draft is a starting point you check.
3. **Check every fact.** Use a trusted source, such as the product leaflet or a guideline.
4. **Check every reference.** If you cannot find it, it may not exist.
5. **Look for gaps.** Did it consider pregnancy, kidney function or other medicines?
6. **You stay responsible.** The chatbot does not take your responsibility away.

For students, **academic integrity** matters. Using a chatbot to explain an idea is usually allowed. Handing in its text as your own work is not. The World Health Organization has published guidance on safe use of these tools in health [9].

> **Through Four Lenses**
> - **Medicine:** Doctors can use approved scribes to save time. They must read every draft, because a wrong finding becomes part of the legal record once signed.
> - **Pharmacy:** Pharmacists will meet patients with chatbot advice. They should check doses and interactions, and explain calmly why a fluent answer can be wrong.
> - **Physical Therapy:** Physiotherapists can use chatbots to draft home-exercise sheets. They must check each exercise, because the chatbot does not know the patient's injury.
> - **Health Sciences:** Public-health officers can draft health messages in several languages. They should test messages with the community, because chatbots may miss local meaning.

> **Myth vs Evidence:** Myth: "If a chatbot passes a medical exam, it is safe to advise patients." Evidence: Exam scores show knowledge on tidy questions [5]. The same tools can invent references [3] and repeat harmful race-based ideas [4].

> **Safety Alert:** Never enter identifying patient details into a public chatbot. Never act on a chatbot's dose or interaction advice without checking a trusted source.

## Key Takeaways
- Chatbots predict the next token; they write likely text, not checked facts.
- Hallucinations are fluent and confident, including fake references.
- High exam scores do not prove safety with real patients.
- Scribes, patient replies and RAG are useful when a professional checks the output.
- Protect patient data, check facts, and keep responsibility.

## Self-Assessment
**Q1.** What is a large language model mainly trained to do? [LO1]
A) Look up facts in a medical database
B) Predict the next token of text
C) Examine patients through a camera
D) Calculate doses from blood tests

**Q2.** A chatbot gives a student a reference to a paper that does not exist. What is the best explanation? [LO1]
A) The paper was withdrawn.
B) The internet failed.
C) Hackers attacked the chatbot.
D) The chatbot wrote likely-looking text without checking the paper exists.

**Q3.** A nurse wants to paste a patient's name, record number and discharge letter into a free public chatbot. What should a colleague say? [LO3]
A) Do not paste identifying data into a public tool; use an approved system.
B) It is fine if the summary is checked.
C) It is fine because chatbots delete everything.
D) It is fine if the patient has gone home.

**Q4.** A hospital links a chatbot to its own drug list so answers quote the list. What is this called? [LO4]
A) Reinforcement learning
B) Adversarial training
C) Retrieval-augmented generation
D) Clustering

**Q5.** Med-PaLM 2 scored 86.5% on exam-style questions. What is the best conclusion? [LO2]
A) It can replace doctors.
B) It has strong medical knowledge, but safety with real patients is not proven.
C) It is right 86.5% of the time for any patient.
D) It no longer makes things up.

**Q6.** A chatbot tells Lina that a herbal supplement is safe with her pill. What should the pharmacist do? [LO5]
A) Accept the answer
B) Tell Lina to stop the pill
C) Ask the chatbot again until it says no
D) Check the interaction in a trusted source and advise Lina

**Q7.** A scribe's draft says "normal abdominal examination", but the doctor did not examine the abdomen. What is the lesson? [LO2]
A) The clinician must check and correct every draft before signing.
B) Scribes should record without consent.
C) Scribes are always right about examinations.
D) The note can be signed because the scribe is approved.

**Q8.** Researchers asked four chatbots about old race-based formulas. What did they find? [LO5]
A) All refused to answer.
B) All gave current, fair answers.
C) The chatbots repeated some disproved race-based claims.
D) The chatbots asked for consent.

**Q9.** Which use by a physiotherapy student fits the checklist? [LO3]
A) Asking it to explain how a muscle contracts, then checking a textbook
B) Handing in its essay as their own
C) Asking it to set a patient's exercise dose without an assessment
D) Uploading a patient's video to a public chatbot

**Q10.** Health professionals preferred chatbot replies to doctors' replies in one study. What limit matters most? [LO5]
A) The chatbot was not a transformer.
B) Only patients rated the replies.
C) The questions came from an online forum, and the study judged writing, not patient outcomes.
D) Only pharmacists took part.

**Case Question.** Rewrite the chatbot's reply to Lina in four or five sentences. It should respect her worry, avoid a diagnosis, name any emergency signs and send her to the right professional.

## Answers and Rationales
**Q1. B** — Chatbots are trained to predict the next token. A, C and D are not what they do.

**Q2. D** — A fake reference is a hallucination [3]. A, B and C are unlikely.

**Q3. A** — Identifying data must not go into public tools. B, C and D all expose patient data.

**Q4. C** — Answering from trusted documents is RAG [8]. A, B and D are different methods.

**Q5. B** — Exam scores show knowledge, not safety [5]. A overreaches. C misreads the number. D is false.

**Q6. D** — Interactions must be checked in a trusted source. A trusts fluent text. B is unsafe. C is not checking.

**Q7. A** — The clinician is responsible for the signed note [6]. B is unethical. C and D are false.

**Q8. C** — The chatbots repeated some harmful race-based claims [4]. A, B and D are wrong.

**Q9. A** — Explaining a concept and then checking it is safe. B breaks academic rules. C and D are unsafe.

**Q10. C** — The setting and what was measured limit the result [7]. A, B and D are wrong.

**Case Question — model answer.** "I can hear you are worried, and it is right to check a changing mole. I cannot tell you if you have cancer; only an examination can. Headaches have many common causes, but a sudden severe headache, weakness or confusion needs emergency care now. Please keep your skin appointment. Ask a pharmacist before taking any supplement, because some weaken the pill."

## References
1. Vaswani A, Shazeer N, Parmar N, et al. Attention is all you need. In: Advances in Neural Information Processing Systems 30. 2017. https://arxiv.org/abs/1706.03762
2. Ji Z, Lee N, Frieske R, et al. Survey of hallucination in natural language generation. ACM Comput Surv. 2023;55(12):1-38. DOI: 10.1145/3571730
3. Bhattacharyya M, Miller VM, Bhattacharyya D, Miller LE. High rates of fabricated and inaccurate references in ChatGPT-generated medical content. Cureus. 2023;15(5):e39238. DOI: 10.7759/cureus.39238
4. Omiye JA, Lester JC, Spichak S, Rotemberg V, Daneshjou R. Large language models propagate race-based medicine. NPJ Digit Med. 2023;6:195. DOI: 10.1038/s41746-023-00939-z
5. Singhal K, Tu T, Gottweis J, et al. Toward expert-level medical question answering with large language models. Nat Med. 2025;31(3):943-950. DOI: 10.1038/s41591-024-03423-7
6. Tierney AA, Gayre G, Hoberman B, et al. Ambient artificial intelligence scribes to alleviate the burden of clinical documentation. NEJM Catal Innov Care Deliv. 2024;5(3). DOI: 10.1056/cat.23.0404
7. Ayers JW, Poliak A, Dredze M, et al. Comparing physician and artificial intelligence chatbot responses to patient questions posted to a public social media forum. JAMA Intern Med. 2023;183(6):589-596. DOI: 10.1001/jamainternmed.2023.1838
8. Lewis P, Perez E, Piktus A, et al. Retrieval-augmented generation for knowledge-intensive NLP tasks. In: Advances in Neural Information Processing Systems 33. 2020. https://arxiv.org/abs/2005.11401
9. World Health Organization. Ethics and governance of artificial intelligence for health: guidance on large multi-modal models. Geneva: WHO; 2024. https://www.who.int/publications/i/item/9789240084759


---

# Chapter 6: Seeing Disease — Imaging, Laboratory and Pathology

## Opening Case
Amal visits her family clinic for her yearly diabetes check. An assistant takes photos of the back of each eye. There is no eye specialist in the clinic. Within a minute, an AI system reports: "Diabetic eye disease detected. Refer to an eye specialist." Amal's hands shake. Her mother went blind from diabetes.

That week, an AI tool flags a likely ligament tear on Karim's knee MRI. Lina's dermatologist sees a risk score for her mole. Three patients, three images, three AI tools. What are these tools doing, and where do they fail?

## Learning Objectives
By the end of this chapter you will be able to:
1. [LO1] Distinguish AI tools that detect, diagnose and triage.
2. [LO2] Describe AI in eye and breast screening and judge the evidence.
3. [LO3] Explain why fast AI-made MRI scans can show features that are not there.
4. [LO4] Describe how AI helps in pathology and the clinical laboratory.
5. [LO5] Identify how imaging and laboratory AI fail in different groups and places.

> **Medical Background in 60 Seconds:** An **X-ray** passes radiation through the body; bone looks white. **CT** builds slices from many X-rays. **MRI** uses a magnet, not radiation, and shows soft tissue such as ligaments. A **retinal photograph** shows the vessels at the back of the eye, where diabetes causes damage. A **biopsy** is a small tissue sample checked under a microscope.

## 6.1 Detect, Diagnose, Triage
Imaging AI tools do three kinds of jobs.

- **Computer-aided detection** (CADe) marks where something may be, such as a box around a lung spot.
- **Computer-aided diagnosis** (CADx) describes a finding, such as "likely cancer".
- **Computer-aided triage** (CADt) moves urgent scans to the top of the list, such as a suspected brain bleed.

The difference matters. A triage tool that misses a bleed does not remove the human read. A diagnosis tool that calls a cancer "benign" can directly mislead a decision.

An AI model sees only the pixels a person sees. It learns patterns, and sometimes those patterns are shortcuts, such as the scanner type (Chapter 3) [1].

## 6.2 Screening Eyes and Breasts
**Eye screening.** Diabetic eye disease is a leading cause of preventable blindness. Many countries lack enough specialists to check every patient. In a study in 900 patients in primary-care clinics, an AI system found significant eye disease with 87% sensitivity and 91% specificity [2]. It became the first AI system in the United States allowed to make this decision without a specialist.

Amal's result is a referral, not a diagnosis. Some referred patients will turn out to be fine. The eye specialist will confirm.

**Breast screening.** In many countries, two radiologists read each mammogram. In a large Swedish randomised trial, AI helped sort the mammograms [3]. Reading work fell by 44%, and about 20% more cancers were found without more false alarms.

![Figure 6.1 — Dermoscopic images and model scores](images/image15.png)
*Figure 6.1 — A model's scores for two skin lesions. The "confidence" values are not true probabilities (Chapter 4). Both lesions are on light skin, like most training images.*

## 6.3 Skin, Knees and Fast MRI
**Skin.** A 2017 model matched dermatologists on test photos of skin lesions [4]. But most training photos show light skin. On a test set balanced across skin tones, several models did worse on darker skin [5]. This matters for Lina, who has dark skin (Chapter 10).

**Knee MRI.** A model called MRNet detected knee ligament tears and was tested at another hospital [6]. Tools like this can put scans such as Karim's first in line. The radiologist still reads the whole scan.

**Fast MRI.** MRI is slow. To save time, the scanner can collect less data. An AI network then fills in the missing parts, based on what anatomy usually looks like [7]. A 40-minute scan can drop to 10 minutes, a 75% saving.

But the missing data are guessed, not recovered. If a patient's anatomy is unusual, the network may smooth away a small lesion or add a realistic-looking feature. This is the imaging version of a chatbot's hallucination (Chapter 5).

## 6.4 Pathology: From Glass Slide to Heatmap
In **digital pathology**, a scanner turns a glass slide into a **whole-slide image**. One image is huge, often several gigabytes.

A model cannot read it in one piece. So it is cut into thousands of small tiles. The model scores each tile. The scores are combined into a colour **heatmap** that shows where suspicious tissue is (Figure 6.2).

![Figure 6.2 — Whole-slide imaging pipeline](rework/figures/orig-image5.png)
*Figure 6.2 — A slide is cut into tiles, each tile is scored, and the results form a heatmap.*

In one large study, a model could have spared pathologists from reviewing most prostate slides while still catching every cancer in the test set [8]. But stain colour and scanners differ between laboratories. A model from one laboratory may fail in another.

## 6.5 The Clinical Laboratory
Most laboratory errors happen before the test is run: wrong patient, wrong tube or poor handling [9]. AI and automation help at several points.

- **Sample checks.** Analysers detect **haemolysis** (burst red cells), **icterus** (high bilirubin) and **lipaemia** (high fat). Each can distort results.
- **Delta checks.** Software compares a new result with the patient's last one. A sudden big change may be real, or it may mean the sample came from the wrong patient.
- **Microscopy.** Digital systems pre-sort blood cells on a slide. A technologist reviews what is flagged.

AI can also find hidden signals. One model predicted blood pressure and smoking from eye photos [10]. This is exciting research, not yet a test for individual patients.

> **Through Four Lenses**
> - **Medicine:** Doctors should know if a tool detects, diagnoses or triages. A triage flag speeds reading; it does not replace a full report or examination.
> - **Pharmacy:** Pharmacists use laboratory values for dosing, such as creatinine. A delta-check or sample warning means the value may be wrong. Confirm before changing a dose.
> - **Physical Therapy:** Physiotherapists read imaging reports to plan rehabilitation. An AI-flagged tear still needs clinical stability tests. Scans and function do not always match.
> - **Health Sciences:** Imaging and laboratory staff make the inputs AI reads. Positioning, stains and analyser settings all change model performance. Record changes and report odd outputs.

> **Myth vs Evidence:** Myth: "Imaging AI works equally well for everyone." Evidence: Skin models tested on a set balanced by skin tone did worse on darker skin [5]. Performance must be checked in each group.

> **Safety Alert:** An AI "normal" is not a guarantee. If the patient's symptoms do not fit the report, ask for a human review.

## Key Takeaways
- Detection marks findings, diagnosis describes them, and triage reorders the list.
- Eye and breast screening have strong evidence; many other tools do not.
- Fast-MRI networks guess missing data, which saves time but can add or hide features.
- Pathology AI tiles huge images and builds heatmaps; stain and scanner changes are key risks.
- Laboratory AI checks sample quality and sudden changes, and every flag needs human review.

## Self-Assessment
**Q1.** An AI tool moves CT scans with a suspected brain bleed to the top of the list. It does not mark the bleed. What type of tool is this? [LO1]
A) Detection (CADe)
B) Diagnosis (CADx)
C) Triage (CADt)
D) A scribe

**Q2.** An eye-screening AI had 87% sensitivity and 91% specificity. Amal's result is "refer". What is the best interpretation? [LO2]
A) She needs a specialist to confirm; some referred patients will be fine.
B) She definitely has sight-threatening disease.
C) The result can be ignored.
D) She should start laser treatment today.

**Q3.** Which evidence would best support using an AI tool for mammography screening? [LO2]
A) The company's own accuracy report
B) A study with secret code and data
C) One study of old data from one hospital
D) A randomised screening trial showing more cancers found without more false alarms

**Q4.** A fast-MRI knee scan shows a small defect that is absent on the standard slow scan. What is a likely explanation? [LO3]
A) The fast scan used radiation.
B) The AI network guessed anatomy and added a feature that is not there.
C) The knee changed in five minutes.
D) Fast MRI recovers all data exactly.

**Q5.** A scan time falls from 40 to 10 minutes. What is the percentage saving? [LO3]
A) 25%
B) 40%
C) 75%
D) 400%

**Q6.** Why are whole-slide images cut into tiles? [LO4]
A) They are far too large for a model to read in one piece.
B) Tiling removes patient names.
C) Pathologists prefer small squares.
D) Tiling fixes stain colour.

**Q7.** A patient's creatinine was 85 yesterday and 300 today. She is well, and her other results match another patient on the ward. What is most likely? [LO4]
A) Contamination from a drip
B) Normal daily change
C) Burst red cells
D) A sample from the wrong patient

**Q8.** A pathology model from one laboratory does poorly in a second laboratory. What is the most likely cause? [LO5]
A) The second laboratory's patients have no cancer.
B) Differences in stain colour and scanners
C) The model was too simple.
D) The second laboratory used MRI.

**Q9.** A skin model does worse on a test set balanced by skin tone. What is the lesson for Lina's care? [LO5]
A) Models can never be used on skin.
B) Only dermatologists can use datasets.
C) Performance must be checked in people like her, including darker skin.
D) The balanced test set was wrong.

**Q10.** A model predicts blood pressure from an eye photo. How should this be described today? [LO5]
A) Exciting research, not yet a proven test for individual patients
B) A replacement for measuring blood pressure
C) Proof that eye photos are useless
D) An approved test everywhere

**Case Question.** Amal is frightened by her "refer" result. Write four sentences explaining what it means, why she needs an eye specialist and why she should not assume the worst.

## Answers and Rationales
**Q1. C** — Reordering the list is triage. A marks findings. B describes them. D writes notes.

**Q2. A** — A screening referral needs confirmation, and false alarms happen [2]. B overstates. C and D are unsafe.

**Q3. D** — A randomised trial is the strongest evidence [3]. A, B and C are weaker.

**Q4. B** — The network guesses missing data and can add or hide features [7]. A is false; MRI uses no radiation. C and D are false.

**Q5. C** — 30 ÷ 40 = 75%. A is the time left. B and D are wrong.

**Q6. A** — The images are too large to read at once. B, C and D are not the reason.

**Q7. D** — A sudden big rise in a well patient, matching another patient, suggests a labelling error. A is wrong because drip contamination dilutes and lowers most values. B and C do not fit.

**Q8. B** — Stain and scanner differences change the data. A, C and D are unsupported.

**Q9. C** — Performance fell on darker skin [5], so it must be checked in each group. A overgeneralises. B and D are wrong.

**Q10. A** — This is promising research [10], not a proven individual test. B, C and D are wrong.

**Case Question — model answer.** "The camera found changes at the back of your eyes that need a closer look. The test is designed to be careful, so it sometimes refers people whose eyes are fine. An eye specialist will examine you and decide if you need treatment. If you do, finding it early like this is exactly what protects your sight."

## References
1. Zech JR, Badgeley MA, Liu M, et al. Variable generalization performance of a deep learning model to detect pneumonia in chest radiographs: a cross-sectional study. PLoS Med. 2018;15(11):e1002683. DOI: 10.1371/journal.pmed.1002683
2. Abràmoff MD, Lavin PT, Birch M, et al. Pivotal trial of an autonomous AI-based diagnostic system for detection of diabetic retinopathy in primary care offices. NPJ Digit Med. 2018;1:39. DOI: 10.1038/s41746-018-0040-6
3. Lång K, Josefsson V, Larsson AM, et al. Artificial intelligence-supported screen reading versus standard double reading in the Mammography Screening with Artificial Intelligence trial (MASAI): a clinical safety analysis of a randomised, controlled, non-inferiority, single-blinded, screening accuracy study. Lancet Oncol. 2023;24(8):936-944. DOI: 10.1016/s1470-2045(23)00298-x
4. Esteva A, Kuprel B, Novoa RA, et al. Dermatologist-level classification of skin cancer with deep neural networks. Nature. 2017;542(7639):115-118. DOI: 10.1038/nature21056
5. Daneshjou R, Vodrahalli K, Novoa RA, et al. Disparities in dermatology AI performance on a diverse, curated clinical image set. Sci Adv. 2022;8(32):eabq6147. DOI: 10.1126/sciadv.abq6147
6. Bien N, Rajpurkar P, Ball RL, et al. Deep-learning-assisted diagnosis for knee magnetic resonance imaging: development and retrospective validation of MRNet. PLoS Med. 2018;15(11):e1002699. DOI: 10.1371/journal.pmed.1002699
7. Hammernik K, Klatzer T, Kobler E, et al. Learning a variational network for reconstruction of accelerated MRI data. Magn Reson Med. 2018;79(6):3055-3071. DOI: 10.1002/mrm.26977
8. Campanella G, Hanna MG, Geneslaw L, et al. Clinical-grade computational pathology using weakly supervised deep learning on whole slide images. Nat Med. 2019;25(8):1301-1309. DOI: 10.1038/s41591-019-0508-1
9. Plebani M. Errors in clinical laboratories or errors in laboratory medicine? Clin Chem Lab Med. 2006;44(6):750-759. DOI: 10.1515/cclm.2006.123
10. Poplin R, Varadarajan AV, Blumer K, et al. Prediction of cardiovascular risk factors from retinal fundus photographs via deep learning. Nat Biomed Eng. 2018;2(3):158-164. DOI: 10.1038/s41551-018-0195-0


---

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


---

# Chapter 8: AI in Motion — Rehabilitation, Wearables and Robotics

## Opening Case
Six weeks after his knee injury, Karim is in rehabilitation. He cannot afford to travel to the clinic three times a week. So his physiotherapist sets up a home programme. Twice a week, Karim films himself squatting with his phone. An app tracks his hips, knees and ankles and reports his knee angle. A wrist band counts his steps.

At the video review, the app says 95° of knee bend. But the squat clearly looks shallower. His trousers are baggy and the room is dark. The physiotherapist measures his knee with a goniometer: 80°. She adjusts his programme.

Movement is data too. How do cameras and sensors turn movement into numbers? How far can we trust them?

## Learning Objectives
By the end of this chapter you will be able to:
1. [LO1] Describe how pose estimation turns video into joint angles.
2. [LO2] Explain how wearable sensors measure movement, and their limits.
3. [LO3] Judge the evidence for remote rehabilitation and home-exercise apps.
4. [LO4] Distinguish the levels of autonomy in medical robots.
5. [LO5] Describe how AI measures surgical skill and where self-operating robots stand.

> **Medical Background in 60 Seconds:** The **gait cycle** is one full step, from one heel strike to the next heel strike of the same foot. **Range of motion** is how far a joint can move, measured in degrees with a goniometer. After a knee injury, physiotherapists track movement, strength and walking to guide recovery.

## 8.1 Pose Estimation: From Video to Joints
**Pose estimation** means finding points on the body, such as hips, knees and ankles, in each video frame. Joining the points makes a stick figure. Software then calculates joint angles and walking speed (Figure 8.1).

OpenPose is a widely used system for this [1]. Researchers have used such tools on ordinary phone videos to measure walking [2]. This could bring gait assessment outside special laboratories.

![Figure 8.1 — Pose estimation](rework/figures/pose-skeleton.svg)
*Figure 8.1 — The model finds body points in each frame; joint angles are worked out from the lines between them.*

Accuracy depends on conditions. Baggy clothes hide joints. Poor light, one camera angle and a body partly out of view all add error. Most models learned from people walking normally. Walking aids, amputations and unusual movement may not be well covered. Karim's case shows these limits.

## 8.2 Wearables: Sensors on the Body
**Wearable** devices include wrist bands, smartwatches and clip-on sensors. Most contain an **inertial measurement unit** (IMU). It combines an accelerometer and a gyroscope, which record movement and rotation. Software turns these signals into steps, activity or sleep.

Consumer devices count steps fairly well in healthy people [3]. They are less accurate at slow walking speeds and with walking aids. These are exactly the patients many physiotherapists treat. So a device should be checked in the patient group that will use it.

## 8.3 Remote Rehabilitation and Home Apps
**Telerehabilitation** means physiotherapy delivered remotely, often by video. A review found that live video rehabilitation for muscle and joint problems improved function about as much as in-person care [4].

AI can add feedback. Apps can count repetitions, check movement quality and remind patients to exercise. The evidence for these apps is still growing. Judge each app with the Chapter 4 questions: Does it measure what it claims? In whom was it tested? Does it help patients?

A **robotic exoskeleton** is a powered frame worn on the legs. It helps people practise walking after a stroke or spinal injury. Trials so far are small [5]. Exoskeletons support therapists; they do not replace them.

## 8.4 Robots in the Operating Room
In robot-assisted surgery, the surgeon sits at a console and controls instruments inside the patient. This is called **leader–follower telemanipulation**: the surgeon's hands lead, and the robot's arms follow.

The robot adds helpful features:

- *Motion scaling* turns a large hand movement into a tiny instrument movement.
- *Tremor filtering* removes the small natural shake of human hands.
- *Wristed instruments* bend like a wrist inside the body.

In joint replacement, some robots use a **haptic boundary**. The cutting tool can move only inside a planned zone, which protects nearby tissue.

## 8.5 Levels of Autonomy
Most surgical robots today have no autonomy. Every movement comes from the surgeon. A common framework describes six levels [6]:

| Level | Meaning | Example |
|---|---|---|
| 0 | No autonomy | Standard leader–follower robot |
| 1 | Robot assistance | Tremor filtering, haptic boundaries |
| 2 | Task autonomy | Robot does one task, such as stitching, under supervision |
| 3 | Conditional autonomy | Robot plans a task; human approves |
| 4 | High autonomy | Robot decides; human can step in |
| 5 | Full autonomy | No human involved |

A research robot called STAR stitched pig bowel with little human help [7]. This was a small animal study in one laboratory. It shows what may be possible, not readiness for patients.

## 8.6 Measuring Skill
Movement data can also assess people. The **Objective Structured Assessment of Technical Skills** (OSATS) is a rating scale for surgical skill [8]. AI can now study instrument movements and surgical video to estimate skill. The same idea works in rehabilitation: movement quality can be measured and tracked over time.

> **Through Four Lenses**
> - **Medicine:** Doctors should know that most surgical robots today are level 0 or 1. Consent talks should explain who controls the instrument.
> - **Pharmacy:** Pharmacists can combine activity data with medicine reviews. Fewer daily steps after a new sedating drug can signal a problem.
> - **Physical Therapy:** Physiotherapists should check app and wearable measures against clinical tests. Clothing, light and slow walking all reduce accuracy.
> - **Health Sciences:** Technical staff maintain sensors, cameras and robots. Software updates and device changes can shift measurements and should be logged.

> **Myth vs Evidence:** Myth: "Self-operating surgical robots already beat surgeons." Evidence: The best-known result, STAR, was a small study in pigs [7]. Robots used on patients today are controlled by surgeons.

> **Safety Alert:** When an app's measurement disagrees with what you see, measure it yourself. Do not progress exercises or clear a patient for work based on an unchecked app number.

## Key Takeaways
- Pose estimation turns video into joint angles; clothing, light and body type affect accuracy.
- Wearables count steps well in healthy walkers, less well in slow or assisted walking.
- Live video rehabilitation for muscle and joint problems works about as well as in-person care.
- Surgical robots today are mostly controlled by surgeons, with helpful features, not self-operating.
- Every movement measure must be checked in the people who will use it.

## Self-Assessment
**Q1.** An app finds Karim's hips, knees and ankles in each video frame. What is this called? [LO1]
A) Pose estimation
B) Retrieval-augmented generation
C) Pharmacovigilance
D) Triage

**Q2.** Karim's app says 95°, but a goniometer shows 80°. He wore baggy trousers in a dark room. What is the most likely cause? [LO1]
A) The goniometer is always wrong.
B) Someone attacked the app.
C) Clothing and poor light reduced the app's accuracy.
D) His knee changed during the call.

**Q3.** An 80-year-old with a walking frame wears a step counter. What should the physiotherapist expect? [LO2]
A) Perfect step counts
B) Possible undercounting, because slow assisted walking reduces accuracy
C) Overcounting of calories only
D) No data at all

**Q4.** What is inside an inertial measurement unit? [LO2]
A) A camera and a microphone
B) A thermometer and an oxygen sensor
C) A magnet and radio coils
D) An accelerometer and a gyroscope

**Q5.** What does a review say about live video rehabilitation for muscle and joint problems? [LO3]
A) It is harmful.
B) It works only for children.
C) It improves function about as much as in-person care.
D) It has never been studied.

**Q6.** What does motion scaling do in robot-assisted surgery? [LO4]
A) Turns a large hand movement into a tiny instrument movement
B) Lets the robot operate alone
C) Measures the patient's blood pressure
D) Records the operation for billing

**Q7.** A robot stitches by itself while the surgeon supervises. Which autonomy level is this? [LO4]
A) Level 0
B) Level 1
C) Level 5
D) Level 2

**Q8.** How should the STAR robot's results be understood? [LO5]
A) STAR is approved for routine human surgery.
B) It is an early animal study showing what may be possible.
C) It proves robots are safer than surgeons.
D) It shows full autonomy in patients.

**Q9.** What is OSATS? [LO5]
A) A robot
B) A drug database
C) A rating scale for surgical skill
D) A wearable sensor

**Q10.** A clinic plans an AI home-exercise app for older patients after hip surgery. What should it check first? [LO3]
A) Whether the app was tested in patients like theirs and improves outcomes
B) Whether the app has nice colours
C) Whether it uses the newest AI
D) Whether it can replace all visits

**Case Question.** Write a short note for Karim's record explaining the gap between the app and the goniometer, its cause and how you will use the app safely.

## Answers and Rationales
**Q1. A** — Finding body points in video is pose estimation [1]. B, C and D are unrelated.

**Q2. C** — Loose clothes and poor light hide joints and add error. A, B and D are unlikely.

**Q3. B** — Step counters are less accurate with slow, assisted walking [3]. A overstates. C and D are wrong.

**Q4. D** — An IMU combines an accelerometer and a gyroscope. A, B and C are other devices.

**Q5. C** — Function improved about as much as standard care [4]. A, B and D are false.

**Q6. A** — Motion scaling makes movements smaller and more precise. B, C and D are not what it does.

**Q7. D** — One task under supervision is level 2 [6]. A has no autonomy. B is assistance only. C has no human.

**Q8. B** — STAR was a small study in pigs [7]. A, C and D overstate it.

**Q9. C** — OSATS is a skill rating scale [8]. A, B and D are wrong.

**Q10. A** — Testing in the right patients and proof of benefit come first. B, C and D do not show safety.

**Case Question — model answer.** "App knee bend 95°; goniometer 80° in the same session. The gap is likely due to loose clothing and low light. The goniometer value is recorded. Next time, Karim will film in good light, wear shorts and keep his whole body in view. I will check the app against a goniometer at each review."

## References
1. Cao Z, Hidalgo G, Simon T, Wei SE, Sheikh Y. OpenPose: realtime multi-person 2D pose estimation using part affinity fields. IEEE Trans Pattern Anal Mach Intell. 2021;43(1):172-186. DOI: 10.1109/TPAMI.2019.2929257
2. Stenum J, Rossi C, Roemmich RT. Two-dimensional video-based analysis of human gait using pose estimation. PLoS Comput Biol. 2021;17(4):e1008935. DOI: 10.1371/journal.pcbi.1008935
3. Fuller D, Colwell E, Low J, et al. Reliability and validity of commercially available wearable devices for measuring steps, energy expenditure, and heart rate: systematic review. JMIR Mhealth Uhealth. 2020;8(9):e18694. DOI: 10.2196/18694
4. Cottrell MA, Galea OA, O'Leary SP, Hill AJ, Russell TG. Real-time telerehabilitation for the treatment of musculoskeletal conditions is effective and comparable to standard practice: a systematic review and meta-analysis. Clin Rehabil. 2017;31(5):625-638. DOI: 10.1177/0269215516645148
5. Louie DR, Eng JJ. Powered robotic exoskeletons in post-stroke rehabilitation of gait: a scoping review. J Neuroeng Rehabil. 2016;13:53. DOI: 10.1186/s12984-016-0162-5
6. Yang GZ, Cambias J, Cleary K, et al. Medical robotics—regulatory, ethical, and legal considerations for increasing levels of autonomy. Sci Robot. 2017;2(4):eaam8638. DOI: 10.1126/scirobotics.aam8638
7. Saeidi H, Opfermann JD, Kam M, et al. Autonomous robotic laparoscopic surgery for intestinal anastomosis. Sci Robot. 2022;7(62):eabj2908. DOI: 10.1126/scirobotics.abj2908
8. Martin JA, Regehr G, Reznick R, et al. Objective structured assessment of technical skill (OSATS) for surgical residents. Br J Surg. 1997;84(2):273-278. DOI: 10.1046/j.1365-2168.1997.02502.x


---

# Chapter 9: Monitoring, Prediction and Population Health

## Opening Case
Amal is in hospital with a urine infection. At 3 a.m., the ward computer shows an alert: "High risk of getting worse in the next 12 hours." Her heart rate has crept up. Her blood pressure has drifted down. Her creatinine is rising.

The night nurse has already seen three alerts tonight. Two were false alarms. She checks Amal herself. Amal is confused and her skin is cool. The nurse calls the doctor, who starts fluids. By morning, Amal is better.

Prediction models promise early warning. But every alert takes time. When does a warning help, and when does it become noise?

## Learning Objectives
By the end of this chapter you will be able to:
1. [LO1] Explain how early-warning models work and why they create many alarms.
2. [LO2] Weigh early warning against false alarms.
3. [LO3] Describe AI that reads the ECG and the trial evidence behind it.
4. [LO4] Describe automatic insulin delivery and who it is for.
5. [LO5] Judge a population-health AI claim using the lesson of Google Flu Trends.

> **Medical Background in 60 Seconds:** **Sepsis** is a life-threatening reaction to infection that damages the body's own organs. Early signs include fast breathing, fast pulse, low blood pressure and confusion. **Acute kidney injury** (AKI) is a sudden fall in kidney function, often seen as rising creatinine. Both are easier to treat when caught early.

## 9.1 Early Warning: From Scores to Models
Hospitals have long used an **early warning score**. Nurses record vital signs, and each value earns points. The National Early Warning Score (NEWS2) is widely used [1]. A high total triggers a review. It is a simple, rule-based system.

Machine-learning models go further. They use many more inputs, such as laboratory results and trends over time. They aim to warn earlier.

The TREWS sepsis system was studied in five hospitals [2]. When doctors confirmed its alert within three hours, fewer patients died. This was not a randomised trial, but it is fairly strong evidence.

Not every tool works as claimed. A popular commercial sepsis model, tested independently, missed two-thirds of cases (Chapter 4) [3].

## 9.2 Early Warning Versus False Alarms
A model can warn early or warn accurately. Doing both is hard. Warning earlier means using weaker signals, which gives more false alarms.

One well-known model predicted AKI up to 48 hours early [4]. It caught 90% of the most severe cases. But for every true alert, it gave about two false ones. Also, 93.6% of patients in its data were men. How well it works for women was unclear.

On a busy ward, many false alerts add up. Each one needs a nurse to check the patient. If staff lose trust, they start ignoring alerts. This is **alarm fatigue**. Before using a model, ask: How many alerts per shift? Who responds, and what do they do?

## 9.3 AI and the ECG
The **electrocardiogram** (ECG) records the heart's electrical activity. It is cheap and available almost everywhere. AI can find patterns in the ECG that people cannot see.

One model spotted people at risk of atrial fibrillation, an irregular rhythm linked to stroke, from an ECG with a normal rhythm [5]. Another finds a weak heart pump from a standard ECG.

That second model was tested in a randomised trial with over 22,000 patients [6]. Teams that saw the AI result found more cases of weak heart pump: 2.1% of patients instead of 1.6%. The benefit was real but modest. This is a realistic picture: AI helps, but often less than accuracy figures suggest.

![Figure 9.1 — Trend-based instability prediction](images/image14.png)
*Figure 9.1 — A sketch of blood pressure over time. A model flags a subtle trend before pressure clearly falls.*

## 9.4 Automatic Insulin Delivery
People with **type 1 diabetes** make no insulin and must replace it every day. A **closed-loop system** links a glucose sensor, a computer program and an insulin pump (Figure 9.2). The sensor measures glucose every few minutes. The program adjusts insulin automatically.

In a six-month randomised trial, closed-loop systems raised the time spent in the healthy glucose range from 59% to 71% of the day [7].

![Figure 9.2 — Closed-loop insulin delivery](rework/figures/orig-image18.png)
*Figure 9.2 — A glucose sensor feeds a dosing program, which adjusts an insulin pump.*

Amal has type 2 diabetes and takes tablets, not insulin. This tool is not for her current treatment. Knowing who a tool is for is part of using it safely.

## 9.5 Population Health
Public health watches whole communities. AI helps by scanning news, social media and health records for signs of outbreaks [8].

Google Flu Trends teaches an important lesson. In 2009, flu-related web searches tracked official flu reports closely [9]. For a few years, it looked like a cheap way to track flu. Then it failed. In 2012–2013, it predicted more than double the real level [10].

Why? People's search habits changed, and media stories about flu made healthy people search too. The model had no link to the biology of flu. This is distribution shift and shortcut learning on a national scale (Chapter 3).

> **Through Four Lenses**
> - **Medicine:** Doctors should know how often an alert is right and how early it warns. An alert should prompt a bedside review, not automatic treatment.
> - **Pharmacy:** Pharmacists can act on kidney alerts by reviewing doses of kidney-cleared drugs. Early medicine review can prevent the injury the model predicts.
> - **Physical Therapy:** Physiotherapists can use monitoring data to time exercise safely. Falling blood pressure may mean waiting, while stable trends support earlier movement.
> - **Health Sciences:** Public-health officers should compare digital signals with laboratory-confirmed data. Laboratory results give surveillance models real biological meaning.

> **Myth vs Evidence:** Myth: "Big data can replace traditional disease surveillance." Evidence: Google Flu Trends first tracked flu well [9], but later more than doubled the true level [10]. Digital signals work best alongside laboratory data.

> **Safety Alert:** An alert is a prompt to look at the patient, not a diagnosis. No alert does not mean no problem. If a patient looks unwell, act.

## Key Takeaways
- Early-warning scores use simple rules; AI models use more data and aim to warn earlier.
- Earlier warnings bring more false alarms; alarm burden decides whether a model helps.
- ECG AI has trial evidence of real but modest benefit.
- Automatic insulin delivery improves glucose control in type 1 diabetes.
- Population AI can fail when behaviour changes, as Google Flu Trends showed.

## Self-Assessment
**Q1.** NEWS2 adds points for vital signs such as breathing rate and pulse. What kind of system is it? [LO1]
A) A deep-learning model
B) A rule-based early warning score
C) A large language model
D) An automatic insulin system

**Q2.** A kidney model warns 48 hours early but gives two false alerts for every true one. What is the main practical concern? [LO2]
A) It cannot find severe cases.
B) Its data were too large.
C) It uses creatinine.
D) Staff workload and alarm fatigue from false alerts

**Q3.** The same model was trained on patients who were 93.6% men. What should a hospital do first? [LO2]
A) Check how it performs in women and in its own patients
B) Use it only at night
C) Use it as it is because the data were large
D) Remove creatinine

**Q4.** In a randomised trial, AI-ECG results raised diagnosis of a weak heart pump from 1.6% to 2.1%. What is the best interpretation? [LO3]
A) The AI replaced heart scans.
B) The AI had no effect.
C) The AI gave a real but modest benefit.
D) The AI caused heart failure.

**Q5.** An AI model spots atrial fibrillation risk from an ECG with a normal rhythm. What does this show? [LO3]
A) The ECG was faulty.
B) AI can find ECG patterns that people cannot see.
C) Atrial fibrillation is not linked to stroke.
D) The model uses age only.

**Q6.** Who is an automatic (closed-loop) insulin system designed for? [LO4]
A) A person with type 1 diabetes who uses insulin
B) Amal, who takes tablets for type 2 diabetes
C) A person with high blood pressure only
D) A patient with a knee injury

**Q7.** What did closed-loop insulin delivery improve in a six-month trial? [LO4]
A) Blood pressure
B) Kidney function
C) Weight only
D) Time spent in the healthy glucose range

**Q8.** Why did Google Flu Trends fail? [LO5]
A) No one searched for flu any more.
B) Laboratory tests stopped.
C) Search habits and media stories changed, so the link to real flu shifted.
D) The model was too small.

**Q9.** An app claims to track an outbreak from social-media posts. How should it be judged? [LO5]
A) Compare its signal over time with laboratory-confirmed data
B) Count how many posts it reads
C) Trust it if it uses AI
D) Check if it has a colourful map

**Q10.** A ward gets 6 alerts a day, and 2 are true. What share of alerts are real? [LO1]
A) 12%
B) 66%
C) 50%
D) 33%

**Case Question.** The ward manager wants to switch off the alerts because "most are false". Write a short reply explaining the trade-off and suggesting one change.

## Answers and Rationales
**Q1. B** — NEWS2 adds points with fixed rules [1]. A, C and D are other tools.

**Q2. D** — Frequent false alerts cause workload and fatigue [4]. A is false. B and C are not concerns.

**Q3. A** — A model trained mostly on men must be checked in women and local patients. B, C and D miss the problem.

**Q4. C** — The trial showed a real but modest gain [6]. A, B and D misread it.

**Q5. B** — AI detects subtle patterns people miss [5]. A, C and D are false.

**Q6. A** — These systems are for insulin users with type 1 diabetes [7]. B, C and D are not the users.

**Q7. D** — Time in range rose from 59% to 71% [7]. A, B and C were not the main result.

**Q8. C** — Changing behaviour broke the link the model relied on [10]. A, B and D are wrong.

**Q9. A** — Digital signals should be checked against confirmed data. B, C and D do not test accuracy.

**Q10. D** — 2 ÷ 6 = 33%. A, B and C are wrong.

**Case Question — model answer.** "I understand, because false alerts take time from other patients. But the alerts also catch real problems early, as with Amal. Switching them off loses that. Instead, we could ask the informatics team to adjust the threshold so fewer low-value alerts fire, and track how many alerts per shift are real."

## References
1. Royal College of Physicians. National Early Warning Score (NEWS) 2: standardising the assessment of acute-illness severity in the NHS. London: RCP; 2017. https://www.rcp.ac.uk/improving-care/resources/national-early-warning-score-news-2/
2. Adams R, Henry KE, Sridharan A, et al. Prospective, multi-site study of patient outcomes after implementation of the TREWS machine learning-based early warning system for sepsis. Nat Med. 2022;28(7):1455-1460. DOI: 10.1038/s41591-022-01894-0
3. Wong A, Otles E, Donnelly JP, et al. External validation of a widely implemented proprietary sepsis prediction model in hospitalized patients. JAMA Intern Med. 2021;181(8):1065-1070. DOI: 10.1001/jamainternmed.2021.2626
4. Tomašev N, Glorot X, Rae JW, et al. A clinically applicable approach to continuous prediction of future acute kidney injury. Nature. 2019;572(7767):116-119. DOI: 10.1038/s41586-019-1390-1
5. Attia ZI, Noseworthy PA, Lopez-Jimenez F, et al. An artificial intelligence-enabled ECG algorithm for the identification of patients with atrial fibrillation during sinus rhythm: a retrospective analysis of outcome prediction. Lancet. 2019;394(10201):861-867. DOI: 10.1016/S0140-6736(19)31721-0
6. Yao X, Rushlow DR, Inselman JW, et al. Artificial intelligence-enabled electrocardiograms for identification of patients with low ejection fraction: a pragmatic, randomized clinical trial. Nat Med. 2021;27(5):815-819. DOI: 10.1038/s41591-021-01335-4
7. Brown SA, Kovatchev BP, Raghinaru D, et al. Six-month randomized, multicenter trial of closed-loop control in type 1 diabetes. N Engl J Med. 2019;381(18):1707-1717. DOI: 10.1056/NEJMoa1907863
8. Freifeld CC, Mandl KD, Reis BY, Brownstein JS. HealthMap: global infectious disease monitoring through automated classification and visualization of Internet media reports. J Am Med Inform Assoc. 2008;15(2):150-157. DOI: 10.1197/jamia.M2544
9. Ginsberg J, Mohebbi MH, Patel RS, et al. Detecting influenza epidemics using search engine query data. Nature. 2009;457(7232):1012-1014. DOI: 10.1038/nature07634
10. Lazer D, Kennedy R, King G, Vespignani A. The parable of Google Flu: traps in big data analysis. Science. 2014;343(6176):1203-1205. DOI: 10.1126/science.1248506


---

# Chapter 10: Bias, Fairness and Privacy

## Opening Case
A university public-health team is planning a skin-cancer campaign. The leader wants to recommend a free skin-check app to all students. A team member mentions Lina. The app flagged her mole, but its website shows almost no photos of dark skin. Would it work as well for her as for lighter-skinned classmates?

Across town, Karim's employer offers workers a free fitness wristband. Karim's physiotherapist reads the terms. Steps, heart rate and sleep data will be shared with an insurance company. Karim worries that his slow recovery could affect his job.

Both stories ask one question: who does health AI protect, and who might it harm?

## Learning Objectives
By the end of this chapter you will be able to:
1. [LO1] Identify where bias can enter an AI tool, from data to use.
2. [LO2] Explain the Obermeyer case and why the choice of label caused bias.
3. [LO3] Distinguish anonymisation, pseudonymisation and de-identification.
4. [LO4] Describe differential privacy and federated learning, and their limits.
5. [LO5] Compare the main ideas of data-protection laws, including Egypt's.

## 10.1 Where Bias Comes From
**Algorithmic bias** means a model works worse, or gives worse advice, for some groups. Bias can enter at every step:

- *Data.* Who is in the dataset? Famous datasets come from a few rich settings (Chapter 2).
- *Labels.* What counts as the "right answer"? A poor label can carry past unfairness.
- *Testing.* Is performance reported for each group, or only on average?
- *Use.* Is the tool used in people like those it was tested on?

Skin tone is a clear example. Skin datasets contain mostly light skin [1]. On a test set balanced across skin tones, models did worse on darker skin [2]. For Lina, this is real.

Bias can also hide in X-rays. One study found that AI missed disease more often in women, Black, Hispanic and younger patients, and in patients with low-income insurance [3]. People who already face barriers were more often told they were healthy when they were not.

## 10.2 The Obermeyer Case: When the Label Is the Problem
A widely used US algorithm chose patients for an extra-care programme [4]. It used health-care *cost* as the label for health *need*. It did not use race as an input.

Researchers found that, at the same score, Black patients were sicker than white patients. The reason was the label. Because of unequal access to care, less money had been spent on equally sick Black patients. The model learned that they would cost less, and wrongly treated that as needing less.

When the label was changed to direct health measures, the share of Black patients chosen for extra help rose from 17.7% to 46.5% [4].

The lesson is often told wrongly. The model was already "race-blind", yet it was biased. The fix was to change what the model predicted.

Also, AI can detect a patient's race from chest X-rays, even though experts cannot see how [5]. So removing race from the inputs does not guarantee fairness. Fairness needs measurement: check performance in each group, choose labels carefully and keep monitoring.

> **Medical Background in 60 Seconds:** The **Fitzpatrick scale** classifies skin from type I (always burns) to type VI (deeply pigmented, rarely burns). Melanoma is less common in darker skin but is often found later, when outcomes are worse. It may appear on the palms, soles or nails.

## 10.3 Privacy: Names Are Not Enough
Health data are among the most sensitive personal data. Removing names does not fully protect them.

Three terms are often confused:

- **De-identification** removes details that could identify a person. The US HIPAA "Safe Harbor" method lists 18 identifiers to remove, such as names and full dates [6].
- **Pseudonymisation** replaces names with a code. Whoever holds the key can re-link the data. Under European law, this is still personal data [7].
- **Anonymisation** makes re-linking impossible by any reasonable means. This is very hard for rich health data.

The danger is **re-identification**. A few ordinary facts together can point to one person. Postcode, birth date and sex together identify most US residents [8]. Wearable data are especially risky, because movement and sleep patterns are almost unique.

![Figure 10.1 — A privacy pipeline for AI training](rework/figures/privacy-pipeline.svg)
*Figure 10.1 — Each protection step reduces, but does not remove, the risk of re-identification.*

## 10.4 Privacy-Protecting Methods
**Differential privacy** adds carefully measured random noise to data or results [9]. This limits how much anyone can learn about one person. More noise means stronger privacy but less accurate results. It is a strong protection, but not an absolute one.

**Federated learning** trains a model across several hospitals without moving patient data. Each hospital trains on its own data and shares only model updates [10]. This reduces data sharing. But updates can still leak some information, so extra protections are often added.

## 10.5 The Law: Shared Principles
Laws differ between countries, but they share core ideas: a lawful reason to use data, using it only for its stated purpose, collecting only what is needed, keeping it secure and respecting people's rights.

- **GDPR** in the European Union gives health data extra protection [7].
- **HIPAA** in the United States sets rules for health providers and insurers [6].

> **Local Context:** Egypt's **Personal Data Protection Law** (Law No. 151 of 2020) treats health data as sensitive. Using it generally needs explicit written consent and stronger security. Detailed rules were issued in 2025 [11].

For Karim, this matters. Wristband data shared with an insurer may not be covered by the rules that apply to clinicians. He has the right to know how his data will be used before he agrees.

> **Through Four Lenses**
> - **Medicine:** Doctors should ask companies for results by sex, age, ethnicity and skin tone. An average can hide poor performance in patients who already get worse care.
> - **Pharmacy:** Pharmacists hold prescription data that reveal diagnoses. Sharing them with apps needs clear consent, because a medicine list can reveal a condition.
> - **Physical Therapy:** Physiotherapists should explain what wearables record and who sees it. Movement and sleep data are personal and hard to make anonymous.
> - **Health Sciences:** Public-health officers should test tools in their own community first. An app that fails on darker skin would widen health gaps, not close them.

> **Myth vs Evidence:** Myth: "If a model does not use race, it cannot be racially biased." Evidence: The Obermeyer algorithm did not use race, yet it under-selected Black patients because of its cost label [4]. Models can also detect race from images [5].

> **Safety Alert:** Before recommending an AI tool to a group, check if it was tested in people like them. If there is no evidence, say so.

## Key Takeaways
- Bias can enter through data, labels, testing and use.
- In the Obermeyer case, a cost label carried unequal access into the model.
- Removing race or sex does not guarantee fairness; measuring by group does.
- A few details together can identify a person; coded data are still personal data.
- Privacy methods reduce risk but do not remove it.

## Self-Assessment
**Q1.** A skin app was trained mostly on light skin. Where did the bias most likely enter? [LO1]
A) User feedback
B) Legal review
C) Data collection
D) File compression

**Q2.** In the Obermeyer case, why were Black patients sicker at the same score? [LO2]
A) The label was cost, which reflected unequal access to care.
B) Race was an input.
C) The dataset was too small.
D) It was a chatbot.

**Q3.** A developer says, "We removed race from the inputs, so our imaging model is fair." What is the best reply? [LO2]
A) Correct; that guarantees fairness.
B) Fairness does not matter in imaging.
C) Images contain no information about race.
D) Models can detect race from images, so fairness must be measured by group.

**Q4.** A team replaces names with codes but keeps a key linking codes to names. What is this? [LO3]
A) Anonymisation
B) Pseudonymisation
C) Differential privacy
D) Federated learning

**Q5.** Why is wearable movement data hard to anonymise? [LO3]
A) It is stored on paper.
B) It contains nothing personal.
C) Movement and sleep patterns are almost unique to each person.
D) It is protected by default.

**Q6.** A hospital adds measured random noise before releasing data. What is true of this method? [LO4]
A) More noise gives stronger privacy but less accurate results.
B) It makes it impossible to learn anything about anyone.
C) It removes the need for consent.
D) It is the same as pseudonymisation.

**Q7.** Five hospitals train a shared model, each on its own data, sending only updates. What is this? [LO4]
A) Retrieval-augmented generation
B) Pseudonymisation
C) Reinforcement learning
D) Federated learning

**Q8.** A Cairo clinic wants to share records with an app company. How does Egypt's law treat health data? [LO5]
A) As public data
B) As sensitive data, generally needing explicit written consent and stronger security
C) As free of any protection
D) As data only employers may use

**Q9.** Under GDPR, what is the status of coded data when a key still exists? [LO5]
A) It is still personal data.
B) It is fully anonymous.
C) The law does not cover it.
D) It can be sold freely.

**Q10.** In an X-ray study, AI missed disease more often in which patients? [LO1]
A) Only older white men
B) All groups equally
C) Women, Black, Hispanic and younger patients, and those with low-income insurance
D) Only patients with rare diseases

**Case Question.** Karim asks whether he should accept the free wristband. Write a short, balanced answer covering the privacy risks and the questions he should ask.

## Answers and Rationales
**Q1. C** — The training images lacked dark skin, so bias entered in data collection [1, 2]. A, B and D are not where it began.

**Q2. A** — Cost reflected unequal access, so equally sick Black patients looked less needy [4]. B is false. C and D are wrong.

**Q3. D** — Race can be detected from images [5]. A, B and C are false.

**Q4. B** — Codes with a key are pseudonymisation. A cannot be re-linked. C adds noise. D trains across sites.

**Q5. C** — Unique patterns allow re-identification. A, B and D are false.

**Q6. A** — Differential privacy trades accuracy for privacy [9]. B overstates it. C and D are wrong.

**Q7. D** — Training locally and sharing updates is federated learning [10]. A, B and C are other methods.

**Q8. B** — Egypt's Law No. 151 of 2020 treats health data as sensitive [11]. A, C and D are wrong.

**Q9. A** — Coded data are still personal data under GDPR [7]. B, C and D are wrong.

**Q10. C** — AI missed more disease in these groups [3]. A, B and D are wrong.

**Case Question — model answer.** "The wristband can help you track activity, but your steps, heart rate and sleep will go to an insurer. That data can reveal a lot about your health and is hard to make anonymous. Ask who will see it, what it is for, how long it is kept and whether you can withdraw. Also ask whether saying no affects your job. If the answers are unclear, you can say no."

## References
1. Adamson AS, Smith A. Machine learning and health care disparities in dermatology. JAMA Dermatol. 2018;154(11):1247-1248. DOI: 10.1001/jamadermatol.2018.2348
2. Daneshjou R, Vodrahalli K, Novoa RA, et al. Disparities in dermatology AI performance on a diverse, curated clinical image set. Sci Adv. 2022;8(32):eabq6147. DOI: 10.1126/sciadv.abq6147
3. Seyyed-Kalantari L, Zhang H, McDermott MBA, Chen IY, Ghassemi M. Underdiagnosis bias of artificial intelligence algorithms applied to chest radiographs in under-served patient populations. Nat Med. 2021;27(12):2176-2182. DOI: 10.1038/s41591-021-01595-0
4. Obermeyer Z, Powers B, Vogeli C, Mullainathan S. Dissecting racial bias in an algorithm used to manage the health of populations. Science. 2019;366(6464):447-453. DOI: 10.1126/science.aax2342
5. Gichoya JW, Banerjee I, Bhimireddy AR, et al. AI recognition of patient race in medical imaging: a modelling study. Lancet Digit Health. 2022;4(6):e406-e414. DOI: 10.1016/s2589-7500(22)00063-2
6. US Department of Health and Human Services. Guidance regarding methods for de-identification of protected health information in accordance with the HIPAA Privacy Rule (45 CFR 164.514). 2012. https://www.hhs.gov/hipaa/for-professionals/special-topics/de-identification/index.html
7. European Parliament and Council. Regulation (EU) 2016/679 (General Data Protection Regulation). Off J Eur Union. 2016;L119:1-88. https://eur-lex.europa.eu/eli/reg/2016/679/oj
8. Sweeney L. k-anonymity: a model for protecting privacy. Int J Uncertain Fuzziness Knowl Based Syst. 2002;10(05):557-570. DOI: 10.1142/s0218488502001648
9. Dwork C, McSherry F, Nissim K, Smith A. Calibrating noise to sensitivity in private data analysis. In: Theory of Cryptography. Lecture Notes in Computer Science. Springer; 2006:265-284. DOI: 10.1007/11681878_14
10. Rieke N, Hancox J, Li W, et al. The future of digital health with federated learning. NPJ Digit Med. 2020;3:119. DOI: 10.1038/s41746-020-00323-1
11. Arab Republic of Egypt. Law No. 151 of 2020 promulgating the Personal Data Protection Law. Official Gazette; 2020. https://mcit.gov.eg/Upcont/Documents/Reports%20and%20Documents_1232021000_Law_No_151_2020_Personal_Data_Protection.pdf


---

# Chapter 11: Regulation, Liability and the Human in the Loop

## Opening Case
Two weeks after leaving hospital, Amal is back with a fever. The hospital's sepsis model gives her a "low risk" score. It is a busy night. A junior doctor sees the score, notes her vital signs are "borderline" and plans to review her in the morning. By morning, Amal is in septic shock and needs intensive care. She survives.

Her family asks hard questions. The hospital bought the model. The doctor followed its score. The company says the tool is "decision support only". Who is responsible when AI-guided care goes wrong? And why did a trained doctor accept a number that did not fit what she saw?

## Learning Objectives
By the end of this chapter you will be able to:
1. [LO1] Explain when software counts as a medical device.
2. [LO2] Distinguish the main US approval routes for AI devices.
3. [LO3] Describe what the EU AI Act requires for high-risk medical AI.
4. [LO4] Apply the four elements of negligence to an AI case and explain the learned intermediary doctrine.
5. [LO5] Explain automation bias, de-skilling and the limits of AI explanations.

## 11.1 When Software Is a Medical Device
Software meant to diagnose, prevent, monitor or treat disease can be a medical device, even with no hardware. This is called **software as a medical device** (SaMD). An eye-screening system, a sepsis model and a dosing calculator can all be SaMD. A staff-rota app is not.

Regulators sort SaMD by risk [1]. Two questions matter. How much does the software drive care: does it diagnose, guide treatment or just inform? And how serious is the condition? Software that diagnoses a critical condition gets the strictest review.

> **Medical Background in 60 Seconds:** A **medical device** is any instrument, machine or software used for a medical purpose, from a thermometer to an MRI scanner. Regulators check that benefits outweigh risks before sale and keep watching afterwards. **Septic shock** is the most severe stage of sepsis, when blood pressure stays dangerously low despite fluids.

## 11.2 The United States: FDA Routes
The US Food and Drug Administration (FDA) has three main routes:

- **510(k) clearance.** The maker shows the device is similar to one already on the market. Most AI devices use this route.
- **De Novo classification.** For new, low-to-moderate-risk devices with nothing similar on the market. The eye-screening AI took this route (Chapter 6).
- **Premarket approval** (PMA). For high-risk devices, with the strongest evidence.

Clearance does not always mean strong evidence. Most cleared AI devices were tested only on old data, often at one or two sites [2].

AI models get updated. A **predetermined change control plan** (PCCP) lets a maker describe planned updates and their testing in advance. Changes within the plan do not need a new application. The FDA issued final guidance on this in 2024 [3].

## 11.3 Europe: The AI Act
In the European Union, medical devices follow the **Medical Device Regulation** (MDR) [4]. Laboratory tests follow the **In Vitro Diagnostic Regulation** (IVDR) [5].

The **EU AI Act** (2024) is the first broad law on AI [6]. Medical AI that needs independent review counts as **high-risk AI**. From August 2027, such tools must have:

- risk management across their whole life;
- checks for bias in training data;
- clear records and logging of use;
- clear instructions for users;
- human oversight built in;
- accuracy, robustness and security.

The AI Act adds to the MDR and IVDR; it does not replace them. The World Health Organization also sets principles for AI in health, including safety, transparency, accountability and fairness [7].

> **Local Context:** In Egypt, medical devices are regulated by the **Egyptian Drug Authority**, set up by Law No. 151 of 2019. Its definition of a medical device includes software for diagnosis, prevention, monitoring or treatment [8]. So AI tools used in Egyptian care fall under device rules, as well as the data rules in Chapter 10.

![Figure 11.1 — Lifecycle governance for AI medical software](rework/figures/orig-image24.png)
*Figure 11.1 — AI medical software moves from development and testing, through review, to use and ongoing monitoring.*

## 11.4 Liability: Who Is Responsible?
**Negligence** is the legal basis of most malpractice claims. A patient must show four things:

1. **Duty.** The professional owed the patient care.
2. **Breach.** The care fell below the accepted **standard of care**.
3. **Causation.** The breach caused the harm.
4. **Damages.** Real harm happened.

AI makes the second point harder. Legal experts suggest that, today, clinicians are safest when they follow standard care [9]. Risk rises when a clinician follows AI advice that departs from standard care and harm results.

Responsibility is usually shared (Figure 11.2). The clinician owns the clinical judgment. The hospital owns choosing, testing and monitoring the tool, and training staff. The maker owns the product's design, testing and warnings.

![Figure 11.2 — Shared responsibility for AI-assisted care](rework/figures/orig-image21.png)
*Figure 11.2 — Responsibility is shared between the clinician, the maker and the hospital.*

The **learned intermediary doctrine** is often misunderstood. A maker of medicines or devices usually meets its duty to warn by warning the prescribing clinician, not each patient. The clinician then advises the patient. This rule limits the maker's duty to warn patients directly. It is not a shield for clinicians.

## 11.5 The Human in the Loop
Amal's doctor was not careless by nature. She showed **automation bias** (Chapter 1): trusting the computer over her own eyes. It is common, especially on busy shifts [10].

**De-skilling** is a longer-term risk. In one study, doctors used to AI support in colonoscopy found fewer precancerous growths when they later worked without it [11]. Skills not practised can fade.

Many hope **explainable AI** (XAI) will help. It often uses heatmaps to show which parts of an image influenced the result. But a heatmap shows where the model looked, not whether it was right [12]. Explanations can even make people trust a wrong answer more [13].

What helps:

- *Design.* Show uncertainty, not just "low risk".
- *Workflow.* Make your own assessment before looking at the AI result.
- *Training.* Learn each tool's known weaknesses.
- *Culture.* Make it normal to override AI when the patient does not fit, and report every mismatch.
- *Monitoring.* Keep checking performance after the tool goes live.

## 11.6 Looking Ahead
AI will change daily work in every health profession. Doctors will spend less time on paperwork. Pharmacists will manage smarter alerts. Physiotherapists will supervise home programmes with movement data. Laboratory, imaging and public-health staff will run the quality checks that keep AI honest.

What AI cannot do is sit with a frightened patient, weigh personal values or take responsibility. These remain human tasks, and they are the heart of every health profession.

> **Through Four Lenses**
> - **Medicine:** Doctors remain responsible for clinical judgment. When a score conflicts with the examination, record the conflict, act on the patient and report the case.
> - **Pharmacy:** Pharmacists should check whether a dosing tool is a regulated device and tested locally. Unregulated calculators used for patient decisions carry extra risk.
> - **Physical Therapy:** Physiotherapists should know if a movement app is a medical device or a wellness product. Wellness apps may not meet clinical standards.
> - **Health Sciences:** Laboratory and imaging staff often do the monitoring after a tool goes live. Logging errors and equipment changes gives regulators the evidence they need.

> **Myth vs Evidence:** Myth: "If a tool is FDA-cleared, it has been proven in clinical trials." Evidence: Most AI devices are cleared through 510(k), and most were tested only on old data at few sites [2].

> **Safety Alert:** A "low risk" score never outweighs your own assessment of a patient who looks unwell. Act on the patient, record your reasoning and report the mismatch.

## Key Takeaways
- Software that diagnoses, monitors or treats can be a medical device, sorted by risk.
- US routes include 510(k), De Novo and PMA; change plans allow planned AI updates.
- The EU AI Act adds duties for high-risk AI, including human oversight.
- Responsibility is usually shared; the learned intermediary doctrine is not a clinician shield.
- Automation bias, de-skilling and over-trust in explanations need design, training and culture to manage.

## Self-Assessment
**Q1.** Which is most likely software as a medical device? [LO1]
A) A staff-rota app
B) Software that reads ECGs to detect atrial fibrillation
C) A canteen menu spreadsheet
D) A library catalogue

**Q2.** A company builds a new, low-to-moderate-risk AI tool with nothing similar on the US market. Which FDA route fits best? [LO2]
A) 510(k) clearance
B) Premarket approval only
C) No review needed
D) De Novo classification

**Q3.** What does a predetermined change control plan allow? [LO2]
A) Planned, pre-described updates without a new application for each
B) Unlimited changes without testing
C) Skipping testing for the first version
D) Selling without a label

**Q4.** An AI sepsis tool in the EU is a medical device that needs independent review. How does the AI Act classify it? [LO3]
A) Minimal-risk AI
B) Banned AI
C) High-risk AI
D) General-purpose AI only

**Q5.** Which is a duty for high-risk AI under the EU AI Act? [LO3]
A) Human oversight built into the design
B) Removing all documents
C) Using only unsupervised learning
D) Not logging use

**Q6.** A clinician follows AI advice that departs from standard care, and the patient is harmed. How does this compare with following standard care? [LO4]
A) It lowers legal risk.
B) It raises legal risk.
C) It has no legal effect.
D) It moves all responsibility to the patient.

**Q7.** What does the learned intermediary doctrine say? [LO4]
A) Clinicians are always liable for product defects.
B) AI companies can never be sued.
C) Patients must read all device manuals.
D) A maker usually meets its duty to warn by warning the prescribing clinician.

**Q8.** Amal's doctor accepted a "low risk" score despite borderline vital signs. What is this? [LO5]
A) De-skilling
B) Differential privacy
C) Automation bias
D) Federated learning

**Q9.** A heatmap highlights part of an X-ray. What can it reliably tell the clinician? [LO5]
A) That the model's reasoning is right
B) Which areas influenced the result, not whether the reasoning was valid
C) The diagnosis
D) That the model is calibrated

**Q10.** Doctors used to AI in colonoscopy later found fewer growths without it. What does this show? [LO5]
A) De-skilling
B) Data leakage
C) Distribution shift
D) Better training

**Case Question.** Use the four elements of negligence to analyse Amal's case. Then suggest two changes the hospital could make.

## Answers and Rationales
**Q1. B** — Reading ECGs to diagnose has a medical purpose [1]. A, C and D do not.

**Q2. D** — De Novo is for new low-to-moderate-risk devices. A needs a similar device. B is for high risk. C is wrong.

**Q3. A** — A PCCP describes planned changes and testing in advance [3]. B, C and D are false.

**Q4. C** — Medical AI needing independent review is high-risk [6]. A, B and D are wrong.

**Q5. A** — Human oversight is a core duty [6]. B, C and D contradict the Act.

**Q6. B** — Following AI away from standard care into harm raises risk [9]. A, C and D are wrong.

**Q7. D** — The doctrine is about the maker warning through the clinician. A and B misstate it. C is the opposite.

**Q8. C** — Trusting a computer over conflicting evidence is automation bias [10]. A is long-term skill loss. B and D are privacy methods.

**Q9. B** — Heatmaps show influence, not correctness [12, 13]. A, C and D overstate them.

**Q10. A** — Skill fell after relying on AI [11]. B, C and D are unrelated.

**Case Question — model answer.** Duty: the doctor and hospital owed Amal care. Breach: accepting "low risk" despite borderline signs and delaying review may fall below the standard of care. Causation: the delay likely contributed to septic shock. Damages: she needed intensive care. The hospital shares responsibility for choosing the tool and training staff. Two changes: show the model's uncertainty instead of "low risk", and require a bedside review for any abnormal vital signs, whatever the score.

## References
1. International Medical Device Regulators Forum. "Software as a Medical Device": possible framework for risk categorization and corresponding considerations. IMDRF/SaMD WG/N12FINAL. 2014. https://www.imdrf.org/documents/software-medical-device-possible-framework-risk-categorization-and-corresponding-considerations
2. Wu E, Wu K, Daneshjou R, et al. How medical AI devices are evaluated: limitations and recommendations from an analysis of FDA approvals. Nat Med. 2021;27(4):582-584. DOI: 10.1038/s41591-021-01312-x
3. US Food and Drug Administration. Marketing submission recommendations for a predetermined change control plan for artificial intelligence-enabled device software functions: final guidance. December 2024. https://www.fda.gov/regulatory-information/search-fda-guidance-documents/marketing-submission-recommendations-predetermined-change-control-plan-artificial-intelligence
4. European Parliament and Council. Regulation (EU) 2017/745 on medical devices. Off J Eur Union. 2017;L117:1-175. https://eur-lex.europa.eu/eli/reg/2017/745/oj
5. European Parliament and Council. Regulation (EU) 2017/746 on in vitro diagnostic medical devices. Off J Eur Union. 2017;L117:176-332. https://eur-lex.europa.eu/eli/reg/2017/746/oj
6. European Parliament and Council. Regulation (EU) 2024/1689 laying down harmonised rules on artificial intelligence (Artificial Intelligence Act). Off J Eur Union. 2024. https://eur-lex.europa.eu/eli/reg/2024/1689/oj
7. World Health Organization. Ethics and governance of artificial intelligence for health: WHO guidance. Geneva: WHO; 2021. https://www.who.int/publications/i/item/9789240029200
8. Arab Republic of Egypt. Law No. 151 of 2019 on the establishment of the Egyptian Drug Authority. Official Gazette No. 34 bis (A); 2019. https://www.eastlaws.com/legislation-full-text/en/egypt/law/25-08-2019/no-151?type=1&id=4747464
9. Price WN, Gerke S, Cohen IG. Potential liability for physicians using artificial intelligence. JAMA. 2019;322(18):1765-1766. DOI: 10.1001/jama.2019.15064
10. Goddard K, Roudsari A, Wyatt JC. Automation bias: a systematic review of frequency, effect mediators, and mitigators. J Am Med Inform Assoc. 2012;19(1):121-127. DOI: 10.1136/amiajnl-2011-000089
11. Budzyń K, Romańczyk M, Kitala D, et al. Endoscopist deskilling risk after exposure to artificial intelligence in colonoscopy: a multicentre, observational study. Lancet Gastroenterol Hepatol. 2025;10(10):896-903. DOI: 10.1016/S2468-1253(25)00133-5
12. Adebayo J, Gilmer J, Muelly M, et al. Sanity checks for saliency maps. In: Advances in Neural Information Processing Systems 31. 2018. https://arxiv.org/abs/1810.03292
13. Ghassemi M, Oakden-Rayner L, Beam AL. The false hope of current approaches to explainable artificial intelligence in health care. Lancet Digit Health. 2021;3(11):e745-e750. DOI: 10.1016/S2589-7500(21)00208-9


---

# Glossary

**Academic integrity** — Honesty in study and assessment, including acknowledging when AI tools were used and not presenting their output as one's own work.

**Accuracy** — The share of all cases a model classifies correctly; misleading when a condition is rare.

**Acute kidney injury** — A rapid fall in kidney function over hours or days, usually detected by a rising creatinine (AKI).

**Adversarial attack** — A small, deliberate change to an input, often invisible to people, crafted to make a specific model give a wrong output.

**Alarm fatigue** — Reduced response to monitoring alarms and alerts after exposure to many false or low-value ones.

**Alert fatigue** — Declining attention to computer alerts after seeing many, often low-value, alerts; leads to important alerts being overridden.

**Algorithmic bias** — Systematically worse performance or recommendations from a model for some groups of people.

**Ambient scribe** — An AI system that listens, with consent, to a consultation and drafts the clinical note for the clinician to review.

**Anonymisation** — Processing data so that individuals can no longer be identified by any reasonable means; hard to achieve for rich health data.

**Anterior cruciate ligament** — A ligament inside the knee that stops the shin bone sliding forward and helps the knee resist twisting (ACL).

**Area under the concentration–time curve** — The total exposure of the body to a drug over a period, used to guide doses of drugs such as vancomycin (AUC).

**Area under the precision–recall curve** — A summary of how precision (PPV) and recall (sensitivity) trade off across thresholds; more informative than AUROC for rare conditions (AUPRC).

**Area under the ROC curve** — The probability that a model scores a random patient with the condition higher than a random patient without it; ranges from 0.5 (chance) to 1.0 (perfect) (AUROC, C-statistic).

**Artificial intelligence** — The broad goal of building computer systems that perform tasks linked with human thinking, such as recognising images, understanding language and predicting outcomes.

**Automation bias** — The tendency to accept a computer's output even when other evidence or one's own judgment disagrees.

**Bias** — A systematic error that makes a model perform better or worse for some groups, settings or cases than others.

**Biopsy** — A small sample of tissue removed for examination under a microscope.

**Calibration** — How closely a model's predicted risks match observed event rates; a calibrated "20% risk" means about 20 in 100 similar patients have the event.

**Class imbalance** — A situation in which one outcome is much rarer than another in the data, such as cancer in screening images.

**Clinical decision support** — Software that gives a health professional advice at the moment of a decision, such as drug-interaction warnings or abnormal-result alerts.

**Closed-loop system** — A system that measures a value, such as glucose, and automatically adjusts treatment, such as insulin, in a continuous feedback loop.

**Computer-aided detection** — Imaging AI that marks where a possible finding is, leaving interpretation to the reader (CADe).

**Computer-aided diagnosis** — Imaging AI that characterises a finding, for example as likely malignant or benign (CADx).

**Computer-aided triage** — Imaging AI that reorders the reading list so suspected urgent cases are read first (CADt).

**Confusion matrix** — A 2 × 2 table comparing a model's positive and negative outputs with the true condition.

**Convolutional neural network** — A neural network designed for images; early layers detect edges and textures, later layers detect shapes (CNN).

**CT** — Computed tomography: an imaging method that combines many X-ray views into cross-sectional slices.

**Data leakage** — Information that would not be available in real use reaching the training or testing of a model, making it look better than it is.

**De-identification** — Removing or altering details that could identify a person, such as the 18 identifiers of the US HIPAA Safe Harbor method.

**De-skilling** — Loss of a professional skill that is no longer practised because a tool performs it.

**Deep learning** — Machine learning with neural networks of many layers, able to learn complex features from images, sound and text.

**Diagnostic test** — A test used when symptoms or signs already raise suspicion of a condition.

**Dice coefficient** — An overlap measure between a model's outline and the true outline: twice the overlap divided by the total size of both; 0 to 1.

**DICOM** — The international standard for storing and exchanging medical images together with their metadata.

**Differential privacy** — A method that adds measured random noise to data or results, giving a mathematical, tunable limit (set by ε) on what can be learned about any one person.

**Digital pathology** — Scanning glass slides into digital images for viewing and analysis on a computer.

**Discrimination** — A model's ability to rank patients, giving higher scores to those with the condition.

**Distribution shift** — A difference between the data a model was trained on and the data it meets in use, such as new patients, machines or practices.

**Drug interaction** — A change in the effect of a medicine caused by another medicine, food or supplement.

**Drug target** — A molecule in the body, usually a protein, that a medicine is designed to act on.

**Early warning score** — A rule-based score that adds points for abnormal vital signs to flag patients at risk of deterioration, such as NEWS2.

**Egyptian Drug Authority** — The Egyptian regulator for medicines and medical devices, including medical software, established by Law No. 151 of 2019 (EDA).

**Electrocardiogram** — A recording of the heart's electrical activity (ECG).

**Electronic health record** — The digital version of a patient's chart, holding diagnoses, medicines, results, notes and appointments.

**EU AI Act** — Regulation (EU) 2024/1689, the European Union's law on artificial intelligence, which sets obligations for high-risk AI systems, including many medical devices.

**Explainable AI** — Methods that show which inputs influenced a model's output, such as heatmaps; they show where a model looked, not whether it reasoned correctly (XAI).

**External validation** — Testing a model on data from a different hospital, time period or population from the one used to develop it.

**Federated learning** — Training a shared model across several sites, each using its own data and sending only model updates, so raw patient data do not move.

**Fitzpatrick scale** — A classification of skin types from I (always burns) to VI (deeply pigmented, rarely burns).

**Gait cycle** — The sequence of movements from one heel strike to the next heel strike of the same foot, with stance and swing phases.

**GDPR** — The European Union's General Data Protection Regulation, which treats health data as a special category needing extra protection.

**Generative AI** — AI that produces new content such as text, images or code.

**Good machine learning practice** — Ten guiding principles agreed by US, Canadian and UK regulators for developing medical AI (GMLP).

**Gradient descent** — The training method that repeatedly nudges a model's parameters in the direction that reduces its loss.

**Haemolysis** — Breakdown of red blood cells in a sample, which releases their contents and can distort results such as potassium.

**Hallucination** — Fluent output from a generative model that is false or unsupported, such as an invented drug dose or reference.

**Haptic boundary** — A software limit that stops a robotic tool from moving outside a planned zone, used for example in joint-replacement surgery.

**Heatmap** — A colour overlay showing which regions of an image contributed most to a model's output.

**High-risk AI** — Under the EU AI Act, AI systems with significant potential to harm health, safety or rights, such as medical devices needing notified-body review.

**HIPAA** — The US Health Insurance Portability and Accountability Act, whose Privacy Rule governs health information held by providers and insurers.

**Icterus** — High bilirubin in a sample, giving it a yellow colour that can interfere with some tests.

**In Vitro Diagnostic Regulation** — The EU regulation for laboratory tests and related software (IVDR, Regulation 2017/746).

**Inertial measurement unit** — A sensor combining an accelerometer and a gyroscope that records acceleration and rotation; found in most wearables (IMU).

**Internal validation** — Testing a model on a held-out part of the same dataset used to develop it.

**Interoperability** — The ability of different health information systems to exchange data and use it correctly.

**Intersection over union** — An overlap measure: the shared area of two outlines divided by their combined area; 0 to 1 (IoU).

**Label** — The correct answer attached to a training example, such as "pneumonia present" for a chest X-ray.

**Label noise** — Errors in the labels a model is trained on; the model learns these errors too.

**Large language model** — A generative model trained on very large amounts of text to predict the next word; the engine behind chatbots.

**Leader–follower telemanipulation** — A robotic surgery set-up in which the surgeon's hand movements at a console lead and the robot's instruments follow.

**Learned intermediary doctrine** — A product-liability rule under which a manufacturer usually meets its duty to warn about risks by warning the prescribing clinician rather than each patient.

**Lipaemia** — High fat content in a sample, making it cloudy and able to interfere with some tests.

**Loss function** — A formula that measures how wrong a model's predictions are during training.

**Machine learning** — A way of building AI in which the computer learns patterns from example data instead of following hand-written rules.

**Medical device** — Any instrument, machine, implant or software intended for a medical purpose, such as diagnosis, monitoring or treatment.

**Medical Device Regulation** — The EU regulation for medical devices, including most medical software (MDR, Regulation 2017/745).

**Metadata** — Data about data, such as the scanner model, hospital and date stored with a medical image.

**Model** — The mathematical function produced by machine learning that turns an input (for example, an image) into an output (for example, a risk score).

**Model-informed precision dosing** — Dosing that combines a pharmacokinetic model with an individual patient's drug levels and characteristics to recommend a dose (MIPD).

**Motion scaling** — A robotic feature that turns a large hand movement into a smaller, more precise instrument movement.

**MRI** — Magnetic resonance imaging: an imaging method using a strong magnet and radio waves, good for soft tissues and free of ionising radiation.

**Negative predictive value** — The share of negative results that are truly negative (NPV).

**Negligence** — Failure to meet the expected standard of care, causing harm; requires duty, breach, causation and damages.

**Neural network** — A model made of layers of simple connected units whose connection strengths are adjusted during training.

**Notified body** — An independent organisation designated in the EU to assess whether a medical device meets legal requirements.

**Objective Structured Assessment of Technical Skills** — A validated rating scale for surgical technical skill (OSATS).

**Oculomics** — Research using eye images, such as retinal photographs, to detect signs of disease elsewhere in the body.

**Omics** — Data describing molecules in the body, such as genomics (DNA) and pharmacogenomics (genes affecting drug response).

**Overfitting** — When a model learns the quirks and noise of its training data so closely that it performs poorly on new data.

**Parameter** — One of the adjustable numbers inside a model that training changes.

**Personal Data Protection Law** — Egypt's Law No. 151 of 2020, which treats health data as sensitive personal data requiring explicit consent and stronger security.

**Pharmacogenomics** — The study of how a person's genes affect their response to medicines.

**Pharmacovigilance** — The monitoring of medicines after approval to detect, assess and prevent adverse effects.

**Pose estimation** — A computer-vision task that locates body key points, such as joints, in images or video.

**Positive predictive value** — The share of positive results that are truly positive; depends strongly on prevalence (PPV, precision).

**Predetermined change control plan** — A plan, authorised by the FDA in advance, describing the changes a maker may make to an AI device and how they will be tested (PCCP).

**Premarket approval** — The FDA's most demanding route to market, for high-risk devices, usually requiring clinical evidence (PMA).

**Prevalence** — How common a condition is in the group being tested.

**Pseudonymisation** — Replacing identifiers with codes while a key allows re-linking; pseudonymised data remain personal data under GDPR.

**Randomised controlled trial** — A study in which patients or sites are randomly assigned to different care, such as with or without AI, to measure its effect (RCT).

**Range of motion** — How far a joint can move, measured in degrees.

**Re-identification** — Working out who a person is from data that were meant to be de-identified, often by combining several ordinary details.

**Reinforcement learning** — Learning by taking actions and receiving rewards or penalties.

**Reporting guideline** — A checklist of what a research paper should report, such as TRIPOD+AI for prediction models or CONSORT-AI for AI trials.

**Retinal photograph** — A photograph of the back of the eye showing the retina and its blood vessels (fundus photograph).

**Retrieval-augmented generation** — A method in which an LLM first retrieves passages from trusted documents and then answers using them, so that sources can be shown (RAG).

**Robotic exoskeleton** — A powered wearable frame that supports or moves the limbs, used for example in gait rehabilitation.

**ROC curve** — A plot of sensitivity against 1 − specificity across all possible thresholds.

**Rule-based system** — Software that follows rules written by people, such as "if drug A and drug B, then warn".

**Screening** — Testing people without symptoms to find disease early.

**Sensitivity** — The share of people with a condition whom a test correctly identifies (recall).

**Sepsis** — A life-threatening reaction to infection in which the body's response damages its own organs.

**Septic shock** — The most severe stage of sepsis, with persistently low blood pressure needing drug support.

**Shortcut learning** — When a model relies on an easy cue that predicts the label in training data but is unrelated to the real task, such as a scanner marker.

**Software as a medical device** — Software intended for a medical purpose, such as diagnosis or monitoring, that is itself a medical device without being part of hardware (SaMD).

**Specificity** — The share of people without a condition whom a test correctly clears.

**Standard of care** — The level of care that a reasonably competent professional would provide in the same circumstances.

**Structured data** — Data that fit into rows and columns, such as laboratory values, codes and prescriptions.

**Supervised learning** — Learning from examples that come with correct answers (labels).

**Surgical data science** — The collection and analysis of data from surgery, such as video and instrument movements, to improve care.

**Telerehabilitation** — Rehabilitation delivered remotely, often by live video.

**Test set** — Data kept aside and used once, at the end, to estimate how a model will perform on new cases.

**Threshold** — The score above which a model's output is treated as positive.

**Token** — A small piece of text, such as a word or part of a word, that a language model reads and predicts.

**Training data** — The examples a machine-learning model learns from.

**Training set** — The data used to adjust a model's parameters.

**Transformer** — The neural-network design behind modern LLMs; its attention mechanism weighs all earlier words when predicting the next one.

**Tremor filtering** — A robotic feature that removes the small natural shake of the surgeon's hands (physiological tremor, about 8–12 Hz).

**Type 1 diabetes** — A form of diabetes in which the body makes no insulin, so insulin must be replaced every day.

**U-Net** — A convolutional neural network that outlines structures pixel by pixel in an image (segmentation).

**Unstructured data** — Data without a fixed table format, such as images, signals and free text.

**Unsupervised learning** — Learning that finds structure, such as groups, in data without labels.

**Validation set** — Data used during development to tune design choices and decide when to stop training.

**Wearable** — A device worn on the body, such as a wrist band or sensor, that records signals like movement or heart rate.

**Whole-slide image** — A very high-resolution digital scan of an entire pathology slide (WSI).

**X-ray** — An imaging method that passes ionising radiation through the body; dense tissues such as bone appear white.
