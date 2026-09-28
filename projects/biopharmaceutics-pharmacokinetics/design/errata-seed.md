# Errata seed — Biopharmaceutics and Pharmacokinetics (PT-312)

Seed rows for `rework/errata-ledger.md`. Every row is a statement in the first edition that this edition changes.
`Status` is `open` until the correction is written and verified in the named chapter, then `fixed`; a row whose
content is removed rather than corrected closes as `removed-with-content`.

Line numbers are `ingest/normalized.md`; page numbers are the source PDF.

| ID | Finding | Chapter | Source | First edition says | This edition says | Status |
|---|---|---|---|---|---|---|
| E-001 | F-001 | ch13 | p99, line 4705 | BCS Class 2 (low solubility, high permeability) does not require an in-vivo bioequivalence study; Class 3 does. | ICH M9 grants BCS-based biowaivers to Class 1 and Class 3. Class 2 requires an in-vivo study, except under the narrow weak-acid pathway the Egyptian Drug Authority guideline allows, whose conditions are stated separately. | open |
| E-002 | F-002 | ch13 | p100, line 4735 | Highly permeable means extent of absorption ≥ 90% (F ≥ 0.9). | ICH M9: ≥ 85%. | open |
| E-003 | F-003 | ch13 | p100, line 4732 | Highly soluble: highest dose strength soluble in < 250 mL over pH 1–7.5. | ICH M9: highest single therapeutic dose soluble in ≤ 250 mL over pH 1.2–6.8 at 37 ± 1 °C. | open |
| E-004 | F-004 | ch13 | pp97–98, lines 4613–4631 | No acceptance criterion is stated. | ICH M13A: the 90% confidence interval of the test/comparator geometric mean ratio for log-transformed AUC and Cmax must lie within 80.00–125.00%, narrowed for narrow-therapeutic-index drugs. | open |
| E-005 | F-005 | ch13 | p98, line 4629 | A 95% confidence level, applied as a test that a difference is significant. | A 90% confidence interval, which is two one-sided tests at α = 0.05 each; the decision is equivalence within limits, not significance of a difference. | open |
| E-006 | F-006 | ch12 | p57, line 2947 | Oligopeptides are degraded by lactase and maltase. | Oligopeptides are hydrolysed by brush-border peptidases (aminopeptidase N, dipeptidyl peptidase IV) and cytosolic peptidases. Lactase and maltase are disaccharidases and move to carbohydrate digestion. | open |
| E-007 | F-007 | ch12 | p65, line 3286 | Tetracyclines are quaternary nitrogen compounds. | Tetracyclines are amphoteric with three ionisable groups. A genuine quaternary ammonium compound replaces them as the ion-pair example; tetracycline is kept as its own case. | open |
| E-008 | F-008 | ch11 | p50, line 2601 | Black men are faster acetylators and metabolizers than white men. | Acetylation rate is set by NAT2 genotype; slow and fast acetylator allele frequencies differ between populations and do not follow skin colour. CYP2D6 and CYP2C19 polymorphisms are given alongside. | open |
| E-009 | F-009 | ch12 | p63, line 3217 | Egyptians have a genetic defect for the carrier of vitamin B₁₂ absorption. | Removed. Vitamin B₁₂ uptake is intrinsic-factor-mediated receptor endocytosis and moves out of the facilitated-diffusion column. | removed-with-content |
| E-010 | F-010 | ch14 | p104, line 4870 | Apparatus 4 flow rate is 4–16 mL/min (usually 10–100 mL/min). | USP <711> Apparatus 4: 4, 8 and 16 mL·min⁻¹. | open |
| E-011 | F-011 | ch01 | p5 figure; p6, line 164 | The MEC-to-MTC band is labelled therapeutic index (TI). | The band is the therapeutic range (therapeutic window). Therapeutic index is the ratio TD50/ED50, defined separately. | open |
| E-012 | F-013 | ch14 | p102, line 4783 | The Noyes–Whitney equation is a picture; only its symbol list is text. | dC/dt = (D·A/h)(Cs − C), set as numbered text, with the sink-condition simplification C ≪ Cs. | open |
| E-013 | F-014 | ch07 | p35, line 1704 | Wagner–Nelson example tabulates Cp in mg/mL. | µg·mL⁻¹, with units carried through AUC and every derived column. | open |
| E-014 | F-016 | ch06 | p29, line 1349 | Example 16: 100 mg oral, systemically available, 60 mg unchanged and 30 mg metabolite recovered. | The assumption covering the unrecovered 10 mg is stated, so fu is determined rather than guessed. | open |
| E-015 | F-026 | ch12 | p56, line 2894 | "studded ببحم with microvilli" | Gloss removed from the body. | removed-with-content |
| E-016 | F-026 | ch13 | p82, line 4014 | "The nonproprietary name دحاو ىأ كلم شم" | Gloss removed; the term goes to the bilingual glossary. | removed-with-content |
| E-017 | F-026 | ch13 | p98, line 4675 | "Criteria for waiver ءافعإ of in vivo bioavailability study" | Gloss removed. | removed-with-content |
| E-018 | F-026 | ch14 | p107, line 4971 | "human cadaver ةثج skin" | Gloss removed. | removed-with-content |
| E-019 | F-027 | ch09 | p45, line 2420 | Procainamide compartment observation followed by ~70 exclamation marks. | The observation is kept and explained: the compartment count is a property of the data and the sampling design, not of the drug. | open |
| E-020 | F-028 | ch11 | p26 and p47, lines 1191 and 2459 | Km is used both for the hepatic elimination rate constant and for the Michaelis constant. | Hepatic elimination rate constant becomes Kh; Km stays the Michaelis constant. | open |
| E-021 | F-031 | ch13 | p100, line 4689 | "by Amidon et al in 1985" | Amidon et al., 1995, cited. | open |
| E-022 | F-012 | ch13 | pp94–95, lines 4514 and 4530 | Volunteers 54–91 kg, age 20–50 years. | ICH M13A: age ≥ 18 years, BMI typically 18.5–30 kg·m⁻². The weight band is labelled as the historical FDA criterion. | open |
| E-023 | F-033 | ch02 | p9, line 379 | Vd changes only in pathological conditions. | Vd changes most markedly in those conditions, and also varies with age, body composition, pregnancy and plasma protein binding. | open |
| E-024 | F-034 | ch13 | p96, line 4600 | Washout period of 10 t½. | ICH M13A asks for a washout long enough that pre-dose concentrations are negligible, commonly at least five terminal half-lives; ten remains a safe practical choice. | open |
| E-025 | F-037 | ch13 | p85, line 4148 | F = 1 for completely absorbed drugs. | F = fa × Fg × Fh. A completely absorbed drug can still have F well below 1 through gut-wall and hepatic first-pass loss; propranolol is the worked case. | open |
| E-026 | F-038 | ch13 | p83, line 4026 | Pharmaceutical equivalents may differ in release mechanism. | Release mechanism moves to the "same" column: products differing in it are pharmaceutical alternatives, not equivalents. | open |
| E-027 | F-039 | ch13 | p93, line 4469 | The reference standard should contain the drug at least 5% of the whole product. | Removed. Replaced by the ICH M13A comparator-selection and batch-potency requirements. | removed-with-content |
| E-028 | F-040 | ch11 | p50, line 2595 | Norfluoxetine, 4-OH propranolol, norverapamil and desmethyldiazepam are toxic metabolites. | They are active metabolites and move to the active list. NAPQI is kept as the toxic example and genuine reactive metabolites are added. | open |
| E-029 | F-041 | ch12 | p81, line 3966 | Bioavailability ranks Solution > emulsion > suspension > soft gelatin capsule > hard gelatin capsule > tablets. | Introduced as a general tendency following from the number of steps before absorption, with one counter-example where formulation overturns it. | open |
| E-030 | F-019 | ch01 | pp33–42 | Examples numbered 1–23, with 22 and 23 printed before 19–21. | Examples numbered per chapter (7.1, 7.2, …), so the order cannot break again. | open |
| E-031 | F-025 | ch06 | pp10 and 26, lines 418 and 1146 | Clearance is defined twice in near-identical words. | Defined once in ch06; ch02 carries a one-line forward reference. | open |
| E-032 | F-035 | ch08 | p40, line 2012 | Accumulation t½ formula asserted, and its IV collapse asserted. | Derived, with log(1) = 0 shown as the reason the bracket collapses, and the Ka > K assumption stated. | open |
