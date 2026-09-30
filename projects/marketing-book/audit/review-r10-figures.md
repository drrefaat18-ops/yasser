# Figure review of commit f864a2f — marketing-book

reviewed_commit: f864a2f

This read-only review by claude-sonnet-5-5 (DEC-003) covered the 16 figures added after the audit closed at dc10263: 9 diagrams, 3 illustrations and 4 photographs. The reviewer looked at every rendered image, checked it against the chapter text, recomputed the numbers, and checked captions, alt text, citations, credits and licences. This file is a summary; its findings were fixed in 617931f and 2ba249a.

verdict: fail
open_blocker_major: 1
reviewer_model: claude-sonnet-5-5

| ID | severity | location | finding | why it matters | suggested fix |
|---|---|---|---|---|---|
| C-001 | major | Figure 4.3, ch04-blueprint | Back-stage "Labels tube" and "Transports" sat under "Registers" and "Waits", before "Gives sample". Read as a timeline, the tube was labelled before the blood was drawn. | Labelling a tube before collection is a known patient-safety error, and it sat in the very fail point the figure teaches. | Put labelling at sampling, and transport and analysis after it. |
| C-002 | minor | Figure 6.2 caption, ch06-pet-mri | The caption's claims about PET-MRI cost, availability and growth are not in the text. | An unsupported claim. | Shorten the caption or cite a source. |
| C-003 | minor | ch06-pet-mri photograph | A clothed patient with a belt and boots lies in the MRI scanner. | It shows imaging students poor MRI safety practice. | Replace the photograph. |
| C-004 | minor | Figure 8.2, ch08-cold-chain | "2–8 °C" is shown unhedged, and the text gives no temperature. | It reads as a rule for all reagents. | Hedge the label and add the range to the text. |
| C-005 | minor | Figure 7.1, ch07-break-even | The "Expected 500" label is struck through by its line. | Legibility. | Move the label. |
| C-006 | minor | Figure 4.2, ch04-ct-room; photo provenance | The caption overclaims ("clear safety signs", "working equipment"), and no source URLs are recorded for the photographs. | The licences cannot be checked later. | Describe only what is visible, and record the source pages. |
| C-007 | minor | Figure 2.2, ch02-demand-elasticity | Steepness is used as a picture of elasticity. | It may teach "steep means inelastic" as a rule. | Add a note on axis scales. |
| C-008 | minor | Figure 8.3, ch08-pharmacy-counter | A US example, not noted as such. | The context is not Egyptian. | Optionally note it. |

The confirmation of 617931f passed with 0 blocker or major findings. It found one minor point, R-001: the CT-room photo licence in figures.json was CC0 while photo-sources.md said public domain.
