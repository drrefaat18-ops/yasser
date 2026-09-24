# Chapter 3: How Models Learn — and How They Fail

## Opening Case
Karim Adel, 34, is a construction worker. He twisted his left knee on site and felt a pop. At the physiotherapy clinic, a new app analyses a video of him doing a single-leg squat. It gives a "knee stability score" of 82 out of 100 and labels his movement "low risk".

The physiotherapist is surprised. Karim's knee gives way when he turns. She reads the app's documentation. The model was trained on 4,000 videos of university athletes, filmed in a bright sports laboratory. Its reported accuracy was 94%.

Karim is older, heavier and filmed in a small clinic room with poor light. He is also in pain, so he moves differently. Why would a model that scored 94% fail for him? This chapter explains how models learn, and the main ways they fail.

## Learning Objectives
By the end of this chapter you will be able to:
1. [LO1] Distinguish supervised, unsupervised and reinforcement learning with health examples.
2. [LO2] Explain in plain words how a model is trained by reducing its errors.
3. [LO3] Describe the purpose of training, validation and test sets.
4. [LO4] Distinguish overfitting, data leakage, shortcut learning and distribution shift.
5. [LO5] Explain class imbalance and why complex models are not always better.

## 3.1 Three Ways to Learn
**Supervised learning** uses labelled examples (Chapter 2). The model sees an input and the correct answer, many times. Examples: X-rays labelled "fracture" or "no fracture", or knee videos labelled "stable" or "unstable".

**Unsupervised learning** has no labels. The model looks for structure by itself, such as groups of similar patients. A clinic might find three patterns of recovery after knee surgery that nobody had named before.

**Reinforcement learning** learns by trial and feedback. The system takes actions and receives rewards. Researchers have used it to suggest fluid and drug doses in intensive care, based on past records [10]. It is still experimental in health care.

## 3.2 How Training Works
A model contains millions of adjustable numbers called **parameter**s. At the start, the parameters are random, so the model guesses badly.

Training repeats three steps:

1. The model makes a prediction for a training example.
2. A **loss function** measures how wrong the prediction was.
3. The parameters are nudged a tiny amount to make the loss smaller.

After millions of nudges, the model's predictions fit the training data well. This process is called **gradient descent**. You can picture a walker in fog, feeling the slope with each step and always moving downhill.

A **convolutional neural network** (CNN) is the classic deep-learning model for images. Its early layers detect edges and textures. Later layers combine them into shapes, such as a bone outline or a mole's border. A **U-Net** is a CNN that outlines structures pixel by pixel, for example a tumour on a scan [8].

> **Deeper Dive:** Imagine a one-parameter model that predicts knee angle as w × (marker distance). The true angle is 60°. With w = 2 and a distance of 20, the model predicts 40°. The squared error is (60 − 40)² = 400. Increasing w a little, to 2.5, gives 50° and an error of 100. Training keeps moving w in the direction that lowers the error. Real models do this for millions of parameters at once.

## 3.3 Splitting the Data
A model always looks good on the data it was trained on. The real question is how it performs on new patients. So developers split their data into three sets (Figure 3.1).

- The **training set** is used to adjust the parameters.
- The **validation set** is used to tune design choices and decide when to stop training.
- The **test set** is locked away and used once, at the end, to estimate real performance.

![Figure 3.1 — Training, validation and test sets](figures/split-leakage.svg)
*Figure 3.1 — Data are split so that the test set stays unseen. Leakage happens when information from the test set reaches training. Illustrative.*

Testing on a separate portion of the same dataset is called **internal validation**. Testing on data from a different hospital, time or population is called **external validation**. External validation is much more informative. Chapter 4 returns to this.

## 3.4 Four Ways Models Fail
**Overfitting.** The model memorises the training data, including its noise and quirks, instead of learning general patterns. It scores very well in training and poorly on new data. It is like a student who memorises last year's exam answers without understanding them.

**Data leakage.** Information that would not be available in real use slips into training or testing [5]. Leakage makes a model look better than it is. Two common forms are:

- *Patient-level leakage.* Several images from the same patient appear in both training and test sets. The model recognises the patient, not the disease.
- *Future leakage.* The model uses information recorded after the moment of prediction. A sepsis model that uses "antibiotics started" as an input is partly reading the clinician's decision.

A review of machine-learning research across many fields found leakage in hundreds of published papers [5]. Leakage is a problem of study design. It is not a privacy problem.

**Shortcut learning.** The model finds an easy cue that happens to predict the label in the training data but has nothing to do with the disease [3]. In one study, a pneumonia model learned features of the hospital and the X-ray machine. Its performance fell when tested at other hospitals [1]. Many COVID-19 X-ray models learned text markers and patient position instead of lung changes [2]. A review of 62 COVID-19 imaging models found none ready for clinical use, largely because of such flaws [4].

**Distribution shift.** The world changes after training. New scanners, new patient groups, new laboratory methods or new clinical habits make today's data differ from training data [6]. Karim's case shows shift: older age, a different body type, pain and poor lighting.

A related threat is an **adversarial attack**: a tiny, deliberate change to an input, invisible to people, that is crafted to fool a specific model [9]. Ordinary image compression or blur is not an attack. It is a form of distribution shift, and it needs different defences.

> **Medical Background in 60 Seconds:** The **anterior cruciate ligament** (ACL) is a strong band inside the knee. It stops the shin bone sliding forward and helps the knee resist twisting. An ACL tear often happens during a sudden turn. Patients describe a "pop" and a knee that later "gives way". Physiotherapists test knee stability and retrain movement before a return to work or sport.

## 3.5 Class Imbalance and the Limits of Complexity
In health care, the condition of interest is often rare. Only a few mammograms in a thousand show cancer. This is called **class imbalance**. A model can reach 99% accuracy by always saying "no cancer". That model is useless. Chapter 4 shows better ways to measure performance when a condition is rare.

More complex is not always better. A review of 71 clinical prediction studies compared machine learning with logistic regression, a traditional statistical method [7]. In well-designed studies, machine learning showed no average advantage. For tabular data, such as vital signs and laboratory values, simple models are often as good and easier to check. Deep learning shows its strength mainly with images, signals and text.

> **Through Four Lenses**
> - **Medicine:** Physicians should ask where a diagnostic model was trained and tested. A model validated only in one teaching hospital may fail in a district clinic with different patients and machines.
> - **Pharmacy:** Pharmacists should watch for future leakage in medication-risk models. A model that uses "drug stopped" or "antidote given" is reading the clinical response, not predicting the event.
> - **Physical Therapy:** Physiotherapists should compare a movement model's training population with their patients. Age, body size, pain, walking aids and room lighting can all create distribution shift.
> - **Health Sciences:** Technologists should report changes in analysers, reagents and scanners. These changes shift the data silently, and a model may keep producing confident but wrong outputs.

> **Myth vs Evidence:** Myth: "Machine learning always beats traditional statistics." Evidence: Across 71 clinical prediction studies, machine learning showed no average performance benefit over logistic regression once study quality was considered [7].

> **Safety Alert:** When an AI output does not match what you see in the patient, trust the patient. Record the mismatch and report it. These reports are how silent failures are discovered.

## Key Takeaways
- Supervised learning uses labels; unsupervised learning finds structure; reinforcement learning learns from rewards.
- Training adjusts parameters to reduce a loss function, step by step.
- Only an untouched test set, ideally from another site, shows real performance.
- Overfitting, leakage, shortcut learning and distribution shift make good-looking models fail.
- With rare conditions, accuracy misleads, and simple models are often as good as complex ones.

## Self-Assessment
**Q1.** A hospital groups its diabetes patients into clusters by their glucose patterns, without any labels. Which type of learning is this? [LO1]
A) Supervised learning
B) Reinforcement learning
C) Transfer learning
D) Unsupervised learning

**Q2.** During training, what does the loss function do? [LO2]
A) It deletes patient records.
B) It measures how far the model's predictions are from the correct answers.
C) It chooses which patients enter the test set.
D) It explains the model's reasoning to clinicians.

**Q3.** A team uses its test set many times to choose between model designs. What is the main problem? [LO3]
A) The test set stops being an unbiased estimate of performance on new data.
B) The model will train faster.
C) The validation set will become too large.
D) There is no problem; this is standard practice.

**Q4.** Karim's knee app scored 94% on videos of athletes filmed in a sports laboratory but fails in a small clinic. Which failure mode best explains this? [LO4]
A) Future leakage
B) Adversarial attack
C) Distribution shift
D) Reinforcement learning

**Q5.** A skin-lesion dataset contains several photos of each patient. The team splits photos randomly, so some patients appear in both training and test sets. What is the likely effect? [LO4]
A) Performance will be underestimated.
B) The model will become unsupervised.
C) Class imbalance will disappear.
D) Performance will be overestimated because of patient-level leakage.

**Q6.** A pneumonia model performs well at the hospital where it was built but poorly elsewhere. Investigators find that it learned features of the X-ray machine. What is this called? [LO4]
A) Shortcut learning
B) Overfitting to the loss function
C) Gradient descent
D) Calibration

**Q7.** A cancer is present in 3 of every 1,000 screening images. A model labels every image "no cancer". What is its accuracy, and is it useful? [LO5]
A) 3%; useful
B) 50%; not useful
C) 99.7%; not useful
D) 100%; useful

**Q8.** A model predicting sepsis uses "IV antibiotics started" as one of its inputs. Why is this a concern? [LO4]
A) Antibiotics are not recorded in health records.
B) It is future leakage: the input reflects a clinician's decision that already suspects sepsis.
C) It makes the model unsupervised.
D) It is an adversarial attack.

**Q9.** A team compares logistic regression and a complex machine-learning model for predicting readmission from 20 laboratory values. Based on current evidence, what is the most likely result? [LO5]
A) Similar performance, with the simpler model easier to check
B) Machine learning always wins by a large margin
C) Logistic regression cannot use laboratory values
D) Neither model can be validated

**Q10.** What is the purpose of the validation set? [LO3]
A) To replace the test set
B) To tune design choices and decide when to stop training
C) To store the model's parameters
D) To collect new patients after deployment

**Case Question.** Karim's physiotherapist wants to report her concerns about the knee app to the clinic manager. Write four sentences explaining what went wrong, using at least two terms from this chapter, and suggest one test the clinic should run before using the app again.

## Answers and Rationales
**Q1. D** — Finding groups without labels is unsupervised learning. A needs labels. B needs rewards. C reuses a model from another task.

**Q2. B** — The loss function measures prediction error, which training reduces. A, C and D are not its role.

**Q3. A** — Repeated use of the test set lets design choices fit it, so its estimate becomes optimistic. B and C are irrelevant. D is wrong.

**Q4. C** — The patients and filming conditions differ from the training data. A concerns inputs from the future. B is deliberate manipulation. D is a learning type.

**Q5. D** — The model can recognise the same patient across sets, inflating performance [5]. A reverses the effect. B and C are unrelated.

**Q6. A** — The model used an irrelevant cue linked to the site [1]. B is not a standard term. C is the training method. D concerns probability accuracy.

**Q7. C** — The model is right 997 times in 1,000 but misses every cancer. A and B are wrong numbers. D is impossible.

**Q8. B** — Starting antibiotics reflects existing clinical suspicion and happens after the moment of prediction. A is false. C and D are unrelated.

**Q9. A** — For tabular data, machine learning shows no average advantage over logistic regression [7]. B overstates. C and D are false.

**Q10. B** — The validation set guides tuning; the test set stays untouched. A, C and D are wrong.

**Case Question — model answer.** The app was trained on young athletes in a bright laboratory, but Karim is older, injured and filmed in a small room. This is distribution shift, so the 94% accuracy does not apply to him. The high score may also reflect shortcut learning, such as lighting or background cues. The app's result conflicted with the clinical finding that his knee gives way. Before using it again, the clinic should test it on a sample of its own patients, with physiotherapist assessment as the reference.

## References
1. Zech JR, Badgeley MA, Liu M, et al. Variable generalization performance of a deep learning model to detect pneumonia in chest radiographs: a cross-sectional study. PLoS Med. 2018;15(11):e1002683. DOI: 10.1371/journal.pmed.1002683
2. DeGrave AJ, Janizek JD, Lee SI. AI for radiographic COVID-19 detection selects shortcuts over signal. Nat Mach Intell. 2021;3(7):610-619. DOI: 10.1038/s42256-021-00338-7
3. Geirhos R, Jacobsen JH, Michaelis C, et al. Shortcut learning in deep neural networks. Nat Mach Intell. 2020;2(11):665-673. DOI: 10.1038/s42256-020-00257-z
4. Roberts M, Driggs D, Thorpe M, et al. Common pitfalls and recommendations for using machine learning to detect and prognosticate for COVID-19 using chest radiographs and CT scans. Nat Mach Intell. 2021;3(3):199-217. DOI: 10.1038/s42256-021-00307-0
5. Kapoor S, Narayanan A. Leakage and the reproducibility crisis in machine-learning-based science. Patterns. 2023;4(9):100804. DOI: 10.1016/j.patter.2023.100804
6. Finlayson SG, Subbaswamy A, Singh K, et al. The clinician and dataset shift in artificial intelligence. N Engl J Med. 2021;385(3):283-286. DOI: 10.1056/nejmc2104626
7. Christodoulou E, Ma J, Collins GS, et al. A systematic review shows no performance benefit of machine learning over logistic regression for clinical prediction models. J Clin Epidemiol. 2019;110:12-22. DOI: 10.1016/j.jclinepi.2019.02.004
8. Ronneberger O, Fischer P, Brox T. U-Net: convolutional networks for biomedical image segmentation. In: Medical Image Computing and Computer-Assisted Intervention – MICCAI 2015. Lecture Notes in Computer Science. Springer; 2015:234-241. DOI: 10.1007/978-3-319-24574-4_28
9. Finlayson SG, Bowers JD, Ito J, et al. Adversarial attacks on medical machine learning. Science. 2019;363(6433):1287-1289. DOI: 10.1126/science.aaw4399
10. Komorowski M, Celi LA, Badawi O, et al. The Artificial Intelligence Clinician learns optimal treatment strategies for sepsis in intensive care. Nat Med. 2018;24(11):1716-1720. DOI: 10.1038/s41591-018-0213-5
