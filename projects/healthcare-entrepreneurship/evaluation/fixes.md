# Fix Protocol — external review of the evaluate stage

Review: `evaluation/codex-review.md` (claude-sonnet-5-5 per DEC-002, verdict fail, 1 major, 14 minor), of commit
4a26675. Protocol: confirm each finding at its cited location, find the root cause, hunt siblings, fix, verify. All
15 were checked against `ingest/normalized.md` before any edit; none was accepted on the reviewer's word alone. The
reviewer's finding numbers refer to the pre-review `findings.json`; the fixes below use the post-review numbers.

| ID | status | real/rejected | root cause | siblings found | fix | verification → result |
|---|---|---|---|---|---|---|
| R-01 | fixed + verified | real, severity lowered to minor | I read the uncertainty-avoidance items only for their topic, not for the direction of the scale. "Tolerance for ambiguity" is the topic Hofstede (2011) names, so the T/F key is defensible as wording, but it reads as if a high score meant high tolerance. Q30's keyed option and its rationale point opposite ways. | Q30 (lines 422–428) and T/F 18 (lines 135–137). | Added F-029 (G1, minor). The report no longer says the Hofstede rationales are all correct. | Lines 135–137 and 427–428 re-read → ok |
| R-02 | fixed + verified | real | F-003 was scoped to the lecture text only. | Lines 118, 134, 228, 380, 399. | F-003's location now runs from line 92 to line 228, and its claim names the items. | Line 228 reads "one of the five dimensions" → ok |
| R-03 | fixed + verified | real | The report's wording described the 4–6 band. | — | G3 stays 3. The report now names the 1–3 anchor and its evidence: F-014 (no key) and F-029 (key contradicts rationale). | Anchors in rubric.json → ok |
| R-04 | fixed + verified | real | I wrote a combined share as a single-strategy score. | — | F-016: "87% of the keys are B or C; always answering B scores 47%". | 14/30 = 46.7%, 26/30 = 86.7% → ok |
| R-05 | fixed + verified | real | Imprecise evidence. | — | F-021 evidence cites lines 75 and 103–104. | Re-read → ok |
| R-06 | fixed + verified | real | Loose attribution. | — | F-001's fix hint now uses the opportunity-based view, "discovery, evaluation and exploitation". | Shane & Venkataraman (2000), p. 218 wording → ok |
| R-07 | fixed + verified | real | Missed. | — | Added F-031 (G3, minor). | "entreprendre" < Latin *inter* + *prehendere* → ok |
| R-08 | fixed + verified | real, with a correction | Missed. The reviewer's "Musk did not found Tesla" is itself too strong: under a 2009 settlement Musk may call himself a co-founder. The book states the founding by Eberhard and Tarpenning (2003) and Musk's role from 2004. | Line 438. | F-008's claim and fix hint name the founders exactly. | — → ok |
| R-09 | fixed + verified | real | Checked only one case item. | The other two case MCQs (Apple, Tesla) are recall of unsourced summaries. | Added F-032 (G3, minor). | Line 446 → ok |
| R-10 | fixed + verified | real | Treated the stages as process content, not as a model needing a source. | Q3 at line 182 and MCQ 5 at line 50. | Added F-030 (G1, minor). | — → ok |
| R-11 | fixed + verified | real | Under-counted. | Lines 255 and 447; lines 145–162. | F-012's span now runs from line 38 to line 447 and quotes all five artefacts. F-014 adds the five keyed MCQs without rationales. | Re-read → ok |
| R-12 | fixed + verified | real | Missed the duplicates; overstated T/F 12–15. | Pairs Q6/Q18, Q10/Q22, Q8/Q21, Q20/Q24. | Added F-033 (G3, minor). F-019 narrowed to items 13 and 15. | Re-read → ok |
| R-13 | fixed + verified | real | Inconsistent severity. | — | F-017 lowered to minor: the notes never define "startup", so the item is arguable rather than wrong. | — → ok |
| R-14 | partly fixed | partly rejected | The findings stand: the brief makes health applicability the purpose of the book, and the D1 1–3 anchor ("health is barely addressed") describes the notes exactly. They are not double-counted: F-011 is the missing process (G2), F-026 the missing tools (D2), F-022 the missing health content (D1). | — | The scores are unchanged. The report now says that D1 and D2 score the source as a base for the book, and gives each score's anchor. | — → ok |
| R-15 | fixed + verified | real | Unverifiable attribution; an overstated claim. | — | F-023 no longer attributes the lists. F-024 now reads "profit is the only aim in the two definitions", noting the social aims at lines 31 and 34. | Lines 7, 10, 31, 34 → ok |

## Rescoring

The added findings are minor and fall in G1 and G3, whose scores already sit in the bands they describe. No score
changes. Total recomputed: (5×20 + 2×20 + 3×10 + 1.5×10 + 1×20 + 2×20) / 10 = 24.5, matching `scorecard.json`.
Counts from `findings.json`: 33 findings, 1 blocker, 14 major, 18 minor, matching `report.md`.

## What the review taught the rework

Every keyed item reused from the source is re-derived from a cited definition, not copied (R-01). Every statement about
a founder is written from a cited source (R-08).
