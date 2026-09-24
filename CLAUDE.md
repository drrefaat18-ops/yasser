# CLAUDE.md — Medical AI Textbook Evaluation Project

## Project Overview
This repository contains the complete manuscript of the textbook:
**"ARTIFICIAL INTELLIGENCE IN MEDICINE"**
By: **Assistant Prof. Dr. Shereen Elsaid Elkholy**

Your primary mission when operating in this workspace is to perform a rigorous, academic, clinical, and pedagogical peer-review of this textbook.

---

## Workspace Structure & Key Files
- `AI_in_Medicine- Assistant Prof Dr Shereen Elkholy.md`: The complete textbook in Markdown format (~26,500 words, 7 Chapters, Tables, Question Banks, and References).
- `images/`: Directory containing 24 clinical figures, neural network architectures, and diagnostic diagrams referenced throughout the text (`image1.jpeg` through `image24.png`).
- `EVALUATION_RUBRIC.md`: The structured peer-review evaluation matrix and scoring rubric.
- `EVALUATION_GUIDE.md`: Step-by-step instructions and recommended prompt workflows for conducting the evaluation.
- `.claude/agents/`: Specialized academic and clinical agent personas for multi-perspective critique:
  - `medical-ai-reviewer.md`: Lead Medical AI Peer Reviewer & Clinical Educator.
  - `academic-statistician.md`: Quantitative methods, validation metrics, and study design auditor.
  - `research-synthesist.md`: Literature sourcing, citation checking, and evidence synthesis.

---

## Textbook Outline
- **Chapter 1:** Fundamentals of Artificial Intelligence in Healthcare (~1,150 words)
- **Chapter 2:** AI in Diagnostic Radiology & Medical Imaging (~3,670 words)
- **Chapter 3:** AI in Clinical Pathology & Automated Laboratory Diagnostics (~1,460 words)
- **Chapter 4:** AI in Surgery & Surgical Robotics (~1,850 words)
- **Chapter 5:** AI in Interventional Medicine & Cardiology (~3,000 words)
- **Chapter 6:** AI Applications Across Clinical Medical Specialties (~2,250 words)
- **Chapter 7:** Ethics, Medicolegal Challenges & Future Horizons (~5,000 words)
- **References:** Consolidated bibliographies across all chapters.

---

## Peer-Review Framework: The 6 Core Pillars

When evaluating any chapter or the entire manuscript, assess against these six dimensions:

### 1. Clinical & Medical Accuracy
- Are anatomical structures, disease definitions, surgical stages, and laboratory assays medically sound and up to date?
- Are clinical workflows (PACS/DICOM triage, digital pathology pipelines, robotic surgical consoles) faithfully represented?
- Are the "Clinical Pearls", "Radiology Alerts", and "Surgical Pearls" practically actionable and safe?

### 2. AI & Computational Rigor
- Are AI/ML/DL concepts explained with technical correctness (e.g., CNNs, ViTs, U-Net, GANs, Transformers, LLMs, Diffusion models)?
- Are evaluation metrics correctly differentiated and applied (e.g., Sensitivity vs. Specificity, AUROC vs. AUPRC, Dice coefficient, F1 score)?
- Are the mathematical explanations (e.g., k-space undersampling, loss functions, Fourier transform) accurate yet accessible?

### 3. Pedagogical Quality & Educational Design
- Is the content well-calibrated for medical students, clinical fellows, and practicing healthcare professionals?
- Does each chapter present clear learning objectives, structured subheadings, and progressive cognitive difficulty?
- Are clinical case vignettes and analogies effective in demystifying computational concepts?

### 4. Self-Assessment & Question Bank Quality
- Are Multiple Choice Questions (MCQs) written with clear clinical vignettes?
- Are distractors plausible rather than trivially false?
- Are answer rationales medically and technically rigorous, explaining *why* the correct answer is right and *why* distractors are wrong?

### 5. Ethics, Medicolegal & Regulatory Depth
- Are regulatory pathways (FDA 510(k), De Novo, PMA, PCCP for adaptive models, EU AI Act, CE-MDR) accurately explained?
- Are medical liability models (Learned Intermediary Doctrine, Vicarious Liability, Enterprise Liability) correctly analyzed?
- Are algorithmic bias, health disparities, HIPAA Safe Harbor, and GDPR requirements thoroughly examined?

### 6. Sourcing, Fact-Checking & Literature Currency
- Are milestone studies, benchmark datasets (CheXpert, MIMIC-CXR, TCGA), and landmark papers accurately cited?
- Are claims supported by current peer-reviewed evidence (2018–2026)?
- Flag any unsubstantiated performance claims, outdated protocols, or potential AI hallucinations.

---

## Deliverables Expected from Claude

1. **Chapter-by-Chapter Peer Review Reports:**
   - Executive Summary & Strengths.
   - Critical Analysis against the 6 Pillars.
   - Specific Line-by-Line Errata & Technical Inaccuracies.
   - Question Bank & MCQ Audit.
   - Concrete Revision Recommendations (with sample replacement text where applicable).

2. **Comprehensive Textbook Scorecard:**
   - Quantitative rubric score (1–10 per pillar).
   - Global Readiness Assessment (Publication / Curriculum readiness).
   - Gap Analysis: Essential missing topics that should be added to the next edition.
