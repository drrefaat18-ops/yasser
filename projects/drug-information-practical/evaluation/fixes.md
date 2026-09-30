# Evaluation fixes (Fix Protocol)

Review: `codex-review.md` (GPT-5 Codex, read-only, reviewed commit ad970bf). Each finding was checked against the source text and a standard reference, its root cause named and siblings hunted. Verification: intake re-run and re-approved (DEC-002); `findings.json`, `scorecard.json` and `report.md` regenerated; `complete evaluate` runs the schema, cap and total checks.

| ID | severity | status | root cause | fix | siblings |
|---|---|---|---|---|---|
| E-01 | major | fixed + verified | Rubric copied from another book; domain anchors kept its pharmacology wording | D1-D3 anchors rewritten for drug information practice, research methods and pharmacovigilance; intake amended and re-approved (DEC-002); scorecard rescored against the new anchors | Other rubric pillars (G1-G4) are domain-free core anchors; checked, unchanged |
| E-02 | major | fixed + verified | Scores set before the missed errors were counted | G1 5 -> 3 (1-3 band: frequent errors), D3 4 -> 3 (important parts wrong); total 35.0 -> 30.0 | D1, D2 re-checked against new anchors: 4 stays (source tier missing, core concepts wrong) |
| E-03 | major | fixed + verified | Source-tier review checked the tertiary list only | Added F-042 (D1 major, lines 209-238): PMC is a full-text archive | F-004 (tertiary online list) is the sibling; kept separate |
| E-04 | major | fixed + verified | Severity scale taken at face value from the slides | Added F-044 (D3 major, safety): severity vs seriousness | Sibling: 'Moderate/Mild' definitions in the same list covered by the same finding |
| E-05 | major | fixed + verified | Management steps read as complete | Added F-045 (D3 major, safety): immediate patient care missing | F-039 (reporting route) is the next step; kept separate |
| E-06 | major | fixed + verified | ADR 'causes' slide not reviewed against the ADR/medication-error distinction | Added F-040 (G1 major, lines 692-698) | Sibling: prescriber risk factors (lines 719-725) mix error and ADR types; covered by F-014 (type scheme) and F-040 |
| E-07 | minor | fixed + verified | Definition not checked against WHO | Added F-046 (D3 minor) | none |
| E-08 | minor | fixed + verified | Eligibility slide missed | Added F-041 (G1 minor, lines 410-418) | none |
| E-09 | minor | fixed + verified | Replaced one universal limit with another | F-013 reworded: limit is journal-specific | none |
| E-10 | minor | fixed + verified | CONSORT 2010 cited from memory; superseded by CONSORT 2025 | All CONSORT sources in findings now cite CONSORT 2025 (BMJ 2025;389:e081123) | brief style note lists CONSORT without a year; the rework cites 2025 and SPIRIT 2025 |
| E-11 | minor | fixed + verified | Severity over-graded | F-036 (Type D) downgraded to minor | none |
| E-12 | minor | fixed + verified | Rule of three misstated | F-015 claim and fix hint corrected (zero-event upper bound, Hanley 1983) | none |
| E-13 | minor | fixed + verified | Search order taken as a rule | Added F-043 (D1 minor, lines 120-124) | none |
| E-14 | minor | fixed + verified | Report praised ADR steps before E-04/E-05 were found | Report strengths line changed; main problems now lead with the ADR safety defects | none |
