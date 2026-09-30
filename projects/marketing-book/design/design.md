# Design — Healthcare Marketing: Marketing and Health Economics for Applied Health Sciences

Inputs: `brief.json`, `rubric.json`, `template.json`, `theme.json`, `agents/healthcare-marketing-reviewer.json`
(DEC-001); `evaluation/report.md`, `evaluation/findings.json`, `evaluation/scorecard.json` (33.0 / 100),
`evaluation/codex-review.md`, `evaluation/fixes.md`.

## 1. What this book is

A first textbook of marketing and health economics for third-year students of the Faculty of Applied Health
Sciences, East Portsaid National University. Its readers will work in medical laboratories, imaging centres and
other health services. They know their service from the bench and the scanner; this book shows them the same
service from the side of the patient who chooses it, the organisation that runs it and the payer who funds it.

The source is nine lecture notes on pharmaceutical marketing and pharmacoeconomics. The book keeps every topic of
those lectures, in their order, and every worked example, corrected where it is wrong. It broadens them in the one
direction the brief asks: from medicines to health care as a whole, and from pharmacoeconomics to health economics.
The text is new; the lectures supply the syllabus, not the wording.

## 2. Principles

1. **Services first.** Most of what the readers will sell is a service: a test, a scan, a session. Every concept is
   taught first for a health service, then shown for medicines and devices. The 7 Ps replace the 4 Ps as the
   organising frame, because people, process and physical evidence are what a patient actually meets.
2. **The patient is not an ordinary consumer.** Who decides, who pays, who uses and who bears the risk differ
   between a self-paid laboratory test, a prescribed MRI and an insured admission. The book returns to that
   distinction in every chapter instead of stating it once.
3. **Ethics inside every topic.** Promotion, pricing and communication in health care are bounded by professional
   ethics and by law. Every chapter carries an Ethics Check, and Chapter 9 treats the rules of promotion in full.
4. **Two lenses.** Every chapter has a Through Two Lenses box with one paragraph for the Medical Laboratory and one
   for Radiology and Medical Imaging, balanced in length (template tolerance 20%).
5. **Egypt as the setting.** Examples use Egyptian pounds (EGP), Egyptian institutions and the Egyptian mix of
   out-of-pocket payment, public provision and the Universal Health Insurance system. Where a fact about Egypt cannot
   be cited it is not stated; numbers in examples are marked as illustrative.
6. **Numbers are checked.** Every calculation in the economics chapters is declared in `rework/math-checks.md` and
   recomputed by the build's math gate. Formulas are set as equations.

## 3. Structure

Twelve chapters in three parts. The order of the lectures is kept; three lectures are split where a topic needs a
chapter of its own (the brief allows merging and splitting).

| Part | Chapters | Content |
|---|---|---|
| I — Marketing and the Healthcare Market | ch01–ch03 | What marketing is, what makes the healthcare market different, and digital marketing |
| II — The Marketing Mix for Health Services | ch04–ch09 | The mix as a whole, then product, life cycle, price, place and promotion in turn |
| III — Health Economics | ch10–ch12 | Costs, outcomes and methods, and applying economic evaluation |

### Chapter shape

1. **Learning Objectives** — 3 to 5, boxed, measurable verbs, each assessed.
2. **Body** — numbered sections of explained prose, mean sentence length at most 16 words.
3. **Required boxes** — at least one each of Through Two Lenses, In Practice and Ethics Check.
4. **Optional boxes** — Key Formula, Worked Example, Common Mistake, Egyptian Context, as the material needs.
5. **Key Takeaways** — 5 to 8 lines.
6. **Check Your Understanding** — 10 four-option MCQs tagged to objectives, then three short essay questions.
7. **Answers and Worked Solutions** — every MCQ with its rationale; every essay question with model answer points.
8. **References** — APA 7, the works the chapter cites; the book closes with the consolidated list.

## 4. Chapters and budgets

Budgets total 34,600 words against a template range of 28,000–45,000. They were set from the
drafted chapters, about 5% above each chapter's length, so that every chapter sits inside its ±15% band.

| ID | Title | Words | Source | Notes |
|---|---|---|---|---|
| ch01 | Marketing in Health Care | 3000 | L1 | Current AMA definition; needs, wants and demands; value, exchange, markets; the scope of marketing for a health service |
| ch02 | The Healthcare Market and Its Customers | 2900 | L2 second half | Who decides, pays and uses; buying triggers; the healthcare market against consumer markets; demand and price sensitivity; principles and problems of healthcare marketing |
| ch03 | Digital Marketing in Health Care | 2800 | L1, L2 first half | Channels, benefits, objectives, digital against traditional as tendencies; health-data privacy |
| ch04 | The Marketing Mix: From Four Ps to Seven | 2650 | L1 marketing mix | The 4 Ps, then people, process and physical evidence for services; the service elements of a pharmaceutical product |
| ch05 | Health Products and Services | 2700 | L3 first half | Goods and services; consumer-product classes in standard terms; medicines and medical devices; customer value |
| ch06 | The Product Life Cycle | 2700 | L3 second half | Four stages with properties and strategies; the pharmaceutical and diagnostic cases; avoiding decline |
| ch07 | Pricing Health Services | 3100 | L4 | Functions and kinds of price; pricing methods; demand, regulation and competition; market structures; setting the price; price policy |
| ch08 | Distribution and Access | 2750 | L5 | Distribution and channels; channel levels for medicines and for diagnostic services; intermediaries; retail trade and pharmacies |
| ch09 | Marketing Communications and Promotion | 2950 | L6 | The communication mix; push and pull; advertising and sales promotion; opinion leaders; the ethical and legal limits of promotion |
| ch10 | Health-Care Costs | 3050 | L7 | Health economics and pharmacoeconomics; inputs and outcomes; perspectives; cost categories; valuing indirect costs; the cost-classification activity, corrected |
| ch11 | Outcomes and Methods of Economic Evaluation | 3250 | L8 | ECHO outcomes; QALYs; the four comparative methods, with cost-of-illness as a descriptive study; ICER and the cost-effectiveness plane; sensitivity analysis; steps of an evaluation |
| ch12 | Applying Economic Evaluation | 2750 | L9 | Micro-costing, CMA against CEA with the corrected ICER, CBA with simple and incremental ratios; laboratory and imaging applications |

## 5. What the evaluation findings require, and where

Every finding of `evaluation/findings.json` is addressed in the chapter named here; `design/errata-seed.md` lists
the wrong statements, and `rework/errata-ledger.md` closes each one.

| Findings | Chapter | Treatment |
|---|---|---|
| F-001 (elasticity) | ch02, ch07 | Law of demand separated from elasticity; necessary care inelastic, elective and OTC services more elastic |
| F-002, F-003, F-004 (incremental cost, total-cost formula, cost activity) | ch10 | Correct definitions; total cost of one option; the activity reworked with a stated perspective |
| F-005, F-028 (ICER value and dominance; CER notation) | ch11, ch12 | −0.9 EGP per percentage point; dominance from the signs of the differences; the cost-effectiveness plane |
| F-006 (translated terms) | ch05, ch07 | Standard terms throughout |
| F-007 (examples) | ch07 | Examples that fit the category |
| F-008, F-009 (advertising claims and functions) | ch09 | Advertising as one tool, with its legal limits |
| F-010 (CUA, COI) | ch11 | Corrected statements |
| F-011 (consignment) | ch08 | Standard meaning of consignment |
| F-012 (QALY baseline) | ch11 | Baseline utility stated |
| F-013 to F-017 (teaching design, assessment) | all | Chapter shape of §3 |
| F-018 to F-021 (sources, currency) | all | APA citations; current AMA definition; the spending figure replaced or removed |
| F-022 to F-027 (scope, 7 Ps, ethics, opinion leaders, payer and decider) | all; ch04, ch09, ch02 | Principles 1–4 of §2 |
| F-029 to F-031 (CBA table, decision rule, micro-costing) | ch12 | Costs and benefits separated; three B/C cases; micro-costing named |
| F-032 to F-034 (formulary rule, WTP grouping, patient perspective) | ch10 | Dominance then incremental comparison; productivity methods separated from WTP; patient and caregiver costs listed |
| F-035 to F-038 (ACER, cost-utility rule, CMA condition, Example 2 basis) | ch11, ch12 | ACER = total C ÷ total E; incremental cost per QALY; equivalence in all relevant outcomes; cost and effect bases stated |
| F-039 (advertising "expands scope") | ch09 | Approved indications only, citing the EDA promotion guidelines |
| F-040, F-041 (price and QALY definitions) | ch07, ch11 | Price distinguished from cost and value; QALY = years × utility |

### Mapping of every blocker and major finding

| Finding | Chapter | Reason |
|---|---|---|
| F-001 | ch02 | Law of demand separated from elasticity; necessary care inelastic, self-paid services more elastic (also ch07). |
| F-002 | ch10 | Incremental cost defined as ΔC between options, the ICER numerator. |
| F-003 | ch10 | Total cost of one option excludes incremental cost; intangible costs reported separately. |
| F-004 | ch10 | Cost activity reworked with a stated perspective; opportunity cost and replacement cost corrected. |
| F-005 | ch11 | Cost-effectiveness plane; dominance read from the quadrant (also ch12). |
| F-006 | ch05 | Standard terms: convenience, shopping, specialty, unsought goods; medical devices (also ch07 for price functions). |
| F-013 | ch01 | Every chapter is explained prose; the chapter shape of §3 applies to all twelve. |
| F-014 | ch01 | Every chapter opens with 3–5 assessed objectives. |
| F-017 | ch01 | Ten MCQs and three essay questions per chapter, with answers. |
| F-018 | ch01 | APA citations throughout; consolidated reference list. |
| F-019 | ch01 | Current AMA definition, cited, with the 1985 wording noted. |
| F-020 | ch10 | Unsourced spending figure removed (errata E-014). |
| F-022 | ch01 | Health services first in every chapter, with the two-lens box. |
| F-023 | ch04 | Seven Ps with people, process and physical evidence applied to laboratory and imaging. |
| F-024 | ch09 | Ethical and legal limits of promotion, with an Ethics Check in every chapter. |
| F-025 | ch09 | Opinion leaders defined as clinicians; regulators described as independent bodies. |
| F-026 | ch02 | Who pays varies; Egyptian out-of-pocket payment described. |
| F-028 | ch11 | CER and ICER distinguished; the worked example in ch12 uses ICER. |
| F-032 | ch10 | Dominance, then incremental comparison, replaces 'most effective at lowest price'. |
| F-033 | ch10 | Productivity methods separated from willingness to pay; friction period defined. |
| F-034 | ch10 | Patient perspective includes time, copayments, lost income and caregiving. |
| F-035 | ch11 | ACER = total cost ÷ total effect; ICER for decisions. |
| F-036 | ch11 | Incremental cost per QALY against a threshold; average ratio descriptive only. |
| F-037 | ch11 | CMA only after equivalence in all relevant outcomes (also ch12). |
| F-038 | ch12 | Example 2 states cost per 30-day supply and effect at three months. |
| F-039 | ch09 | Advertising limited to approved indications; EDA promotion guidelines cited. |
| F-040 | ch07 | Price distinguished from cost and value. |
| F-041 | ch11 | QALY = years × utility, with the utility source named. |

## 6. References

APA 7. Each chapter cites a small set of standard works; the consolidated list at the back is their union. The
core set is a standard marketing text, a services-marketing text, a health-care marketing text, a health-economics
methods text, and the primary sources for any definition or code quoted (the American Marketing Association's
definition; the IFPMA Code of Practice; WHO guidance on economic evaluation). A reference is used only when the
statement it supports has been checked against it.

## 7. Figures

Twenty-two figures, at least one in every chapter, listed in `rework/figures/figures.json` and numbered per chapter
in order of placement. Each is cited in the text, and each has a caption, alt text, a credit and a licence.

- **Diagrams (15), drawn as SVG in the theme palette from the chapter's own content and numbers:** the marketing
  process (ch01); the customer roles and inelastic against elastic demand (ch02); the digital campaign steps (ch03);
  the 7 Ps around the patient and a service blueprint of a blood test (ch04); customer value (ch05); the product
  life cycle (ch06); the break-even chart (ch07); channel levels (ch08); push and pull (ch09); the cost-outcome
  balance (ch10); the ECHO model and the cost-effectiveness plane (ch11); choosing a method (ch12).
- **Illustrations (3), original SVG scenes:** online booking (ch03), the reagent cold chain (ch08) and a health
  awareness day stand (ch09).
- **Photographs (4):** public-domain works from Wikimedia Commons, credited under each photograph, with their
  sources in `rework/figures/photo-sources.md`: an imaging room (ch04), a microbiology laboratory (ch05), a new MRI
  scanner being installed (ch06) and a pharmacy counter (ch08). A photograph shows no unsafe practice and no
  identifiable patient in a clinical situation.

## 8. Risks

- **Egyptian facts.** Regulation, pricing and insurance rules change, and few are easy to cite from here. The book
  states only what it can attribute, names the responsible authority, and keeps the title-page notice.
- **NARS.** The user chose to finish the book without the NARS document. The book makes no claim of NARS alignment.
  If the document is supplied later, the objectives can be mapped to it in a new pass.
- **Credit.** The user chose to credit the author alone and not the source lectures (DEC-001). The book therefore
  writes new text rather than reproducing the lectures' wording.
