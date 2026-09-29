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
