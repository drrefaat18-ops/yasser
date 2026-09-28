# Design — Biopharmaceutics and Pharmacokinetics (PT-312), second edition

Inputs: `brief.json`, `rubric.json`, `template.json`, `theme.json` (DEC-001); `evaluation/report.md`,
`evaluation/findings.json`, `evaluation/scorecard.json` (44.0 / 100), `evaluation/codex-review.md`,
`evaluation/fixes.md`.

## 1. What this edition is

The same 14 subjects, in the same order, taught properly. The brief says simplify and organise, with no new topics,
and the evaluation agrees that the syllabus is right and the arithmetic is right. The book is rebuilt, not rewritten:
every worked example, every dataset and every topic in the source survives into this edition.

Three things change. The notes become a book: numbered chapters, objectives, worked answers, figures with captions,
questions with rationales. The mathematics becomes text: numbered equations, real subscripts, one symbol table. And
nineteen wrong or unsupported statements are corrected against cited sources — which is more content work than
"simplify and organise" suggests, and §5 says how it is bounded.

## 2. Structure

Fourteen chapters in the printed order of the source contents page, grouped into three parts. Parts group consecutive
chapters only; nothing is moved, merged or split, as the user required at intake (`size.restructuring =
keep_chapters`).

| Part | Chapters | Why the boundary falls here |
|---|---|---|
| I — One-Compartment Kinetics | ch01–ch03 | Everything a student can do with one compartment and a single IV dose, by plasma and by urine. |
| II — Extended Models, Clearance and Dosing | ch04–ch11 | Each chapter relaxes one assumption of Part I: a second compartment, continuous input, elimination as clearance, absorption, repeated doses, no model at all, saturable enzymes, a second chemical entity. |
| III — Biopharmaceutics, Bioequivalence and Dissolution | ch12–ch14 | The product rather than the patient: what the dosage form does before the kinetics start. |

Chapter 13 keeps the BCS and the biowaiver criteria, where the source puts them (pages 98–100), rather than opening
chapter 14 with them. Chapter 14 starts where dissolution starts, at page 101.

### Chapter shape

Every chapter, without exception:

1. **Learning objectives** — 3 to 5, boxed, `LO1`…`LOn`, verbs the questions can test (calculate, derive,
   distinguish, select). Never "understand".
2. **Concept** — prose, ≤16 words per sentence on average, building from what the previous chapter established.
3. **Key Equation** callouts — every equation the chapter uses, numbered, with its symbols and its assumptions.
4. **Worked Example** callouts — every example from the source, worked through in print.
5. **Watch the Units / Common Mistake / Why It Matters in Practice** — as the material needs them, not to a quota.
6. **Key Takeaways** — 5 to 8 lines.
7. **Check Your Understanding** — 10 four-option MCQs plus calculation exercises, each tagged to an objective.
8. **Answers and Worked Solutions** — every MCQ with a rationale, every exercise with its steps.

References are a single consolidated list at the end of the book, with numbered `[n]` citations in the text
(user's choice at intake). Each chapter also carries its own short `## References` list, because the harness
checker (`check_book.check_citations`) resolves every `[n]` against the reference entries in the same file and
fails a chapter that cites without one. The chapter lists are the working numbering; the consolidated list at
the back of the book is the one the reader is pointed to, and it is the union of the chapter lists.

## 3. Chapters and budgets

Budgets total 47,400 words against a template range of 38,000–52,000.

| ID | Title | Words | Source pages | Notes |
|---|---|---|---|---|
| ch01 | Introduction to Biopharmaceutics and Pharmacokinetics | 2700 | 4–6 | Definitions, the plasma curve, MEC/MTC/therapeutic range, compartment models. Sets the pattern every other chapter follows. |
| ch02 | One Compartment, IV Bolus: Plasma Data | 3400 | 7–11 | First-order elimination, t½, Vd, Cl; Examples 1–6. |
| ch03 | One Compartment, IV Bolus: Urine Data | 2800 | 12–15 | Excretion-rate and sigma-minus methods, validity of urine data; Examples 7–8. |
| ch04 | Two Compartment, IV Bolus: Plasma Data | 3200 | 16–20 | Biexponential model, method of residuals, hybrid constants; Examples 9–10. |
| ch05 | Intravenous Infusion | 3000 | 20–24 | Css, time to steady state, loading dose; Examples 11–14. |
| ch06 | Clearance | 3400 | 24–30 | Renal mechanisms, clearance ratio, total/renal/hepatic clearance; Examples 15–18. |
| ch07 | Oral Absorption | 4200 | 30–38 | First-order absorption, tmax, feathering, Wagner–Nelson, lag time, flip-flop; Examples 22–23. |
| ch08 | Multiple Dose Regimens | 3400 | 39–42 | Accumulation, Cpmax/min/ave at steady state; Examples 19–21. |
| ch09 | Non-Compartmental Analysis | 2800 | 43–46 | Statistical moments, MRT, MAT, AUMC, Vdss; the source's one fully worked example. |
| ch10 | Non-Linear Pharmacokinetics | 2400 | 47–48 | Michaelis–Menten, the two limits, phenytoin. |
| ch11 | Pharmacokinetics of Metabolites | 2700 | 49–53 | Phase I/II, metabolite equations, formation- vs elimination-rate limited. |
| ch12 | Biopharmaceutical Considerations | 5000 | 54–78 | GI physiology, transport mechanisms, pH-partition, solubility, particle size, polymorphism, dosage form, excipients, manufacture. |
| ch13 | Bioavailability and Bioequivalence | 5000 | 79–100 | Definitions, absolute/relative BA, assessment methods, BE study design and statistics, BCS, biowaivers. |
| ch14 | Dissolution | 3400 | 101–109 | Noyes–Whitney, apparatus 1–7, Q and the S₁/S₂/S₃ stages, IVIVC. |

`source_refs` is empty in `chapter-plan.json` for every chapter. Ingest produced no addressable units
(`ingest/units.json` is empty) because the source PDF carries no extractable heading structure — which is finding
F-022 itself. The source pages above are the reference instead, and they come from the source contents page checked
against the page footers in the PDF text layer.

## 4. Figures

The source embeds 354 images across 61 of its 109 pages, none numbered, captioned or cross-referenced (F-023). None
is reused. Every figure is redrawn as an SVG source under `rework/figures`, numbered `Figure {chapter}.{n}`, with
axis labels, units, a caption saying what the reader should take from it, and a reference from the paragraph that
needs it. The palette is the theme's (`primary` `#104C4A`, `accent` `#B26B00`), so the figures and the page read as
one design.

The recurring set, all of which the source draws unlabelled: plasma concentration–time curve with MEC, MTC and the
therapeutic range; semilog decay with slope −K/2.303; one-, two- and three-compartment schematics; urinary excretion
rate and sigma-minus plots; the feathering construction; infusion approach to Css and post-infusion decay; the oral
absorption curve on linear and semilog axes; effect of dose, Ka and K on Cpmax, tmax and AUC; multiple-dose
accumulation to steady state; AUC and AUMC; the Michaelis–Menten curve; the pH-partition and carrier-transport
diagrams; the dissolution apparatus; the three-formulation comparison.

## 5. Scope boundary

The brief forbids new topics, and nothing here adds one. Two things are nevertheless additions, and both were
authorised at intake:

- **Assessment.** 10 MCQs and calculation exercises per chapter with answers and rationales (`assessment.mcq`,
  `assessment.exercises` in the brief).
- **Apparatus.** Objectives, takeaways, a glossary and a symbol table.

**Corrections are not additions.** Nineteen G1 and D1 findings are wrong or unsupported statements. Correcting them
changes what the book says, and there is no version of "simplify and organise" that leaves a student being taught
that BCS Class 2 needs no bioequivalence study (F-001) or that lactase digests peptides (F-006). Each correction is
made to the minimum extent that makes the statement true, is cited, and is logged in the errata ledger with the
original wording. Where a correction requires material the source does not have — the 80.00–125.00% bioequivalence
criterion (F-004), the ICH M9 and M13A framing (F-032) — that material is added, because its absence is the finding.

Explicitly out of scope: topics not in the source syllabus, clinical dosing recommendations, and any change to the
14 subjects or their order.

## 6. Finding map

Every blocker and major finding from `evaluation/findings.json`, and the minors, mapped to the chapter that fixes it.
Book-wide findings are mapped to ch01, which establishes the pattern the other thirteen follow; the Reason says so.

| Finding | Chapter | Reason |
|---|---|---|
| F-001 | ch13 | BCS table rebuilt on ICH M9: biowaivers for Class 1 and 3, in-vivo study for Class 2, plus the EDA Class 2 weak-acid pathway as a separate, conditioned statement. |
| F-002 | ch13 | High permeability threshold corrected to ≥85% and cited to ICH M9. |
| F-003 | ch13 | High solubility corrected to pH 1.2–6.8, highest single therapeutic dose, cited to ICH M9. |
| F-004 | ch13 | The 90% CI of 80.00–125.00% on log-transformed AUC and Cmax added as the chapter's central statement, cited to ICH M13A, with the narrowed NTI interval. |
| F-005 | ch13 | Two one-sided tests explained; the 95%-confidence-in-a-difference passage replaced. |
| F-006 | ch12 | Peptide digestion corrected to brush-border and cytosolic peptidases; the lactose-intolerance aside moved to carbohydrate digestion. |
| F-007 | ch12 | Ion-pair example corrected; tetracycline kept as an amphoteric case on its own merits. |
| F-008 | ch11 | Race replaced by NAT2 acetylator genotype and the CYP polymorphisms, cited. |
| F-009 | ch12 | Vitamin B₁₂ claim removed; B₁₂ moved out of the facilitated-diffusion column to receptor-mediated endocytosis. |
| F-010 | ch14 | Apparatus 4 flow rate stated once, as USP 4/8/16 mL·min⁻¹. |
| F-011 | ch01 | Therapeutic range and therapeutic index separated in the text and in redrawn Figure 1.1; the corrected usage then holds everywhere the figure is reused. |
| F-013 | ch14 | Noyes–Whitney set as numbered text before its symbol list, with the sink-condition simplification. |
| F-014 | ch07 | Wagner–Nelson table corrected to µg·mL⁻¹ and units carried through every derived column. |
| F-017 | ch01 | Equation policy set here — numbered, real subscripts, one symbol table in the front matter — and applied in all 14 chapters. |
| F-018 | ch01 | Worked-answer policy set here and applied to all 23 examples across the book; ch01 carries the first worked examples. |
| F-020 | ch04 | Method of residuals demonstrated end to end on Example 10's data, with the residual table visible; ch07 then reuses the same layout for Ka. |
| F-021 | ch01 | Objectives introduced here as the chapter-opening block; all 14 chapters carry 3–5. |
| F-022 | ch01 | Numbered chapters, headings and summaries established here for all 14. |
| F-023 | ch01 | Figure policy set here — number, caption, axis labels, cross-reference — and applied to every redrawn figure. |
| F-024 | ch01 | Generated table of contents over real headings, built in the front matter alongside ch01. |
| F-026 | ch12 | All four Arabic lecture glosses removed (ch12 line 2894, ch13 lines 4014 and 4675, ch14 line 4971); useful terms moved to the bilingual glossary. |
| F-028 | ch01 | Symbol table in the front matter and glossary at the back, built with ch01; the duplicate Km renamed to Kh for hepatic elimination. |
| F-029 | ch01 | Assessment pattern set here — 10 MCQs plus exercises, answers and rationales, each tagged to an objective — and applied to all 14 chapters. |
| F-030 | ch01 | Citation policy set here: numbered `[n]` markers in the text, one consolidated list at the back. |
| F-031 | ch13 | DeHann 1972, Regamey 1973, Oser 1945, the 1961 FDA statement, the Australian phenytoin outbreak and Amidon 1995 traced and cited; the Amidon date corrected. Examples 20–21 in ch08 carry the first two citations. |
| F-032 | ch13 | Chapter rebuilt on ICH M9 and ICH M13A with the EDA guideline as the national layer; historical FDA material kept only where still operative. |
| F-037 | ch13 | F separated into fa × Fg × Fh; propranolol, already in the text, used as the worked case. |
| F-038 | ch13 | Release mechanism moved into the "same" column of the pharmaceutical-equivalents definition; the alternatives definition checked for the same confusion. |
| F-039 | ch13 | The invented 5% comparator rule removed and replaced by the ICH M13A comparator-selection and batch-potency requirements. |
| F-040 | ch11 | The four active metabolites moved to the active list; NAPQI kept and genuine reactive metabolites added. |
| F-012 | ch13 | Volunteer eligibility restated as ICH M13A age and BMI criteria, with the old weight band labelled historical. |
| F-016 | ch06 | Example 16 given the stated assumption it needs so fu is determined. |
| F-019 | ch01 | Per-chapter example numbering (Example 7.1, 7.2, …) established here; renumbering removes the out-of-order sequence. |
| F-025 | ch06 | The duplicated clearance treatment kept in full here; ch02 keeps a one-line forward reference. |
| F-027 | ch09 | The exclamation-mark passage replaced by a statement of why the compartment count varies. |
| F-033 | ch02 | Vd variation broadened to age, body composition, pregnancy and protein binding. |
| F-034 | ch13 | Washout stated as the ICH M13A minimum of five terminal half-lives, with ten kept as the conservative practical choice, cited. |
| F-035 | ch08 | Accumulation half-life derived, with the log(1) = 0 collapse shown and the Ka > K assumption stated. |
| F-041 | ch12 | Dosage-form ranking introduced as a general tendency with its mechanism and one counter-example. |

## 7. Build

A4, Word plus a designed PDF through the HTML engine (`theme.build.pdf.engine = html`), stock Windows fonts, the
`ltr-textbook` preset. The title page carries the departmental credit line exactly as the source prints it, the
PT-312 eyebrow and the teaching-not-prescribing notice. No ISBN, no publisher, no invented registration.

## 8. Order of work

ch01 first and alone, for the user to review: it carries the pattern every other chapter inherits — objectives,
equation setting, worked examples, figures, questions, citations. Nothing else is written until that pattern is
approved. Then ch02–ch14, then front matter, glossary and the consolidated reference list, then build.
