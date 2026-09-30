# Audit review of the finished book, round 5 — biopharmaceutics-pharmacokinetics

reviewed_commit: 10215fb

Read-only review by claude-sonnet-5-5 as a fresh-context subagent (DEC-010: in place of Codex, which reached its usage limit partway through its own fifth round; the one finding Codex had confirmed, E8.1, was fixed in eebab26 before this review). Same request as `audit/codex-prompt.md`. The book was written by claude-opus-5-5. Saved from the verdict line on. Kept as a record: its findings were fixed in the next commit.

verdict: fail
open_blocker_major: 3
reviewer_model: claude-sonnet-5-5

| ID | severity | location | finding | why it matters | suggested fix |
|---|---|---|---|---|---|
| C-001 | major | Ch3 §3.5 table row "Ke" ("Obtainable from the intercept" vs "Not obtainable"), §3.4 "Du∞ must be known before a single point can be plotted", Q9 (key B) and its rationale | Q9 asks what sigma-minus cannot provide and keys B (Ke). The book's own equations contradict that: Ke = fe·K = K·Du∞/D_B⁰, and the sigma-minus method supplies K and uses Du∞. The rate method's intercept Ke·D_B⁰ also needs the dose, so the table's asymmetry is false. Option D (Du∞) is also defensible as "not provided", because §3.4 says Du∞ must be known before plotting. Yet LO3 and Q3 say the method determines Du∞ from the intercept. The rationale itself admits "Ke can still be found afterwards from fe". | Two of the four options (B, D) are defensible as the answer to a "cannot provide" item, and the text is circular about Du∞ as input versus output. | Drop Q9 or replace it with a question that has one answer. Fix the table row: Ke follows from either method once Du∞ and the dose are known. State that Du∞ is an input estimated independently, or fitted as a third parameter, and is not an output of the plot. |
| C-002 | major | Ch7 Example 7.1, Step 5: "the absorption term at 16 h would be A·e^(−Ka·16), which is roughly 6 µg·mL⁻¹ against a measured 25.8, or a quarter of it" | With the stated A ≈ 105 and Ka ≈ 0.25, 105·e^(−4) = 1.9 µg·mL⁻¹ (7% of 25.8), not 6. The figure 6.5 (a quarter) comes only from the true parameters A = 160, Ka = 0.200. The step says it is testing the hypothesis Ka ≈ 0.25 but uses numbers from the later-fitted model. | The numerical justification for the diagnosis is not reproducible from the stated inputs. | Either use the residual-line intercept (about 107) with Ka = 0.25, which gives about 2 µg·mL⁻¹ or 8%, and say so. Or move the "quarter" claim to after Step 6 and compute it with A = 160 and Ka = 0.200. |
| C-003 | major | Ch6 §6.4, the paragraph "The symbol Kh is used deliberately…"; Ch10 §10.2 "Chapter 6 used the symbol Kh for the hepatic elimination rate constant"; errata-ledger E-020 ("The hepatic elimination rate constant is Kh throughout ch06") | Ch6 now uses Knr and Cl_nr, and Kh appears nowhere else in the book (the glossary has Knr only). The Ch6 sentence is an orphan, Ch10 refers back to a symbol Ch6 no longer defines, and the ledger row records a fix the text no longer contains. | A dangling cross-reference, and a ledger claim that is false against the text. | In Ch6, replace the paragraph with "Knr, not Kh, is used so that Km stays free for Chapter 10". In Ch10 §10.2, say "Chapter 6 used Knr for the non-renal rate constant". Correct E-020. |
| C-004 | minor | Ch7 §7.7, "Equation 7.1 is symmetric in Ka and K: exchanging the two constants leaves the curve unchanged" | Swapping changes the coefficient: A = F·Ka·D/(Vd(Ka−K)) becomes F·K·D/(Vd(K−Ka)). Only the two-exponential shape, with A free, is symmetric. The curve is reproduced only if Vd/F is also rescaled by K/Ka (a factor of 4 in E7.3). The book never says that the flip-flop misassignment also distorts Vd/F. | The statement is mathematically false as written, and an important consequence is omitted. | Say "the fitted curve is the same for either assignment, with A free. The assignment changes K, t½ and the estimate of Vd/F". |
| C-005 | minor | Ch6 §6.2, "Glucose is reabsorbed completely, so its renal clearance is zero"; Fig 6.1 text "completely reabsorbed as for glucose" | This is a sibling of round-4 C-004. Only the §6.6 table was qualified ("below its renal threshold"); the §6.2 prose and the figure still state zero clearance unconditionally. | The unqualified statement hides saturable transport. | Add "below the renal threshold (transport maximum)" in §6.2 and in the figure label. |
| C-006 | minor | Ch10 "Why It Matters in Practice": "Example 10.1 puts 300 and 400 mg·day⁻¹ on either side of it [10–20 mg·L⁻¹]" | Example 10.1 gives Css = 6.0 and 16.0 mg·L⁻¹. 6 is below the range, but 16 is inside it, so the two doses are not on either side. | A factual slip against the chapter's own example. | "puts 300 mg·day⁻¹ below it and 400 mg·day⁻¹ inside it, yet 100 mg·day⁻¹ more tripled Css"; or say 16 is near the middle and a further small step overshoots. |
| C-007 | minor | Ch11 Key Takeaways, "Metabolism makes a drug more polar: a smaller Vd, less tubular reabsorption, faster excretion" | This is a sibling of round-4 C-008. §11.1 was hedged ("often… smaller"), but the takeaway restates the unhedged rule. | The summary contradicts the corrected body text. | "often a smaller Vd (binding and transport can reverse it)". |
| C-008 | minor | Ch1 Fig 1.2 caption ("Cpmax and tmax describe the rate of absorption"); Ch7 §7.8 ("tmax and Cpmax describe the *rate* of absorption, AUC describes its *extent*") | This is a sibling of round-4 C-011. Ch13, the glossary and the Ch1 Q2 rationale say that Cpmax depends on both rate and extent, while Ch1 §1.2 and the Ch7 text still give the unqualified form. | The same quantity is defined two ways in different chapters. | Use "rate-sensitive endpoints; Cpmax also depends on extent" in both places. |
| C-009 | minor | Ch3 E3.2 Comment, "Repeat the calculation with fe = 0.9 and the half-life rises to about 25 h" | Recomputed: Ke = 0.1247, Knr = 0.0139, K′ = 0.0139 + 0.01247 = 0.02637, t½′ = 26.3 h. | A stated number is not reproducible. | Say "about 26 h". |
| C-010 | minor | Ch5 Q1 rationale, "Option B [R×K×Vd] … would give an amount per time squared" | R·K·Vd has units mg·h⁻¹·h⁻¹·L = mg·L·h⁻², which is not an amount per time squared. | The rationale's unit argument is wrong. | Say "units of mg·L·h⁻², not concentration". |
| C-011 | minor | Ch7 Q8 rationale, "Option A divides ln 4 by K alone" | ln 4 ÷ 0.15 = 9.2 h, not 4.6 h. Option A (4.6 h) is 0.693/K, the elimination half-life. | The stated origin of the distractor is wrong. | "Option A is the elimination half-life 0.693/K". |
| C-012 | minor | Ch13 §13.3 "Five methods are used, in decreasing order of precision" and "the formulation that dissolves fastest in vitro will generally be absorbed fastest in vivo" | The list puts in-vitro dissolution after clinical response, which the same section (and Q6) calls the least sensitive and least accurate method. The dissolution claim is stated as a rule, but it fails for permeability-limited drugs and without an IVIVC (see §14.5). | An internal inconsistency that misleads on method ranking. | Drop "in decreasing order of precision", or reorder. Qualify the dissolution sentence ("for dissolution-limited drugs"). |
| C-013 | minor | Ch12 §12.4 table, "Very weak acid, pKa > 8 … barbiturates", against the same section's "Barbitone (pKa 7.8) and thiopentone (pKa 7.6)" | Barbitone and thiopentone are named barbiturates with pKa below 8, so they sit outside the class the table lists them in. | An internal inconsistency in a table students will memorise. | List "some barbiturates" under the weak-acid row, or drop them from the very-weak-acid row. |
| C-014 | minor | Ch14 §14.3, "since 2023 the performance verification test … uses the USP Dissolution Performance Verification Standard … and the salicylic acid calibrator has been withdrawn" | Checked by web search: the 2023 change replaced Prednisone Tablets RS with the new prednisone DPVS, and the salicylic acid tablet requirement was withdrawn in 2009. The sentence dates the withdrawal to 2023. | A minor regulatory dating error. | "Salicylic acid calibrators were withdrawn in 2009. Since May 2023 the only standard for Apparatus 1 and 2 is the prednisone DPVS." |
| C-015 | minor | Answer keys, first four keys of Ch3, Ch9, Ch10 and Ch12 | All four chapters start BDAC (Ch3 BDACBCDABC, Ch9 BDACDADABC, Ch10 BDACDCDCBA, Ch12 BDACBBDACC), and Ch2, Ch8 and Ch11 also start BD. The fixes note claims the sequences are distinct, which is true only for the full 10. The pattern is still exploitable across chapters. | It weakens the assessment, which was the purpose of the earlier resequencing. | Permute the first four keys in at least two of these chapters. |
| C-016 | minor | errata-ledger E-027 ("Section 13.3 states that no such rule exists") | The 5%-of-product statement is in §13.4 ("The reference product"), not §13.3. | A ledger pointer that does not lead to the text. | Change "Section 13.3" to "Section 13.4". |

## Notes

**Recomputed in Python and found correct**
- Every worked example's final values were reproduced, including intermediate tables: Examples 2.1, 3.1, 4.1, 5.1, 6.1, 7.2, 8.1, 9.1, 10.1, 11.1, 12.1 and 14.1, and the Ch13 example.
- Ch7 Example 7.1: the data are consistent with A = 160, K = 0.1 and Ka = 0.2, and regression over 16 h and later gives A = 105.06.
- Ch7 Example 7.2: the table, the slopes 0.285–0.703 and the zero-order differences reproduce. The 9.83 shown for 0.147 × 67.02 is 9.85, which is cosmetic.
- Example 9.1: the pieces (AUC 52.11, AUMC 290.8, tail shares 4.5% and 19.3%) reproduce. The "11.60" true 6–12 h area is 11.65, which is cosmetic.
- Ch10: the half-life derivation (Vd/Vmax)[Km ln2 + C0/2] is correct, and 12.5 and 23.3 h reproduce. The 20% and 29% are the instantaneous and integrated ratios.
- Ch8: the Eq 8.2 derivation is correct, and so is the 13% overstatement at Ka = 2K (true t = 1.772 t½).
- All 42 exercise solutions and all 140 MCQ keys were checked. No key is arithmetically wrong; only Ch3 Q9 (C-001) has a defensibility problem.
- F = fa × Fg × Fh is consistent across Ch7, Ch8 E8.1, Ch13 and the glossary.
- The symbols fe/fu, K_part, Rac, Kmet and R_D are used consistently, apart from the Kh residue in C-003.

**Regulatory checks made against sources**
- ICH M13A (PDF read): all of the following are consistent with Ch13.
  - washout "e.g., at least 5 elimination half-lives";
  - subjects ≥ 18 years with BMI preferably 18.5–30;
  - the assayed-content difference between test and reference should not exceed 5%;
  - NTI is deferred to M13C, so the book correctly attributes the narrowed NTI range to the EDA only;
  - at least three pre-dose concentrations for steady state.
- 21 CFR 320.33: solubility "less than 5 mg/mL", and "<50% in 30 min, compendial or paddle at 50 rpm in 900 mL water at 37 °C", are as the book states.
- USP <711> Apparatus 4: the flow rates of 4, 8 and 16 mL·min⁻¹ are correct, and "a pump without pulsation may also be used", so Ch14's "pulseless" remark is acceptable.
- USP <711> S1–S3 and the A1–A3 acid-stage criteria match the USP tables from memory.
- The ICH M9 definitions (≤250 mL, ≥85%, 15 and 30 min) and the class biowaiver table match.
- The EDA 4/2026 text could not be retrieved, so its Class 2 weak-acid pathway was not re-verified beyond its internal consistency with E13.3.

**First-edition findings**
- The spot-checked ledger rows (E-001 to E-005, E-008, E-010 to E-012, E-024 to E-028, E-034) are present in the chapter text.
- The exceptions are E-020, which is false (C-003), and E-027, whose pointer is wrong (C-016).

**Earlier-round fixes verified as holding:** Ch13 Cmax and TOST wording (round 4 C-012), E8.1 F = 1 as an assumption, the Ch14 sink wording, the Ch5 steady-state sampling wording, and the Ch7 flip-flop with no K threshold.
