Read-only review of a new university textbook, for the audit stage of a book pipeline.

Working directory: D:\AI\Book maker\projects\marketing-book

Read only these files:
- build/Healthcare_Marketing.md  — the finished book (12 chapters, about 32,000 words)
- brief.json                     — what the book was commissioned to be: healthcare marketing and health economics for third-year Applied Health Sciences students (laboratory and imaging) in Egypt
- rubric.json                    — the six scoring pillars and their anchors
- rework/errata-ledger.md        — the source errors this book claims to correct

Do not read ingest/ or evaluation/ unless a specific ledger claim needs checking against the source.
Use web search only to confirm a specific definition, regulation or reference you are unsure of.

Find what is WRONG WITH THE BOOK. Be adversarial and specific:
1. Recompute every worked example, every numeric MCQ and every essay answer with numbers. Flag any printed
   result you cannot reproduce, any wrong unit, and any wrong decision rule (dominance, B/C, ICER).
2. Content accuracy: wrong definitions of marketing or health-economics terms; statements about Egyptian law,
   regulation or insurance that are wrong or overstated; claims a cited reference does not support; references
   that do not exist or are cited with the wrong year or authors.
3. Ethics: anything that endorses misleading or inducement-based promotion of health services or medicines.
4. Assessment: is each MCQ key correct, is its rationale right, is any distractor also defensible?
5. Internal consistency: contradictions between chapters, wrong cross-references.

Output ONLY the following. First three lines:
verdict: pass or fail
open_blocker_major: <count of blocker and major rows in your table>
reviewer_model: <the model you are>

Then one markdown table:

| ID | severity | location | finding | why it matters | suggested fix |

IDs C-001, C-002, ... Severity is blocker, major or minor. Location is a chapter and section, or a quoted
phrase precise enough to find. Do not report style preferences or anything you have not verified.
Then a short Notes section.
