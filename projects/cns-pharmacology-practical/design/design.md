# Design — Practical Pharmacology of the Central Nervous System

Book: `cns-pharmacology-practical`. Inputs: approved intake (DEC-001), evaluation (36.5/100; 82 findings, 1 blocker, 38 major).

## 1. What the new edition is

A practical companion for the Pharmacology 2 CNS sections (Level 3, Clinical Pharmacy Program, Faculty of Pharmacy, Port Said University). One chapter per section topic, in the section-schedule order. Each chapter turns a slide deck into short, connected explanations, comparison tables, one mechanism diagram, safety boxes, Egyptian brand names, and a full self-assessment. The scientific scope stays that of the slides; errors are corrected and the gaps in the evaluation are filled.

Readers: students who finished Pharmacology 1. Each chapter opens with a very short Quick Recap of the prerequisites (receptor or transmitter physiology) and nothing more.

## 2. Chapters (chapter-plan.json)

| # | ID | Title | Words | Source deck |
|---|---|---|---|---|
| 1 | ch01 | Alzheimer's Disease | 3800 | Alzheimer's disease (19 slides) |
| 2 | ch02 | Psychosis and Antipsychotic Drugs | 5000 | Psychosis (33) |
| 3 | ch03 | Parkinson's Disease | 4600 | Parkinson's disease (21) |
| 4 | ch04 | Depression and Antidepressant Drugs | 5200 | Depression (35) |
| 5 | ch05 | Epilepsy and Antiseizure Drugs | 5000 | Epilepsy (27) |
| 6 | ch06 | Skeletal Muscle Relaxants | 4700 | SMR (41) |
| 7 | ch07 | Anxiolytics, Sedatives and Hypnotics | 5400 | Anxiolytic and hypnotic drugs (58) |
| 8 | ch08 | General Anaesthetics | 4600 | General anaesthetics (22) |
| 9 | ch09 | Local Anaesthetics | 3700 | Local anaesthetics (13) |

Total 42,000 words (template range 36,000-50,000, ±20% per chapter), about 130-150 A4 pages with tables and figures. No parts. Nothing dropped: every source topic is kept; duplicated MCQs (F-040, F-064) are removed.

## 3. Chapter pattern

Every chapter uses the same order (template.json):

1. `# Chapter N: Title`
2. `## Learning Objectives` — 4-6 objectives `[LO1]…`, action verbs (not "understand/know").
3. `> **Quick Recap:**` — 60-120 words of Pharmacology 1 / physiology the chapter needs.
4. Core sections `## N.1 …` — disease in brief (pathophysiology that explains the drug targets), then one section per drug class: members (prototype first), mechanism, clinical uses, adverse effects, interactions and contraindications.
5. One mechanism figure (`fig:<id>`, hand SVG, original).
6. Comparison tables (class vs class, drug vs drug) — at least two per chapter.
7. `## N.x Choosing a Drug` — guideline-based selection table (NICE, ILAE, APA, AAGBI/ASRA as relevant) and patient factors.
8. `## N.x Brands in Egypt` — table: generic name, brand examples (from the source slides, transcribed; photos are not reproduced), dosage form. A note tells the reader that availability changes and the EDA list is the reference.
9. `## N.x For Discussion` — 2-3 section-discussion questions (kept from the source where they exist; written for the other chapters).
10. Boxes, each at least once per chapter: `> **Clinical Pearl:**`, `> **Caution:**` (safety, toxicity, interactions), `> **Exam Tip:**`.
11. `## Key Takeaways` — 5-7 bullets.
12. `## Self-Assessment` — 10 single-best-answer MCQs, options A-D, each tagged `[LOn]`; key balance 2-3 per letter, no letter three times in a row; then `**Clinical Case.**` with 2-3 short cases.
13. `## Answers and Rationales` — `**Qn. X** — why X is right; why the others are wrong.` and `**Clinical Case — model answer.**`.
14. `## References` — Vancouver, numbered, cited as [1]; core textbooks (Katzung 16th ed., Lippincott 8th ed., Rang & Dale 10th ed.) plus current guidelines; at least half from 2021 or later.

Style: en-GB, INN names, short sentences (mean ≤16 words), active voice, no slide fragments, no teacher-timing notes. Doses only where they matter for safety (toxic doses, maximum local-anaesthetic doses, titration).

## 4. Front matter (`chapters/00-front-matter.md`)

Title, co-authors in the approved order, `## How to Use This Book` (chapter pattern, the three boxes, how to use the self-assessment in the section), a short note on brands and on the educational (non-prescribing) purpose. The cover and title page come from theme.json (logos, institution line, eyebrow).

## 5. Figures (`figures/figures.json`, kind `diagram.svg`, licence original)

| ID | Chapter | Shows |
|---|---|---|
| ache-synapse | ch01 | Cholinergic synapse: AChE inhibitors and memantine at the NMDA receptor |
| dopamine-pathways | ch02 | Four dopamine pathways and the effect of D2 block in each |
| levodopa-path | ch03 | Levodopa from gut to brain: AADC, COMT, MAO-B and where carbidopa, entacapone and selegiline act |
| monoamine-synapse | ch04 | Serotonin/noradrenaline synapse: SERT/NET, MAO, alpha2 autoreceptor, with SSRI, SNRI, TCA, MAOI, mirtazapine |
| antiseizure-targets | ch05 | Excitatory and inhibitory synapse with Na+, T-type Ca2+, alpha2delta, SV2A, GABA targets |
| relaxant-sites | ch06 | Brain-spinal cord-neuromuscular junction-muscle: where each relaxant acts |
| gabaa-receptor | ch07 | GABA-A receptor with GABA, benzodiazepine, barbiturate and Z-drug sites; flumazenil |
| balanced-anaesthesia | ch08 | The five goals of anaesthesia and which drug class provides each |
| la-mechanism | ch09 | Unionised base crossing the membrane, ionised form blocking the Na+ channel from inside |

## 6. Errors and gaps (evaluation findings)

All 82 findings are handled in their chapter. Every G1 error is also an erratum in `chapters/errata-ledger.md` (see errata-seed.md) and must end `fixed` or `removed-with-content`. The blocker and major findings map as follows.

| Finding | Chapter | Reason |
|---|---|---|
| F-001 | ch01 | G1 major: Early-onset (<65 y, ~5% of cases; familial autosomal-dominant APP/PSEN1/PSEN2 <1%); late-onset (>=65 y, sporadic, APOE e4 risk). |
| F-004 | ch01 | D3 major: Add: review pulse before and during treatment; caution in conduction disease and with beta-blockers or digoxin; start low and titrate; rivastigmine with food; patch reduces GI effects. |
| F-005 | ch02 | G1 major: Positive symptoms: mesolimbic hyperactivity. Negative and cognitive symptoms: mesocortical hypoactivity. |
| F-006 | ch02 | G1 major: Rewrite: negative symptoms reflect reduced dopamine in the mesocortical pathway; 5-HT2A antagonism by SGAs releases dopamine there. |
| F-007 | ch02 | G1 major: Table of EPS by time of onset: acute dystonia (hours-days; IM anticholinergic), parkinsonism (weeks), akathisia (days-weeks; propranolol), tardive dyskinesia (months-years; often irreversible; valbenazine). |
| F-008 | ch02 | D3 major: NMS: fever, lead-pipe rigidity, altered mental state, autonomic instability (labile or raised BP, tachycardia, sweating), raised CK. Management: stop the antipsychotic, cool, fluids, supportive care; dantrolene or bromocriptine in severe cases. |
| F-009 | ch02 | G1 major: Replace '–ve' with '+ve' for FGAs. |
| F-010 | ch02 | G1 major: Weight gain and metabolic syndrome: H1 and 5-HT2C block (highest with clozapine and olanzapine); monitor weight, glucose and lipids. |
| F-011 | ch02 | D3 major: Agranulocytosis ~1%; baseline ANC, weekly for 18 weeks, then every 2 weeks to 1 year, then monthly; also myocarditis, seizures, constipation. |
| F-014 | ch03 | D1 major: Add non-ergot agonists as the main agonist class; keep bromocriptine as a historical ergot example. |
| F-017 | ch03 | G1 major: Pyridoxine enhances peripheral decarboxylation of levodopa given alone; with carbidopa/levodopa it is not clinically relevant. |
| F-021 | ch04 | D2 major: Stratify by severity and shared decision: less severe - guided self-help or psychological therapy first, antidepressant only if preferred; more severe - CBT plus antidepressant, an antidepressant, or psychological therapy according to need and preference (NICE NG222 1.5-1.6). |
| F-023 | ch04 | G1 major: Attribute each effect to its receptor: alpha1 (hypotension), H1 (sedation, weight gain), M (anticholinergic), 5-HT (GI, sexual). |
| F-030 | ch04 | G1 major: Mirtazapine: alpha2 antagonist raising NA and 5-HT release; 5-HT2/5-HT3 and H1 block (sedation, weight gain). Trazodone: 5-HT2A antagonist, weak SERT inhibitor, alpha1 and H1 block (priapism, sedation). |
| F-031 | ch04 | D3 major: Add a Caution box: monitor for suicidal thoughts in patients under 25 during the first weeks and after dose changes. |
| F-033 | ch05 | G1 major: Classify by mechanism (Na+ channel, T-type Ca2+, GABA, SV2A, alpha2delta, glutamate) in one table. |
| F-034 | ch05 | G1 major: Group inducers (phenytoin, carbamazepine, phenobarbital) versus inhibitor (valproate); teratogenicity highest with valproate. |
| F-035 | ch05 | D3 major: Add the boxed warnings and interactions (oral contraceptives, warfarin). |
| F-036 | ch05 | D2 major: Add a seizure-type table (focal: lamotrigine/levetiracetam; generalised tonic-clonic: valproate in males, lamotrigine/levetiracetam in women of child-bearing potential; absence: ethosuximide) and a status epilepticus box (benzodiazepine then second-line agent). |
| F-042 | ch06 | G1 major: GABA-B agonist: increases K+ conductance (hyperpolarisation) and reduces Ca2+ entry, lowering excitatory transmitter release in the spinal cord. |
| F-044 | ch06 | G1 major: Persistent depolarisation (phase I) followed by desensitisation (phase II). |
| F-045 | ch06 | D3 major: Add hyperkalaemia with contraindications, bradycardia (atropine), myalgia, raised IOP and ICP. |
| F-048 | ch07 | G1 major: Short: midazolam, triazolam. Intermediate: alprazolam, lorazepam, oxazepam, temazepam. Long: diazepam, chlordiazepoxide, clonazepam, flurazepam. |
| F-050 | ch07 | G1 blocker: Replace with: wide margin when taken alone, but combined with alcohol, opioids or other CNS depressants they can cause fatal respiratory depression; elderly: falls and confusion. |
| F-052 | ch07 | G1 major: 5-HT1A partial agonist (some D2 affinity); onset 1-2 weeks or more. |
| F-056 | ch08 | D1 major: Add MAC (potency) and blood:gas solubility (speed) with a comparison table for N2O, sevoflurane, desflurane, isoflurane. |
| F-060 | ch08 | G3 major: Correct key: C. |
| F-062 | ch09 | D3 major: Add LAST: CNS excitation then depression, arrhythmia/arrest (bupivacaine), max doses with/without adrenaline, 20% lipid emulsion. |
| F-065 | ch01 | Book-wide (G2 major); fixed in every chapter ch01-ch09 by the chapter pattern (§3); mapped to ch01, the first chapter written. |
| F-069 | ch01 | Book-wide (G3 major); fixed in every chapter ch01-ch09 by the chapter pattern (§3); mapped to ch01, the first chapter written. |
| F-070 | ch01 | Book-wide (G4 major); fixed in every chapter ch01-ch09 by the chapter pattern (§3); mapped to ch01, the first chapter written. |
| F-071 | ch01 | Book-wide (D2 major); fixed in every chapter ch01-ch09 by the chapter pattern (§3); mapped to ch01, the first chapter written. |
| F-072 | ch01 | G1 major: Say 'may give modest temporary benefit in cognition or function'; contrast with anti-amyloid antibodies for eligible early disease. |
| F-073 | ch04 | G1 major: Separate early transient effects (nausea) from persistent ones (sexual dysfunction) and give management options. |
| F-075 | ch05 | G1 major: Describe awareness per seizure type (absence, tonic-clonic, myoclonic). |
| F-077 | ch07 | D2 major: Remove OCD; separate rescue/status use (route-dependent choices) from maintenance use. |
| F-078 | ch07 | D3 major: Add duration limits, dependence counselling, driving caution and the boxed warning. |
| F-079 | ch08 | D2 major: Teach patient-specific selection; rewrite the MCQ around a haemodynamically unstable child needing painful procedural sedation. |
| F-080 | ch02 | D3 major: Identify the EPS type and timing, then give subtype-specific management. |

Minor findings follow the same line-to-chapter mapping and are fixed in the chapter text; they are listed in `evaluation/findings.json`.

## 7. Decisions for the user

1. **Brand tables instead of package photos.** The 19 brand slides are photographs of packs. The book lists the names in a table (no photos: trademark packaging, low print quality). Four names could not be read with certainty (Achtenon, Dimra, Migrainil, Sleep-aid) and are marked for your check.
2. **Anti-amyloid antibodies, sugammadex, non-ergot dopamine agonists, MAC and LAST** are added as short sections: they are needed to correct the findings and are standard in the core textbooks.
3. **Doses** appear only where safety depends on them.
