Read-only review of a rewritten university textbook, for the audit stage of a book pipeline.

Working directory: D:\AI\Book maker\projects\biopharmaceutics-pharmacokinetics

Read these:
- build/Biopharmaceutics_and_Pharmacokinetics_PT312.md  — the finished book (14 chapters, ~48,000 words)
- rubric.json      — the six scoring pillars, their weights and band anchors
- brief.json       — what this edition was commissioned to be
- rework/errata-ledger.md — the corrections this edition claims to have made
- rework/glossary.md
- evaluation/findings.json — the 39 findings against the FIRST edition, which this rework was meant to fix
- ingest/normalized.md — the first edition, if you need to check what it actually said

Your job is to find what is WRONG WITH THE NEW BOOK. Be adversarial and specific. In particular:

1. Mathematical and unit accuracy. Recompute every worked example and every exercise solution
   independently. Check that units are carried correctly and that stated answers follow from the
   stated inputs. Flag any answer you cannot reproduce.
2. Content accuracy. Any statement that is factually wrong, any definition that is wrong, any
   regulatory figure that does not match current ICH/EDA/USP guidance, any claim a cited reference
   does not support.
3. Whether the 39 first-edition findings were actually fixed, or only claimed to be fixed in the
   errata ledger. Spot-check the ledger's claims against the chapter text.
4. Assessment quality: are the MCQ answer keys correct? Does the stated rationale actually justify
   the keyed option? Are any distractors also defensible as correct?
5. Internal consistency: the same quantity given two different values in two chapters,
   cross-references that point to the wrong place, symbols redefined between chapters.

Output ONLY a markdown table with these columns, then a short Notes section:

| ID | severity | location | finding | why it matters | suggested fix |

Use IDs C-001, C-002, ... Severity is blocker, major or minor. Location must be a chapter and section
or a quoted phrase precise enough to find without searching. Do not report style preferences.
Do not report anything you have not verified against the text.
Before the table, print three lines:
verdict: pass or fail
open_blocker_major: <count>
reviewer_model: <the model you are>
