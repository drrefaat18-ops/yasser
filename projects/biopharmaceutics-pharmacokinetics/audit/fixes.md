# Fix Protocol — Codex review of the finished book

One read-only Codex review of this artifact (Rule 11), recorded verbatim in `audit/codex-audit.md`:
20 findings, 19 major and 1 minor, verdict `fail`. Each was confirmed against the text before any
edit, the root cause was identified, siblings were hunted, and the result was re-checked. Nothing was
accepted on the reviewer's word alone; two findings were narrowed on inspection, and none was
dismissed.

Fixes land in commit `1472d00`. All 14 chapters pass the checker 33/33 and the rebuilt PDF passes all
seven `check_pdf` gates.

## The finding that mattered most

**C-009, ch10.** The chapter printed apparent half-lives of 15.0 h and 29.9 h for phenytoin at 6 and
16 mg·L⁻¹. Codex said both were wrong. They were.

`0.693 · Vd · (Km + C) / Vmax` is 0.693 over the Michaelis–Menten elimination rate constant *at one
instant*. For a first-order drug that equals the halving time, because the rate constant never
changes; here it rises continuously as C falls, so the drug halves sooner. Integrating Equation 10.1
from C₀ to C₀/2 gives `(Vd/Vmax)·[Km·ln 2 + C₀/2]` — 12.5 h and 23.3 h, 20% and 29% below the printed
figures.

This chapter had already been checked by this agent and passed. That check confirmed the arithmetic
of the printed formula and never asked whether the formula measured the quantity the sentence claimed
it measured. Verifying a calculation is not the same as verifying the claim it is offered as evidence
for, and the remaining findings were re-examined on that basis.

**Sibling hunt.** Every other place in the book where a half-life is computed was re-derived. All the
rest are genuinely first-order, where 0.693/K is exact, so C-009 is isolated to ch10. The chapter now
prints both forms, names which is which, and says why they differ.

## The rest, by root cause

**Over-claiming from an underdetermined result** — C-001 (ch04: body weight alone does not fix the
micro-rate constants), C-003 (ch06: a clearance ratio below 1 may be protein binding, not
reabsorption), C-005 (ch06: Mu/AUC is a formation clearance, not hepatic clearance), C-007 (ch07: a
curved residual line has four possible causes, and Example 7.1 is a counterexample to the stated
rule), C-010 (ch10: non-compartmental analysis still runs on non-linear data; what fails is
extrapolation across doses), C-013 (ch13: first-pass loss is part of F and does not invalidate the
urinary method). Each now states the assumption or the alternative explanation instead of asserting a
conclusion the data do not carry.

**Dimensional error** — C-012 (ch12: `D·A·K/h` is a permeability–surface-area product in cm³·s⁻¹; the
permeability coefficient is `p = D·K/h` in cm·s⁻¹) and C-016 (ch14: `D·A·(Cs − C)/h` is a mass rate,
so Equation 14.1 is `dm/dt`, with `dC/dt` carrying the medium volume). C-016 required deviating from
the approved `design/errata-seed.md`, which prescribed the dimensionally impossible form. The rework
had previously kept the approved wording and noted the discrepancy in a callout; that was the right
instinct about approvals and the wrong outcome for a book whose domain pillar is unit accuracy. The
ledger row for E-012 records the deviation and the reasoning.

**Symbol collision** — C-006. ch03 used `fe` and ch06 used `fu` for the fraction excreted unchanged,
while `fu` conventionally means fraction unbound. `fe` now runs through both chapters (15
occurrences changed) and a Watch the Units box warns about the other convention.

**Unit-of-account error** — C-011 (ch11: `fm` is a molar fraction, so `fm·D` in milligrams is exact
only when parent and metabolite share a molar mass). The conversion factor is now stated.

**Regulatory statements wider than the guidance** — C-014 (no blanket biowaiver for topical or
gut-acting products), C-015 (the narrowed NTI range is automatic for AUC, extended to Cmax only where
Cmax matters for safety), C-017 (apparatus 5–7 are USP `<724>`, not `<711>`; the reference is added),
C-018 (the 10% acid-stage limit is the A1 criterion; A2 and A3 allow an average of 10% with no unit
above 25%). Each was checked against the cited guideline before editing.

**Terminology reintroduced after being corrected** — C-019 (ch01 E1.1 called MTC/MEC a
"concentration-based therapeutic index" although §1.2 defines the therapeutic index as TD50/ED50, the
very confusion errata row E-011 closes). It is now the therapeutic concentration ratio, with a
paragraph separating the two.

**Deliverable mismatch** — C-020. The brief asked for one consolidated reference list at the end; the
book had only per-chapter lists. Those cannot be removed, because `check_citations` resolves every
`[n]` inside the file that cites it, so `rework/references.md` was added as back matter and
`harness/tools/assemble.py` now appends an optional references file. The residual awkwardness of three
parallel numberings is recorded as open finding A-004.

**Narrowed on inspection.** C-002 was reported as creatinine being secreted; correct, and the fix
separates inulin (filtration only, measures GFR) from creatinine (also secreted, so its clearance runs
10–20% high). C-008 was reported as a contradiction between the Q10 rationale and Equation 8.2; the
rationale was not wrong so much as unqualified, since the question asks about doubling the dose, and
it now distinguishes the IV case from the oral one rather than being rewritten.

## Found by this agent, not by the review

`ch03` and `ch08`–`ch14` shared a single answer-key sequence, `BDACBCDABC`, and `ch04` and `ch07`
shared `CADBCBADCB`. Eight of the fourteen chapters could therefore be answered by a student who
noticed the pattern in one of them. The chapter checker cannot see this: it enforces 2–3 keys per
letter and a maximum run of 2 *within* a chapter, and every chapter satisfied both.

Eight chapters were resequenced by transposing option slots — 20 questions in all. Every stem is
unchanged, the text of every correct answer is unchanged, and letter references inside rationales
("Option A is the renal clearance instead") were remapped through the same permutation. This was
verified mechanically across all 80 questions in the affected chapters: for each, the keyed option's
text before and after is identical and the set of four options is unchanged. The 14 sequences are now
distinct, each with 2–3 keys per letter and no run above 2.

## Not fixed

The errata ledger is still not printed in the book. Adding it would change `assemble()` for every
book the harness builds and break a committed fixture that asserts the current back matter, so the
front matter's promise was corrected instead and the gap is recorded as open finding A-001.

## Round 3 — review of commit 8d64734

Recorded verbatim in `audit/codex-audit-r3.md`: 18 findings, 14 major and 4 minor, verdict `fail`.
Codex recomputed every worked example and exercise and found no arithmetic or unit error; every
finding is about what a statement claims. Each was confirmed against the text before editing, and
all 18 are real. No text was removed to make room: the fixes took the book to 52,187 words, and the
ceiling was raised instead (DEC-009).

| ID | Root cause | Fix | Siblings hunted |
|---|---|---|---|
| C-001 | A Vd range was stated without comparing it to real body-fluid volumes | ch02 §2.4 gives plasma, ECF and total body water, and reads Vd against them | Every L·kg⁻¹ value in the book; none other interprets a range |
| C-002 | The E1.2 answer said tmax could not be predicted after predicting it | All three follow from the stated linear model; §1.3 already gives tmax's dose independence | — |
| C-003 | The §3.5 table credited the rate method with zero order; Q10 keyed "neither" | Table separates the descriptive rate plot from Equation 3.2; Q10 stem names K and t½ | Q10 rationale updated to cite the table |
| C-004 | The notation box reversed fe and fu | Standard notation: fe excreted unchanged, fu unbound; fu added to the glossary | `fe,unbound` and "unbound fraction times GFR" in ch06 replaced with fu × GFR |
| C-005 | Creatinine called "filtered only" | Inulin is the reference; creatinine reads high because it is secreted | Example 6.1 Step 7 notes the bias; glossary GFR entry already correct |
| C-006 | Ratio table compared with unadjusted GFR | Ratio is Cl / (fu × Cl_inulin); a low unadjusted ratio is compatible with binding alone | Example 6.1 already said so; takeaway aligned |
| C-007 | Formation clearances said to sum to Cl_T | The restrictive mass-balance conditions are stated; otherwise they are partial clearances | — |
| C-008 | Example 7.1 gave the fraction absorbed and used it as F | The input is now F = 0.80, with the fa condition stated | Example 6.1 had the same slip ("absorbed dose" for F × D₀); fixed |
| C-009 | Equation 8.2 is an interval-AUC result presented as a general time to steady state | Named as the time for the interval AUC (Css,av) to reach half; IV bolus peaks and troughs shown to share it; oral peaks and troughs do not | Common Mistake box, takeaway and glossary entry aligned |
| C-010 | Two named studies left uncited, one untraceable | DeHaan 1973 and Regamey 1973 traced by search and cited in ch08 and the consolidated list; procainamide labelled an illustration | Errata row E-035 added for F-031; Oser (ch13) was not flagged and is left as disclosed |
| C-011 | "NCA needs only linearity" contradicted ch10 | Areas compute for any drug; linearity is needed to interpret and scale them | §9.1, takeaway and Q1 rewritten; key unchanged (B), balance unchanged |
| C-012 | Q6 said "non-linear" where only saturable elimination fits the key | Stem narrowed to capacity-limited elimination | — |
| C-013 | Oral protein absorption stated as zero | Very poor, usually below 1%, with vesicular uptake and enhancer products noted | — |
| C-014 | K reused for the partition coefficient | K_part in Equation 12.1, its text and the glossary | No other chapter uses K for partitioning |
| C-015 | Solutions said to give complete absorption | No dissolution step; completeness still depends on stability, permeability and first pass | — |
| C-016 | Equal tmax read as equal rate | tmax is a rate-related endpoint, not Ka; equal rate needs the whole profile | — |
| C-017 | USP <711> A1 written as "less than 10%" | "No individual value exceeds 10%"; exactly 10% passes | §14.4, the summary line, Q8 option A and its rationale |
| C-018 | `[[...]]` wiki tokens in three glossary entries printed literally | Plain italic cross-references | Harness: new `TYPO-WIKILINK` and `BOOK-WIKILINK` checks (commit `9adb992`) scan chapters, front matter, glossary and references; the old glossary fails them |

After the fixes all 14 chapters pass the checker, the build passes its 31 math checks and all seven
`check_pdf` gates (173 pages), `verify --through build` is clean, and no `[[` survives in the PDF.
Because the chapters changed, round 3 no longer describes the content to be scored; the audit
closes on a fresh review of this commit.

## Round 4 — review of commit 5b91e15

Recorded verbatim in `audit/codex-audit-r4.md`: 14 findings, 6 major and 8 minor, verdict `fail`, down
from 18 and 14 major. Codex again reproduced every numerical answer (14 worked examples, 42 exercise
solutions, 140 keyed MCQs). All 14 findings are real; one was narrowed. Two were siblings this agent
missed in round 3, and are recorded as such.

| ID | Root cause | Fix | Siblings hunted |
|---|---|---|---|
| C-001 | Disease effects on Vd stated as universal | Direction depends on the drug; Q8 stem now names a hydrophilic, extracellular drug | — |
| C-002 | "Two-way ANOVA right, t-test wrong" without a design | Unpaired t-test wrong; paired t-test fits two treatments; crossover needs ANOVA or a mixed model | — |
| C-003 | An infusion sample called a trough; five half-lives read as a law | Called a steady-state sample; earlier timed samples interpretable but not as the plateau; Q3 stem says "read directly as the steady state" | Only occurrence of "trough" in ch05 |
| C-004 | Glucose clearance given as zero unconditionally | Below the renal threshold only | — |
| C-005 | A K threshold for flip-flop | Removed as a rule; Ka < K decides, and needs both estimated | — |
| C-006 | ch08 takeaway "half-life only" | Restricted to infusion and IV boluses; Ka named for oral | **Missed sibling of round-3 C-009** |
| C-007 | Glossary "NCA requires only linear kinetics" | Areas computable from any data; interpretation needs linearity | **Missed sibling of round-3 C-011** |
| C-008 | Polar metabolite "has" a smaller Vd | "Often", with the exceptions named | — |
| C-009 | Propranolol food effect given as enzyme saturation | Reduced first-pass hepatic extraction; mechanism not fully resolved | — |
| C-010 | Oser 1945 still uncited | Cited as Melnick, Hochberg, Oser, J Nutr 1945;30(2):67–79, DOI verified through Crossref | Errata row E-035 extended; consolidated list updated |
| C-011 | "Cpmax and tmax measure rate" contradicted ch01 | Both rate-sensitive; Cpmax also depends on extent, tmax on K | ch13 takeaway, glossary tmax |
| C-012 | TOST 5% read as a patient-level risk | Study-level Type I error at the limit | Q7 rationale |
| C-013 | 5 mg/mL and 50%/30 min read as BCS criteria | **Narrowed:** Codex called them obsolete or invented; they are the current examples in 21 CFR 320.33(e), now cited, and distinguished from the BCS criteria of §13.6 | — |
| C-014 | Sink conditions in vivo "maintained naturally" | Absorption helps; not guaranteed; drug-, dose- and formulation-dependent | Glossary sink entry defines the in-vitro term only; unchanged |

Two sentences made long by these fixes were split, with nothing removed. After the fixes all 14
chapters pass the checker (52,743 words), and the build passes its math checks and all seven
`check_pdf` gates; `verify --through build` is clean.

## Round 5 (claude-sonnet-5-5 per DEC-010, commit 10215fb)

Codex reached its usage limit partway through its own fifth review. The one finding it had confirmed, that E8.1 derived F = 1 from complete absorption, was fixed in eebab26. The Sonnet review is recorded in `audit/review-r5.md`: 16 findings, 3 of them major.

| ID | status | real/rejected | root cause | fix |
|---|---|---|---|---|
| C-001 | fixed + verified | real | Du∞ was presented as both an input to and an output of the sigma-minus plot, and Ke was said to be unobtainable from it | §3.4 now says Du∞ is estimated from a complete collection's plateau, or fitted, and the intercept checks it. The table shows Ke from either method once the dose is known. Q9 asks what must be known before plotting (key D). |
| C-002 | fixed + verified | real | The diagnostic step used the final fitted parameters, not the ones being tested | Step 5 uses the residual intercept of 107 with Ka = 0.25 (≈ 2 µg·mL⁻¹, 8%), then gives the quarter figure from the final A = 160 and Ka = 0.200 |
| C-003 | fixed + verified | real | Kh was renamed Knr in round 4, and its siblings were missed | ch06 paragraph, ch10 back-reference and ledger E-020 all say Knr |
| C-004 | fixed + verified | real | The symmetry of the exponentials was stated as symmetry of the whole curve | With A free the fitted curve is the same, but the assignment changes K, t½ and Vd/F by K/Ka. Both mentions in ch07 are fixed. |
| C-005 | fixed + verified | real | Round-4 sibling left in the prose and the figure | §6.2 and the Figure 6.1 label and alt text now say "below its renal threshold" |
| C-006 | fixed + verified | real | Misread of Example 10.1 | 300 mg·day⁻¹ gives 6.0 (below the range), 400 gives 16.0 (inside it) |
| C-007 | fixed + verified | real | Round-4 sibling left in the Key Takeaways | Takeaway hedged: "often a smaller Vd" |
| C-008 | fixed + verified | real | Round-4 sibling left in the Figure 1.2 caption and in ch07 §7.8 | Both now say "most sensitive to rate", noting that Cpmax also depends on extent |
| C-009 | fixed + verified | real | Rounding: t½ recomputes to 26.3 h | "about 26 h" |
| C-010 | fixed + verified | real | Wrong unit argument | "units of mg·L·h⁻², not a concentration" |
| C-011 | fixed + verified | real | Wrong origin given for the distractor | Option A is the elimination half-life, 0.693 ÷ 0.15 |
| C-012 | fixed + verified | real | The five methods were listed in an order the text contradicts | Order claim dropped; the relative precision is stated. The dissolution rule now applies only to dissolution-limited drugs with an IVIVC. |
| C-013 | fixed + verified | real | Barbiturates (pKa about 7.2–8) were listed in the pKa > 8 row | Removed from that row. A sentence after the table places them at the boundary of the two weak-acid rows. |
| C-014 | fixed + verified | real | Date conflated (web check: ECA Academy) | Salicylic acid calibrators were no longer required from December 2009; since May 2023 the prednisone DPVS is the only standard for Apparatus 1 and 2 |
| C-015 | fixed + verified | real | Resequencing made the full sequences distinct, but not their first four keys | Options swapped, with rationale letters updated, in ch09 Q1–4 (now CADB), ch10 Q1–4 (DCBA) and ch12 Q1–3 (ABD). Only ch03 now starts BDAC. The checker's key balance passes. |
| C-016 | fixed + verified | real | Wrong section pointer | E-027 points to Section 13.4 |
