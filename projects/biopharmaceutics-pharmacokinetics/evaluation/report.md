# Evaluation report — Biopharmaceutics and Pharmacokinetics (PT-312)

Source: `source/Biopharmaceutics and Pharmacokinetics Portsaid.pdf` (109 pages, SHA-256 `3cfc215a…9ff9`), read both
as `ingest/normalized.md` and, where the conversion could not be trusted, directly from the PDF.
Rubric: `rubric.json` (DEC-001). Review kind: self. **Total 44.0 / 100.**

| Pillar | Weight | Score | Weighted |
|---|---|---|---|
| G1 Content accuracy | 20 | 4 | 8.0 |
| G2 Pedagogical design and clarity | 20 | 4 | 8.0 |
| G3 Assessment quality | 10 | 4 | 4.0 |
| G4 Sources and currency | 10 | 3 | 3.0 |
| D1 Mathematical and unit accuracy | 20 | 6.5 | 13.0 |
| D2 Derivation and worked-calculation clarity | 20 | 4 | 8.0 |
| **Total** | **100** | | **44.0** |

39 findings: 5 blockers, 25 major, 9 minor. Scores and findings are post-review; `evaluation/fixes.md` records what
the Codex review changed and why.

## A note on method

The book is a PDF whose mathematics is set partly as pictures — 354 embedded images across 61 of its 109 pages — and
partly as Symbol-font characters in floating text boxes. Text extracted from it is therefore damaged in places, and an
absent line can mean either that the authors omitted it or that the converter dropped it. Every finding below that
turns on something being missing is evidenced from the PDF itself (image counts per page, word counts in the text
layer, font list), not from the converted Markdown. The first draft of this evaluation did not make that distinction
and overstated five findings as a result.

## What the book gets right

The topic sequence is sound and is the sequence a pharmacokinetics course should follow: definitions and the plasma
curve, compartment models, IV bolus by plasma and by urine, two-compartment, infusion, clearance, oral absorption,
multiple dosing, non-compartmental analysis, non-linear kinetics, metabolite kinetics, then the biopharmaceutics half
— physiology, formulation factors, bioavailability, bioequivalence and dissolution. Nothing essential to PT-312 is
missing from the syllabus, and nothing is present that does not belong.

Where the mathematics is legible it is correct. Cl = K·Vd, the ln/log₁₀ conversion through 2.303, the biexponential
two-compartment form, the hybrid-constant relations for K, K₁₂ and K₂₁, the Wagner–Nelson derivation, the
Michaelis–Menten limits at low and high concentration, and the USP dissolution S₁/S₂/S₃ acceptance table are all as
they should be. The datasets are internally consistent: Example 6 and the non-compartmental example share the same
300 mg dataset and both yield Cp⁰ ≈ 8.57 mg/L and K ≈ 0.173 h⁻¹; Example 14's single-dose and infusion arms agree on
Vd = 0.1 L/kg and Css ≈ 10 µg/mL; Example 8's urine increments give a monotonically falling excretion rate and recover
984 mg of a 1000 mg dose. Checking these is what puts D1 above the other pillars: the arithmetic in this book holds up.

The two unnumbered worked examples — the non-compartmental analysis with its AUC and AUMC table, and the three-
formulation comparison — show what the whole book could be.

## What has to change

**It is a set of notes, not a book.** The word "chapter" appears zero times in 109 pages, "summary" zero times, and
"objective" twice, neither of them a learning objective (F-021, F-022). The contents page lists 14 subjects with page
numbers that no heading in the body matches (F-024). A student cannot revise from it and a teacher cannot assign from
it.

**The examples have no answers.** None of the 23 numbered examples is worked through: the "Answer" heading is followed
by blank space, or in Example 8 by tables whose calculation columns are empty (F-018). The method of residuals, which
the book relies on twice and which is the hardest technique in the course, is described in prose and never once
demonstrated on numbers, although two examples supply the data for it (F-020). For a calculation-based course this is
the largest single defect.

**The mathematics is not text.** Equations are pictures or Symbol-font runs with subscripts set separately, so the
book cannot be searched, read aloud, translated or reflowed, and the Noyes–Whitney equation exists only as the single
image on page 102, leaving its symbol list defining symbols that appear nowhere in text (F-013, F-017). No equation
and no figure carries a number, and "Figure" appears zero times in the whole text layer (F-023).

**The regulatory chapters are out of date and, in one place, backwards.** The BCS table tells students that Class 2
drugs do not need an in-vivo bioequivalence study (F-001) — Class 2 is precisely the class that does. The biowaiver
thresholds are the withdrawn 2000 FDA numbers rather than ICH M9 (F-002, F-003), and neither ICH M9 nor ICH M13A is
mentioned anywhere (F-032). Most seriously, the bioequivalence chapter never states the acceptance criterion at all:
the 90% confidence interval of 80.00–125.00% appears nowhere in the book (F-004), and what does appear is a 95%
confidence level applied as a test for a difference (F-005). One rule is invented outright — that a comparator
product must contain at least 5% drug (F-039) — and the definition of pharmaceutical equivalence permits products to
differ in release mechanism (F-038), which would make an immediate-release and an extended-release tablet equivalent.

**Nine statements are wrong** and would be learned as fact: lactase and maltase digest oligopeptides (F-006);
tetracyclines are quaternary ammonium compounds (F-007); acetylator status follows race (F-008); Egyptians carry a
vitamin B₁₂ carrier defect (F-009); the flow-through cell runs at two incompatible flow rates (F-010); therapeutic
index means the MEC-to-MTC band (F-011); complete absorption means F = 1, with first-pass loss ignored two pages
after it was taught (F-037); four active metabolites are listed as toxic ones (F-040); and a Wagner–Nelson table
reports plasma concentrations a thousand times too high (F-014).

**Three textbooks support 109 pages, and nothing in the body is cited** (F-030). Named studies, dates and regulatory
statements — DeHann 1972, Regamey 1973, Oser 1945, "in 1961 FDA said", the Australian phenytoin outbreak, "Amidon et
al in 1985" — carry no source, and the Amidon date is wrong by a decade (F-031).

## What this implies for the rework

The brief is simplify and organise, with no new topics. That still holds — the syllabus is right and the arithmetic is
right — but the work is not only structural. It divides in three:

*Reconstruction, which changes no content.* Impose the 14 contents-page subjects as 14 numbered chapters with a fixed
internal shape; reset every equation as numbered text with a symbol table; redraw every figure with a number, a
caption and axis labels; work all 23 examples through in print, step by step with units; remove the duplicated
clearance section and the Arabic lecture glosses.

*Correction, which changes content and must be sourced.* Seventeen G1 findings and two D1 findings are wrong or
unsupported statements, and each needs a cited replacement. The bioequivalence and BCS material needs rebuilding on
ICH M9 and ICH M13A, with the Egyptian Drug Authority guideline as the national layer, and the 80.00–125.00%
criterion stated plainly. This is a larger job than the phrase "simplify and organise" suggests, and the design stage
should budget for it.

*Addition, which the user authorised at intake.* Objectives, takeaways, per-chapter questions with answers and
rationales, a glossary and a symbol table.
