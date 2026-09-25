---
type: interface-contract
step: 2
status: pending-codex-review (STEP 3)
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

`translation_required` is true exactly when `language.source ≠ language.output` (core §4.6 rule 2). Supported pairs: `en→ar`, `ar→en`. Any other pair is refused by `complete intake` with `TR-PAIR-UNSUPPORTED`.

---

## 2. Position in the stage graph (EXT-TR-1)

```text
new → intake ─(intake approval)→ ingest → evaluate → design ─(design approval, incl. termbase)→ translate → rework → build → audit
```

| Decision | Reason |
|---|---|
| **Evaluate runs on the original source**, before any translation. | Findings describe the author's book, not translation artefacts. |
| **Translate runs after design approval.** | Design decides which source material survives (`chapter-plan.json` → `chapters[].source_refs[]`); only those units are translated, so dropped material costs nothing. |
| **Translate is a faithful translation, not a rewrite.** | A faithful unit can be checked against its source unit one to one, which makes the review gate well defined. |
| **Rework runs in the output language** on the translated units, and writes new material directly in that language. | The final text is written once, checked once with the output-language profile, and fixed once after audit. |

**Stage row** (added to the core contract table, core §2.2):

| Field | Value |
|---|---|
| Kind | agentic, unit-based (like `rework`) |
| Inputs (hashed) | `design/*` approved artifacts, `termbase.json`, `ingest/normalized.md`, `ingest/units.json`, `brief.json` |
| Outputs (hashed) | `translation/<unit-id>.md` (one per translated unit), `translation/check-report.json`, `translation/codex-review.md`, `translation/fixes.md`, `trace/source-target-map.json` (translation half), `termbase-additions.json` |
| Extra receipt fields | `pair` (`en-ar` or `ar-en`), `units[]` (per-unit input/output hashes), `author_model`, `reviewer_model` |
| Preconditions | design approval valid (it covers `termbase.json`); `goal.mode = evaluate_and_rework`; `translation_required = true` |
| Invalidates | rework and every later stage |
| Failure and resume | per-unit: `complete translate --unit <unit-id>` writes a unit receipt after the automated checks (§5) pass for that unit; `begin translate` lists units missing or stale. The stage receipt needs every unit valid, the one Codex review saved, and every blocker/major review finding closed in `fixes.md`. |
| QA evidence | `check-report.json` with zero failing checks; review header; fixes table; reviewer ≠ author (§6) |

`rework` gains inputs `translation/*.md` and `trace/source-target-map.json` when translation applies.

---

## 3. Bilingual termbase (EXT-TR-2)

### 3.1 Files

| File | Approval | Written by |
|---|---|---|
| `projects/<p>/termbase.json` | part of the **design** approval set (core §3, `APPROVAL_SETS.design`) | Claude in the `design` stage, from `brief.language.terminology`, the evaluation, and term extraction over the units named in `chapter-plan.json` |
| `projects/<p>/termbase-additions.json` | not approval-gated | appended by `translate` and `rework` when a new term appears |

Editing `termbase.json` after approval re-opens the design approval, like any covered file. New terms go to the additions file instead, so work is not blocked mid-stage.

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

Additions use the same entry schema plus `status: proposed, accepted or rejected` and `first_seen {unit_id}`.

### 3.3 When the termbase is approved

- `termbase.json`: with the design, in one user approval (no new approval kind; core §3 keeps exactly two).
- `termbase-additions.json`: `complete audit` refuses while any addition is still `proposed`. The user accepts or rejects additions in chat; Claude records the batch in `decisions.md` with a DEC ID and sets each status. Accepted additions are checked for consistency like approved entries from the moment they are accepted.

---

## 4. Traceability (EXT-TR-3)

### 4.1 Source units

`ingest` writes `ingest/units.json` (schema `units.v1`, core EXT-TR-3): `units[] {id, heading, level, line_start, line_end, sha256}`. IDs are `src-chNN` for chapters and `src-chNN-sMM` for H2 sections, numbered in document order. `normalized.md` itself is not modified. `chapter-plan.json` `chapters[].source_refs[]` cites these IDs.

### 4.2 Map `trace/source-target-map.json` (schema `trace.v1`)

| Field | Notes |
|---|---|
| `schema_version`, `pair` | |
| `entries[]` | `{source_unit, source_sha256, translation_unit, translation_sha256, target_chapter_id, target_section_ids[], relation}` |
| `relation` | `translated`, `adapted`, `merged`, `split`, `dropped`, `new` |

- `translate` fills `source_unit`, `source_sha256`, `translation_unit`, `translation_sha256`.
- `rework` fills `target_chapter_id`, `target_section_ids[]` and `relation`.
- `dropped` entries need the design reason (`chapter-plan.json` names the unit under `dropped[]`); `new` entries have no source unit.

### 4.3 Traceability checks

| ID | Fails when |
|---|---|
| `TR-UNIT-MISSING` | a unit in `source_refs[]` has no translation unit |
| `TR-UNIT-STALE` | a recorded `source_sha256` or `translation_sha256` no longer matches |
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

The final reworked text is later covered by the independent audit (core §2.2), which checks meaning against the source through the trace map.

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
| `termbase.json` in the design approval set; `termbase.v1`; `termbase-additions.json` and its audit rule | EXT-TR-2 |
| `ingest/units.json` (`units.v1`); `trace/source-target-map.json` (`trace.v1`); `chapter-plan.json` `source_refs[]` and `dropped[]`; `TR-UNIT-*`, `TR-ORPHAN`, `TR-TARGET-UNMAPPED` | EXT-TR-3 |
| `author_model`, `reviewer_model`; `TR-REVIEW-*`; review file and fixes file | EXT-TR-4 |
| per-language processing in §5 and §7; `TB-*` normalised matching; digit rules | EXT-LOC-1 |
| reference handling in §7 | EXT-LOC-4 |
| `TR-PAIR-UNSUPPORTED` | EXT-TR-1 (validated by `complete intake`) |

---

## 9. Acceptance criteria (STEP 11)

Two fixture projects: `tests/fixtures/translation/en-ar/` and `tests/fixtures/translation/ar-en/`. Each holds a small source (two chapters, at least four H2 units, one table, one figure reference, one DOI reference, one formula or SMILES string, one `dnt` term, one `gloss_first_use` term), its `termbase.json`, `units.json`, translated units, a trace map and a stored review file.

| # | Criterion | Literal expectation |
|---|---|---|
| 1 | **termbase consistency** | the good fixture reports zero `TB-*` failures; mutations: remove a required target term → `TB-TERM-MISSING`; insert a forbidden variant → `TB-FORBIDDEN-VARIANT`; alter a `dnt` string → `TB-DNT-ALTERED`; drop a first-use gloss → `TB-GLOSS-MISSING` |
| 2 | **traceability** | good fixture passes; delete a translation unit → `TR-UNIT-MISSING`; edit a source unit after translating → `TR-UNIT-STALE`; add an unmapped unit → `TR-ORPHAN` |
| 3 | **preservation of references and mixed script** | good fixture passes; change a citation number → `PRES-CITATION`; alter a DOI → `PRES-IDENTIFIER`; alter the formula or SMILES → `PRES-PROTECTED` |
| 4 | **review by a different model** | `complete translate` on a fixture state with `reviewer_model = author_model` exits non-zero with `TR-REVIEW-SAME-MODEL`; with the review file absent, `TR-REVIEW-MISSING`; with an open major finding, `TR-REVIEW-OPEN` |
| 5 | **both directions** | criteria 1–4 pass for **both** `en-ar` and `ar-en` |

The test runner exits 0 while each mutation yields its named ID and a non-zero checker exit (core §9.3 convention). STEP 11 also requires one real Codex review of each fixture's translation and that the user has seen both outputs (ticket STEP 11).
