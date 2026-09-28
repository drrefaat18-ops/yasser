# Evaluation report — cns-pharmacology-practical

Source: `ingest/source.md` (markitdown text of `original/cns-sections-combined.pdf`, nine Pharmacology 2 section slide decks, 269 slides).
Review kind: self (Claude, inline persona passes: subject-reviewer, pharmacology-reviewer, instructional-designer, psychologist, research-synthesist). Codex review: `codex-review.md` (GPT-5, 15 findings, all accepted; see `fixes.md`). Scores use the rubric anchor bands: G1 in the 1-3 band (frequent and dangerous errors); G2, G3 and D3 in the 4-6 band (usable structure with serious gaps).

## Score

Total **36.5 / 100**. G1 is capped at 4 by the open safety blocker F-050 (benzodiazepines called "very safe").

| Pillar | Name | Weight | Score | Findings |
|---|---|---|---|---|
| G1 | Content accuracy | 20 | 3 | 44 |
| G2 | Pedagogical design and clarity | 20 | 4 | 5 |
| G3 | Assessment quality | 10 | 4 | 4 |
| G4 | Sources and currency | 10 | 1 | 1 |
| D1 | Mechanism and drug-class coverage | 15 | 5 | 7 |
| D2 | Clinical therapeutics | 15 | 4 | 6 |
| D3 | Drug safety | 10 | 4 | 15 |

Findings: 82 (1 blocker, 38 major, 43 minor).

## What the source does well

- Covers every CNS drug class of the Pharmacology 2 section schedule with a clear per-class pattern (members, MOA, uses, adverse effects).
- Uses real Egyptian brands for every class (19 brand slides) and clinical cases with pharmacist questions.
- The psychosis and depression decks already carry good discussion prompts (partial agonism, clozapine monitoring, counselling).

## Main problems

1. **Accuracy and safety (G1, D3).** Several mechanisms are wrong (buspirone, mirtazapine, baclofen, gabapentinoids, depolarising block), key classifications are wrong (benzodiazepine half-lives, EPS reversibility, anti-epileptic "generations"), and safety content is missing or dangerous (benzodiazepine safety claim, NMS, clozapine monitoring, LAST, succinylcholine hyperkalaemia, antidepressant suicidality warning).
2. **Form (G2).** Slide fragments, no objectives, recap, takeaways or connected explanation; teacher prompts mixed with student text; many spelling errors.
3. **Assessment (G3).** 0-4 MCQs per chapter, five options, one wrong key and two duplicates.
4. **Sources (G4).** No references.
5. **Therapeutics (D2).** Little guideline-based drug choice (seizure type, depression severity, Parkinson's initial therapy).

## Blocker and major findings

| ID | Pillar | Severity | Lines | Claim |
|---|---|---|---|---|
| F-001 | G1 | major | 34-45 | Early-onset Alzheimer's disease is defined as onset below 65 years, not below 40; the 1% figure applies to autosomal-dominant familial disease. |
| F-004 | D3 | major | 106-125 | Cholinesterase-inhibitor safety lists bradycardia but omits syncope and heart-block risk, pulse review, caution in conduction disease or with other bradycardic drugs, and titration advice. |
| F-005 | G1 | major | 264-268 | Positive symptoms are linked to mesolimbic dopamine excess; the mesocortical pathway is hypoactive in schizophrenia. |
| F-006 | G1 | major | 275-279 | Negative symptoms are attributed to serotonin; the accepted model links them to mesocortical dopamine hypofunction (5-HT2A block helps indirectly). |
| F-007 | G1 | major | 324-335 | Extrapyramidal effects are misclassified: acute dystonia is reversible; tardive dyskinesia (late, potentially irreversible) and drug-induced parkinsonism are missing. |
| F-008 | D3 | major | 336-342 | The neuroleptic malignant syndrome description omits altered mental status, autonomic lability, raised creatine kinase/rhabdomyolysis and urgent management; convulsions are not a defining feature. |
| F-009 | G1 | major | 383-390 | The text says FGAs treat only negative symptoms; FGAs mainly treat positive symptoms. |
| F-010 | G1 | major | 420-425 | Metabolic effects of SGAs are attributed to 5-HT2A block; they are mainly due to H1 and 5-HT2C antagonism. |
| F-011 | D3 | major | 428-428 | Clozapine agranulocytosis is called 'leukopenia, often fatal and common' with no monitoring protocol. |
| F-014 | D1 | major | 694-704 | Non-ergot dopamine agonists (pramipexole, ropinirole, rotigotine) are not taught, although they are standard therapy and appear in the chapter's own MCQs; only bromocriptine is covered. |
| F-017 | G1 | major | 777-779 | Pyridoxine is said to be contraindicated with levodopa; the interaction applies to levodopa alone and is abolished by carbidopa, which almost all patients take. |
| F-021 | D2 | major | 1022-1033 | Psychotherapy is presented as first line for all depression; guidelines reserve psychotherapy alone for less severe depression and combine it with an antidepressant for moderate-severe depression. |
| F-023 | G1 | major | 1061-1082 | Orthostatic hypotension and sedation are listed as effects of all antidepressants due to raised amines; they are due to alpha1 and H1 block (TCAs, trazodone, mirtazapine) and are rare with SSRIs. |
| F-030 | G1 | major | 1206-1216 | The mechanisms of mirtazapine and trazodone are wrong or incomplete: mirtazapine is mainly an alpha2 antagonist (also 5-HT2, 5-HT3 and H1 block); trazodone is a 5-HT2A antagonist and weak SERT inhibitor. |
| F-031 | D3 | major | 1158-1198 | The chapter never mentions the boxed warning for suicidality in children and young adults starting antidepressants. |
| F-033 | G1 | major | 1561-1581 | First-generation drugs are said to act mainly on the inhibitory pathway and second-generation on the excitatory pathway; phenytoin and carbamazepine block Na+ channels and several second-generation drugs enhance GABA. The generalisation is false. |
| F-034 | G1 | major | 1599-1618 | Enzyme induction, megaloblastic anaemia and teratogenicity are said to be common to all first-generation drugs; valproate is an enzyme inhibitor and ethosuximide is not an inducer. |
| F-035 | D3 | major | 1637-1655 | Carbamazepine safety omits SJS/TEN with HLA-B*1502, aplastic anaemia/agranulocytosis, and failure of hormonal contraception through induction. |
| F-036 | D2 | major | 1524-1560 | The chapter has no drug-of-choice table by seizure type and no status epilepticus algorithm. |
| F-042 | G1 | major | 1942-1953 | Baclofen is said to increase chloride influx; GABA-B is a G-protein-coupled receptor that opens K+ channels and reduces presynaptic Ca2+ influx. |
| F-044 | G1 | major | 2109-2117 | The classification table says depolarising blockers cause hyperpolarisation; they cause persistent depolarisation. |
| F-045 | D3 | major | 2204-2225 | Succinylcholine safety omits hyperkalaemia (burns, crush injury, denervation, myopathy), bradycardia, raised intra-ocular pressure and muscle pain. |
| F-048 | G1 | major | 2355-2378 | Benzodiazepine half-life classes are wrong: diazepam and clonazepam are long-acting (diazepam 20-80 h plus active nordiazepam); oxazepam is short-intermediate; lorazepam, used later, is missing. |
| F-050 | G1 | blocker | 2536-2538 | Benzodiazepines are called 'very safe' with a toxic dose 1000-fold the therapeutic dose; combined with alcohol, opioids or other depressants they cause fatal respiratory depression (FDA boxed warning). |
| F-052 | G1 | major | 2578-2580 | Buspirone acts as a 5-HT1A partial agonist; the 5-HT2A attribution is wrong. |
| F-056 | D1 | major | 2952-2995 | Inhaled-anaesthetic pharmacokinetics are absent: MAC, blood:gas partition coefficient and speed of induction/recovery are not taught. |
| F-060 | G3 | major | 3168-3187 | The endoscopy MCQ key says D (sevoflurane) but the rationale explains midazolam (C). |
| F-062 | D3 | major | 3257-3268 | Local anaesthetic systemic toxicity lacks seizures, bupivacaine cardiotoxicity, maximum doses and the 20% lipid emulsion treatment. |
| F-065 | G2 | major | 1-3352 | The source is nine slide decks: fragmented bullets, no learning objectives, no recap of prerequisites, no key takeaways, and teacher prompts ('4 minutes', 'the slides mention') mixed with student text. |
| F-069 | G3 | major | 180-3352 | Assessment is uneven: 0-4 MCQs per chapter (none for skeletal muscle relaxants), five options (A-E) instead of four, and some rationales lack the answer letter. |
| F-070 | G4 | major | 1-3352 | The source cites no references at all. |
| F-071 | D2 | major | 1-3352 | Across chapters, therapeutic choice is rarely justified by guideline or patient factors (Parkinson's initial therapy, epilepsy by seizure type, insomnia and GAD algorithms are thin or absent). |
| F-072 | G1 | major | 71-79 | Cholinesterase inhibitors and memantine are presented as slowing disease progression; they are symptomatic treatments with modest, temporary benefit and do not modify the disease course (repeated at lines 101-104 and 196-228). |
| F-073 | G1 | major | 1185-1188 | SSRI sexual dysfunction is said to disappear after two weeks; nausea often settles, but sexual dysfunction commonly persists and must be reviewed. |
| F-075 | G1 | major | 1557-1559 | Loss of consciousness is said to be constant in all generalised seizures; awareness can be preserved in myoclonic seizures. |
| F-077 | D2 | major | 2433-2511 | Benzodiazepine indications mislead: OCD is listed as a routine indication, anticonvulsant use is 'no longer accepted', and diazepam is the only status-epilepticus choice; IV lorazepam or buccal/IM midazolam are preferred by setting and clobazam/clonazepam keep selected roles. |
| F-078 | D3 | major | 2725-2738 | Z-drugs are said to show few withdrawal effects and little tolerance; they can cause dependence, withdrawal, next-day impairment and complex sleep behaviours (FDA boxed warning). |
| F-079 | D2 | major | 3104-3166 | Ketamine is called generally preferred in paediatrics and the MCQ keys it without a scenario; induction-agent choice depends on haemodynamics, airway, procedure and need for analgesia. |
| F-080 | D3 | major | 526-541 | The schizophrenia case answer switches to risperidone for involuntary movements without identifying the movement disorder; risperidone has dose-related EPS and anticholinergics can worsen tardive dyskinesia. |

Minor findings are in `findings.json`.
