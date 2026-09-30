# Confirmation and rescore of commit 2dbaa01 — biopharmaceutics-pharmacokinetics

reviewed_commit: 2dbaa01

This is a read-only review by claude-sonnet-5-5 (DEC-010) of the round-5 fixes, with an independent rescore against rubric.json. It is saved here in summary. Findings F-001 to F-003 were fixed in 918fc28; F-004 needed no action.

verdict: pass
open_blocker_major: 0
reviewer_model: claude-sonnet-5-5

| ID | severity | location | finding | why it matters | suggested fix |
|---|---|---|---|---|---|
| F-001 | minor | Ch4 and Ch9 answer keys | The C-015 fix left Ch4 and Ch9 with the same first four keys, C A D B. | This is the same cross-chapter predictability that C-015 was raised for. | Permute Ch9 Q1–4 again. |
| F-002 | minor | Ch3 LO3 | The objective still presented Du∞ as an output of the sigma-minus method. | It is slightly inconsistent with the corrected §3.4. | "Determine K and t½ … given Du∞, and check Du∞ against the intercept." |
| F-003 | minor | Ch3 Example 3.1 Step 3 | Du∞ = dose was taken by assuming fe = 1, a route §3.4 does not list. | The argument is circular. | State the route explicitly. |
| F-004 | minor | Ch12 barbiturate sentence | Nuance only: a barbiturate is only partly ionised in the intestine. | Nuance only. | No action needed. |

Notes (summary):
- All three majors of round 5 are resolved.
  - C-001: Du∞ is an input; Ke is obtainable from both methods; the new Q9 has exactly one defensible answer, D.
  - C-002: 107·e^(−4) = 1.96 (7.6% of 25.8), and 160·e^(−3.2) = 6.52 (25.3%).
  - C-003: no Kh remains anywhere in rework/ or in the build.
- C-004 to C-016 are all resolved. Every number in the diff recomputes.
- The key balance rules pass in all 14 chapters.
- Rescore: G1 8.5, G2 8.5, G3 8.5, G4 9, D1 9, D2 8.5.
