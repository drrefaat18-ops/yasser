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

![Figure 3.1 — Training, validation and test sets](figures/split-leakage.svg)
*Figure 3.1 — The test set must stay unseen. Leakage happens when test information reaches training. Illustrative.*

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
