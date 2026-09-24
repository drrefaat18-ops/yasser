# Interprofessional Rework — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans (user chose inline execution; personas from `.agents/skills/` are adopted inline, not spawned). Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce an 11-chapter, ~26,500-word interprofessional English textbook for year 1–2 medicine, pharmacy, physical therapy and health-sciences students, rebuilt from Dr. Elkholy's manuscript.

**Architecture:** One Markdown file per chapter under `rework/`, each following a fixed template that a stdlib-Python checker (`rework/tools/check_book.py`) validates. Chapters are drafted in order, each gated by the checker plus a persona review pass; a final assembly script concatenates them into one book file.

**Tech Stack:** Markdown, Python 3 stdlib only (checker, assembler, DOI verifier), git for versioning.

**Spec:** `docs/superpowers/specs/2026-09-24-interprofessional-rework-design.md` — read it before any task.

## Global Constraints

- English only. Audience: year 1–2 pre-clinical, four professions.
- Word budgets (everything except the References section): Ch0 500 · Ch1 2,000 · Ch2 2,000 · Ch3 2,400 · Ch4 2,700 · Ch5 2,400 · Ch6 2,800 · Ch7 2,400 · Ch8 2,400 · Ch9 2,300 · Ch10 2,200 · Ch11 2,400. Tolerance ±15%; book total 24,000–29,000.
- Mean sentence length ≤ 22 words; sentences > 40 words < 5%.
- 10 MCQs (A–D only) + 1 short-answer case per chapter 1–11; per chapter each letter 2–3 times; no letter 3× consecutively; answers only at chapter end.
- Every performance number, trial, dataset, regulation → in-text `[n]` citation; every reference exists (DOI-verified where one exists).
- Default noun "clinician" / "health professional"; "leader–follower" never "master–slave"; no LO uses "understand".
- Original manuscript `.md`/`.docx` is never modified.
- Existing figures referenced as `../images/imageN.png`; new figures in `rework/figures/`.

## Review Focus

1. **Checker false pass on bold labels** — a bold label like `**Note:**` must not be treated as a glossary term, and a real term must not slip through; test pins both (Task 1).
2. **MCQ parse drift** — a question with a missing option or an "E)" option must fail, not be silently skipped (Task 1).
3. **Citation `[1,3]` / `[2–4]` forms** — ranges and lists must resolve each number; an uncited reference must fail (Task 1).
4. **Clinical content re-imported from the original with its old error** — every reused paragraph checked against the spec §7 correction table; ledger row required (every chapter task, Step "ledger").
5. **Lens imbalance** — a chapter whose Pharmacy or PT lens paragraph is a token sentence; checker enforces ±20% length (Task 1), reviewer checks substance.

---

## File Structure

```
rework/
  tools/check_book.py        # all automated acceptance checks (spec §12)
  tools/test_check_book.py   # self-test with pass/fail fixtures
  tools/verify_refs.py       # DOI existence check via CrossRef
  tools/assemble.py          # concatenate chapters into the book file
  _template.md               # canonical chapter skeleton (parsing contract)
  00-front-matter.md
  ch01-what-ai-is.md
  ch02-health-data.md
  ch03-how-models-learn.md
  ch04-reading-performance-claims.md
  ch05-generative-ai-llms.md
  ch06-seeing-disease.md
  ch07-medicines.md
  ch08-ai-in-motion.md
  ch09-monitoring-prediction.md
  ch10-bias-fairness-privacy.md
  ch11-regulation-liability-human.md
  glossary.md
  errata-ledger.md
  figures/
  REVIEW_REPORT.md
AI_in_Health_Care_Interprofessional.md   # assembled output
```

---

### Task 0: Workspace setup

**Files:** Create `rework/`, `rework/tools/`, `rework/figures/`, `.gitignore`

- [ ] **Step 1:** `cd /d/yasser && git init && mkdir -p rework/tools rework/figures`
- [ ] **Step 2:** Write `.gitignore`:
```
__pycache__/
*.pyc
_preview*.png
```
- [ ] **Step 3:** Commit baseline (original manuscript, spec, plan) so every later change is diffable:
```bash
git add -A && git commit -m "chore: baseline original manuscript, review docs, rework spec and plan"
```

---

### Task 1: Chapter template + checker (the test harness)

**Files:**
- Create: `rework/_template.md`, `rework/tools/check_book.py`, `rework/tools/test_check_book.py`

**Interfaces:**
- Produces: `python rework/tools/check_book.py <chapter.md>` → exit 0 + "PASS" or exit 1 + one line per failure. `python rework/tools/check_book.py --all` → checks every `rework/ch*.md` plus book totals, glossary and ledger.
- Parsing contract (every chapter must follow exactly):
  - H1 `# Chapter N: Title`
  - H2 in order: `## Opening Case`, `## Learning Objectives`, core `##` sections, `## Key Takeaways`, `## Self-Assessment`, `## Answers and Rationales`, `## References`
  - Blockquote boxes whose first line is one of: `> **Medical Background in 60 Seconds:**`, `> **Through Four Lenses**`, `> **Myth vs Evidence:**`, `> **Safety Alert:**`, `> **Deeper Dive:**`
  - Lens lines inside the lens box: `> - **Medicine:** …`, `> - **Pharmacy:** …`, `> - **Physical Therapy:** …`, `> - **Health Sciences:** …`
  - LOs: `1. [LO1] Explain …`
  - MCQ: `**Q1.** stem [LO2]` then lines `A) …` … `D) …`
  - Short answer: `**Case Question.** …`
  - Answer lines: `**Q1. C** — rationale …`
  - References: `1. Author … DOI: 10.xxxx/…`
  - Glossary term, first use: `**term**` (bold not ending in `:`); labels always end in `:`.

- [ ] **Step 1: Write `rework/_template.md`** — the skeleton above with one example of every element (this doubles as the passing fixture's shape).

- [ ] **Step 2: Write the failing self-test** `rework/tools/test_check_book.py`:

```python
import pathlib, subprocess, sys, textwrap, tempfile

TOOL = pathlib.Path(__file__).with_name("check_book.py")

GOOD = textwrap.dedent("""\
# Chapter 99: Fixture

## Opening Case
Lina asks a chatbot about a mole. She is worried.

## Learning Objectives
1. [LO1] Explain what a **model** is.
2. [LO2] Calculate positive predictive value.
3. [LO3] Identify one risk of a chatbot.

## Core Idea
A model learns patterns from data [1]. Accuracy can mislead [2, 3].

> **Medical Background in 60 Seconds:** A mole is a skin growth.

> **Through Four Lenses**
> - **Medicine:** Doctors read the output with care.
> - **Pharmacy:** Pharmacists check doses with care.
> - **Physical Therapy:** Therapists check movement with care.
> - **Health Sciences:** Technologists check samples with care.

> **Myth vs Evidence:** Myth. Evidence [1].

> **Safety Alert:** Always confirm.

## Key Takeaways
- One.

## Self-Assessment
{mcqs}
**Case Question.** What would you do?

## Answers and Rationales
{answers}

## References
1. Author A. Title. J. 2020. DOI: 10.1000/x1
2. Author B. Title. J. 2021.
3. Author C. Title. J. 2022.
""")

KEYS = "ABCDABCDAC"

def mcqs(keys=KEYS, extra=""):
    qs = "".join(f"**Q{i+1}.** Stem [LO{1 + i % 3}]\nA) a\nB) b\nC) c\nD) d\n{extra}\n" for i in range(len(keys)))
    ans = "".join(f"**Q{i+1}. {k}** — because.\n" for i, k in enumerate(keys))
    return qs, ans

def run(text, glossary="model\n"):
    d = pathlib.Path(tempfile.mkdtemp())
    (d / "glossary.md").write_text(f"**{glossary.strip()}** — def\n", encoding="utf-8")
    f = d / "ch99.md"
    f.write_text(text, encoding="utf-8")
    r = subprocess.run([sys.executable, str(TOOL), str(f), "--budget", "0", "--glossary", str(d / "glossary.md")],
                       capture_output=True, text=True)
    return r.returncode, r.stdout

def build(keys=KEYS, extra="", body_sub=None):
    q, a = mcqs(keys, extra)
    t = GOOD.format(mcqs=q, answers=a)
    if body_sub:
        t = t.replace(*body_sub)
    return t

def test_good_passes():
    code, out = run(build())
    assert code == 0, out

def test_key_imbalance_fails():
    code, out = run(build(keys="BBBBBBBBBA"))
    assert code == 1 and "key" in out.lower()

def test_option_e_fails():
    code, out = run(build(extra="E) e"))
    assert code == 1 and "option e" in out.lower()

def test_uncited_reference_fails():
    code, out = run(build(body_sub=("[2, 3]", "[2]")))
    assert code == 1 and "uncited" in out.lower()

def test_citation_range_resolves():
    code, out = run(build(body_sub=("[2, 3]", "[2–3]")))
    assert code == 0, out

def test_bold_label_not_glossary_term_but_real_term_checked():
    code, out = run(build(), glossary="other")
    assert code == 1 and "model" in out and "Medicine" not in out

def test_understand_in_lo_fails():
    code, out = run(build(body_sub=("Explain what", "Understand what")))
    assert code == 1 and "understand" in out.lower()

def test_lens_imbalance_fails():
    code, out = run(build(body_sub=("Pharmacists check doses with care.", "Yes.")))
    assert code == 1 and "lens" in out.lower()

def test_master_slave_fails():
    code, out = run(build(body_sub=("A model learns", "A master-slave model learns")))
    assert code == 1 and "master" in out.lower()

if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn(); print("ok", name)
```

- [ ] **Step 3:** Run `python rework/tools/test_check_book.py` → Expected: FAIL (check_book.py missing).

- [ ] **Step 4: Implement `rework/tools/check_book.py`** (stdlib only). Functions, each returning a list of failure strings:
  - `words(text)` — count words excluding the `## References` section.
  - `check_budget(text, budget)` — skip if budget 0; fail if outside ±15%. Default budgets from a dict keyed by chapter number (Global Constraints).
  - `check_sentences(text)` — prose only (drop tables, blockquote labels, MCQ/answer sections, code); split on `(?<=[.!?])\s+`; mean ≤ 22, share > 40 words < 5%.
  - `check_template(text)` — required H2s present in order; all five box labels present (Deeper Dive optional).
  - `check_lenses(text)` — four lens lines present; each length within ±20% of their mean word count; else "lens imbalance: …".
  - `check_los(text)` — lines matching `^\d+\. \[LO\d+\]`; 3–5 of them; fail if any contains "understand" (case-insensitive).
  - `check_mcqs(text)` — parse `**Qn.**` blocks in Self-Assessment: exactly options A–D each; any `^E\)` → "option E present"; exactly 10 questions; each LO tag referenced exists; parse answers `**Qn. X**`; every Q has an answer with non-empty rationale; per-letter counts 2–3 → else "key imbalance"; no letter 3× consecutive; every LO has ≥ 1 question.
  - `check_citations(text)` — collect `\[(\d+(?:\s*[,–-]\s*\d+)*)\]` from body (outside References), expand ranges; each number must exist in References numbering; each reference number cited ≥ 1 → else "uncited reference n"; "missing reference n".
  - `check_glossary(text, glossary_path)` — terms = `\*\*([^*]+?)\*\*` in body where term does not end in `:`, not inside lens lines/box labels, not `Qn.`/answer markers, not `Case Question.`; glossary entries = `^\*\*(.+?)\*\*` lines in glossary file (case-insensitive); fail "glossary missing: term".
  - `check_banned(text)` — "master-slave"/"master–slave" → fail.
  - `--all` mode: run all per-chapter checks with default budgets on `rework/ch*.md`; totals 24,000–29,000; `rework/errata-ledger.md` has no row containing `| open |`; `rework/glossary.md` has ≥ 120 entries.
  - CLI: `check_book.py PATH [--budget N] [--glossary PATH]`; default glossary `rework/glossary.md`; print failures, `PASS` if none; exit code accordingly.

- [ ] **Step 5:** Run `python rework/tools/test_check_book.py` → Expected: all `ok`.
- [ ] **Step 6:** Commit: `git add rework && git commit -m "feat(rework): chapter template and acceptance checker"`

---

### Task 2: Errata ledger + figure triage

**Files:** Create `rework/errata-ledger.md`

- [ ] **Step 1:** Create ledger table `| # | Topic | Original line(s) | Correct statement | Target chapter | Status |` with one row per item of spec §7 correction table (18 rows) plus these from `SESSION_SUMMARY.md` §3.3/3.4: WSI file size (~30 GB uncompressed; 1–3 GB compressed), ASC-US meaning, S. pneumoniae morphology, 7 DOF comparison, haptic fixtures (orthopaedics only), brain shift 10–20 mm, JPEG vs adversarial, FFR-CT uses CFD, cusp-overlap, "70% of decisions" claim (unsupported — do not repeat), GDPR "right to explanation" (contested), McKinney 2020 contested. Status initially `open`; target chapter or `removed-with-content`.
- [ ] **Step 2:** View `images/image7.png`, `image11.png`, `image14.png`, `image16.png` with the Read tool. Record decision (keep/drop + required caption) in a "Figures" section of the ledger. image11: drop if it shows CBV < 30% as core.
- [ ] **Step 3:** Mark `removed-with-content` rows now (TAVR, CVS, IVUS, EVAR, ICG, cusp-overlap, etc.) — closed.
- [ ] **Step 4:** Commit: `git commit -am "docs(rework): errata ledger and figure triage"` (after `git add rework/errata-ledger.md`).

---

### Task 3: Reference verifier

**Files:** Create `rework/tools/verify_refs.py`

**Interfaces:** `python rework/tools/verify_refs.py rework/ch04-….md` → for each reference with a DOI, GET `https://api.crossref.org/works/<doi>`; print `OK n`, `NOT FOUND n`, or `TITLE MISMATCH n` (compare lowercase first 6 title words). Exit 1 on any NOT FOUND/MISMATCH. References without DOI printed as `NO DOI n` (allowed only for laws/guidance documents with a URL).

- [ ] **Step 1:** Implement with `urllib.request` + `json`, 10 s timeout, User-Agent header with `mailto` omitted.
- [ ] **Step 2:** Test on a known DOI: create temp file with `1. Obermeyer Z, et al. Dissecting racial bias in an algorithm used to manage the health of populations. Science. 2019. DOI: 10.1126/science.aax2342` → Expected `OK 1`. Then a fake DOI `10.9999/fake.123` → Expected `NOT FOUND 1`, exit 1.
- [ ] **Step 3:** If network is blocked from Bash, fallback documented in the script docstring: verify via WebFetch tool on `https://api.crossref.org/works/<doi>` manually and record in chapter commit message.
- [ ] **Step 4:** Commit: `git add rework/tools/verify_refs.py && git commit -m "feat(rework): DOI verifier"`

---

### Per-chapter procedure (applies to Tasks 4–15)

Each chapter task below lists content; every one runs these steps:

- [ ] **A. Red:** `python rework/tools/check_book.py rework/<file>` → Expected FAIL (file missing).
- [ ] **B. Draft** the chapter to `_template.md` using the content spec in the task; reused original text rewritten to sentence rules; check each reused claim against the errata ledger.
- [ ] **C. Glossary:** append new bold terms to `rework/glossary.md` as `**term** — one-sentence plain definition.` (alphabetical order).
- [ ] **D. Green:** run checker until PASS.
- [ ] **E. References:** `python rework/tools/verify_refs.py rework/<file>` → all OK (drop or replace any reference that fails; never keep an unverified one).
- [ ] **F. Persona review inline** (read the persona file in `.agents/skills/<name>/SKILL.md` first, then review as that persona; write findings as a short list, fix them): psychologist (cognitive load, emotional arc, MCQ fairness) on every chapter + the personas named in the task.
- [ ] **G. Ledger:** set relevant errata rows to `fixed` with chapter + section.
- [ ] **H. Commit:** `git add rework && git commit -m "feat(rework): chapter N — <title>"`

---

### Task 4: Front matter + patient bible

**File:** `rework/00-front-matter.md` (500 words; checker not applied — template is for chapters)
**Persona:** narratologist, anthropologist

Content: title, author line (Dr. Shereen Elsaid Elkholy), "How to Use This Book" (Part I compulsory for all; per-profession suggested emphasis in Part II: Medicine → 6, 9; Pharmacy → 7, 9; PT → 8, 6; Health Sciences → 2, 6, 9), box legend, "Meet the Patients" — three profiles from spec §4 (age, occupation, conditions, what each is worried about, which professionals meet them). Fixed facts recorded here are canonical for all later chapters (Amal: 61, T2DM + hypertension, 7 medications, eGFR 52; Karim: 34, construction worker, ACL injury left knee; Lina: 20, biology student (not a health-profession student, to avoid audience identity clash), Fitzpatrick V, changing mole on forearm, health anxiety).

Commit: `feat(rework): front matter and patient bible`

---

### Task 5: Chapter 1 — What AI Is — and Isn't (2,000)

**File:** `rework/ch01-what-ai-is.md` · **Personas:** historian, psychologist · **Case:** Lina asks a chatbot about her mole.
**LOs:** distinguish AI/ML/DL/generative AI; contrast rule-based vs learned systems with a health example; describe 3 milestones in medical AI history; identify one benefit and one risk per profession.
**Sections:**
1. Definitions (reuse §1.1, rewritten; Fig 1.1 `../images/image2.png`).
2. Rules vs learning (reuse CLINICAL CORRELATION box, but example: drug-interaction rule vs learned risk model).
3. A short history: Dartmouth 1956, MYCIN 1970s (never deployed — why), 2012 deep learning/ImageNet, 2016 Gulshan retina, 2018 first autonomous FDA device (IDx-DR), 2022–23 LLMs. Historian: mark each date with source.
4. What AI can and cannot do today (reuse §1.2 condensed; remove "eradication of cognitive errors" framing; MASAI claim corrected per ledger).
5. Preview of risks (one paragraph each for bias, hallucination, automation bias — forward links to Ch3, 5, 10, 11).
**Myth vs Evidence:** "AI will replace clinicians."
**Key refs:** McCarthy 1955 proposal; Shortliffe 1976 (MYCIN); Krizhevsky 2012; Gulshan 2016 JAMA; Abràmoff 2018 npj Digit Med; Topol 2019 Nat Med; Rajkomar 2019 NEJM; Lång 2023 Lancet Oncol.

### Task 6: Chapter 2 — Health Data (2,000)

**File:** `rework/ch02-health-data.md` · **Personas:** statistician, anthropologist · **Case:** Amal's record — prescriptions, lab results, retinal photo, nurse notes, pharmacy refill history.
**LOs:** classify health data types (structured, image, signal, text, omics); explain labels and why labelling is costly; identify data-quality problems (missingness, coding errors, bias in who gets tested); describe standards (DICOM, HL7 FHIR, ICD/SNOMED) at recognition level.
**Sections:** data types with one example per profession; where labels come from (clinician annotation, codes, outcomes) and label noise; data quality & "missing not at random"; standards & interoperability; landmark datasets (MIMIC-IV, MIMIC-CXR, CheXpert, ChestX-ray8, TCGA, UK Biobank) with who is (not) represented.
**Deeper Dive:** what an image is to a computer (pixel arrays, DICOM metadata).
**Key refs:** Johnson 2023 Sci Data (MIMIC-IV); Johnson 2019 Sci Data (MIMIC-CXR); Irvin 2019 AAAI (CheXpert); Wang 2017 CVPR; Weinstein 2013 Nat Genet (TCGA); Bycroft 2018 Nature; Agniel 2018 BMJ (timing of lab tests as signal).

### Task 7: Chapter 3 — How Models Learn — and How They Fail (2,400)

**File:** `rework/ch03-how-models-learn.md` · **Personas:** statistician (co-author), psychologist · **Case:** a knee-injury model trained on athletes misses Karim's pattern.
**LOs:** explain supervised vs unsupervised vs reinforcement learning; describe train/validation/test split; distinguish overfitting, data leakage (correct meaning), shortcut learning, distribution shift; explain class imbalance.
**Sections:** learning from examples (loss, parameters — intuitive, no equations in body); neural networks & CNNs in one page (U-Net named, defined); splits (new figure `figures/split-leakage.svg`); overfitting; leakage (patient-level split, future information, e.g. Epic sepsis & label leakage); shortcut learning (Zech 2018 portable-X-ray marker; DeGrave 2021 COVID); distribution shift (reuse §2.4.1 corrected); class imbalance; "ML is not always better" (Christodoulou 2019).
**Deeper Dive:** loss function and gradient descent with one worked number.
**Key refs:** Zech 2018 PLoS Med; DeGrave 2021 Nat Mach Intell; Geirhos 2020 Nat Mach Intell; Roberts 2021 Nat Mach Intell; Kapoor & Narayanan 2023 Patterns; Finlayson 2021 NEJM; Christodoulou 2019 J Clin Epidemiol; Ronneberger 2015 MICCAI.

### Task 8: Chapter 4 — Reading an AI Performance Claim (2,700)

**File:** `rework/ch04-reading-performance-claims.md` · **Personas:** statistician (author), research-synthesist · **Case:** app tells Lina it is "95% accurate".
**LOs:** calculate sensitivity, specificity, PPV, NPV from a 2×2 table; explain PPV dependence on prevalence; interpret ROC/AUROC and when AUPRC is preferable; distinguish discrimination from calibration; rank evidence from retrospective study to RCT.
**Sections:** confusion matrix (new figure `figures/confusion-ppv.svg`); accuracy paradox; worked example 95%/95% at 5/1000 → PPV ≈ 8.7% (show arithmetic); thresholds & ROC; AUROC vs AUPRC under imbalance; calibration (softmax ≠ probability — ledger); segmentation metrics Dice/IoU (one paragraph); internal vs external vs prospective validation; evidence ladder with MASAI, EchoNet-RCT (He 2023), Epic sepsis external validation (Wong 2021); reporting guidelines TRIPOD+AI, CONSORT-AI, SPIRIT-AI, DECIDE-AI; "Ten questions to ask a vendor" checklist.
**Deeper Dive:** Bayes' theorem link to PPV.
**MCQs:** ≥ 4 calculation items.
**Key refs:** Collins 2024 BMJ; Liu 2020 Nat Med; Cruz Rivera 2020 Nat Med; Vasey 2022 Nat Med; Van Calster 2019 BMC Med; Saito & Rehmsmeier 2015 PLoS One; Maier-Hein 2024 Nat Methods; Nagendran 2020 BMJ; Wong 2021 JAMA Intern Med; He 2023 Nature; Lång 2023.

### Task 9: Chapter 5 — Generative AI & LLMs (2,400)

**File:** `rework/ch05-generative-ai-llms.md` · **Personas:** psychologist, research-synthesist · **Case:** Lina pastes her symptoms into an LLM; a pharmacist later drafts a patient leaflet with one.
**LOs:** explain next-token prediction and why it produces hallucination; identify safe vs unsafe uses for a student and a professional; apply a safe-prompting checklist (no identifiable patient data, verify against primary source); describe RAG and ambient scribes; evaluate an LLM answer for accuracy and bias.
**Sections:** how LLMs work (tokens, training, fine-tuning, RLHF — plain language; figure `figures/next-token.svg`); hallucination (fabricated references — link to Ch1); benchmarks vs real care (Med-PaLM exam scores ≠ clinical safety); uses: documentation/ambient scribes, patient communication (Ayers 2023 with its limits), drug information, education; risks: bias (Omiye 2023), privacy, over-trust; RAG; students & academic integrity; WHO LMM guidance.
**Safety Alert:** never paste identifiable patient data into a public chatbot.
**Key refs:** Vaswani 2017; Singhal 2023 Nature; Thirunavukarasu 2023 Nat Med; Lee 2023 NEJM; Ayers 2023 JAMA Intern Med; Omiye 2023 npj Digit Med; Lewis 2020 NeurIPS (RAG); WHO 2024 LMM guidance; Tierney 2024 NEJM Catalyst.

### Task 10: Chapter 6 — Seeing Disease (2,800)

**File:** `rework/ch06-seeing-disease.md` · **Personas:** statistician, anthropologist · **Case:** Amal's retinal screen + Karim's knee MRI; Lina's mole (dermatology on dark skin).
**LOs:** distinguish CADe/CADx/CADt; describe AI in screening (retina, mammography) and its evidence; explain why fast MRI can hallucinate; describe the digital-pathology pipeline; describe lab automation checks (HIL, delta checks).
**Sections:** Medical Background boxes (what X-ray/CT/MRI/retinal photo/biopsy are); triage & CAD types (reuse §2.1.2, fig `../images/image3.png` re-captioned); screening: retina (Gulshan, IDx-DR), mammography (MASAI; McKinney + Haibe-Kains); fast MRI concept (ledger: aliasing, inferred not recovered, 75–80%); knee MRI (MRNet, Bien 2018); dermatology (Esteva 2017, HAM10000, DDI skin-tone gap; fig `../images/image15.png`); digital pathology (WSI tiling, heatmaps, fig `../images/image5.png`; Campanella 2019, PANDA); the laboratory: HIL indices, delta checks (ledger corrected), AI in Gram stain/plate reading (one paragraph); oculomics (`../images/image19.png`, Poplin 2018) as bridge to Ch9; reuse §2.4/2.5 failure modes condensed.
**Lens box:** Health Sciences = imaging/lab technologist's role in QC.
**Key refs:** Gulshan 2016; Abràmoff 2018; Lång 2023; McKinney 2020; Haibe-Kains 2020; Zbontar 2018 arXiv; Hammernik 2018 Magn Reson Med; Bien 2018 PLoS Med; Esteva 2017; Tschandl 2018 Sci Data; Daneshjou 2022 Sci Adv; Campanella 2019; Bulten 2022 Nat Med; Plebani 2006 Clin Chem Lab Med; Poplin 2018 Nat Biomed Eng.

### Task 11: Chapter 7 — Medicines (2,400)

**File:** `rework/ch07-medicines.md` · **Personas:** research-synthesist, anthropologist · **Case:** Amal's new prescription triggers an interaction alert; pharmacist decides.
**LOs:** describe AI's role across drug discovery stages; explain alert fatigue and why most interaction alerts are overridden; describe model-informed precision dosing using a Bayesian example (vancomycin AUC); explain AI in pharmacovigilance (signal detection from text); identify risks of LLM drug information.
**Sections:** Medical Background (drug development stages, what an interaction is); discovery: AlphaFold (structure ≠ drug), generative chemistry, halicin; clinical decision support & alert fatigue; ML medication-error detection (Corny 2020); precision dosing & pharmacogenomics; pharmacovigilance & real-world data; automated dispensing & supply; LLM drug-info pitfalls (link Ch5).
**Key refs:** Jumper 2021 Nature; Stokes 2020 Cell; Zhavoronkov 2019 Nat Biotechnol; van der Sijs 2006 J Am Med Inform Assoc; Corny 2020 J Am Med Inform Assoc; Darwich 2017 Clin Pharmacol Ther; Rybak 2020 Am J Health Syst Pharm; Relling & Evans 2015 Nature; Harpaz 2012 Clin Pharmacol Ther. (Verify all via Step E; replace any that fail.)

### Task 12: Chapter 8 — AI in Motion (2,400)

**File:** `rework/ch08-ai-in-motion.md` · **Personas:** psychologist, historian · **Case:** Karim's rehab — smartphone video gait analysis, wearable step/ROM tracking, tele-rehab.
**LOs:** describe pose estimation and its use in gait/ROM assessment; explain how wearables (IMUs) generate movement data and their validity limits; distinguish levels of autonomy in robotics (0–5); describe AI-based skill assessment; identify safety limits of autonomous systems.
**Sections:** Medical Background (gait cycle, ROM); pose estimation (OpenPose, video gait — new fig `figures/pose-skeleton.svg`); markerless vs marker-based validity; wearables & IMUs; tele-rehab & adherence; exoskeletons (one paragraph); surgical robots: leader–follower telemanipulation, tremor filtering (8–12 Hz), autonomy levels (reuse §4.3.1), STAR as preclinical (ledger); skill assessment (kinematics; OSATS from Martin 1997); AR navigation one paragraph with brain-shift caveat (if image7 kept).
**Key refs:** Cao 2021 IEEE TPAMI (OpenPose); Stenum 2021 PLoS Comput Biol; Kidziński 2020 Nat Commun; Kanko 2021 J Biomech; Cottrell 2017 Clin Rehabil; Yang 2017 Sci Robot; Saeidi 2022 Sci Robot; Martin 1997 Br J Surg; Maier-Hein 2017 Nat Biomed Eng.

### Task 13: Chapter 9 — Monitoring, Prediction & Population Health (2,300)

**File:** `rework/ch09-monitoring-prediction.md` · **Personas:** statistician · **Case:** Amal on a ward; a deterioration score fires at 3 a.m.
**LOs:** explain early-warning and prediction models and their alarm burden; interpret a prediction model's lead time vs false alerts; describe closed-loop insulin delivery; describe AI-ECG; evaluate a public-health AI claim (Google Flu lesson).
**Sections:** early warning & sepsis (TREWS, Epic external validation); AKI prediction (Tomašev with 93.6% male cohort and ~2 false:1 true — ledger); alarm fatigue (link Ch11); AI-ECG (Attia 2019; EAGLE RCT); closed-loop insulin (`../images/image18.png`; Brown 2019 — type 1 diabetes; clarify Amal is T2 so not her tool); hemodynamic monitoring (reuse §5.5/5.6 condensed; image14 per triage); population health: surveillance (HealthMap), Google Flu Trends failure (Ginsberg 2009 → Lazer 2014) as Myth vs Evidence.
**Key refs:** Adams 2022 Nat Med; Wong 2021; Tomašev 2019 Nature; Attia 2019 Lancet; Yao 2021 Nat Med; Brown 2019 NEJM; Brownstein 2008 J Am Med Inform Assoc; Ginsberg 2009 Nature; Lazer 2014 Science.

### Task 14: Chapter 10 — Bias, Fairness & Privacy (2,200)

**File:** `rework/ch10-bias-fairness-privacy.md` · **Personas:** anthropologist, statistician · **Case:** Lina's dermatology app; Karim's wearable data sold to an insurer.
**LOs:** identify sources of bias across the data pipeline; analyse the Obermeyer case correctly (label choice, not race variable); distinguish anonymisation, pseudonymisation and de-identification; explain re-identification risk; compare HIPAA and GDPR at principle level.
**Sections:** sources of bias (reuse §7.4.1); Obermeyer case (reuse §7.4.2) + corrected mitigation (§7.4.3: fix the label; "blindness" does not work — Gichoya 2022 shows race is detectable from images); underdiagnosis (Seyyed-Kalantari 2021); skin tone (Adamson & Smith 2018; Daneshjou 2022); privacy: de-identification (fig `../images/image22.png`), re-identification (Sweeney; Rocher 2019), differential privacy as bounded ε guarantee, federated learning; law: HIPAA Safe Harbor, GDPR (right-to-explanation contested — Wachter 2017), Local Context box: Egypt Personal Data Protection Law No. 151/2020 (verify number/year before writing).
**Key refs:** Obermeyer 2019; Gichoya 2022 Lancet Digit Health; Seyyed-Kalantari 2021 Nat Med; Adamson & Smith 2018 JAMA Dermatol; Rocher 2019 Nat Commun; Dwork 2006; Rieke 2020 npj Digit Med; Wachter 2017 Int Data Priv Law; GDPR Reg. 2016/679.

### Task 15: Chapter 11 — Regulation, Liability & the Human in the Loop (2,400)

**File:** `rework/ch11-regulation-liability-human.md` · **Personas:** psychologist (human factors), research-synthesist · **Case:** Amal is harmed after an ignored alert — who is responsible?
**LOs:** explain SaMD and risk-based classification; distinguish FDA 510(k), De Novo, PMA and PCCP; describe EU AI Act high-risk obligations and interplay with MDR/IVDR; apply the elements of negligence to an AI-assisted case; explain automation bias and de-skilling and design countermeasures.
**Sections:** SaMD & IMDRF risk categories; FDA pathways + PCCP final guidance (Dec 2024) (fig `../images/image24.png`); EU AI Act (Reg. 2024/1689 — medical devices high-risk, obligation timeline) + MDR/IVDR; WHO guidance; Local Context box: Egyptian Drug Authority (verify legal basis); liability (reuse §7.1.1 elements; tripartite model fig `../images/image21.png`; learned-intermediary corrected; Price/Gerke/Cohen 2019); human factors: automation bias (Goddard 2012), de-skilling evidence (Budzyń 2025 — verify), XAI limits (`../images/image23.png`; Adebayo 2018; Ghassemi 2021); future horizons & changing roles for all four professions (reuse §7.6.3 empathy).
**Key refs:** IMDRF 2014 N12; FDA 2021 GMLP; FDA 2024 PCCP final guidance; Reg. (EU) 2024/1689; Reg. (EU) 2017/745; Reg. (EU) 2017/746; WHO 2021 Ethics & governance of AI for health; Price, Gerke & Cohen 2019 JAMA; Goddard 2012 J Am Med Inform Assoc; Adebayo 2018 NeurIPS; Ghassemi 2021 Lancet Digit Health; Muehlematter 2021 Lancet Digit Health.

---

### Task 16: New figures + cover

**Files:** `rework/figures/split-leakage.svg`, `confusion-ppv.svg`, `next-token.svg`, `pose-skeleton.svg`, `pharmacovigilance.svg`, `patient-journeys.svg`, `cover.svg`

- [ ] **Step 1:** Hand-write each as simple inline SVG (text labels, no generated imagery → no hallucinated text). Each labelled "Illustrative" where schematic.
- [ ] **Step 2:** Render check: open each in Chrome headless screenshot (`--screenshot`) to `D:/yasser/_preview_<name>.png`, view with Read tool, fix legibility.
- [ ] **Step 3:** Confirm each is referenced from its chapter ("see Figure n.m"); `grep -c "figures/" rework/ch*.md`.
- [ ] **Step 4:** Commit: `feat(rework): new figures and cover`

### Task 17: Assembly

**Files:** Create `rework/tools/assemble.py`; output `AI_in_Health_Care_Interprofessional.md`

- [ ] **Step 1:** Implement: concatenate front matter, ch01–ch11, glossary, then "Consolidated References" grouped by chapter (per-chapter numbering kept); rewrite `../images/` → `images/` and `figures/` → `rework/figures/`; generate TOC from H1s.
- [ ] **Step 2:** Run `python rework/tools/check_book.py --all` → PASS (totals, ledger closed).
- [ ] **Step 3:** Check every image path in the output exists: `grep -o "(images/[^)]*\|(rework/figures/[^)]*" AI_in_Health_Care_Interprofessional.md | tr -d '(' | xargs -I{} test -f {} || echo missing`.
- [ ] **Step 4:** Commit: `feat(rework): assembled interprofessional edition`

### Task 18: Final audits + review report

**File:** `rework/REVIEW_REPORT.md`

- [ ] **Step 1:** Statistician persona: audit every number in the assembled book (grep `[0-9]+(\.[0-9]+)?%` and all metric words); each has citation and correct arithmetic.
- [ ] **Step 2:** Research-synthesist persona: run `verify_refs.py` on every chapter; report counts (total refs, median year, share 2023–2026, RCTs cited) against spec §8 targets.
- [ ] **Step 3:** Psychologist + master-instructional-design audit A–I on the whole book; lens balance per chapter.
- [ ] **Step 4:** Re-score with `EVALUATION_RUBRIC.md` (six pillars, weights); target ≥ 75. Any pillar < 7 → list fixes and apply before closing.
- [ ] **Step 5:** Write `REVIEW_REPORT.md`: scorecard, before/after table (46 → new), remaining open items (region, authorship).
- [ ] **Step 6:** Commit: `docs(rework): final audit and review report`
