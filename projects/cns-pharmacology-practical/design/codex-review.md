# Design Codex review

reviewed_commit: ab01f05917df1bfc907f3bb0becc2f60f664942a
verdict: fail
open_blocker_major: 1
reviewer_model: GPT-5

## Findings

| ID | Severity (blocker/major/minor) | File:line | Problem | Concrete fix |
|---|---|---|---|---|
| D-01 | major | design/design.md:56 | The figure incorrectly places memantine’s NMDA target within a “cholinergic synapse”; NMDA receptors are glutamatergic. | Redesign this as two clearly separated panels: cholinergic transmission/AChE inhibition and glutamatergic NMDA-receptor antagonism by memantine. |
| D-02 | minor | design/design.md:116 | F-068 is not fully resolved: four uncertain brand transcriptions remain for user checking, while the design merely directs readers to the EDA rather than requiring verification before publication. | Verify every brand name and current dosage form against the EDA database; omit any product that cannot be confirmed. |
