# Chapter 6: Seeing Disease — Imaging, Laboratory and Pathology

## Opening Case
Amal Hassan visits her family clinic for her yearly diabetes review. A healthcare assistant takes two photographs of the back of each eye with a small camera. There is no eye specialist in the clinic. Within a minute, an AI system reports: "More-than-mild diabetic retinopathy detected. Refer to an eye specialist." Amal's hands shake. Her mother went blind from diabetes.

That same week, Karim has an MRI of his injured knee, and an AI tool flags a likely ligament tear before the radiologist reads the scan. Lina's dermatologist photographs her mole with a dermatoscope and sees a risk score from a skin-lesion model.

Three patients, three images, three AI tools. What are these tools actually doing, how good is the evidence, and where do they fail? And what happens to the samples and slides that never reach a camera?

## Learning Objectives
By the end of this chapter you will be able to:
1. [LO1] Distinguish computer-aided detection, diagnosis and triage (CADe, CADx, CADt).
2. [LO2] Describe AI in screening programmes and judge the strength of their evidence.
3. [LO3] Explain why AI-accelerated MRI can create features that are not really there.
4. [LO4] Describe the digital-pathology pipeline and the main uses of AI in the clinical laboratory.
5. [LO5] Identify how imaging and laboratory AI fail across patient groups and settings.

> **Medical Background in 60 Seconds:** An **X-ray** passes radiation through the body; dense tissue such as bone looks white. **CT** combines many X-rays into cross-sectional slices. **MRI** uses a strong magnet and radio waves, with no radiation, and shows soft tissues such as ligaments well. A **retinal photograph** shows the blood vessels at the back of the eye, where diabetes causes damage called diabetic retinopathy. A **biopsy** is a small tissue sample examined under a microscope by a pathologist.

## 6.1 What Imaging AI Does: Detect, Diagnose, Triage
Imaging AI tools fall into three groups.

- **Computer-aided detection** (CADe) marks where something may be, such as a box around a possible lung nodule. The reader decides what it is.
- **Computer-aided diagnosis** (CADx) characterises a finding, such as "likely malignant" or "likely benign".
- **Computer-aided triage** (CADt) reorders the reading list so that urgent cases are read first, such as a suspected brain bleed on CT.

The difference matters for safety. A CADt tool that misses a bleed does not delay the case beyond normal practice, because a human still reads every scan. A CADx tool that labels a cancer "benign" can directly mislead a decision.

A model reading a chest X-ray has no more information than the human looking at the same image. It does not "see through" overlapping structures. It learns statistical patterns in the pixels. Those patterns can include shortcuts, such as the hospital's scanner type, instead of disease (Chapter 3) [17].

## 6.2 Screening: Eyes and Breasts
**Diabetic eye screening.** Diabetic retinopathy is a leading cause of preventable blindness, and screening all patients needs more specialists than many countries have. In a retrospective study, a deep-learning model graded retinal photos with high sensitivity and specificity [1]. The stronger evidence came later. An autonomous system was tested prospectively in 900 patients in primary-care clinics. It found more-than-mild retinopathy with 87.2% sensitivity and 90.7% specificity [2]. This supported its authorisation as the first autonomous AI diagnostic device in the United States.

Amal's result is a referral, not a diagnosis. With a specificity near 91%, some referred patients will not have significant disease. The eye specialist will confirm.

**Breast screening.** In many countries, two radiologists read every screening mammogram. In the MASAI randomised trial in Sweden, AI sorted mammograms by risk and helped decide which needed one or two readers [3]. Screen-reading workload fell by 44%. About 20% more cancers were detected, and false-positive rates did not rise. A prospective Swedish study also found that AI plus one radiologist was non-inferior to two radiologists [6].

Earlier, a widely publicised retrospective study reported that AI outperformed radiologists [4]. Other scientists pointed out that the code and data were not shared, so the result could not be reproduced [5]. Reproducibility is part of evidence.

![Figure 6.1 — Dermoscopic images and model scores](../images/image15.png)
*Figure 6.1 — A model's output for a suspicious and a benign lesion. The "confidence" values are uncalibrated scores, not probabilities (Chapter 4). Both lesions are shown on light skin, which reflects the bias of many training sets. Illustrative.*

## 6.3 Skin, Knees and Fast MRI
**Dermatology.** A 2017 study trained a CNN on about 129,000 skin images and matched dermatologists on test images [9]. Public datasets such as HAM10000 later made research easier [10]. But most images in these collections show light skin. When researchers built a test set balanced across skin tones, several published models performed markedly worse on darker skin [11]. For Lina, who has Fitzpatrick type V skin, this matters directly (Chapter 10).

**Knee MRI.** A model called MRNet detected ligament and meniscus tears on knee MRI and was tested on data from another hospital [8]. Tools like this can prioritise scans such as Karim's. The radiologist still reads the whole study, because the model looks only for the findings it was trained on.

**Fast MRI.** MRI is slow because the scanner collects its data point by point in a frequency space called k-space. Collecting fewer points saves time. But skipping points in a regular pattern always creates artefacts, called aliasing. Modern methods skip points in an irregular pattern, which spreads the artefact like noise. A trained network then removes that noise, using what it has learned about how anatomy usually looks [7]. The missing data are not recovered. They are inferred.

This has two consequences. First, scans become much faster: cutting a 25-minute scan to 5 minutes, or 40 minutes to 10, is a 75–80% reduction. Second, the network can "fill in" typical anatomy where the patient's anatomy is unusual. A small lesion could be smoothed away, or a realistic-looking structure added. This is the imaging version of hallucination (Chapter 5).

## 6.4 Pathology: From Glass Slide to Heatmap
In **digital pathology**, a scanner turns a glass slide into a **whole-slide image** (WSI). A single slide scanned at high magnification can reach 100,000 × 100,000 pixels. Uncompressed, that is about 30 gigabytes. After standard compression, it is usually 1–3 gigabytes.

No model can read such an image in one piece. So the image is cut into thousands of small tiles. A CNN scores each tile. The scores are combined into a slide-level result and a colour **heatmap** that shows where the model found suspicious tissue (Figure 6.2).

![Figure 6.2 — Whole-slide imaging pipeline](figures/orig-image5.png)
*Figure 6.2 — A whole-slide image is tiled, each tile is analysed by a CNN, and results are combined into a heatmap. Illustrative.*

Two studies show what is possible. One trained models on 44,732 slides using only the diagnosis from the pathology report as the label, without drawing outlines [12]. The authors estimated that it could spare pathologists from reviewing 65–75% of prostate slides while still catching every cancer in the test set. An international competition on prostate biopsies found that the best algorithms graded cancer in agreement with expert pathologists, including on slides from other countries [13].

![Figure 6.3 — AI-flagged regions in a whole-slide image](figures/orig-image17.png)
*Figure 6.3 — A digital slide before and after AI analysis, with flagged regions highlighted for the pathologist. Illustrative.*

Pathology AI has its own shift problems. Stain colour varies between laboratories and batches. Scanners differ. A model trained on one laboratory's slides may fail on another's.

## 6.5 The Clinical Laboratory
Laboratory results guide many decisions. A popular claim says they drive "70% of medical decisions". Researchers traced this figure and found no primary evidence for it [15]. It is better to say that laboratory results are central to diagnosis and monitoring, and to cite real studies.

Most laboratory errors happen before analysis: wrong patient, wrong tube, poor sample handling [14]. AI and automation help at several points.

- **Sample quality checks.** Analysers measure the colour of serum to detect **haemolysis** (burst red cells), **icterus** (high bilirubin) and **lipaemia** (high fat). These are called the HIL indices. Each can distort certain results, and the analyser flags or withholds them.
- **Delta checks.** Software compares a new result with the same patient's previous one. A sudden large change may be real, or it may mean the wrong patient's sample. For example, blood drawn from an arm with an intravenous drip is diluted, so most values fall falsely. A sudden false rise in creatinine suggests a mislabelled sample from another patient, or an interfering substance. The flag goes to the technologist and the requesting clinician to decide.
- **Image-based microscopy.** Digital systems pre-classify blood cells on a smear, and camera systems read bacterial culture plates. A technologist reviews what the system flags.

Machine-learning versions of these checks can combine many results at once. They still depend on stable analysers and good sample labelling.

> **Deeper Dive:** AI can find signals that people do not know how to see. A model trained on retinal photographs predicted age, sex, smoking status and blood pressure [16]. This field is called **oculomics**. These are research findings. They are not yet validated tests for individual patients.

> **Through Four Lenses**
> - **Medicine:** Physicians receiving AI-assisted reports should know whether a tool detects, diagnoses or triages. A triage flag speeds reading; it does not replace a full report or clinical correlation.
> - **Pharmacy:** Pharmacists rely on laboratory values for dosing, such as creatinine for kidney-cleared drugs. A delta-check flag or HIL warning means the value may be wrong. Confirm before adjusting a dose.
> - **Physical Therapy:** Physiotherapists read imaging reports to plan rehabilitation. An AI-flagged ligament tear still needs clinical tests of stability. Imaging findings and function do not always match.
> - **Health Sciences:** Imaging and laboratory technologists produce the inputs AI reads. Positioning, image quality, stain batches and analyser calibration all shift model performance. Document changes and report unusual outputs.

> **Myth vs Evidence:** Myth: "Imaging AI works equally well for everyone." Evidence: Dermatology models tested on a set balanced by skin tone performed worse on darker skin than on lighter skin [11]. Performance must be checked in each population.

> **Safety Alert:** An AI "normal" is not a guarantee. If the patient's symptoms or examination do not fit the report, ask for a human review.

## Key Takeaways
- CADe marks findings, CADx characterises them, and CADt reorders the worklist; each carries different risks.
- Diabetic eye screening and breast screening have prospective and randomised evidence; many other tools do not.
- Fast-MRI networks infer missing data, which saves time but can add or remove features.
- Digital pathology tiles huge images, scores each tile and builds a heatmap; stain and scanner shift are key risks.
- Laboratory AI supports sample-quality checks, delta checks and microscopy, and every flag needs human review.

## Self-Assessment
**Q1.** An AI tool moves CT scans with a suspected brain bleed to the top of the radiologist's list. It does not mark or describe the bleed. What type of tool is this? [LO1]
A) CADe
B) CADx
C) CADt
D) An ambient scribe

**Q2.** In a prospective primary-care study, an autonomous retinal system had 87.2% sensitivity and 90.7% specificity. Amal's result is "refer". What is the best interpretation? [LO2]
A) She needs specialist confirmation; some referred patients will not have significant disease.
B) She definitely has sight-threatening disease.
C) The result can be ignored because AI is not reliable.
D) She should start laser treatment today.

**Q3.** A radiology department wants to use an AI model for mammography. Which evidence would most strongly support its use in screening? [LO2]
A) A developer's report of high accuracy on its own data
B) A study with unpublished code and data
C) A single retrospective study from one hospital
D) A randomised screening trial showing more cancers found without more false positives

**Q4.** A fast-MRI knee scan shows a small cartilage defect that is absent on the standard slow scan. What is a plausible explanation? [LO3]
A) The fast scan used more radiation.
B) The reconstruction network inferred anatomy and added a feature that is not really there.
C) The patient's knee changed in five minutes.
D) Fast MRI recovers all missing data exactly.

**Q5.** A scan time falls from 40 minutes to 10 minutes. What is the percentage reduction? [LO3]
A) 25%
B) 40%
C) 75%
D) 400%

**Q6.** Why are whole-slide images cut into tiles before analysis? [LO4]
A) They are far too large for a model to process in one piece.
B) Tiling removes patient identifiers.
C) Pathologists prefer to see small squares.
D) Tiling corrects stain colour automatically.

**Q7.** A patient's creatinine was 85 µmol/L yesterday and is 300 µmol/L today. She is well, and her other results match another patient on the ward. What is the most likely explanation? [LO4]
A) Contamination from an intravenous drip, which raises creatinine
B) Normal daily variation
C) A haemolysed sample
D) A mislabelled sample from another patient

**Q8.** A pathology model trained in one laboratory performs poorly in a second laboratory. Which cause is most likely? [LO5]
A) The second laboratory's patients have no cancer.
B) Differences in stain colour and scanners between laboratories
C) The model was too simple.
D) The second laboratory used MRI instead of slides.

**Q9.** A skin-lesion model performs well on HAM10000 but worse on a test set balanced by skin tone. What is the most important lesson for Lina's care? [LO5]
A) Models cannot be used on skin.
B) Only dermatologists can read HAM10000.
C) Performance must be checked in people like her, including darker skin tones.
D) The balanced test set was wrong.

**Q10.** A retinal model predicts a patient's blood pressure from a photograph. How should this be described today? [LO5]
A) An interesting research finding, not yet a validated clinical test for individuals
B) A replacement for blood-pressure measurement
C) Proof that retinal photos contain no useful information
D) A regulated diagnostic test in all countries

**Case Question.** Amal is frightened by her "refer" result. As the healthcare assistant or nurse, write four sentences that explain what the result means, why she needs an eye specialist, and why she should not assume the worst.

## Answers and Rationales
**Q1. C** — Reordering the worklist is triage. A marks findings. B characterises them. D writes notes.

**Q2. A** — A referral from a screening tool needs confirmation; with 90.7% specificity, false positives occur [2]. B overstates. C dismisses good evidence. D skips diagnosis.

**Q3. D** — A randomised trial measuring detection and false positives is the strongest evidence [3]. A, B and C are weaker.

**Q4. B** — Reconstruction networks infer missing data from learned anatomy and can add or remove features [7]. A is false; MRI has no radiation. C is implausible. D is false.

**Q5. C** — (40 − 10) ÷ 40 = 75%. A is the remaining share. B and D are wrong calculations.

**Q6. A** — Gigapixel images exceed what models can process at once. B, C and D are not the reason.

**Q7. D** — A sudden large rise in a well patient, matching another patient's results, suggests a labelling error. A is wrong because drip contamination dilutes and lowers most values. B cannot explain this size of change. C affects some tests, such as potassium, more than creatinine.

**Q8. B** — Stain and scanner differences create distribution shift. A, C and D are unsupported.

**Q9. C** — Performance fell on darker skin in a balanced test set [11], so it must be checked in each group. A overgeneralises. B and D are wrong.

**Q10. A** — Oculomics findings are promising research [16], not validated individual tests. B, C and D are wrong.

**Case Question — model answer.** "The camera and computer found changes in the blood vessels at the back of your eyes that need a closer look. This test is designed to be careful, so it sometimes refers people whose eyes turn out to be fine. An eye specialist will examine you properly and decide whether you need treatment. If treatment is needed, catching it early like this is exactly what protects sight."

## References
1. Gulshan V, Peng L, Coram M, et al. Development and validation of a deep learning algorithm for detection of diabetic retinopathy in retinal fundus photographs. JAMA. 2016;316(22):2402-2410. DOI: 10.1001/jama.2016.17216
2. Abràmoff MD, Lavin PT, Birch M, et al. Pivotal trial of an autonomous AI-based diagnostic system for detection of diabetic retinopathy in primary care offices. NPJ Digit Med. 2018;1:39. DOI: 10.1038/s41746-018-0040-6
3. Lång K, Josefsson V, Larsson AM, et al. Artificial intelligence-supported screen reading versus standard double reading in the Mammography Screening with Artificial Intelligence trial (MASAI): a clinical safety analysis of a randomised, controlled, non-inferiority, single-blinded, screening accuracy study. Lancet Oncol. 2023;24(8):936-944. DOI: 10.1016/s1470-2045(23)00298-x
4. McKinney SM, Sieniek M, Godbole V, et al. International evaluation of an AI system for breast cancer screening. Nature. 2020;577(7788):89-94. DOI: 10.1038/s41586-019-1799-6
5. Haibe-Kains B, Adam GA, Hosny A, et al. Transparency and reproducibility in artificial intelligence. Nature. 2020;586(7829):E14-E16. DOI: 10.1038/s41586-020-2766-y
6. Dembrower K, Crippa A, Colón E, Eklund M, Strand F. Artificial intelligence for breast cancer detection in screening mammography in Sweden: a prospective, population-based, paired-reader, non-inferiority study. Lancet Digit Health. 2023;5(10):e703-e711. DOI: 10.1016/S2589-7500(23)00153-X
7. Hammernik K, Klatzer T, Kobler E, et al. Learning a variational network for reconstruction of accelerated MRI data. Magn Reson Med. 2018;79(6):3055-3071. DOI: 10.1002/mrm.26977
8. Bien N, Rajpurkar P, Ball RL, et al. Deep-learning-assisted diagnosis for knee magnetic resonance imaging: development and retrospective validation of MRNet. PLoS Med. 2018;15(11):e1002699. DOI: 10.1371/journal.pmed.1002699
9. Esteva A, Kuprel B, Novoa RA, et al. Dermatologist-level classification of skin cancer with deep neural networks. Nature. 2017;542(7639):115-118. DOI: 10.1038/nature21056
10. Tschandl P, Rosendahl C, Kittler H. The HAM10000 dataset, a large collection of multi-source dermatoscopic images of common pigmented skin lesions. Sci Data. 2018;5:180161. DOI: 10.1038/sdata.2018.161
11. Daneshjou R, Vodrahalli K, Novoa RA, et al. Disparities in dermatology AI performance on a diverse, curated clinical image set. Sci Adv. 2022;8(32):eabq6147. DOI: 10.1126/sciadv.abq6147
12. Campanella G, Hanna MG, Geneslaw L, et al. Clinical-grade computational pathology using weakly supervised deep learning on whole slide images. Nat Med. 2019;25(8):1301-1309. DOI: 10.1038/s41591-019-0508-1
13. Bulten W, Kartasalo K, Chen PHC, et al. Artificial intelligence for diagnosis and Gleason grading of prostate cancer: the PANDA challenge. Nat Med. 2022;28(1):154-163. DOI: 10.1038/s41591-021-01620-2
14. Plebani M. Errors in clinical laboratories or errors in laboratory medicine? Clin Chem Lab Med. 2006;44(6):750-759. DOI: 10.1515/cclm.2006.123
15. Hallworth MJ. The '70% claim': what is the evidence base? Ann Clin Biochem. 2011;48(6):487-488. DOI: 10.1258/acb.2011.011177
16. Poplin R, Varadarajan AV, Blumer K, et al. Prediction of cardiovascular risk factors from retinal fundus photographs via deep learning. Nat Biomed Eng. 2018;2(3):158-164. DOI: 10.1038/s41551-018-0195-0
17. Zech JR, Badgeley MA, Liu M, et al. Variable generalization performance of a deep learning model to detect pneumonia in chest radiographs: a cross-sectional study. PLoS Med. 2018;15(11):e1002683. DOI: 10.1371/journal.pmed.1002683
