# Design — Healthcare Marketing: Marketing and Health Economics for Applied Health Sciences

Inputs: `brief.json`, `rubric.json`, `template.json`, `theme.json`, `agents/healthcare-marketing-reviewer.json`
(DEC-001); `evaluation/report.md`, `evaluation/findings.json`, `evaluation/scorecard.json` (37.0 / 100),
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

Budgets total 36,200 words against a template range of 28,000–45,000.

| ID | Title | Words | Source | Notes |
|---|---|---|---|---|
| ch01 | Marketing in Health Care | 2900 | L1 | Current AMA definition; needs, wants and demands; value, exchange, markets; the scope of marketing for a health service |
| ch02 | The Healthcare Market and Its Customers | 3000 | L2 second half | Who decides, pays and uses; buying triggers; the healthcare market against consumer markets; demand and price sensitivity; principles and problems of healthcare marketing |
| ch03 | Digital Marketing in Health Care | 2800 | L1, L2 first half | Channels, benefits, objectives, digital against traditional as tendencies; health-data privacy |
| ch04 | The Marketing Mix: From Four Ps to Seven | 2900 | L1 marketing mix | The 4 Ps, then people, process and physical evidence for services; the service elements of a pharmaceutical product |
| ch05 | Health Products and Services | 3000 | L3 first half | Goods and services; consumer-product classes in standard terms; medicines and medical devices; customer value |
| ch06 | The Product Life Cycle | 2900 | L3 second half | Four stages with properties and strategies; the pharmaceutical and diagnostic cases; avoiding decline |
| ch07 | Pricing Health Services | 3200 | L4 | Functions and kinds of price; pricing methods; demand, regulation and competition; market structures; setting the price; price policy |
| ch08 | Distribution and Access | 3000 | L5 | Distribution and channels; channel levels for medicines and for diagnostic services; intermediaries; retail trade and pharmacies |
| ch09 | Marketing Communications and Promotion | 3200 | L6 | The communication mix; push and pull; advertising and sales promotion; opinion leaders; the ethical and legal limits of promotion |
| ch10 | Health-Care Costs | 3000 | L7 | Health economics and pharmacoeconomics; inputs and outcomes; perspectives; cost categories; valuing indirect costs; the cost-classification activity, corrected |
| ch11 | Outcomes and Methods of Economic Evaluation | 3300 | L8 | ECHO outcomes; QALYs; the five methods; ICER and the cost-effectiveness plane; sensitivity analysis; steps of an evaluation |
| ch12 | Applying Economic Evaluation | 3000 | L9 | Micro-costing, CMA against CEA with the corrected ICER, CBA with simple and incremental ratios; laboratory and imaging applications |

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

## 6. References

APA 7. Each chapter cites a small set of standard works; the consolidated list at the back is their union. The
core set is a standard marketing text, a services-marketing text, a health-care marketing text, a health-economics
methods text, and the primary sources for any definition or code quoted (the American Marketing Association's
definition; the IFPMA Code of Practice; WHO guidance on economic evaluation). A reference is used only when the
statement it supports has been checked against it.

## 7. Figures

Drawn as SVG sources in `rework/figures/src`, listed in `rework/figures/figures.json`:
the 7 Ps around the patient (ch04), the product life cycle (ch06), channel levels (ch08), push and pull (ch09),
the cost-outcome balance (ch10), and the cost-effectiveness plane (ch11).

## 8. Risks

- **Egyptian facts.** Regulation, pricing and insurance rules change, and few are easy to cite from here. The book
  states only what it can attribute, names the responsible authority, and keeps the title-page notice.
- **NARS.** The user chose to start without the NARS document. The book makes no claim of NARS alignment; when the
  document is supplied, the objectives are mapped to it in a later pass.
- **Credit.** The user chose to credit the author alone and not the source lectures (DEC-001). The book therefore
  writes new text rather than reproducing the lectures' wording.
