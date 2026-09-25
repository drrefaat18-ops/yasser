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
