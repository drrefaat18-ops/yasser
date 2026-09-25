---
type: interface-contract
step: 2
status: amended after STEP 3 Codex review (fixes in docs/harness/reviews/step3-fixes.md); final approval pending
date: 2026-09-25
core_spec: docs/superpowers/specs/2026-09-25-book-harness-core-design.md (approved at 0284376, DEC-031; amended in the STEP 2 commit as allowed by the ticket)
companion: docs/superpowers/specs/2026-09-25-arabic-locale-contract.md
binding: docs/harness/VISION.md
---

# Translation — Interface Contract

This contract defines how a book whose source language differs from its output language moves through the harness, in **both directions, English→Arabic and Arabic→English** (DEC-007, DEC-019). It fixes **interfaces, schemas and acceptance criteria only**. Implementation is STEP 11.

Every field maps to a named core extension point (core spec §11): **EXT-TR-1** stage slot, **EXT-TR-2** termbase and approval set, **EXT-TR-3** traceability units, **EXT-TR-4** independent review gate; locale-dependent processing uses **EXT-LOC-1**. The map is in §8.

CDR §5 (`docs/harness/codex-design-review-2026-09-25.md:287`) is the requirement: "a pair of language fields alone does not provide translation support"; translation needs an explicit policy, bilingual terminology and a translation-review gate.

---

## 1. When translation applies

| `goal.mode` | `language.translation_required` | Effect |
|---|---|---|
| `evaluate_only` | false | no translation |
| `evaluate_only` | true | no book translation; the evaluation report (`evaluation/report.md`) is written in `language.output` while findings keep source-language quotes |
| `evaluate_and_rework` | false | no translation |
| `evaluate_and_rework` | true | the `translate` stage joins the mandatory set (§2) |

`translation_required` is true exactly when the **primary language subtags** of `language.source` and `language.output` differ (core §4.6 rule 2). Regions play no part here: `ar-EG → ar` and `en-GB → en-US` are not translation. Supported pairs, by primary subtag: `en→ar` and `ar→en`. Any other pair of different subtags is refused by `complete intake` with `TR-PAIR-UNSUPPORTED`. `pair` values below use primary subtags (`en-ar`, `ar-en`).

---

## 2. Position in the stage graph (EXT-TR-1)

```text
new → intake ─(intake approval)→ ingest → evaluate → design ─(design approval, incl. termbase)→ translate → rework → build → audit
```

| Decision | Reason |
|---|---|
| **Evaluate runs on the original source**, before any translation. | Findings describe the author's book, not translation artefacts. |
| **Translate is the first step of vision phase 4 (Rewrite)**, not a new phase (core §2.1 phase map). | The vision fixes six phases and requires translation; translation belongs to rewriting the book. |
| **Translate runs after design approval.** | Design decides which source material survives (`chapter-plan.json` → `chapters[].source_refs[]`); only those units are translated, so dropped material costs nothing. |
| **Translate is a faithful translation, not a rewrite.** | A faithful unit can be checked against its source unit one to one, which makes the review gate well defined. |
| **Rework runs in the output language** on the translated units, and writes new material directly in that language. | The final text is written once, checked once with the output-language profile, and fixed once after audit. |

**Stage row** (added to the core contract table, core §2.2):

| Field | Value |
|---|---|
| Kind | agentic, unit-based (like `rework`) |
| Inputs (hashed) | `design/*` approved artifacts, `termbase.json`, `ingest/normalized.md`, `ingest/units.json`, `brief.json` |
| Outputs (hashed) | `translation/<unit-id>.md` (one per translated unit), `translation/check-report.json`, `translation/codex-review.md`, `translation/fixes.md`, `trace/translation-map.json` (`trace.v1`, `kind: translation`), `terms/translate-proposals.json`. No later stage edits any of them (core §2.3, one owner per file). |
| Extra receipt fields | `pair` (`en-ar` or `ar-en`), `units[]` (per-unit input/output hashes), `author_model`, `reviewer_model` |
| Preconditions | core `require_gates` (intake approval and design approval valid; the design approval covers `termbase.json`); design receipt valid; `goal.mode = evaluate_and_rework`; `translation_required = true` |
| Invalidates | rework and every later stage |
| Failure and resume | per-unit: `complete translate --unit <unit-id>` writes a unit receipt after the automated checks (§5) pass for that unit; `begin translate` lists units missing or stale. The stage receipt needs every unit valid, the one Codex review saved, and every blocker/major review finding closed in `fixes.md`. |
| QA evidence | `check-report.json` with zero failing checks; review header; fixes table; reviewer ≠ author (§6) |

When translation applies, `rework` gains the inputs `translation/*.md`, `trace/translation-map.json`, `termbase.json` and `termbase-additions.json`, and the outputs `trace/source-target-map.json` (`kind: final`) and `terms/rework-proposals.json` (core §2.2).

---

## 3. Bilingual termbase (EXT-TR-2)

### 3.1 Files

| File | Approval | Written by |
|---|---|---|
| `projects/<p>/termbase.json` | part of the **design** approval set (core §3, `APPROVAL_SETS.design`) | Claude in the `design` stage, from `brief.language.terminology`, the evaluation, and term extraction over the units named in `chapter-plan.json` |
| `projects/<p>/terms/translate-proposals.json`, `terms/rework-proposals.json` | not approval-gated; hashed outputs of their stage | written by `translate` and `rework` respectively when a new term appears; never edited by another stage |
| `projects/<p>/termbase-additions.json` | resolution record, bound to a DEC row hash | written only by `run_stage.py --project P terms resolve --dec DEC-NNN` (§3.3); hashed input of `rework` and `audit` |

Editing `termbase.json` after approval re-opens the design approval, like any covered file. New terms go to a proposals file instead, so work is not blocked mid-stage.

### 3.2 Schema `termbase.v1`

| Field | Notes |
|---|---|
| `schema_version` | 1 |
| `pair` | `en-ar` or `ar-en` |
| `transliteration` | policy for names: `as-in-source`, `ala-lc` or `simplified` |
| `entries[]` | see below |

Entry fields:

| Field | Notes |
|---|---|
| `id` | `T-NNNN`, stable |
| `kind` | `term`, `name`, `abbreviation`, `dnt` (do not translate: gene symbols, product names, SMILES, units) |
| `source` | source-language form |
| `target` | required target-language form (for `dnt`, equals `source`) |
| `allowed_variants[]` | other acceptable target forms (e.g. grammatical forms the matcher's normalisation does not cover) |
| `forbidden_variants[]` | target forms that must not appear |
| `gloss_first_use` | bool; when true, the first use in each chapter shows the source term in parentheses, e.g. `التعلم الآلي (machine learning)`; this links to the Arabic glossary `gloss` (Arabic contract §4) |
| `note` | domain note for the translator and reviewer |

**Proposal form** (`terms/*-proposals.json`): the same entry schema plus `first_seen {unit_id}`. IDs are `P-T-NNNN` in translate proposals and `P-R-NNNN` in rework proposals, so no two stages can claim the same ID.

**Resolution form** (`termbase-additions.json`): `{schema_version, pair, resolutions[] {proposal_id, status: accepted or rejected, entry, dec_id, dec_row_sha256}}`. An accepted resolution's `entry` is the term as accepted, which may be edited from the proposal.

### 3.3 When the termbase is approved

- `termbase.json`: with the design, in one user approval (no new approval kind; core §3 keeps exactly two).
- Proposals: the user accepts or rejects them in chat. Claude records the batch in `decisions.md` with a DEC ID, then runs `terms resolve --dec DEC-NNN`, which writes the resolutions and the DEC row hash (core §3). A proposal with no resolution is **open**.
- `complete audit` refuses while any proposal in either proposals file is open (`TB-PROPOSAL-OPEN`).
- Accepted entries are checked like approved entries from then on.
- A rejected proposal's target form must not appear in the translated or reworked text (`TB-REJECTED-PRESENT`).
- Because `termbase-additions.json` is a rework input, resolving proposals makes the rework receipt stale. `complete rework` is re-run; if it proposes nothing new, the process converges in one pass.

---

## 4. Traceability (EXT-TR-3)

### 4.1 Source units

`ingest` writes `ingest/units.json` (schema `units.v1`, core EXT-TR-3): `units[] {id, heading, level, line_start, line_end, sha256}`. IDs are `src-chNN` for chapters and `src-chNN-sMM` for H2 sections, numbered in document order. `normalized.md` itself is not modified. `chapter-plan.json` `chapters[].source_refs[]` cites these IDs.

### 4.2 Maps `trace/translation-map.json` and `trace/source-target-map.json` (schema `trace.v1`)

| Field | Notes |
|---|---|
| `schema_version`, `pair` | |
| `kind` | `translation` (written by `translate` to `translation-map.json`) or `final` (written by `rework` to `source-target-map.json`) |
| `entries[]` | `{source_unit, source_sha256, translation_unit, translation_sha256, target_chapter_id, target_section_ids[], relation}` |
| `relation` | `translated`, `adapted`, `merged`, `split`, `dropped`, `new` |

- **`kind: translation`**: every entry requires `source_unit`, `source_sha256`, `translation_unit` and `translation_sha256`. The target fields and `relation` are forbidden.
- **`kind: final`**: every entry requires `relation`. For all relations except `new`, it also requires the four translation fields, copied from `translation-map.json`. For all relations except `dropped`, it requires `target_chapter_id` and `target_section_ids[]`. `rework` never edits `translation-map.json`.
- `dropped` entries need the design reason (`chapter-plan.json` names the unit under `dropped[]`); `new` entries have no source unit.

### 4.3 Traceability checks

| ID | Fails when |
|---|---|
| `TR-UNIT-MISSING` | a unit in `source_refs[]` has no translation unit |
| `TR-UNIT-STALE` | a recorded `source_sha256` or `translation_sha256` no longer matches, in either map, or the final map's copied hashes differ from `translation-map.json` |
| `TR-ORPHAN` | a translation unit has no source unit |
| `TR-TARGET-UNMAPPED` | (after rework) a target chapter has no entry, or a translated unit has no target chapter and is not `dropped` |

---

## 5. Automated translation checks

Run by `harness/tools/check_translation.py --project P [--unit ID]`, emitting `checker-report.v1` (core §9.3). Source text uses the source-language profile and target text the output-language profile (Arabic contract P3; core EXT-LOC-1). Term matching uses each profile's `normalisation.compare`.

| ID | Check | Fails when |
|---|---|---|
| `TB-TERM-MISSING` | termbase consistency | a unit's source contains an entry's `source` form but the target contains neither `target` nor an `allowed_variants` form |
| `TB-FORBIDDEN-VARIANT` | termbase consistency | a target contains a `forbidden_variants` form |
| `TB-DNT-ALTERED` | termbase consistency | a `dnt` entry is not reproduced verbatim |
| `TB-GLOSS-MISSING` | termbase consistency | an entry with `gloss_first_use` lacks the parenthesised source term at its first use in a chapter |
| `PRES-CITATION` | preservation of references | the set of citation numbers differs between source and target unit (after digit normalisation) |
| `PRES-IDENTIFIER` | preservation of references | the multiset of DOIs, URLs or e-mail addresses differs |
| `PRES-PROTECTED` | preservation of mixed script | protected spans (Arabic contract P4: formulas, SMILES/SMARTS, code, units, gene symbols) differ |
| `PRES-FIGURE` | preservation | figure or table references differ |
| `PRES-LATIN-TERM` | mixed script (en→ar) | a Latin term kept in the source-language form in the termbase (`dnt` or gloss) is missing from the target |
| `TB-REJECTED-PRESENT` | termbase resolution | the target form of a rejected proposal appears in a translated unit or reworked chapter |
| `TB-PROPOSAL-OPEN` | termbase resolution | a proposal has no resolution (checked by `complete audit`) |
| traceability IDs | §4.3 | as listed |

Numbers that are not in protected spans (e.g. "three" vs `3`) are listed in the report under `notes[]` for the reviewer, not failed, because spelled-out numbers change form legitimately between languages.

---

## 6. Translation review gate (EXT-TR-4)

- **One** review of the translation by a **different model** from the translator: Codex, read-only, through `codex-delegate` (DEC-017, DEC-030). The translator is Claude.
- Scope: every translated unit against its source unit, for accuracy, omissions, additions, terminology (against `termbase.json` and accepted additions), register for the audience in `brief.audience`, and the direction-specific rules in §7.
- The report is saved verbatim to `translation/codex-review.md` with header `reviewer_model`, `verdict`, `open_blocker_major`; findings cite `unit-id:line`.
- Claude resolves findings through the Fix Protocol into `translation/fixes.md` (`ID | real/rejected | root cause | siblings found | fix | verification → result`). No second review.
- `complete translate` fails with:
  - `TR-REVIEW-MISSING` if the review file is absent;
  - `TR-REVIEW-SAME-MODEL` if `reviewer_model = author_model` (core EXT-TR-4 check);
  - `TR-REVIEW-OPEN` if a blocker or major finding lacks a `fixed + verified`, `rejected` or `ruled by user` row.

The final reworked text is later covered by the independent audit (core §2.2). The audit checks meaning against the source through the final trace map. Every artifact it uses is a hashed audit input and is recorded in `codex_audited_inputs`: `ingest/normalized.md`, `ingest/units.json`, `translation/*.md`, `translation/check-report.json`, `trace/source-target-map.json`, `termbase.json` and `termbase-additions.json`. A change to any of them after the audit makes the audit receipt stale.

---

## 7. Direction-specific rules

| Rule | en→ar | ar→en |
|---|---|---|
| target locale profile | `ar` (Arabic contract §2) | `en` |
| digits in target | `digits.output` of the project (default `arabic-indic`); protected spans stay Western | Western |
| terms without an established target form | kept in English as `dnt` or given an Arabic form with `gloss_first_use` | translated; the Arabic form is not repeated unless the termbase says so |
| names | per `termbase.transliteration`; Arabic script in target | transliterated per `termbase.transliteration` (`ala-lc` default for scholarly books) |
| references | English references stay in their original form (Latin script); the entry is not translated | Arabic references keep the original Arabic title, followed by an English translation in square brackets and the note `[in Arabic]`; the reference policy mode is `original-language` with marker `[Original title: …]` (Arabic contract §5.2) |
| direction and theme | `theme.direction = rtl`, preset `rtl-textbook` | `theme.direction = ltr`, preset `ltr-textbook` |
| readability | Arabic calibrated thresholds (Arabic contract §2.1) apply to the reworked chapters | English thresholds |

---

## 8. Field → extension point map

| Contract field | Core extension point |
|---|---|
| `translate` stage, its position, mandatory-set condition, invalidation, receipt fields | EXT-TR-1 |
| `termbase.json` in the design approval set; `termbase.v1` (entry, proposal, resolution forms); `terms/*-proposals.json`; `termbase-additions.json`, `terms resolve`; `TB-PROPOSAL-OPEN`, `TB-REJECTED-PRESENT` | EXT-TR-2 |
| `ingest/units.json` (`units.v1`); `trace/translation-map.json` and `trace/source-target-map.json` (`trace.v1`, `kind`); `chapter-plan.json` `source_refs[]` and `dropped[]`; `TR-UNIT-*`, `TR-ORPHAN`, `TR-TARGET-UNMAPPED` | EXT-TR-3 |
| `author_model`, `reviewer_model`; `TR-REVIEW-*`; review file and fixes file | EXT-TR-4 |
| per-language processing in §5 and §7; `TB-*` normalised matching; digit rules | EXT-LOC-1 |
| reference handling in §7 | EXT-LOC-4 |
| `TR-PAIR-UNSUPPORTED` | EXT-TR-1 (validated by `complete intake`) |

---

## 9. Acceptance criteria (STEP 11)

Two fixture projects: `tests/fixtures/translation/en-ar/` and `tests/fixtures/translation/ar-en/`. Each holds a small source (two chapters, at least four H2 units, one table, one figure reference, one DOI reference, one formula or SMILES string, one `dnt` term, one `gloss_first_use` term), its `termbase.json`, `units.json`, translated units, both trace maps, a proposals file with one accepted and one rejected proposal plus its resolution record, and a stored review file. Tests run the real CLI on a copy of each fixture inside a temporary git repository (core §9.6); the immutable fixture is never passed to `--project` directly.

| # | Criterion | Literal expectation |
|---|---|---|
| 1 | **termbase consistency** | the good fixture reports zero `TB-*` failures; mutations: remove a required target term → `TB-TERM-MISSING`; insert a forbidden variant → `TB-FORBIDDEN-VARIANT`; alter a `dnt` string → `TB-DNT-ALTERED`; drop a first-use gloss → `TB-GLOSS-MISSING`; insert a rejected proposal's form → `TB-REJECTED-PRESENT`; remove the resolution of a proposal → `complete audit` exits non-zero with `TB-PROPOSAL-OPEN` |
| 2 | **traceability** | good fixture passes; delete a translation unit → `TR-UNIT-MISSING`; edit a source unit after translating → `TR-UNIT-STALE`; add an unmapped unit → `TR-ORPHAN` |
| 3 | **preservation of references and mixed script** | good fixture passes; change a citation number → `PRES-CITATION`; alter a DOI → `PRES-IDENTIFIER`; alter the formula or SMILES → `PRES-PROTECTED` |
| 4 | **review by a different model** | `complete translate` on a copied fixture state with `reviewer_model = author_model` exits non-zero with `TR-REVIEW-SAME-MODEL`; with the review file absent, `TR-REVIEW-MISSING`; with an open major finding, `TR-REVIEW-OPEN` |
| 5 | **both directions** | criteria 1–4 pass for **both** `en-ar` and `ar-en` |
| 6 | **language tags** | `complete intake` accepts `ar-EG → en-GB` as pair `ar-en`, treats `en-GB → en-US` as no translation, and refuses `fr → ar` with `TR-PAIR-UNSUPPORTED` |

The test runner exits 0 while each mutation yields its named ID and a non-zero checker exit (core §9.3 convention). STEP 11 also requires one real Codex review of each fixture's translation and that the user has seen both outputs (ticket STEP 11).
