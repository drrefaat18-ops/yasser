# Evaluation fixes (Fix Protocol)

Review: `codex-review.md` (GPT-5, read-only, reviewed commit 0a25871). Every finding was checked against the source text and a standard reference, its root cause was named, and siblings were hunted. Verification: `findings.json`, `scorecard.json` and `report.md` regenerated; `complete evaluate` runs the schema, cap and total checks.

| ID | severity | status | root cause | fix | siblings |
|---|---|---|---|---|---|
| E-01 | minor | fixed + verified | F-004 described cautions as contraindications | F-004 claim and fix hint reworded (pulse review, caution in conduction disease, bradycardic drugs) | none |
| E-02 | minor | fixed + verified | F-008 treated hypertension as wrong; it is part of autonomic lability | F-008 reworded: omissions are mental status, autonomic lability, CK, management; convulsions not defining | none |
| E-03 | major | fixed + verified | F-021 fix hint over-simplified NICE NG222 | Fix hint now stratifies by severity with shared decision (psychological therapy, antidepressant, or both) | F-071 (therapeutics, all chapters) keeps guideline wording general |
| E-04 | minor | fixed + verified | Severity inflated for an imprecise, not unrelated, target | F-039 downgraded to minor | none |
| E-05 | major | fixed + verified | F-063 fix hint revived the absolute end-artery rule | F-063 reworded: caution in impaired circulation and with sympathomimetics; digital blocks acceptable when selected | none |
| E-06 | major | fixed + verified | Missed: disease-modifying claim for symptomatic AD drugs | Added F-072 (G1 major, lines 71-79, repeats at 101-104, 196-228) | F-003 (anti-amyloid update) already covers the contrast |
| E-07 | major | fixed + verified | Missed: SSRI sexual dysfunction said to resolve | Added F-073 (G1 major, lines 1185-1188) | F-029 (PPI advice) is the adjacent line; kept separate |
| E-08 | minor | fixed + verified | Missed: amantadine reuptake wording | Added F-074 (G1 minor) | none |
| E-09 | major | fixed + verified | Missed: consciousness 'constant' in generalised seizures | Added F-075 (G1 major, lines 1557-1559) | F-041 (absence mechanism) stays minor |
| E-10 | minor | fixed + verified | Missed: vecuronium active metabolite | Added F-076 (G1 minor) | Sibling found: pancuronium 'renally unchanged' (line 2167) added as F-082 |
| E-11 | major | fixed + verified | Missed: benzodiazepine indications (OCD, epilepsy, status epilepticus) | Added F-077 (D2 major, lines 2433-2511) | Sibling found: epilepsy deck line 1574 limits BZs to status/febrile seizures, added as F-081 |
| E-12 | major | fixed + verified | Missed: Z-drug dependence and boxed warning | Added F-078 (D3 major, safety, lines 2725-2738) | none |
| E-13 | major | fixed + verified | Missed: ketamine 'preferred in paediatrics' and scenario-free MCQ | Added F-079 (D2 major, lines 3104-3166) | F-060 (wrong key) is the other GA MCQ defect |
| E-14 | major | fixed + verified | Missed: unsafe EPS management in the schizophrenia case | Added F-080 (D3 major, safety, lines 526-541) | F-007 (EPS classification) is the teaching-text sibling |
| E-15 | major | fixed + verified | Scores interpolated outside the anchor bands | Rescored to bands: G1 3 (cap 4 still applied), G2 4, G3 4, D3 4; total recomputed to 36.5 | none |
