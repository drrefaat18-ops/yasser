# Biopharmaceutics and Pharmacokinetics

**PT-312** · Faculty of Pharmacy, Pharmaceutical Technology Department

Prepared from the course notes of the Staff Members of the Pharmaceutical Technology Department.

These notes are for teaching. They are not prescribing guidance. Doses, product performance and
regulatory requirements change; check the current official sources before applying any figure in
practice.

## About This Edition

This edition keeps the fourteen subjects of the original notes, in the order they were taught. What
has changed is how they are presented.

The original notes were written as a reference for students who had already heard the lectures. Every
equation was there, but the reasoning between the equations often was not, and the twenty-three
numbered examples were set as questions without answers. A student revising alone had no way to check
whether an attempt was right.

Three things have been added throughout. Each chapter now opens with learning objectives and closes
with ten multiple-choice questions and three calculation exercises, every one of them worked through
step by step with the units carried at each line. Each chapter contains at least one fully worked
example built from a dataset in the original notes. And the figures have been redrawn, so that a
diagram can be read at the size it is printed.

Every number in this edition was recalculated before it was used. That exercise was worth doing: the
original datasets turn out to be more closely related than the notes reveal. Examples 5 and 8 are the
plasma and the urine view of one study, and Examples 9 and 10 describe one drug. Where the
recalculation disagreed with the printed answer, the disagreement is explained rather than hidden.

A small number of statements in the first edition were wrong, and they have been corrected. Several
follow international guidance that was revised after those notes were printed. The rest are ordinary
slips of the kind that survive any number of readings until someone works the arithmetic again. Each
correction is made in the chapter where the statement belongs, and the reasoning is given there rather
than being left for the reader to reconstruct. A separate errata ledger, issued with the course
materials alongside this book, tabulates all of them: what the first edition said, what this edition
says, and where the corrected figure comes from. Nothing there reflects on the teachers who wrote the
original notes.

## Contents

- [Chapter 1: Introduction to Biopharmaceutics and Pharmacokinetics](#chapter-1-introduction-to-biopharmaceutics-and-pharmacokinetics)
- [Chapter 2: One Compartment, IV Bolus: Plasma Data](#chapter-2-one-compartment-iv-bolus-plasma-data)
- [Chapter 3: One Compartment, IV Bolus: Urine Data](#chapter-3-one-compartment-iv-bolus-urine-data)
- [Chapter 4: Two Compartment, IV Bolus: Plasma Data](#chapter-4-two-compartment-iv-bolus-plasma-data)
- [Chapter 5: Intravenous Infusion](#chapter-5-intravenous-infusion)
- [Chapter 6: Clearance](#chapter-6-clearance)
- [Chapter 7: Oral Absorption](#chapter-7-oral-absorption)
- [Chapter 8: Multiple Dose Regimens](#chapter-8-multiple-dose-regimens)
- [Chapter 9: Non-Compartmental Analysis](#chapter-9-non-compartmental-analysis)
- [Chapter 10: Non-Linear Pharmacokinetics](#chapter-10-non-linear-pharmacokinetics)
- [Chapter 11: Pharmacokinetics of Metabolites](#chapter-11-pharmacokinetics-of-metabolites)
- [Chapter 12: Biopharmaceutical Considerations](#chapter-12-biopharmaceutical-considerations)
- [Chapter 13: Bioavailability and Bioequivalence](#chapter-13-bioavailability-and-bioequivalence)
- [Chapter 14: Dissolution](#chapter-14-dissolution)
- [Glossary](#glossary)
- [References](#references)

## How to Use This Book

Read the chapters in order. Each one assumes the one before it, and the cross-references are specific,
so a forward reference to Chapter 7 means that the point really is settled there and not earlier.

Work the examples with a pen. A worked example read passively teaches very little; the same example
attempted first and then checked teaches a great deal. The solutions give every step, so it is always
possible to find the line where an attempt diverged.

Carry the units through every calculation. This is the cheapest error check in the subject, and it is
used in every worked solution in this book. An answer that comes out in the wrong units is wrong,
whatever the arithmetic looked like.

Terms in **bold** are defined in the glossary at the back. Figures are numbered by chapter, and so are
examples and equations, so Equation 7.1 is the first equation of Chapter 7.

Six kinds of boxed note appear throughout:

- **Key Equation** — an equation to know, with its symbols and units.
- **Worked Example** — a full calculation from real data.
- **Watch the Units** — a unit trap that produces a plausible wrong answer.
- **Common Mistake** — an error that is easy to make and hard to spot.
- **Why It Matters in Practice** — the clinical consequence of the point just made.
- **Deeper Dive** — an extension beyond what the course requires.

The multiple-choice questions are tagged with the objective each one tests, so a wrong answer points
back to the section to reread.


---

# Chapter 1: Introduction to Biopharmaceutics and Pharmacokinetics

## Learning Objectives
By the end of this chapter you will be able to:
1. [LO1] Distinguish biopharmaceutics from pharmacokinetics by what each one studies.
2. [LO2] Label a plasma concentration–time curve with Cpmax, tmax, AUC, MEC and MTC, and say what each one measures.
3. [LO3] Distinguish the therapeutic range from the therapeutic index.
4. [LO4] State the assumptions of the one-compartment open model and say when a second compartment is needed.

## 1.1 Two Sciences, One Question

A tablet is swallowed. Hours later the patient feels better, or does not. Between those two moments sit two sciences, and they ask different questions.

**Pharmacokinetics** is the kinetic study of ADME: **absorption**, **distribution**, **metabolism** and **elimination**. It asks how fast each happens, and what concentration results at any time [1].

**Biopharmaceutics** studies how the physicochemical properties of the drug, the dosage form and the route of administration control the rate and extent of absorption [2]. It asks what the product does before the kinetics begin. Four things about a product concern it: the stability of the drug in the dosage form, whether the drug is released, how fast it is released, and how much is absorbed systemically.

**Bioavailability** is where the two sciences meet. It is the rate and the extent of drug absorption from the dosage form into the systemic circulation. Both words matter, and Chapter 13 separates them. Some products are not meant to reach the blood at all. For an antacid, bioavailability is assessed from the effect at the site of action, not from a plasma sample.

![A left-to-right chain of four boxes: drug in dosage form, drug released and dissolved, drug in systemic circulation, drug in tissues. An arrow runs down from tissues to pharmacological response, and out from systemic circulation to elimination by metabolism and excretion. A bracket labelled Biopharmaceutics spans the first three boxes; a bracket labelled Pharmacokinetics spans from systemic circulation onwards.](../rework/figures/out/ch01-release-to-response.png)

*Figure 1.1 — From dosage form to response. Biopharmaceutics governs the steps up to systemic circulation; pharmacokinetics governs what happens after. No step in the chain can be skipped.*  
Original diagram, redrawn from the first edition page 4 (original)

Read Figure 1.1 from left to right. No step can be skipped. A drug that never dissolves never reaches the blood, whatever its potency.

## 1.2 Measuring the Drug

Drug concentration can be measured in plasma, urine, saliva or milk. Plasma is the most direct and accurate, and is this book's default. Urine mirrors plasma for drugs excreted unchanged, and Chapter 3 uses it.

The amount of drug in the body cannot be measured directly. The plasma concentration can. Every method here works from that one fact.

![A concentration-time curve rising to a peak at about two hours and then falling. The area beneath it is shaded and labelled AUC. Dashed lines mark the peak concentration on the vertical axis and the time of the peak on the horizontal axis. Two horizontal dashed lines mark the minimum effective concentration and the minimum toxic concentration, with the band between them bracketed and labelled therapeutic range.](../rework/figures/out/ch01-plasma-curve.png)

*Figure 1.2 — The plasma concentration-time curve after an oral dose. Cpmax and tmax describe the rate of absorption; the shaded area (AUC) describes its extent. The band between MEC and MTC is the therapeutic range.*  
Original diagram, redrawn from the first edition page 5 (original)

Three quantities are read off Figure 1.2.

**Cpmax** is the peak plasma concentration. It depends on the dose, on the absorption rate constant Ka and on the elimination rate constant K.

**tmax** is the time of the peak. It measures the *rate* of absorption, and Chapter 7 shows that it does not depend on the dose.

**AUC**, the area under the curve, measures the *extent* of absorption — the total amount of drug reaching the circulation.

Two horizontal lines complete it. The **minimum effective concentration** (MEC) is the concentration below which the drug does not work. The **minimum toxic concentration** (MTC) is the concentration above which it harms.

> **Common Mistake:** The band between MEC and MTC is the **therapeutic range**, also called the therapeutic window. It is not the therapeutic index. The **therapeutic index** is a *ratio*, classically TD50/ED50, and it carries no units. A range is a band of concentrations; an index is a number. The first edition used "therapeutic index" for both. Keep them apart: calculating an index and keeping a patient inside a range are different tasks.

Pharmacokinetics is studied from two sides. The *experimental* side develops sampling, assays and data handling. The *theoretical* side builds models that predict disposition. This book works mostly on the second, but every equation in it was fitted to data someone had to collect.

## 1.3 What a Pharmacokinetic Model Is

A **pharmacokinetic model** is an equation that simulates the rate processes of ADME and predicts the drug concentration in the body at any time. Models earn their place by what they let you do: estimate accumulation on repeated dosing, keep the concentration inside the therapeutic range, and relate concentration to response.

The simplest useful models are **compartmental**. A compartment is not an organ. It is a group of tissues that the drug reaches at a similar rate, treated as one well-mixed space. The **central compartment** is the blood together with the highly perfused organs.

![Three schematics. One compartment: a central box with an elimination arrow labelled K. Two compartments: a central box exchanging with a tissue box through arrows K12 and K21, with elimination K leaving the central box. Three compartments: a central box exchanging with two separate tissue boxes through K12, K21, K13 and K31, with elimination K leaving the central box; the two tissue boxes are not connected to each other.](../rework/figures/out/ch01-compartment-models.png)

*Figure 1.3 — One-, two- and three-compartment open models. Peripheral compartments exchange only with the central compartment, and elimination takes place only from the central compartment.*  
Original diagram, redrawn from the first edition pages 6 and 7 (original)

### The one-compartment open model

The one-compartment open model treats the whole body as a single space. "Open" means the drug leaves it — elimination never stops.

It rests on five assumptions, and every equation in Chapters 2 and 3 inherits them:

- **a.** The body is one central compartment, to which drug is added and from which it is eliminated.
- **b.** Once injected, the drug equilibrates with the tissues instantaneously. There is no distribution phase.
- **c.** Concentration is proportional to dose: the relationship is linear.
- **d.** Elimination is first order, so its rate depends on the blood concentration.
- **e.** A change in plasma level produces a proportional change in tissue and urine levels.

> **Watch the Units:** Assumption (d) is what makes K a **rate constant** rather than a rate. A first-order rate constant has units of reciprocal time (h⁻¹), because the rate itself (mg·h⁻¹) is already proportional to the amount. Write K in mg·h⁻¹ and you have written a zero-order rate, which is a different model — Chapter 10.

Assumption (b) fails most often. When it does, the drug needs a second compartment.

### Two and three compartments

In the **two-compartment open model** the drug distributes rapidly into the central compartment and slowly into a **peripheral (tissue) compartment**. Transfer between them is first order, governed by K₁₂ from central to tissue and K₂₁ from tissue to central. Elimination still happens only from the central compartment.

At time zero there is no drug in the tissue and the plasma concentration is at its peak. As drug moves outward the plasma level falls quickly — the **distribution phase**. Once the gradient reverses, the fall slows to the **elimination phase**. Chapter 4 separates the two.

The **three-compartment open model** adds a second peripheral compartment. Compartments 2 and 3 are not connected to each other. Each exchanges only with the central compartment, from which elimination takes place.

Drawing the model is not decoration. The diagram lets you write the differential equation for each compartment, shows the rate processes, and names every rate constant you will need.

> **Key Equation:** Equation 1.1 — total amount in the body
>
> $$D_B = C_p \times V_d$$
>
> where D_B is the total amount of drug in the body (mg), Cp the plasma concentration (mg·L⁻¹) and Vd the apparent volume of distribution (L). This is the bridge between what you can measure and what you want to know. Chapter 2 derives Vd and explains why it is *apparent*.

## 1.4 Choosing the Model

Always use the fewest compartments that describe the data adequately. A model with more will always fit better; that is not a reason to prefer it.

How many you observe depends on the route, the absorption rate, the sampling time, the number and timing of samples, and the sensitivity of the assay. Sample too late or too rarely and a distribution phase disappears.

The test is simple: plot Cp against time on semilog paper, sampling at short intervals early on.

- A *straight line* means one compartment.
- A *curved line* means two or more.

> **Worked Example:** Example 1.1 — reading a semilog plot
>
> A drug is given as an IV bolus. Plasma is sampled at 0.25, 0.5, 1, 2, 4 and 6 h. On semilog axes the six points fall on one straight line. A second drug, sampled at the same times, gives points that curve steeply for the first hour and then straighten.
>
> *Which model fits each drug, and what would happen if the first three samples had not been taken?*
>
> **Step 1 — the first drug.** One straight line on semilog axes means a single first-order process: the concentration falls by the same *fraction* in every equal interval. One compartment fits.
>
> **Step 2 — the second drug.** Two slopes mean two processes. The steep early phase is distribution into tissue; the shallow later phase is elimination. Two compartments fit.
>
> **Step 3 — the missing samples.** Drop the 0.25, 0.5 and 1 h points and only the shallow phase remains. It would look straight, and the drug would be assigned to one compartment.
>
> **Answer.** Drug 1: one compartment. Drug 2: two. Sampling too late hides a distribution phase, so the compartment count is a property of the study design as much as of the drug.

> **Why It Matters in Practice:** Choosing one compartment when the drug has two makes you underestimate the peak after a rapid infusion. For a narrow therapeutic range, that is the difference between a therapeutic level and a toxic one. It is why aminoglycoside monitoring specifies *when* to draw the sample.

## Key Takeaways
- Pharmacokinetics studies the rates of ADME. Biopharmaceutics studies what the product does before absorption begins.
- Bioavailability has two parts: rate and extent. tmax reflects rate; AUC reflects extent.
- The therapeutic range is the band between MEC and MTC. The therapeutic index is a ratio. They are different quantities.
- A compartment is a kinetic space, not an organ. The central compartment is blood plus the highly perfused organs.
- The one-compartment model assumes instantaneous distribution and first-order elimination.
- Use the fewest compartments that fit. A curved semilog plot means more than one, and what you see depends on the sampling design.

## Check Your Understanding

**Q1.** [LO1] Which statement describes biopharmaceutics rather than pharmacokinetics?
A) It calculates the elimination half-life from plasma data.
B) It studies how particle size affects the rate of absorption.
C) It predicts the concentration in the body at any time.
D) It measures the rate of renal excretion.

**Q2.** [LO2] Which parameter is the measure of the *extent* of drug absorption?
A) tmax
B) Cpmax
C) AUC
D) Ka

**Q3.** [LO3] A drug has TD50 = 400 mg and ED50 = 50 mg. Its MEC is 2 µg·mL⁻¹ and its MTC is 10 µg·mL⁻¹. What is its therapeutic index?
A) 8
B) 5
C) 2–10 µg·mL⁻¹
D) 0.2

**Q4.** [LO4] Which assumption of the one-compartment open model fails when a distribution phase is seen?
A) Instantaneous equilibrium with the surrounding tissues
B) First-order elimination
C) Linearity between dose and concentration
D) Proportional changes in tissue and urine levels

**Q5.** [LO2] The plasma concentration of a drug stays below its MEC after an oral dose. Which statement is correct?
A) The AUC must be zero.
B) The drug was not absorbed at all.
C) The drug is toxic.
D) The drug reached the circulation but produced no therapeutic effect.

**Q6.** [LO4] In the two-compartment model, elimination takes place from:
A) Both compartments equally
B) The central compartment only
C) The peripheral compartment only
D) Whichever compartment holds more drug

**Q7.** [LO4] A drug is sampled only at 6, 12 and 24 h after an IV bolus. The semilog plot is a straight line. What can you conclude?
A) The drug certainly follows a one-compartment model.
B) The drug certainly follows a two-compartment model.
C) A distribution phase may have been missed because sampling started late.
D) The assay was not sensitive enough.

**Q8.** [LO1] Bioavailability of an antacid is assessed by:
A) AUC after an intravenous dose
B) The cumulative amount excreted in urine
C) The plasma concentration at tmax
D) The effect measured at the site of action

**Q9.** [LO4] What does "open" mean in "one-compartment open model"?
A) The model has no fixed volume.
B) The drug undergoes continuous elimination.
C) The compartment exchanges with a tissue compartment.
D) Absorption is first order.

**Q10.** [LO2] Which set of units is correct for AUC?
A) mg·L⁻¹
B) h⁻¹
C) µg·h·mL⁻¹
D) L·h⁻¹

### Exercises

**E1.1** [LO2] A drug has an MEC of 4 µg·mL⁻¹ and an MTC of 12 µg·mL⁻¹. After an oral dose, Cpmax is 10 µg·mL⁻¹ at tmax = 2 h. State whether the dose is therapeutic, and give the therapeutic index on a concentration basis.

**E1.2** [LO2] The same drug is given at twice the dose. Predict what happens to Cpmax, to tmax and to AUC, and say which of the three you can predict with confidence from Chapter 1 alone.

**E1.3** [LO4] A drug has a plasma concentration of 5 mg·L⁻¹ and an apparent volume of distribution of 20 L. Calculate the total amount of drug in the body, showing the units at each step.

## Answers and Worked Solutions

**Q1. B** — Particle size is a property of the dosage form, and its effect on absorption rate is what biopharmaceutics studies. A, C and D are kinetic calculations on drug already in the body.

**Q2. C** — AUC is proportional to the amount reaching the circulation, so it measures extent. tmax and Ka describe rate. Cpmax depends on both, so it measures neither alone.

**Q3. A** — The therapeutic index is TD50/ED50 = 400/50 = *8*, a dimensionless ratio. Option C is the therapeutic *range*, the distractor this question exists to catch. Option B is MTC/MEC = 5, a concentration-based index, but the question gives TD50 and ED50.

**Q4. A** — A distribution phase is time spent distributing; assumption (b) says that time is zero. B, C and D can all still hold in a two-compartment drug.

**Q5. D** — AUC can be large while the peak stays below MEC; a slowly absorbed drug does this. So A and B are wrong, and nothing here suggests toxicity.

**Q6. B** — A defining feature of the model. The peripheral compartment exchanges through K₁₂ and K₂₁ but has no elimination pathway of its own.

**Q7. C** — By 6 h a distribution phase would be over, so the straight line describes only the terminal phase. A and B both claim certainty the data cannot support.

**Q8. D** — An antacid is not intended to reach the blood, so plasma and urine methods measure nothing useful. Its availability is assessed from acid neutralisation.

**Q9. B** — "Open" refers to elimination, not to the number of compartments. A closed model would retain the drug indefinitely.

**Q10. C** — AUC is a concentration multiplied by a time. A is a concentration, B is a first-order rate constant and D is a clearance.

---

**E1.1 — worked solution**

*Step 1 — is the dose therapeutic?* The therapeutic range is 4 to 12 µg·mL⁻¹, and Cpmax is 10 µg·mL⁻¹. Since 4 < 10 < 12, the peak sits inside the range.

*Step 2 — the ratio of the two limits.*

therapeutic concentration ratio = MTC / MEC = 12 µg·mL⁻¹ ÷ 4 µg·mL⁻¹ = *3*

The units cancel, as they must: a ratio of two concentrations is a pure number.

*Answer.* The dose is therapeutic, and the ratio of MTC to MEC is 3. The peak is only 2 µg·mL⁻¹ below the MTC, so there is little room for error, which is why such drugs are monitored.

*Do not call this the therapeutic index.* The therapeutic index is TD50/ED50, a ratio of two *doses* measured in populations, and Section 1.2 keeps the two apart deliberately. MTC/MEC is a ratio of two concentrations in one patient's plasma. The two often point the same way, but they are different measurements and neither can be computed from the other. This exercise gives concentrations, so it can only give the concentration ratio.

**E1.2 — worked solution**

*Cpmax.* Assumption (c) is linearity: concentration is proportional to dose. Doubling the dose *doubles Cpmax*, to 20 µg·mL⁻¹ — now above the MTC of E1.1.

*AUC.* Also proportional to dose, so it *doubles*.

*tmax.* tmax depends on Ka and K, and on neither the dose nor the volume. It is *unchanged* at 2 h. Chapter 7 derives this.

*Which can you predict with confidence?* Cpmax and AUC, because linearity is an assumption you were given. tmax needs Chapter 7. All three hold only while kinetics stay linear; if the doubled dose saturates an enzyme they all fail, which is Chapter 10.

**E1.3 — worked solution**

*Step 1 — choose the equation.* Equation 1.1: D_B = Cp × Vd.

*Step 2 — substitute, carrying units.*

D_B = 5 mg·L⁻¹ × 20 L

*Step 3 — cancel.* L⁻¹ × L = 1, leaving mg.

D_B = *100 mg*

*Check.* The answer is an amount, and it came out in mg. Divide instead of multiply and you get 0.25 mg·L⁻², which is not an amount of anything. Carrying units through is the cheapest error check in pharmacokinetics, and this book does it in every worked example.

## References
1. Shargel L, Yu ABC. *Applied Biopharmaceutics and Pharmacokinetics*. 8th ed. New York: McGraw Hill Medical; 2022.
2. Aulton ME, Taylor KMG, editors. *Aulton's Pharmaceutics: The Design and Manufacture of Medicines*. 6th ed. Edinburgh: Elsevier; 2021.


---

# Chapter 2: One Compartment, IV Bolus: Plasma Data

## Learning Objectives
By the end of this chapter you will be able to:
1. [LO1] Write the first-order elimination equation in exponential and logarithmic form, and identify each symbol.
2. [LO2] Calculate the elimination rate constant K and the half-life from two plasma concentrations or from a semilog plot.
3. [LO3] Define the apparent volume of distribution, calculate it by both available routes, and state what alters it.
4. [LO4] Calculate total body clearance from K and Vd, and give its units.
5. [LO5] Predict the fraction of a dose remaining at any time, and the duration of action after a change in dose.

## 2.1 One Compartment, One Equation

An intravenous bolus is the simplest case in this book. The whole dose enters the central compartment at once, so there is no absorption to model. If the body behaves as one compartment, only one process remains: elimination.

Chapter 1 gave the assumption that governs it. Elimination is **first order**, which means its rate is proportional to the amount of drug present:

dD_B/dt = −K · D_B

The minus sign says the amount is falling. K is the **elimination rate constant**, in reciprocal time. Integrating this between time zero and time t gives the working equations.

> **Key Equation:** Equation 2.1 — first-order decline
>
> In exponential form:
>
> $$D_B = D_B^0\, e^{-Kt} \qquad \text{and} \qquad C_p = C_p^0\, e^{-Kt}$$
>
> In logarithmic form:
>
> $$\log C_p = \log C_p^0 - \frac{Kt}{2.303}$$
>
> where Cp⁰ is the plasma concentration extrapolated back to time zero, and 2.303 converts natural logarithms to base 10. The two forms carry identical information [1]. The second is the useful one, because it is the equation of a straight line.

Dividing the amount equation by Vd gives the concentration equation, and this is legitimate only because assumption (c) of Chapter 1 holds: Vd is a constant.

## 2.2 Why the Plot Is Semilogarithmic

Plot Cp against time on ordinary axes and you get a curve. Nothing can be read from it directly. Plot log Cp against the same times and you get a straight line, because Equation 2.1 in logarithmic form is y = c + mx with:

- intercept = log Cp⁰
- slope = −K / 2.303

![Two plots side by side sharing the same data. On the left, linear axes show a falling curve from which no constant can be read. On the right, semilogarithmic axes show the same points on a straight line; the intercept is marked Cp zero equals 8.57 and the slope is annotated as minus K over 2.303, with K equal to 0.170 per hour and half-life 4.07 hours.](../rework/figures/out/ch02-semilog.png)

*Figure 2.1 — The same seven plasma concentrations after a 300 mg IV bolus, plotted on linear and on semilogarithmic axes. Only the semilogarithmic plot gives a straight line, from which Cp⁰ is read at the intercept and K from the slope.*  
Original diagram, drawn from the first edition Example 6 dataset, page 11 (original)

Semilog paper does the logarithm for you: the vertical axis is already spaced logarithmically, so you plot Cp itself and still read a straight line. This is why pharmacokinetic data are almost always shown this way.

> **Watch the Units:** The slope of a semilog plot is *not* K. It is −K/2.303. Forgetting the 2.303 inflates every half-life by a factor of 2.303, which turns a 4-hour drug into a 9-hour one. If you work in natural logarithms instead, the slope *is* −K and no conversion is needed. Decide which logarithm you are using before you start, and stay with it.

## 2.3 Half-Life

The **elimination half-life** (t½) is the time taken for the amount of drug in the body to fall by half. Setting Cp = Cp⁰/2 in Equation 2.1 and solving gives a result that does not contain the dose at all.

> **Key Equation:** Equation 2.2 — half-life
>
> $$t_{1/2} = \frac{0.693}{K}$$
>
> where 0.693 is ln 2. The relationship works both ways: K = 0.693 / t½.

Three consequences follow, and they are worth stating separately.

*First, t½ is independent of the dose.* Double the dose and the concentration at every time doubles, but the time to halve it is unchanged. This is the signature of a first-order process, and Chapter 10 shows what happens when it fails.

*Second, K and t½ are properties of the drug in that patient*, set by how the body clears it. A sustained-release formulation appears to lengthen the half-life, but it does so by slowing input, not elimination; Chapter 7 explains this as flip-flop kinetics.

*Third, half-lives can be counted instead of calculated.* Because each one removes half of what remains, the fraction left after n half-lives is 1/2ⁿ:

| Half-lives elapsed | Fraction remaining | Percent eliminated |
|---|---|---|
| 1 | 1/2 | 50% |
| 2 | 1/4 | 75% |
| 3 | 1/8 | 87.5% |
| 4 | 1/16 | 93.75% |
| 5 | 1/32 | 96.9% |
| 7 | 1/128 | 99.2% |
| 10 | 1/1024 | 99.9% |

Ten half-lives is the practical definition of "gone". Five is the practical definition of "steady state reached", and Chapter 5 uses it.

## 2.4 Apparent Volume of Distribution

Equation 1.1 defined the **apparent volume of distribution** (Vd) as the proportionality constant linking the amount of drug in the body to the plasma concentration. It is time to take the word *apparent* seriously.

Vd is not a physiological volume. It is the volume the drug would need to occupy if it were present everywhere at the concentration found in plasma. Consider 100 mg of drug in 1000 mL of fluid. If none of it binds anywhere, Cp is 0.1 mg·mL⁻¹ and Vd is 1000 mL, which is the real volume. Now add 1 g of charcoal that binds 99 mg of the drug. Only 1 mg stays in solution, Cp falls to 0.001 mg·mL⁻¹, and the calculation returns:

Vd = 100 mg ÷ 0.001 mg·mL⁻¹ = 100 000 mL

The fluid is still 1000 mL. The charcoal stands for tissue binding, and the 100-fold inflation of Vd is the whole point: a large Vd means the drug has left the plasma, not that the patient is large.

*Interpreting the number.* A low Vd, roughly 0.1 to 1 L·kg⁻¹, indicates a drug held in the plasma, usually by protein binding. Acidic, hydrophilic drugs such as the sulphonamides and aspirin behave this way. A high Vd, above about 1 L·kg⁻¹, indicates extensive tissue distribution, typical of basic lipophilic drugs such as the amphetamines.

*What changes Vd.* In one patient under stable conditions Vd behaves as a constant, which is why it can be used as a proportionality constant at all. It is not fixed for life. It changes most markedly in disease: renal dysfunction, liver cirrhosis, congestive heart failure and oedema all raise it by expanding total body water, while haemorrhage, diarrhoea and vomiting lower it by depleting body fluid. It also varies with age, with body composition, in pregnancy, and with anything that alters plasma protein binding. Treat Vd as a parameter that must be estimated for the patient in front of you [2].

> **Common Mistake:** Reporting Vd in litres alone invites comparison between patients of different sizes. Normalise it. The usual forms are litres per kilogram of body weight, or litres per 1.73 m² of body surface area. A Vd of 35 L means one thing in a 50 kg woman and another in a 90 kg man.

## 2.5 Two Ways to Find Vd

Both routes start from an intravenous dose, because only then is the amount entering the body known exactly.

*Route 1 — from the extrapolated intercept.* Read Cp⁰ off the semilog plot and divide:

Vd = D_B⁰ / Cp⁰

This needs early samples. Extrapolating from points collected after distribution is complete gives a Cp⁰ that is too low and a Vd that is too high.

*Route 2 — from the area under the curve.* Integrating the elimination equation over all time gives:

Vd = D_B⁰ / (K · AUC)

This route needs no extrapolation, and Chapter 9 generalises it to drugs that do not follow any compartment model.

## 2.6 Clearance

**Total body clearance** (Cl) is the volume of plasma completely cleared of drug per unit time, and its units are volume per time. It says nothing about mechanism: renal excretion, hepatic metabolism or both may be responsible. Chapter 6 defines it fully and separates the routes. For a first-order process it is constant, independent of concentration.

> **Key Equation:** Equation 2.3 — clearance from K and Vd
>
> $$Cl = K \cdot V_d = \frac{0.693\, V_d}{t_{1/2}}$$
>
> Clearance is therefore inversely proportional to half-life at constant Vd. Doubling clearance halves the half-life.

Read Equation 2.3 in the right direction. Clearance and Vd are the physiological quantities: clearance is set by organ function, Vd by binding and partitioning. K and t½ are what those two produce. A rising half-life in a patient means clearance has fallen, or Vd has risen, and the equation cannot tell you which on its own.

> **Worked Example:** Example 2.1 — a complete IV bolus analysis
>
> A 50 kg woman receives a single intravenous dose of an antibacterial drug at 6 mg·kg⁻¹. Plasma concentrations are:
>
> | t (h) | 0.25 | 0.50 | 1.0 | 3.0 | 6.0 | 12.0 | 18.0 |
> |---|---|---|---|---|---|---|---|
> | Cp (µg·mL⁻¹) | 8.21 | 7.87 | 7.23 | 5.15 | 3.09 | 1.11 | 0.40 |
>
> Find K, t½, Cp⁰, Vd and Cl. Then find the time the concentration stays above 2 µg·mL⁻¹, and the extra time gained by doubling the dose.
>
> *Step 1 — the dose.* 6 mg·kg⁻¹ × 50 kg = 300 mg.
>
> *Step 2 — K from any two points on the line.* Using natural logarithms and the first and last points:
>
> K = [ln 8.21 − ln 0.40] / (18.0 − 0.25) = (2.1054 + 0.9163) / 17.75 = 0.170 h⁻¹
>
> Repeat with the 1 h and 18 h points and you get 0.170 h⁻¹ again. That agreement is the evidence that one compartment fits.
>
> *Step 3 — half-life.* t½ = 0.693 / 0.170 = 4.07 h.
>
> *Step 4 — back-extrapolate to Cp⁰.*
>
> ln Cp⁰ = ln 8.21 + (0.170 × 0.25) = 2.1054 + 0.0426 = 2.1480, so Cp⁰ = 8.57 µg·mL⁻¹
>
> *Step 5 — Vd, carrying units.* Convert the concentration first: 8.57 µg·mL⁻¹ = 8.57 mg·L⁻¹.
>
> Vd = 300 mg ÷ 8.57 mg·L⁻¹ = 35.0 L, which is 0.70 L·kg⁻¹
>
> *Step 6 — clearance.* Cl = K · Vd = 0.170 h⁻¹ × 35.0 L = 5.96 L·h⁻¹, or 99 mL·min⁻¹.
>
> *Step 7 — duration above 2 µg·mL⁻¹.*
>
> t = ln(8.57 / 2) ÷ 0.170 = 1.455 ÷ 0.170 = 8.6 h
>
> *Step 8 — double the dose.* Cp⁰ becomes 17.14 µg·mL⁻¹, and the same calculation gives 12.6 h. The gain is 4.07 h.
>
> *Answer.* K = 0.170 h⁻¹, t½ = 4.07 h, Vd = 35.0 L (0.70 L·kg⁻¹), Cl = 5.96 L·h⁻¹. The concentration stays above 2 µg·mL⁻¹ for 8.6 h, and doubling the dose adds 4.07 h.
>
> *Note what Step 8 shows.* The gain equals exactly one half-life, and it always will. Doubling a dose buys one half-life of extra duration, no matter what the drug is. Doubling it again buys one more. Duration grows by addition while the dose grows by multiplication, which is why escalating the dose is a poor way to extend cover.

> **Why It Matters in Practice:** Step 8 is the argument for shortening the dosing interval rather than raising the dose. Four doublings of an aminoglycoside dose would add only four half-lives of cover, while multiplying the peak sixteenfold and taking it far above the minimum toxic concentration. Chapter 8 makes this quantitative.

## Key Takeaways
- First-order elimination gives Cp = Cp⁰·e^(−Kt). On semilog axes this is a straight line of slope −K/2.303.
- t½ = 0.693/K, and it does not depend on the dose.
- After n half-lives, 1/2ⁿ of the dose remains. Ten half-lives is effectively complete elimination.
- Vd is apparent, not anatomical. A high value means tissue binding, not a large patient.
- Vd is stable in a stable patient, but changes with fluid status, disease, age, body composition and protein binding.
- Vd can be found from D₀/Cp⁰ or from D₀/(K·AUC). The second needs no extrapolation.
- Cl = K·Vd. Clearance and Vd are the physiological quantities; K and t½ follow from them.

## Check Your Understanding

**Q1.** [LO1] In the equation log Cp = log Cp⁰ − Kt/2.303, the slope of the line is:
A) −K
B) −K/2.303
C) −0.693/K
D) −2.303K

**Q2.** [LO2] A drug has an elimination half-life of 6 h and follows first-order kinetics. What percentage of a single IV dose is lost in 24 h?
A) 75%
B) 87.5%
C) 96.9%
D) 93.75%

**Q3.** [LO3] A drug has an apparent volume of distribution of 4 L·kg⁻¹. This most likely means the drug is:
A) Extensively bound to plasma proteins
B) Extensively distributed into tissues
C) Confined to the plasma water
D) Eliminated unusually quickly

**Q4.** [LO4] Which set of units is correct for total body clearance?
A) L·h⁻¹
B) h⁻¹
C) mg·L⁻¹
D) L

**Q5.** [LO2] Serum concentrations 2 h and 5 h after an IV bolus are 1.2 and 0.3 µg·mL⁻¹. The half-life is:
A) 0.75 h
B) 3.0 h
C) 1.5 h
D) 4.5 h

**Q6.** [LO3] Vd is described as *apparent* because:
A) It is measured with poor precision.
B) It changes continuously during elimination.
C) It need not correspond to any real body volume.
D) It can only be estimated after oral dosing.

**Q7.** [LO5] Doubling an IV bolus dose of a drug that follows linear kinetics will:
A) Double Cp⁰ and double the half-life
B) Double Cp⁰ and leave the half-life unchanged
C) Leave Cp⁰ unchanged and double the half-life
D) Double both the clearance and Cp⁰

**Q8.** [LO3] Which change would be expected to *decrease* the apparent volume of distribution?
A) Congestive heart failure with oedema
B) Liver cirrhosis with ascites
C) Renal dysfunction with fluid retention
D) Severe diarrhoea and vomiting

**Q9.** [LO4] Clearance is 6 L·h⁻¹ and Vd is 30 L. The half-life is:
A) 3.5 h
B) 0.2 h
C) 5.0 h
D) 8.7 h

**Q10.** [LO5] A patient's half-life for a drug has doubled since the previous admission. From this alone you can conclude that:
A) Clearance has halved.
B) Vd has doubled.
C) Either clearance has fallen or Vd has risen, and the half-life cannot distinguish them.
D) The drug now follows zero-order kinetics.

### Exercises

**E2.1** [LO2] A new drug is given as a single 200 mg IV dose to an 80 kg man. After 6 h the blood concentration is 1.5 mg per 100 mL. The apparent Vd is 10% of body weight. Calculate the total amount of drug remaining in the body at 6 h, the elimination rate constant and the half-life.

**E2.2** [LO3] A 50 kg woman receives a single IV dose of a new antibiotic at 20 mg·kg⁻¹. Plasma concentrations are 4.2, 3.5, 2.5, 1.25, 0.31 and 0.08 µg·mL⁻¹ at 0.25, 0.5, 1, 2, 4 and 6 h. Determine K, t½, Cp⁰, Vd and total clearance, and comment on the size of the clearance you obtain.

**E2.3** [LO5] A drug has a half-life of 8 h and first-order elimination. A 62 kg woman is given 600 mg by rapid IV injection, and the apparent Vd is 400 mL·kg⁻¹. Calculate the percentage of the dose eliminated in 24 h and the expected plasma concentration at 24 h.

## Answers and Worked Solutions

**Q1. B** — The logarithmic form divides Kt by 2.303 to convert from natural to base-10 logarithms. Option A is the slope when natural logarithms are plotted instead.

**Q2. D** — 24 h is four half-lives, so 1/16 remains. That is 6.25% remaining and 93.75% lost. Option B is three half-lives and C is five.

**Q3. B** — A Vd far above total body water means the drug has partitioned into tissue. Option A would give a *low* Vd, because protein-bound drug is held in the plasma and raises Cp.

**Q4. A** — Clearance is a volume per unit time. B is a first-order rate constant, C a concentration and D a volume.

**Q5. C** — K = ln(1.2/0.3) ÷ 3 h = 1.386 ÷ 3 = 0.462 h⁻¹, so t½ = 0.693 ÷ 0.462 = 1.5 h. Equivalently, the concentration quartered in 3 h, which is two half-lives.

**Q6. C** — It is the volume that would be needed if the drug were everywhere at the plasma concentration. The charcoal example gives 100 L for a 1 L system.

**Q7. B** — Linearity makes concentration proportional to dose, so Cp⁰ doubles. The half-life depends on K alone, which is unchanged. Clearance is also unchanged, ruling out D.

**Q8. D** — Diarrhoea and vomiting deplete body fluid and contract the distribution space. A, B and C all expand total body water and raise Vd.

**Q9. A** — Cl = K·Vd, so K = 6 ÷ 30 = 0.2 h⁻¹, and t½ = 0.693 ÷ 0.2 = 3.47 h. Option B is K itself, not the half-life.

**Q10. C** — t½ = 0.693·Vd/Cl, so a doubled half-life is consistent with halved clearance, doubled Vd, or any combination. A and B each assert one cause without evidence. This is why clearance and Vd are estimated separately.

---

**E2.1 — worked solution**

*Step 1 — Vd.* 10% of 80 kg is 8 kg of fluid, which is 8 L.

*Step 2 — convert the concentration.* 1.5 mg per 100 mL = 15 mg·L⁻¹.

*Step 3 — amount remaining at 6 h.*

D_B = Cp × Vd = 15 mg·L⁻¹ × 8 L = 120 mg

*Step 4 — K from the amount lost.* The dose was 200 mg and 120 mg remains.

K = ln(200/120) ÷ 6 h = 0.5108 ÷ 6 = 0.0851 h⁻¹

*Step 5 — half-life.* t½ = 0.693 ÷ 0.0851 = 8.1 h.

*Answer.* 120 mg remains, K = 0.0851 h⁻¹ and t½ = 8.1 h.

*Check.* 6 h is a little under one half-life, and indeed a little under half the dose has gone. The arithmetic is consistent with the physiology.

**E2.2 — worked solution**

*Step 1 — the dose.* 20 mg·kg⁻¹ × 50 kg = 1000 mg.

*Step 2 — K.* Using the 1 h and 4 h points:

K = [ln 2.5 − ln 0.31] ÷ 3 h = (0.9163 + 1.1712) ÷ 3 = 0.696 h⁻¹

The 2 h and 6 h points give 0.686 h⁻¹. Take K = 0.693 h⁻¹.

*Step 3 — half-life.* t½ = 0.693 ÷ 0.693 = 1.00 h exactly.

*Step 4 — Cp⁰.* ln Cp⁰ = ln 4.2 + (0.693 × 0.25) = 1.4351 + 0.1733 = 1.6084, so Cp⁰ = 5.0 µg·mL⁻¹.

*Step 5 — Vd.* 5.0 µg·mL⁻¹ = 5.0 mg·L⁻¹.

Vd = 1000 mg ÷ 5.0 mg·L⁻¹ = 200 L, which is 4.0 L·kg⁻¹

*Step 6 — clearance.* Cl = 0.693 h⁻¹ × 200 L = 138.6 L·h⁻¹, which is 2310 mL·min⁻¹.

*Comment.* The Vd of 4 L·kg⁻¹ is high but ordinary for a lipophilic drug. The clearance is not ordinary. Hepatic blood flow is about 1500 mL·min⁻¹ and renal plasma flow about 650 mL·min⁻¹, so no single organ can clear 2310 mL·min⁻¹. Such a value points to elimination at more than one site, or to elimination in blood or tissue rather than in an organ. Always test a calculated clearance against physiological flow. The arithmetic here is correct, and it is the arithmetic that tells you the simple picture is incomplete.

**E2.3 — worked solution**

*Step 1 — count the half-lives.* 24 h ÷ 8 h = 3 half-lives.

*Step 2 — fraction remaining.* 1/2³ = 1/8 = 12.5%, so 87.5% has been eliminated.

*Step 3 — amount remaining.* 12.5% of 600 mg = 75 mg.

*Step 4 — Vd.* 400 mL·kg⁻¹ × 62 kg = 24 800 mL = 24.8 L.

*Step 5 — concentration at 24 h.*

Cp = 75 mg ÷ 24.8 L = 3.02 mg·L⁻¹

*Answer.* 87.5% eliminated, and Cp at 24 h is 3.02 mg·L⁻¹ (3.02 µg·mL⁻¹).

*Check.* Note that Steps 1 and 2 never used the dose or the volume. Counting half-lives gives the *fraction* directly, and the dose and Vd are needed only to turn that fraction into an amount and a concentration.

## References
1. Shargel L, Yu ABC. *Applied Biopharmaceutics and Pharmacokinetics*. 8th ed. New York: McGraw Hill Medical; 2022.
2. Rowland M, Tozer TN. *Clinical Pharmacokinetics and Pharmacodynamics: Concepts and Applications*. 5th ed. Philadelphia: Wolters Kluwer; 2019.


---

# Chapter 3: One Compartment, IV Bolus: Urine Data

## Learning Objectives
By the end of this chapter you will be able to:
1. [LO1] Explain why urine data can substitute for plasma data, and state the condition that must hold.
2. [LO2] Determine K and t½ by the urinary excretion rate method, and say why midpoint time is used.
3. [LO3] Determine K, t½ and Du∞ by the sigma-minus method.
4. [LO4] Choose between the two methods for a given study, giving the reason.
5. [LO5] List the conditions under which a urine collection yields valid kinetic data.

## 3.1 Why Collect Urine at All

Plasma sampling is invasive; urine collection is not. That matters in volunteers, in children and in long studies. For a drug excreted largely unchanged by the kidney, the urine record mirrors the plasma record. As the amount in the body falls, the cumulative amount in the urine rises, and the two curves are reflections of one another [1].

The mirror is exact only under one condition. Renal excretion must itself be first order, and so proportional to the amount of drug in the body:

dDu/dt = Ke · D_B

Here Du is the **cumulative amount excreted unchanged** in urine and **Ke** is the **renal excretion rate constant**. Ke is not the same as K. The total elimination rate constant covers every route of loss, so:

K = Ke + Knr

where **Knr** is the **non-renal elimination rate constant**, mostly metabolism. The ratio of the two gives a quantity used throughout Chapters 6 and 13.

> **Key Equation:** Equation 3.1 — fraction excreted unchanged
>
> $$f_e = \frac{D_u^\infty}{D_B^0} = \frac{K_e}{K}$$
>
> where Du∞ is the total amount ultimately recovered unchanged and D_B⁰ is the intravenous dose. A drug with fe = 1 is cleared entirely by renal excretion of unchanged drug. A drug with fe = 0.1 loses 90% of the dose by other routes.

Note the consequence. Urine data give K, the *total* elimination rate constant, not Ke. Ke follows only once fe is known, and fe needs the dose.

## 3.2 The Urinary Excretion Rate Method

Substituting the first-order decline of D_B from Chapter 2 into the excretion equation gives the rate of appearance of drug in urine at any time.

> **Key Equation:** Equation 3.2 — excretion rate
>
> $$\frac{dD_u}{dt} = K_e\, D_B^0\, e^{-Kt}$$
>
> and in logarithmic form:
>
> $$\log \frac{dD_u}{dt} = \log\left(K_e\, D_B^0\right) - \frac{Kt}{2.303}$$

Read the second line carefully, because it contains the point of the method. The *slope* carries K, the total elimination rate constant. The *intercept* carries Ke·D_B⁰. Plot the excretion rate on semilog axes against time and both constants fall out of one straight line.

In practice the rate is never measured directly. Urine is collected over intervals, each yielding an amount ΔDu over a time Δt. The ratio ΔDu/Δt is the *average* rate over that interval, plotted as an estimate of the instantaneous rate.

## 3.3 Why Midpoint Time

An average rate over an interval is not the rate at the end of the interval. It is closest to the rate somewhere in the middle. Plot ΔDu/Δt against the time at the *end* of each collection and the points curve. Plot them against the **midpoint time** of each interval and they fall on a line.

![Two semilogarithmic plots. On the left, urinary excretion rate against time: filled points plotted at interval midpoints lie on a straight line, while open points plotted at end-of-interval times curve above it and flatten the slope. On the right, the amount remaining to be excreted against time: filled points using Du infinity of 1000 mg lie on a straight line from an intercept of 1000, while open points using 984 mg fall away below the line at the late times.](../rework/figures/out/ch03-urine-methods.png)

*Figure 3.1 — The two ways of reading urine data, both applied to the Example 3.1 collection. Filled points are plotted correctly; open points show the characteristic error of each method — end-of-interval time on the left, and an underestimated Du∞ on the right.*  
Original diagram, drawn from the first edition Example 8 dataset, page 16 (original)

> **Common Mistake:** Plotting the excretion rate against end-of-interval time is the commonest error in this calculation. It does not produce an obviously wrong answer. It produces a gently curved plot, from which a reader will happily draw a line and report a half-life that is too long. Tabulate the midpoint time as its own column before you plot anything.

The midpoint is itself an approximation, and it worsens as intervals lengthen. Across an interval longer than about one half-life the average rate exceeds the true midpoint rate, and the late points drift above the line. Collect frequently while the concentration is falling fast.

## 3.4 The Sigma-Minus Method

The second method avoids rates altogether. Integrating Equation 3.2 from zero to t gives the cumulative amount excreted:

Du = (Ke · D_B⁰ / K) · (1 − e^(−Kt))

At infinite time the exponential vanishes, so Du∞ = Ke·D_B⁰/K. Substituting that back and rearranging isolates a quantity that decays as cleanly as the plasma concentration does.

> **Key Equation:** Equation 3.3 — sigma-minus
>
> $$D_u^\infty - D_u = D_u^\infty\, e^{-Kt}$$
>
> and in logarithmic form:
>
> $$\log\left(D_u^\infty - D_u\right) = \log D_u^\infty - \frac{Kt}{2.303}$$

The term (Du∞ − Du) is the **amount remaining to be excreted**, abbreviated ARE. The method is named for the sigma, the summation, that produces the cumulative Du.

The plot of log ARE against time is a straight line of slope −K/2.303 and intercept log Du∞. Notice that ordinary time is used here, not the midpoint. ARE is a quantity at an instant, not an average over an interval.

> **Watch the Units:** ARE is an amount, in milligrams, not a rate. The excretion-rate plot has milligrams per hour on its vertical axis; the sigma-minus plot has milligrams. Both slopes are −K/2.303 and both give the same half-life, but the intercepts mean different things: Ke·D_B⁰ in the first, Du∞ in the second.

The method has one hard requirement, and it is a real one. Du∞ must be known before a single point can be plotted, because every ARE value is a subtraction from it.

> **Common Mistake:** Du∞ is the amount excreted at infinite time, not the last cumulative value in your table. If collection stopped at six half-lives, that last value is about 98% of Du∞. Using it as Du∞ forces the final ARE to zero and makes the ones before it far too small. The late points then bend sharply downwards and the fitted K comes out too large.

## 3.5 Choosing Between the Two Methods

| | Urinary excretion rate method | Sigma-minus method |
|---|---|---|
| Knowledge of Du∞ | Not required | Required, and a small error in it corrupts every point |
| One missing sample | Loses that one point; the rest stand | Invalidates the cumulative total, and so every later point |
| Scatter from incomplete bladder emptying | Shows directly as scatter about the line | Damped by cumulation, so the plot looks better than the data are |
| Order of elimination | Works for zero-order and first-order elimination | First-order elimination only |
| Ke | Obtainable from the intercept | Not obtainable |

Two entries that look like advantages of the sigma-minus method are one property seen twice. Cumulation smooths the data, and smoothing hides experimental error rather than removing it. A tidy sigma-minus plot is therefore not evidence of a careful collection. The excretion-rate plot is more honest about sample quality, at the cost of looking worse.

## 3.6 When Urine Data Can Be Trusted

Seven conditions must hold before a urine collection supports a kinetic calculation.

1. At least 20% of the dose must be excreted unchanged. Below that, the quantity measured is too small a fraction of the dose to be reliable.
2. Collection must continue until most of the drug is out: seven half-lives for 99%, ten for 99.9%.
3. Sampling must be frequent, especially early, or the curve is undefined where it is steepest.
4. The bladder must be emptied completely at each collection. Otherwise drug is carried into the next interval and the whole record is displaced.
5. Urinary pH and volume must be taken into account, since both can alter the excretion rate of an ionisable drug.
6. The assay must be specific for the intact drug, so that a metabolite is not counted as parent. HPLC is the usual choice.
7. Analysis must allow for between-subject variation. Two-way analysis of variance is appropriate; a Student t-test is not, because it ignores the subject as a source of variation.

Condition 4 deserves emphasis, because it is the one the subject controls rather than the investigator [2].

> **Worked Example:** Example 3.1 — the same drug, seen through the urine
>
> A 50 kg woman receives a single IV dose of an antibiotic at 20 mg·kg⁻¹. Urine is collected and the amount of intact drug in each collection is:
>
> | Collection ending at (h) | 0.25 | 0.50 | 1.0 | 2.0 | 4.0 | 6.0 |
> |---|---|---|---|---|---|---|
> | Amount in that collection (mg) | 160 | 140 | 200 | 250 | 188 | 46 |
>
> Determine K and t½ by both methods, and find fe.
>
> *Step 1 — the dose.* 20 mg·kg⁻¹ × 50 kg = 1000 mg.
>
> *Step 2 — build the table.* Interval length and midpoint must be worked out before anything is plotted.
>
> | Interval (h) | Δt (h) | Midpoint (h) | ΔDu (mg) | ΔDu/Δt (mg·h⁻¹) | Cumulative Du (mg) | ARE = 1000 − Du (mg) |
> |---|---|---|---|---|---|---|
> | 0–0.25 | 0.25 | 0.125 | 160 | 640 | 160 | 840 |
> | 0.25–0.50 | 0.25 | 0.375 | 140 | 560 | 300 | 700 |
> | 0.50–1.0 | 0.50 | 0.75 | 200 | 400 | 500 | 500 |
> | 1.0–2.0 | 1.0 | 1.5 | 250 | 250 | 750 | 250 |
> | 2.0–4.0 | 2.0 | 3.0 | 188 | 94 | 938 | 62 |
> | 4.0–6.0 | 2.0 | 5.0 | 46 | 23 | 984 | 16 |
>
> *Step 3 — where 1000 mg came from.* The collections total 984 mg, which is 98.4% of the dose. That is exactly what a first-order process leaves after six half-lives, so the drug is excreted entirely unchanged and Du∞ is the dose itself, 1000 mg. Using 984 mg as Du∞ would force the last ARE to zero and ruin the plot.
>
> *Step 4 — excretion rate method.* Take two widely separated midpoints.
>
> K = [ln 640 − ln 23] ÷ (5.0 − 0.125) = (6.461 − 3.135) ÷ 4.875 = 0.682 h⁻¹
>
> *Step 5 — sigma-minus method.* Take two widely separated times.
>
> K = [ln 840 − ln 62] ÷ (4.0 − 0.25) = (6.733 − 4.127) ÷ 3.75 = 0.695 h⁻¹
>
> *Step 6 — half-life.* Taking K = 0.693 h⁻¹, t½ = 0.693 ÷ 0.693 = 1.00 h.
>
> *Step 7 — fe and Ke.*
>
> fe = Du∞ / D_B⁰ = 1000 mg ÷ 1000 mg = 1.00, so Ke = fe × K = 0.693 h⁻¹
>
> *Answer.* K = 0.693 h⁻¹, t½ = 1.00 h, Du∞ = 1000 mg, fe = 1.00 and Ke = K = 0.693 h⁻¹.
>
> *Two checks worth making.* The ARE column halves at 1 h, 2 h, 3 h and 4 h, which is the half-life read straight off the table. And this is the same drug as Exercise E2.2 of Chapter 2, where plasma data on the same 50 kg woman at the same 20 mg·kg⁻¹ dose also gave t½ = 1.00 h. Plasma and urine agree, as they must when fe = 1.

> **Why It Matters in Practice:** Renal impairment reduces Ke but not Knr. For a drug with fe near 1, losing renal function removes almost the whole elimination pathway, the half-life rises steeply, and the dose must be cut. For a drug with fe near 0 the same loss changes little. Knowing fe is therefore the first step in deciding whether a drug needs renal dose adjustment at all, and it comes straight out of the calculation above.

## Key Takeaways
- Urine data give K, the total elimination rate constant, because the amount in the body drives excretion.
- Ke comes only from fe = Du∞/D_B⁰, which needs the dose.
- The excretion-rate plot is log(ΔDu/Δt) against *midpoint* time: slope −K/2.303, intercept Ke·D_B⁰.
- The sigma-minus plot is log(Du∞ − Du) against ordinary time: slope −K/2.303, intercept Du∞.
- Sigma-minus needs Du∞ and collapses if a sample is lost. The rate method needs neither but shows more scatter.
- Cumulation smooths the sigma-minus plot. A smooth plot is not evidence of a good collection.
- Urine data are valid only if at least 20% is excreted unchanged, collection runs to seven half-lives or more, and the bladder is emptied completely each time.

## Check Your Understanding

**Q1.** [LO1] The slope of a urinary excretion rate plot gives:
A) The renal excretion rate constant Ke
B) The total elimination rate constant K
C) The non-renal rate constant Knr
D) The fraction excreted unchanged

**Q2.** [LO2] The excretion rate is plotted against midpoint time rather than end-of-interval time because:
A) Midpoint time gives a steeper and therefore more precise slope.
B) The intercept is meaningless if end-of-interval time is used.
C) Bladder emptying is most complete at the midpoint of an interval.
D) ΔDu/Δt is an average rate over the interval, not the rate at its end.

**Q3.** [LO3] In the sigma-minus method, the intercept of the line gives:
A) Du∞
B) Ke·D_B⁰
C) The elimination rate constant
D) The fraction excreted unchanged

**Q4.** [LO4] A study loses one urine collection through a missed void. Which method is more seriously affected?
A) The excretion rate method, because the rate for that interval is unknown
B) Neither, because both use the same slope
C) The sigma-minus method, because every subsequent cumulative total is wrong
D) Both equally, because both depend on the total recovered

**Q5.** [LO3] A drug fits the equation Du∞ − Du = 50 e^(−0.2t), with Du∞ in mg and t in hours. The half-life is:
A) 0.2 h
B) 3.47 h
C) 5.0 h
D) 50 h

**Q6.** [LO1] A drug has fe = 0.15. This means:
A) Renal excretion is the main route of elimination.
B) 15% of an oral dose is absorbed.
C) 15% of the dose is recovered in urine as unchanged drug.
D) The renal excretion rate constant is 0.15 h⁻¹.

**Q7.** [LO5] Urine data are generally unsuitable for kinetic analysis when:
A) The drug has a short half-life.
B) The drug is given intravenously.
C) Collections are made every hour.
D) Less than 20% of the dose is excreted unchanged.

**Q8.** [LO3] A student uses the last cumulative amount collected, at six half-lives, as Du∞. The reported K will be:
A) Too large, because the late ARE values come out too small
B) Too small, because the late ARE values come out too large
C) Unaffected, because Du∞ affects only the intercept
D) Correct only if the drug is excreted entirely unchanged

**Q9.** [LO4] Which one of these can the sigma-minus method *not* provide?
A) The half-life
B) Ke
C) The total elimination rate constant
D) Du∞

**Q10.** [LO2] For a drug eliminated by zero-order kinetics, the appropriate method is:
A) Sigma-minus only
B) Either method equally
C) The urinary excretion rate method
D) Neither, since urine data require first-order elimination

### Exercises

**E3.1** [LO3] Urine data for an antibiotic fit the equation Du∞ − Du = 50 e^(−0.2t), with Du∞ in mg and t in hours. Determine Du∞, K and t½, and state how long collection must continue to recover 99% of the recoverable drug.

**E3.2** [LO1] A 400 mg IV dose is given and 120 mg of intact drug is eventually recovered in urine. The half-life measured from plasma is 5 h. Calculate fe, Ke and Knr, then predict the half-life in a patient whose renal function is so reduced that Ke falls to one tenth of normal.

**E3.3** [LO2] Using the table in Example 3.1, calculate the excretion rate and midpoint time for the 2.0–4.0 h interval. Then pair that point with the 0.50–1.0 h point and calculate K twice: once with midpoint times and once with end-of-interval times. Report how much the estimated half-life changes.

## Answers and Worked Solutions

**Q1. B** — Excretion is driven by the amount in the body, which falls with the total rate constant K. Ke appears in the intercept term Ke·D_B⁰, not in the slope.

**Q2. D** — ΔDu/Δt is the mean rate across the interval, and the mean of a falling exponential is matched best near the middle. Using the end time places every point too late and bends the plot.

**Q3. A** — Setting t = 0 in Equation 3.3 gives ARE = Du∞. Option B is the intercept of the excretion rate plot instead.

**Q4. C** — The sigma-minus method depends on a running total, so one missing amount displaces every total after it. The excretion rate method loses only the affected point.

**Q5. B** — Comparing with Du∞·e^(−Kt) gives K = 0.2 h⁻¹, so t½ = 0.693 ÷ 0.2 = 3.47 h. Option A is K itself and D is Du∞.

**Q6. C** — fe is the fraction of the dose recovered unchanged. At 0.15 the drug is cleared mainly by other routes, which rules out A. Option D confuses a fraction with a rate constant.

**Q7. D** — Below about 20% the measured amount is too small a fraction of the dose for the calculation to be reliable. A short half-life is no obstacle provided collections are frequent enough.

**Q8. A** — The late ARE values are computed as small differences, so understating Du∞ shrinks them disproportionately. Those points drop below the line and steepen it, raising K. Option C fails because Du∞ enters every ARE value, not just the intercept.

**Q9. B** — The sigma-minus plot contains no term in Ke: its intercept is Du∞ and its slope is −K/2.303. Ke can still be found afterwards from fe, but not from the plot.

**Q10. C** — The excretion rate method assumes nothing about the order, since it plots the observed rate. Sigma-minus is derived from the first-order integral and fails for zero order.

---

**E3.1 — worked solution**

*Step 1 — match the equation to the general form.* Equation 3.3 is Du∞ − Du = Du∞·e^(−Kt). Comparing term by term:

Du∞ = 50 mg    and    K = 0.2 h⁻¹

*Step 2 — half-life.*

t½ = 0.693 ÷ 0.2 h⁻¹ = 3.47 h

*Step 3 — time to recover 99%.* Recovering 99% leaves 1% remaining.

t = ln(100) ÷ 0.2 h⁻¹ = 4.605 ÷ 0.2 = 23.0 h

*Answer.* Du∞ = 50 mg, K = 0.2 h⁻¹, t½ = 3.47 h, and collection must run about 23 h.

*Check.* 23.0 h ÷ 3.47 h = 6.6 half-lives, consistent with the rule of thumb that 99% takes about seven.

**E3.2 — worked solution**

*Step 1 — fe.*

fe = Du∞ / D_B⁰ = 120 mg ÷ 400 mg = 0.30

*Step 2 — K from the half-life.*

K = 0.693 ÷ 5 h = 0.1386 h⁻¹

*Step 3 — split K into its two parts.*

Ke = fe × K = 0.30 × 0.1386 = 0.0416 h⁻¹

Knr = K − Ke = 0.1386 − 0.0416 = 0.0970 h⁻¹

*Step 4 — the impaired patient.* Knr is unchanged, and Ke falls to one tenth.

K' = 0.0970 + (0.0416 ÷ 10) = 0.0970 + 0.0042 = 0.1012 h⁻¹

t½' = 0.693 ÷ 0.1012 = 6.85 h

*Answer.* fe = 0.30, Ke = 0.0416 h⁻¹, Knr = 0.0970 h⁻¹, and the half-life rises from 5.0 h to 6.85 h.

*Comment.* Renal function fell by 90% and the half-life rose by only 37%, because 70% of elimination never used the kidney. Repeat the calculation with fe = 0.9 and the half-life rises to about 25 h instead. This is why fe, not renal function alone, decides whether a drug needs dose adjustment.

**E3.3 — worked solution**

*Step 1 — the interval.* From 2.0 to 4.0 h, Δt = 2.0 h and ΔDu = 188 mg.

ΔDu/Δt = 188 mg ÷ 2.0 h = 94 mg·h⁻¹

*Step 2 — the two candidate times.* Midpoint = (2.0 + 4.0)/2 = 3.0 h. End of interval = 4.0 h.

*Step 3 — K using midpoint times.* Pair it with the 0.50–1.0 h point, whose rate is 400 mg·h⁻¹ at a midpoint of 0.75 h.

K = [ln 400 − ln 94] ÷ (3.0 − 0.75) = (5.991 − 4.543) ÷ 2.25 = 0.644 h⁻¹

*Step 4 — K using end-of-interval times.* The same two rates would now be plotted at 1.0 h and 4.0 h.

K = [ln 400 − ln 94] ÷ (4.0 − 1.0) = 1.448 ÷ 3.0 = 0.483 h⁻¹

*Step 5 — convert both to half-lives.*

From midpoints: t½ = 0.693 ÷ 0.644 = 1.08 h. From end times: t½ = 0.693 ÷ 0.483 = 1.44 h.

*Answer.* The rate is 94 mg·h⁻¹ at a midpoint of 3.0 h. Using end-of-interval time stretches the time axis, flattens the slope and inflates the half-life from 1.08 h to 1.44 h, an error of about a third.

*Why the error grows with interval length.* The displacement is Δt/2 for every point, so short early intervals barely move while long late ones shift most. The plot never looks broken — only slightly curved — which is what makes the error easy to miss.

## References
1. Shargel L, Yu ABC. *Applied Biopharmaceutics and Pharmacokinetics*. 8th ed. New York: McGraw Hill Medical; 2022.
2. Rowland M, Tozer TN. *Clinical Pharmacokinetics and Pharmacodynamics: Concepts and Applications*. 5th ed. Philadelphia: Wolters Kluwer; 2019.


---

# Chapter 4: Two Compartment, IV Bolus: Plasma Data

## Learning Objectives
By the end of this chapter you will be able to:
1. [LO1] Describe the two-compartment open model and name the four rate constants it uses.
2. [LO2] Identify A, B, a and b in a biexponential equation and state what each one represents.
3. [LO3] Apply the method of residuals to separate the distribution phase from the elimination phase.
4. [LO4] Calculate K, K₁₂, K₂₁ and Vp from A, B, a and b.
5. [LO5] Explain why b is not the elimination rate constant, and what follows from confusing them.

## 4.1 When One Compartment Is Not Enough

Chapter 2 assumed that a drug reaches equilibrium with the tissues instantly. For many drugs it does not. Plot the plasma concentration on semilog axes and instead of one straight line you see two: a steep early segment and a shallower later one, joined by a curve.

The steep segment is the **distribution phase**. Drug is leaving the plasma for the tissues faster than it is being eliminated, so the concentration falls quickly. The shallow segment is the **elimination phase**. Once the tissue concentration has risen enough for transfer to run both ways at similar rates, the only remaining net loss is elimination, and the fall slows.

Five statements define the model.

1. The drug equilibrates rapidly and uniformly in the central compartment, and slowly in the peripheral compartment.
2. Transfer between the two compartments is first order in both directions.
3. At time zero there is no drug in the tissue compartment, and the plasma concentration is at its peak.
4. As drug distributes into tissue, the plasma concentration falls steeply while the tissue concentration rises to its own peak.
5. Once the concentration gradient between the compartments disappears, tissue concentration begins to fall as well.

Statement 3 is what makes an intravenous bolus the right experiment for measuring these constants [1]. The whole dose is in the central compartment at a known instant.

## 4.2 The Four Rate Constants

Two constants govern transfer. **K₁₂** carries drug from central to tissue, **K₂₁** carries it back. A third, K, governs elimination, and it acts only on the central compartment. The rate of change of drug in the tissue compartment is the difference between what arrives and what leaves:

dCt/dt = K₁₂ · Cp − K₂₁ · Ct

Concentrations are amounts divided by the volume of their own compartment. Cp = Dp/Vp in the central compartment, and Ct = Dt/Vt in the tissue compartment. **Vp**, the **volume of the central compartment**, is the one that can be measured from plasma data alone.

> **Watch the Units:** K, K₁₂ and K₂₁ are all first-order rate constants with units of reciprocal time. They are not interchangeable and they are not additive in any simple way. Vp and Vt are volumes, and Vt cannot be obtained from plasma data, because no plasma sample ever sees the tissue compartment directly.

## 4.3 The Biexponential Equation

Solving the two simultaneous differential equations gives the plasma concentration as the sum of two exponentials.

> **Key Equation:** Equation 4.1 — the biexponential decline
>
> $$C_p = A\, e^{-at} + B\, e^{-bt}$$
>
> where a and b are **hybrid rate constants** for the distribution and elimination phases, A and B are the zero-time intercepts of the two exponential terms, and a > b always.

The word *hybrid* is the important one. Neither a nor b is a single physical process. Each is a combination of K, K₁₂ and K₂₁, and the two combinations are constrained by two relationships that will be used to invert them later:

a + b = K + K₁₂ + K₂₁    and    a · b = K · K₂₁

Because a > b, the first term dies away faster than the second. After a few multiples of 1/a the term A·e^(−at) is effectively zero, and the equation collapses to:

Cp = B·e^(−bt),   so   log Cp = log B − bt / 2.303

That is the shallow straight line seen on the semilog plot at late times. Its slope gives b and its back-extrapolated intercept gives B.

## 4.4 The Method of Residuals

The elimination phase is easy because it survives on its own at late times. The distribution phase is not, because it never appears alone: the early points contain both exponentials added together. The **method of residuals**, also called feathering or stripping, separates them by subtraction.

The procedure has four steps.

1. Plot log Cp against time and identify the terminal straight portion.
2. Fit that portion, read b from its slope and B from its intercept, then extend the line back to time zero.
3. For each early point, read the extrapolated value Cp′ off the extended line and subtract it from the measured Cp. The difference is the **residual concentration**.
4. Plot log(Cp − Cp′) against time. This is the residual line, of slope −a/2.303 and intercept A.

![A semilogarithmic plot of plasma concentration against time. Filled circles curve steeply at first and then straighten from four hours onwards. A dashed line fitted to the straight portion is extrapolated back to an intercept marked B equals 15, with slope minus b over 2.303 and b equal to 0.21 per hour. Open squares below the early circles show the residuals, lying on a steeper dotted line back-extrapolated to an intercept marked A equals 45, with slope minus a over 2.303 and a equal to 1.8 per hour.](../rework/figures/out/ch04-residuals.png)

*Figure 4.1 — The method of residuals applied to the Example 4.1 data. The terminal line is fitted to the late points and extrapolated back to give b and B; subtracting it from each early point gives the residuals, whose own line gives a and A.*  
Original diagram, drawn from the first edition Example 10 dataset, page 20 (original)

The logic is worth stating in one sentence. The extended terminal line is what the concentration *would have been* if only the slow process were acting, so whatever is left over must belong to the fast one.

> **Common Mistake:** The residual line can only be built from points that lie in the distribution phase. Once the curve has joined the terminal line, the residual is the difference between two nearly equal numbers, and its logarithm is dominated by measurement error. Residual points that scatter wildly or go negative are a sign that you have gone too far along the curve, not a sign of a bad assay. Stop at the last point that lies clearly above the terminal line.

## 4.5 Recovering the Real Constants

A, B, a and b are what the plot gives. K, K₁₂, K₂₁ and Vp are what the model means. Four equations connect them.

> **Key Equation:** Equation 4.2 — from intercepts and hybrids to model constants
>
> $$K_{21} = \frac{A b + B a}{A + B}$$
>
> $$K = \frac{a b}{K_{21}}$$
>
> $$K_{12} = a + b - K_{21} - K$$
>
> $$V_p = \frac{D_B^0}{A + B}$$
>
> The order matters: K₂₁ must be found first, because K depends on it and K₁₂ depends on both.

Note the last one. Setting t = 0 in Equation 4.1 gives Cp⁰ = A + B, so the central-compartment volume follows from the same relation used in Chapter 2, with A + B in place of Cp⁰.

The area under the curve also has a compact form, and it provides a useful arithmetic check:

AUC = A/a + B/b = D_B⁰ / (K · Vp)

## 4.6 Why b Is Not K

This is the single most common misreading of a two-compartment analysis. The terminal slope of a semilog plot gives b, and b is not the elimination rate constant.

K is the true elimination rate constant: it describes loss from the body. The constant b is a hybrid, held down by the drug returning from the tissue compartment. That returning drug partly refills the plasma as elimination empties it, so the observed terminal decline is *slower* than elimination alone would be. In every two-compartment drug, b is smaller than K [2].

> **Common Mistake:** Reporting 0.693/b as "the half-life" without qualification. It is the terminal half-life, which is the right number for predicting how long a concentration takes to fall, and for deciding a washout period. It is not 0.693/K, and it does not describe the rate at which the body clears the drug. State which one you mean.

> **Worked Example:** Example 4.1 — feathering a two-compartment curve
>
> An antibiotic is given as a 300 mg IV bolus to a 75 kg volunteer. Plasma concentrations are:
>
> | t (h) | 0.25 | 0.5 | 1.0 | 1.5 | 2.0 | 4.0 | 8.0 | 12.0 | 16.0 |
> |---|---|---|---|---|---|---|---|---|---|
> | Cp (µg·mL⁻¹) | 43 | 32 | 20 | 14 | 11 | 6.5 | 2.8 | 1.2 | 0.52 |
>
> Determine a, b, A, B, K, K₁₂, K₂₁, Vp and the terminal half-life.
>
> *Step 1 — find the terminal phase.* On semilog axes the points from 4 h onwards lie on one straight line. The earlier points bend above it, which is the distribution phase.
>
> *Step 2 — b from the terminal slope.* Using the 4 h and 16 h points:
>
> b = [ln 6.5 − ln 0.52] ÷ (16.0 − 4.0) = (1.872 + 0.654) ÷ 12 = 0.210 h⁻¹
>
> *Step 3 — B by back-extrapolation.*
>
> ln B = ln 6.5 + (0.210 × 4.0) = 1.872 + 0.840 = 2.712, so B = 15.1 ≈ 15 µg·mL⁻¹
>
> *Step 4 — build the residual table.* For each early time, Cp′ = 15·e^(−0.21t).
>
> | t (h) | Cp measured | Cp′ extrapolated | residual Cp − Cp′ |
> |---|---|---|---|
> | 0.25 | 43 | 14.23 | 28.77 |
> | 0.50 | 32 | 13.51 | 18.49 |
> | 1.00 | 20 | 12.16 | 7.84 |
> | 1.50 | 14 | 10.95 | 3.05 |
> | 2.00 | 11 | 9.86 | 1.14 |
>
> *Step 5 — a from the residual slope.* Using the 0.25 h and 2.0 h residuals:
>
> a = [ln 28.77 − ln 1.14] ÷ (2.00 − 0.25) = (3.359 − 0.131) ÷ 1.75 = 1.84 h⁻¹
>
> Rounding to the precision the data support, a = 1.8 h⁻¹.
>
> *Step 6 — A by back-extrapolation of the residual line.*
>
> ln A = ln 28.77 + (1.8 × 0.25) = 3.359 + 0.450 = 3.809, so A = 45 µg·mL⁻¹
>
> *Step 7 — the equation of the curve.*
>
> Cp = 45·e^(−1.8t) + 15·e^(−0.21t)
>
> *Step 8 — the model constants, in the order Equation 4.2 requires.*
>
> K₂₁ = (45 × 0.21 + 15 × 1.8) ÷ (45 + 15) = (9.45 + 27.0) ÷ 60 = 0.608 h⁻¹
>
> K = (1.8 × 0.21) ÷ 0.608 = 0.378 ÷ 0.608 = 0.622 h⁻¹
>
> K₁₂ = 1.8 + 0.21 − 0.608 − 0.622 = 0.780 h⁻¹
>
> *Step 9 — Vp, carrying units.* Cp⁰ = A + B = 60 µg·mL⁻¹ = 60 mg·L⁻¹.
>
> Vp = 300 mg ÷ 60 mg·L⁻¹ = 5.0 L
>
> *Step 10 — the terminal half-life.*
>
> t½ = 0.693 ÷ 0.210 = 3.30 h
>
> *Answer.* a = 1.8 h⁻¹, b = 0.21 h⁻¹, A = 45 µg·mL⁻¹, B = 15 µg·mL⁻¹, K₂₁ = 0.608 h⁻¹, K = 0.622 h⁻¹, K₁₂ = 0.780 h⁻¹, Vp = 5.0 L and the terminal half-life is 3.30 h.
>
> *Check by a second route.* AUC from the intercepts is 45/1.8 + 15/0.21 = 25.0 + 71.4 = 96.4 µg·h·mL⁻¹. AUC from the dose is 300 mg ÷ (0.622 h⁻¹ × 5.0 L) = 96.5 mg·h·L⁻¹. The two agree, which confirms every constant used in them.
>
> *Read Step 8 against Section 4.6.* Here b = 0.21 h⁻¹ while K = 0.622 h⁻¹, so the true elimination rate constant is three times the terminal one. Taking 0.693/b as the elimination half-life would understate the body's clearing capacity threefold.

> **Why It Matters in Practice:** Vp, not the total volume of distribution, is what a loading dose must fill to reach a target peak immediately. Using a larger volume overshoots. This is why a loading dose of a two-compartment drug such as digoxin or lidocaine is given slowly or in divided portions: an instant bolus sized on the total volume would produce a central-compartment concentration far above the minimum toxic concentration before distribution had time to lower it.

## Key Takeaways
- A curved semilog plot after an IV bolus means more than one compartment.
- The biexponential equation is Cp = A·e^(−at) + B·e^(−bt), with a > b always.
- a and b are hybrid constants. Each combines K, K₁₂ and K₂₁, and neither is a single process.
- The terminal line gives b and B. The method of residuals recovers a and A by subtracting the extrapolated terminal line from the early points.
- Build the residual line only from points clearly above the terminal line.
- K₂₁ must be calculated first, then K, then K₁₂. Vp = dose/(A + B).
- b is always smaller than K, because drug returning from tissue slows the observed decline.

## Check Your Understanding

**Q1.** [LO2] In the equation Cp = A·e^(−at) + B·e^(−bt), the constant b is obtained from:
A) The intercept of the residual line
B) The slope of the residual line
C) The slope of the terminal straight portion
D) The sum of the two intercepts

**Q2.** [LO5] For a drug following a two-compartment model, which statement is correct?
A) b is smaller than K, because drug returning from tissue slows the terminal decline.
B) b is larger than K, because the distribution phase is faster.
C) b equals K once distribution is complete.
D) b and K cannot be compared, since they have different units.

**Q3.** [LO3] The residual concentration used in the method of residuals is:
A) The concentration remaining at the last sampling time
B) The difference between the tissue and plasma concentrations
C) The concentration predicted by the terminal line alone
D) The measured concentration minus the extrapolated terminal value

**Q4.** [LO1] In the two-compartment open model, elimination is assumed to occur from:
A) The tissue compartment only
B) The central compartment only
C) Both compartments at rate K
D) Whichever compartment has the higher concentration

**Q5.** [LO4] A drug gives A = 40, B = 10 µg·mL⁻¹, a = 2.0 h⁻¹ and b = 0.25 h⁻¹. K₂₁ is:
A) 1.65 h⁻¹
B) 1.13 h⁻¹
C) 0.60 h⁻¹
D) 0.25 h⁻¹

**Q6.** [LO4] After a 400 mg IV bolus a drug gives A = 60 and B = 20 µg·mL⁻¹. Vp is:
A) 20.0 L
B) 5.0 L
C) 6.7 L
D) 0.2 L

**Q7.** [LO3] A student's residual points scatter badly and two of them are negative. The most likely cause is:
A) Residuals were calculated from points that had already joined the terminal line.
B) The assay was insufficiently sensitive at early times.
C) The terminal slope was read over too short a time span.
D) The drug follows a three-compartment model.

**Q8.** [LO2] Which pair of statements about A and B is correct?
A) A is the dose and B is the volume of the central compartment.
B) A belongs to the elimination phase and B to the distribution phase.
C) Their difference gives the concentration at time zero.
D) They are the zero-time intercepts of the two exponential terms, and their sum is Cp⁰.

**Q9.** [LO1] Which quantity cannot be determined from plasma data alone in this model?
A) K₁₂
B) K₂₁
C) Vt, the volume of the tissue compartment
D) Vp, the volume of the central compartment

**Q10.** [LO5] A two-compartment drug has b = 0.1 h⁻¹ and K = 0.4 h⁻¹. A washout period between study arms should be based on:
A) 0.693/K, because K describes true elimination
B) 0.693/b, because the terminal phase governs how long concentrations persist
C) The average of the two half-lives
D) K₁₂, because distribution controls the time course

### Exercises

**E4.1** [LO4] An antibiotic is given IV at 300 mg to a 75 kg volunteer. The plasma curve fits Cp = 45·e^(−1.8t) + 15·e^(−0.21t), with Cp in µg·mL⁻¹ and t in hours. Determine K, K₁₂, K₂₁, Vp, the terminal half-life and the AUC, and state which of these would change if the same dose were given to a 60 kg volunteer with the same Vp per kilogram.

**E4.2** [LO3] Using the data of Example 4.1, calculate the residual at t = 3.0 h given that the measured Cp there is 7.9 µg·mL⁻¹. Comment on whether this point should be used in the residual line, and justify your answer numerically.

**E4.3** [LO5] A drug has a = 1.2 h⁻¹, b = 0.15 h⁻¹, A = 30 and B = 10 µg·mL⁻¹ after a 200 mg IV bolus. Calculate K and the two half-lives 0.693/K and 0.693/b. A colleague reports "the half-life is 4.6 hours" without saying which. Explain in one sentence what could go wrong if that number were used to estimate how fast the body clears the drug.

## Answers and Worked Solutions

**Q1. C** — At late times the A term has vanished and only B·e^(−bt) remains, so the terminal slope is −b/2.303. The residual line carries a and A instead.

**Q2. A** — Drug flowing back from tissue partly replaces what elimination removes, so the observed terminal decline is slower than elimination alone. Both constants have units of reciprocal time, which rules out D.

**Q3. D** — The extrapolated terminal line is what the concentration would be if only the slow process acted, so the remainder belongs to the fast one.

**Q4. B** — Elimination from the central compartment only is a defining assumption. The peripheral compartment exchanges through K₁₂ and K₂₁ but has no exit of its own.

**Q5. C** — K₂₁ = (A·b + B·a)/(A + B) = (40 × 0.25 + 10 × 2.0)/50 = (10 + 20)/50 = 0.60 h⁻¹. Option A is a + b minus something; D is b itself.

**Q6. B** — Cp⁰ = A + B = 80 µg·mL⁻¹ = 80 mg·L⁻¹, so Vp = 400 mg ÷ 80 mg·L⁻¹ = 5.0 L. Option A divides by B alone and C by A alone.

**Q7. A** — Beyond the distribution phase the residual is the difference between two nearly equal numbers, so noise dominates and it can go negative. A sensitive assay cannot prevent this, because the problem is arithmetic rather than analytical.

**Q8. D** — Setting t = 0 in Equation 4.1 gives Cp⁰ = A + B. Option B reverses them: A belongs to the fast distribution term.

**Q9. C** — No plasma sample measures the tissue compartment, so Vt is inaccessible from plasma data. K₁₂ and K₂₁ are still obtainable, because they shape the plasma curve itself.

**Q10. B** — A washout must let concentrations decay to negligible levels, and that is governed by the slowest phase. Here 0.693/b = 6.9 h against 0.693/K = 1.7 h, so basing the washout on K would leave carry-over into the next arm.

---

**E4.1 — worked solution**

*Step 1 — read the four constants off the equation.*

A = 45 µg·mL⁻¹, a = 1.8 h⁻¹, B = 15 µg·mL⁻¹, b = 0.21 h⁻¹

*Step 2 — K₂₁ first.*

K₂₁ = (45 × 0.21 + 15 × 1.8) ÷ 60 = 36.45 ÷ 60 = 0.608 h⁻¹

*Step 3 — K.*

K = (1.8 × 0.21) ÷ 0.608 = 0.622 h⁻¹

*Step 4 — K₁₂.*

K₁₂ = 1.8 + 0.21 − 0.608 − 0.622 = 0.780 h⁻¹

*Step 5 — Vp.* A + B = 60 µg·mL⁻¹ = 60 mg·L⁻¹.

Vp = 300 mg ÷ 60 mg·L⁻¹ = 5.0 L, which is 0.067 L·kg⁻¹

*Step 6 — terminal half-life.* t½ = 0.693 ÷ 0.21 = 3.30 h.

*Step 7 — AUC.* AUC = 45/1.8 + 15/0.21 = 25.0 + 71.4 = 96.4 µg·h·mL⁻¹.

*Which values change in a 60 kg volunteer?* At the same Vp per kilogram, Vp falls to 0.067 × 60 = 4.0 L. The four rate constants are properties of the drug and the transfer processes, so a, b, K, K₁₂ and K₂₁ are unchanged, and so is the terminal half-life. But the same 300 mg dose now fills a smaller central compartment, so A + B rises to 300 ÷ 4.0 = 75 mg·L⁻¹ and the whole curve shifts upwards by a factor of 1.25. AUC rises in the same proportion, to 120 µg·h·mL⁻¹.

*Answer.* K = 0.622 h⁻¹, K₁₂ = 0.780 h⁻¹, K₂₁ = 0.608 h⁻¹, Vp = 5.0 L, terminal t½ = 3.30 h, AUC = 96.4 µg·h·mL⁻¹. In the lighter volunteer, *if the micro-rate constants K, K₁₂ and K₂₁ are assumed unchanged* — which body weight alone does not establish — only Vp, the intercepts and the AUC change. Nothing in the data tests that assumption: a smaller person may also clear the drug differently, in which case the exponents move too and the whole curve must be refitted.

**E4.2 — worked solution**

*Step 1 — the extrapolated terminal value at 3.0 h.*

Cp′ = 15 · e^(−0.21 × 3.0) = 15 · e^(−0.63) = 15 × 0.5326 = 7.99 µg·mL⁻¹

*Step 2 — the residual.*

Cp − Cp′ = 7.9 − 7.99 = −0.09 µg·mL⁻¹

*Step 3 — interpret it.* The residual is negative, so its logarithm does not exist and the point cannot go on the residual plot.

*Justify it numerically.* At 3.0 h the fast term contributes A·e^(−at) = 45 · e^(−1.8 × 3.0) = 45 × 0.0045 = 0.20 µg·mL⁻¹, which is 2.5% of the measured concentration. The distribution phase is effectively over. A measurement uncertainty of only ±1% on 7.9 µg·mL⁻¹ is ±0.08 µg·mL⁻¹, which is a third of the whole signal being sought.

*Answer.* The residual is about −0.09 µg·mL⁻¹ and the point must not be used. By 3.0 h the true residual has fallen below the noise in the measurement, so this point lies past the end of the usable distribution phase.

**E4.3 — worked solution**

*Step 1 — K₂₁.*

K₂₁ = (30 × 0.15 + 10 × 1.2) ÷ 40 = (4.5 + 12.0) ÷ 40 = 0.4125 h⁻¹

*Step 2 — K.*

K = (1.2 × 0.15) ÷ 0.4125 = 0.18 ÷ 0.4125 = 0.436 h⁻¹

*Step 3 — the two half-lives.*

0.693 / K = 0.693 ÷ 0.436 = 1.59 h

0.693 / b = 0.693 ÷ 0.15 = 4.62 h

*Which one did the colleague quote?* 4.6 h is 0.693/b, the terminal half-life.

*What could go wrong.* Used as an elimination half-life it understates the body's clearing capacity by a factor of about three, so any dosing interval or infusion rate derived from it would deliver far more drug than intended and the drug would accumulate.

*Answer.* K = 0.436 h⁻¹, 0.693/K = 1.59 h and 0.693/b = 4.62 h. The quoted figure is the terminal half-life, which is correct for predicting persistence and washout but wrong for estimating clearance.

## References
1. Shargel L, Yu ABC. *Applied Biopharmaceutics and Pharmacokinetics*. 8th ed. New York: McGraw Hill Medical; 2022.
2. Rowland M, Tozer TN. *Clinical Pharmacokinetics and Pharmacodynamics: Concepts and Applications*. 5th ed. Philadelphia: Wolters Kluwer; 2019.


---

# Chapter 5: Intravenous Infusion

## Learning Objectives
By the end of this chapter you will be able to:
1. [LO1] Explain why a constant infusion produces a plateau, and write the equation of the approach to it.
2. [LO2] Calculate the steady-state concentration from the infusion rate and clearance, and the reverse.
3. [LO3] State how long steady state takes, and explain why that time does not depend on the infusion rate.
4. [LO4] Determine K and t½ from concentrations measured during an infusion.
5. [LO5] Calculate a loading dose and predict the concentration when a loading dose and an infusion are combined.

## 5.1 Zero Order In, First Order Out

Every dose so far has arrived all at once. A constant intravenous infusion delivers drug at a fixed amount per unit time, which is a **zero order** input: the rate does not depend on how much drug is already present. Elimination remains first order, so it speeds up as the concentration rises.

Those two facts together produce a plateau. Early on, little drug is present, elimination is slow, and the concentration climbs steeply. As it climbs, elimination accelerates. Eventually elimination matches input exactly, the net rate of change becomes zero, and the concentration stops changing. That plateau is the **steady-state concentration**, Css [1].

The net rate of change of drug in the body is input minus output:

dD_B/dt = R − K · D_B

where R is the zero-order infusion rate, in amount per unit time.

## 5.2 The Infusion Equation

Integrating that equation from an empty body at time zero, and dividing by Vd to convert amount to concentration, gives the working equation of this chapter.

> **Key Equation:** Equation 5.1 — the approach to steady state
>
> $$C_p = \frac{R}{K V_d}\left(1 - e^{-Kt}\right)$$
>
> As t → ∞ the exponential vanishes and the bracket becomes 1, leaving:
>
> $$C_{ss} = \frac{R}{K V_d} = \frac{R}{Cl}$$
>
> where Cl is total body clearance from Chapter 2.

The second form is the one to remember. Steady state is the infusion rate divided by clearance, and nothing else enters it. Vd does not appear. Vd controls how large the swings are on the way up, but not where the plateau sits.

Two consequences follow immediately, and both are used in practice.

*Css is directly proportional to R.* Double the infusion rate and the plateau doubles. Halve it and the plateau halves. The relationship is linear because both the input and the clearance are independent of concentration.

*Css is inversely proportional to clearance.* A patient with half the normal clearance reaches twice the plateau on the same infusion rate. This is the usual reason an infusion has to be reduced in renal or hepatic impairment.

> **Watch the Units:** R is an amount per time, such as mg·h⁻¹. Cl is a volume per time, such as L·h⁻¹. Their quotient is an amount per volume, which is a concentration. If your answer for Css comes out in mg·h⁻¹ or in litres, you have divided the wrong way round. Check the units before checking the arithmetic.

## 5.3 How Long Steady State Takes

Set Cp = f · Css in Equation 5.1 and the R, K and Vd all cancel, leaving a relation between the fraction of steady state reached and the number of half-lives elapsed. The time to any given fraction of Css therefore depends on the half-life alone.

| Half-lives elapsed | Percent of Css reached |
|---|---|
| 1 | 50% |
| 2 | 75% |
| 3 | 87.5% |
| 3.32 | 90% |
| 4.32 | 95% |
| 5 | 96.9% |
| 6.65 | 99% |

This is the same series as the elimination table in Chapter 2, read upside down. What is being eliminated there is being accumulated here.

> **Common Mistake:** Raising the infusion rate to reach steady state sooner. It does not work. Doubling R doubles the plateau, and the concentration still takes the same number of half-lives to get there, so at every moment it is twice as high as before but exactly as far from its own target. The only way to reach a chosen concentration quickly is a loading dose, which is Section 5.5.

Five half-lives is the practical rule for "at steady state", and it is when a monitoring sample should be drawn. Theophylline has a half-life of about 7 h, so a trough concentration means little before 5 × 7 = 35 h of constant infusion. A concentration measured at 10 h is not a low steady state; it is an incomplete approach to a steady state that has not arrived.

![Two plots of plasma concentration against time over 24 hours. On the left, three rising curves for infusion rates of 7.5, 15 and 30 mg per hour approach plateaus of 5, 10 and 20 micrograms per millilitre; a vertical dashed line at 15 hours marks the point where all three have reached 95 per cent of their own plateau. On the right, three curves with the same infusion: one starting at 15 and falling to the plateau of 10, one flat at 10 throughout, and one starting at zero and rising to 10.](../rework/figures/out/ch05-infusion.png)

*Figure 5.1 — Left: three infusion rates of the same drug. The plateau is proportional to the rate, but all three reach 95% of their own plateau at the same moment, because the time course depends only on the half-life. Right: the effect of a loading dose. A dose of exactly Css · Vd holds the concentration flat at Css from the first instant.*  
Original diagram, drawn from the first edition Example 14 dataset, page 24 (original)

Note also that steady state is approached but never reached exactly. The exponential never becomes zero. Ninety-nine per cent after 6.65 half-lives is as close as the model ever gets, which is why the practical definitions are stated as percentages.

## 5.4 Finding K During an Infusion

An infusion can be used to measure the half-life, which matters when a patient's own kinetics are needed rather than the population value. Rearranging Equation 5.1 isolates a term that decays exponentially:

Css − Cp = Css · e^(−Kt),   so   log(Css − Cp) = log Css − Kt / 2.303

The quantity (Css − Cp) is how far the concentration still has to climb. It falls with exactly the same rate constant that governs elimination. So a plot of log(Css − Cp) against time is a straight line of slope −K/2.303.

This needs Css, which in practice comes from a late sample. A sample taken after five or more half-lives is within a few per cent of the plateau and can be used as Css directly.

## 5.5 The Loading Dose

A **loading dose** is an intravenous bolus given at the start of an infusion, sized so that the concentration jumps straight to Css instead of climbing to it.

The requirement is simply that the bolus fills the volume of distribution to the target concentration.

> **Key Equation:** Equation 5.2 — loading dose
>
> $$D_L = C_{ss} V_d = \frac{R}{K}$$
>
> The two forms are the same equation. Substituting Css = R/(K·Vd) into the first gives the second, and the Vd cancels.

When a loading dose and an infusion run together, the concentration is the sum of two contributions: the bolus decaying and the infusion accumulating.

Cp = (D_L / Vd) · e^(−Kt) + Css · (1 − e^(−Kt))

If D_L has been chosen as Css·Vd, then D_L/Vd equals Css, and the expression collapses:

Cp = Css · e^(−Kt) + Css · (1 − e^(−Kt)) = Css

The concentration is flat at Css from the first instant. Every molecule the bolus loses, the infusion replaces. If the loading dose is too large the curve starts high and falls to the plateau; if too small it starts low and climbs.

> **Why It Matters in Practice:** This is why an antiarrhythmic such as lidocaine, or an antibiotic in sepsis, is started with a bolus followed by an infusion. Without the bolus a drug with a 6 h half-life would take 30 h to become effective, which is far too slow when the indication is urgent. The bolus buys the whole approach period, and the infusion holds what the bolus achieved [2].

## 5.6 After the Infusion Stops

Once the infusion is switched off there is no input, and the drug decays by first-order elimination from whatever concentration it had reached.

Cp = Cp_stop · e^(−Kt′)

where t′ is time measured from the moment of stopping. The post-infusion decline is an ordinary Chapter 2 problem, and its slope on semilog axes gives the same K.

> **Worked Example:** Example 5.1 — one drug, both routes
>
> A drug is given to a 75 kg patient on two occasions: once as a single IV dose of 1 mg·kg⁻¹, and once as a constant IV infusion of 0.2 mg·kg⁻¹·h⁻¹. Serum concentrations, in µg·mL⁻¹, are:
>
> | t (h) | 0 | 2 | 4 | 6 | 8 | 10 | 12 | 18 | 24 |
> |---|---|---|---|---|---|---|---|---|---|
> | Single IV dose | 10 | 6.7 | 4.5 | 3.0 | 2.0 | 1.35 | — | — | — |
> | Constant infusion | 0 | 3.3 | 5.5 | 7.0 | 8.0 | 8.6 | 9.1 | 9.7 | 9.9 |
>
> Find Css, the time to 95% of Css, the clearance, the concentration 4 h after stopping a 24 h infusion, the rate needed to hold 10 µg·mL⁻¹, and the concentration 4 h after a 1 mg·kg⁻¹ bolus followed by the same infusion.
>
> *Step 1 — K and Vd from the bolus arm.* Using the 0 h and 10 h points:
>
> K = [ln 10 − ln 1.35] ÷ 10 = (2.303 − 0.300) ÷ 10 = 0.200 h⁻¹, so t½ = 0.693 ÷ 0.200 = 3.47 h
>
> The dose was 1 mg·kg⁻¹ × 75 kg = 75 mg, and Cp⁰ = 10 µg·mL⁻¹ = 10 mg·L⁻¹.
>
> Vd = 75 mg ÷ 10 mg·L⁻¹ = 7.5 L, which is 0.10 L·kg⁻¹
>
> *Step 2 — clearance.*
>
> Cl = K · Vd = 0.200 h⁻¹ × 7.5 L = 1.5 L·h⁻¹
>
> *Step 3 — Css.* The infusion rate is 0.2 mg·kg⁻¹·h⁻¹ × 75 kg = 15 mg·h⁻¹.
>
> Css = R ÷ Cl = 15 mg·h⁻¹ ÷ 1.5 L·h⁻¹ = 10 mg·L⁻¹ = 10 µg·mL⁻¹
>
> The infusion column reaches 9.9 at 24 h, which confirms it.
>
> *Step 4 — time to 95% of Css.*
>
> t = 4.32 × t½ = 4.32 × 3.47 h = 15.0 h
>
> *Step 5 — 4 h after stopping at 24 h.* The concentration at the moment of stopping is 9.9 µg·mL⁻¹.
>
> Cp = 9.9 × e^(−0.200 × 4) = 9.9 × 0.449 = 4.45 µg·mL⁻¹
>
> *Step 6 — rate to hold 10 µg·mL⁻¹.*
>
> R = Css × Cl = 10 mg·L⁻¹ × 1.5 L·h⁻¹ = 15 mg·h⁻¹
>
> This is the rate already being used, which is why the plateau sat at 10.
>
> *Step 7 — bolus plus infusion, at 4 h.* The bolus contributes a decaying term and the infusion an accumulating one. With e^(−0.2 × 4) = 0.449:
>
> from the bolus: (75 mg ÷ 7.5 L) × 0.449 = 10 × 0.449 = 4.49 mg·L⁻¹
>
> from the infusion: 10 × (1 − 0.449) = 10 × 0.551 = 5.51 mg·L⁻¹
>
> total: 4.49 + 5.51 = 10.0 µg·mL⁻¹
>
> *Answer.* Css = 10 µg·mL⁻¹; 95% of it at 15.0 h; Cl = 1.5 L·h⁻¹; 4.45 µg·mL⁻¹ four hours after stopping; 15 mg·h⁻¹ to hold 10 µg·mL⁻¹; and 10.0 µg·mL⁻¹ at 4 h with the bolus.
>
> *Look at Step 7 again.* The answer is exactly Css, and not by coincidence. The 75 mg bolus equals Css × Vd = 10 mg·L⁻¹ × 7.5 L = 75 mg, which is the ideal loading dose. Repeat Step 7 at any other time and it still gives 10.0. The two terms always sum to Css, so the concentration is flat from the first instant and the 15 h approach period disappears entirely.

## Key Takeaways
- A constant infusion is zero-order input against first-order output, which produces a plateau.
- Css = R/Cl. Vd does not appear, so it does not set the plateau.
- Css is proportional to R and inversely proportional to clearance.
- The time to any fraction of Css depends only on t½: 95% at 4.32 half-lives, 99% at 6.65.
- Raising R raises the plateau but does not shorten the time to reach it.
- log(Css − Cp) against time is a straight line of slope −K/2.303, which yields the patient's own half-life.
- D_L = Css·Vd = R/K. A correct loading dose makes the concentration flat at Css from time zero.

## Check Your Understanding

**Q1.** [LO2] The steady-state concentration during a constant IV infusion is given by:
A) R × Vd
B) R × K × Vd
C) R / Vd
D) R / Cl

**Q2.** [LO3] The infusion rate of a drug is doubled. Compared with before, steady state will be:
A) Twice as high and reached in half the time
B) Twice as high and reached in the same time
C) The same height and reached in half the time
D) Four times as high and reached in the same time

**Q3.** [LO3] A drug has a half-life of 8 h. A plasma sample for therapeutic monitoring during a constant infusion should be taken no earlier than about:
A) 40 h
B) 16 h
C) 8 h
D) 4 h

**Q4.** [LO1] Which statement about the approach to steady state is correct?
A) Steady state is reached exactly after five half-lives.
B) The concentration rises linearly until the plateau is reached.
C) Steady state is approached asymptotically and never reached exactly.
D) The rate of rise is constant because the input is zero order.

**Q5.** [LO5] An infusion runs at 30 mg·h⁻¹ and the drug has K = 0.15 h⁻¹. The loading dose that brings the concentration immediately to steady state is:
A) 4.5 mg
B) 200 mg
C) 45 mg
D) 20 mg

**Q6.** [LO2] A patient's clearance falls to half its normal value while the infusion rate is unchanged. The new steady-state concentration will be:
A) Unchanged, because Css depends on the infusion rate
B) Half the previous value
C) One quarter of the previous value
D) Twice the previous value

**Q7.** [LO4] During an infusion, a plot of log(Css − Cp) against time gives a straight line. Its slope equals:
A) −K
B) −R/(K·Vd)
C) −K/2.303
D) −0.693/K

**Q8.** [LO5] A loading dose larger than Css·Vd is given at the start of an infusion. The concentration will:
A) Start above Css and fall towards it
B) Start at Css and stay flat
C) Start below Css and rise towards it
D) Rise above Css and continue rising

**Q9.** [LO1] During an infusion, the reason the concentration stops rising is that:
A) The infusion pump reduces its rate automatically.
B) Elimination has accelerated until it matches the infusion rate.
C) The volume of distribution has become saturated.
D) Elimination has become zero order.

**Q10.** [LO2] An infusion of 20 mg·h⁻¹ produces a steady state of 4 mg·L⁻¹. The clearance is:
A) 80 L·h⁻¹
B) 0.2 L·h⁻¹
C) 5 L·h⁻¹
D) 24 L·h⁻¹

### Exercises

**E5.1** [LO2] An antibiotic has Vd = 10 L and K = 0.2 h⁻¹, and a steady-state plasma concentration of 10 µg·mL⁻¹ is wanted. Calculate the required infusion rate, and state what the rate would have to be in a patient whose clearance is 40% of normal.

**E5.2** [LO4] An antibiotic has a half-life of 3.6 h in the general population. A patient receives it by IV infusion at 15 mg·h⁻¹, and blood samples at 8 h and 24 h give 5.5 and 6.5 mg·L⁻¹. Estimate the half-life in this patient, and calculate the infusion rate needed to hold 8 mg·L⁻¹.

**E5.3** [LO5] An infusion runs at 2 mg·h⁻¹ in a patient with K = 0.1 h⁻¹ and Vd = 10 L. Calculate the steady-state concentration, the loading dose needed to reach 2 µg·mL⁻¹ immediately, and the concentration at 3 h if the loading dose is given but the infusion is forgotten.

## Answers and Worked Solutions

**Q1. D** — Css = R/(K·Vd), and K·Vd is clearance. Option B is the reverse operation and would give an amount per time squared.

**Q2. B** — Css is proportional to R, so it doubles. The time course depends only on K, so the approach takes the same number of half-lives.

**Q3. A** — Five half-lives is the practical rule, and 5 × 8 = 40 h. A sample at 16 h is only at two half-lives, or 75% of the plateau.

**Q4. C** — The exponential term never reaches zero, so the plateau is an asymptote. Option A states the practical rule as if it were exact, and B and D both describe a linear rise, which does not happen.

**Q5. B** — D_L = R/K = 30 mg·h⁻¹ ÷ 0.15 h⁻¹ = 200 mg. Option A multiplies instead of dividing.

**Q6. D** — Css = R/Cl, so halving the denominator doubles the plateau. This is the usual reason an infusion must be reduced in organ impairment.

**Q7. C** — Taking base-10 logarithms of Css − Cp = Css·e^(−Kt) introduces the factor 2.303. Option A is the slope when natural logarithms are used.

**Q8. A** — The bolus term starts above Css and decays faster than the infusion term accumulates, so the curve falls onto the plateau from above.

**Q9. B** — First-order elimination accelerates as the concentration rises, until output equals input and the net rate of change is zero. Nothing becomes saturated, which rules out C and D.

**Q10. C** — Cl = R/Css = 20 mg·h⁻¹ ÷ 4 mg·L⁻¹ = 5 L·h⁻¹. Option A multiplies the two instead of dividing.

---

**E5.1 — worked solution**

*Step 1 — clearance.*

Cl = K × Vd = 0.2 h⁻¹ × 10 L = 2.0 L·h⁻¹

*Step 2 — convert the target concentration.* 10 µg·mL⁻¹ = 10 mg·L⁻¹.

*Step 3 — infusion rate.*

R = Css × Cl = 10 mg·L⁻¹ × 2.0 L·h⁻¹ = 20 mg·h⁻¹

*Step 4 — the impaired patient.* Clearance is 40% of normal, so Cl = 0.8 L·h⁻¹.

R = 10 mg·L⁻¹ × 0.8 L·h⁻¹ = 8 mg·h⁻¹

*Answer.* 20 mg·h⁻¹ normally, and 8 mg·h⁻¹ at 40% of normal clearance.

*Check the direction.* The impaired patient needs *less* drug per hour, not more, because each hour removes less. Giving 20 mg·h⁻¹ to that patient would settle at 25 mg·L⁻¹, two and a half times the target.

**E5.2 — worked solution**

*Step 1 — is 24 h close to steady state?* On the population half-life of 3.6 h, 24 h is 6.7 half-lives, so the 24 h sample is within about 1% of the plateau. Take Css ≈ 6.5 mg·L⁻¹.

*Step 2 — apply the approach equation at 8 h.*

Css − Cp = 6.5 − 5.5 = 1.0 mg·L⁻¹

*Step 3 — solve for K.*

ln(Css − Cp) = ln Css − Kt, so ln 1.0 = ln 6.5 − 8K

0 = 1.872 − 8K, so K = 0.234 h⁻¹

*Step 4 — half-life in this patient.*

t½ = 0.693 ÷ 0.234 = 2.96 h, or about 3.0 h

*Step 5 — clearance, then the new rate.*

Cl = R ÷ Css = 15 mg·h⁻¹ ÷ 6.5 mg·L⁻¹ = 2.31 L·h⁻¹

R = 8 mg·L⁻¹ × 2.31 L·h⁻¹ = 18.5 mg·h⁻¹

*Answer.* The patient's half-life is about 3.0 h, shorter than the population value of 3.6 h, and 18.5 mg·h⁻¹ is needed to hold 8 mg·L⁻¹.

*A shorter route to the same rate.* Since Css is proportional to R, the rate can be scaled directly: 15 × (8 ÷ 6.5) = 18.5 mg·h⁻¹. The clearance need not be calculated at all, though knowing it is more useful if the target changes again.

**E5.3 — worked solution**

*Step 1 — clearance and Css.*

Cl = 0.1 h⁻¹ × 10 L = 1.0 L·h⁻¹

Css = 2 mg·h⁻¹ ÷ 1.0 L·h⁻¹ = 2 mg·L⁻¹ = 2 µg·mL⁻¹

The infusion already delivers the target concentration, once it gets there.

*Step 2 — loading dose, by either form of Equation 5.2.*

D_L = Css × Vd = 2 mg·L⁻¹ × 10 L = 20 mg

D_L = R ÷ K = 2 mg·h⁻¹ ÷ 0.1 h⁻¹ = 20 mg

*Step 3 — the bolus alone at 3 h.* With no infusion, this is first-order decay from 2 mg·L⁻¹.

Cp = 2 × e^(−0.1 × 3) = 2 × 0.741 = 1.48 mg·L⁻¹

*Answer.* Css = 2 µg·mL⁻¹, the loading dose is 20 mg, and without the infusion the concentration has fallen to 1.48 µg·mL⁻¹ by 3 h.

*Why the two forms of the loading dose agree.* D_L = Css·Vd and D_L = R/K are the same statement, because Css itself is R/(K·Vd). The first form is the one to use when a target concentration is given, the second when only an infusion rate is.

## References
1. Shargel L, Yu ABC. *Applied Biopharmaceutics and Pharmacokinetics*. 8th ed. New York: McGraw Hill Medical; 2022.
2. Rowland M, Tozer TN. *Clinical Pharmacokinetics and Pharmacodynamics: Concepts and Applications*. 5th ed. Philadelphia: Wolters Kluwer; 2019.


---

# Chapter 6: Clearance

## Learning Objectives
By the end of this chapter you will be able to:
1. [LO1] Describe the three renal processes that determine how much drug leaves in the urine.
2. [LO2] Define clearance in both of its equivalent forms and give its units.
3. [LO3] Calculate total, renal and non-renal clearance, and relate them through the fraction excreted unchanged.
4. [LO4] Determine renal clearance from urine and plasma data by two methods.
5. [LO5] Interpret the clearance ratio, stating what it settles and what it leaves open, and justify preferring clearance to half-life.

## 6.1 Routes of Elimination

**Elimination** is the irreversible removal of drug from the body, and it happens by two kinds of process. Excretion removes the drug chemically unchanged, mainly through the kidney but also in bile, sweat, saliva and milk. Metabolism converts it enzymatically into something else, mainly in the liver, and is the subject of Chapter 11.

Renal excretion dominates for drugs that are non-volatile, water soluble, of low molecular weight and slowly metabolised. Those four properties describe a molecule the kidney can handle and the liver has little reason to touch [1].

## 6.2 How the Kidney Handles a Drug

Three processes act on a drug in the nephron, and the net amount excreted is their algebraic sum.

> **Key Equation:** Equation 6.1 — net renal excretion
>
> rate of renal excretion = rate of glomerular filtration + rate of active secretion − rate of tubular reabsorption
>
> The minus sign is the whole point: reabsorption returns drug to the blood, so it reduces excretion.

![Two panels. The upper panel shows a blood channel above a tubular fluid channel. Arrows point down for glomerular filtration, described as passive and free drug only with a GFR of 125 to 130 millilitres per minute, and down for active secretion, described as carrier and energy against the gradient. A third arrow points up for reabsorption, described as favouring the unionised form and set by urine pH and pKa. The tubular fluid channel leads out to urine, and a caption reads excretion equals filtration plus secretion minus reabsorption. The lower panel is a horizontal scale of the clearance ratio marked at zero for completely reabsorbed as for glucose, less than one for filtered then partially reabsorbed, equal to one for filtered only as for inulin, and greater than one for actively secreted as for PAH.](../rework/figures/out/ch06-renal-handling.png)

*Figure 6.1 — Top: the three renal processes acting on a drug. Filtration and secretion move drug towards the urine; reabsorption returns it to the blood, which is why it enters the balance with a minus sign. Bottom: what the clearance ratio reveals about which process dominates.*  
Original diagram, redrawn from the first edition pages 25 to 28 (original)

**Glomerular filtration** is passive. Small unionised or ionised free drug passes with the concentration gradient from blood to filtrate. Protein-bound drug does not, because the complex is too large to cross the glomerulus. Only free drug is filtered, which is why protein binding lowers renal clearance. Inulin is filtered and then neither secreted nor reabsorbed, so its clearance measures the
**glomerular filtration rate** itself, normally 125–130 mL·min⁻¹. Creatinine is the practical
substitute, because it is made steadily by muscle and needs no infusion, but it is *not* handled by
filtration alone: a share of it is secreted by the proximal tubule, so creatinine clearance runs above
the true GFR, typically by 10–20% and by more as renal function falls.

**Active tubular secretion** moves drug from blood into the tubular fluid against its concentration gradient, so it needs a carrier and energy. The kidney has two carrier systems, one for weak acids and one for weak bases. Drugs of similar structure compete for the same carrier, which is the basis of a real drug interaction: probenecid competes with penicillin and raises its concentration. Para-aminohippuric acid is secreted so efficiently that its clearance, 425–650 mL·min⁻¹, measures renal plasma flow.

**Tubular reabsorption** returns drug from the filtrate to the blood, and it favours the more lipid-soluble, unionised form. It may be active or passive. Glucose is reabsorbed completely, so its renal clearance is zero. For weak acids and weak bases the extent depends on urinary pH and on the pKa of the drug, because those two together fix how much of the drug is unionised at any moment.

> **Why It Matters in Practice:** Give amphetamine, a weak base, with a urinary alkaliniser and more of it stays unionised in the tubule, so more is reabsorbed and less appears in the urine. The same logic runs the other way in overdose: alkalinising the urine ionises a weak acid such as aspirin, traps it in the tubule and speeds its removal. Manipulating urinary pH is a treatment, and it is also a way of defeating a urine drug screen.

## 6.3 What Clearance Is

Chapter 2 introduced clearance as K·Vd. The definition behind that product is a rate divided by a concentration.

> **Key Equation:** Equation 6.2 — clearance, two equivalent forms
>
> $$Cl = \frac{\text{rate of drug elimination}}{C_p} = \frac{dD_e/dt}{C_p}$$
>
> $$Cl = K \cdot V_d = \frac{0.693\, V_d}{t_{1/2}}$$
>
> The first form is the definition; the second follows from it when elimination is first order.

The first form explains the units at once. Dividing µg·min⁻¹ by µg·mL⁻¹ leaves mL·min⁻¹, a volume per time. Clearance is therefore the volume of plasma from which drug is completely removed per unit time. If a penicillin has a clearance of 15 mL·min⁻¹ in a patient whose Vd is 12 L, then each minute 15 mL of those 12 L is stripped entirely of drug. No real volume of plasma is ever fully cleared; the figure is an equivalent volume, in the same spirit as the apparent volume of distribution.

> **Watch the Units:** Clearance is a volume per time and K is a reciprocal time. They are different quantities and they cannot be compared directly. A clearance of 5 has no meaning until the units are attached, because 5 mL·min⁻¹ and 5 L·h⁻¹ differ by a factor of about 17.

One consequence is worth stating early. In a two-compartment drug, Cl = K·Vp and renal clearance is Ke·Vp, where Vp is the central compartment volume. The number of compartments does not change the clearance, because clearance is a property of the organs doing the clearing.

## 6.4 The Clearance Family

Clearances by different routes add, because the organs work in parallel on the same blood.

> **Key Equation:** Equation 6.3 — additivity and its consequences
>
> $$Cl_T = Cl_r + Cl_{nr} \qquad \text{(total = renal + non-renal)}$$
>
> $$Cl_r = K_e V_d \qquad \text{and} \qquad Cl_{nr} = K_{nr} V_d$$
>
> $$f_e = \frac{D_u^\infty}{\text{dose reaching the circulation}} = \frac{K_e}{K} = \frac{Cl_r}{Cl_T}$$
>
> $$Cl_r = f_e\, Cl_T \qquad \text{and} \qquad Cl_{nr} = (1 - f_e)\, Cl_T$$
>
> where Knr is the non-renal elimination rate constant and fe is the fraction of the available dose
> excreted unchanged, the same fe defined in Chapter 3.

The non-renal term is written Cl_nr, not Cl_h, because the liver is usually the largest non-renal
route but never the only one: biliary, intestinal, pulmonary and other losses fall in the same term.
Writing Cl_T = Cl_r + Cl_h would silently assign every non-renal loss to the liver. Where the liver
genuinely is the whole of it, Cl_nr and Cl_h coincide.

> **Watch the Units:** In most of the pharmacokinetic literature fe means the *fraction unbound* in
> plasma, not the fraction excreted unchanged. This book uses fe for the fraction excreted unchanged
> throughout, in Chapter 3 and here, and does not use fu at all. If you meet fu in another text,
> check which quantity it names before putting it in an equation.

The symbol Kh is used deliberately. Chapter 10 needs Km for the Michaelis constant, which is a concentration and not a rate constant at all, and the two must not share a letter.

Two further routes to clearance come from areas rather than rate constants, and they are the ones Chapters 9 and 13 rely on:

Cl_T = D₀(IV) / AUC = F · D₀(oral) / AUC,   Cl_r = Du∞ / AUC,   Cl_f = Mu / AUC

where Mu is the total amount recovered as one metabolite. Cl_f is a *formation clearance*: the part of
total clearance that produces that metabolite. It is not the hepatic clearance, and calling it that
would claim three things the data do not show — that the liver made all of it, that no competing
pathway consumed the parent, and that one mole of parent gave one mole of the metabolite recovered.
Formation clearances for every metabolite, plus Cl_r, sum to Cl_T; a single metabolite's does not. A third route comes from an infusion at steady state, and it holds whatever the number of compartments:

Cl_T = R / Css

## 6.5 Measuring Renal Clearance

Two plots follow directly from Cl_r = (dDu/dt) / Cp.

*Rate against concentration.* Rearranged, dDu/dt = Cl_r · Cp. Plot the urinary excretion rate against the plasma concentration at the midpoint of the same interval, and the slope is renal clearance. A rapidly excreted drug gives a steep line, a slowly excreted one a shallow line.

*Cumulative amount against cumulative area.* Integrating both sides gives Du = Cl_r · AUC. Plot the cumulative amount excreted against the area under the plasma curve up to the same time, and the slope is again renal clearance. This version needs no rates and so no midpoint times, which makes it the more robust of the two.

## 6.6 Which Mechanism? The Clearance Ratio

Comparing a drug's renal clearance with the glomerular filtration rate reveals which of the three processes dominates. Inulin or creatinine clearance supplies the reference, since both are filtered only.

| Clearance ratio, Cl_drug / Cl_inulin | Dominant mechanism |
|---|---|
| Zero | Filtered, then completely reabsorbed, as for glucose |
| Less than 1 | Filtered, then partially reabsorbed |
| Equal to 1 | Filtered only |
| Greater than 1 | Actively secreted as well as filtered |

The ratio identifies the *net* result, not every process acting. A ratio of 1 is consistent with no secretion and no reabsorption, and equally with secretion and reabsorption that happen to cancel.

## 6.7 Why Clearance Rather Than Half-Life

Asked how fast a drug leaves the body, reach for clearance and not half-life. The reason is in Equation 6.2 read backwards:

t½ = 0.693 · Vd / Cl

Half-life depends on two independent things. A patient with oedema or obesity has an altered Vd, and a patient with renal or hepatic disease has an altered clearance. If both change, the half-life may not move at all while the body's capacity to remove the drug has changed substantially. Clearance isolates that capacity; half-life mixes it with distribution [2].

> **Worked Example:** Example 6.1 — the full clearance breakdown
>
> A 250 mg oral dose of an antibiotic is given to a 32-year-old man of 78 kg whose creatinine clearance is 122 mL·min⁻¹. The literature gives an apparent Vd of 21% of body weight and an elimination half-life of 2 h. The dose is 90% bioavailable, and 70% of the absorbed dose is recovered in urine as unchanged drug.
>
> Determine total, renal and non-renal clearance, and identify the probable renal mechanism.
>
> *Step 1 — Vd.*
>
> Vd = 0.21 × 78 kg = 16.4 L
>
> *Step 2 — K from the half-life.*
>
> K = 0.693 ÷ 2 h = 0.347 h⁻¹
>
> *Step 3 — total clearance.*
>
> Cl_T = K × Vd = 0.347 h⁻¹ × 16.4 L = 5.68 L·h⁻¹
>
> Converting: 5.68 L·h⁻¹ × 1000 ÷ 60 = 94.6 mL·min⁻¹.
>
> *Step 4 — the amount actually reaching the circulation.* Only the absorbed fraction can be cleared.
>
> absorbed dose = 0.90 × 250 mg = 225 mg
>
> *Step 5 — fe.* Of that absorbed dose, 70% appears unchanged in the urine.
>
> Du∞ = 0.70 × 225 mg = 157.5 mg, so fe = 157.5 ÷ 225 = 0.70
>
> Note that fe is 0.70 and not 0.63. It is a fraction of what reached the circulation, not of what was swallowed.
>
> *Step 6 — renal and non-renal clearance.*
>
> Cl_r = fe × Cl_T = 0.70 × 5.68 = 3.98 L·h⁻¹ = 66.2 mL·min⁻¹
>
> Cl_nr = Cl_T − Cl_r = 5.68 − 3.98 = 1.70 L·h⁻¹ = 28.4 mL·min⁻¹
>
> *Step 7 — the mechanism.* Creatinine clearance gives the filtration reference.
>
> clearance ratio = 66.2 ÷ 122 = 0.54
>
> *Answer.* Cl_T = 5.68 L·h⁻¹ (94.6 mL·min⁻¹), Cl_r = 3.98 L·h⁻¹ (66.2 mL·min⁻¹) and Cl_nr = 1.70 L·h⁻¹ (28.4 mL·min⁻¹). The clearance ratio of 0.54 is below 1, so the kidney's *net* handling of this drug removes less than filtration alone would.
>
> *What the ratio does not settle.* It is tempting to read 0.54 as reabsorption, and that is one explanation — but not the only one. The ratio compares Cl_r with the clearance of *total* drug at the glomerulus, while only unbound drug is filtered. A drug 46% bound to plasma protein would give a ratio near 0.54 with no reabsorption at all. The mechanism is separated only by comparing Cl_r with fe,unbound × GFR, and this exercise gives no binding data, so the honest answer is that net handling is below filtration and the cause is undetermined. A ratio *above* 1 is different: no amount of binding can push clearance above the filtration of total drug, so secretion is the only explanation, which is why Q2 can be answered and this one cannot.
>
> *Check the split.* Renal clearance is 70% of total, which is exactly fe, as Equation 6.3 requires. If your Cl_r came out above Cl_T, you have multiplied where you should have divided.

## Key Takeaways
- Net renal excretion is filtration plus secretion minus reabsorption.
- Only free drug is filtered, so protein binding lowers renal clearance.
- Inulin clearance measures GFR, about 125–130 mL·min⁻¹; creatinine clearance approximates it but reads high because creatinine is also secreted; PAH clearance measures renal plasma flow.
- Clearance is a rate of elimination divided by a concentration, so its units are volume per time.
- Clearances add: Cl_T = Cl_r + Cl_nr, and Cl_r = fe · Cl_T.
- fe is a fraction of the dose that reached the circulation, not of the dose given.
- Renal clearance is the slope of dDu/dt against Cp, or of Du against AUC.
- A clearance ratio above 1 proves active secretion. A ratio below 1 means net handling is below filtration of total drug, which may be reabsorption or simply plasma protein binding; the two are separated only by comparing Cl_r with the unbound fraction times GFR.
- Use clearance rather than half-life, because half-life also moves when Vd moves.

## Check Your Understanding

**Q1.** [LO1] Protein-bound drug is not removed by glomerular filtration because:
A) It is too lipid soluble to enter the filtrate.
B) The drug–protein complex is too large to cross the glomerulus.
C) It is actively reabsorbed in the proximal tubule.
D) Binding prevents the drug from reaching the kidney.

**Q2.** [LO5] A drug has a renal clearance of 300 mL·min⁻¹ and the patient's creatinine clearance is 120 mL·min⁻¹. The drug is:
A) Filtered only
B) Completely reabsorbed
C) Actively secreted in addition to being filtered
D) Partially reabsorbed after filtration

**Q3.** [LO2] Which set of units is correct for clearance?
A) mL·min⁻¹
B) min⁻¹
C) mg·mL⁻¹
D) mg·min⁻¹

**Q4.** [LO3] A drug has Cl_T = 8 L·h⁻¹ and fe = 0.25. Its non-renal clearance is:
A) 2 L·h⁻¹
B) 0.25 L·h⁻¹
C) 32 L·h⁻¹
D) 6 L·h⁻¹

**Q5.** [LO4] A plot of the cumulative amount of drug excreted in urine against the cumulative AUC of the plasma curve gives a straight line. Its slope is:
A) The renal excretion rate constant
B) The total body clearance
C) The renal clearance
D) The fraction excreted unchanged

**Q6.** [LO5] Why is clearance preferred to half-life as a measure of the body's ability to remove a drug?
A) Clearance is easier to measure experimentally.
B) Half-life depends on Vd as well as clearance, so it can stay constant while clearance changes.
C) Half-life is undefined for drugs following two-compartment kinetics.
D) Clearance is independent of the route of administration.

**Q7.** [LO1] Giving a weak base with a urinary alkaliniser will:
A) Increase its renal clearance, because more is ionised in the tubule
B) Leave its renal clearance unchanged, since pH affects only weak acids
C) Increase its active secretion by the basic carrier system
D) Decrease its renal clearance, because more is unionised and so reabsorbed

**Q8.** [LO3] A 200 mg IV dose gives a total clearance of 6 L·h⁻¹, and 50 mg is recovered unchanged in urine. The renal clearance is:
A) 1.5 L·h⁻¹
B) 24 L·h⁻¹
C) 4.5 L·h⁻¹
D) 0.25 L·h⁻¹

**Q9.** [LO2] For a drug following two-compartment kinetics, total body clearance is:
A) Larger than for a one-compartment drug with the same K
B) Dependent on K₁₂ and K₂₁
C) K · Vp, and unaffected by the number of compartments
D) Impossible to determine without tissue samples

**Q10.** [LO3] During a constant IV infusion at steady state, clearance can be obtained as:
A) Css / R
B) R / Css
C) R × Css
D) R × Vd

### Exercises

**E6.1** [LO3] A new antibiotic is actively secreted by the kidney. Its Vd is 35 L in a normal adult and its clearance is 650 mL·min⁻¹. Calculate the usual half-life, and the half-life in an adult with partial renal failure whose clearance is only 75 mL·min⁻¹. Comment on how the two answers are related.

**E6.2** [LO4] To estimate renal clearance in a patient, urine is collected for the 2 h after a dose and found to contain 200 mg of drug. A midpoint plasma sample taken at 1 h contains 2.5 mg%. Calculate the renal clearance in both L·h⁻¹ and mL·min⁻¹.

**E6.3** [LO3] A single 100 mg oral dose of a drug is given and is completely systemically available. Urine collection recovers 60 mg of unchanged drug and 30 mg of metabolite. The drug has t½ = 3.3 h and Vd = 1000 mL. Determine Cl_T, Cl_r and Cl_nr, stating explicitly the assumption you make about the 10 mg that was not recovered, and show how the answer would differ under one alternative assumption.

## Answers and Worked Solutions

**Q1. B** — Filtration is a size-limited passive process, so only free drug crosses. Option D is wrong because bound drug does reach the kidney; it simply is not filtered.

**Q2. C** — A clearance ratio of 300/120 = 2.5 exceeds 1, and filtration alone cannot exceed GFR. The extra must come from active secretion.

**Q3. A** — Clearance is a rate divided by a concentration, so its units are volume per time. Option B is a rate constant and D a rate.

**Q4. D** — Cl_nr = (1 − fe) × Cl_T = 0.75 × 8 = 6 L·h⁻¹. Option A is the renal clearance instead.

**Q5. C** — Integrating Cl_r = (dDu/dt)/Cp gives Du = Cl_r · AUC, so the slope is renal clearance. This version avoids rates and midpoint times altogether.

**Q6. B** — t½ = 0.693·Vd/Cl, so a rise in Vd and a fall in clearance can offset one another and leave the half-life looking normal. This is the situation in oedema and in obesity.

**Q7. D** — An alkaline urine keeps a weak base unionised, and the unionised form is the one that is reabsorbed. Less drug therefore appears in the urine.

**Q8. A** — fe = 50/200 = 0.25, so Cl_r = 0.25 × 6 = 1.5 L·h⁻¹. Option B divides the clearance by fe instead of multiplying.

**Q9. C** — Clearance is a property of the clearing organs, so the compartmental description does not alter it. In two-compartment form it is K·Vp rather than K·Vd.

**Q10. B** — Css = R/Cl, so Cl = R/Css. This holds for one and two compartments alike.

---

**E6.1 — worked solution**

*Step 1 — convert the clearance.* 650 mL·min⁻¹ × 60 ÷ 1000 = 39.0 L·h⁻¹.

*Step 2 — K, then the usual half-life.*

K = Cl ÷ Vd = 39.0 L·h⁻¹ ÷ 35 L = 1.114 h⁻¹

t½ = 0.693 ÷ 1.114 = 0.62 h, or about 37 min

*Step 3 — the impaired patient.* 75 mL·min⁻¹ = 4.5 L·h⁻¹, and Vd is unchanged at 35 L.

K = 4.5 ÷ 35 = 0.1286 h⁻¹

t½ = 0.693 ÷ 0.1286 = 5.39 h

*Answer.* About 0.62 h normally, and 5.39 h in partial renal failure.

*How the two are related.* Clearance fell by a factor of 650/75 = 8.67, and the half-life rose by 5.39/0.62 = 8.67. At constant Vd the half-life is exactly inversely proportional to clearance, so the two factors must match. Checking that they do is a quick test of the arithmetic.

**E6.2 — worked solution**

*Step 1 — the excretion rate.*

dDu/dt = 200 mg ÷ 2 h = 100 mg·h⁻¹

*Step 2 — convert the plasma concentration.* The unit mg% means mg per 100 mL.

Cp = 2.5 mg / 100 mL = 25 mg·L⁻¹

*Step 3 — renal clearance.*

Cl_r = 100 mg·h⁻¹ ÷ 25 mg·L⁻¹ = 4.0 L·h⁻¹

*Step 4 — convert.* 4.0 L·h⁻¹ × 1000 ÷ 60 = 66.7 mL·min⁻¹.

*Answer.* Cl_r = 4.0 L·h⁻¹, which is 66.7 mL·min⁻¹.

*Why the sample was taken at 1 h.* The excretion rate is an average across the 0–2 h interval, so it must be paired with the plasma concentration at the midpoint of that interval, exactly as in Chapter 3. Pairing it with the concentration at 2 h would give a plasma value that is too low and a clearance that is too high.

**E6.3 — worked solution**

*Step 1 — K and total clearance.*

K = 0.693 ÷ 3.3 h = 0.210 h⁻¹

Cl_T = K × Vd = 0.210 h⁻¹ × 1.0 L = 0.210 L·h⁻¹ = 3.5 mL·min⁻¹

*Step 2 — account for the dose.* The drug is completely systemically available, so all 100 mg reached the circulation. Recovery was 60 mg unchanged plus 30 mg as metabolite, which is 90 mg. Ten milligrams is unaccounted for.

*Step 3 — state the assumption.* The calculation of fe needs a denominator, and the honest choice must be declared. Assume that the urine collection of *unchanged* drug was complete, so Du∞ = 60 mg, and that the missing 10 mg left by a non-renal route not measured here, such as further metabolism, biliary excretion, or a metabolite the assay did not detect. Then:

fe = 60 mg ÷ 100 mg = 0.60

*Step 4 — the split.*

Cl_r = 0.60 × 0.210 = 0.126 L·h⁻¹ = 2.1 mL·min⁻¹

Cl_nr = 0.210 − 0.126 = 0.084 L·h⁻¹ = 1.4 mL·min⁻¹

*Step 5 — the alternative assumption.* Suppose instead the collection was incomplete and the 90 mg recovered is representative of the whole. Then fe = 60/90 = 0.667, giving Cl_r = 0.140 L·h⁻¹ and Cl_nr = 0.070 L·h⁻¹, a renal clearance 11% higher.

*Answer.* Cl_T = 0.210 L·h⁻¹. Under the stated assumption, Cl_r = 0.126 L·h⁻¹ and Cl_nr = 0.084 L·h⁻¹. Under the alternative, Cl_r = 0.140 L·h⁻¹ and Cl_nr = 0.070 L·h⁻¹.

*Why the assumption must be written down.* The two answers differ by more than a tenth, and nothing in the data decides between them. A mass-balance gap is a result in its own right, and reporting fe without saying which denominator produced it hides a real uncertainty behind a precise-looking number. Where a study matters, it is resolved by collecting until recovery is complete rather than by choosing a denominator.

## References
1. Shargel L, Yu ABC. *Applied Biopharmaceutics and Pharmacokinetics*. 8th ed. New York: McGraw Hill Medical; 2022.
2. Rowland M, Tozer TN. *Clinical Pharmacokinetics and Pharmacodynamics: Concepts and Applications*. 5th ed. Philadelphia: Wolters Kluwer; 2019.


---

# Chapter 7: Oral Absorption

## Learning Objectives
By the end of this chapter you will be able to:
1. [LO1] Distinguish zero-order from first-order absorption and name a dosage form giving each.
2. [LO2] Write the oral plasma equation, identify its terms, and calculate tmax and Cpmax.
3. [LO3] Determine Ka by the method of residuals, and recognise when the method has failed.
4. [LO4] Apply the Wagner–Nelson method to decide the order of an absorption process.
5. [LO5] Explain lag time and flip-flop, and predict the effect of dose, Ka and K on Cpmax, tmax and AUC.

## 7.1 Two Kinds of Input

An oral dose must be released, dissolved and then absorbed before any of Chapter 2 applies. The absorption step can follow either of two kinetic patterns, and the pattern is set by the dosage form.

**Zero-order absorption** delivers drug to the blood at a constant rate, independent of how much is left in the gut. An osmotic pump does this, and so does a well-designed sustained-release tablet. Kinetically it is the oral equivalent of the infusion in Chapter 5.

**First-order absorption** delivers drug at a rate proportional to the amount still in solution in the gut, so the rate falls as the gut empties of drug. Rapidly dissolving forms behave this way: immediate-release tablets and capsules, suppositories, and aqueous intramuscular injections [1].

This chapter treats the first-order case in detail, because it is the commoner one and because its analysis generalises. Two assumptions carry over from Chapter 2: the body is one compartment, and elimination is first order with no distribution phase.

The amount remaining in the gut falls exponentially:

D_GI = D₀ · e^(−Ka·t)

where **Ka** is the **absorption rate constant** and D₀ is the oral dose. The rate at which drug enters the body is F·Ka·D_GI, where F is the fraction of the dose absorbed.

## 7.2 The Shape of the Oral Curve

The body now gains drug by absorption and loses it by elimination at the same time:

dD_B/dt = F · Ka · D₀ · e^(−Ka·t) − K · D_B

Integrating gives the equation that describes every first-order oral plasma curve.

> **Key Equation:** Equation 7.1 — the oral plasma curve
>
> Cp = [F · Ka · D₀ / (Vd · (Ka − K))] · (e^(−Kt) − e^(−Ka·t))
>
> which is written compactly as
>
> Cp = A · (e^(−Kt) − e^(−Ka·t)),   where   A = F · Ka · D₀ / (Vd · (Ka − K))
>
> and therefore   Vd = F · Ka · D₀ / (A · (Ka − K)).

Two exponentials again, but subtracted rather than added. That difference is what makes the curve rise from zero, turn over, and then fall. Early on the second term dominates and the concentration climbs. Later the second term dies away faster, because Ka is normally larger than K, and the equation collapses to:

Cp = A · e^(−Kt)

which is an ordinary first-order decline. The straight terminal portion on semilog axes is therefore the **post-absorption phase**, and its slope is −K/2.303, exactly as in Chapter 2.

> **Common Mistake:** Reading the terminal slope as Ka. It is K. Absorption has finished by then, which is precisely why the line is straight. Ka has to be recovered by subtraction, and Section 7.4 does it.

## 7.3 tmax and Cpmax

Differentiating Equation 7.1 and setting the derivative to zero gives the time of the peak.

> **Key Equation:** Equation 7.2 — time of the peak
>
> $$t_{max} = \frac{\ln(K_a / K)}{K_a - K}$$
>
> Neither the dose nor Vd nor F appears. tmax depends on the two rate constants alone.

Calculate tmax from Equation 7.2 rather than reading it off the graph. A plasma curve is flat near its peak, so the graphical estimate is imprecise: in the dataset of Example 7.1 the measured concentration is 39.6 µg·mL⁻¹ at both 6 h and 8 h.

Cpmax then follows by substituting tmax back into Equation 7.1. Unlike tmax, it is proportional to the dose.

> **Watch the Units:** Ka and K both have units of reciprocal time, so Ka − K in the denominator of A is also a reciprocal time. Multiplying by Ka on top leaves A with the units of D₀/Vd, a concentration. If A comes out with stray time units, you have mixed hours and minutes between the two constants.

## 7.4 Finding Ka by the Method of Residuals

The procedure is the one from Chapter 4, with one sign change. There the two exponentials were added and the residual was measured minus extrapolated. Here they are subtracted, so the residual is *extrapolated minus measured*.

1. Plot log Cp against time and fit the terminal straight portion. Its slope gives K and its back-extrapolated intercept gives A.
2. For each early point, read the extrapolated value Cp′ off the extended line.
3. Form the residual Cp′ − Cp and plot its logarithm against time. The slope is −Ka/2.303.

If the residual line is not straight, something in the analysis is wrong — but not necessarily the assumption of first-order absorption. Curvature can come from a terminal window chosen too early, from flip-flop kinetics, from multi-compartment disposition, or from absorption that genuinely is not first order. Example 7.1 shows the first of these: its residual line curves, yet the data are generated by first-order absorption throughout. Diagnose the cause before discarding the model.

![Two panels. On the left, a semilogarithmic plot of an oral plasma curve rising to a peak near seven hours and then falling. A dashed line fitted to the points from sixteen hours onwards is extrapolated back to an intercept marked A approximately 105. Open squares below it show the residuals, which follow a visibly curved path rather than a straight line. On the right, the apparent absorption rate constant calculated from each successive pair of residuals is plotted against the midpoint of the pair; the values climb steadily from 0.25 to 0.36 per hour, well above a dashed reference line at the true value of 0.200 per hour.](../rework/figures/out/ch07-oral-feathering.png)

*Figure 7.1 — Feathering the oral curve of Example 7.1, and the sign that it has not worked. The residuals do not fall on a straight line, and the apparent Ka taken from successive pairs climbs steadily instead of scattering about one value. Ka here is only twice K, so the two exponentials never separate and no terminal window is free of absorption.*  
Original diagram, drawn from the first edition Example 22 dataset, page 33 (original)

> **Worked Example:** Example 7.1 — feathering an oral curve, and checking the result
>
> A 50 kg patient receives a single oral dose of 10 mg·kg⁻¹, of which 80% is absorbed. Plasma concentrations in µg·mL⁻¹ are:
>
> | t (h) | 2 | 4 | 6 | 8 | 10 | 12 | 14 |
> |---|---|---|---|---|---|---|---|
> | Cp | 23.7 | 35.4 | 39.6 | 39.6 | 37.2 | 33.7 | 29.7 |
>
> | t (h) | 16 | 18 | 20 | 22 | 24 | 26 | 28 |
> |---|---|---|---|---|---|---|---|
> | Cp | 25.8 | 22.1 | 18.7 | 15.8 | 13.2 | 11.0 | 9.14 |
>
> Find Ka, t½, tmax, Vd, Cpmax and the concentration at 11 h.
>
> *Step 1 — the dose.* 10 mg·kg⁻¹ × 50 kg = 500 mg, and F = 0.80.
>
> *Step 2 — terminal slope, from the points at 16 h and beyond.*
>
> K = [ln 25.8 − ln 9.14] ÷ (28 − 16) = (3.250 − 2.213) ÷ 12 = 0.0865 h⁻¹
>
> Back-extrapolating gives A ≈ 105 µg·mL⁻¹.
>
> *Step 3 — the residuals, using Cp′ = 105·e^(−0.0865t).*
>
> | t (h) | 2 | 4 | 6 | 8 | 10 | 12 |
> |---|---|---|---|---|---|---|
> | Cp′ | 88.3 | 74.2 | 62.4 | 52.5 | 44.1 | 37.1 |
> | Cp′ − Cp | 64.6 | 38.9 | 22.8 | 12.9 | 6.9 | 3.4 |
>
> *Step 4 — read the residual slope, and stop.* Taking successive pairs gives Ka = 0.254, 0.266, 0.286, 0.310 and 0.356 h⁻¹. These are not scatter about one value; they climb steadily. The residual line is curved, so the method has not worked.
>
> *Step 5 — diagnose it.* A curved residual line means the terminal line was not clean: absorption was still contributing where the line was fitted. Test that directly. If Ka were about 0.25 h⁻¹, the absorption term at 16 h would be A·e^(−Ka·16), which is roughly 6 µg·mL⁻¹ against a measured 25.8, or a quarter of it. The "post-absorption" phase had not begun.
>
> *Step 6 — fit both exponentials together instead.* Doing so gives a curve passing through every point to within 0.1 µg·mL⁻¹:
>
> K = 0.100 h⁻¹, Ka = 0.200 h⁻¹, A = 160 µg·mL⁻¹
>
> *Step 7 — the answers follow.*
>
> t½ = 0.693 ÷ 0.100 = 6.93 h
>
> tmax = ln(0.200 / 0.100) ÷ (0.200 − 0.100) = 0.693 ÷ 0.100 = 6.93 h
>
> Cpmax = 160 × (e^(−0.693) − e^(−1.386)) = 160 × (0.500 − 0.250) = 40.0 µg·mL⁻¹
>
> Vd = F·Ka·D₀ / (A·(Ka − K)) = (0.80 × 0.200 × 500) ÷ (160 × 0.100) = 80 ÷ 16 = 5.0 L
>
> Cp at 11 h = 160 × (e^(−1.10) − e^(−2.20)) = 160 × (0.3329 − 0.1108) = 35.5 µg·mL⁻¹
>
> *Answer.* Ka = 0.200 h⁻¹, t½ = 6.93 h, tmax = 6.93 h, Vd = 5.0 L, Cpmax = 40.0 µg·mL⁻¹ and Cp(11 h) = 35.5 µg·mL⁻¹.
>
> *Check by two routes.* The fitted Cpmax of 40.0 matches the measured 39.6 at the flat top of the curve. And the AUC computed from the constants, A/K − A/Ka = 1600 − 800 = 800 µg·h·mL⁻¹, equals F·D₀/Cl = 400 mg ÷ 0.5 L·h⁻¹ = 800 mg·h·L⁻¹.
>
> *Why feathering failed here.* Ka is only twice K. The two exponentials therefore decay at comparable rates and never separate cleanly, so no terminal window in this study is free of absorption. Feathering needs Ka to be several times K. The curving residual line is the warning sign, and it is the reason Step 4 stops rather than averaging five disagreeing numbers into one.

## 7.5 The Wagner–Nelson Method

Feathering assumes first-order absorption before it begins. The **Wagner–Nelson method** assumes nothing about absorption at all, which is why it can be used to decide the order. It assumes only that the body is one compartment and that elimination is first order, so K must be known accurately.

The reasoning is a mass balance. At any time, the amount absorbed equals the amount still in the body plus the amount already eliminated:

Ab = Cp·Vd + K·Vd·(AUC)₀ᵗ

At infinite time the body is empty, so Ab∞ = K·Vd·(AUC)₀^∞. Dividing one by the other cancels Vd.

> **Key Equation:** Equation 7.3 — fraction unabsorbed
>
> $$\frac{Ab}{Ab_\infty} = \frac{C_p + K (AUC)_0^t}{K (AUC)_0^\infty}$$
>
> and the **fraction unabsorbed** is 1 − Ab/Ab∞.

Plot the fraction unabsorbed against time both ways. A straight line on *semilog* axes means first-order absorption, with slope −Ka/2.303. A straight line on *ordinary* axes means zero-order absorption. Use only the points up to tmax; beyond it the fraction unabsorbed is a small difference between large numbers and scatters badly.

> **Worked Example:** Example 7.2 — deciding the order of absorption
>
> A tablet containing 100 mg of drug is given to a healthy volunteer. Plasma concentrations in µg·mL⁻¹ are 0.6, 1.2, 1.8, 2.3, 3.4, 4.3 and 6.0 at 0.25, 0.5, 0.75, 1, 1.5, 2 and 3 h, then 5.6, 2.3, 0.9 and 0.4 at 6, 12, 18 and 24 h.
>
> Does absorption follow first-order or zero-order kinetics?
>
> *Step 1 — K from the terminal points.* Using 6 h and 24 h:
>
> K = [ln 5.6 − ln 0.4] ÷ 18 = (1.723 + 0.916) ÷ 18 = 0.147 h⁻¹, so t½ = 4.7 h
>
> *Step 2 — cumulative AUC by the trapezoidal rule*, starting from zero at time zero. The tail beyond the last point is Cp_last/K = 0.4 ÷ 0.147 = 2.73, giving (AUC)₀^∞ = 64.29 + 2.73 = 67.02 µg·h·mL⁻¹.
>
> *Step 3 — the denominator.* K × (AUC)₀^∞ = 0.147 × 67.02 = 9.83 µg·mL⁻¹.
>
> *Step 4 — the table, working only to tmax at 3 h.*
>
> | t (h) | Cp | (AUC)₀ᵗ | K·(AUC)₀ᵗ | Ab/Vd | Ab/Ab∞ | 1 − Ab/Ab∞ |
> |---|---|---|---|---|---|---|
> | 0.25 | 0.6 | 0.08 | 0.01 | 0.61 | 0.062 | 0.938 |
> | 0.50 | 1.2 | 0.30 | 0.04 | 1.24 | 0.127 | 0.873 |
> | 0.75 | 1.8 | 0.68 | 0.10 | 1.90 | 0.193 | 0.807 |
> | 1.00 | 2.3 | 1.19 | 0.17 | 2.47 | 0.252 | 0.748 |
> | 1.50 | 3.4 | 2.61 | 0.38 | 3.78 | 0.385 | 0.615 |
> | 2.00 | 4.3 | 4.54 | 0.67 | 4.97 | 0.505 | 0.495 |
> | 3.00 | 6.0 | 9.69 | 1.42 | 7.42 | 0.755 | 0.245 |
>
> *Step 5 — test first order.* Take logarithms of the last column and read successive slopes: 0.285, 0.318, 0.301, 0.392, 0.436 and 0.704 h⁻¹. They rise by a factor of two and a half. The semilog plot is not a straight line, so absorption is not first order.
>
> *Step 6 — test zero order.* Take ordinary differences of the last column per hour instead: 0.258, 0.267, 0.234, 0.267, 0.241 and 0.250. These agree to within a few per cent about a constant 0.25 per hour.
>
> *Answer.* Absorption is **zero order**. The fraction unabsorbed falls linearly at 0.25 per hour, so absorption is complete at 1 ÷ 0.25 = 4 h. There is no first-order Ka to report, and quoting one would be wrong.
>
> *A note on units.* The first edition tabulated these concentrations as mg·mL⁻¹. At that scale a 100 mg tablet would have to produce 6 mg in every millilitre of plasma, which is 6 g·L⁻¹ — more drug in the plasma than was swallowed. The values are µg·mL⁻¹, and every derived column above inherits that unit: (AUC)₀ᵗ in µg·h·mL⁻¹, K·(AUC)₀ᵗ and Ab/Vd in µg·mL⁻¹, and the last two columns dimensionless.
>
> *What could not be found.* Vd cannot be obtained here. Ab∞/Vd = 9.83 µg·mL⁻¹ gives only the ratio F·D₀/Vd, so F and Vd cannot be separated from oral data alone. Either F must be known independently, or Vd must come from an intravenous study.

## 7.6 Lag Time

**Lag time** is the delay between administration and the start of absorption. Slow gastric emptying or reduced intestinal motility will cause it, as will anything else that stops absorption beginning at once.

It shows on a feathered plot as two different intercepts: the elimination line and the residual line no longer meet on the vertical axis, but cross at some time t₀. The curve is then described by shifting the whole time axis:

Cp = A · [e^(−K(t − t₀)) − e^(−Ka(t − t₀))]

> **Common Mistake:** Treating lag time as the onset of action. They are different quantities and lag time is always the shorter. Absorption begins at t₀, but the concentration must then climb from zero to the minimum effective concentration before any effect appears. Onset of action is the time at which the curve crosses the MEC, which is later than t₀ and depends on the dose.

## 7.7 Flip-Flop

Equation 7.1 is symmetric in Ka and K: exchanging the two constants leaves the curve unchanged. The plasma data alone therefore cannot say which constant is which, and the usual assumption that the terminal slope is K can be exactly wrong.

**Flip-flop** is the name for that situation, and it occurs whenever K is greater than Ka. The terminal phase is then controlled by the slower process, which is absorption, so the terminal slope gives Ka and the residual line gives K.

Suspect it in two cases. A rapidly eliminated drug, with K above about 0.69 h⁻¹, has a good chance of eliminating faster than it absorbs. A sustained-release formulation deliberately slows absorption, and can slow it below elimination.

The resolution is experimental, not algebraic [2]. Give the drug intravenously, where there is no absorption at all, and measure K directly. If the intravenous K matches the terminal slope from the oral study, there is no flip-flop; if it matches the residual slope instead, there is. For one such drug the intravenous study gives K = 1.72 h⁻¹, while the oral feathering gives a terminal slope of 0.7 h⁻¹ and a residual slope of 1.72 h⁻¹ — so Ka is 0.7 h⁻¹ and the labels must be exchanged.

## 7.8 What Changes What

| Change | Cpmax | tmax | AUC |
|---|---|---|---|
| Double the dose | Doubles | Unchanged | Doubles |
| Increase Ka, K constant | Increases | Decreases | Unchanged |
| Increase K, Ka constant | Decreases | Decreases | Decreases |

The middle row is the one worth dwelling on. Absorbing a drug faster raises the peak and brings it forward, but does not change the total amount that reaches the circulation, so the AUC is unmoved. This is the quantitative form of the distinction Chapter 1 drew: tmax and Cpmax describe the *rate* of absorption, AUC describes its *extent*. Chapter 13 makes both the basis of bioequivalence.

> **Why It Matters in Practice:** Two formulations of the same drug at the same dose can have identical AUC and still behave differently. A faster-absorbing one produces a higher peak, which matters when the peak approaches the minimum toxic concentration, and an earlier peak, which matters for an analgesic. Equal extent is not equal performance, which is why bioequivalence tests both Cmax and AUC.

## Key Takeaways
- Zero-order absorption delivers a constant amount per unit time; first-order absorption a constant fraction.
- Cp = A·(e^(−Kt) − e^(−Ka·t)). The terminal slope is −K/2.303, not Ka.
- tmax = ln(Ka/K)/(Ka − K) and depends on the two rate constants alone, never on the dose.
- Feathering gives Ka from the residual line. Here the residual is extrapolated minus measured.
- A curved residual line means the method has failed, usually because Ka is not several times K.
- Wagner–Nelson assumes nothing about absorption, so it can decide the order: linear on semilog axes means first order, linear on ordinary axes means zero order.
- Use Wagner–Nelson points only up to tmax.
- Lag time is not onset of action; onset is later and depends on the dose.
- Flip-flop occurs when K exceeds Ka, and only intravenous data can settle it.
- Doubling the dose doubles Cpmax and AUC but leaves tmax alone.

## Check Your Understanding

**Q1.** [LO2] In the equation Cp = A·(e^(−Kt) − e^(−Ka·t)), the slope of the terminal straight portion on semilog axes gives:
A) −K/2.303
B) Ka − K
C) Ka
D) −Ka/2.303

**Q2.** [LO1] Which dosage form is most likely to show zero-order absorption?
A) A rectal suppository
B) An immediate-release capsule
C) An aqueous intramuscular injection
D) An osmotic pump tablet

**Q3.** [LO3] In the method of residuals applied to an oral curve, the residual at each early time is:
A) The measured concentration minus the extrapolated terminal value
B) The difference between two successive measured concentrations
C) The concentration remaining in the gut
D) The extrapolated terminal value minus the measured concentration

**Q4.** [LO4] A Wagner–Nelson plot of the fraction unabsorbed against time is a straight line on ordinary axes but curved on semilog axes. Absorption is:
A) Zero order
B) First order
C) Not occurring
D) Impossible to classify from these data

**Q5.** [LO5] Flip-flop kinetics should be suspected when:
A) The drug is given intravenously.
B) Absorption is much faster than elimination.
C) Elimination is faster than absorption, as in a sustained-release form.
D) The plasma curve shows a lag time.

**Q6.** [LO3] A student's residual line curves upwards, giving apparent Ka values that climb steadily from 0.25 to 0.36 h⁻¹. The best conclusion is:
A) The assay drifted during the later samples.
B) Absorption and elimination have not separated, so feathering cannot be used here.
C) The residual values should be averaged to give Ka = 0.30 h⁻¹.
D) The drug follows two-compartment kinetics.

**Q7.** [LO5] Lag time differs from onset of action because:
A) Onset of action occurs later, when the concentration first exceeds the MEC.
B) Lag time is measured from the peak rather than from dosing.
C) Onset of action is independent of the dose.
D) Lag time applies only to intravenous administration.

**Q8.** [LO2] A drug has Ka = 0.6 h⁻¹ and K = 0.15 h⁻¹. Its tmax is:
A) 4.6 h
B) 1.5 h
C) 0.75 h
D) 3.1 h

**Q9.** [LO4] Which assumption does the Wagner–Nelson method require?
A) Absorption is first order.
B) The drug is given intravenously.
C) Elimination is first order and K is known accurately.
D) The terminal phase has been sampled to ten half-lives.

**Q10.** [LO5] Two formulations of the same drug at the same dose give the same AUC, but formulation X has a higher Cpmax and an earlier tmax than formulation Y. It follows that:
A) X delivers more drug to the circulation than Y.
B) X is absorbed faster than Y, but to the same extent.
C) X has a larger volume of distribution than Y.
D) X is eliminated more slowly than Y.

### Exercises

**E7.1** [LO2] A drug has Ka = 0.35 h⁻¹, K = 0.07 h⁻¹, Vd = 20 L and F = 0.75. A 400 mg oral dose is given. Calculate A, tmax and Cpmax, then state which of the three would change if the dose were raised to 800 mg.

**E7.2** [LO4] Using the constants found in Example 7.1 (A = 160 µg·mL⁻¹, Ka = 0.200 h⁻¹, K = 0.100 h⁻¹), calculate the AUC by the equation AUC = A/K − A/Ka, and confirm it independently from the dose and the clearance. Then calculate what the AUC would be if a reformulation doubled Ka to 0.400 h⁻¹, and comment.

**E7.3** [LO5] An oral study of a drug gives a terminal slope corresponding to 0.30 h⁻¹ and a residual slope corresponding to 1.20 h⁻¹. A separate intravenous study in the same volunteers gives an elimination half-life of 35 minutes. Identify Ka and K, state whether flip-flop is present, and explain what would have been concluded from the oral data alone.

## Answers and Worked Solutions

**Q1. A** — By the terminal phase the absorption term has decayed, leaving Cp = A·e^(−Kt), whose base-10 logarithmic slope is −K/2.303. Option D is the slope of the residual line.

**Q2. D** — An osmotic pump releases drug at a constant rate set by the device, not by how much remains, which is the definition of zero order. The other three dissolve rapidly and deliver a constant *fraction* per unit time.

**Q3. D** — The two exponentials are subtracted in an oral curve, so the extrapolated line lies above the measured points and the residual is taken in that order. Option A is the rule for the two-compartment curve of Chapter 4, where the terms are added.

**Q4. A** — Linearity on ordinary axes means the fraction unabsorbed falls by a constant amount per unit time, which is zero order. First order would be linear on semilog axes instead.

**Q5. C** — Flip-flop arises when K exceeds Ka, so the terminal phase reflects the slower absorption. Sustained-release forms slow absorption deliberately and are a common cause.

**Q6. B** — A systematic climb is not random scatter. It means the terminal line still contained absorption, so subtracting it left a residual contaminated with elimination. Averaging, as in C, would hide the problem rather than solve it.

**Q7. A** — Absorption starts at t₀, but the concentration must then climb to the MEC before an effect appears, so onset is always later than lag time and falls as the dose rises.

**Q8. D** — tmax = ln(0.6/0.15) ÷ (0.6 − 0.15) = ln 4 ÷ 0.45 = 1.386 ÷ 0.45 = 3.08 h. Option A divides ln 4 by K alone.

**Q9. C** — The method makes no assumption about absorption, which is what lets it determine the order, but it depends entirely on a correct K, since K multiplies every AUC term.

**Q10. B** — Equal AUC means equal extent of absorption. A higher and earlier peak means a faster rate. This is precisely the rate-versus-extent distinction that bioequivalence tests.

---

**E7.1 — worked solution**

*Step 1 — A.*

A = F·Ka·D₀ / (Vd·(Ka − K)) = (0.75 × 0.35 × 400) ÷ (20 × (0.35 − 0.07))

A = 105 ÷ (20 × 0.28) = 105 ÷ 5.6 = 18.75 mg·L⁻¹

*Step 2 — tmax.*

tmax = ln(0.35 / 0.07) ÷ (0.35 − 0.07) = ln 5 ÷ 0.28 = 1.609 ÷ 0.28 = 5.75 h

*Step 3 — Cpmax.* Substitute tmax into Equation 7.1. With K·tmax = 0.4025 and Ka·tmax = 2.0125:

Cpmax = 18.75 × (e^(−0.4025) − e^(−2.0125)) = 18.75 × (0.6686 − 0.1337) = 18.75 × 0.5349

Cpmax = 10.0 mg·L⁻¹

*Step 4 — doubling the dose.* A is proportional to D₀, so it doubles to 37.5 mg·L⁻¹, and Cpmax doubles with it to 20.0 mg·L⁻¹. tmax contains no dose term and is unchanged at 5.75 h.

*Answer.* A = 18.75 mg·L⁻¹, tmax = 5.75 h, Cpmax = 10.0 mg·L⁻¹. Doubling the dose doubles A and Cpmax and leaves tmax at 5.75 h.

*Check.* Cpmax must be smaller than A, since the bracket in Equation 7.1 is always less than 1. Here 10.0 is a little over half of 18.75, which is the expected size.

**E7.2 — worked solution**

*Step 1 — AUC from the constants.*

AUC = A/K − A/Ka = (160 ÷ 0.100) − (160 ÷ 0.200) = 1600 − 800 = 800 µg·h·mL⁻¹

*Step 2 — the independent check.* Chapter 6 gives Cl = K·Vd, and Example 7.1 found Vd = 5.0 L.

Cl = 0.100 h⁻¹ × 5.0 L = 0.50 L·h⁻¹

The amount reaching the circulation is F·D₀ = 0.80 × 500 mg = 400 mg.

AUC = F·D₀ / Cl = 400 mg ÷ 0.50 L·h⁻¹ = 800 mg·h·L⁻¹ = 800 µg·h·mL⁻¹

The two agree.

*Step 3 — doubling Ka.* A itself depends on Ka, so it must be recalculated:

A = F·Ka·D₀ / (Vd·(Ka − K)) = (0.80 × 0.400 × 500) ÷ (5.0 × 0.300) = 160 ÷ 1.5 = 106.7 µg·mL⁻¹

AUC = 106.7/0.100 − 106.7/0.400 = 1067 − 267 = 800 µg·h·mL⁻¹

*Answer.* AUC = 800 µg·h·mL⁻¹ by both routes, and it is still 800 µg·h·mL⁻¹ after Ka is doubled.

*Comment.* The second route shows why. AUC = F·D₀/Cl contains no Ka at all, so absorption rate cannot change it. Doubling Ka changes how quickly the drug arrives, raising Cpmax and bringing tmax forward, but the same 400 mg still reaches the circulation and the same clearance still removes it.

**E7.3 — worked solution**

*Step 1 — what the intravenous study gives.* There is no absorption after an intravenous dose, so its terminal slope is K itself.

K = 0.693 ÷ 35 min = 0.693 ÷ 0.583 h = 1.19 h⁻¹

*Step 2 — match it against the oral constants.* The oral study produced 0.30 h⁻¹ from the terminal line and 1.20 h⁻¹ from the residual line. The intravenous K of 1.19 h⁻¹ matches the *residual* slope, not the terminal one.

*Step 3 — assign the constants.*

K = 1.20 h⁻¹ and Ka = 0.30 h⁻¹

*Step 4 — is this flip-flop?* K exceeds Ka, so yes. Elimination is four times faster than absorption, and the terminal phase is therefore governed by the rate at which drug is still arriving.

*Answer.* Ka = 0.30 h⁻¹ and K = 1.20 h⁻¹. Flip-flop is present.

*What the oral data alone would have given.* The usual assumption assigns the terminal slope to K, which would have given K = 0.30 h⁻¹ and a half-life of 2.3 h instead of the true 35 min — four times too long. A dosing interval built on that figure would be four times longer than it should be, and the concentration would fall below the MEC between doses. Equation 7.1 is symmetric in Ka and K, so no amount of analysis of the oral curve can resolve this; only the intravenous study can.

## References
1. Shargel L, Yu ABC. *Applied Biopharmaceutics and Pharmacokinetics*. 8th ed. New York: McGraw Hill Medical; 2022.
2. Rowland M, Tozer TN. *Clinical Pharmacokinetics and Pharmacodynamics: Concepts and Applications*. 5th ed. Philadelphia: Wolters Kluwer; 2019.


---

# Chapter 8: Multiple Dose Regimens

## Learning Objectives
By the end of this chapter you will be able to:
1. [LO1] Explain why repeated doses accumulate, and state when they do not.
2. [LO2] Calculate the accumulation index and the fraction of a dose remaining after one dosage interval.
3. [LO3] Calculate the maximum, minimum and average amounts and concentrations at steady state after repeated intravenous doses.
4. [LO4] Derive the accumulation half-life and use it to predict how long steady state takes.
5. [LO5] Design a dose or a dosage interval that gives a chosen average steady-state concentration.

## 8.1 Why Doses Accumulate

Antibiotics and antirheumatics are given as a series of doses. What happens to the concentration depends on how much of the previous dose remains when the next one arrives. Give a second dose a week after the first, and the first has long since been eliminated. The second curve is a copy of the first, and nothing accumulates.

Give the second dose while some of the first remains, and the two add. Each new dose starts from a higher baseline than the last. The peaks climb, the troughs climb, and the climb slows as it goes. Eventually the amount eliminated during each interval equals the amount given at its start. From then on every interval is a copy of the one before. That repeating pattern is steady state for a multiple dose regimen [1].

![A sawtooth plasma concentration curve over 36 hours. A dose every 6 hours produces a vertical jump followed by an exponential fall. The first peak is 50 micrograms per millilitre; later peaks rise towards a dashed line at 66.7 and troughs towards a dashed line at 16.7, with a third dashed line at the average of 36.1. A dotted curve shows the first dose alone decaying to near zero.](../rework/figures/out/ch08-accumulation.png)

*Figure 8.1 — Repeated IV bolus doses of Example 8.1. Each dose adds to what the previous doses left, so peaks and troughs climb until the loss in one interval equals one dose. The average level lies below the midpoint of peak and trough.*  
Original diagram, redrawn from the first edition pages 39-40 (original)

Two numbers control the result. The first is the size of each dose, D₀. The second is the **dosage interval**, τ, the time from one dose to the next. Everything in this chapter is a function of D₀, τ and the elimination rate constant K.

## 8.2 What a Regimen Must Achieve

A continuous infusion gives a flat plateau, as Chapter 5 showed. Repeated doses give a plateau that swings. At steady state the concentration rises to a maximum, Css,max, just after each dose. It then falls to a minimum, Css,min, just before the next.

A good regimen puts both ends of that swing inside the therapeutic range. Css,max must stay below the minimum toxic concentration, or the patient is exposed to toxicity once in every interval. Css,min must stay above the minimum effective concentration, or the drug stops working for part of every interval.

> **Why It Matters in Practice:** Two regimens can deliver the same total daily dose and behave very differently. A drug given as 1200 mg once a day swings far more widely than the same drug given as 300 mg every 6 hours. The once-daily peak may cross the toxic threshold and its trough may fall below the effective one.

The rest of this chapter assumes a one-compartment drug given by repeated intravenous bolus, with first order elimination, a constant dose and a constant interval. Section 8.5 notes which results also hold for oral doses.

## 8.3 The Accumulation Index

Each dose adds D₀ to whatever the previous doses left behind. After one interval the fraction of a dose still in the body is:

f = e^(−Kτ)

This fraction depends on K and τ only. It does not depend on the size of the dose. A long interval makes f small, because most of each dose has gone before the next arrives.

The amounts left by earlier doses simply add. This is the **principle of superposition**, and it holds whenever elimination is first order. Immediately after the nth dose the amount in the body is the dose just given plus what remains of every earlier one:

D_max,n = D₀ (1 + f + f² + … + f^(n−1))

That is a geometric series. Its sum is D₀(1 − fⁿ)/(1 − f). As n grows, fⁿ shrinks towards zero, because f is less than 1. The peak therefore approaches a limit rather than growing without end.

> **Key Equation:** Equation 8.1 — the accumulation index
>
> $$R = \frac{C_{ss,max}}{C_{max,1}} = \frac{1}{1 - e^{-K\tau}}$$
>
> where Cmax,1 is the peak after the first dose, D₀/Vd, and Css,max is the peak at steady state.

The **accumulation index**, R, measures how much higher the steady-state peak is than the first peak. R = 1 means no accumulation. R > 1 means the drug accumulates. Like f, it depends on K and τ and not on the dose.

Consider a drug given once every half-life, so that Kτ = 0.693 and f = 0.5. Then R = 1/(1 − 0.5) = 2. The steady-state peak is twice the first peak. Give the same drug every two half-lives and f = 0.25, so R = 1.33. Halving the frequency cut the accumulation from twofold to one third.

> **Watch the Units:** K and τ must be in the same time unit, because their product sits in an exponent. An exponent must be a pure number. K = 0.231 h⁻¹ with τ = 6 h gives Kτ = 1.39. Entering τ as 360 min with K still in h⁻¹ gives Kτ = 83, a fraction remaining of essentially zero and an accumulation index of exactly 1. The answer looks reasonable and is wrong.

## 8.4 How Long Steady State Takes

Chapter 5 found that a constant infusion reaches any given fraction of steady state in a fixed number of half-lives. Repeated doses behave the same way, and the reason can be derived rather than assumed.

*Step 1 — the area in one interval.* Consider the area under the curve during the nth interval. By superposition it is the sum of the pieces contributed by every dose given so far. The first dose contributes its area between (n − 1)τ and nτ. The second contributes its area between (n − 2)τ and (n − 1)τ, and so on back to the latest dose, which contributes its area between 0 and τ. Laid end to end, these pieces make up the area of a single-dose curve from 0 to nτ.

*Step 2 — the area at steady state.* At steady state the same argument covers every dose back to the beginning. The area in one interval is then the whole single-dose area, AUC from 0 to ∞.

*Step 3 — the fraction of steady state.* Divide one by the other. The fraction of steady state reached in the interval that ends at t = nτ is:

f_ss = AUC(0 → t) / AUC(0 → ∞) of one dose

This is exact, and it holds for any route.

*Step 4 — the intravenous case.* For a bolus, AUC(0 → t) / AUC(0 → ∞) = 1 − e^(−Kt). That is Equation 5.1 read as a fraction, and it gives the table of Chapter 5 unchanged: 50% at one half-life, 90% at 3.32, 95% at 4.32 and 99% at 6.65.

*Step 5 — the oral case.* For a first order absorption curve with Ka > K, the single-dose fraction of area is:

f_ss = 1 − [Ka · e^(−Kt) − K · e^(−Ka·t)] / (Ka − K)

Because Ka > K, the term in e^(−Ka·t) dies away much faster than the term in e^(−Kt). Well before half of steady state is reached it is negligible. Drop it, set f_ss = 0.5, and rearrange:

e^(−Kt) = 0.5 · (Ka − K) / Ka

t = [ln 2 + ln(Ka / (Ka − K))] / K

*Step 6 — express it in half-lives.* Divide through by t½ = ln 2 / K. Then use ln x / ln 2 = log x / log 2, and 1 / log 2 = 3.32.

> **Key Equation:** Equation 8.2 — the accumulation half-life
>
> $$t_{1/2,acc} = t_{1/2}\left[1 + 3.32 \log\frac{K_a}{K_a - K}\right]$$
>
> valid when Ka > K, so that the absorption exponential can be neglected.

The **accumulation half-life** is the time taken to reach half of the steady-state level. For an oral drug it is longer than the elimination half-life, because the drug must first be absorbed. The slower the absorption relative to elimination, the larger the bracket.

*Step 7 — the intravenous collapse.* An intravenous bolus is absorption that is instantaneous, so Ka → ∞. K is then negligible beside Ka, and Ka / (Ka − K) → 1. The logarithm of 1 is 0, so the second term in the bracket vanishes and the bracket becomes 1:

t½,acc = t½ · [1 + 3.32 × 0] = t½

For repeated intravenous doses, the accumulation half-life equals the elimination half-life. It depends on neither the dose nor the interval.

The assumption Ka > K is not decoration. If Ka < K, then Ka − K is negative and the logarithm has no real value. The derivation then fails at Step 5, because the slower exponential is now the absorption one and it is the elimination term that should have been dropped. This is the flip-flop situation, in which the terminal slope of the curve reflects absorption rather than elimination. Equation 8.2 must not be used there.

> **Common Mistake:** Shortening the interval to reach steady state sooner. The time to steady state is set by the half-life. Doubling the dose, or halving the interval, raises the plateau without bringing it any closer. If a drug is given once every half-life, reaching 99% of steady state takes 6.65 half-lives, and so about seven doses, whatever the size of each dose.

## 8.5 Amounts and Concentrations at Steady State

The limit of the geometric series in Section 8.3 gives the steady-state peak directly. The trough follows because one interval of first order decline multiplies the peak by f. The difference between them is exactly one dose, which is the amount given at the start of each interval to replace what was lost.

> **Key Equation:** Equation 8.3 — amounts at steady state, repeated IV bolus
>
> D_max = D₀ / (1 − f)    D_min = D_max · f    D_max − D_min = D₀
>
> with f = e^(−Kτ). Divide each amount by Vd to obtain the concentration:
>
> $$C_{ss,max} = \frac{D_0 / V_d}{1 - e^{-K\tau}} \qquad C_{ss,min} = C_{ss,max}\, e^{-K\tau}$$

The ratio of peak to trough is Css,max / Css,min = e^(Kτ). A short interval relative to the half-life keeps the swing small. A long interval makes it large.

The average level needs a different argument. Step 2 of Section 8.4 showed that the area under the curve in one steady-state interval equals the area under a single-dose curve. The single-dose area is F·D₀ / (K·Vd), from Chapter 2. The average concentration over the interval is that area divided by its length, τ.

> **Key Equation:** Equation 8.4 — average steady-state concentration and amount
>
> Css,av = F · D₀ / (K · Vd · τ) = F · D₀ / (Cl · τ)
>
> D_av = F · D₀ / (K · τ) = 1.44 · F · D₀ · t½ / τ
>
> The factor 1.44 is 1/0.693.

The **average steady-state concentration** is the constant level that would give the same area over one interval. It is not the arithmetic mean of the peak and the trough. The concentration falls exponentially, quickly at first and slowly later, so it spends more of each interval near the trough than near the peak. The true average therefore lies below the midpoint.

Equation 8.4 holds for oral doses as well, since it depends only on areas. F corrects for incomplete bioavailability, and F = 1 for an intravenous dose. It also shows that the average level depends on the dosing rate, D₀/τ, and on the clearance. Doubling D₀ and doubling τ together leaves Css,av unchanged, although the swing about it grows. Equation 8.3, by contrast, assumes each dose enters the body at once, and holds only for the intravenous bolus.

> **Worked Example:** Example 8.1 — steady state on repeated IV doses
>
> A patient receives 1000 mg of an antibiotic every 6 hours by repeated intravenous injection. The elimination half-life is 3 hours, the drug follows a one-compartment model, and Vd = 20 L.
>
> Find the maximum, minimum and average amounts in the body at steady state, and the corresponding plasma concentrations.
>
> *Step 1 — K.*
>
> K = 0.693 ÷ 3 h = 0.231 h⁻¹
>
> *Step 2 — Kτ and the fraction remaining.* Both are in hours, so the product is a pure number.
>
> Kτ = 0.231 h⁻¹ × 6 h = 1.386
>
> f = e^(−1.386) = 0.250
>
> The interval is exactly two half-lives, so one quarter of each dose remains when the next is given.
>
> *Step 3 — maximum amount.*
>
> D_max = 1000 mg ÷ (1 − 0.250) = 1000 mg ÷ 0.750 = 1333 mg
>
> *Step 4 — minimum amount.*
>
> D_min = 1333 mg × 0.250 = 333 mg
>
> *Step 5 — average amount.*
>
> D_av = 1000 mg ÷ (0.231 h⁻¹ × 6 h) = 1000 mg ÷ 1.386 = 722 mg
>
> *Step 6 — concentrations.* Divide each amount by Vd = 20 L.
>
> Css,max = 1333 mg ÷ 20 L = 66.7 mg·L⁻¹ = 66.7 µg·mL⁻¹
>
> Css,min = 333 mg ÷ 20 L = 16.7 µg·mL⁻¹
>
> Css,av = 722 mg ÷ 20 L = 36.1 µg·mL⁻¹
>
> *Answer.* At steady state the body holds between 333 mg and 1333 mg of drug, with an average of 722 mg. The plasma concentration swings between 16.7 and 66.7 µg·mL⁻¹, with an average of 36.1 µg·mL⁻¹.
>
> *Check by a second route.* The peak minus the trough must be one dose: 1333 − 333 = 1000 mg, as Equation 8.3 requires. The average by the half-life form of Equation 8.4 is 1.44 × 1000 mg × 3 h ÷ 6 h = 720 mg. That matches Step 5 to within the rounding of 1.44. Finally, the average lies below the arithmetic midpoint of (1333 + 333) ÷ 2 = 833 mg, as it must for an exponential decline. An average above the midpoint would signal an error.
>
> *What it means.* The accumulation index is 1 ÷ 0.750 = 1.33, so the steady-state peak is one third higher than the first peak of 50 µg·mL⁻¹. With a 3 h half-life, 95% of steady state is reached by 4.32 × 3 = 13 h, which is during the third interval.

## 8.6 Designing a Regimen

Equation 8.4 is the design equation. Rearranged, it gives the dose needed for a chosen average level at a chosen interval:

D₀ = Css,av · Cl · τ / F = Css,av · K · Vd · τ / F

Or it gives the interval for a chosen dose:

τ = F · D₀ / (Css,av · Cl)

The designer fixes τ first, from the half-life and the width of the therapeutic range. A narrow range needs a short interval, so the swing stays small. The dose then follows from the target average. The last step is to check the swing with Equation 8.3, confirming that Css,max stays below the minimum toxic concentration and that Css,min stays above the minimum effective concentration.

> **Deeper Dive:** If Vd is proportional to body weight and the dose is given per kilogram, the weight cancels from Equation 8.4. A regimen of 1 mg·kg⁻¹ then gives the same average level at 60 kg as at 90 kg. This holds only while K is unchanged, and renal impairment changes it [2].

## Key Takeaways
- Repeated doses accumulate whenever part of the previous dose remains when the next is given.
- The fraction of a dose left after one interval is f = e^(−Kτ); it depends on K and τ, not on the dose.
- The accumulation index is R = 1/(1 − e^(−Kτ)); R = 2 when the drug is given once every half-life.
- The accumulation half-life is t½·[1 + 3.32·log(Ka/(Ka − K))], valid for Ka > K.
- For IV dosing Ka → ∞, log 1 = 0, and the accumulation half-life equals the elimination half-life.
- Time to steady state depends on the half-life only; 95% at 4.32 half-lives and 99% at 6.65.
- At steady state D_max = D₀/(1 − f), D_min = D_max·f, and their difference is one dose.
- Css,av = F·D₀/(Cl·τ); it is lower than the arithmetic mean of peak and trough.
- Choose τ for an acceptable swing, then choose D₀ for the target average.

## Check Your Understanding

**Q1.** [LO1] A second dose of a drug is given one week after the first, and the half-life is 4 h. The second plasma curve will:
A) Start from a higher baseline than the first
B) Be a copy of the first, with no accumulation
C) Reach a peak twice as high as the first
D) Reach steady state immediately

**Q2.** [LO2] A drug is given by IV bolus at an interval equal to its elimination half-life. The accumulation index is:
A) 0.5
B) 1.0
C) 1.44
D) 2.0

**Q3.** [LO4] For repeated intravenous bolus doses, the accumulation half-life equals:
A) The dosage interval
B) The elimination half-life
C) Twice the elimination half-life
D) The elimination half-life multiplied by the accumulation index

**Q4.** [LO3] At steady state on a regimen of 200 mg every τ hours by IV bolus, the maximum amount in the body is 800 mg. The minimum amount in the body is:
A) 160 mg
B) 400 mg
C) 600 mg
D) 1000 mg

**Q5.** [LO5] The average steady-state plasma concentration during a multiple dose regimen is given by:
A) Css,av = F · D₀ / (Cl · τ)
B) Css,av = (Css,max + Css,min) / 2
C) Css,av = D₀ / (Vd · (1 − e^(−Kτ)))
D) Css,av = F · D₀ · τ / Cl

**Q6.** [LO2] The accumulation index of a drug given by repeated IV bolus depends on:
A) The dose only
B) The dose and the volume of distribution
C) The elimination rate constant and the dosage interval
D) The volume of distribution and the dosage interval

**Q7.** [LO4] A drug is given every half-life by IV bolus. About how many doses are needed to reach 99% of steady state?
A) 2
B) 3
C) 5
D) 7

**Q8.** [LO3] The average amount of drug in the body at steady state is less than the arithmetic mean of D_max and D_min because:
A) The amount falls exponentially and spends more of each interval near the trough
B) Part of each dose is never absorbed
C) The volume of distribution increases during each interval
D) Elimination becomes zero order at high amounts

**Q9.** [LO1] The interval is halved and the dose is halved, so that the dosing rate D₀/τ is unchanged. At steady state:
A) The average concentration is halved
B) The accumulation index is unchanged
C) Steady state is reached in half the time
D) The swing between peak and trough is smaller, and the average concentration is unchanged

**Q10.** [LO5] The dose of a drug is doubled while the interval stays the same. Compared with before:
A) The average steady-state level is unchanged and steady state arrives sooner
B) The average steady-state level is doubled and steady state arrives sooner
C) The average steady-state level is doubled and the time to steady state is unchanged
D) The accumulation index is doubled

### Exercises

**E8.1** [LO5] For clindamycin, DeHaan and co-workers reported K = 0.247 h⁻¹, t½ = 2.81 h and Vd = 43.9 L per 1.73 m². A patient of 1.73 m² takes 150 mg orally every 6 hours for a week, and the drug is completely absorbed. Calculate the average steady-state concentration, and state why a week of dosing is enough to call it steady state.

**E8.2** [LO5] Regamey and associates reported an elimination half-life of 2.15 h for tobramycin and a volume of distribution of 33.5% of body weight. (a) Calculate the IV dose every 8 hours that gives an average steady-state level of 2.5 µg·mL⁻¹ in an 80 kg patient. (b) The manufacturer recommends 1 mg·kg⁻¹ every 8 hours. Calculate the average steady-state level this regimen gives, and explain why the answer is the same for any body weight.

**E8.3** [LO4] An oral drug has Ka = 1.0 h⁻¹ and K = 0.1 h⁻¹. Calculate its elimination half-life and its accumulation half-life. Verify the result by substituting it back into the exact expression for the fraction of steady state.

## Answers and Worked Solutions

**Q1. B** — After a week the first dose has passed through 42 half-lives and none of it remains. The second dose starts from zero, so its curve is a copy of the first.

**Q2. D** — With τ = t½, f = e^(−0.693) = 0.5, and R = 1/(1 − 0.5) = 2. Option C is the factor 1/0.693 from Equation 8.4, not an accumulation index.

**Q3. B** — For a bolus Ka → ∞, so Ka/(Ka − K) → 1. Since log 1 = 0, the bracket in Equation 8.2 collapses to 1.

**Q4. C** — The peak minus the trough is exactly one dose, so D_min = 800 − 200 = 600 mg. Option A multiplies the dose by an arbitrary fraction instead of using that difference.

**Q5. A** — The average is the steady-state area in one interval divided by τ, and that area equals F·D₀/Cl. Option B is the arithmetic mean, which overestimates it; option C is the steady-state peak.

**Q6. C** — R = 1/(1 − e^(−Kτ)) contains only K and τ. The dose cancels because every dose accumulates in the same proportion.

**Q7. D** — Ninety-nine per cent takes 6.65 half-lives, and with τ = t½ that is about seven doses.

**Q8. A** — An exponential decline falls fastest at the start of the interval. The amount therefore spends longer near D_min than near D_max, which pulls the time-average below the midpoint.

**Q9. D** — Css,av depends on D₀/τ and on clearance, both unchanged. The peak-to-trough ratio is e^(Kτ), which falls when τ is shortened. Option B is wrong because R depends on τ.

**Q10. C** — Css,av is proportional to D₀, so it doubles. The time to steady state is set by the rate constants, not the dose, so it does not change — by t½ alone for an IV regimen, and by Ka as well after oral doses (Equation 8.2).

---

**E8.1 — worked solution**

*Step 1 — the clearance.* For a patient of 1.73 m², Vd = 43.9 L.

Cl = K × Vd = 0.247 h⁻¹ × 43.9 L = 10.84 L·h⁻¹

*Step 2 — the average steady-state concentration.* F = 1.

Css,av = 150 mg ÷ (10.84 L·h⁻¹ × 6 h) = 150 mg ÷ 65.1 L = 2.31 mg·L⁻¹

*Step 3 — is a week enough?* One week is 168 h, and 168 ÷ 2.81 = 60 half-lives. Steady state is 99% reached after 6.65 half-lives, so after a week the regimen is at steady state by a wide margin.

*Answer.* Css,av = 2.31 µg·mL⁻¹.

*Check by a second route.* The half-life form gives 1.44 × 150 mg × 2.81 h ÷ (43.9 L × 6 h) = 607 ÷ 263 = 2.31 µg·mL⁻¹. The two routes agree, which also confirms that the reported K and t½ are consistent with each other.

**E8.2 — worked solution**

*Step 1 — Vd and K.*

Vd = 0.335 × 80 kg = 26.8 L

K = 0.693 ÷ 2.15 h = 0.322 h⁻¹

*Step 2 — clearance.*

Cl = 0.322 h⁻¹ × 26.8 L = 8.64 L·h⁻¹

*Step 3 — part (a), the dose.* A target of 2.5 µg·mL⁻¹ is 2.5 mg·L⁻¹, and F = 1 for an IV dose.

D₀ = Css,av × Cl × τ = 2.5 mg·L⁻¹ × 8.64 L·h⁻¹ × 8 h = 173 mg

*Step 4 — part (b), the manufacturer's regimen.* For 80 kg, 1 mg·kg⁻¹ is 80 mg.

Css,av = 80 mg ÷ (8.64 L·h⁻¹ × 8 h) = 80 mg ÷ 69.1 L = 1.16 µg·mL⁻¹

*Answer.* (a) About 173 mg every 8 hours. (b) About 1.16 µg·mL⁻¹, less than half the target of part (a).

*Check by a second route.* Css,av is proportional to the dose, so 2.5 × 80 ÷ 173 = 1.16 µg·mL⁻¹, as found.

*Why body weight does not matter.* Both the dose and Vd are proportional to weight. Written per kilogram, Css,av = 1 mg·kg⁻¹ ÷ (0.335 L·kg⁻¹ × 0.322 h⁻¹ × 8 h) = 1.16 mg·L⁻¹. The kilograms cancel, so every patient with this K gets the same average level.

**E8.3 — worked solution**

*Step 1 — the elimination half-life.*

t½ = 0.693 ÷ 0.1 h⁻¹ = 6.93 h

*Step 2 — the bracket.* Ka > K, so Equation 8.2 applies.

Ka ÷ (Ka − K) = 1.0 ÷ 0.9 = 1.111

log 1.111 = 0.0458, and 3.32 × 0.0458 = 0.152

*Step 3 — the accumulation half-life.*

t½,acc = 6.93 h × (1 + 0.152) = 7.98 h

*Answer.* The elimination half-life is 6.93 h and the accumulation half-life is about 8.0 h. Slower-than-instant absorption adds about an hour.

*Check by substitution.* At t = 7.98 h, Kt = 0.798 and e^(−0.798) = 0.450. The retained term is 1.111 × 0.450 = 0.500, so f_ss = 1 − 0.500 = 0.500. The dropped term is (0.1 ÷ 0.9) × e^(−7.98) = 0.111 × 0.00034 = 0.00004. It is far too small to matter, which confirms that neglecting it was justified.

## References
1. Shargel L, Yu ABC. *Applied Biopharmaceutics and Pharmacokinetics*. 8th ed. New York: McGraw Hill Medical; 2022.
2. Rowland M, Tozer TN. *Clinical Pharmacokinetics and Pharmacodynamics: Concepts and Applications*. 5th ed. Philadelphia: Wolters Kluwer; 2019.


---

# Chapter 9: Non-Compartmental Analysis

## Learning Objectives
By the end of this chapter you will be able to:
1. [LO1] State what a non-compartmental analysis assumes, and what it does not.
2. [LO2] Calculate AUC and AUMC from plasma data by the trapezoidal rule, including the extrapolated tails.
3. [LO3] Calculate mean residence time, clearance and the steady-state volume of distribution from AUC and AUMC.
4. [LO4] Relate mean residence, transit and absorption times to the elimination and absorption rate constants.
5. [LO5] Compare non-compartmental with compartmental analysis, and explain why the number of compartments belongs to the data.

## 9.1 Analysis Without a Model

Chapters 2 to 8 fitted the plasma curve to a model. One compartment gave a single exponential, two compartments gave two, and every parameter came from the fitted constants. That works well when the model is right. It raises an awkward question when the data do not clearly choose between models.

**Non-compartmental analysis** avoids that question. It obtains pharmacokinetic parameters from the areas under the plasma curve, without fitting the data to any compartmental model [1]. Only one assumption is needed: the kinetics are linear. Every dose must produce a curve of the same shape, scaled by the dose. Chapter 10 describes what happens when that fails.

The method treats the time course of drug in the body statistically. Think of the dose as a very large number of molecules, each entering the body, staying for a while, and leaving. Each molecule has its own residence time. The plasma curve describes how those residence times are distributed across the whole dose. A **statistical moment** is a summary of that distribution, and the first two moments carry most of the useful information.

## 9.2 Moments of the Curve: AUC and AUMC

The zero moment is the area under the plasma concentration curve, AUC, which earlier chapters have used already. The first moment comes from a second curve. Multiply each concentration by its time, plot Cp·t against t, and take the area under that. The result is the **AUMC**, the area under the first moment curve.

> **Key Equation:** Equation 9.1 — the two moments
>
> $$AUC = \int_0^\infty C_p\, dt \qquad \text{(zero moment)}$$
>
> $$AUMC = \int_0^\infty C_p\, t\, dt \qquad \text{(first moment)}$$
>
> AUC has units of concentration × time, such as mg·h·L⁻¹. AUMC has units of concentration × time², such as mg·h²·L⁻¹.

Both areas are measured in two parts. The part from zero to the last sample, tn, comes from the data by the trapezoidal rule. Each interval contributes its width multiplied by the mean of the two values at its ends. The part beyond tn has no data, so it is extrapolated from the terminal slope.

> **Key Equation:** Equation 9.2 — the extrapolated tails
>
> $$AUC(t_n \to \infty) = \frac{C_n}{\lambda_z}$$
>
> $$AUMC(t_n \to \infty) = \frac{t_n C_n}{\lambda_z} + \frac{C_n}{\lambda_z^2}$$
>
> where Cn is the last measured concentration and λz is the terminal rate constant, 2.303 × the magnitude of the terminal slope on a log₁₀ plot.

The AUMC tail has a second term, and that term matters. Multiplying by t gives heavy weight to late times. The first moment curve rises, peaks and then falls much more slowly than Cp itself. A larger share of AUMC than of AUC lies beyond the last sample, so AUMC is the more sensitive of the two to how long sampling continued.

![Two side-by-side plots over 0 to 36 hours. Left: plasma concentration falls exponentially from about 8.6 milligrams per litre, with seven measured points; a thin shaded sliver beyond the last sample at 18 hours is labelled tail 4.5 percent of AUC. Right: concentration multiplied by time rises to a peak near 6 hours and falls slowly; the shaded region beyond 18 hours is much larger and is labelled tail 19 percent of AUMC. A dashed vertical line marks the last sample in each plot.](../rework/figures/out/ch09-moments.png)

*Figure 9.1 — The two moment curves for Example 9.1. Multiplying by time shifts weight to late times, so the part of AUMC beyond the last sample is four times larger, as a share, than the part of AUC. AUMC, and everything derived from it, depends on how long sampling continued.*  
Original diagram, drawn from the first edition data on page 45 (original)

> **Watch the Units:** λz² appears in the AUMC tail, so the term Cn/λz² has units of mg·L⁻¹ ÷ h⁻² = mg·h²·L⁻¹. That matches the rest of AUMC. If the tail comes out in mg·h·L⁻¹, one factor of λz is missing.

## 9.3 Mean Residence Time and the Times Built From It

Dividing the first moment by the zero moment gives the mean of the distribution. For drug in the body, that mean is a time.

> **Key Equation:** Equation 9.3 — mean residence time
>
> $$MRT = \frac{AUMC}{AUC}$$
>
> For a one-compartment drug given by IV bolus, MRT = 1/K, so t½ = 0.693 · MRT.

**Mean residence time** is the average time the molecules of a dose spend in the body. It is measured after an instantaneous intravenous dose, so that every molecule starts its residence at the same moment. MRT reflects the elimination process: a short MRT means rapid elimination. It plays the same role in non-compartmental analysis as the elimination half-life does in the one-compartment model.

The relation MRT = 1/K holds only for a single exponential. For a multi-exponential curve, MRT still exists and is still AUMC/AUC. It just no longer equals the reciprocal of any one rate constant. Exercise E9.3 shows this for the two-compartment drug of Chapter 4.

After an oral dose, the average time a molecule spends in the body is longer. It must first be absorbed, and time spent at the absorption site adds to its time in the body. The area ratio after an oral dose therefore gives the **mean transit time**, MTT, for a non-instantaneous input. Subtracting the intravenous MRT removes the time spent in the body and leaves the time spent getting in.

> **Key Equation:** Equation 9.4 — mean absorption time
>
> $$MAT = MRT_{oral} - MRT_{IV}$$
>
> For first order absorption, MAT = 1/Ka, so the absorption half-life is 0.693 · MAT.

The **mean absorption time** is the average time molecules spend at the absorption site before entering the systemic circulation. It needs both an oral and an intravenous study in the same subjects.

There is one caution about MAT. It is the mean time for molecules that are absorbed. If part of the dose is degraded or lost in the gut, those molecules never arrive and never enter the average. The average time spent at the absorption site can then differ from the average time of arrival in the blood. That difference is one reason MAT is interpreted alongside F, from Chapter 13, and not in isolation.

## 9.4 Clearance and the Steady-State Volume

Clearance needs only the zero moment. For an intravenous dose, Cl = D₀/AUC, which Chapter 6 introduced. The volume needs both moments.

> **Key Equation:** Equation 9.5 — volume of distribution at steady state
>
> $$V_{ss} = Cl \cdot MRT = \frac{D_0\, AUMC}{AUC^2} \qquad \text{(IV bolus)}$$

The **volume of distribution at steady state**, Vss, is the volume that relates the amount in the body to the plasma concentration when distribution is at equilibrium, as during a long infusion. It needs no model. For a one-compartment drug it equals Vd, because MRT = 1/K and Cl/K = Vd. For a multi-compartment drug it lies above the central volume, because the drug also occupies the tissues.

> **Worked Example:** Example 9.1 — a non-compartmental analysis
>
> A 300 mg IV bolus is given and plasma concentrations are measured. This is the dataset of Chapter 2, analysed now without a model.
>
> | t (h) | 0 | 0.25 | 0.5 | 1.0 | 3.0 | 6.0 | 12.0 | 18.0 |
> |---|---|---|---|---|---|---|---|---|
> | Cp (mg·L⁻¹) | 8.57 | 8.21 | 7.87 | 7.23 | 5.15 | 3.09 | 1.11 | 0.40 |
>
> The value at zero time is the back-extrapolated Cp⁰ from Chapter 2. The terminal rate constant is λz = 0.170 h⁻¹, from the same chapter.
>
> Find AUC, AUMC, MRT, Cl and Vss.
>
> *Step 1 — the Cp·t column, in mg·h·L⁻¹.* Multiply each Cp by its time: 0, 2.05, 3.94, 7.23, 15.45, 18.54, 13.32, 7.20.
>
> *Step 2 — AUC from 0 to 18 h.* Each trapezoid is the interval width times the mean of its two ends.
>
> | Interval (h) | AUC piece (mg·h·L⁻¹) | AUMC piece (mg·h²·L⁻¹) |
> |---|---|---|
> | 0–0.25 | 2.10 | 0.26 |
> | 0.25–0.5 | 2.01 | 0.75 |
> | 0.5–1 | 3.78 | 2.79 |
> | 1–3 | 12.38 | 22.68 |
> | 3–6 | 12.36 | 50.99 |
> | 6–12 | 12.60 | 95.58 |
> | 12–18 | 4.53 | 61.56 |
> | Total | 49.75 | 234.61 |
>
> *Step 3 — the AUC tail.*
>
> AUC(18 → ∞) = 0.40 mg·L⁻¹ ÷ 0.170 h⁻¹ = 2.35 mg·h·L⁻¹
>
> AUC = 49.75 + 2.35 = 52.11 mg·h·L⁻¹
>
> *Step 4 — the AUMC tail.* There are two terms.
>
> 18 h × 0.40 mg·L⁻¹ ÷ 0.170 h⁻¹ = 42.35 mg·h²·L⁻¹
>
> 0.40 mg·L⁻¹ ÷ (0.170 h⁻¹)² = 0.40 ÷ 0.0289 = 13.84 mg·h²·L⁻¹
>
> AUMC = 234.61 + 42.35 + 13.84 = 290.80 mg·h²·L⁻¹
>
> Nearly a fifth of AUMC is extrapolated, against under a twentieth of AUC.
>
> *Step 5 — MRT.*
>
> MRT = 290.80 ÷ 52.11 = 5.58 h
>
> *Step 6 — clearance.*
>
> Cl = 300 mg ÷ 52.11 mg·h·L⁻¹ = 5.76 L·h⁻¹
>
> *Step 7 — Vss.*
>
> Vss = 5.76 L·h⁻¹ × 5.58 h = 32.1 L
>
> *Answer.* AUC = 52.1 mg·h·L⁻¹, AUMC = 291 mg·h²·L⁻¹, MRT = 5.58 h, Cl = 5.76 L·h⁻¹ and Vss = 32.1 L.
>
> *Check by a second route.* Chapter 2 fitted these data to one compartment and found K = 0.170 h⁻¹, Vd = 35.0 L and Cl = 5.96 L·h⁻¹. The model predicts MRT = 1/K = 5.88 h and Vss = Vd = 35.0 L. The non-compartmental values are 3% low for clearance, 5% low for MRT and 8% low for Vss. The fault is not in the model. It is in the linear trapezoid over the wide intervals from 3 to 18 h. A straight chord across a falling exponential curve lies above the curve, so each wide trapezoid overstates its area. The 6–12 h piece alone is 12.60 by trapezoid but 11.60 for the true exponential. The model-free method is only as good as its sampling.

## 9.5 Strengths and Limits

Non-compartmental analysis is widely used because it asks so little of the data. Its limits follow from the same fact.

| Advantages | Disadvantages |
|---|---|
| Needs fewer assumptions than a compartmental fit | Gives no number of compartments to describe disposition |
| Avoids choosing between models the data cannot separate | Cannot show organ-specific elimination |
| Gives Cl, Vss and MRT for any linear drug | Cannot relate its parameters to physiological quantities |
| Uses the same calculation for every drug | Cannot show drug–drug or drug–nutrient interactions |
| | Is sensitive to sampling frequency and duration |

The second advantage deserves an example. Procainamide was given intravenously to ten subjects. In some subjects the data were best described by a two-compartment model, and in others by a three-compartment model. That looks like a contradiction, as if the drug had changed its nature between people. It is not.

The number of compartments is a property of the data and the sampling design, not of the drug. A compartment is detected only when its exponential phase is both large enough and long enough to show up above the noise, at the times samples were taken. A fast distribution phase shows up only if several samples fall inside it. With early samples a third exponential appears. With fewer early samples, or noisier assay values, it merges into its neighbour and the fit prefers two. The subjects may differ a little in how their tissues take up the drug, or they may not differ at all. Either way, the model count answers a question about the data. Non-compartmental analysis sidesteps that question, and the clearance and MRT it gives are the same whichever model a subject's data happened to favour [2].

> **Common Mistake:** Reporting 0.693 · MRT as the half-life of a multi-compartment drug. That equality holds only for one compartment. For the two-compartment drug of Exercise E9.3, 0.693 · MRT is 2.5 h, while the terminal half-life is 3.3 h.

> **Why It Matters in Practice:** Bioequivalence studies, the subject of Chapter 13, compare AUC and Cmax without fitting any model. That is non-compartmental analysis. The sampling lessons of Example 9.1 apply directly: sample densely where the curve bends, and long enough that the extrapolated tail is a small part of the total.

## Key Takeaways
- Non-compartmental analysis needs linear kinetics and no compartmental model.
- AUC is the zero moment; AUMC, the area under Cp·t against t, is the first moment.
- Tails beyond the last sample: AUC gains Cn/λz, and AUMC gains tn·Cn/λz + Cn/λz².
- AUMC depends more heavily than AUC on late samples and on the extrapolated tail.
- MRT = AUMC/AUC; for a one-compartment IV drug it equals 1/K, so t½ = 0.693·MRT.
- MAT = MTT(oral) − MRT(IV), and equals 1/Ka for first order absorption.
- Cl = D₀/AUC and Vss = Cl·MRT = D₀·AUMC/AUC² after an IV bolus.
- Linear trapezoids over wide intervals overestimate the area of a falling curve.
- The number of compartments is set by the data and the sampling, not by the drug.

## Check Your Understanding

**Q1.** [LO1] The one assumption non-compartmental analysis requires is that:
A) The drug follows a one-compartment model
B) The kinetics are linear
C) The drug is given intravenously
D) Elimination is entirely renal

**Q2.** [LO2] AUMC is the area under a plot of:
A) Cp against log t
B) log Cp against t
C) Cp against t
D) Cp·t against t

**Q3.** [LO3] The mean residence time is calculated as:
A) AUMC / AUC
B) AUC / AUMC
C) AUC × AUMC
D) D₀ / AUMC

**Q4.** [LO4] For a drug following one-compartment kinetics after an IV bolus, MRT equals:
A) 0.693 / K
B) K / 0.693
C) 1 / K
D) Vd / Cl²

**Q5.** [LO2] The last sample is Cn = 2 mg·L⁻¹ and λz = 0.25 h⁻¹. The AUC beyond the last sample is:
A) 0.5 mg·h·L⁻¹
B) 2.25 mg·h·L⁻¹
C) 32 mg·h·L⁻¹
D) 8 mg·h·L⁻¹

**Q6.** [LO3] After an IV bolus, the volume of distribution at steady state is:
A) Cl × MRT
B) AUC / MRT
C) D₀ / AUC
D) Cl / MRT

**Q7.** [LO4] A drug has MTT = 9 h after an oral dose and MRT = 6 h after an IV dose. For first order absorption, MAT and Ka are:
A) 15 h and 0.067 h⁻¹
B) 1.5 h and 0.667 h⁻¹
C) 6 h and 0.167 h⁻¹
D) 3 h and 0.333 h⁻¹

**Q8.** [LO5] Procainamide data were best fitted by two compartments in some subjects and three in others. The best explanation is that:
A) The number of compartments detected depends on the data and the sampling design
B) Procainamide changes its chemical structure between subjects
C) Non-compartmental analysis was applied incorrectly
D) Three-compartment drugs cannot be studied in humans

**Q9.** [LO5] Which is a disadvantage of non-compartmental analysis?
A) It requires the number of compartments to be known in advance
B) It cannot show organ-specific elimination
C) It cannot give clearance
D) It applies only to oral doses

**Q10.** [LO3] A one-compartment drug has MRT = 10 h after an IV bolus. Its elimination half-life is:
A) 10 h
B) 14.4 h
C) 6.93 h
D) 5 h

### Exercises

**E9.1** [LO4] The drug of Example 9.1 has a true MRT(IV) of 5.88 h. After an oral dose in the same subjects, the mean transit time is 7.50 h. Calculate MAT, Ka, the absorption half-life and the elimination half-life, and say which process is faster.

**E9.2** [LO2] After a 500 mg IV bolus, trapezoids give AUC = 80 mg·h·L⁻¹ and AUMC = 600 mg·h²·L⁻¹ from 0 to 24 h. The 24 h sample is 2.0 mg·L⁻¹ and λz = 0.10 h⁻¹. Calculate the complete AUC and AUMC, then MRT, Cl and Vss. Comment on the share of each area that is extrapolated.

**E9.3** [LO5] The two-compartment drug of Chapter 4 follows Cp = 45·e^(−1.8t) + 15·e^(−0.21t) after a 300 mg IV bolus, with Cp in mg·L⁻¹ and t in h. Its constants are K = 0.622 h⁻¹ and Vp = 5.0 L. Using the exact areas of each exponential, AUC = A/a + B/b and AUMC = A/a² + B/b², calculate MRT, Cl and Vss. Compare Cl with K·Vp, and compare MRT with 1/K and with 1/b.

## Answers and Worked Solutions

**Q1. B** — Linearity means every dose gives a curve of the same shape, so areas scale with dose. No particular model is assumed.

**Q2. D** — The first moment curve is concentration multiplied by time. Option C is the ordinary plasma curve, whose area is AUC.

**Q3. A** — MRT is the first moment divided by the zero moment, which is the mean of the residence-time distribution.

**Q4. C** — For a single exponential, AUMC/AUC = (C⁰/K²)/(C⁰/K) = 1/K. Option A is the half-life, which is 0.693·MRT.

**Q5. D** — The tail is Cn/λz = 2 ÷ 0.25 = 8 mg·h·L⁻¹. Option A multiplies instead of dividing.

**Q6. A** — Vss = Cl·MRT, which equals D₀·AUMC/AUC². Option C is clearance itself.

**Q7. D** — MAT = 9 − 6 = 3 h, and Ka = 1/MAT = 0.333 h⁻¹. Option A adds the two times instead of subtracting.

**Q8. A** — A phase is detected only if the samples capture it clearly. The compartment count describes what the data can resolve.

**Q9. B** — The method uses only plasma areas, so it cannot separate renal from hepatic elimination. It gives clearance readily, which rules out option C.

**Q10. C** — t½ = 0.693 × MRT = 0.693 × 10 h = 6.93 h. This equality holds only for one compartment.

---

**E9.1 — worked solution**

*Step 1 — MAT.*

MAT = MTT(oral) − MRT(IV) = 7.50 h − 5.88 h = 1.62 h

*Step 2 — Ka and the absorption half-life.*

Ka = 1 ÷ 1.62 h = 0.617 h⁻¹

absorption t½ = 0.693 × 1.62 h = 1.12 h

*Step 3 — the elimination half-life.*

t½ = 0.693 × 5.88 h = 4.07 h

*Answer.* MAT = 1.62 h, Ka = 0.617 h⁻¹, absorption t½ = 1.12 h and elimination t½ = 4.07 h. Absorption is about 3.6 times faster than elimination.

*Check.* K = 1/5.88 = 0.170 h⁻¹, the value found in Chapter 2. Ka exceeds K, so this is not a flip-flop case, and the terminal slope after an oral dose would still reflect elimination.

**E9.2 — worked solution**

*Step 1 — the AUC tail.*

AUC(24 → ∞) = 2.0 mg·L⁻¹ ÷ 0.10 h⁻¹ = 20 mg·h·L⁻¹

AUC = 80 + 20 = 100 mg·h·L⁻¹

*Step 2 — the AUMC tail.*

24 h × 2.0 mg·L⁻¹ ÷ 0.10 h⁻¹ = 480 mg·h²·L⁻¹

2.0 mg·L⁻¹ ÷ (0.10 h⁻¹)² = 200 mg·h²·L⁻¹

AUMC = 600 + 480 + 200 = 1280 mg·h²·L⁻¹

*Step 3 — MRT, Cl and Vss.*

MRT = 1280 ÷ 100 = 12.8 h

Cl = 500 mg ÷ 100 mg·h·L⁻¹ = 5.0 L·h⁻¹

Vss = 5.0 L·h⁻¹ × 12.8 h = 64 L

*Answer.* AUC = 100 mg·h·L⁻¹, AUMC = 1280 mg·h²·L⁻¹, MRT = 12.8 h, Cl = 5.0 L·h⁻¹ and Vss = 64 L.

*The share extrapolated.* The tail is 20% of AUC but 53% of AUMC. More than half of MRT and Vss therefore rests on the value of λz and on the single last sample. Sampling should have continued well beyond 24 h.

*Check by a second route.* Vss = D₀·AUMC/AUC² = 500 × 1280 ÷ 100² = 64 L, as found.

**E9.3 — worked solution**

*Step 1 — AUC.*

AUC = 45/1.8 + 15/0.21 = 25.0 + 71.4 = 96.4 mg·h·L⁻¹

*Step 2 — AUMC.*

AUMC = 45/1.8² + 15/0.21² = 45/3.24 + 15/0.0441 = 13.9 + 340.1 = 354.0 mg·h²·L⁻¹

*Step 3 — MRT, Cl and Vss.*

MRT = 354.0 ÷ 96.4 = 3.67 h

Cl = 300 mg ÷ 96.4 mg·h·L⁻¹ = 3.11 L·h⁻¹

Vss = 3.11 L·h⁻¹ × 3.67 h = 11.4 L

*Answer.* MRT = 3.67 h, Cl = 3.11 L·h⁻¹ and Vss = 11.4 L.

*Check against the compartmental values.* K·Vp = 0.622 h⁻¹ × 5.0 L = 3.11 L·h⁻¹, identical to the non-compartmental clearance. Clearance does not depend on the model, as Chapter 6 said.

*The comparisons.* 1/K = 1.61 h and 1/b = 4.76 h. MRT lies between them and equals neither, because the curve has two exponentials. Vss is 11.4 L, more than twice Vp. The drug spends much of its time in the peripheral compartment, which the central volume alone cannot show.

## References
1. Shargel L, Yu ABC. *Applied Biopharmaceutics and Pharmacokinetics*. 8th ed. New York: McGraw Hill Medical; 2022.
2. Rowland M, Tozer TN. *Clinical Pharmacokinetics and Pharmacodynamics: Concepts and Applications*. 5th ed. Philadelphia: Wolters Kluwer; 2019.


---

# Chapter 10: Non-Linear Pharmacokinetics

## Learning Objectives
By the end of this chapter you will be able to:
1. [LO1] Distinguish linear from non-linear kinetics by how concentrations and parameters respond to a change in dose.
2. [LO2] Explain how a saturable enzyme system produces non-linear kinetics.
3. [LO3] Apply the Michaelis–Menten equation, and show that it becomes first order at low concentration and zero order at high concentration.
4. [LO4] Calculate the steady-state concentration of a drug with saturable elimination, and explain why it rises out of proportion to the dose.

## 10.1 Linear and Non-Linear Kinetics

Every chapter so far has assumed that doubling the dose doubles the concentration. That assumption has a name. In **linear pharmacokinetics** the concentration changes in proportion to the dose, and K, Vd and t½ do not depend on the dose at all. The kinetics are dose-independent.

In **non-linear pharmacokinetics** that proportionality fails. Doubling the dose gives more than twice the concentration, or less. The parameters themselves now change with the dose, so the kinetics are dose-dependent [1].

| Feature | Linear | Non-linear |
|---|---|---|
| Dose doubled | Concentration and AUC double | Concentration and AUC change by more or less than twofold |
| K, Vd, t½ | Independent of dose | Depend on dose |
| Description | Dose-independent kinetics | Dose-dependent kinetics |
| Predicting a new dose | Scale the old result | Needs the underlying rate law |

A half-life is then no longer a single number, and a clearance measured at one dose does not apply at another. Chapter 9's non-compartmental analysis still runs — AUC and clearance can be computed from any set of concentrations — but the numbers describe that one dose only. Superposition and dose proportionality fail, so no multiple-dose prediction can be built by adding single doses. The arithmetic survives; the extrapolation does not.

## 10.2 Why Kinetics Become Non-Linear

The main cause is a saturable system. Most often it is an enzyme that metabolises the drug, but a carrier that transports it behaves the same way. Drug metabolism runs largely through the cytochrome P450 and N-acetyltransferase systems, which Chapter 11 describes.

An enzyme works by binding its substrate, converting it and releasing the product:

enzyme (E) + drug (D) ⇌ E–D complex → enzyme + metabolite

The enzyme is released unchanged, but there is a finite amount of it. At low concentrations most enzyme molecules are free, and more drug means more conversion. At high concentrations nearly all are occupied, so more drug adds no capacity. The system is saturated.

Chapter 6 used the symbol Kh for the hepatic elimination rate constant, precisely so that Km could be kept for what follows. Km is a concentration, not a rate constant.

## 10.3 The Michaelis–Menten Equation

The rate of an enzyme-catalysed reaction is described by the **Michaelis–Menten equation**.

> **Key Equation:** Equation 10.1 — the Michaelis–Menten equation
>
> $$V = -\frac{dC}{dt} = \frac{V_{max}\, C}{K_m + C}$$
>
> where V is the rate of the reaction, C is the drug concentration, Vmax is the maximum rate, and Km is the Michaelis–Menten constant.

**Vmax** is the maximum rate of the process, reached when the concentration is very high and the enzyme is saturated. **Km** is the concentration at which the rate is half of Vmax. Setting C = Km in Equation 10.1 gives V = Vmax · Km / (2Km) = Vmax / 2. Km reflects the affinity of the drug for the enzyme. A low Km means the enzyme reaches half its capacity at a low concentration.

![Two plots. Left: reaction rate as a fraction of Vmax against concentration from 0 to 20 milligrams per litre. The curve rises steeply, then flattens towards a dashed horizontal line at 1 labelled zero order limit. A dotted straight line from the origin, labelled first order limit, follows the curve only at low concentration. Dotted guides mark the point where concentration equals Km and the rate is one half of Vmax. Right: steady-state concentration against dosing rate from 0 to 500 milligrams per day. The curve starts low, passes points labelled 300 to 6 and 400 to 16, and turns almost vertical near a dashed vertical line labelled Vmax at 500. A dotted straight line labelled linear prediction runs through the 300 milligram point and reaches only 10 at 500.](../rework/figures/out/ch10-saturation.png)

*Figure 10.1 — Saturable elimination. Left: the Michaelis–Menten rate follows its first order limit at low concentration and approaches Vmax at high concentration, passing Vmax/2 at C = Km. Right: for the drug of Example 10.1 the steady-state level rises far above the linear prediction as the dosing rate approaches Vmax.*  
Original diagram, redrawn from the first edition page 48 (original)

The value of the equation lies in its two limits.

*When C is much smaller than Km.* The denominator Km + C is then close to Km, so:

V ≈ (Vmax / Km) · C

Vmax/Km is a constant, so the rate is proportional to concentration. That is first order kinetics, with an apparent rate constant Vmax/Km. The enzyme is far from saturation and the rate can still rise.

*When C is much larger than Km.* The denominator is then close to C, which cancels:

V ≈ Vmax

The rate is now constant whatever the concentration. That is zero order kinetics. The enzyme is saturated and its maximum rate cannot be exceeded.

One drug can therefore be first order at a low dose and zero order at a high one, and neither in between.

> **Watch the Units:** In Equation 10.1, V and Vmax are rates of change of concentration, such as mg·L⁻¹·h⁻¹. Dosing work expresses Vmax as an amount per time, such as mg·day⁻¹, which is the first form multiplied by Vd. Km is a concentration in both. Never mix the two forms.

> **Deeper Dive:** For a drug following Equation 10.1, the apparent elimination rate constant at concentration C is V/C = Vmax/(Km + C). It falls as C rises, so 0.693 · Vd · (Km + C)/Vmax rises with concentration, and so with dose. This is the precise sense in which t½ is dose-dependent in the table of Section 10.1.
>
> Read it carefully: that is 0.693 over the rate constant *at this instant*, not the time the drug takes to halve. For a first-order drug the two coincide; here the rate constant rises as C falls, so the drug halves sooner. Integrating Equation 10.1 from C₀ to C₀/2 gives the real halving time:
>
> t½ = (Vd / Vmax) · [Km · ln 2 + C₀/2]

## 10.4 Steady State When Elimination Saturates

Steady state is reached when the rate of elimination equals the dosing rate, as in Chapters 5 and 8. With first order elimination this gave Css = R/Cl, proportional to R. With saturable elimination the rate law changes.

Write the dosing rate as R, in mg·day⁻¹, and Vmax in the same units. At steady state the elimination rate equals R:

R = Vmax · Css / (Km + Css)

Rearranging for Css gives the working result.

> **Key Equation:** Equation 10.2 — steady state with saturable elimination
>
> $$C_{ss} = \frac{K_m\, R}{V_{max} - R}$$
>
> valid only while R < Vmax.

The denominator is the whole story. As R approaches Vmax, Vmax − R approaches zero and Css climbs steeply. A small increase in dose near that limit produces a large increase in concentration. If R reaches or exceeds Vmax, no steady state exists at all. The body is removing drug as fast as it can, the dose is arriving faster, and the concentration rises until the dose is reduced.

> **Worked Example:** Example 10.1 — a small dose change and a large concentration change
>
> Phenytoin is a drug with saturable elimination. Take a patient with Km = 4 mg·L⁻¹ and Vmax = 500 mg·day⁻¹, which are typical adult values, and Vd = 45 L [2]. Find the steady-state concentration at 300 and at 400 mg·day⁻¹, and the apparent half-life at each.
>
> *Step 1 — check that steady state exists.* Both dosing rates are below Vmax = 500 mg·day⁻¹, so Equation 10.2 applies.
>
> *Step 2 — Css at 300 mg·day⁻¹.*
>
> Css = 4 mg·L⁻¹ × 300 mg·day⁻¹ ÷ (500 − 300) mg·day⁻¹ = 1200 ÷ 200 = 6.0 mg·L⁻¹
>
> *Step 3 — Css at 400 mg·day⁻¹.*
>
> Css = 4 mg·L⁻¹ × 400 mg·day⁻¹ ÷ (500 − 400) mg·day⁻¹ = 1600 ÷ 100 = 16.0 mg·L⁻¹
>
> *Step 4 — the proportions.* The dose rose by 400/300 = 1.33, a third. The concentration rose by 16.0/6.0 = 2.67, which is 167% higher.
>
> *Step 5 — the instantaneous apparent half-life.* From the Deeper Dive, 0.693 · Vd · (Km + C) / Vmax — 0.693 over the rate constant at that concentration, not a halving time.
>
> At 6.0 mg·L⁻¹: t½ = 0.693 × 45 L × 10.0 mg·L⁻¹ ÷ 500 mg·day⁻¹ = 0.624 day = 15.0 h
>
> At 16.0 mg·L⁻¹: t½ = 0.693 × 45 L × 20.0 mg·L⁻¹ ÷ 500 mg·day⁻¹ = 1.25 day = 29.9 h
>
> *Step 6 — the time each level really takes to halve.* With Vd/Vmax = 45 ÷ 500 = 0.0900 L·day·mg⁻¹ and Km·ln 2 = 2.77 mg·L⁻¹:
>
> From 6.0 mg·L⁻¹: 0.0900 × (2.77 + 3.00) = 0.519 day = 12.5 h
>
> From 16.0 mg·L⁻¹: 0.0900 × (2.77 + 8.00) = 0.970 day = 23.3 h
>
> *Answer.* Css is 6.0 mg·L⁻¹ at 300 mg·day⁻¹ and 16.0 mg·L⁻¹ at 400 mg·day⁻¹. A one-third increase in dose gives a 2.67-fold increase in concentration. The instantaneous apparent half-life rises from 15.0 to 29.9 h, and the time actually needed to halve rises from 12.5 to 23.3 h.
>
> *Why they differ.* The instantaneous figure fixes the rate constant at the starting concentration, but as C falls towards Km that constant climbs, so the real halving is faster — by 20% at 6 mg·L⁻¹ and 29% at 16. The gap widens as C₀ rises above Km.
>
> *Check by substitution.* Put Css = 16.0 back into the rate law: 500 × 16.0 ÷ (4 + 16.0) = 400 mg·day⁻¹, the dosing rate. The same test at 6.0 gives 300 mg·day⁻¹.
>
> *What linear thinking would have predicted.* Scaling 6.0 mg·L⁻¹ by 1.33 gives 8.0 mg·L⁻¹, only half the true value.

## 10.5 Consequences in Practice

Non-linear kinetics matter most at high doses, because saturation needs high concentrations. Three consequences follow for anyone dosing such a drug.

*A single dose can mislead.* The concentrations after one dose may stay below Km, where elimination looks first order. The accumulation that occurs on repeated dosing takes the concentration into the saturable range. The non-linearity then appears only on multiple dosing, and a single-dose study would not have predicted it.

*Dose changes must be small.* Near Vmax a modest dose increase produces a disproportionate rise in concentration. A dose scaled in proportion to the level wanted may even exceed Vmax, as Exercise E10.2 shows.

*Products need in-vivo comparison.* A small difference in absorption between two formulations is amplified by saturable elimination. Drugs such as phenytoin therefore require in-vivo bioequivalence studies, the subject of Chapter 13.

> **Why It Matters in Practice:** The usual target range quoted for phenytoin is about 10–20 mg·L⁻¹, and Example 10.1 puts 300 and 400 mg·day⁻¹ on either side of it. The dose in between is found by small steps and monitoring, not by proportion [2].

## Key Takeaways
- Linear kinetics: concentration is proportional to dose, and K, Vd and t½ are independent of dose.
- Non-linear kinetics: concentration changes out of proportion to dose, and the parameters are dose-dependent.
- The main cause is a saturable enzyme or carrier system.
- Michaelis–Menten: V = Vmax·C/(Km + C); Km is the concentration at which V = Vmax/2.
- When C ≪ Km, elimination is first order with rate constant Vmax/Km; when C ≫ Km, it is zero order at Vmax.
- The instantaneous apparent half-life, 0.693·Vd·(Km + C)/Vmax, rises with concentration; the real halving time, (Vd/Vmax)·[Km·ln 2 + C₀/2], is shorter.
- At steady state Css = Km·R/(Vmax − R); no steady state exists when R ≥ Vmax.
- Non-linearity may appear only on multiple dosing, so single-dose data can mislead.
- Saturable drugs such as phenytoin need small dose steps, monitoring, and in-vivo bioequivalence studies.

## Check Your Understanding

**Q1.** [LO1] The dose of a drug with linear kinetics is doubled. The steady-state concentration will:
A) Increase more than twofold
B) Double
C) Stay the same
D) Increase less than twofold

**Q2.** [LO3] When the drug concentration equals Km, the rate of a Michaelis–Menten process is:
A) Zero
B) Vmax
C) 2 × Vmax
D) Vmax / 2

**Q3.** [LO3] At concentrations far below Km, elimination is:
A) First order, with an apparent rate constant Vmax/Km
B) Zero order, at a rate equal to Vmax
C) Independent of concentration
D) Mixed order at all times

**Q4.** [LO2] The main cause of non-linear pharmacokinetics is:
A) An increase in Vd at high doses
B) Incomplete absorption at low doses
C) A saturable enzyme or carrier system
D) An error in the assay at high concentrations

**Q5.** [LO4] A drug has Km = 4 mg·L⁻¹ and Vmax = 500 mg·day⁻¹, and is given at 250 mg·day⁻¹. The steady-state concentration is:
A) 2 mg·L⁻¹
B) 16 mg·L⁻¹
C) 8 mg·L⁻¹
D) 4 mg·L⁻¹

**Q6.** [LO1] For a drug with non-linear kinetics, the elimination half-life:
A) Is the same at every dose
B) Is shorter at higher doses
C) Depends on the dose and rises as elimination saturates
D) Cannot be defined at any concentration

**Q7.** [LO4] A drug with saturable elimination is given at a rate greater than its Vmax. The result is:
A) A lower steady state than expected
B) A steady state reached more quickly
C) First order elimination
D) No steady state, with the concentration rising continuously

**Q8.** [LO3] At concentrations far above Km, the rate of elimination:
A) Falls towards zero
B) Is proportional to concentration
C) Approaches Vmax and no longer depends on concentration
D) Equals Vmax / Km

**Q9.** [LO2] The Michaelis–Menten constant Km:
A) Is the maximum rate of the reaction
B) Is the concentration at which the rate is half of Vmax, and reflects affinity for the enzyme
C) Is a first order rate constant in h⁻¹
D) Increases with the dose

**Q10.** [LO4] Why can a single-dose study fail to reveal non-linear kinetics?
A) Saturation may appear only at the higher concentrations reached on repeated dosing
B) Km cannot be measured after one dose
C) Single doses are always given intravenously
D) Vmax changes after the first dose

### Exercises

**E10.1** [LO3] A drug has Km = 2 mg·L⁻¹ and Vmax = 1.0 mg·L⁻¹·h⁻¹. Calculate the rate of elimination at 0.2, 2 and 20 mg·L⁻¹, and express each as a percentage of Vmax. At the lowest and highest concentrations, compare the exact rate with the first order and zero order approximations.

**E10.2** [LO4] A patient on phenytoin 300 mg·day⁻¹ has a steady-state level of 8 mg·L⁻¹. Assume Km = 4 mg·L⁻¹. Estimate the patient's Vmax, then the daily dose that would give 15 mg·L⁻¹. Compare it with the dose a proportional calculation would suggest, and state what would happen if that dose were given.

**E10.3** [LO1] A drug is given intravenously. A 100 mg dose gives AUC = 20 mg·h·L⁻¹, and a 200 mg dose in the same subject gives AUC = 60 mg·h·L⁻¹. Calculate the clearance at each dose. Decide whether the kinetics are linear, and state what the result suggests about the elimination process and about the half-life at the higher dose.

## Answers and Worked Solutions

**Q1. B** — In linear kinetics concentration is proportional to dose. Options A and D describe non-linear behaviour.

**Q2. D** — Setting C = Km gives V = Vmax·Km/(2Km) = Vmax/2. This is the definition of Km.

**Q3. A** — When C ≪ Km, Km + C ≈ Km, so V ≈ (Vmax/Km)·C. The rate is proportional to concentration.

**Q4. C** — Enzymes and carriers have finite capacity, and once saturated they cannot keep pace with concentration.

**Q5. D** — Css = 4 × 250 ÷ (500 − 250) = 1000 ÷ 250 = 4 mg·L⁻¹. The dosing rate is half of Vmax, which places Css exactly at Km.

**Q6. C** — The instantaneous apparent half-life is 0.693·Vd·(Km + C)/Vmax, which rises with concentration. Option B has the direction reversed. The integrated halving time is shorter but rises with concentration too.

**Q7. D** — The body cannot eliminate faster than Vmax, so a larger input accumulates without limit. Equation 10.2 gives a negative Css, which has no physical meaning.

**Q8. C** — When C ≫ Km, Km + C ≈ C and the rate approaches Vmax. That is zero order elimination.

**Q9. B** — Km is a concentration, not a rate or a rate constant. Option C describes Vmax/Km, not Km.

**Q10. A** — One dose may stay below Km, where elimination looks first order; accumulation then exposes saturation.

---

**E10.1 — worked solution**

*Step 1 — the three rates.* Use V = Vmax·C/(Km + C) with Vmax = 1.0 mg·L⁻¹·h⁻¹ and Km = 2 mg·L⁻¹.

At 0.2 mg·L⁻¹: V = 1.0 × 0.2 ÷ 2.2 = 0.091 mg·L⁻¹·h⁻¹, which is 9.1% of Vmax

At 2 mg·L⁻¹: V = 1.0 × 2 ÷ 4 = 0.50 mg·L⁻¹·h⁻¹, which is 50% of Vmax

At 20 mg·L⁻¹: V = 1.0 × 20 ÷ 22 = 0.909 mg·L⁻¹·h⁻¹, which is 90.9% of Vmax

*Step 2 — the first order approximation at 0.2 mg·L⁻¹.*

V ≈ (Vmax/Km)·C = (1.0 ÷ 2) × 0.2 = 0.100 mg·L⁻¹·h⁻¹

*Step 3 — the zero order approximation at 20 mg·L⁻¹.*

V ≈ Vmax = 1.0 mg·L⁻¹·h⁻¹

*Answer.* The rates are 0.091, 0.50 and 0.909 mg·L⁻¹·h⁻¹, or 9.1%, 50% and 90.9% of Vmax. Each approximation overestimates the exact rate by 10%.

*Why the errors match.* Each approximation drops a term one tenth the size of the one kept. A limit is therefore good to about 10% when the concentration is a factor of ten from Km.

**E10.2 — worked solution**

*Step 1 — Vmax from the measured steady state.* Rearrange R = Vmax·Css/(Km + Css):

Vmax = R · (Km + Css) / Css = 300 mg·day⁻¹ × (4 + 8) mg·L⁻¹ ÷ 8 mg·L⁻¹ = 450 mg·day⁻¹

*Step 2 — the dose for 15 mg·L⁻¹.*

R = Vmax · Css / (Km + Css) = 450 × 15 ÷ (4 + 15) = 6750 ÷ 19 = 355 mg·day⁻¹

*Step 3 — the proportional estimate.*

300 mg·day⁻¹ × 15 ÷ 8 = 563 mg·day⁻¹

*Answer.* Vmax ≈ 450 mg·day⁻¹, and about 355 mg·day⁻¹ gives 15 mg·L⁻¹. The proportional estimate is 563 mg·day⁻¹.

*What the proportional dose would do.* It exceeds Vmax, so the body could never eliminate the drug as fast as it arrived. There would be no steady state, and the concentration would keep rising into the toxic range. The correct increase is 55 mg·day⁻¹, not 263.

*Check by substitution.* Css = 4 × 355 ÷ (450 − 355) = 1420 ÷ 95 = 14.9 mg·L⁻¹, as intended.

**E10.3 — worked solution**

*Step 1 — clearance at each dose.*

Cl(100 mg) = 100 mg ÷ 20 mg·h·L⁻¹ = 5.0 L·h⁻¹

Cl(200 mg) = 200 mg ÷ 60 mg·h·L⁻¹ = 3.33 L·h⁻¹

*Step 2 — the test for linearity.* Linear kinetics would give AUC = 40 mg·h·L⁻¹ at 200 mg. The observed value is 60, three times the AUC for twice the dose.

*Answer.* Clearance falls from 5.0 to 3.33 L·h⁻¹ as the dose doubles, so the kinetics are non-linear.

*What it suggests.* A clearance that falls as the dose rises is the signature of saturable elimination, most likely a metabolising enzyme approaching its Vmax. If Vd is unchanged, the half-life at the higher dose is longer by the ratio 5.0/3.33 = 1.5.

## References
1. Shargel L, Yu ABC. *Applied Biopharmaceutics and Pharmacokinetics*. 8th ed. New York: McGraw Hill Medical; 2022.
2. Rowland M, Tozer TN. *Clinical Pharmacokinetics and Pharmacodynamics: Concepts and Applications*. 5th ed. Philadelphia: Wolters Kluwer; 2019.


---

# Chapter 11: Pharmacokinetics of Metabolites

## Learning Objectives
By the end of this chapter you will be able to:
1. [LO1] Describe what metabolism does to a drug, where it happens, and how Phase I differs from Phase II.
2. [LO2] Explain why metabolite kinetics matter, giving correct examples of active and toxic metabolites.
3. [LO3] Explain how genetic polymorphism in NAT2, CYP2D6 and CYP2C19 changes metabolism in an individual patient.
4. [LO4] Calculate the metabolite concentration, its peak time and its AUC after an intravenous dose of the parent drug.
5. [LO5] Decide whether a metabolite's decline is formation-rate-limited or elimination-rate-limited, and state what its curve can then reveal.

## 11.1 Metabolism and Where It Happens

Chapter 6 divided elimination into excretion and metabolism, and left metabolism for this chapter. Metabolism, or biotransformation, is the chemical process by which the body converts a drug into another chemical species, the metabolite. The metabolite is usually more polar, so it is more water soluble than the parent. That has two consequences. A polar metabolite distributes less into tissues, so its volume of distribution is smaller. It is also reabsorbed less in the renal tubule, as Chapter 6 explained, so it is excreted more readily. Metabolism often reduces the activity of the parent as well, which is why it is described as detoxification.

Metabolism is not confined to the liver. It occurs in the gut lumen and gut wall, the liver, blood, lungs, skin, kidney, brain and placenta. The gut wall and liver can metabolise an oral dose before it reaches the circulation, which Chapter 13 takes up. At therapeutic concentrations metabolism is usually a first order process. Chapter 10 showed what happens when it saturates.

The reactions fall into two groups [1].

| | Phase I | Phase II |
|---|---|---|
| What it does | Adds or unmasks a polar group | Joins the drug to an endogenous compound |
| Reactions | Oxidation, reduction | Conjugation, such as glucuronidation or acetylation |
| Requirements | NADPH, molecular oxygen, microsomal enzymes | An activated endogenous donor molecule |
| Product | A more polar metabolite, sometimes still active | A more polar conjugate, usually inactive |

The terminal oxidising enzyme of Phase I is **cytochrome P450**. It takes its name from its carbon monoxide complex, which absorbs light at 450 nm. It is not one enzyme but a family of isoenzymes with different substrate specificities, encoded by more than 70 genes across species.

## 11.2 Why Metabolite Kinetics Matter

Once formed, a metabolite is a separate chemical entity, with its own volume of distribution, its own clearance and its own half-life. Four reasons make those worth measuring.

*Metabolites can be active.* An **active metabolite** has pharmacological activity of its own and contributes to the response. The table lists examples.

| Parent | Active metabolite |
|---|---|
| Imipramine | Desipramine |
| Phenacetin | Acetaminophen (paracetamol) |
| Terfenadine | Fexofenadine |
| Procainamide | N-acetylprocainamide |
| Fluoxetine | Norfluoxetine |
| Propranolol | 4-hydroxypropranolol |
| Verapamil | Norverapamil |
| Diazepam | Desmethyldiazepam |

The last four rows are active metabolites, not toxic ones; desmethyldiazepam is itself a long-acting benzodiazepine.

*Metabolites can be toxic.* The standard example is acetaminophen. A small fraction of each dose is oxidised to a reactive metabolite, N-acetyl-p-benzoquinone imine (NAPQI). Normally glutathione conjugates it at once, but in overdose glutathione runs out and NAPQI damages the liver. Cyclophosphamide yields acrolein, which injures the bladder. Pethidine (meperidine) yields norpethidine, which accumulates in renal failure and can cause seizures [2].

*Metabolites can interact.* A metabolite may inhibit or induce the cytochrome P450 enzymes. It then alters the disposition of its own parent or of other drugs given at the same time.

*Metabolism varies between people.* Extrinsic factors matter: smoking and diet both change the metabolism of theophylline, for example. Intrinsic genetic factors matter as well, and Section 11.3 treats them.

> **Why It Matters in Practice:** Measuring only the parent can mislead. If an active metabolite has a longer half-life than its parent, the response outlasts the parent's concentration. Norfluoxetine is an example: it persists for weeks after fluoxetine is stopped, which is why a washout period is needed before starting a drug that interacts with it.

## 11.3 Genetic Polymorphism

A **genetic polymorphism** is a variation in a gene that is common in a population, not rare. When the gene encodes a drug-metabolising enzyme, people who carry different variants metabolise the same drug at different rates.

N-acetyltransferase 2 (NAT2) is the classic case. It acetylates isoniazid, hydralazine and procainamide, among others. A person's NAT2 genotype determines whether that person is a slow or a fast acetylator. Slow acetylators reach higher parent concentrations on the same dose and are more exposed to concentration-related adverse effects.

The frequency of slow and fast acetylator alleles differs between populations. Within every population, both kinds of acetylator occur. The acetylation rate of a patient is therefore a property of that patient's genotype. It is not predicted by skin colour, and the claim that one skin colour marks faster acetylators is wrong. The same holds for every polymorphism in this section.

Two cytochrome P450 enzymes show the same pattern.

| Enzyme | Phenotypes | Example of the consequence |
|---|---|---|
| NAT2 | Slow and fast acetylators | Slow acetylators accumulate isoniazid and procainamide |
| CYP2D6 | Poor, intermediate, normal and ultrarapid metabolisers | Ultrarapid metabolisers convert more codeine to morphine and risk opioid toxicity |
| CYP2C19 | Poor, intermediate, normal and rapid metabolisers | Poor metabolisers form less of clopidogrel's active metabolite and gain less antiplatelet effect |

The codeine and clopidogrel rows show that the direction of the risk depends on which molecule is active. When the parent is active, a poor metaboliser risks toxicity. When the metabolite is active, a poor metaboliser risks treatment failure [2].

## 11.4 A Model for a Metabolite

A drug can be metabolised in sequence or in parallel. In sequential metabolism the drug forms metabolite 1, which forms metabolite 2. In parallel metabolism the drug forms metabolites 1 and 2 independently. The simplest model follows one metabolite formed from a parent given as an intravenous bolus:

A → Am → Ae(m)

A is the amount of parent in the body, Am the amount of metabolite in the body, and Ae(m) the amount of metabolite eliminated. The parent is eliminated with rate constant K, and a fraction fm of it becomes the metabolite. The metabolite is eliminated with rate constant Kmet.

The first edition writes the metabolite's rate constant as K(m). This edition writes Kmet, so that Km remains the Michaelis constant of Chapter 10.

> **Key Equation:** Equation 11.1 — the metabolite curve after an IV dose of parent
>
> Cp(m) = [fm · K · D / (Vd(m) · (Kmet − K))] · (e^(−K·t) − e^(−Kmet·t))
>
> $$t_{max(m)} = \frac{\ln(K_{met} / K)}{K_{met} - K}$$
>
> where D is the IV dose of parent and Vd(m) is the volume of distribution of the metabolite.

The equation has the same shape as the oral absorption curve of Chapter 7. The parent plays the part of the gut, feeding the metabolite compartment by a first order process. At tmax(m) the rate of metabolite formation equals the rate of its elimination, so dCp(m)/dt = 0.

> **Watch the Units:** fm · K · D is a rate, in mg·h⁻¹ at time zero. Dividing by Vd(m) and by (Kmet − K) in h⁻¹ leaves mg·L⁻¹. If Kmet < K, both the coefficient and the bracket are negative, and their product is still positive. Keep the signs.

## 11.5 Which Step Limits the Curve

After the peak, one exponential in Equation 11.1 vanishes first. Which one depends on which rate constant is larger, and it decides what the metabolite curve can tell you.

| | Elimination-rate-limited | Formation-rate-limited |
|---|---|---|
| Condition | Kmet < K | Kmet > K |
| Half-lives | Metabolite t½ longer than parent t½ | Metabolite t½ shorter than parent t½ |
| Term that vanishes | e^(−K·t) | e^(−Kmet·t) |
| Late curve | Cp(m) ∝ e^(−Kmet·t) | Cp(m) ∝ e^(−K·t) |
| Terminal slope gives | Kmet, the metabolite's own half-life | K, the parent's half-life |

In the **elimination-rate-limited** case the metabolite is formed quickly and eliminated slowly. Its terminal decline reflects its own elimination, so its half-life can be read from its own curve.

In the **formation-rate-limited** case the metabolite is eliminated as soon as it forms. The slow step is formation. The metabolite curve then declines in parallel with the parent. Its terminal slope gives K, not Kmet, and the metabolite's own half-life cannot be read from it.

![Two semilogarithmic plots of relative concentration against time from 0 to 36 hours, each curve scaled to its own peak. Left, titled elimination-rate-limited: the parent falls as a steep dashed straight line with slope 0.2 per hour, while the metabolite rises, peaks near 7 hours and then falls along a shallower line with slope 0.1, staying far above the parent. Right, titled formation-rate-limited: the parent falls as a dashed line with slope 0.1, and the metabolite rises quickly, peaks near 4 hours, and then falls along a line parallel to the parent, also with slope 0.1.](../rework/figures/out/ch11-rate-limiting.png)

*Figure 11.1 — Which step sets the metabolite's terminal slope. When the metabolite is eliminated more slowly than it is formed (left, Example 11.1), its curve outlasts the parent and its slope is its own. When it is eliminated faster (right, Exercise E11.1), it declines in parallel with the parent and its own rate constant cannot be read from the curve.*  
Original diagram, redrawn from the first edition page 53 (original)

> **Common Mistake:** Reading a metabolite half-life off the terminal slope without checking which step is slower. If the metabolite declines in parallel with the parent, the slope belongs to the parent. Measuring Kmet then needs the metabolite itself to be given intravenously.

## 11.6 Metabolite Area and Clearance

Integrating Equation 11.1 from zero to infinity gives the area under the metabolite curve. The amount of metabolite formed is fm · D, and all of it is eventually cleared with clearance Cl(m):

> **Key Equation:** Equation 11.2 — metabolite AUC, clearance and volume
>
> $$AUC_{(m)} = \frac{f_m D}{Cl_{(m)}}$$
>
> Since D = Cl_T · AUC for the parent: AUC(m) / AUC = fm · Cl_T / Cl(m)
>
> $$V_{d(m)} = \frac{Cl_{(m)}}{K_{met}}$$

These hold whichever step is rate-limiting. The ratio form needs no dose: relative exposure depends only on fm and the two clearances.

> **Watch the Units:** fm is a *molar* fraction: metabolism conserves moles, not milligrams. This chapter carries fm · D in milligrams, which is exact only when parent and metabolite share a molar mass. When they differ, multiply by MW_metabolite / MW_parent: a parent of 300 g·mol⁻¹ giving a glucuronide of 476 yields 59% more milligrams than the uncorrected arithmetic predicts, and every Cmax(m) and AUC(m) is wrong by that factor. Working in moles avoids it.

> **Worked Example:** Example 11.1 — the metabolite of an IV dose
>
> The constants here are illustrative. A 500 mg IV bolus of a parent drug is given. The parent has K = 0.2 h⁻¹, and a fraction fm = 0.4 is converted to one metabolite. The metabolite has Kmet = 0.1 h⁻¹ and Vd(m) = 20 L. Parent and metabolite are taken to have the same molar mass.
>
> Find tmax(m), Cmax(m), Cl(m) and AUC(m), and identify the rate-limiting step.
>
> *Step 1 — the rate-limiting step.* Kmet = 0.1 h⁻¹ is less than K = 0.2 h⁻¹, so the metabolite is eliminated more slowly than it is formed. The curve is elimination-rate-limited.
>
> *Step 2 — tmax(m).*
>
> tmax(m) = ln(0.1/0.2) ÷ (0.1 − 0.2) h⁻¹ = (−0.693) ÷ (−0.1 h⁻¹) = 6.93 h
>
> *Step 3 — the coefficient of Equation 11.1.*
>
> fm · K · D = 0.4 × 0.2 h⁻¹ × 500 mg = 40 mg·h⁻¹
>
> Vd(m) · (Kmet − K) = 20 L × (−0.1 h⁻¹) = −2.0 L·h⁻¹
>
> coefficient = 40 ÷ (−2.0) = −20 mg·L⁻¹
>
> *Step 4 — Cmax(m).* At 6.93 h, e^(−0.2 × 6.93) = 0.250 and e^(−0.1 × 6.93) = 0.500.
>
> Cmax(m) = −20 mg·L⁻¹ × (0.250 − 0.500) = 5.0 mg·L⁻¹
>
> *Step 5 — Cl(m) and AUC(m).*
>
> Cl(m) = Kmet × Vd(m) = 0.1 h⁻¹ × 20 L = 2.0 L·h⁻¹
>
> AUC(m) = fm × D ÷ Cl(m) = 0.4 × 500 mg ÷ 2.0 L·h⁻¹ = 100 mg·h·L⁻¹
>
> *Answer.* The metabolite peaks at 5.0 mg·L⁻¹ at 6.93 h. Cl(m) = 2.0 L·h⁻¹ and AUC(m) = 100 mg·h·L⁻¹. The decline is elimination-rate-limited, so the terminal slope gives the metabolite's own half-life, 0.693/0.1 = 6.93 h.
>
> *Check at the peak.* At tmax(m), formation must equal elimination. Formation is fm·K times the parent remaining: 0.4 × 0.2 × (500 × 0.250) = 10 mg·h⁻¹. Elimination is Kmet times the metabolite in the body: 0.1 × (5.0 × 20) = 10 mg·h⁻¹. They are equal.
>
> *Check the area by integration.* The integral of Equation 11.1 is the coefficient times (1/K − 1/Kmet) = −20 × (5 − 10) = 100 mg·h·L⁻¹. That is the same as Step 5, reached without using Cl(m).

## Key Takeaways
- Metabolism makes a drug more polar: a smaller Vd, less tubular reabsorption, faster excretion.
- Phase I adds a polar group by oxidation or reduction, largely by cytochrome P450; Phase II conjugates.
- Norfluoxetine, 4-hydroxypropranolol, norverapamil and desmethyldiazepam are active metabolites; NAPQI is the classic toxic one.
- NAT2, CYP2D6 and CYP2C19 genotype set an individual's metabolic rate; population allele frequencies do not follow skin colour.
- A poor metaboliser risks toxicity when the parent is active, and treatment failure when the metabolite is active.
- Cp(m) = [fm·K·D/(Vd(m)·(Kmet − K))]·(e^(−Kt) − e^(−Kmet·t)); tmax(m) = ln(Kmet/K)/(Kmet − K).
- Elimination-rate-limited (Kmet < K): the terminal slope gives the metabolite's own half-life.
- Formation-rate-limited (Kmet > K): the metabolite declines in parallel with the parent.
- AUC(m) = fm·D/Cl(m), and AUC(m)/AUC = fm·Cl_T/Cl(m).

## Check Your Understanding

**Q1.** [LO1] Cytochrome P450 takes its name from:
A) The number of amino acids in the enzyme
B) The absorption at 450 nm of its carbon monoxide complex
C) The 450 drugs it is known to metabolise
D) Its molecular weight of 450 kDa

**Q2.** [LO2] Norfluoxetine, formed from fluoxetine, is correctly described as:
A) A toxic reactive metabolite
B) An inactive conjugate
C) A Phase II product
D) An active metabolite

**Q3.** [LO3] Whether a patient is a slow or a fast acetylator is determined by:
A) The patient's NAT2 genotype
B) The patient's skin colour
C) The dose of the acetylated drug
D) The route of administration

**Q4.** [LO4] After an IV dose of parent, the time of the metabolite peak is:
A) 0.693 / Kmet
B) ln(Kmet / K) / (Kmet − K)
C) ln(K / Kmet) / K
D) 1 / (Kmet + K)

**Q5.** [LO5] A metabolite is eliminated much faster than it is formed. Its terminal decline:
A) Gives the metabolite's own half-life
B) Runs parallel to the parent, with slope K
C) Is zero order
D) Cannot be observed in plasma

**Q6.** [LO1] Phase II metabolism consists of:
A) Oxidation by cytochrome P450
B) Reduction using NADPH
C) Conjugation with an endogenous compound
D) Hydrolysis in the gut lumen

**Q7.** [LO4] After an IV dose D of parent, the AUC of a metabolite equals:
A) D / Cl_T
B) fm · Cl_T / Cl(m)
C) Cl(m) / Kmet
D) fm · D / Cl(m)

**Q8.** [LO2] Which is a toxic reactive metabolite?
A) NAPQI, formed from acetaminophen
B) Desipramine, formed from imipramine
C) Fexofenadine, formed from terfenadine
D) Desmethyldiazepam, formed from diazepam

**Q9.** [LO3] A CYP2D6 ultrarapid metaboliser is given codeine. The expected consequence is:
A) More morphine and a risk of opioid toxicity
B) Less morphine and a weaker effect
C) No change, since CYP2D6 does not act on codeine
D) Slower acetylation of codeine

**Q10.** [LO5] For an elimination-rate-limited metabolite, its own half-life is best obtained from:
A) The rising part of its curve
B) The parent's terminal slope
C) The terminal slope of the metabolite curve
D) The ratio AUC(m)/AUC

### Exercises

**E11.1** [LO5] A 500 mg IV dose of parent has K = 0.1 h⁻¹, with fm = 0.4, Kmet = 0.5 h⁻¹ and Vd(m) = 20 L. Calculate tmax(m), Cmax(m) and AUC(m). Using Cp(m) at 20 h and 30 h, calculate the terminal slope, and state which rate constant it reflects.

**E11.2** [LO4] A parent drug has Cl_T = 10 L·h⁻¹ and AUC = 20 mg·h·L⁻¹ after an IV dose. A fraction fm = 0.3 forms a metabolite with Cl(m) = 6 L·h⁻¹ and Kmet = 0.3 h⁻¹. Calculate the dose, AUC(m) by two routes, and Vd(m).

**E11.3** [LO3] A drug is cleared with Cl_T = 10 L·h⁻¹ in two patients, and its acetyl metabolite has Cl(m) = 5 L·h⁻¹. In a fast acetylator fm = 0.5; in a slow acetylator fm = 0.2. For a 500 mg IV dose, calculate AUC(m) in each patient. Explain what decides which exposure a new patient will have.

## Answers and Worked Solutions

**Q1. B** — Its reduced carbon monoxide complex absorbs at 450 nm. The family has many isoenzymes, so option C is not the origin either.

**Q2. D** — Norfluoxetine is an active metabolite that contributes to, and prolongs, the effect of fluoxetine. It is not a reactive toxic species.

**Q3. A** — Acetylation rate follows NAT2 genotype. Allele frequencies differ between populations, but both phenotypes occur in all of them, so skin colour predicts nothing.

**Q4. B** — Setting dCp(m)/dt = 0 in Equation 11.1 gives tmax(m) = ln(Kmet/K)/(Kmet − K). It has the same form as the oral tmax of Chapter 7.

**Q5. B** — Fast elimination makes formation the slow step. The metabolite then tracks the parent, and its slope is K.

**Q6. C** — Phase II joins the drug or its Phase I product to an endogenous molecule. Options A and B are Phase I reactions.

**Q7. D** — All fm·D of metabolite formed is eventually cleared by Cl(m). Option B is the ratio AUC(m)/AUC, not AUC(m) itself.

**Q8. A** — NAPQI is the reactive metabolite that causes liver injury in acetaminophen overdose. The others are active metabolites.

**Q9. A** — CYP2D6 converts codeine to morphine, so an ultrarapid metaboliser forms more morphine. Option B describes a poor metaboliser.

**Q10. C** — When Kmet < K, the parent's exponential dies first, and the metabolite's terminal slope is Kmet.

---

**E11.1 — worked solution**

*Step 1 — tmax(m).*

tmax(m) = ln(0.5/0.1) ÷ (0.5 − 0.1) h⁻¹ = 1.609 ÷ 0.4 = 4.02 h

*Step 2 — the coefficient.*

fm·K·D / (Vd(m)·(Kmet − K)) = (0.4 × 0.1 × 500) ÷ (20 × 0.4) = 20 ÷ 8 = 2.5 mg·L⁻¹

*Step 3 — Cmax(m).* At 4.02 h, e^(−0.402) = 0.669 and e^(−2.01) = 0.134.

Cmax(m) = 2.5 × (0.669 − 0.134) = 1.34 mg·L⁻¹

*Step 4 — AUC(m).*

Cl(m) = 0.5 h⁻¹ × 20 L = 10 L·h⁻¹, so AUC(m) = 0.4 × 500 ÷ 10 = 20 mg·h·L⁻¹

*Step 5 — the terminal slope.*

Cp(m) at 20 h = 2.5 × (e^(−2) − e^(−10)) = 2.5 × (0.1353 − 0.0000) = 0.338 mg·L⁻¹

Cp(m) at 30 h = 2.5 × (e^(−3) − e^(−15)) = 2.5 × 0.0498 = 0.124 mg·L⁻¹

slope = ln(0.338 / 0.124) ÷ 10 h = 1.003 ÷ 10 = 0.100 h⁻¹

*Answer.* tmax(m) = 4.02 h, Cmax(m) = 1.34 mg·L⁻¹, AUC(m) = 20 mg·h·L⁻¹. The terminal slope is 0.100 h⁻¹, which is K, the parent's rate constant.

*Why.* Kmet > K, so the case is formation-rate-limited. The metabolite's own half-life, 0.693/0.5 = 1.39 h, is invisible in its curve.

*Check.* The integral is 2.5 × (1/0.1 − 1/0.5) = 2.5 × 8 = 20 mg·h·L⁻¹, agreeing with Step 4.

**E11.2 — worked solution**

*Step 1 — the dose.*

D = Cl_T × AUC = 10 L·h⁻¹ × 20 mg·h·L⁻¹ = 200 mg

*Step 2 — AUC(m) directly.*

AUC(m) = fm × D ÷ Cl(m) = 0.3 × 200 ÷ 6 = 10 mg·h·L⁻¹

*Step 3 — AUC(m) from the ratio.*

AUC(m) / AUC = fm × Cl_T ÷ Cl(m) = 0.3 × 10 ÷ 6 = 0.50, so AUC(m) = 0.50 × 20 = 10 mg·h·L⁻¹

*Step 4 — Vd(m).*

Vd(m) = Cl(m) ÷ Kmet = 6 L·h⁻¹ ÷ 0.3 h⁻¹ = 20 L

*Answer.* The dose was 200 mg, AUC(m) = 10 mg·h·L⁻¹ by both routes, and Vd(m) = 20 L.

**E11.3 — worked solution**

*Step 1 — the fast acetylator.*

AUC(m) = 0.5 × 500 mg ÷ 5 L·h⁻¹ = 50 mg·h·L⁻¹

*Step 2 — the slow acetylator.*

AUC(m) = 0.2 × 500 mg ÷ 5 L·h⁻¹ = 20 mg·h·L⁻¹

*Answer.* The fast acetylator is exposed to 2.5 times as much metabolite, 50 against 20 mg·h·L⁻¹.

*What decides it.* The patient's NAT2 genotype sets the fraction acetylated. Both phenotypes occur in every population, so only testing or a measured concentration answers the question for the individual.

## References
1. Shargel L, Yu ABC. *Applied Biopharmaceutics and Pharmacokinetics*. 8th ed. New York: McGraw Hill Medical; 2022.
2. Rowland M, Tozer TN. *Clinical Pharmacokinetics and Pharmacodynamics: Concepts and Applications*. 5th ed. Philadelphia: Wolters Kluwer; 2019.


---

# Chapter 12: Biopharmaceutical Considerations

## Learning Objectives
By the end of this chapter you will be able to:
1. [LO1] Describe the structure of the gastrointestinal tract and the physiological factors that change drug absorption.
2. [LO2] Distinguish the mechanisms by which drugs cross the intestinal membrane.
3. [LO3] Apply the Henderson–Hasselbalch equation and the pH-partition hypothesis, and state the limits of the hypothesis.
4. [LO4] Explain how the solubility, stability, particle size and crystal form of a drug affect its absorption.
5. [LO5] Explain how the dosage form, the excipients and the manufacturing process change bioavailability.

## 12.1 The Oral Route and the Gut

Chapter 7 treated absorption as a single rate constant, Ka. This chapter looks inside it. An oral dose reaches the systemic circulation in two steps. It crosses the epithelium of the gut wall into the capillaries, and it then passes through the portal vein and the liver. Drug can be lost at either step, to metabolism in the gut wall or in the liver, before it is ever measured in plasma.

The oral route is the most used because it is convenient, painless and cheap. Oral products need no sterilisation, and they come in many forms: fast release, slow release, enteric coated, suspensions and mixtures. Its main weakness is the one this chapter is about. A high dose, or a drug poorly soluble in the gut fluids, may be incompletely absorbed. Griseofulvin is the standard example. Reformulated as a micronised powder, it was absorbed so much better that its dose could be halved.

The small intestine is the main site of absorption. It is 4–7 m long and has three parts: the duodenum, about 25 cm; the jejunum, about 2.5 m; and the ileum, about 3.5 m. It is called small because it is narrow, not because it is short. It is four to five times longer than the large intestine.

Three structures multiply its absorbing area far beyond that of a smooth tube. Mucosal folds act as baffles that mix the contents. Villi project into the lumen and are covered with absorbing epithelial cells. Microvilli stud the luminal membrane of those cells like the bristles of a brush. The cells are therefore called the **brush border**, and the enzymes embedded in their microvilli are brush-border enzymes. The epithelium also contains goblet cells that secrete mucus, endocrine cells, Paneth cells that defend against microbes, and stem cells that replace dying cells. The tight junctions between cells vary in tightness along the gut.

The upper small intestine is the optimum site for absorption. It is richly perfused, so blood keeps carrying absorbed drug away and the concentration gradient from lumen to blood is maintained.

| Segment | pH | Main function |
|---|---|---|
| Stomach | 1–3.5 | Digestion of food |
| Duodenum | 4–6.5 | Neutralisation of acid; absorption of most drugs |
| Jejunum | 5–7 | Absorption of nutrients and drugs |
| Ileum | 6–8 | Absorption of nutrients and drugs |
| Colon | 6–8 | Absorption of water and of some drugs |

A drug can be degraded before it is absorbed. The causes are acid hydrolysis in the stomach, enzymatic breakdown in the stomach or intestine, metabolism in the brush border, metabolism by colonic bacteria, and metabolism in the liver.

Protein drugs show the first three at work. Pepsin in the stomach, and trypsin, chymotrypsin and carboxypeptidases from the pancreas, break proteins into oligopeptides. The oligopeptides are then hydrolysed by peptidases of the brush border, such as aminopeptidase N and dipeptidyl peptidase IV, and by cytosolic peptidases inside the enterocyte. The products are free amino acids and very small peptides. Lactase and maltase, also brush-border enzymes, are disaccharidases: they digest carbohydrates, not peptides. Intact proteins have no carrier in normal enterocytes and cannot pass the tight junctions. Protein drugs are therefore not absorbed after oral administration [1].

## 12.2 Physiological Factors Affecting Absorption

*Perfusion.* The splanchnic circulation receives about 28% of the cardiac output, and its flow rises after meals. Faster mesenteric flow removes absorbed drug from the gut wall faster and so speeds absorption. Some lipophilic drugs, like dietary lipids, are absorbed into the lymph instead. Lymphatic absorption does not depend on blood flow and bypasses the liver.

*Gastric emptying.* Most absorption happens after the stomach empties, so gastric emptying often limits the rate. Liquids leave faster than tablets and capsules, and food delays emptying. A large indigestible solid, bigger than the closed pylorus, cannot leave during the fed state. It must wait for the **interdigestive migrating myoelectric complex** (IMMC), a cycle of motor activity that sweeps the fasting stomach and intestine every 1.5–2 h.

| IMMC phase | Duration (min) | Activity |
|---|---|---|
| 1 (basal) | 45–60 | Nearly quiescent |
| 2 (preburst) | 30–45 | Contractions of rising frequency and strength |
| 3 (burst) | 5–15 | Maximal contractions; the pylorus opens and the housekeeper wave clears indigestible solids |
| 4 | 0–5 | Short transition back to phase 1 |

Slow gastric emptying delays the onset of action and reduces the rate, and perhaps the extent, of absorption. It prolongs the exposure of acid-labile drugs such as penicillin to gastric acid. It lengthens the contact of aspirin with the gastric mucosa, and so its irritation. It also delays the release of an enteric-coated tablet, which does not begin until the tablet leaves the stomach.

*Food.* Food changes absorption in several ways. It raises gastric pH, which changes the dissolution of pH-sensitive drugs. Ketoconazole and itraconazole need an acid stomach to dissolve, and an acidic cola drink improves their absorption. Food delays emptying, which prolongs acid exposure and degrades acid-sensitive drugs such as erythromycin and penicillin. It increases mesenteric blood flow, so a drug such as propranolol reaches the liver faster, saturates more of its first-pass metabolism, and gives a higher bioavailability. Fatty meals increase bile flow, which emulsifies and solubilises lipophilic drugs such as griseofulvin. And food is taken with irritant drugs such as NSAIDs and iron salts to protect the stomach. That may slow absorption, but it leaves the extent unchanged.

*Transit.* Small-intestinal transit is fairly regular, averaging 3 ± 1 h. The effective time available for absorption is therefore about 3–8 h. That sets a limit on sustained-release design: a product releasing drug over 12 h will carry part of the dose past the small intestine before it is released. The colon has a smaller surface and a variable transit of 20–36 h. It is still the absorption site for drugs that need bacterial activation, such as sulfasalazine. Transit is measured by radiography, with a radio-opaque marker such as barium, or more safely by gamma scintigraphy, with a short-lived radionuclide such as technetium-99m.

*Disease.* Heart failure lowers mesenteric blood flow and so reduces absorption. Diarrhoea shortens residence time. Parkinson's disease slows motility. Achlorhydria raises gastric pH and changes drug solubility. Crohn's disease and ulceration alter membrane permeability, gallstones alter the bile available to lipophilic drugs, and changes in enzyme secretion or gut flora alter drug stability.

## 12.3 How Drugs Cross the Membrane

The gut membrane is a phospholipid bilayer, with the polar heads facing outward and the fatty chains inward, carrying proteins and crossed by protein-lined aqueous pores. A drug can cross it by two routes. The **transcellular** route goes through the cells and suits drugs that are unionised and lipid soluble. The **paracellular** route goes between the cells, through the tight junctions, and suits small polar molecules such as water, urea and some ions. Large or highly charged molecules, including proteins and protein-bound drug, can use neither.

![A row of four epithelial cells with microvilli on their upper surface, between a band labelled gut lumen above and a band labelled blood below. In the first cell a straight arrow runs from lumen to blood, labelled passive diffusion, unionised and lipid soluble. A dashed arrow runs down through the gap between the first and second cells, labelled paracellular, small polar molecules. In the second cell an arrow with carrier dots on both membranes runs down, labelled carrier-mediated, active or facilitated, saturable. In the third cell a red arrow runs upward from inside the cell back into the lumen, labelled P-gp efflux. In the fourth cell an arrow enters a dashed vesicle and continues to the blood, labelled vesicular transport, for example vitamin B12 with intrinsic factor.](../rework/figures/out/ch12-transport.png)

*Figure 12.1 — Routes across the intestinal epithelium. Unionised, lipid-soluble drug diffuses through the cells; small polar molecules pass between them; carriers move drug in either direction and saturate; P-glycoprotein pumps drug back into the lumen; and vesicles carry large molecules such as vitamin B12 bound to intrinsic factor.*  
Original diagram, redrawn from the first edition pages 61-66 (original)

*Convective (pore) transport.* Very small molecules, such as water, urea and low molecular weight sugars, pass through water-filled channels about 0.4 nm wide. Pore transport matters little for drug absorption from the gut, but it contributes to renal excretion and hepatic uptake.

*Passive diffusion.* **Passive diffusion** is the commonest transcellular mechanism. Drug moves from high to low concentration, down its gradient, with no expenditure of energy.

> **Key Equation:** Equation 12.1 — Fick's law for absorption
>
> $$\frac{dQ}{dt} = \frac{D A K}{h}\left(C_{GI} - C_p\right) = p A \left(C_{GI} - C_p\right)$$
>
> Because Cp is small compared with C_GI:    dQ/dt ≈ p · A · C_GI
>
> D is the diffusion coefficient (cm²·s⁻¹), A the surface area (cm²), K the lipid/water partition coefficient (dimensionless), h the membrane thickness (cm), and p = D·K/h the **permeability coefficient**, in cm·s⁻¹.
>
> Keep the area outside the coefficient. D·K/h has units of cm²·s⁻¹ ÷ cm = cm·s⁻¹, a velocity, which is what a permeability coefficient is. Multiplying by A gives p·A in cm³·s⁻¹, a volume per time — the permeability–surface-area product, often written PS. Texts that call D·A·K/h "the permeability coefficient" have folded the anatomy of the gut into a constant that is supposed to describe the membrane alone.

The simplified form is a first order process, which is why Chapter 7 could describe absorption with a single rate constant. The membrane has much the same thickness at all absorption sites. The capillaries of the brain are the exception: tightly joined and surrounded by glial cells, they make up the blood–brain barrier.

*Carrier-mediated transport.* A carrier in the membrane binds the drug and moves it across. There are two kinds.

| | Active transport | Facilitated diffusion |
|---|---|---|
| Direction | Against the concentration gradient | Down the concentration gradient |
| Energy | Required, from ATP | Not required |
| Competition between similar molecules | Yes | Yes |
| Saturation at high dose | Yes; the rate becomes constant | Yes |
| Examples | Glucose and galactose, carried with sodium by SGLT1; amino acids | Fructose; some renal reabsorption |

Both are saturable, so at high doses the rate of absorption approaches a ceiling. That is Chapter 10's Michaelis–Menten behaviour, now at the gut wall. Lactose and starch have no carrier and must be digested to monosaccharides first.

The brush border holds many nutrient transporters, and drugs of similar structure can use them. Oral cephalosporins are absorbed by one such transporter, which cefazolin, a cephalosporin given only by injection, does not use. **P-glycoprotein** works in the opposite direction. It pumps a range of lipophilic and cytotoxic drugs back out of the enterocyte into the lumen and so reduces their absorption. Inhibiting it increases the absorption of those drugs.

*Vesicular transport.* In **vesicular transport** the cell membrane folds around a particle or a volume of fluid and engulfs it. Pinocytosis takes in fluid and small solutes; phagocytosis takes in larger particles. It is the proposed route for the oral Sabin polio vaccine and some large proteins. Vitamin B₁₂ enters this way too, bound to intrinsic factor, by receptor-mediated endocytosis in the ileum. Exocytosis is the reverse, as when insulin leaves the pancreatic cell.

*Ion-pair formation.* A drug that is charged at every gut pH cannot diffuse passively. It may still be absorbed if it combines with an endogenous organic ion of opposite charge. The resulting **ion pair** is electrically neutral, partitions into the membrane and diffuses across. Quaternary ammonium compounds, which carry a permanent positive charge, are the example this mechanism was proposed for. Propranolol forms an ion pair with oleic acid, and quinine with hexylsalicylate.

Tetracycline is not a quaternary compound. It is amphoteric, with three ionisable groups, so a large part of it carries a charge at every gut pH. Its absorption is incomplete, and it falls further when calcium, magnesium or iron forms an insoluble complex with it.

## 12.4 pH, pKa and the pH-Partition Hypothesis

Most drugs are weak acids or weak bases. Only the unionised form crosses the membrane readily, so the fraction unionised at the site of absorption matters. The **Henderson–Hasselbalch equation** gives it from the pKa of the drug and the pH of the fluid.

> **Key Equation:** Equation 12.2 — Henderson–Hasselbalch
>
> Weak acid:  pKa − pH = log([U]/[I]),  so the fraction unionised is 1 / (1 + 10^(pH − pKa))
>
> Weak base:  pKa − pH = log([I]/[U]),  so the fraction unionised is 1 / (1 + 10^(pKa − pH))
>
> where [U] and [I] are the concentrations of unionised and ionised drug.

The ionisation of a weak acid increases as the pH rises. The ionisation of a weak base increases as the pH falls.

The **pH-partition hypothesis** states that drugs cross the gut membrane by passive diffusion, in proportion to the unionised fraction at the pH next to the membrane. A drug may therefore be well absorbed from a segment with a favourable pH and poorly from another.

| Drug type | pKa | Examples | Ionisation in the gut | Absorption |
|---|---|---|---|---|
| Very weak acid | > 8 | Phenytoin, ethosuximide, barbiturates | Unionised at all gut pH | Rapid, independent of pH |
| Weak acid | 2.5–7.5 | Aspirin, ibuprofen, penicillins | Unionised in stomach, ionised in intestine | Favoured in stomach |
| Strong acid | < 2.5 | Cromolyn sodium | Ionised at all gut pH | Poor throughout |
| Very weak base | < 5 | Caffeine, theophylline, diazepam | Unionised at all gut pH | Rapid, independent of pH |
| Weak base | 5–11 | Morphine, chloroquine, imipramine, amitriptyline | Ionised in stomach, unionised in intestine | Favoured in intestine |
| Strong base | > 11 | Mecamylamine, guanethidine | Ionised at all gut pH | Poor throughout |

Gastric pH is not fixed. Gastric secretion itself is below pH 1, but the contents are usually at pH 1–3 and rise briefly to about 5 after a meal. Fasting lowers the pH, duodenal ulcer lowers it further, and fatty food inhibits acid secretion. Antacids, H₂-receptor blockers such as cimetidine and ranitidine, and drugs with anticholinergic activity such as atropine all raise it.

Brodie expressed the hypothesis as an equilibrium ratio. At equilibrium the unionised concentration is the same on both sides of the membrane, because only that form crosses. The ionised concentration on each side is set by the local pH.

> **Key Equation:** Equation 12.3 — Brodie's distribution ratio
>
> R_D = total concentration in blood / total concentration in the gut = ([U] + [I])_blood / ([U] + [I])_gut

A large R_D means a steep effective gradient from gut to blood. The first edition calls this ratio D; it is written R_D here so that it is not confused with the dose or with the diffusion coefficient.

> **Worked Example:** Example 12.1 — where is a weak acid favoured?
>
> A weak acid has pKa = 5.4. Compare R_D for absorption from the stomach (pH 3.4) and from the intestine (pH 6.4), with blood at pH 7.4.
>
> *Step 1 — the blood side.* For an acid, [U]/[I] = 10^(pKa − pH) = 10^(5.4 − 7.4) = 10^(−2) = 0.01.
>
> So [I] = 100 [U], and the total in blood = [U] + 100[U] = 101 [U].
>
> *Step 2 — the stomach.* [U]/[I] = 10^(5.4 − 3.4) = 10² = 100.
>
> So [I] = 0.01 [U], and the total in the stomach = 1.01 [U].
>
> *Step 3 — R_D from the stomach.* The unionised concentration is equal on both sides and cancels.
>
> R_D = 101 [U] ÷ 1.01 [U] = 100
>
> *Step 4 — the intestine.* [U]/[I] = 10^(5.4 − 6.4) = 10^(−1) = 0.1.
>
> So [I] = 10 [U], and the total in the intestine = 11 [U].
>
> *Step 5 — R_D from the intestine.*
>
> R_D = 101 [U] ÷ 11 [U] = 9.2
>
> *Answer.* R_D is 100 from the stomach and 9.2 from the intestine. On the pH-partition hypothesis alone, the stomach is the favoured site for this acid by a factor of about 11.
>
> *Check by a second route.* R_D is the ratio of the unionised fractions, gut over blood, because [U] is common to both. The unionised fraction in the stomach is 1/(1 + 10^(3.4 − 5.4)) = 1/1.01 = 0.990. In blood it is 1/(1 + 10^(7.4 − 5.4)) = 1/101 = 0.0099. Their ratio is 0.990/0.0099 = 100, the same answer.

The hypothesis is a useful first guide, but it fails in known ways. Most weak acids are in fact well absorbed from the small intestine, contrary to Example 12.1. Quaternary ammonium compounds are ionised at every pH yet are absorbed to some extent. Barbitone (pKa 7.8) and thiopentone (pKa 7.6) are both almost wholly unionised in the stomach, but thiopentone is absorbed much better because its unionised form is far more lipid soluble.

The discrepancies have four explanations. The very large surface area of the small intestine outweighs its less favourable pH. So does the long residence time there. Some charged drugs are absorbed as ion pairs. And some drugs are carried by active transport. The hypothesis also ignores lipid solubility, which the barbiturate pair shows is decisive.

> **Common Mistake:** Treating R_D as a rate. It is an equilibrium ratio. The rate of absorption also depends on the area available and the time spent there, and on both counts the small intestine wins by a wide margin.

## 12.5 Physicochemical Properties of the Drug

A drug must dissolve before it can be absorbed. For a sparingly soluble drug, the rate of dissolution often limits the rate of absorption. The slowest step in a series of processes is the **rate-limiting step**. For a tablet the series is disintegration, then dissolution, then absorption.

| Property | Why it matters |
|---|---|
| pKa and pH profile | Controls solubility and stability of the final product |
| Particle size | Controls surface area and so the dissolution rate |
| Crystal form | Different forms have different solubilities and stabilities |
| Hygroscopicity | Absorbed moisture can change physical structure and stability |
| Partition coefficient | A very lipophilic drug may dissolve poorly from its product |
| Excipient interactions | Incompatibility or trace impurities can reduce stability |
| pH stability profile | Shows the pH at which the drug degrades |

*Solubility and pH.* A weak base dissolves best in acid, forming a soluble salt. A weak acid dissolves best in the more alkaline intestine. An acidic or basic excipient can improve solubility; an alkaline buffer, for instance, speeds the dissolution of aspirin.

*Stability and pH.* The pH stability profile plots the degradation rate constant against pH. Erythromycin decomposes rapidly in acid but is stable at neutral and alkaline pH. It is protected in two ways: by an enteric coat, or by a poorly soluble salt such as erythromycin stearate, which passes the stomach undissolved and releases the base in the intestine. Penicillin G is also acid-labile and is best formulated to dissolve little in the stomach and quickly in the intestine.

*Particle size.* Reducing particle size increases the surface area and so the dissolution rate. **Micronisation** has improved the absorption of griseofulvin, nitrofurantoin, chloramphenicol, tetracycline and many steroids.

Smaller is not always better. Micronised aspirin, phenacetin and phenobarbital dissolve more slowly, because their effective surface area falls. Hydrophobic particles adsorb air and resist wetting. Particles below about 0.1 µm reaggregate. Some particles acquire an electrical charge that keeps the wetting medium away.

*Crystal form.* **Crystal polymorphism** is the ability of a drug to crystallise in more than one arrangement. Polymorphs share a chemical structure but differ in solubility, density, hardness and compressibility. The form with the lowest free energy is the most stable, and metastable forms may convert to it on storage. An amorphous, non-crystalline form usually dissolves faster than any crystal. Chloramphenicol palmitate is the classic case. Given as a suspension, its plasma concentration depended on the proportion of the more soluble polymorph B. A crystal may also include solvent, forming a solvate, or water, forming a hydrate. Erythromycin dihydrate, monohydrate and anhydrate dissolve at different rates.

## 12.6 The Dosage Form, Excipients and Manufacture

Every step a product must go through before absorption is another place the rate can be limited. A solution needs no disintegration and no dissolution. A suspension needs dissolution. A capsule must first release its contents, and a tablet must first disintegrate. That gives the usual ranking of bioavailability:

solution > emulsion > suspension > soft gelatin capsule > hard gelatin capsule > tablet > coated tablet > enteric-coated tablet > sustained-release product

Read it as a tendency that follows from the number of steps, not as a law. Chapter 7 showed that slowing absorption moves Cpmax and tmax but need not move the AUC. The formulation can also overturn the order entirely. An unprotected solution of erythromycin base is degraded by gastric acid, so an enteric-coated tablet of the same drug can deliver more of it than the solution. The position of any product in the ranking must be measured, not assumed.

*Solutions.* Absorption is rapid and complete, and gastric emptying is often the rate-limiting step. An acidic drug given as a salt may precipitate in the stomach, but the precipitate is fine and redissolves readily. A poorly water-soluble drug can be dissolved in a mixed solvent of water with alcohol or glycerol, or given as an oily emulsion or in a soft gelatin capsule.

*Suspensions.* A well-formulated suspension is second only to a solution. A finely divided powder dissolves fast, and a surfactant improves dispersion and prevents caking. Phenytoin, poorly water soluble, is often better given this way.

*Capsules.* The hard gelatin shell must break down quickly. The contents are not compressed, so a capsule should perform better than a tablet. A hydrophobic drug needs a dispersing agent to stop the powder clumping.

*Tablets.* The tablet is the commonest and the most complex oral form. Compression reduces the effective surface area, and any coating must break down quickly. Sustained-release tablets allow less frequent dosing of short half-life drugs and give steadier plasma levels. Their formulation is more complex and more expensive, and a failure of the release mechanism can deliver a large, toxic dose at once.

*Excipients.* An **excipient** is any non-drug component of the formulation. Excipients ensure acceptability, stability and uniform dosing, but they also change absorption.

| Excipient | Effect on absorption |
|---|---|
| Suspending agent (methylcellulose) | Raises viscosity and complexes nitrofurantoin; reduces rate and extent |
| Lubricant (magnesium stearate) | Hydrophobic; in excess repels water and slows dissolution |
| Coating (shellac) | Cross-links on ageing and slows dissolution |
| Surfactant | Low levels improve wetting; high levels trap drug in micelles. Polysorbate 80 improves phenacetin absorption |
| Alkaline excipient (sodium bicarbonate) | Dissolves aspirin as its salt: dissolution in a reactive medium |
| Calcium carbonate | Forms an insoluble complex with tetracycline |
| Talc | Adsorbs cyanocobalamin and reduces its absorption |

> **Why It Matters in Practice:** In the Australian phenytoin outbreak, epileptic patients stable on sodium phenytoin capsules developed signs of phenytoin toxicity. The only change was the diluent: calcium sulphate dihydrate had been replaced by lactose, with the same amount of drug in each capsule. Calcium sulphate had been reducing absorption, probably by forming a poorly absorbed calcium–phenytoin complex. With lactose, bioavailability rose, and so did the plasma levels, beyond the safe range. Chapter 10 explains why the rise was so large: phenytoin elimination is saturable [2].

*Manufacturing.* Three process variables matter. Wet granulation, the most usual method, generally improves the dissolution of poorly soluble drugs. Compression force raises tablet density and hardness, lowers porosity and slows penetration of fluid, although very high forces can instead fracture particles. The packing density of capsule contents can either slow dissolution or, by building pressure as fluid enters, make the capsule burst and disperse faster.

## Key Takeaways
- The upper small intestine is the main absorption site, thanks to its area and blood supply.
- Brush-border and cytosolic peptidases hydrolyse oligopeptides; lactase and maltase digest carbohydrates.
- Gastric emptying often limits the rate of absorption; indigestible solids leave only with the phase 3 housekeeper wave.
- Passive diffusion follows Fick's law and is first order; carrier-mediated transport saturates.
- Vitamin B₁₂ is absorbed by intrinsic-factor-mediated receptor endocytosis.
- Tetracycline is amphoteric with three ionisable groups; quaternary ammonium compounds are the ion-pair case.
- Henderson–Hasselbalch gives the unionised fraction; the pH-partition hypothesis ignores area, residence time and lipid solubility.
- Smaller particles usually dissolve faster, but hydrophobic micronised powders may not.
- The dosage-form ranking is a tendency from the number of steps; formulation can overturn it.
- Excipients change absorption, as the Australian phenytoin outbreak showed.

## Check Your Understanding

**Q1.** [LO1] The main site of drug absorption after an oral dose is:
A) The stomach
B) The upper small intestine
C) The colon
D) The oesophagus

**Q2.** [LO2] Oligopeptides produced by digestion of a protein drug are hydrolysed by:
A) Lactase and maltase
B) Pepsin in the stomach
C) Bacterial enzymes in the colon
D) Brush-border and cytosolic peptidases

**Q3.** [LO3] A weak acid has pKa = 4.4. The fraction unionised at pH 2.4 is:
A) 0.99
B) 0.50
C) 0.10
D) 0.01

**Q4.** [LO2] Active transport differs from facilitated diffusion because it:
A) Uses a carrier
B) Can be saturated
C) Requires energy and moves drug against its concentration gradient
D) Shows competition between similar molecules

**Q5.** [LO5] In the Australian phenytoin outbreak, toxicity followed:
A) An increase in the amount of phenytoin per capsule
B) Replacement of calcium sulphate dihydrate by lactose as the diluent
C) A change from capsules to tablets
D) A change in the crystal form of phenytoin

**Q6.** [LO4] Micronisation slows the dissolution of aspirin because:
A) Aspirin is a protein
B) Hydrophobic particles adsorb air, resist wetting and reaggregate
C) Smaller particles always have less surface area
D) Aspirin is absorbed only as an ion pair

**Q7.** [LO3] Tetracycline is correctly described as:
A) A quaternary ammonium compound
B) A strong base ionised at all gut pH
C) A neutral molecule absorbed by pore transport
D) Amphoteric, with three ionisable groups

**Q8.** [LO1] Phase 3 of the interdigestive migrating myoelectric complex:
A) Opens the pylorus and sweeps indigestible solids from the stomach
B) Is the longest phase of the cycle
C) Occurs only after a meal
D) Is a period of motor quiescence

**Q9.** [LO4] Compared with a crystalline form of the same drug, an amorphous form usually:
A) Dissolves more slowly
B) Has a different chemical structure
C) Dissolves faster
D) Is the most stable form

**Q10.** [LO5] The ranking solution > suspension > capsule > tablet is best described as:
A) A law that holds for every drug
B) A regulatory requirement
C) A tendency from the number of steps before absorption, which formulation can overturn
D) A ranking of the extent of absorption only

### Exercises

**E12.1** [LO3] Aspirin is a weak acid with pKa = 3.5. Calculate its unionised fraction at pH 1.5 and at pH 6.5. Explain why aspirin is nonetheless absorbed mainly from the small intestine.

**E12.2** [LO3] A weak base has pKa = 6.4. Calculate Brodie's ratio R_D for absorption from the stomach (pH 3.4) and from the intestine (pH 6.4), with blood at pH 7.4. Compare the result with Example 12.1.

**E12.3** [LO5] A patient takes 400 mg·day⁻¹ of phenytoin, with Km = 4 mg·L⁻¹ and Vmax = 500 mg·day⁻¹ as in Example 10.1. Suppose a change of diluent raises the bioavailability from 0.80 to 1.00. Calculate the steady-state concentration before and after, and explain the size of the change.

## Answers and Worked Solutions

**Q1. B** — The upper small intestine combines the largest absorbing area with a rich blood supply. The stomach has a small area and a short residence time.

**Q2. D** — Oligopeptides are hydrolysed by brush-border peptidases, such as aminopeptidase N and dipeptidyl peptidase IV, and by cytosolic peptidases. Lactase and maltase are disaccharidases.

**Q3. A** — For an acid the unionised fraction is 1/(1 + 10^(2.4 − 4.4)) = 1/1.01 = 0.99. Two pH units below the pKa, an acid is almost entirely unionised.

**Q4. C** — Both use saturable carriers with competition. Only active transport spends energy to move drug uphill.

**Q5. B** — The drug content was unchanged. Calcium sulphate had been reducing absorption, so replacing it raised bioavailability and plasma levels.

**Q6. B** — Micronisation should raise the surface area, but for these hydrophobic drugs the effective, wetted area falls. Option C is wrong because size reduction raises total area.

**Q7. D** — Tetracycline has three ionisable groups and is amphoteric. Quaternary ammonium compounds carry a permanent charge.

**Q8. A** — Phase 3, the burst, lasts 5–15 min with maximal contractions and an open pylorus. Phase 1 is the long quiescent phase.

**Q9. C** — An amorphous solid has no crystal lattice to break, so it dissolves faster. It is usually less stable and may crystallise on storage.

**Q10. C** — Each extra step can slow release, but an acid-labile drug such as erythromycin base is better delivered by an enteric-coated tablet than by a solution.

---

**E12.1 — worked solution**

*Step 1 — pH 1.5.*

unionised fraction = 1 / (1 + 10^(1.5 − 3.5)) = 1 / (1 + 0.01) = 0.990

*Step 2 — pH 6.5.*

unionised fraction = 1 / (1 + 10^(6.5 − 3.5)) = 1 / (1 + 1000) = 0.0010

*Answer.* Aspirin is 99.0% unionised at pH 1.5 but only 0.10% unionised at pH 6.5.

*Why the intestine still wins.* The unionised fraction in the intestine is a thousand times smaller, but the absorbing area is enormously larger and the residence time much longer. As fast as the unionised form is absorbed, more of the drug converts to it, so absorption continues. This is the first limitation of the pH-partition hypothesis in Section 12.4.

**E12.2 — worked solution**

For a base, [U]/[I] = 10^(pH − pKa).

*Step 1 — blood, pH 7.4.* [U]/[I] = 10^(1) = 10, so [I] = 0.1 [U] and the total = 1.1 [U].

*Step 2 — stomach, pH 3.4.* [U]/[I] = 10^(−3), so [I] = 1000 [U] and the total = 1001 [U].

R_D = 1.1 ÷ 1001 = 0.0011

*Step 3 — intestine, pH 6.4.* [U]/[I] = 10⁰ = 1, so [I] = [U] and the total = 2 [U].

R_D = 1.1 ÷ 2 = 0.55

*Answer.* R_D = 0.0011 from the stomach and 0.55 from the intestine.

*Comparison.* For this base the intestine is favoured by a factor of 500. For the acid of Example 12.1 the stomach was favoured. The acid is trapped as ions in alkaline blood, raising R_D; the base is trapped as ions in the acid stomach, lowering it.

**E12.3 — worked solution**

*Step 1 — the dose actually absorbed.*

before: 0.80 × 400 = 320 mg·day⁻¹    after: 1.00 × 400 = 400 mg·day⁻¹

*Step 2 — steady state before.* From Equation 10.2:

Css = 4 × 320 ÷ (500 − 320) = 1280 ÷ 180 = 7.1 mg·L⁻¹

*Step 3 — steady state after.*

Css = 4 × 400 ÷ (500 − 400) = 1600 ÷ 100 = 16.0 mg·L⁻¹

*Answer.* The steady-state level rises from 7.1 to 16.0 mg·L⁻¹, a factor of 2.25, for a 25% rise in bioavailability.

*Why the change is so large.* With linear kinetics a 25% rise in absorbed dose would raise Css by 25%. Phenytoin's elimination is close to saturation at these doses, so the extra absorbed drug meets almost no extra elimination capacity. This is exactly what the Australian patients experienced.

## References
1. Shargel L, Yu ABC. *Applied Biopharmaceutics and Pharmacokinetics*. 8th ed. New York: McGraw Hill Medical; 2022.
2. Rowland M, Tozer TN. *Clinical Pharmacokinetics and Pharmacodynamics: Concepts and Applications*. 5th ed. Philadelphia: Wolters Kluwer; 2019.


---

# Chapter 13: Bioavailability and Bioequivalence

## Learning Objectives
By the end of this chapter you will be able to:
1. [LO1] Define pharmaceutical equivalents, pharmaceutical alternatives, therapeutic equivalents and bioequivalent products, and tell them apart.
2. [LO2] Calculate absolute and relative bioavailability from plasma or urine data, and separate F into its absorption, gut-wall and hepatic parts.
3. [LO3] Compare the methods used to assess bioavailability, and interpret plasma curves for rate and extent.
4. [LO4] Describe the design of a bioequivalence study and apply the acceptance criterion correctly.
5. [LO5] Classify a drug by the Biopharmaceutics Classification System and decide whether a biowaiver can apply.

## 13.1 Terms That Recur

Chapter 1 defined bioavailability as the rate and extent of absorption of a drug from its dosage form into the systemic circulation. For a product not meant to reach the blood, such as an antacid, bioavailability is judged instead by its effect at the site of action. The concept dates from 1945, when Oser and colleagues compared the absorption of vitamins from different products. It became a regulatory issue in the late 1960s, as prescribing by generic name spread and pharmacists began choosing between products. The question was simple: is a cheaper product containing the same dose as good as the original?

A drug substance is the active pharmaceutical ingredient. A drug product is the finished dosage form, containing the active ingredient with inactive ingredients. The generic, or non-proprietary, name is assigned to the compound during early development, such as acetaminophen. The proprietary name is the trade name given by the innovator company. A single-source product is available from one manufacturer, usually under patent. A multi-source product contains the same active ingredient in the same dosage form but is marketed by several manufacturers.

The definitions that matter most for substitution are these.

**Pharmaceutical equivalents** contain the same molar amount of the same active ingredient, in the same dosage form, meeting comparable standards, and are given by the same route [6].

| Must be the same | May differ |
|---|---|
| Active ingredient | Shape |
| Strength or concentration | Scoring configuration |
| Dosage form, including its release type (immediate or modified) | Packaging |
| Route of administration | Excipients, such as colour, flavour or preservative |
| | Expiry date |
| | Minor aspects of labelling |

The release type belongs in the left column. An immediate-release tablet and an extended-release tablet of the same drug and strength are different dosage forms. They are not pharmaceutical equivalents.

**Pharmaceutical alternatives** contain the same active moiety, given by the same route. They differ in dosage form, or in chemical form such as the salt or ester. Tetracycline phosphate and tetracycline hydrochloride, each equivalent to 250 mg of tetracycline base, are alternatives; so are a paracetamol tablet and a paracetamol syrup. Dispensing an alternative in place of the prescribed product is pharmaceutical substitution, and it needs the prescriber's approval.

**Therapeutic equivalents** are pharmaceutical equivalents that give the same clinical efficacy and safety when given to the same patients in the same regimen. Pharmaceutical equivalence alone does not guarantee this: excipients and manufacturing can change performance, as Chapter 12 showed. Therapeutic alternatives contain different active ingredients of the same pharmacological class, used for the same purpose, such as ibuprofen and naproxen. Dispensing one for the other is therapeutic substitution, and it also needs approval.

Products are **bioequivalent** when they are pharmaceutical equivalents or alternatives and give the same rate and extent of absorption under the same conditions. Interchangeable products are bioequivalent products accepted as therapeutic equivalents, so a pharmacist may dispense any of them.

## 13.2 Absolute and Relative Bioavailability

Three things control how much drug reaches its site of action. The first is release from the dosage form and absorption. The second is first-pass loss on the way to the circulation. The third is distribution and elimination afterwards [1]. Bioavailability studies compare the first two. Comparative studies between products compare only the first.

**Absolute bioavailability**, F, compares an oral dose with an intravenous one. Chapter 7 showed that AUC = F·D₀/Cl. If clearance is the same on both occasions, it cancels.

> **Key Equation:** Equation 13.1 — absolute and relative bioavailability
>
> F = (AUC_oral / D_oral) ÷ (AUC_IV / D_IV) = (Du∞,oral / D_oral) ÷ (Du∞,IV / D_IV)
>
> $$F_{rel} = \frac{AUC_{test} / D_{test}}{AUC_{ref} / D_{ref}}$$
>
> Multiply by 100 for a percentage. F = 1 for an intravenous dose, and lies between 0 and 1 for an extravascular one.

The urine form uses Du∞, the total amount excreted unchanged, from Chapter 3. It needs a drug excreted unchanged in significant amount and a collection long enough to recover it all, usually 7–10 half-lives.

**Relative bioavailability** compares a product with a reference product instead of an intravenous dose. It is the measure used when a generic is compared with the innovator, and it can exceed 100%.

What F measures is easy to misread. It is not the fraction absorbed. A dose that crosses the gut wall must still pass the gut-wall enzymes and then the liver before it reaches the systemic circulation. Each can remove part of it. This loss before the drug is ever measured in plasma is the **first-pass effect**.

> **Key Equation:** Equation 13.2 — the three parts of F
>
> $$F = f_a \times F_g \times F_h$$
>
> fa is the fraction of the dose absorbed across the gut wall. Fg is the fraction escaping gut-wall metabolism, and Fh the fraction escaping the liver on its first pass.

A drug can therefore be completely absorbed, with fa = 1, and still have F well below 1. The fraction lost on the first pass is 1 − F. The first-pass effect matters most for drugs with a high clearance, because the liver that clears them from the blood also clears them from the portal vein [2].

> **Worked Example:** Example 13.1 — a well-absorbed drug with low bioavailability
>
> The constants are illustrative, of the size reported for propranolol. A 10 mg IV dose gives AUC = 200 µg·h·L⁻¹. An 80 mg oral dose gives AUC = 400 µg·h·L⁻¹. A radiolabel study shows that 95% of the oral dose is absorbed. Find F, the clearance, and the fraction surviving the liver, assuming no gut-wall metabolism.
>
> *Step 1 — absolute bioavailability.*
>
> F = (400 ÷ 80) ÷ (200 ÷ 10) = 5.0 ÷ 20.0 = 0.25
>
> *Step 2 — clearance, from the IV dose.* Convert the area: 200 µg·h·L⁻¹ = 0.200 mg·h·L⁻¹.
>
> Cl = 10 mg ÷ 0.200 mg·h·L⁻¹ = 50 L·h⁻¹
>
> *Step 3 — separate F.* With fa = 0.95 and Fg taken as 1:
>
> Fh = F ÷ (fa × Fg) = 0.25 ÷ 0.95 = 0.26
>
> *Answer.* F = 0.25 and Cl = 50 L·h⁻¹. Of the drug absorbed, only 26% survives the liver; 74% is removed on the first pass.
>
> *Check by a second route.* The oral area gives Cl/F directly: 80 mg ÷ 0.400 mg·h·L⁻¹ = 200 L·h⁻¹. Dividing the IV clearance by F gives 50 ÷ 0.25 = 200 L·h⁻¹. The two agree, which confirms that clearance was the same on both occasions, the condition Equation 13.1 needs.
>
> *What it means.* The drug is almost completely absorbed, yet three quarters of every oral dose is lost before it reaches the circulation. That is why the oral dose of propranolol is several times the intravenous dose. It is also why food, which speeds delivery to the liver, can raise its F (Chapter 12).

## 13.3 Measuring Bioavailability

Five methods are used, in decreasing order of precision.

*Plasma data.* The AUC measures extent, and Cpmax and tmax measure rate, as Chapter 1 set out. Cpmax also shows whether the drug is absorbed enough to act, and warns of toxic levels. Chapter 7 showed that tmax depends only on Ka and K. AUC is found by the trapezoidal rule. It should rise in proportion to the dose. A rise more than proportional suggests saturation of a metabolic pathway, as in Chapter 10.

*Urine data.* Du∞ is proportional to the amount absorbed. The excretion rate dDu/dt follows the plasma curve, because it equals Ke·Vd·Cp, so its peak time parallels tmax.

*Acute pharmacological effect.* When the drug cannot be measured accurately, a measurable effect is plotted against time and the area under the effect curve is used. Examples are pupil diameter, heart rate, blood pressure and the skin blanching produced by a topical corticosteroid. The effect should be followed for at least three half-lives.

*Clinical response.* Failure suggests poor availability, a good response adequate availability, and toxicity high availability. This is the least sensitive, least accurate and least reproducible method, because patients differ in their response for reasons unrelated to absorption: receptor sensitivity, interactions, age and tolerance. It is used for products such as topical antifungals.

*In-vitro dissolution.* This is the cheapest method, needing no volunteers. The formulation that dissolves fastest in vitro will generally be absorbed fastest in vivo. Chapter 14 describes it.

![Three plasma concentration curves over 24 hours. Curve A rises steeply to the highest peak, about 6.7 relative units, at 2 hours. Curve B rises more slowly to a lower, broader peak of about 4.5 at 4 hours and stays higher than A later on. Curve C peaks at 2 hours like A but at half its height. Dashed lines drop from each peak to the time axis. A key at the right lists A with AUC 50 and tmax 2 hours, B with AUC 50 and tmax 4 hours, and C with AUC 25 and tmax 2 hours.](../rework/figures/out/ch13-rate-extent.png)

*Figure 13.1 — Rate and extent read from plasma curves, for the three formulations of the first edition's example. A and B have the same AUC and so the same extent, but A peaks earlier and so is absorbed faster. C has the same tmax as A and so the same rate, but half the AUC and so half the extent.*  
Original diagram, redrawn from the first edition page 92 (original)

The figure shows how plasma curves are read. Products A and B have the same AUC, so they have the same extent of bioavailability. A peaks at 2 h and B at 4 h, so A has the faster rate. Product C has half the AUC of A but the same tmax: the same rate, half the extent. Reading both features from each curve is the whole skill.

## 13.4 Designing a Bioequivalence Study

A bioequivalence study compares a test product, usually a generic, with a reference product. It is needed because products once assumed to be pharmaceutical equivalents turned out not to give the same effect in patients. The Egyptian Drug Authority requires one for the registration of most generic products [6].

*The reference product.* The comparator is the innovator product whose efficacy and safety were established in clinical trials, called the reference listed drug. The test and reference must have the same dose, dosage form and route. The first edition states that the reference must contain the drug at a minimum of 5% of the product. No such rule exists. The real requirement concerns the batches. The assayed content of the reference batch should be close to its label claim. The test and reference batches should differ in content by no more than about 5% [5, 6].

*The design.* The standard design is a single-dose, randomised, two-period, two-sequence, two-treatment crossover in healthy volunteers, usually fasted overnight. In a **crossover design** each subject receives both products, in random order, in two periods. Each subject is thus his or her own control, which removes the large variation between subjects from the comparison.

| | Period 1 | Period 2 |
|---|---|---|
| Sequence 1 | Test | Reference |
| Sequence 2 | Reference | Test |

With three or more products the same idea extends to a Latin square, in which every subject receives every product once. A replicated crossover, in which each subject receives each product twice over four periods, estimates the within-subject variability of each product. That is useful for highly variable drugs.

*The washout.* The periods are separated by a **washout period** long enough for the pre-dose concentration in the next period to be negligible. ICH M13A asks for at least five terminal half-lives [5]. The Egyptian guideline asks for more than five half-lives, and at least seven days, with a pre-dose level below 5% of Cmax [6]. Ten half-lives, the figure in the first edition, is a safe practical choice, but it is not the rule.

*The subjects.* ICH M13A asks for healthy subjects aged 18 years or more, with a body mass index usually between 18.5 and 30 kg·m⁻² [5]. The Egyptian guideline gives 18–55 years and the same BMI range [6]. The first edition's 54–91 kg and 20–50 years is the historical FDA criterion, not the current one. Subjects give informed consent, take no other medication beforehand, and are assayed by a validated, sensitive method such as HPLC.

*Other designs.* A food-effect study repeats the crossover with a standard high-fat meal before the dose, because a meal changes gastric emptying and gut physiology the most. A multiple-dose study at steady state suits drugs taken chronically, such as anticonvulsants. Steady state is confirmed by three consecutive trough concentrations that agree. Its drug levels are higher and easier to assay, and it can reveal changes in metabolism that a single dose would not show, but it takes longer.

## 13.5 Deciding Bioequivalence

The first edition analyses the data with an analysis of variance and asks whether the products differ significantly at p < 0.05. That is the wrong question. A significance test asks whether a difference *exists*. A small, noisy study can then fail to detect a large difference and seem to pass, while a large, precise study can flag a trivial difference and fail. Bioequivalence asks a different question: is any difference small enough not to matter?

AUC and Cmax are first log-transformed. They are ratio-scale quantities that are roughly log-normally distributed, and on the log scale a ratio becomes a difference. The result is a **geometric mean ratio**, test over reference, with its confidence interval.

> **Key Equation:** Equation 13.3 — the bioequivalence criterion
>
> The 90% confidence interval of the test/reference geometric mean ratio, for log-transformed AUC and Cmax, must lie within 80.00–125.00%.
>
> For narrow-therapeutic-index drugs the range is narrowed to 90.00–111.11% in the Egyptian guideline. The narrowing is not applied to both endpoints alike: it is automatic for AUC, and it is extended to Cmax only where Cmax itself matters for safety, efficacy or monitoring. Where it is not extended, Cmax keeps 80.00–125.00%.

The limits look lopsided but are symmetric on the log scale: ln 0.80 = −0.223 and ln 1.25 = +0.223.

The interval is a 90% interval, not a 95% one, for a precise reason. The decision is made by **two one-sided tests**, each at α = 0.05. One tests that the ratio is not below 80%; the other, that it is not above 125%. Both must succeed. Passing both one-sided tests at 5% each is exactly equivalent to the 90% two-sided interval lying inside the limits [5]. The risk that a patient receives a product that is truly outside the limits is held at 5%.

> **Common Mistake:** Concluding that two products are bioequivalent because "the difference was not significant". Absence of evidence of a difference is not evidence of equivalence. Only the confidence interval, lying inside the limits, shows equivalence.

A difference in rate alone may still be acceptable. That is so when it is intended and labelled, as for a fast-acting or a modified-release product, or when it does not affect safety or efficacy.

## 13.6 When an In-Vivo Study Is or Is Not Needed

*When a study is required.* An in-vivo study is needed where there is evidence that products differ in effect, or that they are not bioequivalent. It is also needed for a narrow-therapeutic-index drug, or where non-equivalence would cause serious harm. Physicochemical warnings include aqueous solubility below 5 mg·mL⁻¹, slow dissolution (below 50% in 30 min) and a critical particle size. Poorly dissolving polymorphs or solvates, a high excipient-to-drug ratio, and excipients that affect absorption are others. Pharmacokinetic warnings include absorption from one localised site and poor absorption even from solution (F < 0.5). Extensive first-pass metabolism, rapid elimination, instability in part of the gut, and non-linear kinetics are others.

*When a study can be waived.* A **biowaiver** is the acceptance of bioequivalence without an in-vivo study. Bioavailability is self-evident for an intravenous solution. Inhaled gases and vapours qualify, as do oral solutions containing no excipient known to affect absorption.

Locally acting products are the case most often stated too broadly. There is no blanket waiver for topical or for gut-acting products. A waiver is available where the test and the comparator are *qualitatively and quantitatively the same simple solution* — for example two identical aqueous solutions applied to the skin — and there the argument is that the products are indistinguishable, not that equivalence needs no evidence. Anything else is decided product by product, and the evidence demanded may be in-vitro release, binding capacity, a pharmacodynamic endpoint, local or systemic pharmacokinetics, or a clinical endpoint study. Waiving a *systemic pharmacokinetic* study is not the same as waiving proof of equivalence.

*The BCS.* The **Biopharmaceutics Classification System** was proposed by Amidon and colleagues in 1995 [3]. It classifies a drug substance by its solubility and its intestinal permeability. With the dissolution of the product, these two properties govern absorption from an immediate-release oral dosage form. ICH M9 sets the definitions [4].

| Term | ICH M9 definition |
|---|---|
| Highly soluble | The highest single therapeutic dose dissolves completely in ≤ 250 mL of buffer at every pH from 1.2 to 6.8, at 37 ± 1 °C |
| Highly permeable | The extent of absorption in humans is ≥ 85%, from mass balance or absolute bioavailability |
| Very rapidly dissolving | ≥ 85% dissolves within 15 min, at pH 1.2, 4.5 and 6.8 |
| Rapidly dissolving | ≥ 85% dissolves within 30 min, at pH 1.2, 4.5 and 6.8 |

| Class | Solubility | Permeability | Limiting factor | Biowaiver under ICH M9 |
|---|---|---|---|---|
| 1 | High | High | Gastric emptying | Yes, if very rapidly dissolving, or rapidly dissolving with similar profiles |
| 2 | Low | High | Dissolution | No; an in-vivo study is required |
| 3 | High | Low | Permeability | Yes, if very rapidly dissolving, with excipients qualitatively the same and quantitatively very similar |
| 4 | Low | Low | Both | No |

The first edition has Classes 2 and 3 the wrong way round. Class 2 is the class whose absorption depends on the formulation, because its dissolution is the slow step, so it is the class that needs an in-vivo study. Class 3 drugs dissolve fast, and the membrane, not the formulation, limits them. For them the concern is excipients that might change permeability, which is why their excipients must match closely.

The Egyptian guideline adds one narrow national pathway that ICH M9 does not have [6]. A Class 2 drug that is a weak acid may receive a biowaiver if all four conditions hold:

1. its dose-to-solubility ratio is 250 mL or less at pH 6.8;
2. the generic dissolves rapidly, not less than 85% in 30 min at pH 6.8;
3. its dissolution profile is similar to the reference at pH 1.2, 4.5 and 6.8; and
4. its excipients, such as surfactants, have been critically evaluated in type and amount.

Every BCS biowaiver, whatever the class, is excluded for narrow-therapeutic-index drugs, non-linear drugs, modified-release products, and products absorbed in the mouth. It is also excluded where a rapid onset, and so tmax, is critical to the product's use.

> **Why It Matters in Practice:** A weak acid is poorly soluble in the stomach but dissolves readily at the pH of the small intestine, where it is absorbed. That is why the Egyptian pathway tests solubility at pH 6.8. Outside that pathway, a Class 2 drug needs an in-vivo study, and a pharmacist asked whether a Class 2 generic was waived should expect that it was not.

## Key Takeaways
- Pharmaceutical equivalents share the active ingredient, strength, dosage form including release type, and route.
- Products differing in dosage form or salt are pharmaceutical alternatives; IR and ER products are alternatives.
- F = (AUC/D)oral ÷ (AUC/D)IV, provided clearance is unchanged; relative bioavailability uses a reference product instead.
- F = fa × Fg × Fh, so a completely absorbed drug can have F far below 1.
- AUC measures extent; Cpmax and tmax measure rate.
- The standard bioequivalence study is a randomised two-period crossover with a washout of at least five half-lives.
- Bioequivalence: the 90% CI of the log-transformed geometric mean ratio of AUC and Cmax lies within 80.00–125.00%.
- The 90% interval is two one-sided tests at α = 0.05 each; equivalence, not significance, is the question.
- ICH M9 grants biowaivers to BCS Class 1 and Class 3; Class 2 needs an in-vivo study.
- The Egyptian guideline allows a Class 2 weak-acid biowaiver under four stated conditions.

## Check Your Understanding

**Q1.** [LO1] An immediate-release tablet and an extended-release tablet contain the same drug at the same strength. They are:
A) Pharmaceutical alternatives
B) Pharmaceutical equivalents
C) Therapeutic alternatives
D) Identical products

**Q2.** [LO2] A drug is completely absorbed from the gut (fa = 1), yet its absolute bioavailability is 0.3. The most likely reason is:
A) Slow dissolution of the tablet
B) An error, since F must equal fa
C) Rapid renal excretion
D) First-pass metabolism in the gut wall or the liver

**Q3.** [LO4] Two products are accepted as bioequivalent when:
A) The 90% confidence interval of the geometric mean ratio for AUC and Cmax lies within 80.00–125.00%
B) Their mean AUCs do not differ significantly at p < 0.05
C) Their tmax values are identical
D) The ratio of their mean AUCs is exactly 1.00

**Q4.** [LO2] An oral dose of 100 mg gives AUC = 30 mg·h·L⁻¹, and an IV dose of 50 mg gives AUC = 25 mg·h·L⁻¹. The absolute bioavailability is:
A) 0.30
B) 1.20
C) 0.60
D) 0.83

**Q5.** [LO5] Under ICH M9, BCS-based biowaivers may be granted to:
A) Class 2 and Class 4
B) Class 1 and Class 3
C) Class 1 only
D) All four classes

**Q6.** [LO3] The least sensitive and least reproducible way to assess bioavailability is:
A) Plasma concentration data
B) Urinary excretion data
C) Clinical response
D) In-vitro dissolution

**Q7.** [LO4] A 90% rather than a 95% confidence interval is used because:
A) Bioequivalence studies have few subjects
B) The limits are asymmetric
C) Regulators accept a 10% risk of error
D) It is equivalent to two one-sided tests, each at α = 0.05

**Q8.** [LO5] Under ICH M9 a drug is highly permeable when the extent of absorption in humans is:
A) At least 50%
B) At least 90%
C) At least 85%
D) 100%

**Q9.** [LO4] The washout period in a crossover bioequivalence study should be:
A) Exactly 24 hours
B) Long enough for pre-dose concentrations to be negligible, commonly at least five terminal half-lives
C) Equal to one dosing interval
D) Unnecessary if the subjects are healthy

**Q10.** [LO3] Products A and B have the same AUC, but A peaks at 2 h and B at 4 h. Therefore:
A) They have the same extent, and A has the faster rate
B) B has the faster rate of absorption
C) A has the greater extent of bioavailability
D) They cannot be compared without urine data

### Exercises

**E13.1** [LO2] A 100 mg IV dose of a drug gives Du∞ = 40 mg of unchanged drug in the urine. A 200 mg oral dose of a tablet in the same subject gives Du∞ = 60 mg. Calculate the absolute bioavailability, and state the conditions the urine method needs.

**E13.2** [LO4] In a crossover study the log-transformed AUC ratio, test minus reference, has mean 0.050 and standard error 0.040, with t = 1.717 for the one-sided 5% level. Calculate the geometric mean ratio and its 90% confidence interval, and decide bioequivalence under the standard limits and under the Egyptian narrow-therapeutic-index limits.

**E13.3** [LO5] Classify each immediate-release product and state whether a BCS biowaiver can apply under ICH M9 and under the Egyptian guideline. (a) The highest dose dissolves in 200 mL at pH 1.2–6.8, absorption is 95%, and the product dissolves 90% in 15 min. (b) A weak acid whose highest dose dissolves in 250 mL at pH 6.8 but not at pH 1.2; absorption is 95%; the product dissolves 88% in 30 min at pH 6.8 with profiles similar to the reference at pH 1.2, 4.5 and 6.8; it is not a narrow-therapeutic-index drug. (c) The highest dose dissolves in 150 mL at pH 1.2–6.8, absorption is 60%, and the product dissolves 80% in 15 min.

## Answers and Worked Solutions

**Q1. A** — The release type is part of the dosage form, so the two differ in dosage form. That makes them pharmaceutical alternatives.

**Q2. D** — F = fa × Fg × Fh. With fa = 1, the loss must lie in Fg or Fh, which is the first-pass effect. Option B confuses F with fa.

**Q3. A** — The criterion is an interval inside limits. Option B is a significance test, which answers a different question.

**Q4. C** — F = (30/100) ÷ (25/50) = 0.30 ÷ 0.50 = 0.60. Option A forgets to normalise the IV area by its dose.

**Q5. B** — Class 1 and Class 3 dissolve fast, so the formulation matters less. Class 2 is limited by dissolution, which the formulation controls.

**Q6. C** — Clinical response varies with receptor sensitivity, age, interactions and tolerance, none of which reflect absorption.

**Q7. D** — Two one-sided tests at 5% each correspond exactly to a two-sided 90% interval. The patient's risk is still held at 5%.

**Q8. C** — ICH M9 uses ≥ 85%. The first edition's 90% is an older FDA figure.

**Q9. B** — The aim is that the first period leaves nothing behind. The Egyptian guideline also sets a minimum of seven days.

**Q10. A** — Equal AUCs mean equal extent; the earlier tmax means the faster rate.

---

**E13.1 — worked solution**

*Step 1 — normalise each Du∞ by its dose.*

oral: 60 mg ÷ 200 mg = 0.30    IV: 40 mg ÷ 100 mg = 0.40

*Step 2 — absolute bioavailability.*

F = 0.30 ÷ 0.40 = 0.75

*Answer.* F = 0.75, or 75%.

*The conditions.* The drug must be excreted unchanged in the urine in significant amount, here 40% of an IV dose. Urine must be collected until excretion is complete, about 7–10 half-lives, on both occasions. The fraction of the drug *that reaches the systemic circulation* and is excreted unchanged must be the same on both occasions — that is, systemic disposition must be linear and independent of the route by which the drug arrived.

A large first-pass effect does not break that condition. First-pass loss is part of F, which is exactly what the method measures: the drug destroyed on the first pass never reaches the circulation and so never reaches the urine, and the ratio Du∞(oral)/Du∞(IV) falls in proportion. The method is in fact most useful for low-F drugs, where the difference between the routes is largest. What does break it is saturable or route-dependent disposition, or an incomplete collection.

**E13.2 — worked solution**

*Step 1 — the geometric mean ratio.*

GMR = e^0.050 = 1.051, or 105.1%

*Step 2 — the 90% interval on the log scale.*

0.050 ± 1.717 × 0.040 = 0.050 ± 0.0687, giving −0.0187 to 0.1187

*Step 3 — back-transform.*

e^(−0.0187) = 0.9815 and e^0.1187 = 1.1260, so the interval is 98.15% to 112.60%

*Step 4 — the decisions.* Under 80.00–125.00% the interval lies wholly inside, so the products are bioequivalent. Under 90.00–111.11% its upper end, 112.60%, lies outside, so they are not.

*Answer.* GMR = 105.1%, 90% CI 98.15–112.60%. Bioequivalent under the standard limits; not bioequivalent for a narrow-therapeutic-index drug.

*Check.* The point estimate lies at the centre of the interval on the log scale: (−0.0187 + 0.1187) ÷ 2 = 0.050, as it must.

**E13.3 — worked solution**

*(a)* Highly soluble (200 mL ≤ 250 mL across pH 1.2–6.8) and highly permeable (95% ≥ 85%): Class 1. It dissolves very rapidly (90% in 15 min). A biowaiver can apply under both ICH M9 and the Egyptian guideline, provided the excipients do not affect absorption.

*(b)* Not highly soluble across the whole range, but highly permeable: Class 2. ICH M9 gives no biowaiver, so an in-vivo study is required. Under the Egyptian guideline it meets the weak-acid pathway: the dose dissolves in 250 mL at pH 6.8, dissolution is ≥ 85% in 30 min at pH 6.8, and the profiles are similar at all three pH values. A biowaiver can apply once the excipients have been critically evaluated, provided tmax is not critical to its use.

*(c)* Highly soluble but only 60% absorbed: Class 3. A Class 3 biowaiver needs very rapid dissolution, ≥ 85% in 15 min. At 80% the product fails that condition, so an in-vivo study is required under both frameworks.

*The lesson.* The class of the drug substance is only the first question. The dissolution of the product, and for Class 3 its excipients, decide the rest.

## References
1. Shargel L, Yu ABC. *Applied Biopharmaceutics and Pharmacokinetics*. 8th ed. New York: McGraw Hill Medical; 2022.
2. Rowland M, Tozer TN. *Clinical Pharmacokinetics and Pharmacodynamics: Concepts and Applications*. 5th ed. Philadelphia: Wolters Kluwer; 2019.
3. Amidon GL, Lennernäs H, Shah VP, Crison JR. A theoretical basis for a biopharmaceutic drug classification: the correlation of in vitro drug product dissolution and in vivo bioavailability. *Pharm Res*. 1995;12(3):413–420. DOI: 10.1023/A:1016212804288
4. International Council for Harmonisation. *ICH Harmonised Guideline M9: Biopharmaceutics Classification System-Based Biowaivers*. Geneva: ICH; 2019.
5. International Council for Harmonisation. *ICH Harmonised Guideline M13A: Bioequivalence for Immediate-Release Solid Oral Dosage Forms*. Geneva: ICH; 2024.
6. Egyptian Drug Authority. *Egyptian Guideline for Conducting Bioequivalence Studies for Marketing Authorization of Generic Products* (EDREX: GL.CAPP.024), version 04/2026. Cairo: EDA; 2026.


---

# Chapter 14: Dissolution

## Learning Objectives
By the end of this chapter you will be able to:
1. [LO1] Explain why dissolution is tested, and how its purpose differs between quality control and development.
2. [LO2] Apply the Noyes–Whitney equation and state what the sink condition means.
3. [LO3] Describe the compendial dissolution apparatus and choose one for a given dosage form.
4. [LO4] Apply the staged acceptance criteria of the pharmacopoeia, and the two-stage test for enteric-coated products.
5. [LO5] Describe the alternative methods, the sources of variability, and what an in-vitro–in-vivo correlation is.

## 14.1 Why Dissolution Is Tested

**Dissolution** is the process by which a solid drug substance becomes dissolved in a solvent. Chapter 12 showed that a drug must dissolve before it can be absorbed, and that for a poorly soluble drug dissolution is often the rate-limiting step. A dissolution test measures that step outside the body. It is an official pharmacopoeial test of drug release from solid and semisolid dosage forms [1].

The same test serves two different purposes.

| | Quality control | Research and development |
|---|---|---|
| Focus | Batch-to-batch consistency | Prediction of in-vivo performance |
| Question asked | Was this batch made to specification? | How will this formulation behave in a patient? |
| Typical use | Batch release, stability testing, detecting manufacturing deviations | Choosing between candidate formulations, assessing risks |

In development, dissolution data help choose between candidate formulations. They help assess risks, especially for modified-release products: dose dumping, food effects, and interactions that change conditions in the gut. They support decisions when the manufacturing site, the process or the formulation changes, and can show whether a new bioavailability study is needed. Chapter 13 showed the strongest use of all: for BCS Class 1 and Class 3 drugs, similar dissolution can replace an in-vivo bioequivalence study.

Novel dosage forms make the test harder to design. Their physicochemical properties, and the environment in which they must release the drug, may have no counterpart in a standard vessel.

## 14.2 The Noyes–Whitney Equation

A dissolving particle is surrounded by a thin **stagnant layer** of solvent. At the surface of the solid the solution is saturated, at concentration Cs. In the bulk of the medium it is at C. Drug diffuses across the layer, from Cs down to C.

![A block labelled solid drug, surface area A, on the left. To its right a shaded band labelled stagnant layer, with a bracket beneath marking its thickness h. A concentration line starts high at the solid surface, labelled Cs saturated, falls in a straight line across the stagnant layer, and then runs flat through the region labelled bulk medium, well stirred, at the level labelled C bulk. An arrow inside the stagnant layer, labelled diffusion D, points from the solid towards the bulk.](../rework/figures/out/ch14-noyes-whitney.png)

*Figure 14.1 — The picture behind the Noyes–Whitney equation. The solution is saturated (Cs) at the surface of the solid and falls across a stagnant layer of thickness h to the bulk concentration C. The rate of dissolution is proportional to the surface area and to the gradient across the layer.*  
Original diagram, drawn for the first edition page 102 (original)

> **Key Equation:** Equation 14.1 — the Noyes–Whitney equation
>
> $$\frac{dm}{dt} = \frac{D A}{h}\left(C_s - C\right) \qquad \text{and so} \qquad \frac{dC}{dt} = \frac{D A}{h V}\left(C_s - C\right)$$
>
> D is the diffusion coefficient of the drug, A the surface area of the dissolving solid, h the thickness of the stagnant layer, Cs the solubility of the drug, C its concentration in the bulk medium, V the volume of that medium, and m the mass dissolved.

The **Noyes–Whitney equation** names every lever a formulator has. The rate rises with the surface area, which is why micronisation works (Chapter 12). It rises with the solubility, which is why a salt or a buffering excipient can help. It falls as the stagnant layer thickens, which is why agitation matters. And it falls as the bulk concentration climbs towards Cs, because the driving gradient shrinks.

> **Watch the Units:** D·A·(Cs − C)/h has units of cm²·s⁻¹ × cm² × mg·cm⁻³ ÷ cm = mg·s⁻¹ — a *mass* per time, not a concentration per time. This is why Equation 14.1 is written as dm/dt first. The first edition, like many texts, prints the same right-hand side labelled dC/dt, which is dimensionally impossible; the V is there, silently absorbed into the constant. Check which form a text is using before you compare its numbers with yours.

The **sink condition** is the state in which the bulk concentration stays far below the solubility, C ≪ Cs. Then Cs − C ≈ Cs, and the equation simplifies:

dm/dt ≈ (D · A / h) · Cs    and    dC/dt ≈ (D · A) / (h · V) · Cs

The rate is now set by the drug and the product alone, not by how much has already dissolved. That is the condition a dissolution test tries to maintain, and inside the body it is maintained naturally, because absorption keeps removing dissolved drug. A test that loses sink conditions slows itself down artificially and underestimates the release that would occur in a patient.

## 14.3 Test Conditions and the Compendial Apparatus

Five conditions must be fixed in every method.

*The vessel.* Dissolution vessels range from millilitres to several litres.

*The volume of medium.* Usually 500–1000 mL. A poorly soluble drug may need up to 2000 mL to keep sink conditions.

*The agitation.* The speed of the basket or paddle sets the hydrodynamics, and so the thickness h of the stagnant layer. Too low a speed gives poorly reproducible hydrodynamics; too high a speed gives turbulence.

*The temperature.* Most tests run at 37 °C, body temperature. Transdermal products are tested at 32 °C, the temperature of the skin surface.

*The medium.* Water, or aqueous buffers at pH values that simulate the gut.

The pharmacopoeia describes seven apparatus, but not all in one place. Apparatus 1 to 4 — basket, paddle, reciprocating cylinder and flow-through cell — are the dissolution apparatus of USP General Chapter <711> [2]. Apparatus 5 to 7 — paddle over disc, rotating cylinder and reciprocating holder — are drug-release apparatus for transdermal and other modified-release dosage forms, and they belong to General Chapter <724> [3]. The monograph for each product specifies which one to use.

| Apparatus | Name | Main use |
|---|---|---|
| 1 | Rotating basket | Capsules, and dosage forms that float or disintegrate slowly |
| 2 | Paddle | Tablets, capsules, modified-release products, suspensions |
| 3 | Reciprocating cylinder | Extended-release products, especially bead-type |
| 4 | Flow-through cell | Modified-release products of poorly soluble drugs |
| 5 | Paddle over disk | Transdermal products |
| 6 | Rotating cylinder | Transdermal products |
| 7 | Reciprocating holder | Extended-release products |
| Not official | Rotating bottle | Controlled-release beads |
| Not official | Franz diffusion cell | Ointments, creams, transdermal products |

*Apparatus 1, the basket.* A cylindrical basket on a motor shaft holds the sample and rotates in a round-bottomed vessel immersed in a bath at 37 °C. The usual speed is 100 rpm. It suits capsules and products that float. It is sensitive to clogging of the mesh by gummy materials, which can create a local loss of sink.

*Apparatus 2, the paddle.* A coated paddle, attached vertically to a variable-speed motor, stirs the medium in a round-bottomed vessel at 37 °C. The usual speeds are 50 rpm for solid oral dosage forms and 25 rpm for suspensions. It is the usual choice for tablets. It is very sensitive to tilting and to the centring of the paddle. A sinker, such as a few turns of wire, stops a capsule floating and keeps a sticky film-coated tablet under the paddle.

*Apparatus 3, the reciprocating cylinder.* Glass cylinders move up and down inside flat-bottomed vessels. Six units are tested at 37 °C. It suits extended-release beads, and allows the medium to be changed from one pH to another.

*Apparatus 4, the flow-through cell.* A pump forces fresh or recirculated medium through a cell that holds the sample in a fixed position. A pulseless pump gives laminar flow. The standard flow rates are 4, 8 and 16 mL·min⁻¹ [2]. It is valuable for poorly soluble drugs. In the open configuration fresh medium passes once, so the rate of dissolution at any moment can be measured directly, sink conditions are easy to keep, a large total volume can be used, and operation is easily automated.

*Apparatus 5 and 6, for transdermal products.* In the paddle-over-disk method the patch is held in a disk assembly at the bottom of the vessel, under the paddle. In the rotating-cylinder method, a modification of the basket, the patch is mounted on a stainless steel cylinder. Both run at 32 °C, and samples are drawn midway between the surface of the medium and the top of the paddle or cylinder.

Calibrator tablets have been used to verify apparatus performance: disintegrating prednisone tablets for disintegrating products, and non-disintegrating salicylic acid tablets for non-disintegrating products. Buccal and sublingual tablets are tested by the procedure for uncoated tablets.

## 14.4 Meeting the Requirements

The result is expressed as the amount dissolved in a stated time, as a percentage of the label content. The specification sets a value Q. For many immediate-release products Q is 75% in 45 min; others require 85% in 30 min, or 75% in 60 min. Testing proceeds in up to three stages, and stops as soon as a stage is passed [2].

> **Key Equation:** Equation 14.2 — the staged acceptance criteria
>
> | Stage | Units tested | Criterion |
> |---|---|---|
> | S1 | 6 | Every unit ≥ Q + 5% |
> | S2 | 6 more (12 in all) | Average of 12 ≥ Q, and no unit < Q − 15% |
> | S3 | 12 more (24 in all) | Average of 24 ≥ Q, not more than 2 units < Q − 15%, and no unit < Q − 25% |

The stages get more lenient on individual units but always demand that the average reach Q. The first stage is strict on every unit because it rests on only six.

*Enteric-coated products.* These are tested in the apparatus named in the monograph, usually Apparatus 1 or 2, in two phases. The acid phase uses 0.1 N HCl for 2 h; the buffer phase follows at pH 6.8, usually for 45 min, and a specified percentage must then be released. The test mirrors the product's purpose: to survive the stomach and release in the intestine.

The acid phase is staged like the dissolution test itself. At A1, each of 6 units must release less than 10%. If that fails, A2 tests 12 units: their *average* must be no more than 10% and no single unit may exceed 25%. If that fails, A3 tests 24: the average must be no more than 10% and no unit may exceed 25%. The 10% figure alone is therefore the A1 rule, not a universal ceiling for every unit.

> **Worked Example:** Example 14.1 — a batch through the stages
>
> The specification is Q = 75% in 45 min. The results are illustrative.
>
> Stage 1, six units: 82, 79, 85, 77, 88 and 81%.
>
> Stage 2, six more units: 78, 84, 76, 80, 83 and 79%.
>
> Decide whether the batch passes, and at which stage.
>
> *Step 1 — the S1 limit.* Every unit must be at least Q + 5% = 80%.
>
> *Step 2 — test S1.* Two units, 79% and 77%, are below 80%. S1 fails, so six more units are tested.
>
> *Step 3 — the S2 limits.* The average of all 12 must be at least Q = 75%, and no unit may be below Q − 15% = 60%.
>
> *Step 4 — the average of 12.*
>
> S1 sum = 82 + 79 + 85 + 77 + 88 + 81 = 492
>
> S2 sum = 78 + 84 + 76 + 80 + 83 + 79 = 480
>
> average = (492 + 480) ÷ 12 = 972 ÷ 12 = 81.0%
>
> *Step 5 — the lowest unit.* The lowest of the 12 is 76%, well above 60%.
>
> *Answer.* The batch fails S1 but passes S2, with an average of 81.0% and no unit below 60%. Stage 3 is not needed.
>
> *Check.* The S1 failure did not depend on the average. The six S1 units average 82.0%, comfortably above both Q and Q + 5%, and still fail, because S1 judges each unit. Averaging S1 and concluding that it passed is the commonest error in applying the table.

## 14.5 Other Methods, Variability and IVIVC

*The rotating bottle.* Bottles holding controlled-release beads are capped and rotated in a bath at 37 °C. At set times the contents are decanted through a 40-mesh screen, the residue is assayed, and fresh medium is added. The medium can be changed to simulate passage through the gut. One recommended sequence is pH 1.2 and then pH 2.5, for 1 h each; pH 4.5 and then pH 7, for 1.5 h each; and pH 7.5 for 2 h. The method is manual and tedious.

*Intrinsic dissolution.* **Intrinsic dissolution** measures the dissolution of the pure drug from a constant surface area, without excipients. It is expressed in mg·cm⁻²·min⁻¹ and is used to screen new drug substances. Holding A constant turns Equation 14.1 into a direct measure of the drug's own dissolution properties.

*Diffusion cells.* The **Franz diffusion cell** is a static system for studying drug permeation through a skin model. Human cadaver skin or animal skin, such as hairless mouse skin, is mounted between a donor chamber and a receptor fluid, which is sampled over time. It is used to compare release and skin permeation between candidate topical and transdermal formulations.

*Variability.* Results from the same equipment and procedure can differ by 25% or more. The usual causes are these:

| Cause | Effect |
|---|---|
| Paddle not centred or vessel tilted | Changed hydrodynamics |
| Turbulence | Increased agitation and faster dissolution |
| Clogging of the basket mesh | Local loss of sink conditions |
| Dissolved gas forming bubbles on the unit | Reduced wetted surface in basket and paddle methods |
| Low-density or floating units | Poor wetting; needs a sinker |

This is why the medium is degassed and the apparatus calibrated and aligned before use.

*In-vitro–in-vivo correlation.* An **in-vitro–in-vivo correlation** (IVIVC) is a relationship between a physicochemical property of the product, such as its dissolution rate, and a biological property, such as the plasma concentration or the rate of absorption. For a correlation to exist, some aspect of release in vitro must relate to performance in vivo. A useful IVIVC must also stay predictive across a range of release rates and manufacturing changes. The in-vitro result depends on the drug substance, the formulation, the hydrodynamics of the apparatus and the medium. It is therefore a designed quantity, not a fixed property of the drug [3].

> **Why It Matters in Practice:** An established IVIVC lets a manufacturer justify a change of site or process from dissolution data alone. Without one, the same change may need a new bioequivalence study. Chapter 13 described that study. A good dissolution method is the cheaper way to answer the same question.

## Key Takeaways
- Dissolution testing checks batch consistency in quality control and predicts in-vivo behaviour in development.
- Noyes–Whitney: dm/dt = (D·A/h)(Cs − C) is a mass rate; divide by the medium volume V for dC/dt.
- Under sink conditions, C ≪ Cs, the rate reduces to (D·A/h)·Cs.
- Most tests run at 37 °C; transdermal tests at 32 °C.
- The basket usually runs at 100 rpm; the paddle at 50 rpm for tablets and 25 rpm for suspensions.
- Apparatus 4 flow rates are 4, 8 and 16 mL·min⁻¹.
- S1: every unit ≥ Q + 5%. S2: average of 12 ≥ Q, none < Q − 15%. S3: average of 24 ≥ Q, at most 2 < Q − 15%, none < Q − 25%.
- Enteric-coated products: 2 h in 0.1 N HCl (A1: each of 6 below 10%; A2/A3: average ≤ 10%, no unit above 25%), then pH 6.8 buffer.
- IVIVC links an in-vitro release property to an in-vivo one.

## Check Your Understanding

**Q1.** [LO2] According to the Noyes–Whitney equation, the dissolution rate increases when:
A) The stagnant layer becomes thicker
B) The solubility of the drug falls
C) The bulk concentration approaches Cs
D) The surface area of the solid increases

**Q2.** [LO3] The standard flow rates for the flow-through cell, Apparatus 4, are:
A) 1, 2 and 4 mL·min⁻¹
B) 10 to 100 mL·min⁻¹
C) 50 and 100 mL·min⁻¹
D) 4, 8 and 16 mL·min⁻¹

**Q3.** [LO4] The criterion at stage S1 of the dissolution test is:
A) Each of six units is not less than Q + 5%
B) The average of six units is not less than Q
C) No unit is below Q − 15%
D) The average of 12 units is not less than Q

**Q4.** [LO3] Dissolution tests on transdermal products are run at:
A) 25 °C
B) 37 °C
C) 32 °C
D) 40 °C

**Q5.** [LO2] The sink condition means that:
A) The drug has completely dissolved
B) The bulk concentration stays far below the solubility, so the rate is set by Cs
C) The medium is at 37 °C
D) The stagnant layer has zero thickness

**Q6.** [LO1] In quality control, the main purpose of dissolution testing is:
A) To confirm batch-to-batch consistency and detect manufacturing deviations
B) To choose between candidate formulations
C) To predict the plasma curve in patients
D) To replace the assay of drug content

**Q7.** [LO3] The usual paddle speed for a solid oral dosage form is:
A) 25 rpm
B) 100 rpm
C) 150 rpm
D) 50 rpm

**Q8.** [LO4] The acid phase for an enteric-coated product is:
A) 2 h in 0.1 N HCl, with less than 10% released from each of the six units at the first stage
B) 45 min at pH 6.8
C) 1 h in water
D) 2 h in 0.1 N HCl, with at least 75% released

**Q9.** [LO5] Intrinsic dissolution is expressed in:
A) mg·min⁻¹
B) mg·cm⁻²·min⁻¹
C) % per minute
D) mL·min⁻¹

**Q10.** [LO5] An in-vitro–in-vivo correlation is:
A) A test of drug content uniformity
B) The comparison of two apparatus
C) A relationship between an in-vitro release property and an in-vivo property of the product
D) A requirement for all immediate-release products

### Exercises

**E14.1** [LO2] A drug has D = 5 × 10⁻⁶ cm²·s⁻¹ and Cs = 1.0 mg·mL⁻¹. A compact of surface area 2.0 cm² dissolves in 900 mL of medium with a stagnant layer 50 µm thick. Assuming sink conditions, calculate the dissolution rate in mg·h⁻¹ and the rate of rise of the bulk concentration. Check that sink conditions still hold after 1 h, and state the effect of halving the particle diameter at constant mass.

**E14.2** [LO4] A product with Q = 75% has reached stage S3. The 24 units average 77%. Two units dissolved 58% and 59%, and all others are above 60%. Decide whether the batch passes. Then decide again if a third unit had dissolved 57%.

**E14.3** [LO3] A poorly soluble drug, Cs = 0.5 mg·mL⁻¹, is tested in an open flow-through cell at 16 mL·min⁻¹. A 10 min fraction contains 2.4 mg of drug. Calculate the dissolution rate and the concentration leaving the cell, and decide whether sink conditions hold. Repeat the concentration at 4 mL·min⁻¹, assuming the same dissolution rate.

## Answers and Worked Solutions

**Q1. D** — A appears in the numerator, so a larger area gives a faster rate. Option A, C and D all reduce the rate.

**Q2. D** — The pharmacopoeia specifies 4, 8 and 16 mL·min⁻¹. Option B repeats a range given in the first edition, which is not the official one.

**Q3. A** — S1 judges every one of the six units against Q + 5%. The averages belong to S2 and S3.

**Q4. C** — Transdermal products are tested at 32 °C, the temperature of the skin surface, not of the body core.

**Q5. B** — Under sink conditions Cs − C ≈ Cs, so the rate no longer depends on how much has already dissolved.

**Q6. A** — Quality control asks whether the batch was made to specification. Prediction and formulation choice belong to development.

**Q7. D** — 50 rpm is usual for tablets and capsules; 25 rpm is used for suspensions, and 100 rpm is the usual basket speed.

**Q8. A** — The acid phase checks that the coat survives the stomach, and at A1 the limit applies to each of the six units. Option B describes the buffer phase that follows. Note that the per-unit 10% limit is the A1 criterion; at A2 and A3 the average must be ≤ 10% with no unit above 25%.

**Q9. B** — Intrinsic dissolution is normalised to a constant surface area, so it carries area in its units.

**Q10. C** — An IVIVC links a physicochemical property of the product in vitro to a biological one in vivo.

---

**E14.1 — worked solution**

*Step 1 — convert h.* 50 µm = 50 × 10⁻⁴ cm = 5.0 × 10⁻³ cm. Cs = 1.0 mg·mL⁻¹ = 1.0 mg·cm⁻³.

*Step 2 — the mass rate under sink conditions.*

dm/dt = D · A · Cs / h = (5 × 10⁻⁶ cm²·s⁻¹ × 2.0 cm² × 1.0 mg·cm⁻³) ÷ 5.0 × 10⁻³ cm = 2.0 × 10⁻³ mg·s⁻¹

In hours: 2.0 × 10⁻³ mg·s⁻¹ × 3600 s·h⁻¹ = 7.2 mg·h⁻¹

*Step 3 — the rate of rise of concentration.* Divide by the volume.

dC/dt = 7.2 mg·h⁻¹ ÷ 900 mL = 0.0080 mg·mL⁻¹·h⁻¹

*Step 4 — sink after 1 h.* C ≈ 0.0080 mg·mL⁻¹, which is 0.8% of Cs. Sink conditions hold comfortably.

*Step 5 — halving the diameter.* At constant mass, halving the diameter of the particles doubles their total surface area. The rate doubles, to 14.4 mg·h⁻¹, provided the particles wet properly (Chapter 12).

*Answer.* 7.2 mg·h⁻¹, a concentration rise of 0.0080 mg·mL⁻¹·h⁻¹, still under sink conditions after 1 h; halving the diameter doubles the rate.

**E14.2 — worked solution**

*Step 1 — the S3 limits.* Average of 24 ≥ Q = 75%. Not more than two units below Q − 15% = 60%. No unit below Q − 25% = 50%.

*Step 2 — the first case.* The average is 77%, which passes. Exactly two units, 58% and 59%, are below 60%, which is the maximum allowed. None is below 50%. The batch passes.

*Step 3 — the second case.* Three units are now below 60%, one more than allowed. The batch fails, even though no unit is below 50% and the average may still exceed 75%.

*Answer.* The batch passes in the first case and fails in the second.

**E14.3 — worked solution**

*Step 1 — the dissolution rate.* In an open cell each fraction holds the drug dissolved during its collection time.

rate = 2.4 mg ÷ 10 min = 0.24 mg·min⁻¹

*Step 2 — the concentration at 16 mL·min⁻¹.* The fraction volume is 16 mL·min⁻¹ × 10 min = 160 mL.

C = 2.4 mg ÷ 160 mL = 0.015 mg·mL⁻¹, which is 3% of Cs

*Step 3 — the concentration at 4 mL·min⁻¹.* The same 2.4 mg now leaves in 40 mL.

C = 2.4 mg ÷ 40 mL = 0.060 mg·mL⁻¹, which is 12% of Cs

*Answer.* The dissolution rate is 0.24 mg·min⁻¹. The outflow concentration is 3% of Cs at 16 mL·min⁻¹ and 12% at 4 mL·min⁻¹.

*Interpretation.* At 16 mL·min⁻¹ sink conditions clearly hold. At 4 mL·min⁻¹ the medium is four times richer in drug, the driving gradient falls by about a tenth, and the measured rate would begin to underestimate the true one. This is why the flow rate is a controlled variable, restricted to the three official values.

## References
1. Shargel L, Yu ABC. *Applied Biopharmaceutics and Pharmacokinetics*. 8th ed. New York: McGraw Hill Medical; 2022.
2. United States Pharmacopeial Convention. General Chapter <711> Dissolution. In: *United States Pharmacopeia and National Formulary (USP–NF)*. Rockville, MD: USP; current edition.

3. United States Pharmacopeial Convention. General Chapter <724> Drug Release. In: *United States Pharmacopeia and National Formulary (USP–NF)*. Rockville, MD: USP; current edition.
3. Aulton ME, Taylor KMG, editors. *Aulton's Pharmaceutics: The Design and Manufacture of Medicines*. 6th ed. Edinburgh: Elsevier; 2021.


---

# Glossary

**Absolute bioavailability** — F. The fraction of an extravascular dose that reaches the systemic circulation, found by comparing its dose-normalised AUC (or Du∞) with that of an intravenous dose, provided clearance is unchanged.

**absorption** — The movement of drug from the site of administration into the systemic circulation. The first process of ADME, and the only one a dosage form can be designed to control.

**absorption rate constant** — Ka. The first-order rate constant governing transfer of drug from solution in the gut into the systemic circulation, in reciprocal time.

**accumulation half-life** — t½,acc. The time taken to reach half of the steady-state level on a multiple dose regimen, t½·[1 + 3.32·log(Ka/(Ka − K))] for Ka > K. For repeated intravenous doses it equals the elimination half-life.

**accumulation index** — R. The ratio of the steady-state peak to the peak after the first dose, 1/(1 − e^(−Kτ)). It depends on K and the dosage interval, not on the dose; R = 1 means no accumulation.

**active metabolite** — A metabolite with pharmacological activity of its own that contributes to the response, such as norfluoxetine from fluoxetine or desipramine from imipramine.

**Active transport** — Carrier-mediated movement of drug across a membrane against its concentration gradient, using energy from ATP. It is saturable and shows competition between similar molecules; glucose and galactose are carried this way by SGLT1.

**Active tubular secretion** — Carrier-mediated transport of drug from blood into the tubular fluid, against its concentration gradient, requiring energy. The kidney has separate carriers for weak acids and weak bases, and drugs sharing a carrier compete.

**amount remaining to be excreted** — ARE. The quantity (Du∞ − Du): the amount of drug still to appear unchanged in the urine at time t. Its logarithm falls linearly with time, which is the basis of the sigma-minus method.

**apparent volume of distribution** — Vd. The proportionality constant linking the amount of drug in the body to the plasma concentration, Vd = D_B / Cp. It is the volume the drug would occupy if it were present throughout at the plasma concentration, and it need not correspond to any real body volume.

**AUC** — Area under the plasma concentration–time curve, in concentration × time units (for example µg·h·mL⁻¹). It is proportional to the total amount of drug reaching the systemic circulation, and so measures the *extent* of absorption.

**AUMC** — Area under the first moment curve: the area under a plot of Cp·t against t, in concentration × time² units. Divided by AUC it gives the mean residence time.

**average steady-state concentration** — Css,av. The constant concentration giving the same area as the real curve over one steady-state dosing interval, F·D₀/(Cl·τ). It lies below the arithmetic mean of the peak and the trough.

**Bioavailability** — The rate and the extent of absorption of a drug from its dosage form into the systemic circulation. Both parts are required: two products with the same AUC can differ in tmax and behave differently in a patient.

**bioequivalent** — Describing pharmaceutical equivalents or alternatives that give the same rate and extent of absorption under the same conditions, judged by the 90% confidence interval of the geometric mean ratio of AUC and Cmax.

**Biopharmaceutics** — The study of how the physicochemical properties of the drug, the dosage form and the route of administration control the rate and extent of drug absorption.

**Biopharmaceutics Classification System** — BCS. The scheme of Amidon and colleagues (1995) that classifies drug substances by aqueous solubility and intestinal permeability into Classes 1–4. Under ICH M9 it supports biowaivers for Classes 1 and 3.

**biowaiver** — Acceptance of bioequivalence without an in-vivo study, for example on the basis of the BCS class of the drug and the dissolution of the product.

**brush border** — The luminal surface of the intestinal epithelial cells, covered with microvilli that resemble the bristles of a brush. Its embedded enzymes, including peptidases and disaccharidases, are brush-border enzymes.

**central compartment** — In a compartmental model, the blood together with the highly perfused organs (heart, lung, liver, kidney), treated as one well-mixed kinetic space. Elimination is assumed to occur from here.

**compartmental** — Describing a model that represents the body as one or more kinetic spaces rather than as anatomical organs. Contrast with non-compartmental analysis, which uses statistical moments instead.

**Cpmax** — The peak plasma concentration reached after a dose. It depends on the dose, on the absorption rate constant Ka and on the elimination rate constant K, so it reflects both the rate and the extent of absorption.

**crossover design** — A study design in which each subject receives every product, in randomised order and in separate periods, so that each subject serves as his or her own control.

**Crystal polymorphism** — The ability of a drug to crystallise in more than one arrangement. Polymorphs share a chemical structure but differ in solubility, stability and compressibility, so they can differ in bioavailability.

**cumulative amount excreted unchanged** — Du. The running total of intact drug recovered in the urine up to time t. Its limiting value at infinite time is Du∞.

**cytochrome P450** — The family of haem-containing isoenzymes that performs most Phase I oxidations. Named from the 450 nm absorption of its carbon monoxide complex.

**Dissolution** — The process by which a solid drug substance becomes dissolved in a solvent; also the pharmacopoeial test that measures drug release from a solid or semisolid dosage form.

**distribution** — The reversible transfer of drug from the systemic circulation into and out of the tissues. The second process of ADME.

**distribution phase** — The early, steeply falling part of a biexponential plasma curve, during which drug is moving from the central compartment into the peripheral compartment faster than it is being eliminated.

**dosage interval** — τ. The time from one dose to the next in a multiple dose regimen. With the dose size, it is one of the two quantities a prescriber controls.

**elimination** — The irreversible loss of drug from the body, by excretion, by metabolism, or by both.

**elimination half-life** — t½. The time taken for the amount of drug in the body, or its plasma concentration, to fall by half. For a first-order process t½ = 0.693/K and is independent of the dose.

**elimination phase** — The later, shallower part of a biexponential plasma curve, reached once distribution has equilibrated, whose slope gives the terminal rate constant.

**elimination rate constant** — K. The first-order rate constant governing loss of drug from the body, in reciprocal time. It is the product of clearance and the reciprocal of Vd: K = Cl/Vd.

**elimination-rate-limited** — Describes a metabolite eliminated more slowly than it is formed (Kmet < K). Its terminal decline reflects its own elimination, so its half-life can be read from its curve.

**excipient** — Any non-drug component of a formulation, such as a diluent, binder, lubricant, coating or surfactant. Excipients can raise or lower bioavailability.

**Facilitated diffusion** — Carrier-mediated movement of drug down its concentration gradient, without energy. It is saturable and competitive; fructose is absorbed this way.

**first order** — Describing a process whose rate is proportional to the amount or concentration of drug driving it. A constant *fraction* is lost per unit time, so the plot of log concentration against time is a straight line. Contrast zero order, where a constant *amount* is lost per unit time.

**First-order absorption** — Absorption at a rate proportional to the amount of drug still in solution at the absorption site, so that a constant *fraction* is absorbed per unit time. Typical of rapidly dissolving forms such as immediate-release tablets and capsules.

**first-pass effect** — Loss of an oral dose to metabolism in the gut wall or the liver before it reaches the systemic circulation. It makes F smaller than the fraction absorbed: F = fa × Fg × Fh.

**Flip-flop** — The situation in which the elimination rate constant exceeds the absorption rate constant, so that the terminal phase of an oral curve reflects absorption rather than elimination and the two constants are assigned the wrong way round. Only intravenous data can resolve it.

**formation-rate-limited** — Describes a metabolite eliminated faster than it is formed (Kmet > K). It declines in parallel with the parent, and its own half-life cannot be read from its curve.

**fraction unabsorbed** — 1 − Ab/Ab∞, the proportion of the ultimately absorbed dose that has not yet been absorbed at time t. Plotted against time it is linear on semilogarithmic axes for first-order absorption and on ordinary axes for zero-order absorption.

**Franz diffusion cell** — A static diffusion cell in which a skin membrane separates a donor chamber from a sampled receptor fluid, used to compare drug release and skin permeation of topical and transdermal formulations.

**genetic polymorphism** — A gene variant common in a population. In drug-metabolising enzymes such as NAT2, CYP2D6 and CYP2C19 it makes individuals slow, normal or rapid metabolisers; it is a property of the individual's genotype.

**geometric mean ratio** — The ratio of the geometric means of a pharmacokinetic measure, such as AUC, for test and reference products, obtained by back-transforming the mean difference of the log-transformed values.

**Glomerular filtration** — Passive movement of free drug from blood into the glomerular filtrate, with the concentration gradient. Protein-bound drug is not filtered, because the complex is too large to cross.

**glomerular filtration rate** — GFR. The volume of plasma filtered at the glomerulus per unit time, normally 125–130 mL·min⁻¹. It is measured as the clearance of a substance that is filtered but neither secreted nor reabsorbed, such as inulin or creatinine.

**Henderson–Hasselbalch equation** — The relation between pH, pKa and the ratio of ionised to unionised drug: for a weak acid pKa − pH = log([U]/[I]), for a weak base pKa − pH = log([I]/[U]).

**hybrid rate constants** — a and b, the two exponents of a biexponential plasma curve. Neither is a single physical process: each combines K, K₁₂ and K₂₁, subject to a + b = K + K₁₂ + K₂₁ and a·b = K·K₂₁. Always a > b.

**in-vitro–in-vivo correlation** — IVIVC. A predictive relationship between an in-vitro property of a product, such as its dissolution rate, and an in-vivo property, such as plasma concentration or absorption rate.

**interdigestive migrating myoelectric complex** — IMMC. The cycle of gastrointestinal motor activity, every 1.5–2 h in the fasting state, whose phase 3 (the housekeeper wave) opens the pylorus and clears indigestible solids.

**Intrinsic dissolution** — The dissolution rate of a pure drug substance from a constant surface area, without excipients, expressed in mg·cm⁻²·min⁻¹.

**ion pair** — A neutral complex formed between a charged drug and an endogenous organic ion of opposite charge. It can partition into the membrane and diffuse across, the proposed route for quaternary ammonium compounds.

**Ka** — The absorption rate constant. See [[absorption-rate-constant]].

**Ke** — The renal excretion rate constant: the first-order constant governing loss of intact drug into the urine. See [[renal-excretion-rate-constant]].

**Km** — The Michaelis–Menten constant: the drug concentration at which a saturable process runs at half its maximum rate. It is a concentration, not a rate constant, and reflects the affinity of the drug for the enzyme.

**Knr** — The non-renal elimination rate constant: the first-order constant covering every route of loss other than renal excretion of intact drug, chiefly metabolism. K = Ke + Knr.

**K₁₂** — The first-order rate constant for transfer of drug from the central compartment to the peripheral (tissue) compartment.

**K₂₁** — The first-order rate constant for transfer of drug from the peripheral (tissue) compartment back to the central compartment.

**Lag time** — t₀. The delay between administration and the start of absorption, caused by slow gastric emptying, reduced motility or any other factor that stops absorption beginning at once. It is shorter than the onset of action.

**linear pharmacokinetics** — Dose-independent kinetics: concentrations and AUC change in proportion to the dose, and K, Vd and t½ do not depend on the dose.

**loading dose** — Dₗ. An intravenous bolus given at the start of an infusion, sized as Css · Vd (equivalently R/K) so that the target concentration is reached immediately instead of over about five half-lives.

**mean absorption time** — MAT. The average time absorbed molecules spend at the absorption site before reaching the systemic circulation, MTT(oral) − MRT(IV). For first order absorption it equals 1/Ka.

**Mean residence time** — MRT. The average time the molecules of a dose spend in the body after an instantaneous (IV) dose, AUMC/AUC. For a one-compartment drug it equals 1/K.

**mean transit time** — MTT. The mean residence time measured after a non-instantaneous input such as an oral dose; it includes the time spent at the absorption site.

**metabolism** — The enzymatic conversion of drug into one or more chemically different metabolites. Part of elimination, and the subject of Chapter 11.

**method of residuals** — Also feathering or stripping. A graphical method that separates two exponential processes by fitting the slower one to the terminal data, extrapolating it back, and subtracting it from the earlier points. Used for distribution in Chapter 4 and for absorption in Chapter 7.

**Michaelis–Menten equation** — V = Vmax·C/(Km + C). The rate law of a saturable enzyme or carrier process; first order when C ≪ Km and zero order when C ≫ Km.

**Micronisation** — Reduction of particle size, usually by milling, to raise surface area and dissolution rate. It improves the absorption of drugs such as griseofulvin, but can slow dissolution of hydrophobic drugs that resist wetting.

**midpoint time** — The time halfway through a urine collection interval. An excretion rate calculated as ΔDu/Δt is an average over the interval, so it is plotted against the midpoint rather than the end.

**minimum effective concentration** — MEC. The plasma concentration below which the drug produces no therapeutic effect. The lower boundary of the therapeutic range.

**minimum toxic concentration** — MTC. The plasma concentration above which the drug produces toxic effects. The upper boundary of the therapeutic range.

**Non-compartmental analysis** — Estimation of pharmacokinetic parameters from the areas under the plasma curve (statistical moments) without fitting any compartmental model. It requires only linear kinetics.

**non-linear pharmacokinetics** — Dose-dependent kinetics: concentrations change out of proportion to the dose, and parameters such as t½ and clearance vary with it. Usually caused by a saturable enzyme or carrier.

**non-renal elimination rate constant** — Knr. The part of the total elimination rate constant that does not represent renal excretion of intact drug, chiefly metabolism.

**Noyes–Whitney equation** — dC/dt = (D·A/h)(Cs − C): the dissolution rate is proportional to the surface area and to the concentration gradient across the stagnant layer. Taken literally D·A(Cs − C)/h is a mass rate, and dividing by the medium volume gives dC/dt.

**P-glycoprotein** — P-gp. An efflux transporter in the intestinal brush border that pumps many lipophilic and cytotoxic drugs back into the gut lumen, reducing their absorption. Inhibiting it increases their absorption.

**paracellular** — Describing passage between epithelial cells, through the tight junctions. It suits small polar molecules such as water, urea and some ions.

**Passive diffusion** — Movement of drug through the lipid membrane down its concentration gradient, without a carrier or energy. It follows Fick's law and is a first order process; the commonest route of drug absorption.

**peripheral (tissue) compartment** — In a two- or three-compartment model, a kinetic space that exchanges drug with the central compartment by first-order transfer but from which no elimination occurs.

**permeability coefficient** — p = D·K/h, the velocity (cm·s⁻¹) at which a drug crosses unit area of a membrane per unit concentration gradient. It describes the membrane and the drug only. Multiplied by the available surface area it gives the permeability–surface-area product, p·A, a volume per time; the two are often confused, and only the product depends on anatomy.

**pH-partition hypothesis** — The proposal that drugs are absorbed by passive diffusion in proportion to their unionised fraction at the local pH. A useful first guide that ignores surface area, residence time and lipid solubility.

**Pharmaceutical alternatives** — Products containing the same active moiety by the same route but differing in dosage form (including release type) or in chemical form, such as the salt or ester.

**Pharmaceutical equivalents** — Products containing the same molar amount of the same active ingredient, in the same dosage form (including release type), meeting comparable standards and given by the same route. They may differ in shape, scoring, packaging, excipients and expiry date.

**pharmacokinetic model** — A set of equations that simulates the rate processes of ADME and so predicts the concentration of drug in the body at any time.

**Pharmacokinetics** — The kinetic study of absorption, distribution, metabolism and elimination: how fast each process occurs and what drug concentration results at any given time.

**Phase I** — Metabolic reactions that add or unmask a polar group, mainly oxidation and reduction, largely catalysed by cytochrome P450 with NADPH and molecular oxygen.

**Phase II** — Metabolic reactions that conjugate a drug or its Phase I product with an endogenous compound, such as glucuronic acid or an acetyl group, giving a more polar and usually inactive product.

**post-absorption phase** — The later part of an oral plasma curve, after the absorption term has decayed, during which the concentration falls with the elimination rate constant alone. It is the straight terminal portion on semilogarithmic axes.

**principle of superposition** — For first order (linear) kinetics, the concentration after several doses is the sum of the concentrations each dose would give on its own. It is the basis of all multiple dose equations.

**rate constant** — The proportionality constant linking a rate to the amount or concentration driving it. A first-order rate constant has units of reciprocal time (h⁻¹); a zero-order rate constant has units of amount or concentration per unit time.

**rate-limiting step** — The slowest step in a series of kinetic processes, which sets the overall rate. For a tablet it is often disintegration or dissolution rather than membrane transport.

**Relative bioavailability** — The bioavailability of a product compared with a reference product rather than with an intravenous dose: the ratio of their dose-normalised AUCs. It can exceed 100%.

**renal excretion rate constant** — Ke. The first-order rate constant for excretion of intact drug into the urine, so that dDu/dt = Ke·D_B. It equals fe × K, and is always less than or equal to K.

**residual concentration** — The difference Cp − Cp′ between a measured concentration and the value extrapolated from the terminal line at the same time. Its logarithm falls linearly with time during the distribution phase.

**sink condition** — The state in which the bulk concentration of dissolved drug stays far below its solubility (C ≪ Cs), so the dissolution rate is set by Cs and not by how much has already dissolved.

**stagnant layer** — The thin layer of unstirred solvent around a dissolving particle, of thickness h, across which drug diffuses from the saturated surface (Cs) to the bulk medium (C).

**statistical moment** — A summary of a distribution. In pharmacokinetics the zero moment of the plasma curve is AUC and the first is AUMC.

**steady-state concentration** — Css. The plateau concentration reached during a constant-rate infusion, at which the rate of elimination equals the rate of input. Css = R/Cl, so it depends on the infusion rate and clearance but not on Vd.

**Therapeutic equivalents** — Pharmaceutical equivalents that give the same clinical efficacy and safety when given to the same patients in the same regimen.

**therapeutic index** — A dimensionless ratio expressing the margin between toxic and effective exposure, classically TD50/ED50, or on a concentration basis MTC/MEC. It is a number, not a band of concentrations.

**therapeutic range** — The band of plasma concentrations between the MEC and the MTC, within which the drug is effective without being toxic. Also called the therapeutic window. It is not the therapeutic index.

**three-compartment open model** — A model with a central compartment and two peripheral compartments. The two peripheral compartments are not connected to each other; each exchanges only with the central compartment, from which elimination takes place.

**tmax** — The time at which Cpmax occurs. It measures the *rate* of absorption and, in linear kinetics, does not change with the dose.

**Total body clearance** — Cl. The volume of plasma completely cleared of drug per unit time, in volume per time. It is the sum of all clearing processes, Cl = K·Vd, and says nothing about which organ is responsible.

**transcellular** — Describing passage through epithelial cells, across both cell membranes. It suits unionised, lipid-soluble drugs.

**Tubular reabsorption** — Return of drug from the tubular fluid to the blood. It favours the more lipid-soluble, unionised form, so for weak acids and weak bases its extent depends on urinary pH and on the pKa of the drug.

**two one-sided tests** — The equivalence procedure behind bioequivalence: one test that the ratio is not below the lower limit and one that it is not above the upper limit, each at α = 0.05. Together they equal a 90% confidence interval lying inside the limits.

**two-compartment open model** — A model in which drug distributes rapidly into a central compartment and more slowly into a peripheral compartment, with first-order transfer between them (K₁₂ and K₂₁) and elimination from the central compartment only.

**vesicular transport** — Uptake of particles or fluid by invagination and engulfment of the cell membrane: pinocytosis, phagocytosis and receptor-mediated endocytosis, as for vitamin B₁₂ bound to intrinsic factor.

**Vmax** — The maximum rate of a saturable process, reached when the enzyme or carrier is fully occupied. Expressed as concentration per time, or as amount per time when multiplied by Vd.

**volume of distribution at steady state** — Vss. The volume relating amount in the body to plasma concentration when distribution is at equilibrium, Cl·MRT = D₀·AUMC/AUC² after an IV bolus. It needs no model.

**volume of the central compartment** — Vp. The apparent volume of the rapidly equilibrating compartment, obtained as the dose divided by (A + B). It is smaller than the total apparent volume of distribution, and it is the volume a loading dose fills immediately.

**Vp** — The volume of the central compartment. See [[volume-of-the-central-compartment]].

**Wagner–Nelson method** — A method for determining the amount of drug absorbed at each time by mass balance, requiring only that the body behaves as one compartment and that elimination is first order. Because it assumes nothing about absorption, it can be used to decide whether absorption is first order or zero order.

**washout period** — The interval between periods of a crossover study, long enough for pre-dose concentrations to be negligible; ICH M13A asks for at least five terminal half-lives, and the Egyptian guideline also for at least seven days.

**zero order** — Describing a process whose rate is constant and independent of the amount of drug present, so that a constant *amount* is transferred per unit time. A constant-rate infusion is zero-order input; saturated metabolism is zero-order output (Chapter 10).

**Zero-order absorption** — Absorption at a constant rate, independent of the amount of drug remaining at the absorption site, so that a constant *amount* is absorbed per unit time. Produced by osmotic pumps and well-designed sustained-release forms.


---

# References

Every work cited anywhere in this book, in one list. Each chapter also prints the short list it cites,
numbered for that chapter alone, so a citation such as [2] means the second entry of that chapter's own
list. The numbering here is independent of those lists; the chapters each entry is cited in are given
at the end of the entry.

1. Amidon GL, Lennernäs H, Shah VP, Crison JR. A theoretical basis for a biopharmaceutic drug classification: the correlation of in vitro drug product dissolution and in vivo bioavailability. *Pharm Res*. 1995;12(3):413–420. DOI: 10.1023/A:1016212804288 (Chapter 13.)

2. Aulton ME, Taylor KMG, editors. *Aulton's Pharmaceutics: The Design and Manufacture of Medicines*. 6th ed. Edinburgh: Elsevier; 2021. (Chapters 1, 14.)

3. Egyptian Drug Authority. *Egyptian Guideline for Conducting Bioequivalence Studies for Marketing Authorization of Generic Products* (EDREX: GL.CAPP.024), version 04/2026. Cairo: EDA; 2026. (Chapter 13.)

4. International Council for Harmonisation. *ICH Harmonised Guideline M13A: Bioequivalence for Immediate-Release Solid Oral Dosage Forms*. Geneva: ICH; 2024. (Chapter 13.)

5. International Council for Harmonisation. *ICH Harmonised Guideline M9: Biopharmaceutics Classification System-Based Biowaivers*. Geneva: ICH; 2019. (Chapter 13.)

6. Rowland M, Tozer TN. *Clinical Pharmacokinetics and Pharmacodynamics: Concepts and Applications*. 5th ed. Philadelphia: Wolters Kluwer; 2019. (Chapters 12 chapters.)

7. Shargel L, Yu ABC. *Applied Biopharmaceutics and Pharmacokinetics*. 8th ed. New York: McGraw Hill Medical; 2022. (Chapters 14 chapters.)

8. United States Pharmacopeial Convention. General Chapter <711> Dissolution. In: *United States Pharmacopeia and National Formulary (USP–NF)*. Rockville, MD: USP; current edition. (Chapter 14.)
