# Chapter 2: Health Data — What AI Learns From

## Opening Case
Amal Hassan, 61, has lived with type 2 diabetes for twelve years. Her story is spread across many computers. The family clinic holds her blood-pressure readings and diagnoses. The laboratory holds ten years of glucose and kidney results. The pharmacy holds every refill of her seven medicines. The eye clinic holds three retinal photographs.

A laboratory technologist is asked to help build a model that predicts which patients like Amal will lose kidney function in the next two years. She opens the data. Some results are missing. Some diagnoses are coded differently in the two clinics. The pharmacy data use a different patient number. What does a model actually learn from, and what can go wrong before learning even starts?

## Learning Objectives
By the end of this chapter you will be able to:
1. [LO1] Classify health data into structured data, images, signals, text and omics.
2. [LO2] Explain what a label is and why labelling is costly and error-prone.
3. [LO3] Identify common data-quality problems, including missing data and bias in who gets tested.
4. [LO4] Recognise the main health-data standards and famous public datasets, and who they leave out.

## 2.1 Five Kinds of Health Data
Health data come in five broad kinds.

**Structured data** fit neatly into rows and columns. Examples are age, blood pressure, laboratory values, diagnosis codes, prescriptions and dispensing records. Amal's creatinine results and refill dates are structured data.

Images are grids of numbers. X-rays, CT and MRI scans, retinal photographs, skin photos and scanned pathology slides are all images. So is a video of a patient walking.

Signals are measurements over time. An electrocardiogram (ECG), a continuous glucose monitor and a wrist accelerometer all produce signals.

Text is written language: clinic notes, discharge letters, radiology reports and pharmacy counselling notes. Text is rich but messy.

**Omics** data describe molecules. Genomics reads DNA. Pharmacogenomics looks at genes that change how a person handles a drug.

Images, signals and text are often called **unstructured data**. They need more processing before a model can use them.

> **Medical Background in 60 Seconds:** An **electronic health record** (EHR) is the digital version of a patient's chart. It holds diagnoses, medicines, results, notes and appointments. Creatinine is a waste product filtered by the kidneys. A rising blood creatinine suggests falling kidney function. Doctors use it to estimate the glomerular filtration rate (eGFR). Amal's eGFR is 52, which is mildly reduced.

> **Deeper Dive:** To a computer, a grey-scale CT slice is a 512 × 512 grid of numbers. Each number records how strongly that point absorbed X-rays. A colour photo has three such grids: red, green and blue. Medical images are stored in the **DICOM** format. A DICOM file also carries **metadata**: the patient's age, the scanner model, the hospital and the date. Metadata help clinicians. They can also let a model "cheat" by learning which scanner was used instead of what disease is present. Chapter 3 calls this shortcut learning.

## 2.2 Labels: The Answers a Model Learns From
Most medical AI uses supervised learning. The model sees an input and the correct answer, then learns to link them. The correct answer is called a **label**. For Amal's kidney model, the label might be "eGFR fell by 30% or more within two years: yes or no."

Labels come from four main sources:

- **Expert annotation.** A specialist marks each image or case. This is accurate but slow and expensive.
- **Codes.** Diagnosis codes entered for billing or records. Cheap, but often incomplete or wrong.
- **Outcomes.** Something that happened later, such as death, admission or a laboratory value crossing a threshold.
- **Text mining.** Software reads reports and extracts a label. Several famous chest X-ray datasets were labelled this way [3, 4].

Every source has errors. Wrong labels are called **label noise**. A model trained on noisy labels learns the noise too. If the codes miss half of the patients with kidney disease, the model learns an incomplete picture of kidney disease.

The choice of label also carries values. Chapter 10 describes a model that used health-care cost as its label for health need. Because less money had been spent on some groups, the model under-rated their need.

## 2.3 Data Quality: Problems Before Learning Starts
Health data are collected for care and billing, not for training AI. This creates predictable problems.

**Missing data.** Many values are empty. Data can be missing for random reasons, such as a lost sample. More often they are missing for meaningful reasons. A test is ordered because a clinician is worried. So the mere presence of a test carries information. One large study found that whether and when a laboratory test was ordered was strongly linked to survival, often more than the result itself [7]. A model can learn the ordering habits of clinicians, not the biology of disease.

**Bias in who gets tested.** People who cannot reach a clinic produce fewer records. Their disease may look rarer in the data than it really is.

**Inconsistent coding.** The same condition may be coded in different ways in different clinics. The same drug may have a brand name in one system and a generic name in another.

**Linkage errors.** Amal's pharmacy record uses a different patient number. Joining the records wrongly could attach someone else's medicines to her.

**Changes over time.** Laboratory methods, coding systems and clinical guidelines change. Data from ten years ago may mean something different from data collected today.

## 2.4 Speaking the Same Language: Standards
Data from different systems can only be combined if they use shared rules. This ability to exchange and use data is called **interoperability**.

| Standard | What it covers | Example |
|---|---|---|
| DICOM | Medical images and their metadata | A CT scan moving from scanner to viewing station |
| HL7 FHIR | Exchange of health records between systems | A clinic app requesting Amal's latest results |
| ICD | Diagnosis codes | E11 for type 2 diabetes |
| SNOMED CT | Detailed clinical terms | Specific findings, procedures and body sites |
| LOINC | Laboratory and clinical observations | A code for serum creatinine |
| ATC | Drug classification | A10BA02 for metformin |

You need not memorise these codes. When an AI tool fails at a new site, a coding mismatch is a common reason.

## 2.5 Famous Datasets and Who They Leave Out
A few large public datasets trained a large share of published medical AI.

- MIMIC-IV contains records of intensive-care and emergency patients from one hospital in Boston, USA [1]. MIMIC-CXR adds over 370,000 chest X-rays with reports from the same hospital [2].
- CheXpert holds 224,316 chest X-rays from 65,240 patients at Stanford, labelled by software reading the reports [3].
- ChestX-ray8 from the US National Institutes of Health holds 108,948 X-rays labelled the same way [4].
- The Cancer Genome Atlas (TCGA) links tumour genetics, pathology slides and outcomes for thousands of patients [5].
- UK Biobank follows about half a million adults aged 40 to 69 from the United Kingdom [6]. Its volunteers are healthier and less ethnically diverse than the general population [8].

These open datasets are valuable. But they come mostly from a few wealthy countries and large academic hospitals. A model built on them may not fit a clinic in Cairo, Lagos or a rural district anywhere.

> **Through Four Lenses**
> - **Medicine:** Physicians create much of the record. Clear diagnoses and complete problem lists become labels. Vague or copied notes become label noise that future models will learn from.
> - **Pharmacy:** Pharmacists hold dispensing data that show what patients actually collect. Refill gaps reveal non-adherence that prescriptions alone hide. This makes pharmacy data valuable for prediction models.
> - **Physical Therapy:** Physiotherapists record range of motion, pain scores and exercise progress. When these are free text, models cannot use them. Structured outcome measures make rehabilitation visible in the data.
> - **Health Sciences:** Laboratory and imaging technologists control how samples and images are produced. Calibration logs, analyser changes and scanner settings explain many shifts that later confuse AI models.

> **Myth vs Evidence:** Myth: "More data always means a better model." Evidence: Large datasets can still be biased or noisy. Test-ordering patterns alone predict outcomes, so a big dataset may teach clinician behaviour rather than disease [7]. Quality and representativeness matter as much as size.

> **Safety Alert:** Never copy patient data to a personal device or a public website to "try out" an AI tool. Health data are sensitive, and re-identification is easier than most people think (Chapter 10).

## Key Takeaways
- Health data include structured data, images, signals, text and omics.
- Supervised models learn from labels, and every label source contains errors.
- Missing data are rarely random; the pattern of testing itself carries information.
- Standards such as DICOM, HL7 FHIR, ICD and SNOMED CT make data exchange possible.
- Famous public datasets come from a few settings, so models built on them may not fit yours.

## Self-Assessment
**Q1.** Amal's continuous glucose monitor records a value every five minutes. Which data type is this? [LO1]
A) Omics
B) Free text
C) Signal
D) Image

**Q2.** A model is trained to detect pneumonia on chest X-rays. Its labels were extracted by software reading radiology reports. What is the main weakness of this label source? [LO2]
A) Some labels will be wrong because reports can be ambiguous or misread.
B) The labels will be perfect because software does not tire.
C) The labels cannot be stored in a computer.
D) The labels contain the patients' genomes.

**Q3.** A dataset shows that patients with a blood-culture result are more likely to die than those without one. What is the best explanation? [LO3]
A) Blood cultures cause death.
B) The laboratory made errors.
C) The dataset is too small.
D) Blood cultures are ordered when clinicians already suspect serious illness.

**Q4.** Which standard is designed mainly for storing and moving medical images with their metadata? [LO4]
A) SNOMED CT
B) DICOM
C) ATC
D) LOINC

**Q5.** A pharmacist notices that Amal collects her metformin every 60 days, although each pack lasts 30 days. Which data source revealed this, and what does it suggest? [LO1]
A) Dispensing data; possible non-adherence
B) Genomic data; a gene variant
C) Imaging data; kidney damage
D) Laboratory data; a calibration error

**Q6.** A research team wants to train a model on UK Biobank and use it in a clinic in Egypt. What is the most important concern? [LO4]
A) UK Biobank data cannot be read by computers.
B) UK Biobank contains only children.
C) The participants differ in health, ethnicity and setting from the Egyptian clinic's patients.
D) UK Biobank has no outcome data.

**Q7.** A model is trained on diagnosis codes. Half of the patients who truly have chronic kidney disease were never coded. What will the model most likely learn? [LO2]
A) A perfect definition of kidney disease
B) An incomplete picture, because the labels contain systematic noise
C) Nothing, because codes cannot be labels
D) Only the genomics of kidney disease

**Q8.** A physiotherapy department records knee range of motion only in free-text notes. Why does this limit AI? [LO3]
A) Free text is illegal to store.
B) Range of motion cannot be measured.
C) Physiotherapy data are never useful for models.
D) Unstructured notes are hard for models to use unless the measures are also recorded in structured form.

**Q9.** A chest X-ray model learns to recognise which hospital's scanner produced each image, not the disease. Which part of the DICOM file might have made this easy? [LO1]
A) The metadata, such as scanner model and hospital
B) The patient's prescription history
C) The ICD diagnosis code
D) The ATC drug class

**Q10.** What does interoperability mean in health data? [LO4]
A) Keeping data on paper only
B) Deleting old records
C) The ability of different systems to exchange and use data
D) Training AI without labels

**Case Question.** You are the laboratory technologist in the opening case. List three data problems you would check before Amal's kidney-risk model is trained, and explain in one sentence each why they matter.

## Answers and Rationales
**Q1. C** — Values recorded over time form a signal. A describes molecules. B is written language. D is a pixel grid.

**Q2. A** — Report-mining software makes mistakes, and reports themselves can be uncertain [3]. B is false. C and D are irrelevant.

**Q3. D** — Tests are ordered for sicker patients, so their presence carries information [7]. A confuses association with cause. B and C do not explain the pattern.

**Q4. B** — DICOM stores images and metadata. A covers clinical terms. C classifies drugs. D covers laboratory observations.

**Q5. A** — Refill timing in dispensing data suggests doses are being missed. B, C and D are unrelated to refill patterns.

**Q6. C** — UK Biobank volunteers are healthier and less diverse than many populations [8]. A, B and D are false.

**Q7. B** — Systematically missing labels make the model learn an incomplete version of the disease. A is false. C is false because codes are often used as labels. D is unrelated.

**Q8. D** — Structured measures make rehabilitation data usable. A is false. B is false. C overgeneralises.

**Q9. A** — Metadata can reveal the scanner and site, which a model can exploit. B, C and D are not in the image file.

**Q10. C** — Interoperability is the ability of systems to exchange and use data. A, B and D are unrelated.

**Case Question — model answer.** First, check missing values and why they are missing, because tests ordered only for worried cases can bias the model. Second, check that the clinic, laboratory and pharmacy records are correctly linked, because a linkage error could attach another patient's data to Amal. Third, check whether laboratory methods or coding changed over the ten years, because a change in the creatinine assay could look like a change in kidney function.

## References
1. Johnson AEW, Bulgarelli L, Shen L, et al. MIMIC-IV, a freely accessible electronic health record dataset. Sci Data. 2023;10:1. DOI: 10.1038/s41597-022-01899-x
2. Johnson AEW, Pollard TJ, Berkowitz SJ, et al. MIMIC-CXR, a de-identified publicly available database of chest radiographs with free-text reports. Sci Data. 2019;6:317. DOI: 10.1038/s41597-019-0322-0
3. Irvin J, Rajpurkar P, Ko M, et al. CheXpert: a large chest radiograph dataset with uncertainty labels and expert comparison. Proc AAAI Conf Artif Intell. 2019;33(01):590-597. DOI: 10.1609/aaai.v33i01.3301590
4. Wang X, Peng Y, Lu L, et al. ChestX-ray8: hospital-scale chest X-ray database and benchmarks on weakly-supervised classification and localization of common thorax diseases. In: 2017 IEEE Conference on Computer Vision and Pattern Recognition (CVPR). 2017:3462-3471. DOI: 10.1109/cvpr.2017.369
5. Cancer Genome Atlas Research Network, Weinstein JN, Collisson EA, et al. The Cancer Genome Atlas Pan-Cancer analysis project. Nat Genet. 2013;45(10):1113-1120. DOI: 10.1038/ng.2764
6. Bycroft C, Freeman C, Petkova D, et al. The UK Biobank resource with deep phenotyping and genomic data. Nature. 2018;562(7726):203-209. DOI: 10.1038/s41586-018-0579-z
7. Agniel D, Kohane IS, Weber GM. Biases in electronic health record data due to processes within the healthcare system: retrospective observational study. BMJ. 2018;361:k1479. DOI: 10.1136/bmj.k1479
8. Fry A, Littlejohns TJ, Sudlow C, et al. Comparison of sociodemographic and health-related characteristics of UK Biobank participants with those of the general population. Am J Epidemiol. 2017;186(9):1026-1034. DOI: 10.1093/aje/kwx246
