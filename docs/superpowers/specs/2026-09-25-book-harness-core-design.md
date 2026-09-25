---
type: design-spec
step: 1
status: pending-user-approval
date: 2026-09-25
ticket: docs/harness/TICKET.md (approved at 23d819f, DEC-026)
binding: docs/harness/VISION.md
---

# Book Harness — Core Design Spec

This spec defines the **core** of the book harness: layout, stage contract, approvals, schemas, rubric core, agent overlays, figure system, evaluate stage, regression strategy, the hardcoded-value inventory mapping and the extension points that STEP 2 fills for Arabic and translation.

It is design only. It contains no code and creates no schema files. Every design choice below is either a user ruling (cited as DEC-NNN) or a design choice of this spec; the user approves the spec as a whole at the end of STEP 1.

**Sources read:** `docs/harness/VISION.md`, `docs/harness/DECISIONS.md`, `docs/harness/codex-design-review-2026-09-25.md` (cited as *CDR*), `docs/harness/reviews/ticket-review-1.md` (cited as *TR1*), `docs/superpowers/specs/2026-09-24-interprofessional-rework-design.md`, `docs/superpowers/plans/2026-09-24-interprofessional-rework.md`, `EVALUATION_RUBRIC.md`, `rework/tools/*.py`, `convert_docx_to_md.py`, `docs/harness/INTAKE_QUESTIONNAIRE.md`.

---

## 0. Principles carried from the rulings

| Principle | Source |
|---|---|
| One repo, one folder per book under `projects/<book>/`; shared tools and personas. | DEC-002 |
| Intake first; no stage after `intake` runs without a hash-matching user approval, enforced in code in every executable. | DEC-005, Rule 7 |
| A second user approval (design) gates `rework`. | Rule 7, TR1 blocker 2 |
| Rubric = fixed generic pillars + generated domain pillars, approved at intake, before evaluation. | DEC-003, CDR §1 |
| Shared code carries no domain literal; all of it comes from project config. | Rule 8 |
| Inline by default; ≤ 2 Claude subagents, each with a logged reason; Codex dispatches excluded. | DEC-014, DEC-015, Rule 11 |
| Control plane and checker: Python stdlib only. Conversion/build keep python-docx, Pillow, pywin32, Word. | Rule 10 |
| Figures from code; no paid image generation. | DEC-008, DEC-016 |
| Approach A: skills are thin wrappers over one Python stage runner that enforces gates. | DEC-011 (approved DEC-026) |

---

## 1. Layout (a)

```text
D:\yasser\
  CLAUDE.md                      # harness instructions (rewritten in STEP 7; medical copy moves to the project)
  harness/                       # shared, domain-free production code and data
    state.py                     # receipts, approvals, hashing, staleness, invalidation, locks
    run_stage.py                 # the one stage runner (CLI); every entry point routes through state.py
    preflight.py                 # dependency and environment probe
    defaults.json                # harness-level defaults (e.g. reference-provider settings)
    rubric_core.json             # fixed generic pillars (§5)
    schemas/                     # versioned JSON Schemas (§4)
      brief.v1.json  rubric.v1.json  template.v1.json  theme.v1.json
      chapter-plan.v1.json  overlay.v1.json  state.v1.json
      findings.v1.json  scorecard.v1.json  checker-report.v1.json
      source-manifest.v1.json  conversion-report.v1.json  figures.v1.json
      golden.v1.json  golden-diff.v1.json
    agents/                      # shared reviewer personas (domain-free), §6
    locale/                      # locale profiles, one file per language tag (§11)
      en.json
    presets/                     # tested theme presets (§4.4)
      ltr-textbook.json
      rtl-textbook.json          # STEP 10 (Arabic contract §3)
    tools/                       # generalised tools (STEP 8)
      convert_docx.py  check_book.py  assemble.py  build_book.py
      verify_refs.py  renumber_refs.py  capture_golden.py  compare_golden.py  leak_scan.py
      check_translation.py       # STEP 11 (translation contract §5)
    figures/                     # figure system (§7)
      render.py  check_figures.py  charts.py
      packs/
        chemistry/               # optional dependency group (RDKit), DEC-009
  .claude/skills/book-*/         # thin skill wrappers over run_stage.py (STEP 7)
  projects/
    <book>/                      # one per book; layout in §1.1
  tests/
    fixtures/
      ai-in-medicine/            # immutable golden fixture: golden.json + src/
      positive-config/           # books without MCQs / glossary / cases / lenses / errata
      mutations/                 # mutation definitions (§9.3)
      ingest/                    # DOCX fixtures with high-risk structures
      locale/<tag>/              # locale acceptance corpora (filled by STEP 2/10)
    test_*.py                    # stdlib unittest
  docs/harness/  docs/superpowers/
```

### 1.1 Project layout

```text
projects/<book>/
  brief.json  rubric.json  template.json  theme.json   # intake artifacts (approved together)
  agents/<overlay-id>.json                             # approved domain overlays (§6)
  state.json  state.lock                               # workflow state (§2.3); lock is transient
  decisions.md                                         # per-project DEC log (user words for each approval)
  source/                                              # custody copies of source files (read-only by convention)
  source-manifest.json
  ingest/        normalized.md  units.json  assets/  conversion-report.json
  evaluation/    findings.json  scorecard.json  report.md  codex-review.md  fixes.md
  design/        design.md  chapter-plan.json  errata-seed.md
  termbase.json  termbase-additions.json               # only when translation applies (translation contract §3)
  translation/   <unit-id>.md  check-report.json  codex-review.md  fixes.md   # only when translation applies
  trace/         source-target-map.json               # only when translation applies
  references-manual.json                              # manual reference verifications (Arabic contract §5.3)
  <chapters>/    front matter, chapter files, glossary, errata ledger   # dir name = template.paths.chapters
  figures/       figures.json  src/  out/
  build/         <basename>.md  <basename>.docx  <basename>.pdf  build-report.json
  audit/         findings.json  scorecard.json  codex-audit.md  fixes.md
```

Every path inside a project is resolved from `template.paths` (§4.3) relative to the project root. Defaults are the names above; a project may override them. The medical project keeps its historical layout (`rework/` chapters with `images/` beside it, STEP 6) by setting `template.paths.chapters = "rework"` and `template.paths.allowed_asset_roots = ["images", "rework/figures"]`.

**Asset model.** An image link in a chapter file is relative to that file. The assembler resolves each link to an absolute path, checks it lies under one of `template.paths.allowed_asset_roots`, then rewrites it relative to the output file with a path-relative computation. There is no string replacement of prefixes (fixes CDR §4 on `assemble.py:21-37`).

**Project selection.** Every executable requires `--project <path>`. The resolved path must be a direct child of `<repo>/projects/`, and its name must match `^[a-z0-9][a-z0-9-]{1,62}$`. No tool infers a default project (CDR §2).

---

## 2. Stage contract (b)

### 2.1 Stage graph

The graph is data in `state.py` (`STAGES`), not a hardcoded sequence, so STEP 2 can insert a stage (EXT-TR-1).

```text
new → intake ─(intake approval)→ ingest → evaluate → design ─(design approval)→ [translate] → rework → build → audit
```

**Mandatory stage set** depends on `brief.goal.mode`:

| `goal.mode` | Mandatory stages |
|---|---|
| `evaluate_only` | new, intake, ingest, evaluate |
| `evaluate_and_rework` | new, intake, ingest, evaluate, design, rework, build, audit |

When `brief.language.translation_required` is true **and** `goal.mode = evaluate_and_rework`, the `translate` stage joins the mandatory set between `design` and `rework` (EXT-TR-1; stage row in the translation contract §2). With `evaluate_only`, translation means only that the evaluation report is written in the output language.

**Stage kinds.**
- `auto` stages run fully in Python: `run_stage.py --project P run <stage>`.
- `agentic` stages are work Claude does in the session, bracketed by two runner calls: `begin <stage>` (checks gates, marks downstream invalid, prints the task brief and the required outputs) and `complete <stage>` (validates outputs against their schemas and QA rules, then writes the receipt). Nothing counts as done until `complete` exits 0.

### 2.2 Contract table

Receipt fields common to every stage are in §2.3; the table lists only stage-specific additions.

| Stage | Kind | Inputs (hashed) | Outputs (hashed) | Extra receipt fields | Preconditions | Invalidates | Failure and resume | QA evidence |
|---|---|---|---|---|---|---|---|---|
| `new` | auto | slug argument | `projects/<slug>/` skeleton, `state.json`, empty `decisions.md` | `slug` | slug matches pattern; directory does not exist | — | If it fails after creating the directory, it removes only what this invocation created. Re-run is safe. | `state.json` validates against `state.v1` |
| `intake` | agentic | `harness/rubric_core.json`, `harness/locale/<tag>.json`, `harness/presets/<preset>.json` | `brief.json`, `rubric.json`, `template.json`, `theme.json`, `agents/*.json` | `questionnaire_ids` (A–M answered) | `new` receipt ok | every later stage (through the intake approval hash) | `complete` fails with the list of schema and cross-file errors; files stay for editing; re-run `complete`. | schema validation of all five kinds; cross-file rules in §4.6; `brief.unresolved` is empty |
| `ingest` | auto | `brief.source.files[]` originals, `template.paths`, `template.ingest` | `source/*`, `source-manifest.json`, `ingest/normalized.md`, `ingest/units.json`, `ingest/assets/*`, `ingest/conversion-report.json` | `converter` (`docx-native` or `markitdown`), `source_formats` | intake approval valid | evaluate and everything after | Writes into `ingest/.tmp/` and swaps into place only on success; on failure the previous outputs stay and the receipt is `failed`. Exit 2 if a structure is `lost` (§2.4). | conversion-report counts per structure; custody hashes equal the originals |
| `evaluate` | agentic | `brief.json`, `rubric.json`, `agents/*.json`, `ingest/normalized.md`, `ingest/conversion-report.json` | `evaluation/findings.json`, `scorecard.json`, `report.md`, `codex-review.md`, `fixes.md` | `rubric_digest`, `personas[]`, `author_model`, `reviewer_model`, `subagents[]` (each with reason) | intake approval valid; ingest receipt valid | design and after | `complete` refuses while any blocker/major Codex finding lacks a `fixes.md` row with status `fixed + verified`, `rejected` or `ruled by user`. Re-run `complete` after fixing. | §8 checks; scorecard recomputed in code from rubric weights and must equal the file |
| `design` | agentic | `evaluation/*` outputs, `brief.json`, `template.json`, `theme.json` | `design/design.md`, `design/chapter-plan.json`, `design/errata-seed.md` | `chapter_count`, `total_budget` | evaluate receipt valid; `goal.mode = evaluate_and_rework` | rework and after (through the design approval hash) | Same as intake: `complete` lists errors; re-run. | `chapter-plan.v1` validation; budgets sum inside `template.budgets.total`; every evaluate blocker/major finding is mapped to a chapter or to `out-of-scope` with a reason |
| `rework` | agentic, unit-based | design artifacts, intake artifacts, `ingest/normalized.md` | chapter files, glossary, errata ledger, `figures/src/*`, `figures/figures.json` | `units[]`: one entry per chapter with its own input/output hashes, checker-report hash and `verify_refs` summary | design approval valid | build and after | **Per-chapter resume**: `complete rework --unit <chapter-id>` writes a unit receipt; `begin rework` lists units still missing or stale. The stage receipt is written by `complete rework` once every unit in `chapter-plan.json` is valid and the book-level checks pass. | per-unit checker JSON with zero failing checks; `verify_refs` with zero `NOT FOUND`/`TITLE MISMATCH`/`ERROR`/disallowed `NO DOI`; book-level checks (errata closed where enabled) |
| `build` | auto | rework outputs, `template.json`, `theme.json`, `design/chapter-plan.json`, `figures/*` | `figures/out/*`, `build/<basename>.md`, `.docx`, `.pdf`, `build-report.json` | `backend`, `page_count`, `bookmarks_count` | rework receipt valid; preflight for the build backend passes | audit | Renders figures, runs the figure checker, assembles, builds DOCX, then PDF. A Word COM failure keeps the DOCX, marks the receipt `failed` with the step name; re-run repeats the whole stage (it is deterministic). | `build-report.json`: DOCX package facts (§9.1), TOC field present, image count, PDF page count and bookmarks |
| `audit` | agentic | build outputs, chapter files, `rubric.json`, `evaluation/scorecard.json` | `audit/findings.json`, `scorecard.json`, `codex-audit.md`, `fixes.md` | `rubric_digest` (must equal the evaluate receipt's), `codex_audited_build` (build hashes Codex saw), `review_kind` per score | build receipt valid | — | One Codex audit (DEC-030). Claude fixes via the Fix Protocol; fixes that change chapters make build stale, so Claude re-runs `build`, then `complete audit`, which binds the **post-fix** build hashes and records the pre-fix ones in `codex_audited_build`. | rubric digest equality; scorecard with `self` and `independent` scores kept separate; zero blocker/major findings without a closed fixes row |

### 2.3 State, receipts and invalidation

`state.json` (schema `state.v1`) holds:

```json
{
  "schema_version": 1,
  "project_id": "<slug>",
  "receipts": { "<stage>": { "...": "..." } },
  "approvals": { "intake": { "...": "..." }, "design": { "...": "..." } }
}
```

**Receipt** (per the ticket's Definitions), for each completed stage:

| Field | Meaning |
|---|---|
| `stage` | stage id |
| `status` | `ok` or `failed` |
| `inputs` | `{path: sha256}` for every input file |
| `outputs` | `{path: sha256}` for every output file |
| `tool_sha` | last commit touching the stage's `tool_paths` (below) |
| `time` | ISO-8601 UTC |
| `error` | present only when `status = failed` |
| `invalidated_by` | present only when an upstream stage was re-begun after this receipt: `"<stage>@<time>"` |
| stage extras | from the table in §2.2 |

**Hashing.** JSON files are hashed in canonical form: parsed, then serialised with sorted keys, separators `(",", ":")`, `ensure_ascii=False`, UTF-8. Text files (`.md`, `.txt`, `.svg`, `.py`) are hashed after normalising CRLF to LF, so a Windows checkout does not make a receipt stale. Binary files are hashed as raw bytes.

**Tool SHA.** Each stage declares `tool_paths` (the harness files it executes, e.g. `harness/tools/check_book.py`). `tool_sha` = `git log -1 --format=%H -- <tool_paths>`. If any of those paths has uncommitted changes, the receipt is refused (`dirty tool`). This makes a tool change stale only the stages that run that tool.

**Staleness.** A receipt is stale if any input hash no longer matches, its `tool_sha` differs from the current value for its `tool_paths`, it has `invalidated_by`, or its status is `failed`. A stale receipt blocks every downstream stage.

**Invalidation.** `begin <stage>` and `run <stage>` write `invalidated_by` on every transitive downstream receipt **before** doing any work, so an upstream run that later fails still blocks downstream.

**Lock.** Every write to `state.json` holds `state.lock`, created with exclusive-create. A leftover lock produces a named error telling the user which process and time created it; it is never removed silently.

**`verify`.** `run_stage.py --project P verify [--through <stage>]` checks: each approval that exists up to the boundary still matches its hashes, and each mandatory receipt up to the boundary is valid (status ok, current input hashes, expected tool SHA, no invalidation marker). It exits 0 only when all pass, otherwise 1 with one line per failure.

### 2.4 Ingest fidelity

`conversion-report.json` records, for each structure, `source_count`, `output_count` and `status`:

| Structure | How the source is counted (DOCX) | Status rule |
|---|---|---|
| headings | paragraphs with a Heading style or matching `template.ingest.heading_rules` | `ok` if equal, else `lost` |
| tables | `w:tbl` elements (1×1 tables are callouts and counted separately) | `ok` if equal, else `lost` |
| figures | `a:blip` references | `ok` if equal, else `lost` |
| equations | `m:oMath` elements | `lossy` if converted to text, `lost` if dropped |
| footnotes | `w:footnoteReference` | `lossy` if inlined, `lost` if dropped |
| text | characters of body text vs characters in `normalized.md` (markup stripped) | `lost` if the output has < 98% of source characters |

Exit 2 if any structure is `lost`. `lossy` items become findings that evaluate must address. For non-DOCX input converted by `markitdown`, source counts that cannot be taken are recorded as `not_measurable` and the report says so; they never count as `ok`.

---

## 3. Approvals (c)

There are exactly two user approvals.

| Approval | Covers (hashed) | Written when | Blocks without it |
|---|---|---|---|
| `intake` | `brief.json`, `rubric.json`, `template.json`, `theme.json`, every `agents/*.json` | after the user explicitly approves, in chat, the exact files shown | every stage after `intake` |
| `design` | `design/design.md`, `design/chapter-plan.json`, `design/errata-seed.md`; plus `termbase.json` when translation applies (EXT-TR-2) | after the user explicitly approves, in chat, the exact files shown | `rework` and every stage after it |

**Record** (in `state.json` → `approvals.<kind>`): `kind`, `files {path: sha256}`, `dec_id`, `approved_at`, `approved_by: "user"`.

**Writing an approval.** Only Claude writes it, only right after the user's explicit approval, with `run_stage.py --project P approve <kind> --dec DEC-NNN`. The command refuses unless `projects/<p>/decisions.md` already contains a row for `DEC-NNN` naming this approval kind with the user's words. The approval set is data (`APPROVAL_SETS` in `state.py`) so STEP 2 can add files (EXT-TR-2).

**Changing an approved file.** Any edit to a covered file makes the approval stale, which blocks every gated stage until the user re-approves. There is no "minor edit" exemption (Rule 7). The design stage may need to change `template.json` or `theme.json` (e.g. a new callout); that edit re-opens the **intake** approval, and the user re-approves both. Stage receipts whose own inputs did not change stay valid after re-approval.

**Tests** use fixture projects with fixture approvals and never edit a real project's state.

---

## 4. Versioned schemas (d)

All schemas are JSON Schema (draft 2020-12 subset: `type`, `required`, `properties`, `additionalProperties`, `items`, `enum`, `pattern`, `minimum`, `maximum`, `minItems`, `maxItems`, `const`). The control plane validates them with a small stdlib validator of exactly that subset (Rule 10). Every document carries `"schema_version": 1`.

**Migration policy.** A breaking change creates `<name>.v2.json` plus a pure migration function `v1 → v2` in `state.py`. Tools read only the current version; `run_stage.py migrate` rewrites a project's files and, because hashes change, re-opens its approvals. Non-breaking additions (new optional field) keep the version.

### 4.1 `brief` — job facts from intake (covers questionnaire A–M)

No approval state lives here (CDR §3).

| Field | Type | Q | Notes |
|---|---|---|---|
| `schema_version` | const 1 | — | |
| `project_id` | slug | — | equals the project directory name |
| `identity.title` | string | A | |
| `identity.subtitle` | string or null | A | |
| `identity.edition` | string or null | A | |
| `identity.authors[]` | `{name, credit_line, role}` | A | `role`: `author`, `editor`, `translator`, `contributor` |
| `identity.credit_policy` | string | A | how authors are credited in the new edition |
| `identity.rework_authorised` | enum `yes`, `no`, `unknown` | A | with `identity.rework_authorised_note` |
| `source.files[]` | `{path, format, sha256}` | A | `format`: `docx`, `pdf`, `md`, `other`; paths outside the project are copied into `source/` by ingest |
| `domain.primary` | string | B | |
| `domain.subfields[]` | string | B | |
| `figures.packs[]` | enum from the pack registry (`charts`, `chemistry`) | B | `charts` is core (0b.6) and always available |
| `figures.notes` | string | B | |
| `audience.year_of_study` | string | C | |
| `audience.programmes[]` | string | C | programmes or professions |
| `audience.prior_knowledge` | string | C | |
| `audience.display_line` | string or null | C | printed on the title page if not null |
| `perspectives.enabled` | bool | D | |
| `perspectives.items[]` | `{id, label}` | D | empty when disabled; copied into `template.perspectives` |
| `goal.mode` | enum `evaluate_only`, `evaluate_and_rework` | E | drives the mandatory stage set (§2.1) |
| `goal.directions[]` | enum `simplify`, `broaden`, `update`, `restructure`, `other` | E | required non-empty when rework |
| `goal.notes` | string | E | |
| `language.source` | BCP-47 tag | F | e.g. `en`, `ar` |
| `language.output` | BCP-47 tag | F | selects `harness/locale/<tag>.json` |
| `language.translation_required` | bool | F | must be `true` when source ≠ output (cross-rule) |
| `language.terminology` | string | F | required terms or conventions; the termbase itself is STEP 2 (EXT-TR-2) |
| `size.target_words_total` | integer or null | G | |
| `size.chapter_count_target` | integer or null | G | |
| `size.restructuring` | enum `keep_chapters`, `merge_split_allowed`, `free` | G | with `size.restructuring_note` |
| `assessment.mcq.enabled` | bool | H | |
| `assessment.mcq.per_chapter` | integer or null | H | |
| `assessment.mcq.options` | integer or null | H | options per question |
| `assessment.mcq.format` | string | H | e.g. vignette share, answers at chapter end |
| `assessment.cases.enabled` | bool | H | |
| `assessment.exercises.enabled` | bool | H | |
| `context.country` | string or null | I | |
| `context.curriculum_standards[]` | string | I | e.g. NARS |
| `context.frameworks[]` | string | I | regulatory or professional frameworks |
| `references.style` | enum `vancouver`, `apa`, `harvard`, `ieee`, `other` | J | with `references.style_note` |
| `references.recency` | `{min_share_since: {year, share}}` or null | J | e.g. ≥ 25% since 2023 |
| `references.evidence_cutoff` | date or null | J | |
| `constraints.must_keep[]` | string | K | |
| `constraints.must_not_change[]` | string | K | |
| `constraints.isbn` | string or null | K | never invented; null unless the user gives one |
| `constraints.publisher` | string or null | K | |
| `constraints.deadline` | date or null | K | |
| `output.formats[]` | enum `docx`, `pdf` | L | |
| `output.page_size` | enum `A4`, `Letter`, `B5` | L | |
| `output.fonts` | string or null | L | preference; resolved into `theme.fonts` |
| `output.branding` | `{logo: path or null, colours: [hex] }` | L | |
| `domain_pillars[]` | `{id, name, weight, reviewer_ids[]}` | M | Claude proposes, the user approves or edits; must equal the domain pillars in `rubric.json` (cross-rule) |
| `answers` | `{A..M: {provenance, note}}` | A–M | `provenance`: `user` or `default-confirmed`; every letter present |
| `unresolved[]` | string | — | must be empty for `complete intake` to pass |

**Coverage check (exit criterion):** every questionnaire item A–M maps to fields above — A identity + source; B domain + figures; C audience; D perspectives; E goal; F language; G size; H assessment; I context; J references; K constraints; L output; M domain_pillars. The `answers` object also requires one entry per letter, so `complete intake` fails if any topic was skipped.

### 4.2 `rubric` — scoring system

| Field | Notes |
|---|---|
| `schema_version`, `project_id` | |
| `core_version` | the `rubric_core.json` version the fixed pillars came from |
| `pillars[]` | `{id, kind: fixed or domain, name, description, weight, anchors, hard_caps[], reviewer_ids[], applicable}` |
| `pillars[].anchors` | `{"9-10", "7-8", "4-6", "1-3"}` text per band, and `evidence_required` per band |
| `pillars[].hard_caps[]` | `{condition, max_score}`, e.g. an unfixed safety-critical error caps the accuracy pillar at 4 |
| `provenance` | `{generated_by, from_brief_sha256, edited_by_user: bool}` |

Validation rules are in §5.

### 4.3 `template` — content grammar (parser contract)

Stable semantic IDs are the machine keys; labels are presentation only (CDR §3).

| Field | Notes |
|---|---|
| `paths` | `chapters`, `chapter_glob`, `front_matter`, `glossary`, `errata`, `figures`, `normalized_source`, `assets`, `asset_link_prefix`, `allowed_asset_roots[]` |
| `ingest` | `heading_rules[] {pattern, level}`, `toc_end_pattern` or null, `drop_source_toc: bool` |
| `chapter_heading_pattern` | regex with named groups `num` and `title`; default from locale |
| `sections[]` | H2 sections: `{id, label, role, required, boxed}`; `role` ∈ `opening`, `objectives`, `core`, `takeaways`, `assessment`, `answers`, `references`, `how_to_use`, `other`; list order = required order |
| `callouts[]` | `{id, label, syntax, required, min, max, parts[] }`; `syntax` is the literal first-line marker; `parts[]` names labelled sub-parts (e.g. myth and evidence) |
| `perspectives` | `{enabled, callout_id, items[] {id, label}, balance_tolerance}` — from brief D |
| `learning_objectives` | `{enabled, id_pattern, min, max, discouraged_verbs[]}`; verbs default from locale |
| `assessment.mcq` | `{enabled, count, option_labels[], option_display_labels[], allow_other_labels: false, key_balance {min, max}, max_run, rationale_required, answers_section_role}` — from brief H |
| `assessment.case_question` | `{required, label}` |
| `citations` | `{style: numeric-bracket or author-year, pattern}` |
| `references` | `{section_role, entry_pattern, identifier_patterns[], no_doi_policy {allowed_types[], requires_url}, title_match {mode: heuristic, original-language or manual, words, threshold}, original_title_marker, providers}` |
| `locale_overrides` | any field of the locale profile, overriding it for this project (e.g. `digits.output`); EXT-LOC-1 |
| `glossary` | `{enabled, term_syntax, excluded_callout_ids[], minimum_terms}` |
| `readability` | `{mean_sentence_max, long_sentence_words, long_share_max}`; defaults from locale |
| `budgets` | `{tolerance, total {min, max}, front_matter}`; per-chapter budgets live in `chapter-plan.json` |
| `banned_terms[]` | `{pattern, replacement}`; merged with the locale list |
| `errata` | `{enabled, file, status_column, open_values[], closed_values[]}` |
| `figures` | `{caption_pattern}`; default from locale |
| `front_matter` | `{toc_insert_before_section_id}` |

### 4.4 `theme` — rendering only

A theme names a tested preset and overrides only what it must (CDR §3: no untestable layout engine).

| Field | Notes |
|---|---|
| `preset` | a file in `harness/presets/` (`ltr-textbook` now; the RTL preset is STEP 10) |
| `direction`, `lang_tag` | `ltr`/`rtl`, BCP-47; must agree with `brief.language.output` (cross-rule; EXT-LOC-2) |
| `page` | `{size, margins, header_distance, footer_distance}` |
| `fonts` | `{serif, serif_heading, sans, complex_script}` |
| `palette` | `{ink, primary, accent, muted}` hex |
| `layout.text_width` | cm |
| `alignment` | `{body, headings}` |
| `lists` | `{indent, hanging}` |
| `callouts.<callout_id>` | `{fill, label_colour, layout: box, grid or split}` |
| `boxed_section_ids[]`, `toc_excluded_section_ids[]` | section IDs |
| `toc` | `{levels}` |
| `cover` | `{asset or null}` |
| `title_page` | `{notices[]}`; title, subtitle, credits and audience line are read from `brief`, never duplicated here |
| `labels` | `{contents, update_toc_instruction, chapter, part, glossary, figure, table, question_prefix, objective_prefix}` — localized UI strings bound to IDs; machine markers in chapter Markdown stay ASCII and are shown with these labels (Arabic contract P1) |
| `output.basename` | build file name stem |
| `build` | `{backend: word_com, word_com {toc_styles}, pdf {bookmarks: headings, embed_fonts}}` |

### 4.5 Other schemas (named here, fields fixed by the plan in STEP 4)

`chapter-plan.v1` (chapters `{id, file, title, word_budget, part_id, source_refs[]}`, `parts[] {id, label, title}`, `dropped[] {source_unit, reason}`), `overlay.v1` (§6), `state.v1` (§2.3), `findings.v1` and `scorecard.v1` (§8), `checker-report.v1` (§9.1), `source-manifest.v1` and `conversion-report.v1` (§2.4), `figures.v1` (§7), `golden.v1` and `golden-diff.v1` (§9); `units.v1` (EXT-TR-3); defined by the STEP 2 contracts: `references-manual.v1`, `termbase.v1`, `trace.v1`.

### 4.6 Cross-file rules checked by `complete intake`

1. `rubric.pillars[kind=domain]` IDs and weights equal `brief.domain_pillars`.
2. `language.translation_required` is true if and only if `language.source ≠ language.output`.
3. `theme.lang_tag` and `theme.direction` agree with `language.output` and its locale profile.
4. `template.perspectives.enabled` equals `brief.perspectives.enabled`, and the items match.
5. `template.assessment.mcq.enabled` equals `brief.assessment.mcq.enabled`; if enabled, `count` and the number of `option_labels` equal `per_chapter` and `options`.
6. Every `reviewer_ids[]` entry in the rubric names a shared persona in `harness/agents/` or an overlay in `agents/`.
7. Every figure pack in `brief.figures.packs` exists in the pack registry.
8. `brief.unresolved` is empty and `brief.answers` has A–M.

---

## 5. Rubric core (e)

### 5.1 Fixed pillars (`harness/rubric_core.json`)

| ID | Pillar | Weight | Owns |
|---|---|:---:|---|
| `G1` | Content accuracy | 20 | every factually wrong statement, wrong number, wrong definition, wrong citation-to-claim link, anywhere in the book |
| `G2` | Pedagogical design and clarity | 20 | objectives, structure, progression, cognitive load, readability, figures' teaching value |
| `G3` | Assessment quality | 10 | questions, distractors, rationales, key balance, alignment to objectives |
| `G4` | Sources and currency | 10 | reference existence, recency against `brief.references.recency`, evidence hierarchy, citation coverage |
| | **Generic total** | **60** | |

### 5.2 Reserved split

- Generic pillars: **60** of 100, fixed.
- Domain pillars: **40** of 100, from intake (questionnaire M): 1–4 pillars, each an integer from 5 to 25, summing to exactly 40.
- If `brief.assessment` has MCQs, cases and exercises all disabled, `G3.applicable = false` and its 10 points move to `G2` (weight 30). No other reallocation is allowed.
- Validation: unique IDs; all four fixed IDs present with core weights (after the one allowed reallocation); total exactly 100; every pillar has ≥ 1 reviewer.

This split is a design choice of this spec. The previous medical rubric (`EVALUATION_RUBRIC.md:13-18`) put correctness inside domain pillars (clinical accuracy 25, AI rigour 20); here correctness moves to `G1` so no defect is counted twice.

### 5.3 Overlap rule

Each finding carries exactly one `pillar_id`. Assignment order:

1. A statement that is **false** (fact, number, definition, law, dose, date) → `G1`, whatever its domain.
2. A reference that does not exist, does not support the claim, or is out of date → `G4`.
3. An assessment item defect → `G3`.
4. A clarity, structure or level defect → `G2`.
5. Otherwise, a domain pillar: missing or shallow domain coverage, weak domain method or practice (e.g. regulatory depth, experimental method). Domain pillars never score correctness of an individual statement.

`complete evaluate` rejects a finding with zero or several pillars, and merges findings with the same location and claim, keeping the first pillar by this order.

### 5.4 Score and digest

- Each applicable pillar is scored 1–10 in 0.5 steps against its anchors, after `hard_caps`.
- Weighted total = Σ (score × weight) / 10, reported out of 100 with one decimal. The runner computes it; a hand-written total that disagrees fails `complete`.
- **Rubric digest** = SHA-256 of canonical `rubric.json` (§2.3). The evaluate and audit receipts both store it; `complete audit` fails if they differ. Baseline and rescore are therefore always on the same rubric.
- The medical project's new `rubric.json` is a different rubric from `EVALUATION_RUBRIC.md`. Its historic scores (46 and the self-assessed 81, `rework/REVIEW_REPORT.md:8`) are kept as history and never compared with harness scores.

---

## 6. Domain-agent overlay format (f)

Shared personas live in `harness/agents/` as fixed, domain-free Markdown. Initial set, taken from `.claude/agents/` and `.agents/skills/` with domain wording removed: `subject-reviewer` (the generic form of `medical-ai-reviewer`), `statistician`, `research-synthesist`, `psychologist`, `narratologist`, `anthropologist`, `historian`, `geographer`, `instructional-designer`. The medical-specific text of `medical-ai-reviewer.md` becomes the medical project's overlay, not a shared persona.

A project never adds a free-form agent. It adds **overlays**: `projects/<p>/agents/<id>.json`, schema `overlay.v1`, `additionalProperties: false`:

| Field | Limit |
|---|---|
| `schema_version` | 1 |
| `id` | slug, unique in the project |
| `base_persona` | an id in `harness/agents/` |
| `scope` | string, ≤ 400 characters |
| `criteria[]` | ≤ 12 strings, each ≤ 200 characters |
| `exclusions[]` | ≤ 8 strings, each ≤ 200 characters |
| `evidence_expectations[]` | ≤ 8 strings, each ≤ 200 characters |
| `pillar_ids[]` | domain pillar IDs this overlay reviews |

At use, the persona text is loaded, and the overlay is appended under a fixed heading "Project scope (data)" as a quoted list. Overlay text is treated as data: it cannot name tools, change permissions or alter the stage flow, because only these fields exist and each is length-capped. Overlays are covered by the intake approval.

---

## 7. Figure system and chemistry pack interface (g)

### 7.1 Figure manifest

`projects/<p>/figures/figures.json` (schema `figures.v1`), one entry per figure:

| Field | Notes |
|---|---|
| `id` | slug; stable across edits |
| `chapter_id` | from `chapter-plan.json` |
| `kind` | `chart.<type>`, `diagram.svg`, `chem.structure`, `chem.reaction`, `raster.existing`, `author-asset` |
| `source` | path under `figures/src/` (Python for charts, JSON data, hand SVG, SMILES/SMARTS JSON) or an existing image under an allowed asset root |
| `caption`, `alt` | required, non-empty |
| `credit`, `licence` | required; `licence` from a fixed list (`original`, `CC-BY-4.0`, `CC0`, `public-domain`, `permission-granted`, `author-supplied`) |
| `status` | `generated`, `existing`, `needs-author-asset` |

Numbering is computed, never stored: `Figure {chapter}.{n}` by order of first reference in the chapter, formatted by `template.figures.caption_pattern`.

### 7.2 Rendering

`harness/figures/render.py --project P` renders every generated figure to `figures/out/<id>.svg` and `figures/out/<id>.png` at 300 dpi at the theme's text width. Rendering is deterministic (fixed fonts, fixed seeds, no timestamps in output metadata). Charts use matplotlib (core, 0b.6). Hand SVGs are rasterised by a headless Chromium browser (Edge on stock Windows, or Chrome), as the current build does (`rework/tools/build_book.py:5-6`). Diagrams made with the `diagram-design` skill are saved as SVG source first. No paid or AI image generation (DEC-016).

### 7.3 Figure checker

`harness/figures/check_figures.py --project P` emits checker-report JSON with these check IDs: `FIG-UNREFERENCED` (in manifest, never referenced), `FIG-UNKNOWN` (referenced, not in manifest), `FIG-CAPTION`, `FIG-ALT`, `FIG-LICENCE`, `FIG-RESOLUTION` (PNG below 300 dpi at placed width), `FIG-AUTHOR-ASSET` (any `needs-author-asset`). `build` fails on any of them. A figure the harness cannot honestly generate (a real micrograph, a photograph) is `needs-author-asset`; the harness never fakes it.

### 7.4 Pack interface

A pack is a Python package `harness/figures/packs/<name>/` that exposes:

| Member | Contract |
|---|---|
| `KINDS` | set of figure kinds it renders, e.g. `{"chem.structure", "chem.reaction"}` |
| `preflight() -> list[str]` | missing dependencies as human-readable lines; empty means ready. Never installs anything (Rule 10). |
| `validate(spec) -> list[Finding]` | semantic validation before rendering, returning check IDs |
| `render(spec, out_svg, out_png) -> None` | deterministic render; raises a named error on invalid input |
| `crosscheck(spec, mode, cache_dir) -> {status, detail}` | `status` ∈ `pass`, `fail`, `unverified`; `mode` ∈ `offline`, `live` |

The registry is the set of package directories; `brief.figures.packs` must name registered packs.

### 7.5 Chemistry pack

Optional dependency group with a pinned RDKit version (the version is fixed by the plan after the Windows preflight in STEP 9).

| Kind | Spec fields | Validation | Check IDs |
|---|---|---|---|
| `chem.structure` | `smiles`, `name`, optional `pubchem_cid` | parse and sanitise; an invalid SMILES fails | `CHEM-SMILES-INVALID`, `CHEM-SANITIZE` |
| `chem.reaction` | `smarts`, `name`, optional `conditions` | parse the reaction SMARTS; every reactant and product sanitises | `CHEM-SMARTS-INVALID` |
| cross-check | `name` / `pubchem_cid` against PubChem | live: timeout 10 s, results cached under `figures/.cache/pubchem/`; offline or network failure → `unverified`, never `pass` | `CHEM-PUBCHEM-MISMATCH`, `CHEM-UNVERIFIED` |

Tests use mocked PubChem responses only.

---

## 8. Evaluate stage (h)

Designed under Rule 11: inline persona passes, then one Codex review. The first run's four parallel reviewer agents (`SESSION_SUMMARY.md` §1) are replaced.

**Procedure** (between `begin evaluate` and `complete evaluate`):

1. **Read** `ingest/normalized.md` and `conversion-report.json` in the main session.
2. **Persona passes, inline and sequential.** For each persona named in `rubric.pillars[].reviewer_ids`, Claude loads the shared persona plus its overlays and reviews the book as that persona, appending findings to `evaluation/findings.json`. The generic pillars are always covered: `subject-reviewer` for G1, `instructional-designer` and `psychologist` for G2 and G3, `research-synthesist` for G4.
3. **Deterministic evidence.** Where the source's structure allows, the harness checker and `verify_refs` run on the normalized source and their results are cited as evidence inside findings. Missing structure (a book that does not follow any template yet) is itself a G2 finding, not a crash.
4. **Score** each pillar in `evaluation/scorecard.json` with its evidence finding IDs; the runner computes the total.
5. **One Codex review** via `codex-delegate`, read-only, of `findings.json`, `scorecard.json` and `report.md` against the source. Claude saves the report verbatim to `evaluation/codex-review.md`, header `verdict`, `open_blocker_major`.
6. **Fix Protocol** (DEC-030) on the evaluation: confirm each Codex finding at its cited location, find the root cause, hunt siblings, fix, verify; record in `evaluation/fixes.md` with columns `ID | real/rejected | root cause | siblings found | fix | verification → result`.
7. `complete evaluate`.

**`findings.v1`:** `{id: F-NNN, pillar_id, severity: blocker, major or minor, location {file, line_start, line_end}, claim, evidence, source: persona id or codex, fix_hint}`.

**`scorecard.v1`:** `{rubric_digest, pillars[] {id, score, applicable, evidence_finding_ids[]}, total, review_kind: self or independent}`. Evaluate scores are `self`; the audit stage adds `independent` scores from Codex.

**Subagents.** Default 0. A spawn is allowed only for context isolation of a very large read whose conclusion alone is needed, or for genuinely independent parallel work; at most 2; each is logged in the receipt's `subagents[]` with its reason. "One agent per chapter" and "each persona deserves its own agent" are not reasons (Rule 11).

---

## 9. Regression strategy (i)

### 9.1 Golden report (`golden.v1`)

Produced by `harness/tools/capture_golden.py --project P --out FILE`. Top-level keys, all sorted for byte-stable output:

| Key | Content |
|---|---|
| `schema_version`, `project`, `tool_sha` | |
| `checks[]` | `{id, target, status: pass, fail or not_applicable, measured {…}}` — every checker check, per chapter and book-level |
| `chapters[]` | chapter files in order with titles |
| `words` | per chapter and total, as counted by the checker |
| `references` | per chapter: count, count with DOI, count without |
| `verify_refs[]` | `{chapter, n, status}`; capture exits 2 if any `ERROR` (network) line appears, so a flaky result is never frozen |
| `images[]` | `{path, width_px, height_px, dpi}` |
| `docx` | package part list, paragraph count per style, embedded image count, TOC field present, core properties minus volatile fields |
| `pdf` | page count and bookmark titles (read with pypdf, already installed; declared as a capture dependency) |
| `hashes` | semantic hashes of assembled Markdown, DOCX document part and each chapter |
| `volatile_excluded[]` | the exact list of excluded fields: `docProps/core.xml` `created`, `modified`, `lastModifiedBy`, `revision`; `docProps/app.xml` `TotalTime`; PDF `CreationDate`, `ModDate`, document ID |

Capturing twice with no change must produce byte-identical files (STEP 5 exit).

### 9.2 Comparator (`golden-diff.v1`)

`harness/tools/compare_golden.py A B --allow ALLOWLIST` walks both JSON trees and emits `{diffs[] {pointer, before, after, allowed, reason}}`. `ALLOWLIST` is a JSON list of `{pointer_glob, reason}` (JSON-pointer paths with `*` wildcards). Exit 0 only if every diff is allowed. The STEP 6 manifest carries its `expected_diff` allowlist in this format.

### 9.3 Stable check IDs and mutations

The checker emits `checker-report.v1`: `{target, checks[] {id, status, message, measured}}`. Check IDs are stable strings:

| Group | IDs |
|---|---|
| template | `TPL-H1`, `TPL-SECTION-MISSING`, `TPL-SECTION-ORDER`, `TPL-CALLOUT-MISSING`, `TPL-CALLOUT-COUNT` |
| perspectives | `PERSP-MISSING`, `PERSP-BALANCE` |
| objectives | `LO-COUNT`, `LO-VERB`, `LO-UNASSESSED` |
| assessment | `MCQ-COUNT`, `MCQ-OPTIONS`, `MCQ-EXTRA-OPTION`, `MCQ-LO-TAG`, `MCQ-LO-UNKNOWN`, `MCQ-CASE`, `KEY-MISSING`, `KEY-RATIONALE`, `KEY-BALANCE`, `KEY-RUN` |
| citations | `CIT-MISSING`, `CIT-UNCITED` |
| readability | `READ-MEAN`, `READ-LONG`, `READ-NOPROSE` |
| budget | `BUDGET-CHAPTER`, `BUDGET-TOTAL`, `BUDGET-FRONT` |
| glossary | `GLOSS-MISSING`, `GLOSS-MIN` |
| language | `BANNED-TERM` |
| book | `BOOK-CHAPTER-COUNT`, `BOOK-FRONT-MISSING`, `ERRATA-OPEN` |
| assets | `ASSET-MISSING`, `ASSET-OUTSIDE-ROOT` |
| references | `REF-NOT-FOUND`, `REF-TITLE-MISMATCH`, `REF-NO-DOI-DISALLOWED`, `REF-ERROR` |
| figures, chemistry | §7.3, §7.5 |
| Arabic locale | `AR-DIGIT-MIXED`, `AR-DIGIT-INCONSISTENT`, `REF-MANUAL-PENDING` (Arabic contract §6.4) |
| translation | `TB-*`, `PRES-*`, `TR-*` (translation contract §4.3, §5, §6) |

A check whose feature is disabled in `template.json` reports `not_applicable`, never `pass`.

**Minimum mutation set** (each must produce its named ID and a non-zero checker exit, while the test runner itself exits 0):

| Mutation | Expected ID |
|---|---|
| remove a required callout | `TPL-CALLOUT-MISSING` |
| break an image path | `ASSET-MISSING` |
| skew the answer key | `KEY-BALANCE` |
| reopen an erratum | `ERRATA-OPEN` |
| break a citation (cite a number with no reference) | `CIT-MISSING` |
| drop a perspective (only where configured) | `PERSP-MISSING` |
| exceed the word budget | `BUDGET-CHAPTER` |

### 9.4 Positive-config fixtures

Five small fixture projects under `tests/fixtures/positive-config/`, each a valid book with one feature disabled in its template: `no-mcq`, `no-glossary`, `no-cases`, `no-perspectives`, `no-errata`. Each must pass the checker with zero failing checks, and the disabled checks must report `not_applicable`. They prove shared code does not assume the medical book's structure (TR1, structural leakage).

### 9.5 Scoped leak scan

`harness/tools/leak_scan.py` scans **shared production code and schemas only**: `harness/**/*.py`, `harness/**/*.json`, `harness/agents/*.md`, `.claude/skills/book-*/**`. It excludes `projects/`, `tests/`, `docs/`.

It fails on:
- any literal from `tests/fixtures/leak/forbidden.txt`, which is generated from the medical project's config (profession and perspective labels, callout labels, title, subtitle, author names) plus a fixed list of clinical terms;
- any absolute path pattern (`[A-Za-z]:\\`, `/Users/`, `/home/`).

Its own test plants one forbidden literal in a temp copy and asserts exit 1. Structural leaks are caught by §9.4, not by the scan.

---

## 10. Inventory mapping (j)

One row per entry of the CDR "Hardcoded values inventory" (48 entries, in order). Target is a config key (§4) or `removed`.

| ID | Source (file:line) | Hardcoded value | Target |
|---|---|---|---|
| INV-01 | `convert_docx_to_md.py:13-15` | absolute source, Markdown and image paths under `D:\yasser` | `brief.source.files[]`, `template.paths.normalized_source`, `template.paths.assets` |
| INV-02 | `convert_docx_to_md.py:33-42` | extracted images always linked as `images/<file>` | `template.paths.asset_link_prefix` |
| INV-03 | `convert_docx_to_md.py:127-138` | English `Chapter N`, `Table of Contents`, `p.` grammar | `template.ingest.drop_source_toc` (the source TOC is dropped and regenerated at build) |
| INV-04 | `convert_docx_to_md.py:142-175` | English heading recognition (`Chapter Executive Overview`, `References`, `Self-Assessment Quiz`, `Chapter … Review`) | `template.ingest.heading_rules[]` |
| INV-05 | `convert_docx_to_md.py:154-155,288-289` | book title `ARTIFICIAL INTELLIGENCE IN MEDICINE` | `removed` (title comes from `brief.identity.title`; no title-specific cleanup) |
| INV-06 | `convert_docx_to_md.py:247-250` | TOC ends at literal `Chapter 1:` | `template.ingest.toc_end_pattern` |
| INV-07 | `convert_docx_to_md.py:280-286` | adds the medical book's missing Chapter 7 and References TOC links | `removed` |
| INV-08 | `rework/tools/check_book.py:12` | project root inferred from tool location | `removed` (required `--project`, §1.1) |
| INV-09 | `rework/tools/check_book.py:14-17` | eleven chapter budgets, readability limits, front-matter budget | `chapter-plan.chapters[].word_budget`, `template.readability.*`, `template.budgets.front_matter` |
| INV-10 | `rework/tools/check_book.py:18-22` | six section labels, four box labels, four perspective labels | `template.sections[]`, `template.callouts[]`, `template.perspectives.items[]` |
| INV-11 | `rework/tools/check_book.py:23,83-97` | ASCII word tokenizer, English sentence splitting | `locale.tokenizer`, `locale.sentence_terminators` |
| INV-12 | `rework/tools/check_book.py:39-49` | literal `References` and `Self-Assessment` boundaries | `template.sections[].role` (`references`, `assessment`) |
| INV-13 | `rework/tools/check_book.py:103-116` | `# Chapter N: Title` and literal box syntax | `template.chapter_heading_pattern`, `template.callouts[].syntax` |
| INV-14 | `rework/tools/check_book.py:120-132` | exactly four perspectives, ±20% balance | `template.perspectives.items[]` (count), `template.perspectives.balance_tolerance` |
| INV-15 | `rework/tools/check_book.py:136-146` | `LO` IDs, 3–5 objectives, banned verb `understand` | `template.learning_objectives.*`, `locale.discouraged_objective_verbs` |
| INV-16 | `rework/tools/check_book.py:150-199` | ten MCQs, A–D, no E, one case question, key counts 2–3, no triple run | `template.assessment.mcq.*`, `template.assessment.case_question` |
| INV-17 | `rework/tools/check_book.py:202-221` | numeric square-bracket citations | `template.citations.style`, `template.citations.pattern` |
| INV-18 | `rework/tools/check_book.py:225-249` | bold marks glossary terms; literal perspective-box exception | `template.glossary.term_syntax`, `template.glossary.excluded_callout_ids[]` |
| INV-19 | `rework/tools/check_book.py:252-253` | English banned term and replacement | `template.banned_terms[]` (merged with `locale.banned_terms`) |
| INV-20 | `rework/tools/check_book.py:259-289` | `chNN`, glossary file, 11 chapters, front-matter file, 17k–21k total, errata file, literal open status, ≥ 120 glossary terms | `template.paths.*`, `chapter-plan.chapters[]`, `template.budgets.total`, `template.errata.*`, `template.glossary.minimum_terms` |
| INV-21 | `rework/tools/build_book.py:21-28` | root/rework/output paths; book title, subtitle, author | `template.paths.*`, `theme.output.basename`, `brief.identity.title`, `brief.identity.subtitle`, `brief.identity.authors[]` |
| INV-22 | `rework/tools/build_book.py:30-32` | fonts, palette, text width | `theme.fonts.*`, `theme.palette.*`, `theme.layout.text_width` |
| INV-23 | `rework/tools/build_book.py:35-44` | callout labels and colours | `theme.callouts.<callout_id>` |
| INV-24 | `rework/tools/build_book.py:45-51` | three parts with chapter spans; boxed and unlisted sections | `chapter-plan.parts[]`, `theme.boxed_section_ids[]`, `theme.toc_excluded_section_ids[]` |
| INV-25 | `rework/tools/build_book.py:204-237` | `en-GB`, left-aligned styles | `theme.lang_tag`, `theme.direction`, `theme.alignment.*` |
| INV-26 | `rework/tools/build_book.py:289-317` | LTR option/reference/glossary indentation | `theme.lists.*`, `theme.direction` |
| INV-27 | `rework/tools/build_book.py:429-472` | four perspectives in a 2×2 grid; literal perspective, myth and evidence labels | `template.perspectives.*`, `template.callouts[].parts[]`, `theme.callouts.<callout_id>.layout` |
| INV-28 | `rework/tools/build_book.py:501-519` | figure path assumptions, PNG mirror directory, English `Figure N.N` captions | `template.paths.figures`, `figures.json` (`figures.v1`), `template.figures.caption_pattern` |
| INV-29 | `rework/tools/build_book.py:569-573` | A4 page and fixed margins/distances | `theme.page.*` |
| INV-30 | `rework/tools/build_book.py:598-653` | English section names and callout grammar drive rendering | `removed` (the renderer consumes the checker's parsed representation keyed by section and callout IDs) |
| INV-31 | `rework/tools/build_book.py:663-703` | cover detected by filename substring; English Q/LO grammar; A–E options | `theme.cover.asset`, `template.assessment.mcq.option_labels[]`, `template.learning_objectives.id_pattern` |
| INV-32 | `rework/tools/build_book.py:715-751` | literal `References`, `Learning Objectives`, `Answers and Rationales` | `template.sections[].role` (`references`, `objectives`, `answers`) |
| INV-33 | `rework/tools/build_book.py:761-805` | fixed cover file, title-page layout, title/subtitle/author | `theme.cover.asset`, `theme.title_page.*`, `brief.identity.*` |
| INV-34 | `rework/tools/build_book.py:805-825` | four-profession audience line; named fictional-patient notice | `brief.audience.display_line`, `theme.title_page.notices[]` |
| INV-35 | `rework/tools/build_book.py:827-832` | English `Contents` and fallback message | `theme.labels.contents`, `theme.labels.update_toc_instruction` |
| INV-36 | `rework/tools/build_book.py:841-908` | `How to Use This Book`, `Chapter`, `Glossary`, `ch*.md`, part structure | `template.sections[].role` (`how_to_use`), `theme.labels.*`, `template.chapter_heading_pattern`, `template.paths.chapter_glob`, `chapter-plan.parts[]` |
| INV-37 | `rework/tools/build_book.py:918-923` | core metadata language `en-GB` | `theme.lang_tag` |
| INV-38 | `rework/tools/build_book.py:928-964` | Word COM, hidden instance, TOC styles, embedded fonts, PDF settings | `theme.build.backend`, `theme.build.word_com.*`, `theme.build.pdf.*` |
| INV-39 | `rework/tools/assemble.py:10-12` | tool-relative root, `rework/`, root-level output name | `template.paths.chapters`, `theme.output.basename` (and required `--project`) |
| INV-40 | `rework/tools/assemble.py:21-23` | prefix rewriting of `../images/` and `figures/` | `removed` (path-relative asset resolver, §1.1) |
| INV-41 | `rework/tools/assemble.py:28-34` | front-matter file, `ch*.md`, glossary file, `Contents`, `How to Use This Book` | `template.paths.*`, `theme.labels.contents`, `template.front_matter.toc_insert_before_section_id` |
| INV-42 | `rework/tools/assemble.py:37` | only `images/` and `rework/figures/` are asset roots | `template.paths.allowed_asset_roots[]` |
| INV-43 | `rework/tools/verify_refs.py:17,44-48` | ASCII title tokenizer, first six words, 60% overlap | `template.references.title_match.*` |
| INV-44 | `rework/tools/verify_refs.py:20-23` | literal `References` and numbered-entry grammar | `template.sections[].role` (`references`), `template.references.entry_pattern` |
| INV-45 | `rework/tools/verify_refs.py:27-40` | Crossref endpoint, user agent, 5 retries, 15 s timeout, fixed backoff | `defaults.references.providers.crossref.*` (harness `defaults.json`; overridable by `template.references.providers`) |
| INV-46 | `rework/tools/verify_refs.py:53-57` | DOI patterns; every no-DOI reference passes despite the stated rule | `template.references.identifier_patterns[]`, `template.references.no_doi_policy` |
| INV-47 | `rework/tools/renumber_refs.py:8,30-46` | numeric square-bracket citations; English `## References` | `template.citations.pattern`, `template.sections[].role` (`references`) |
| INV-48 | `rework/_template.md:1-52` | medical chapter skeleton with English headings | `removed` (a skeleton is generated from `template.json` by the runner at `begin rework`) |

**Completeness:** 48 CDR rows → INV-01…INV-48. 42 map to config keys; 6 are `removed` (INV-05, INV-07, INV-08, INV-30, INV-40, INV-48). No row is unmapped.

---

## 11. Locale and translation extension points (k)

Named here; STEP 2 fills them. Core code must route through these points, so Arabic and translation add data and implementations, not new call sites.

| ID | Extension point | Core obligation now |
|---|---|---|
| EXT-LOC-1 | **Locale profile** `harness/locale/<tag>.json`, selected by `brief.language.output`: `tokenizer`, `sentence_terminators[]`, `digit_policy`, readability defaults, `discouraged_objective_verbs[]`, `banned_terms[]`, default `chapter_heading_pattern`, `figure_caption_pattern`, default labels; project overrides via `template.locale_overrides` | Every locale-dependent function takes the profile as a **parameter** (no global language): chapters use the output-language profile, source text and translation checks use the source-language profile. `en.json` reproduces today's behaviour |
| EXT-LOC-2 | **Direction and bidi** `theme.direction`, `theme.lang_tag`, `theme.fonts.complex_script` | The DOCX renderer creates every paragraph, run and table through one function that applies direction and language properties from the theme; LTR behaviour is today's |
| EXT-LOC-3 | **Labels bound to stable IDs** `template.sections[].label`, `template.callouts[].label`, `theme.labels.*` | No shared code compares against a display string; parsing matches the configured label for an ID |
| EXT-LOC-4 | **Reference policy** `template.references.title_match.mode` and a separate DOI-existence result | `verify_refs` reports existence and title match as two fields; `mode` selects the matcher |
| EXT-LOC-5 | **Acceptance corpus** `tests/fixtures/locale/<tag>/` | The test runner discovers per-locale corpora by directory |
| EXT-TR-1 | **Stage slot** in the `STAGES` data (§2.1): `translate` between `design` and `rework`, mandatory when `translation_required` and `goal.mode = evaluate_and_rework` | Stage graph, mandatory sets and invalidation are data-driven |
| EXT-TR-2 | **Termbase and approval set** `projects/<p>/termbase.json` joins the design approval set when translation applies; `termbase-additions.json` is not gated; `APPROVAL_SETS` is data (§3) | An approval set can gain a file without code changes to the gate |
| EXT-TR-3 | **Traceability units** `ingest/units.json` (source unit IDs `src-chNN`, `src-chNN-sMM`), `trace/source-target-map.json`; target chapter IDs from `chapter-plan.json`, section IDs from `template.sections[].id` | Ingest writes `units.json`; chapter and section IDs are stable and exposed by the checker's parsed representation |
| EXT-TR-4 | **Independent review gate** receipt fields `author_model`, `reviewer_model` | `state.py` exposes one check that `reviewer_model ≠ author_model` for any stage that declares it |

---

## 12. Dependencies (Rule 10)

| Layer | Dependencies | Missing-dependency behaviour |
|---|---|---|
| control plane (`state.py`, `run_stage.py`), checker, assembler, `verify_refs`, comparator, leak scan | Python 3.11 stdlib | — |
| ingest | python-docx, lxml (DOCX); `markitdown` (non-DOCX, optional) | preflight names the missing package; ingest of that format exits non-zero with the name |
| build | python-docx, Pillow, pywin32, Microsoft Word; Edge or Chrome for SVG rasterising | preflight names what is missing; build exits non-zero |
| figures | matplotlib (core charts); RDKit (chemistry pack, optional group) | pack `preflight()` lists what is missing |
| golden capture | pypdf (PDF facts) | capture exits non-zero naming it |

Runtime code never installs anything.

---

## 13. What this spec deliberately leaves to later steps

| Item | Step |
|---|---|
| Arabic tokenizer, digits, thresholds, bidi XML, RTL preset, Arabic reference policy internals | STEP 2 (contract), STEP 10 (implementation) |
| Translation stage position, termbase schema, traceability map schema, review gate procedure | STEP 2, STEP 11 |
| Exact commands, exit codes, task order, migration manifest format | STEP 4 plan |
| Field-level detail of the schemas listed in §4.5 | STEP 4 plan, STEP 7 implementation |

---

## 14. Decisions this spec asks the user to approve

These are design choices of this spec, listed so the approval is explicit:

1. **Rubric split 60 generic / 40 domain**, with `G1` owning all correctness (§5).
2. **Two stage kinds** (`auto` and `agentic` with `begin`/`complete`) and **per-chapter resume** for rework (§2).
3. **`chapter-plan.json` is a design artifact**; per-chapter budgets and parts live there, not in the intake template (§4.3).
4. **Editing an intake file during design re-opens the intake approval** (§3).
5. **Tool SHA per stage `tool_paths`**, not the whole repo (§2.3).
6. **Audit binds the post-fix build**, recording the Codex-audited build separately (§2.2).
