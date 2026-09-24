# Chapter 1: What AI Is — and Isn't

## Opening Case
It is 11 p.m. Lina Osei, a 20-year-old biology student, notices that the mole on her forearm looks larger. One edge seems darker than before. She does not want to wait for a clinic. She opens a chatbot on her phone and types, "Is this mole cancer?" She uploads a photo.

The reply arrives in two seconds. It is calm, fluent and kind. It lists the warning signs of melanoma. It says her mole "shows some features of concern" and advises her to see a doctor. Lina feels both reassured and frightened.

The next morning she shows the reply to a community pharmacist. The pharmacist asks a simple question: "What exactly looked at your photo, and how does it know?" This chapter answers that question.

## Learning Objectives
By the end of this chapter you will be able to:
1. [LO1] Distinguish artificial intelligence, machine learning, deep learning and generative AI.
2. [LO2] Contrast a rule-based system with a learned model using a health example.
3. [LO3] Describe four milestones in the history of AI in health care.
4. [LO4] Identify one realistic benefit and one realistic risk of AI for each health profession.

## 1.1 Four Words You Will Hear Every Day
**Artificial intelligence** (AI) is the broad goal of building computer systems that perform tasks we link with human thinking. Examples are recognising images, understanding language and making predictions.

**Machine learning** (ML) is one way to reach that goal. Instead of following rules written by a person, the computer learns patterns from examples. The examples are called **training data**. The result of learning is a **model**: a mathematical function that turns an input into an output.

**Deep learning** is a type of machine learning that uses a **neural network** with many layers. Each layer transforms the data a little. Together, the layers can learn very complex patterns. Deep learning is good with images, sound and text, because it finds useful features by itself.

**Generative AI** produces new content, such as text, images or computer code. A **large language model** (LLM) is a generative model trained on huge amounts of text. The chatbot that answered Lina is an LLM.

![Figure 1.1 — Nested fields of AI](figures/orig-image2.png)
*Figure 1.1 — Artificial intelligence contains machine learning, which contains deep learning. Generative AI and large language models are built with deep learning. Illustrative.*

These terms nest inside each other, as Figure 1.1 shows. Every LLM is a deep-learning model. Not every AI system is a deep-learning model.

## 1.2 Rules Versus Learning
Older computer programs in health care were **rule-based system**s. A person writes each rule. For example: "If the patient takes warfarin and a new prescription contains aspirin, show a bleeding-risk warning." The logic is transparent. Anyone can read the rule and check it. But rules break when reality is messier than the rule writer imagined.

A learned model works differently. It sees thousands of past prescriptions and outcomes. It learns which combinations of drugs, doses, ages and kidney function were followed by bleeding. It then gives a risk score for a new prescription. It can capture patterns no person wrote down. It can also learn patterns that are wrong, biased or accidental. You cannot read its logic line by line.

Neither approach is always better. In many clinical prediction tasks, simple statistical models perform as well as complex machine learning [7]. Chapter 3 returns to this point.

> **Medical Background in 60 Seconds:** A **clinical decision support** system is software that gives a health professional advice at the moment of a decision. Examples are drug-interaction warnings in a pharmacy system, reminders for overdue vaccines and alerts for abnormal laboratory results. Some use rules. Some use machine learning.

## 1.3 A Short History
**1956 — the name.** A summer workshop at Dartmouth College in the United States gave the field its name. The 1955 proposal claimed that "every aspect of learning" could in principle be simulated by a machine [1]. Early optimism was high. Progress was slower than promised.

**1970s — expert systems.** At Stanford, MYCIN used about 600 hand-written rules to recommend antibiotics for blood infections [2]. In tests, its advice compared well with that of specialists. It was never used in routine care. Computers were not at the bedside, and no one had settled who would be responsible for its advice. This lesson still matters: good performance in a study does not guarantee use in practice.

**2012 — deep learning takes off.** A deep neural network won a large image-recognition competition by a wide margin [3]. Better computer chips and large image collections made this possible. Medicine soon followed. In 2016 a deep-learning model graded diabetic eye disease from retinal photographs with high accuracy in a retrospective study [4].

**2018 — the first autonomous diagnostic device.** The US Food and Drug Administration authorised an AI system that screens retinal photos for diabetic eye disease without a specialist reading them [5]. It was tested prospectively in primary-care clinics. This was a turning point: AI made the screening decision itself.

**2020s — generative AI.** In 2021 AlphaFold predicted protein structures with near-experimental accuracy [9]. From 2022, LLMs such as ChatGPT reached the public. Health professionals now use them to draft notes, summarise papers and explain conditions to patients [10].

## 1.4 What AI Can and Cannot Do Today
AI is strong at narrow, well-defined tasks with lots of examples. It can sort, detect, measure and predict. A large Swedish randomised trial of breast screening is a good example [8]. When AI helped read mammograms, the screen-reading workload fell by 44%. About 20% more cancers were detected, and false-positive recalls did not rise.

AI is weak at tasks it has never seen. It has no common sense and no understanding of a patient's life. A model trained in one hospital may fail in another. An LLM can write a confident answer that is false. It cannot examine a patient, notice fear in a voice or take responsibility for a decision.

The honest summary is this: AI is a powerful tool with a narrow field of vision [6]. It works best as part of a team.

> **Through Four Lenses**
> - **Medicine:** Physicians meet AI in image reading, risk scores and note writing. The benefit is faster, more consistent detection. The risk is trusting a score without checking the patient.
> - **Pharmacy:** Pharmacists meet AI in interaction checks, dosing tools and drug-information chatbots. The benefit is catching dangerous combinations. The risk is alert fatigue and fluent but wrong answers.
> - **Physical Therapy:** Physiotherapists meet AI in video movement analysis, wearables and home exercise apps. The benefit is objective progress measures. The risk is a model trained on athletes misjudging older or injured bodies.
> - **Health Sciences:** Laboratory and imaging technologists meet AI in automated analysers, slide scanners and image quality checks. The benefit is speed and consistency. The risk is silent failure after equipment changes.

## 1.5 Three Risks to Watch
This book returns to three risks again and again.

First, **bias**. A model learns from past data. If the data under-represent some groups, the model may perform worse for them. Chapter 10 covers this.

Second, **hallucination**. An LLM predicts plausible words. It does not check facts. It can invent a drug dose or a journal article. Chapter 5 covers this.

Third, **automation bias**. People tend to accept a computer's answer, even when their own judgment disagrees. Chapter 11 covers this.

Lina's chatbot illustrates all three. It may not have learned from many photos of dark skin. It wrote fluent text, not a checked diagnosis. And its calm tone made her trust it. The pharmacist was right to ask how it knew.

> **Myth vs Evidence:** Myth: "AI will soon replace clinicians." Evidence: AI performs well on narrow tasks, such as screening images, but it has not replaced professional judgment. Even in the largest screening trial, AI changed the reading workflow; radiologists still made the final decisions [8].

> **Safety Alert:** A chatbot's answer is not a diagnosis. Any changing mole, new symptom or medicine question needs a qualified health professional. Tell patients this clearly and kindly.

## Key Takeaways
- AI is the broad goal; machine learning learns from data; deep learning uses many-layered neural networks; generative AI creates new content.
- Rule-based systems are transparent but brittle. Learned models are flexible but harder to inspect.
- History shows that good test results do not guarantee safe, real-world use.
- AI is strong at narrow, data-rich tasks and weak outside the conditions it learned.
- Bias, hallucination and automation bias affect every profession.

## Self-Assessment
**Q1.** A pharmacy system shows a warning whenever warfarin and aspirin appear on the same prescription. A programmer wrote this condition by hand. What kind of system is this? [LO2]
A) A deep-learning model
B) A rule-based system
C) A large language model
D) An unsupervised clustering model

**Q2.** Which statement about the relationship between these terms is correct? [LO1]
A) Machine learning includes artificial intelligence as a subtype.
B) Every AI system uses a neural network.
C) Generative AI is unrelated to deep learning.
D) Deep learning is a type of machine learning.

**Q3.** MYCIN performed well in tests in the 1970s but was never used in routine care. What is the main lesson for today's AI tools? [LO3]
A) Good study performance does not guarantee real-world adoption and safe use.
B) Rule-based systems are always less accurate than learned models.
C) Antibiotic prescribing cannot be supported by computers.
D) Expert systems were banned by regulators.

**Q4.** A physiotherapy clinic buys an app that scores knee movement from phone videos. It was trained only on young athletes. Karim is 34 and a manual worker with an injured knee. Which risk is most important? [LO4]
A) Hallucination of a drug dose
B) Loss of patient privacy through the pharmacy system
C) Poor performance on people unlike those in the training data
D) The app will refuse to work on videos

**Q5.** A student says, "The chatbot is an LLM, so it checks medical facts before answering." What is wrong with this statement? [LO1]
A) LLMs cannot produce text.
B) LLMs predict plausible text and do not check facts by design.
C) LLMs only work with images.
D) LLMs always refuse medical questions.

**Q6.** What happened in 2018 that marked a turning point for AI in health care? [LO3]
A) An autonomous AI system for diabetic eye screening was authorised in the United States.
B) The term "artificial intelligence" was first used.
C) AlphaFold solved protein structures.
D) MYCIN entered routine hospital use.

**Q7.** In the MASAI breast-screening trial, what did AI support achieve? [LO4]
A) It replaced radiologists entirely.
B) It reduced cancer detection but saved time.
C) It halved the number of women screened.
D) It reduced screen-reading workload by 44% while detecting more cancers.

**Q8.** Which feature best describes an advantage of a learned model over a rule-based system? [LO2]
A) Its logic can be read line by line.
B) It never makes errors.
C) It can capture patterns that no person wrote down.
D) It needs no data.

**Q9.** A laboratory analyser's AI works well for months. Then the reagent supplier changes, and error rates rise without any warning. Which risk from this chapter does this show? [LO4]
A) Silent failure when conditions change from those the model learned
B) Hallucination of references
C) Automation bias in patients
D) A rule written incorrectly by a programmer

**Q10.** What was a key enabler of the deep-learning breakthrough around 2012? [LO3]
A) New laws requiring AI in hospitals
B) Faster computer chips and large collections of labelled images
C) The invention of rule-based systems
D) The end of the Dartmouth workshop

**Case Question.** Lina shows you the chatbot's answer about her mole. In four or five sentences, explain to her what kind of system produced the answer, one reason it might be wrong for her, and what she should do next.

## Answers and Rationales
**Q1. B** — A condition written by a person is a rule. A and D learn from data. C generates text.

**Q2. D** — Deep learning is a subtype of machine learning. A reverses the nesting. B is false because rule-based AI exists. C is false because generative AI is built with deep learning.

**Q3. A** — MYCIN was never adopted because of practical and responsibility barriers, not poor accuracy. B overgeneralises. C is false. D did not happen.

**Q4. C** — A model trained on one group may fail on people who differ from it. A concerns LLMs. B is unrelated. D is not the main risk.

**Q5. B** — LLMs generate the most plausible next words; fact-checking is not built in. A, C and D are false.

**Q6. A** — In 2018 the FDA authorised an autonomous diabetic-retinopathy screening system [5]. B happened in 1956. C happened in 2021. D never happened.

**Q7. D** — Workload fell by 44% and detection rose by about 20% [8]. A and C are false. B reverses the finding.

**Q8. C** — Learned models find patterns from examples. A describes rule-based systems. B and D are false.

**Q9. A** — A change in inputs caused a silent drop in performance. B and C are unrelated. D is wrong because the system learned, not followed a written rule.

**Q10. B** — Better hardware and large labelled image sets made deep learning practical [3]. A, C and D are wrong.

**Case Question — model answer.** The answer came from a large language model, which writes plausible text but does not check facts or examine skin. It may have learned mostly from images of light skin, so it may misjudge a mole on dark skin. Its fluent tone can make it sound more certain than it is. A changing mole should be examined by a clinician, ideally a dermatologist, soon. The chatbot's advice to see a doctor is the part to follow.

## References
1. McCarthy J, Minsky ML, Rochester N, Shannon CE. A proposal for the Dartmouth summer research project on artificial intelligence. 1955. http://jmc.stanford.edu/articles/dartmouth/dartmouth.pdf
2. Shortliffe EH. Design considerations for MYCIN. In: Computer-Based Medical Consultations: MYCIN. Elsevier; 1976:63-78. DOI: 10.1016/b978-0-444-00179-5.50008-1
3. Krizhevsky A, Sutskever I, Hinton GE. ImageNet classification with deep convolutional neural networks. Commun ACM. 2017;60(6):84-90. DOI: 10.1145/3065386
4. Gulshan V, Peng L, Coram M, et al. Development and validation of a deep learning algorithm for detection of diabetic retinopathy in retinal fundus photographs. JAMA. 2016;316(22):2402-2410. DOI: 10.1001/jama.2016.17216
5. Abràmoff MD, Lavin PT, Birch M, et al. Pivotal trial of an autonomous AI-based diagnostic system for detection of diabetic retinopathy in primary care offices. NPJ Digit Med. 2018;1:39. DOI: 10.1038/s41746-018-0040-6
6. Topol EJ. High-performance medicine: the convergence of human and artificial intelligence. Nat Med. 2019;25(1):44-56. DOI: 10.1038/s41591-018-0300-7
7. Christodoulou E, Ma J, Collins GS, et al. A systematic review shows no performance benefit of machine learning over logistic regression for clinical prediction models. J Clin Epidemiol. 2019;110:12-22. DOI: 10.1016/j.jclinepi.2019.02.004
8. Lång K, Josefsson V, Larsson AM, et al. Artificial intelligence-supported screen reading versus standard double reading in the Mammography Screening with Artificial Intelligence trial (MASAI): a clinical safety analysis of a randomised, controlled, non-inferiority, single-blinded, screening accuracy study. Lancet Oncol. 2023;24(8):936-944. DOI: 10.1016/s1470-2045(23)00298-x
9. Jumper J, Evans R, Pritzel A, et al. Highly accurate protein structure prediction with AlphaFold. Nature. 2021;596(7873):583-589. DOI: 10.1038/s41586-021-03819-2
10. Thirunavukarasu AJ, Ting DSJ, Elangovan K, et al. Large language models in medicine. Nat Med. 2023;29(8):1930-1940. DOI: 10.1038/s41591-023-02448-8
