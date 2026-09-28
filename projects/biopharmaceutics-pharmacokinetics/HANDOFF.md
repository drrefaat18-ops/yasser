# Handoff prompt — finish the Biopharmaceutics & Pharmacokinetics book

Paste everything below the line into a new Claude Code session opened at `D:\AI\Book maker`.

---

Continue the book at `projects/biopharmaceutics-pharmacokinetics`. Chapters 1–6 are written and each
passes all 33 harness checks. Write **ch07 through ch14**, then the front matter, the glossary tail and
the errata ledger, then close the rework stage, build and audit. Read `CLAUDE.md` first — Rules 7, 8
and 11 bind you.

## Where things stand

- Gates passed and approved: intake (DEC-001), design (DEC-003, which supersedes DEC-002).
- `rework` is the open stage. **Do not run `begin rework` if a run is already active** — run
  `python harness/run_stage.py --project projects/biopharmaceutics-pharmacokinetics verify` first and
  read the nonce out of any `RUN-ACTIVE` line.
- Written and passing: ch01–ch06, `rework/glossary.md` (49 of the 90 terms required),
  `rework/figures/figures.json` with 8 figures.
- Still to write: ch07–ch14, `rework/00-front-matter.md`, `rework/errata-ledger.md`, and the rest of
  the glossary.
- Last commit: `e2e6f32`.

## Environment quirks that will cost you an hour if you miss them

- **Git is not on PATH.** Prefix every PowerShell command with
  `$env:Path = "C:\Program Files\Git\cmd;$env:Path";`. The Bash tool has git already.
- **Hashes for approvals are canonical, not raw.** `harness/hashing.py::hash_file` hashes `.json` as
  canonical JSON and normalises CRLF→LF for `.md/.txt/.svg/.py`. `Get-FileHash` gives the wrong value
  and the harness will reject it with `DEC-HASH-MISMATCH`.
- **One Codex review only.** The user said "يكفي مراجعة واحدة لكودكس فقط". The evaluate artifact has
  had its one review. Do not run Codex again on it.
- Write chapter files with the Write tool. A bash heredoc chokes on this content.

## The checker is the specification

Run it after every chapter:

```
python "<scratchpad>/chk.py" ch07
```

`chk.py` already exists in the session scratchpad; if the new session has a fresh scratchpad, recreate it:

```python
import json, pathlib, sys
sys.path.insert(0, r"D:\AI\Book maker")
from harness.tools import check_book, config
P = pathlib.Path(r"D:\AI\Book maker\projects\biopharmaceutics-pharmacokinetics")
cfg = config.load(P)
for cid in (sys.argv[1:] or [c["id"] for c in cfg["chapter_plan"]["chapters"]]):
    entry = next(c for c in cfg["chapter_plan"]["chapters"] if c["id"] == cid)
    f = P / "rework" / entry["file"]
    if not f.is_file():
        print(f"{cid}: not written"); continue
    rep = check_book.check_chapter(f, cfg, entry)
    bad = [c for c in rep["checks"] if c["status"] == "fail"]
    print(f"{cid}: {len(rep['checks'])} checks, {len(bad)} fail")
    for c in bad:
        for line in c["message"].split("; "):
            print("   FAIL", c["id"], "-", line)
```

Exact formats it demands — these are not style preferences, they are regexes:

- Heading: `# Chapter 7: Title`
- Sections, in this order and with these exact labels: `## Learning Objectives`, numbered body
  sections, `## Key Takeaways`, `## Check Your Understanding`, `## Answers and Worked Solutions`,
  `## References`.
- Objectives: 3–5 lines of the form `1. [LO1] Verb ...`. The verb "understand" is rejected.
- MCQs: exactly 10, each `**Q1.** [LO2] Stem?` then four option lines `A) text` — `A.` fails.
- Answer key: `**Q1. B** — rationale`, with an em dash.
- Key balance: each of A/B/C/D correct 2–3 times, and no letter may repeat more than twice in a row.
  Plan the key before writing the questions. A sequence that works: B D A C B C D A B C.
- Every LO must be assessed by at least one question.
- Callouts, at least one of each of the first two:
  `> **Key Equation:**`, `> **Worked Example:**`, `> **Watch the Units:**`, `> **Common Mistake:**`,
  `> **Why It Matters in Practice:**`, `> **Deeper Dive:**`.
- **Bold is the glossary marker.** Every `**bold**` span in prose becomes a glossary term and must
  have an entry in `rework/glossary.md`. Use *italics* for emphasis, never bold. Do not bold
  paragraph lead-ins.
- Citations: any `[n]` must resolve against a numbered entry in that chapter's own `## References`
  section, and every listed reference must be cited at least once. Two references per chapter is
  enough. The References section is excluded from the word budget.
- Readability: mean sentence ≤ 16 words, and at most 5% of sentences over 28 words.
- Budget: the chapter's `word_budget` in `design/chapter-plan.json` ±15%.

`GLOSS-MISSING` failures are fixed by appending to `rework/glossary.md` in the format
`**term** — definition`, one blank line between entries, alphabetical.

## Budgets and titles still to write

| id | title | budget | source pages |
|---|---|---|---|
| ch07 | Oral Absorption | 4200 | 30–38 |
| ch08 | Multiple Dose Regimens | 3400 | 39–42 |
| ch09 | Non-Compartmental Analysis | 2800 | 43–46 |
| ch10 | Non-Linear Pharmacokinetics | 2400 | 47–48 |
| ch11 | Pharmacokinetics of Metabolites | 2700 | 49–53 |
| ch12 | Biopharmaceutical Considerations | 5000 | 54–78 |
| ch13 | Bioavailability and Bioequivalence | 5000 | 79–100 |
| ch14 | Dissolution | 3400 | 101–109 |

Source text is `ingest/normalized.md` (5018 lines). It is a markitdown conversion, so equations are
badly mangled — the *content* is readable but every formula must be reconstructed and every number
re-derived. **Never copy an equation from it without checking the arithmetic yourself.** Useful line
offsets: oral absorption ~1376–1850, multiple dose ~1850–2160, statistical moments 2162, non-linear
2431, metabolites 2592, biopharmaceutics 2851+, bioavailability 4061+, bioequivalence 4465,
dissolution 4700+.

## House style, so ch07–ch14 match ch01–ch06

Read ch02 and ch06 before writing anything; they are the pattern.

- Voice: plain declarative sentences, second person for instructions, no hedging, no filler.
- Each chapter: 4–6 numbered sections, then the fixed tail sections.
- Every chapter has one full **Worked Example** built from a real dataset in the source, solved in
  numbered steps with units carried through every line, ending in an explicit *Answer* and then a
  *Check* that verifies the result by an independent route.
- Three exercises `**E7.1** [LO2] ...` in the assessment section, each fully solved under
  `## Answers and Worked Solutions` after a `---` rule.
- Cross-reference other chapters by number in prose ("Chapter 9 generalises it").
- Prefer a table to a list when the content is a comparison.

## Figures

Each chapter gets one figure where a figure genuinely teaches. Workflow:

1. Write `<scratchpad>/figNN.py` importing `figlib` (already in the scratchpad; it holds
   `head/box/arrow/label/line/polyline/dot/frame/write`, the theme palette, and a `halo=True` option
   on `label` for annotations that sit over lines). Palette: ink `#1D2A38`, primary `#104C4A`,
   accent `#B26B00`, muted `#5A6470`.
2. Run it — it writes to `rework/figures/src/<id>.svg`.
3. Render to PNG and **look at it** before accepting it. Headless Edge is flaky; retry up to three
   times and pass a per-figure `--user-data-dir`:
   `& "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --headless=new --disable-gpu --force-device-scale-factor=2 --user-data-dir="$env:TEMP\edge-X" --window-size=W,H --screenshot="out.png" "file:///..."`
4. Check for overlapping labels. This has caught a problem on almost every figure so far.
5. Append an entry to `rework/figures/figures.json` with `id`, `chapter_id`, `kind: "diagram.svg"`,
   `source`, a teaching `caption`, a full prose `alt`, `credit`, `licence: "original"`,
   `status: "generated"`.
6. Reference it in the chapter as `![](fig:<id>)`. Numbering comes from the template, not from you.

Do not reuse the PDF's raster images — the user asked for everything redrawn.

## Errata that must land in these chapters

`design/errata-seed.md` holds 32 rows. These belong to the remaining chapters:

- **ch07** — E-013 (F-014): the Wagner–Nelson example tabulates Cp in mg/mL; it is µg·mL⁻¹, and the
  units must be carried through AUC and every derived column.
- **ch08** — E-032 (F-035): the accumulation-half-life formula and its IV collapse are asserted.
  Derive them, show log(1) = 0 as the reason the bracket collapses, and state the Ka > K assumption.
- **ch09** — E-019 (F-027): a procainamide observation is followed by about seventy exclamation
  marks. Keep the observation and explain it: the compartment count is a property of the data and
  the sampling design, not of the drug.
- **ch11** — E-008 (F-008): "Black men are faster acetylators than white men" is wrong and must go.
  Acetylation rate is set by NAT2 genotype; allele frequencies differ between populations and do not
  track skin colour. Give CYP2D6 and CYP2C19 polymorphisms alongside. E-028 (F-040): norfluoxetine,
  4-OH propranolol, norverapamil and desmethyldiazepam are labelled toxic; they are *active*
  metabolites. Keep NAPQI as the toxic example.
- **ch12** — E-006 (F-006): oligopeptides are said to be digested by lactase and maltase; they are
  hydrolysed by brush-border peptidases (aminopeptidase N, DPP-IV) and cytosolic peptidases, and the
  disaccharidases move to carbohydrate digestion. E-007 (F-007): tetracyclines are not quaternary
  nitrogen compounds; they are amphoteric with three ionisable groups. E-009 (F-009): the claim that
  Egyptians have a genetic defect in the vitamin B₁₂ carrier is removed; B₁₂ uptake is
  intrinsic-factor-mediated receptor endocytosis. E-029 (F-041): the dosage-form bioavailability
  ranking is a tendency following from the number of steps before absorption, not a universal law —
  give one counter-example. E-015: drop the stray Arabic gloss.
- **ch13** — the heaviest. E-001 (F-001): **BCS Class 2 is backwards in the source.** ICH M9 grants
  biowaivers to Class 1 and Class 3; Class 2 needs an in-vivo study. E-002: high permeability is
  ≥ 85%, not ≥ 90%. E-003: highly soluble means the highest single therapeutic dose in ≤ 250 mL over
  pH 1.2–6.8 at 37 ± 1 °C. E-004: state the acceptance criterion — the 90% CI of the test/comparator
  geometric mean ratio for log-transformed AUC and Cmax within 80.00–125.00%, narrowed for NTI drugs.
  E-005: it is a 90% CI (two one-sided tests at α = 0.05), not a 95% significance test. E-021:
  Amidon et al. 1995, not 1985. E-022: ICH M13A subjects are ≥ 18 years with BMI 18.5–30 kg·m⁻²; the
  54–91 kg band is the historical FDA criterion. E-024: washout is long enough that pre-dose
  concentrations are negligible, commonly ≥ 5 terminal half-lives (ICH **M13A**, not M9). E-025
  (F-037): F = 1 does not mean complete absorption — F = fa × Fg × Fh; use propranolol as the case.
  E-026 (F-038): release mechanism is *not* a permitted difference between pharmaceutical
  equivalents; products differing in it are pharmaceutical alternatives. E-027 (F-039): the
  "comparator must contain at least 5% drug" rule is invented — delete it and use the ICH M13A
  comparator-selection and batch-potency requirements.
- **ch14** — E-010 (F-010): USP <711> Apparatus 4 flow rates are 4, 8 and 16 mL·min⁻¹. E-012
  (F-013): set the Noyes–Whitney equation as numbered text, dC/dt = (D·A/h)(Cs − C), with the
  sink-condition simplification C ≪ Cs.
- **All chapters** — E-030 (F-019): number examples per chapter (7.1, 7.2, …), never with the
  source's global 1–23 sequence, which printed 22 and 23 before 19–21.

When a chapter's errata are written and verified, that row's `Status` becomes `fixed` in
`rework/errata-ledger.md` (create it from `design/errata-seed.md`, keeping the same IDs and columns).
The book-level check `ERRATA-OPEN` fails while any row is still `open`, so every row must close as
`fixed` or `removed-with-content` before the build.

## Source arithmetic already verified — reuse it, do not re-derive from scratch

- Examples 5 and 8 are the plasma and urine views of one study: 50 kg, 20 mg·kg⁻¹ = 1000 mg,
  K = 0.693 h⁻¹, t½ = 1.00 h, fe = 1, Du∞ = 1000 mg. Used in ch02 and ch03.
- Example 6: 300 mg, K = 0.170 h⁻¹, Cp⁰ = 8.57 µg·mL⁻¹, Vd = 35.0 L, Cl = 5.96 L·h⁻¹. Used in ch02.
- Examples 9 and 10 are the same drug: Cp = 45e^(−1.8t) + 15e^(−0.21t), giving K₂₁ = 0.608,
  K = 0.622, K₁₂ = 0.780 h⁻¹, Vp = 5.0 L. Used in ch04.
- Example 14: 75 kg, K = 0.2 h⁻¹, Vd = 7.5 L (0.1 L·kg⁻¹), Cl = 1.5 L·h⁻¹, Css = 10 µg·mL⁻¹, and the
  1 mg·kg⁻¹ bolus is exactly Css·Vd so the combined curve is flat. Used in ch05.
- Example 18: Vd = 16.4 L, Cl_T = 5.68 L·h⁻¹, fu = 0.70, Cl_r = 3.98, Cl_nr = 1.70 L·h⁻¹, clearance
  ratio 0.54. Used in ch06.
- **Example 22 (ch07) was not finished.** The terminal fit over t = 16–28 h gives K = 0.0867 h⁻¹
  (t½ = 8.0 h) and A ≈ 105 µg·mL⁻¹, but the residual line is not straight: successive residual
  slopes steepen from −0.26 to −0.29 h⁻¹, and the resulting Ka does not reproduce the observed peak
  near 7 h. Fit the full biexponential Cp = A(e^(−Kt) − e^(−Ka·t)) numerically before you write
  anything, and if the data are internally inconsistent, say so in the chapter rather than quoting a
  number the data do not support. Dose is 500 mg with F = 0.80.

## Finishing the book

1. `rework/00-front-matter.md` — budget 600 words. Title page matter, the teaching-not-prescribing
   notice from `theme.json`, credit to "Staff Members of the Pharmaceutical Technology Department",
   and a `## How to Use This Book` section. The contents page is generated by the build; do not
   write one.
2. `rework/glossary.md` — must reach **≥ 90 entries** and must contain every bolded term in every
   chapter.
3. `rework/errata-ledger.md` — all 32 rows closed.
4. One consolidated reference list at the back of the book is the user's intake choice. The
   per-chapter lists are the working numbering; the back-of-book list is their union.
5. Then:
   ```
   python harness/run_stage.py --project projects/biopharmaceutics-pharmacokinetics complete rework --nonce <N>
   python harness/run_stage.py --project projects/biopharmaceutics-pharmacokinetics run build
   python harness/run_stage.py --project projects/biopharmaceutics-pharmacokinetics run audit
   ```
   Output is Word plus a designed A4 PDF, basename `Biopharmaceutics_and_Pharmacokinetics_PT312`.
6. Commit after each gate passes. Never push. End commit messages with
   `Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>`.

## Scope boundary

The user's intake choice was **simplify and organise only, no new topics**, keeping the same 14
subjects in the printed order. Correcting the errata above is in scope because the user approved it
explicitly at the design gate. Adding topics the source does not cover is not.

If you hit a genuine fork — a budget that cannot be met without cutting teaching content, or a
finding that needs a decision — stop and ask, and if it changes an approved artifact, amend it, show
the canonical hashes, get a clear yes, add a DEC row to `decisions.md`, and only then run
`approve design --dec DEC-NNN`.
