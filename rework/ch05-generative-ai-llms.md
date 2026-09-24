# Chapter 5: Generative AI and Large Language Models

## Opening Case
Lina is waiting for her dermatology appointment. She is anxious, so she types into a free chatbot: "I'm 20, I have a mole that changed shape, I've had headaches this week and I feel tired. Do I have cancer that has spread?" The chatbot replies with a long, warm answer. It lists possible causes of headache. It mentions that melanoma "can spread to the brain". It suggests two supplements and cites a journal article.

Lina shows the answer to the community pharmacist. The pharmacist checks the article. It does not exist. One supplement interacts with the contraceptive pill Lina takes.

The same afternoon, the pharmacist uses an approved hospital chatbot to draft a leaflet on sun protection. It saves her an hour. She checks every sentence before printing. Why was the tool dangerous in one case and helpful in the other? This chapter explains.

## Learning Objectives
By the end of this chapter you will be able to:
1. [LO1] Explain next-token prediction and why it produces hallucinations.
2. [LO2] Identify safe and unsafe uses of LLMs for students and health professionals.
3. [LO3] Apply a safe-use checklist, including protection of patient data and checking against primary sources.
4. [LO4] Describe retrieval-augmented generation and ambient clinical documentation.
5. [LO5] Evaluate an LLM answer for accuracy, completeness and bias.

## 5.1 How a Large Language Model Works
A **large language model** is trained to do one thing: predict the next piece of text. Text is split into small pieces called **token**s. A token is a word or part of a word. During training, the model reads billions of sentences. Again and again, it guesses the next token and adjusts its parameters when it is wrong (Chapter 3).

The design behind modern LLMs is the **transformer** [5]. Its key feature, called attention, lets the model weigh every earlier word when choosing the next one. This is how it keeps track of meaning across long passages.

After this first stage, the model is often fine-tuned. People rate its answers, and the model is adjusted to give answers people prefer. This makes it more helpful and polite. It does not make it more truthful.

When you ask a question, the model writes an answer one token at a time (Figure 5.1). Each token is the one that seems most likely to follow, given your question and the words already written.

![Figure 5.1 — Next-token prediction](figures/next-token.svg)
*Figure 5.1 — An LLM writes by repeatedly choosing a likely next token. It predicts plausible text; it does not look up facts unless connected to a source. Illustrative.*

## 5.2 Why LLMs Hallucinate
An LLM predicts what text usually looks like. It has no built-in check of whether the text is true. When it lacks knowledge, it still produces fluent, confident text. This is a **hallucination** [4].

Hallucinations are dangerous in health care because they look exactly like correct answers. When researchers asked a chatbot to write medical articles with references, almost half of the references were invented. Most of the rest contained errors. Only 7% were both real and accurate [2]. The article cited to Lina was one of these inventions.

LLMs also inherit problems from their training text. A study asked four major LLMs questions based on debunked, race-based medical ideas, such as race-based kidney-function formulas. All four repeated some of these harmful claims [9].

## 5.3 Exam Scores Are Not Clinical Safety
LLMs have passed medical licensing-style exams. ChatGPT reached near the passing level of the US licensing exam [3]. Google's Med-PaLM reached 67.6% on a set of exam-style questions, and Med-PaLM 2 reached 86.5% [1, 6].

These results show strong medical knowledge. They do not show safety in care. Exam questions are tidy, complete and have one right answer. Real patients bring missing information, mixed symptoms, fear and competing priorities. An exam does not test whether a model notices what is missing, admits uncertainty or recognises an emergency.

> **Medical Background in 60 Seconds:** A **drug interaction** happens when one medicine, food or supplement changes the effect of another. Some supplements, such as St John's wort, speed up the liver's breakdown of hormonal contraceptives. This can make the pill less effective and lead to pregnancy. Pharmacists check for interactions whenever a new product is added.

## 5.4 Useful Applications
**Documentation.** An **ambient scribe** listens, with consent, to a consultation and drafts the clinical note. In one large health system, thousands of physicians used ambient scribes across hundreds of thousands of visits. Users reported less time on documentation and more attention to patients [11]. The clinician must still review and sign every note.

**Patient communication.** In one study, health professionals compared chatbot and physician replies to patient questions posted online. They preferred the chatbot's replies in 79% of ratings, for both quality and empathy [8]. The questions came from a public forum, not real clinical care, and the evaluators judged writing, not patient outcomes.

**Drug information and education.** LLMs can explain a mechanism, summarise a guideline or generate practice questions. They are good tutors for concepts. They are poor sources for doses, interactions and recent evidence unless connected to a trusted source.

**Retrieval-augmented generation.** In **retrieval-augmented generation** (RAG), the system first searches a trusted collection of documents, such as a hospital formulary or national guideline. It then gives those passages to the LLM and asks it to answer from them [10]. RAG reduces hallucination and allows the answer to show its sources. It does not remove errors completely, because the model can still misread or ignore the passages.

## 5.5 Using LLMs Safely: A Checklist
1. **Protect patient data.** Never paste names, record numbers, dates of birth, photos or other identifiable details into a public chatbot. Use only tools approved by your institution.
2. **Use LLMs for drafts, not decisions.** A draft note, leaflet or summary is a starting point that you check.
3. **Verify every clinical fact.** Check it against a primary source: the product information, a guideline or the original paper.
4. **Check every reference.** Search for it. If you cannot find it, it may not exist.
5. **Watch for missing information.** Ask what the answer did not consider, such as pregnancy, kidney function or other medicines.
6. **Be alert to bias.** Question answers that use race, sex or age in ways that current guidelines do not.
7. **Stay within your scope.** An LLM does not change who is responsible for advice. You are.

For students, the same tools raise questions of **academic integrity**. Follow your faculty's policy. Using an LLM to explain a concept is usually allowed. Submitting its text as your own work is usually not.

The World Health Organization has published guidance on the ethics and governance of these models in health, covering transparency, data protection and accountability [7].

> **Through Four Lenses**
> - **Medicine:** Physicians can use approved scribes to save documentation time. They must read every draft note, because an invented examination finding becomes part of the legal record once it is signed.
> - **Pharmacy:** Pharmacists will see patients arrive with chatbot advice. They should check doses and interactions against product information, and explain calmly why a fluent answer can still be wrong.
> - **Physical Therapy:** Physiotherapists can use LLMs to draft home-exercise sheets in plain language. They must check each exercise for safety and fit, because the model does not know the patient's injury.
> - **Health Sciences:** Public-health officers can use LLMs to draft campaign messages in several languages. They should test messages with the community, because models may miss cultural meaning.

> **Myth vs Evidence:** Myth: "If an LLM passes a medical exam, it is safe to advise patients." Evidence: Exam performance reflects knowledge on tidy questions [1, 3]. The same models can invent references [2] and repeat harmful race-based claims [9]. Safety in care needs different testing.

> **Safety Alert:** Never enter identifiable patient information into a public chatbot, and never act on a chatbot's dose or interaction advice without checking an authoritative source.

## Key Takeaways
- LLMs predict the next token; they generate plausible text, not verified facts.
- Hallucinations are fluent and confident, including invented references.
- High exam scores do not prove safety in real care.
- Ambient scribes, patient messages and RAG are useful when a professional checks the output.
- Protect patient data, verify facts and references, and keep responsibility for every decision.

## Self-Assessment
**Q1.** What is a large language model fundamentally trained to do? [LO1]
A) Look up facts in a medical database
B) Predict the next token in a sequence of text
C) Examine patients through a camera
D) Calculate drug doses from blood tests

**Q2.** An LLM gives a student a reference to a paper that does not exist. What is the best explanation? [LO1]
A) The paper was withdrawn from the journal.
B) The student's internet connection failed.
C) The model was attacked by hackers.
D) The model generated plausible text without checking that the paper exists.

**Q3.** A nurse wants to paste a patient's full name, record number and discharge letter into a free public chatbot to get a summary. What should a colleague advise? [LO3]
A) Do not paste identifiable data into a public tool; use an approved system or remove identifiers.
B) It is fine if the summary is checked afterwards.
C) It is fine because chatbots delete everything.
D) It is fine if the patient is discharged.

**Q4.** A hospital connects an LLM to its own drug formulary so that answers quote the formulary. What is this approach called? [LO4]
A) Reinforcement learning
B) Adversarial training
C) Retrieval-augmented generation
D) Unsupervised clustering

**Q5.** Med-PaLM 2 scored 86.5% on exam-style medical questions. What is the most accurate conclusion? [LO2]
A) It is safe to replace clinicians in primary care.
B) It shows strong medical knowledge, but not safety in real clinical care.
C) It is 86.5% likely to be right for any patient.
D) It no longer hallucinates.

**Q6.** Lina asks a chatbot whether a herbal supplement is safe with her contraceptive pill. The chatbot says yes. What should the pharmacist do? [LO5]
A) Accept the answer because chatbots are trained on medical text
B) Tell Lina to stop the pill
C) Ask the chatbot again until it says no
D) Check the interaction against an authoritative source and advise Lina

**Q7.** An ambient scribe drafts a note that includes "normal abdominal examination", but the physician did not examine the abdomen. What is the key lesson? [LO2]
A) The clinician must review and correct every draft before signing it.
B) Ambient scribes should record without consent.
C) Scribes are always accurate for examinations.
D) The note can be signed because the scribe is approved.

**Q8.** Researchers asked several LLMs about kidney-function formulas and lung capacity in different races. What did they find? [LO5]
A) All models refused to answer.
B) All models gave current, bias-free answers.
C) The models repeated some debunked race-based medical claims.
D) The models asked for patient consent.

**Q9.** Which use of an LLM by a physiotherapy student best fits the safe-use checklist? [LO3]
A) Asking it to explain how a muscle contracts, then checking the explanation against a textbook
B) Submitting its essay as the student's own work
C) Asking it to choose a patient's exercise dose without an assessment
D) Uploading a patient's video to a public chatbot

**Q10.** Health professionals preferred chatbot replies to physician replies in 79% of ratings in one study. Which limitation matters most when applying this result? [LO5]
A) The chatbot was not a transformer.
B) The ratings were done by patients only.
C) The questions came from an online forum, and the study measured writing quality, not patient outcomes.
D) The study included only pharmacists.

**Case Question.** Rewrite the chatbot's reply to Lina, in five sentences or fewer, as a safe answer should look. It should acknowledge her worry, avoid a diagnosis, flag any urgent symptom, and direct her to the right professional.

## Answers and Rationales
**Q1. B** — LLMs are trained on next-token prediction. A describes retrieval, which is an added component. C and D are not what LLMs do.

**Q2. D** — A fabricated reference is a hallucination: plausible text without verification [2]. A, B and C are unlikely explanations.

**Q3. A** — Identifiable data must not go into public tools. B, C and D all expose patient data.

**Q4. C** — Retrieving trusted documents and answering from them is RAG [10]. A, B and D are different methods.

**Q5. B** — Exam scores show knowledge, not clinical safety [1]. A overreaches. C misreads the number. D is false.

**Q6. D** — Interactions must be checked against authoritative information. A trusts fluent output. B is unsafe. C is repeated prompting, not verification.

**Q7. A** — The clinician remains responsible for the signed note [11]. B is unethical. C and D are false.

**Q8. C** — All four models repeated some harmful race-based claims [9]. A, B and D do not describe the findings.

**Q9. A** — Using an LLM to explain a concept, then checking it, is safe. B breaches academic integrity. C and D are unsafe.

**Q10. C** — The setting and outcome measured limit how far the result applies [8]. A is irrelevant. B and D are wrong about the study.

**Case Question — model answer.** "I can hear that you are worried, and it makes sense to check a changing mole. I cannot tell you whether you have cancer; only an examination can do that. Headaches and tiredness have many common causes, but if you have a sudden severe headache, weakness, confusion or vomiting, seek emergency care now. Please keep your dermatology appointment, and bring a list of everything you take, including supplements. Before starting any supplement, ask a pharmacist, because some reduce the effect of the contraceptive pill."

## References
1. Singhal K, Azizi S, Tu T, et al. Large language models encode clinical knowledge. Nature. 2023;620(7972):172-180. DOI: 10.1038/s41586-023-06291-2
2. Bhattacharyya M, Miller VM, Bhattacharyya D, Miller LE. High rates of fabricated and inaccurate references in ChatGPT-generated medical content. Cureus. 2023;15(5):e39238. DOI: 10.7759/cureus.39238
3. Kung TH, Cheatham M, Medenilla A, et al. Performance of ChatGPT on USMLE: potential for AI-assisted medical education using large language models. PLOS Digit Health. 2023;2(2):e0000198. DOI: 10.1371/journal.pdig.0000198
4. Ji Z, Lee N, Frieske R, et al. Survey of hallucination in natural language generation. ACM Comput Surv. 2023;55(12):1-38. DOI: 10.1145/3571730
5. Vaswani A, Shazeer N, Parmar N, et al. Attention is all you need. In: Advances in Neural Information Processing Systems 30. 2017. https://arxiv.org/abs/1706.03762
6. Singhal K, Tu T, Gottweis J, et al. Toward expert-level medical question answering with large language models. Nat Med. 2025;31(3):943-950. DOI: 10.1038/s41591-024-03423-7
7. World Health Organization. Ethics and governance of artificial intelligence for health: guidance on large multi-modal models. Geneva: WHO; 2024. https://www.who.int/publications/i/item/9789240084759
8. Ayers JW, Poliak A, Dredze M, et al. Comparing physician and artificial intelligence chatbot responses to patient questions posted to a public social media forum. JAMA Intern Med. 2023;183(6):589-596. DOI: 10.1001/jamainternmed.2023.1838
9. Omiye JA, Lester JC, Spichak S, Rotemberg V, Daneshjou R. Large language models propagate race-based medicine. NPJ Digit Med. 2023;6:195. DOI: 10.1038/s41746-023-00939-z
10. Lewis P, Perez E, Piktus A, et al. Retrieval-augmented generation for knowledge-intensive NLP tasks. In: Advances in Neural Information Processing Systems 33. 2020. https://arxiv.org/abs/2005.11401
11. Tierney AA, Gayre G, Hoberman B, et al. Ambient artificial intelligence scribes to alleviate the burden of clinical documentation. NEJM Catal Innov Care Deliv. 2024;5(3). DOI: 10.1056/cat.23.0404
