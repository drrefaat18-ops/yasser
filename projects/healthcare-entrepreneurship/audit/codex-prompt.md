Read-only review of a new university textbook, for the audit stage of a book pipeline.

Working directory: D:\AI\Book maker\projects\healthcare-entrepreneurship

Read only these files:
- build/Entrepreneurship_in_Healthcare.md — the finished book (14 chapters, about 39,000 words)
- brief.json                     — what the book was commissioned to be: entrepreneurship in the health sector for third-year Applied Health Sciences students (laboratory and imaging) in Egypt, with verified examples of Egyptian health entrepreneurs
- rubric.json                    — the six scoring pillars and their anchors
- rework/errata-ledger.md        — the source errors this book claims to correct
- rework/math-checks.md          — the arithmetic the build recomputes

Do not read ingest/ or evaluation/ unless a specific ledger claim needs checking against the source.

Find what is WRONG WITH THE BOOK. Be adversarial and specific:
1. Named people and companies (the brief's strictest rule). Every "Egyptian Entrepreneur" box and every other
   statement about a real person, company, programme or law must be supported by the source it cites. Fetch the
   cited URLs where you can and check founders, years, amounts and figures. Flag any fact the cited source does
   not support, any wrong attribution, and anything promotional. If a URL cannot be fetched, say so rather than
   guessing.
2. Recompute every worked example, every numeric MCQ and every essay answer with numbers (break-even, margin of
   safety, runway, market size, weighted scores, dilution). Flag any printed result you cannot reproduce.
3. Content accuracy: wrong definitions of entrepreneurship, business or culture terms (Hofstede, Danhof, Porter,
   the Business Model Canvas, MVP); statements about Egyptian law, regulation or accreditation that are wrong or
   overstated; claims a cited reference does not support; references that do not exist or have the wrong year
   or authors.
4. Ethics: anything that endorses unsafe testing, misleading promotion or inducements.
5. Assessment: is each MCQ key correct, is its rationale right, is any distractor also defensible?
6. Internal consistency: contradictions between chapters, wrong cross-references, figures that do not match the
   text.

Output ONLY the following. First three lines:
verdict: pass or fail
open_blocker_major: <count of blocker and major rows in your table>
reviewer_model: <the model you are>

Then one markdown table:

| ID | severity | location | finding | why it matters | suggested fix |

IDs C-001, C-002, ... Severity is blocker, major or minor. Location is a chapter and section, or a quoted
phrase precise enough to find. Do not report style preferences or anything you have not verified.

Then a section "Scores" with one line per rubric pillar (G1, G2, G3, G4, D1, D2): the score from 1 to 10 under
the rubric's anchors, and the finding IDs that justify it. Then a short Notes section, including which cited
URLs you fetched and what they supported.
