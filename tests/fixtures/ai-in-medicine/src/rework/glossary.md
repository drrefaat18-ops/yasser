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
