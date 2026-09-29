Read-only review of a textbook evaluation, for the evaluate stage of a book pipeline.

Working directory: D:\AI\Book maker\projects\marketing-book

Read only these files:
- ingest/normalized.md       — the source: nine lecture notes on pharmaceutical marketing and pharmacoeconomics (1,457 lines)
- brief.json                 — the book to be made from them: healthcare marketing for third-year Applied Health Sciences students (laboratory and imaging), Egypt
- rubric.json                — the six pillars and their band anchors
- evaluation/findings.json   — 31 findings against the source
- evaluation/scorecard.json  — the scores
- evaluation/report.md       — the report

Your job is to check the EVALUATION, adversarially and specifically:
1. Is each finding true of the source at the cited lines? Is its evidence quoted accurately? Is its severity and pillar right?
2. What did the evaluation MISS in the source: wrong definitions, wrong economics, wrong arithmetic, misleading
   claims, missing ethics or regulation? Recompute every worked example in lectures 7–9.
3. Do the scores follow from the findings and the rubric anchors? Is the total arithmetic right?
4. Is anything in a fix_hint itself wrong?

Do not browse widely; use web search only to confirm a specific definition or regulation you are unsure of.

Output ONLY the following. First three lines:
verdict: pass or fail
open_blocker_major: <count of blocker and major rows in your table>
reviewer_model: <the model you are>

Then one markdown table with these columns:

| ID | severity | location | finding | why it matters | suggested fix |

IDs C-001, C-002, ... Severity is blocker, major or minor. Location is a finding ID or a line of ingest/normalized.md.
Do not report style preferences. Do not report anything you have not verified. Then a short Notes section.
