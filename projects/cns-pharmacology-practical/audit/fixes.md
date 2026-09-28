# Audit fixes (Fix Protocol)

## Round 1 — Codex audit of commit 098cf0e (GPT-5, read-only; independent score 69.5)

Every finding was checked against the chapter text and a standard reference, its root cause was named, and siblings were hunted in all nine chapters. Verification: each chapter passed `complete rework --unit`, the book was rebuilt, and the fixed book was audited again (round 2).

| ID | severity | status | root cause | fix | siblings |
|---|---|---|---|---|---|
| A-01 | major | fixed + verified | Slide shorthand "dopamine inhibitory, ACh excitatory" kept in the disease summary | ch03 3.1 now explains D1 direct-pathway stimulation and D2 indirect-pathway inhibition, both facilitating movement, with ACh opposing | ch03 recap, Q1 and takeaways checked: they state only dopamine loss and ACh dominance, which is correct |
| A-02 | major | fixed + verified | Status-epilepticus timeline ordered thiamine before glucose | ch05 5.7: check and correct glucose at once; IV thiamine alongside when alcohol misuse or malnutrition is likely, never delaying glucose | ch05 Case 2 answer already says check glucose first; ch07 alcohol case now also gives thiamine |
| A-03 | major | fixed + verified | Case 2 asked for withdrawal treatment in a patient who was only intoxicated | ch07 Case 2 now adds withdrawal signs on day 2 and asks why benzodiazepines are not given while intoxicated; model answer: airway and monitoring first, monitored benzodiazepine regimen when withdrawal appears, thiamine | ch07 Caution box on benzodiazepines with alcohol is consistent |
| A-04 | minor | fixed + verified | Case copied a disinhibited presentation that suggests frontotemporal dementia | ch01 Case 1 now describes two years of progressive episodic memory loss | none |
| A-05 | major | fixed + verified | Approved brand list (DEC-002) had no names for epilepsy, so the promised section was dropped | User extended the list (DEC-008); ch05 5.8 Brands in Egypt added with EDA note | A-06, A-07 |
| A-06 | major | fixed + verified | Same as A-05 for general anaesthetics | ch08 8.6 Brands in Egypt (Diprivan, Ketalar, Dormicum, named on the slides) | A-05, A-07 |
| A-07 | major | fixed + verified | Same as A-05 for local anaesthetics | ch09 9.7 Brands in Egypt (Xylocaine, Marcaine) | A-05, A-06 |
| A-08 | minor | fixed + verified | Outdated absolute ban on adrenaline in digits | ch09 Caution rewritten to current evidence (dilute adrenaline safe with normal circulation; avoid in poor circulation and the penis), cited [4]; Table 9.5, takeaway and Q6 with its rationale rewritten to match | ch09 Q6 key was built on the old rule and was fixed with it |
| A-09 | minor | fixed + verified | Partial agonists described as lower in all EPS | ch02 now says lower parkinsonism, prolactin and weight gain; akathisia common | ch02 comparison table checked |
