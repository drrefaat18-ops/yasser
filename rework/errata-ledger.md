# Errata Ledger

Every error found in the original review (`SESSION_SUMMARY.md` §3) is tracked here. Status: `open` → `fixed` (with chapter/section) or `removed-with-content` (topic dropped from the rework).

## Content errors

| # | Topic | Original line(s) | Correct statement | Target | Status |
|---|---|---|---|---|---|
| 1 | k-space undersampling | 164 | Undersampling produces aliasing; networks suppress it with incoherent sampling plus a learned prior; missing data is inferred, not recovered | Ch6 | open |
| 2 | Fast-MRI time saving | 170 | 25→5 and 40→10 min = 75–80% reduction | Ch6 | open |
| 3 | Breast-screening trial claim | 59 | Cite MASAI (Lång 2023): 44% screen-reading workload reduction; ~20% more cancers detected; recall not reduced | Ch1, Ch4, Ch6 | open |
| 4 | Softmax output as "confidence"/probability | 256, 559, 2563 | Model score is not a calibrated probability or statistical confidence | Ch4 | fixed (Ch4 §4.4) |
| 5 | Stroke infarct core | 1534, 1546, 1682, 1826, 1834, 1836 | rCBF < 30% (not CBV) | Ch6 (one-line mention at most) | open |
| 6 | Delta-check creatinine rise | 611 | IV-line contamination dilutes (lowers) analytes; false rise = wrong patient, mislabel, interference; alert goes to technologist and requesting clinician | Ch6 | open |
| 7 | ICG shows ureters | 1306 | ICG is excreted by the liver into bile; it does not show ureters | — | removed-with-content |
| 8 | AML ≥20% blasts | Ch3 Q6 | WHO 5th ed. (2022) removed the 20% threshold for AML with defining genetic abnormalities; ICC uses ≥10% | — | removed-with-content |
| 9 | Physiological tremor frequency | 1010, Q17 | 8–12 Hz | Ch8 | open |
| 10 | ML superior to logistic regression | 1107, 1418 | No average performance benefit in clinical prediction (Christodoulou 2019) | Ch3 | fixed (Ch3 §3.5) |
| 11 | AKI prediction (Tomašev 2019) | 2083 | Cohort 93.6% male (US veterans); about two false alerts per true alert | Ch9 | open |
| 12 | STAR robot superiority | 1074, 1264 | Pre-clinical animal study, small numbers, single lab | Ch8 | open |
| 13 | Data leakage definition | 2643 | Leakage = information from test data or the future contaminating training, not a privacy problem | Ch3 | fixed (Ch3 §3.4) |
| 14 | Learned intermediary doctrine | 2500, 2695, 2709 | Product-liability doctrine: manufacturer discharges its duty to warn by warning the clinician; it does not shield clinicians | Ch11 | open |
| 15 | §7.4.3 lesson from Obermeyer | 2599 | Algorithm was already race-blind; bias came from cost used as a proxy label → fix the label, "blindness" does not remove bias | Ch10 | open |
| 16 | Differential privacy as absolute | Ch7 | Bounded, tunable guarantee controlled by ε; not absolute | Ch10 | open |
| 17 | XAI as cure for the black box | §7.3 | Saliency maps show where a model looked, not whether its reasoning is valid (Adebayo 2018) | Ch11 | open |
| 18 | "master–slave" terminology | 1004 | "leader–follower" | Ch8 | open |
| 19 | WSI file size | 618 | ~30 GB uncompressed for 100,000 × 100,000 RGB; 1–3 GB after compression | Ch6 | open |
| 20 | ASC-US | 659 | "Atypical squamous cells of undetermined significance" — not a diagnosis of dysplasia; managed by reflex HPV testing | — | removed-with-content |
| 21 | S. pneumoniae morphology | 690 | Lancet-shaped diplococci, not chains | — | removed-with-content |
| 22 | 7 DOF comparison | 1014 | 7 DOF counted across the whole instrument; compare with 4 DOF of a rigid laparoscopic tool | Ch8 (if mentioned) | open |
| 23 | Haptic virtual fixtures at skull base | 1025 | Established in orthopaedics (e.g., knee/hip robots), not licensed for skull-base boundaries | Ch8 (if mentioned) | open |
| 24 | AR navigation "sub-millimetre" | 1090 | Brain shift of 10–20 mm after dural opening limits navigation accuracy | — | removed-with-content |
| 25 | JPEG artefacts called adversarial | 256 | Adversarial perturbations are crafted against a model; compression artefacts are distribution shift | Ch3 | fixed (Ch3 §3.4) |
| 26 | FFR-CT described as PINN | Ch5 | Licensed FFR-CT uses conventional computational fluid dynamics | — | removed-with-content |
| 27 | TAVR cusp-overlap / circular annulus | 1562 | Topic dropped | — | removed-with-content |
| 28 | CVS includes common bile duct | 1049 | Topic dropped (CVS requires only two structures entering the gallbladder; CBD not dissected) | — | removed-with-content |
| 29 | "70% of clinical decisions rely on lab results" | 587 | No primary evidence (Hallworth 2011) — do not repeat | Ch6 | open |
| 30 | GDPR "right to explanation" as settled law | 2531 | Contested (Wachter 2017) | Ch10 | open |
| 31 | McKinney 2020 as settled | Ref 6 | Cite with Haibe-Kains 2020 reproducibility critique | Ch6 | open |
| 32 | PINN for MRI reconstruction | 164, 1086 | Clinical reconstruction uses physics-informed unrolled networks (variational networks, MoDL), not PINNs | Ch6 (if mentioned) | open |
| 33 | "Randomized trials proved…" without naming trials | 4 places | Name the trial and cite it, or remove the claim | All | open |
| 34 | AI "sees through" overlapping structures | 549 | A CNN reading the same 2D projection has no extra physical information; it learns statistical cues | Ch6 | open |

## Figures

| Image | Decision | Reason | Used as |
|---|---|---|---|
| image1 (cover) | drop | AI-generated with hallucinated text | replaced by `figures/cover.svg` |
| image2 | keep (title cropped) | Correct hierarchy; baked "Figure 1.1" removed | `figures/orig-image2.png`, Ch1 |
| image3 | drop | Internally inconsistent ("segmental" vs "right main"); physician-only topic | — |
| image4 | drop | Radiomics out of year-1 scope | — |
| image5 | keep (title cropped) | WSI pipeline correct | `figures/orig-image5.png`, Ch6 |
| image6 | drop | CVS depiction unsafe | — |
| image7 | drop | States "sub-millimeter precision" (brain shift ignored) | — |
| image8 | drop | Orphan, mislabelled | — |
| image9, 10, 12, 13 | drop | Topics removed (IVUS, FFR-CT, TAVR, EVAR) | — |
| image11 | drop | Encodes the CBV < 30% error | — |
| image14 | keep | Schematic, labelled; no error | `../images/image14.png`, Ch9 |
| image15 | keep | Caption must state the "confidence" is an uncalibrated score and lesions shown are on light skin | `../images/image15.png`, Ch6 |
| image16 | drop | Overlapping, unreadable labels | — |
| image17 | keep (title cropped) | Digital pathology heatmap | `figures/orig-image17.png`, Ch6 |
| image18 | keep (title cropped) | Closed-loop insulin | `figures/orig-image18.png`, Ch9 |
| image19 | keep (title cropped) | Oculomics; caption must say "research use" | `figures/orig-image19.png`, Ch6 |
| image20 | drop | Invented values; physicians' specialties only | — |
| image21 | keep (title + footer cropped) | Footer stated the inverted learned-intermediary doctrine — removed | `figures/orig-image21.png`, Ch11 |
| image22 | drop | Conflates HIPAA Safe Harbor with anonymisation | replaced by `figures/privacy-pipeline.svg`, Ch10 |
| image23 | drop | Overclaims XAI ("clinically verifiable rationale"); overlapping boxes | — |
| image24 | keep (title cropped) | SaMD lifecycle; caption must mention PCCP | `figures/orig-image24.png`, Ch11 |

## Rulings

- Ruling: figures with baked-in old numbers are cropped rather than re-numbered in the caption only — mismatched numbers confuse students — cost if wrong: re-run crop script.
- Ruling: image20, image22, image23, image3 dropped although spec §9 listed them as "keep" — visual check found errors the spec did not know about — cost if wrong: one fewer figure in Ch6/Ch10/Ch11.
