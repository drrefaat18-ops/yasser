# Glossary

**Artificial intelligence** — The broad goal of building computer systems that perform tasks linked with human thinking, such as recognising images, understanding language and predicting outcomes.

**Automation bias** — The tendency to accept a computer's output even when other evidence or one's own judgment disagrees.

**Bias** — A systematic error that makes a model perform better or worse for some groups, settings or cases than others.

**Clinical decision support** — Software that gives a health professional advice at the moment of a decision, such as drug-interaction warnings or abnormal-result alerts.

**Deep learning** — Machine learning with neural networks of many layers, able to learn complex features from images, sound and text.

**Generative AI** — AI that produces new content such as text, images or code.

**Hallucination** — Fluent output from a generative model that is false or unsupported, such as an invented drug dose or reference.

**Large language model** — A generative model trained on very large amounts of text to predict the next word; the engine behind chatbots.

**Machine learning** — A way of building AI in which the computer learns patterns from example data instead of following hand-written rules.

**Model** — The mathematical function produced by machine learning that turns an input (for example, an image) into an output (for example, a risk score).

**Neural network** — A model made of layers of simple connected units whose connection strengths are adjusted during training.

**Rule-based system** — Software that follows rules written by people, such as "if drug A and drug B, then warn".

**Training data** — The examples a machine-learning model learns from.

**DICOM** — The international standard for storing and exchanging medical images together with their metadata.

**Electronic health record** — The digital version of a patient's chart, holding diagnoses, medicines, results, notes and appointments.

**Interoperability** — The ability of different health information systems to exchange data and use it correctly.

**Label** — The correct answer attached to a training example, such as "pneumonia present" for a chest X-ray.

**Label noise** — Errors in the labels a model is trained on; the model learns these errors too.

**Metadata** — Data about data, such as the scanner model, hospital and date stored with a medical image.

**Omics** — Data describing molecules in the body, such as genomics (DNA) and pharmacogenomics (genes affecting drug response).

**Structured data** — Data that fit into rows and columns, such as laboratory values, codes and prescriptions.

**Unstructured data** — Data without a fixed table format, such as images, signals and free text.

**Adversarial attack** — A small, deliberate change to an input, often invisible to people, crafted to make a specific model give a wrong output.

**Anterior cruciate ligament** — A ligament inside the knee that stops the shin bone sliding forward and helps the knee resist twisting (ACL).

**Class imbalance** — A situation in which one outcome is much rarer than another in the data, such as cancer in screening images.

**Convolutional neural network** — A neural network designed for images; early layers detect edges and textures, later layers detect shapes (CNN).

**Data leakage** — Information that would not be available in real use reaching the training or testing of a model, making it look better than it is.

**Distribution shift** — A difference between the data a model was trained on and the data it meets in use, such as new patients, machines or practices.

**External validation** — Testing a model on data from a different hospital, time period or population from the one used to develop it.

**Gradient descent** — The training method that repeatedly nudges a model's parameters in the direction that reduces its loss.

**Internal validation** — Testing a model on a held-out part of the same dataset used to develop it.

**Loss function** — A formula that measures how wrong a model's predictions are during training.

**Overfitting** — When a model learns the quirks and noise of its training data so closely that it performs poorly on new data.

**Parameter** — One of the adjustable numbers inside a model that training changes.

**Reinforcement learning** — Learning by taking actions and receiving rewards or penalties.

**Shortcut learning** — When a model relies on an easy cue that predicts the label in training data but is unrelated to the real task, such as a scanner marker.

**Supervised learning** — Learning from examples that come with correct answers (labels).

**Test set** — Data kept aside and used once, at the end, to estimate how a model will perform on new cases.

**Training set** — The data used to adjust a model's parameters.

**U-Net** — A convolutional neural network that outlines structures pixel by pixel in an image (segmentation).

**Unsupervised learning** — Learning that finds structure, such as groups, in data without labels.

**Validation set** — Data used during development to tune design choices and decide when to stop training.

**Accuracy** — The share of all cases a model classifies correctly; misleading when a condition is rare.

**Area under the precision–recall curve** — A summary of how precision (PPV) and recall (sensitivity) trade off across thresholds; more informative than AUROC for rare conditions (AUPRC).

**Area under the ROC curve** — The probability that a model scores a random patient with the condition higher than a random patient without it; ranges from 0.5 (chance) to 1.0 (perfect) (AUROC, C-statistic).

**Calibration** — How closely a model's predicted risks match observed event rates; a calibrated "20% risk" means about 20 in 100 similar patients have the event.

**Confusion matrix** — A 2 × 2 table comparing a model's positive and negative outputs with the true condition.

**Diagnostic test** — A test used when symptoms or signs already raise suspicion of a condition.

**Dice coefficient** — An overlap measure between a model's outline and the true outline: twice the overlap divided by the total size of both; 0 to 1.

**Discrimination** — A model's ability to rank patients, giving higher scores to those with the condition.

**Intersection over union** — An overlap measure: the shared area of two outlines divided by their combined area; 0 to 1 (IoU).

**Negative predictive value** — The share of negative results that are truly negative (NPV).

**Positive predictive value** — The share of positive results that are truly positive; depends strongly on prevalence (PPV, precision).

**Prevalence** — How common a condition is in the group being tested.

**Randomised controlled trial** — A study in which patients or sites are randomly assigned to different care, such as with or without AI, to measure its effect (RCT).

**Reporting guideline** — A checklist of what a research paper should report, such as TRIPOD+AI for prediction models or CONSORT-AI for AI trials.

**ROC curve** — A plot of sensitivity against 1 − specificity across all possible thresholds.

**Screening** — Testing people without symptoms to find disease early.

**Sensitivity** — The share of people with a condition whom a test correctly identifies (recall).

**Specificity** — The share of people without a condition whom a test correctly clears.

**Threshold** — The score above which a model's output is treated as positive.

**Academic integrity** — Honesty in study and assessment, including acknowledging when AI tools were used and not presenting their output as one's own work.

**Ambient scribe** — An AI system that listens, with consent, to a consultation and drafts the clinical note for the clinician to review.

**Drug interaction** — A change in the effect of a medicine caused by another medicine, food or supplement.

**Retrieval-augmented generation** — A method in which an LLM first retrieves passages from trusted documents and then answers using them, so that sources can be shown (RAG).

**Token** — A small piece of text, such as a word or part of a word, that a language model reads and predicts.

**Transformer** — The neural-network design behind modern LLMs; its attention mechanism weighs all earlier words when predicting the next one.
