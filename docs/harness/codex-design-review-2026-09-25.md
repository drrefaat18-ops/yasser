# Codex design review of Approach A (2026-09-25, read-only)

> Source: codex-cli 0.153.3 relay run, read-only sandbox. Verbatim final report. Two claims spot-checked by Claude: verify_refs.py:53-57 accepts every NO DOI; REVIEW_REPORT.md:8 admits self-assessment.

## Overall verdict

**Concern — approve only after redesigning the control plane.**

Approach A has the right basic shape: one repository, isolated `projects/<book>/` workspaces, shared tools, project-specific configuration, and interactive approval. It is substantially better than a non-interactive `claude -p` orchestrator or a prose-only playbook.

The current proposal is not yet safe or generic enough because:

- It omits an explicit ingest/conversion stage even though conversion is one of the six required stages.
- Slash commands are being treated as enforcement boundaries. They are only user interfaces; every executable must enforce gates itself.
- The approval record is not defined strongly enough to detect later edits to the approved brief, rubric, agents, or template.
- “Identical checker results” can mean nothing more than both implementations printing `PASS`.
- Arabic affects the parsing contract and document renderer, not merely a language setting.
- “Stdlib Python only” conflicts with the existing build and conversion stack: `python-docx`, Pillow, pywin32, and Microsoft Word are already required (`convert_docx_to_md.py:5-9`; `rework/tools/build_book.py:12-19,505-506,928-964`).

I would retain Approach A’s project model and interactive commands, but put a shared Python stage runner and state machine underneath them.

## Point-by-point (1–6)

### 1. Stage breakdown

**Verdict: Concern**

The ordering is broadly correct, but `/book-new -> /book-intake -> /book-evaluate` skips source ingestion. The existing pipeline has a real conversion step with media extraction and structural heuristics (`convert_docx_to_md.py:13-30,127-193,237-294`). That is not merely project initialization.

There is also naming ambiguity: `brief.json` is said to contain intake answers, while `/book-brief` comes after evaluation. Those are two different artifacts:

- An approved intake/job brief needed before any work.
- A rework design/specification derived from the baseline evaluation.

The repository itself separates baseline review from the later rework design and implementation plan: the design consumes the verdict, session summary, and rubric (`docs/superpowers/specs/2026-09-24-interprofessional-rework-design.md:4-5`), while the implementation plan applies checker and persona gates during drafting (`docs/superpowers/plans/2026-09-24-interprofessional-rework.md:262-273`).

The proposed stage sequence also hides verification inside “rework” and “build.” The existing process treats checker, reference verification, errata closure, persona review, and final audit as distinct gates (`docs/superpowers/plans/2026-09-24-interprofessional-rework.md:266-273,388-404`).

**Concrete fix**

Treat `/book-new` and `/book-intake` as control-plane operations, then preserve six core production stages:

1. **Ingest/normalize** — copy source into project custody, convert DOCX to Markdown, extract assets, create a conversion report, and perform source-to-Markdown QA.
2. **Baseline evaluate** — use the already approved rubric and domain agents.
3. **Design** — produce the rework brief, specification, plan, chapter architecture, template, and acceptance criteria; require a second approval before drafting.
4. **Rework** — chapter drafting plus checker, citations, errata, and reviewer gates.
5. **Build** — assemble Markdown, produce DOCX/PDF, and run artifact QA.
6. **Independent final audit/rescore** — use the same rubric digest as the baseline and clearly identify self-review versus independent review.

Rename `/book-brief` to `/book-design` or `/book-rework-plan`. “Brief” should refer only to the intake artifact.

The rubric and generated domain agents must be generated and approved during intake, before baseline evaluation. Otherwise the system is choosing its scoring rules after seeing the manuscript.

---

### 2. Enforcing “no stage runs until brief.json is approved”

**Verdict: Disagree with skill-level enforcement; agree with code-enforced preconditions**

Skill or slash-command instructions are not sufficient. Users, agents, tests, or future automation can call `check_book.py`, `build_book.py`, or other entry points directly. The current tools contain no project-state precondition: `check_book.py` goes directly from argument parsing to checking (`rework/tools/check_book.py:294-312`), while the builder immediately generates artifacts (`rework/tools/build_book.py:835-925,967-971`).

A Boolean such as `"approved": true` inside `brief.json` is also inadequate. Editing the brief after approval would leave the Boolean intact.

**Concrete fix**

Create a shared module such as `harness/state.py`, used by every stage entry point:

- `require_project(project_dir)`
- `require_approved_intake(project_dir)`
- `require_stage_dependencies(project_dir, target_stage)`
- `record_stage_result(...)`
- `invalidate_downstream(...)`

Use separate files:

- `brief.json` — user-approved intake facts and constraints.
- `rubric.json` — approved scoring system.
- `template.json` and `theme.json` — approved structural and rendering contracts.
- `agents/*.json` or `.md` — approved domain reviewer definitions.
- `state.json` — current workflow state.
- `events.jsonl` — append-only audit trail, if an audit log is valuable.

The approval record in `state.json` should bind a canonical digest:

```json
{
  "schema_version": 1,
  "project_id": "ai-in-medicine",
  "intake_approval": {
    "status": "approved",
    "approved_at": "2026-09-25T...",
    "approved_by": "user",
    "brief_sha256": "...",
    "rubric_sha256": "...",
    "template_sha256": "...",
    "agents_sha256": "..."
  }
}
```

Every stage must recompute those hashes. A mismatch makes approval stale and blocks execution. Later stages must likewise bind their upstream artifacts:

- Evaluation binds the approved brief, rubric, agents, normalized source, and tool version.
- Design binds the evaluation result.
- Rework binds the approved design/template.
- Build binds the validated chapter set.
- Rescore binds the baseline rubric digest and built artifact hashes.

Use an explicit dependency graph, not only a monotonically increasing stage number. Editing an earlier artifact must invalidate all downstream stages.

The slash commands should be thin interfaces over the same Python runner, for example:

```text
python harness/run_stage.py --project projects/ai-in-medicine evaluate
```

No tool should infer a default current project. Require `--project`, resolve it, and reject paths outside `projects/`.

This protects against accidental bypass, not a malicious local user who can edit code and state. Cryptographic signatures would be unnecessary over-engineering for that threat model.

---

### 3. Configuration schema and full genericity

**Verdict: Concern**

The proposed three files are directionally right, but their responsibilities are underspecified. A truly generic system should not put editorial intent, parser grammar, visual design, and workflow approval into one document.

The current parser uses English display text as machine identifiers: `"Opening Case"`, `"References"`, `"Through Four Lenses"`, `"Case Question"`, and similar strings are embedded throughout `check_book.py` (`rework/tools/check_book.py:18-22,39-49,101-199`). That design cannot support Arabic cleanly.

**Concrete fix**

Use stable semantic IDs internally and localized labels only for presentation.

`brief.json` should include:

- `schema_version`, `project_id`, title, subtitle, edition, author/credit policy.
- Source files, source format, source hashes, source language.
- Output language, locale, text direction, and whether translation is required.
- Institution, program/course, audience, learner level, prerequisites.
- Domain and subdomains.
- Purpose: evaluate only, revise, translate, build, or all stages.
- Desired deliverables and formats.
- Jurisdictions/local context.
- Evidence cutoff date and permitted source types/databases.
- Chapter preservation/restructuring policy.
- Accessibility and branding requirements.
- User constraints, exclusions, and unresolved questions.

Do not put approval state inside this file.

`rubric.json` should include:

- Stable pillar IDs.
- `kind: fixed | domain`.
- Localized name and description.
- Weight and 1–10 scoring anchors.
- Evidence required to award each score band.
- Hard-fail conditions.
- Assigned reviewer agent IDs.
- Generation provenance.
- Validation rules: unique IDs, weights total exactly 100, and required fixed pillars present.

The current rubric demonstrates why this is necessary: its medical accuracy, AI rigor, and medicolegal pillars are domain-specific (`EVALUATION_RUBRIC.md:13-18,25-48`). Baseline and rescore must use the same approved rubric digest or the score change is not comparable.

I recommend reserving a fixed total weight for the four generic pillars and a fixed pool for domain pillars. Also define whether “scientific accuracy” contains domain accuracy or whether domain pillars add coverage/depth; otherwise the same defect can be double-counted.

`template.json` should include:

- Chapter filename and H1 patterns.
- Required and optional section IDs, order, and localized labels.
- Chapter count or chapter manifest.
- Per-chapter and total word budgets.
- Callout definitions: stable ID, localized label, required/optional, cardinality.
- Perspective/lens definitions, cardinality, and balance tolerance.
- Learning-objective syntax, allowed count, localized discouraged verbs.
- Question-bank structure, option labels, count, case-question requirement, key-balance rules, rationale requirements.
- Citation style and reference-section grammar.
- Glossary rules and minimums.
- Sentence tokenizer profile and language-specific thresholds.
- Errata ledger schema and closure states.
- Figure/caption syntax.
- Front matter and back matter section IDs.

Use `theme.json` for build-only concerns:

- Page size, margins, fonts, palette.
- LTR/RTL and language tags.
- Box styling mapped by semantic callout ID.
- Parts, chapter spans, cover asset.
- TOC, glossary, reference and running-head labels.
- Title-page metadata, audience line, notices.
- Output basename and artifact locations.

Do not make every low-level Word spacing constant user-configurable. Provide a small number of tested presets plus narrowly scoped overrides.

---

### 4. Migrating the medical book

**Verdict: Concern**

A move to `projects/ai-in-medicine/` is feasible, but many paths currently depend on fixed ancestor counts and root locations:

- Checker root is `parents[1]` (`rework/tools/check_book.py:12`).
- Builder root and rework paths are based on `parents[2]` and root output (`rework/tools/build_book.py:21-24`).
- Assembler has the same assumption (`rework/tools/assemble.py:10-12`).
- Converter uses absolute `D:\yasser` paths (`convert_docx_to_md.py:13-15`).
- Repository instructions still describe root-level manuscripts and images (`CLAUDE.md:12-20`).
- Product documentation specifies `rework/` and `images/` as root locations (`PRODUCT.md:42-46`).

The `../images/` links can remain valid only if the migration preserves this relative layout:

```text
projects/ai-in-medicine/
  images/
  rework/
    ch*.md
```

Current chapters mix `../images/...` and `figures/...` (`rework/ch06-seeing-disease.md:36,53`; `rework/ch09-monitoring-prediction.md:43,51`). The assembler then rewrites both forms to repository-root conventions (`rework/tools/assemble.py:21-37`). Moving files without first defining one project-relative asset model will break assembled links or duplicate assets.

“Identical checker results” is not a sufficient regression test. Today the entire book produces only a terminal `PASS`; a generalized checker that accidentally skips every check could produce the same result. The current tests are also tightly tied to the medical template and cover only checker/ref-verifier behavior (`rework/tools/test_check_book.py:5-45,75-132`; `rework/tools/test_verify_refs.py:14-31`). There are no equivalent tests for assembly, DOCX structure, PDF export, TOC, RTL, or images.

**Concrete fix**

Migrate in separate commits:

1. Freeze a baseline manifest: structured checker findings, word counts, chapter list, reference counts, image-resolution results, output metadata, and hashes where appropriate.
2. Perform pure `git mv` operations with no refactor.
3. Update paths and project discovery.
4. Generalize tools.
5. Add Arabic and multi-project behavior.

Git generally detects renames, and `git log --follow` can preserve practical history, but mixing moves with broad rewrites in one commit will make that history much harder to inspect.

Keep the live project at `projects/ai-in-medicine/`, but keep immutable golden fixtures under `tests/fixtures/ai-in-medicine/`. Regression should compare a structured JSON report containing every named check, measured value, and outcome—not stdout alone.

Also add negative mutation tests: remove a required box, break an image path, alter an answer distribution, reopen an erratum, and change a citation. Each mutation must fail for the expected check ID. For builds, verify DOCX package structure, metadata, embedded images, TOC field, PDF page count, links/bookmarks, and a small set of rendered-page snapshots.

---

### 5. Arabic support

**Verdict: Concern — feasible, but much larger than proposed**

The current checker is fundamentally English-only:

- Word tokens accept only ASCII letters and digits (`rework/tools/check_book.py:23`).
- Sentence splitting only recognizes `. ! ?` followed by whitespace (`rework/tools/check_book.py:83-97`).
- Headings and chapter titles are fixed English strings (`rework/tools/check_book.py:18-22,39-49,101-117`).
- Objective and MCQ rules depend on English tokens such as `"understand"` and `"Case Question"` (`rework/tools/check_book.py:136-199`).
- Reference and glossary parsing also uses fixed English headings (`rework/tools/check_book.py:202-249`).

The builder is likewise LTR English:

- Document language is `en-GB` (`rework/tools/build_book.py:204-215`).
- Headings, options, references, headers, and title matter are explicitly left-aligned (`rework/tools/build_book.py:218-332`).
- `"Through Four Lenses"` and `"Myth vs Evidence"` have custom English parsing (`rework/tools/build_book.py:429-472,635-653`).
- Title, audience, fictional-patient notice, TOC, chapter syntax, and glossary are English (`rework/tools/build_book.py:761-832,841-908`).
- Core document metadata remains `en-GB` (`rework/tools/build_book.py:918-923`).

**Concrete fix**

Scope Arabic as a distinct renderer/parser profile:

- Use stable section IDs with Arabic display labels.
- Implement Unicode-aware word tokenization using standard-library Unicode semantics, not the current ASCII regex.
- Recognize Arabic question mark `؟`, ellipsis `…`, and configured sentence terminators.
- Decide how Arabic-Indic digits, Western digits, chapter numbering, question labels, and citation numbers are accepted.
- Calibrate sentence-length thresholds independently for Arabic; English thresholds should not be copied without evidence.
- Add Arabic reference behavior. The current DOI-title heuristic tokenizes only `[a-z0-9]` and compares the first six Crossref-title words (`rework/tools/verify_refs.py:17,44-48`), so translated Arabic reference titles will fail or become meaningless.
- Separate DOI existence from title matching and allow original-language titles or manual review states.

For DOCX:

- Set paragraph/style `w:bidi`.
- Set run `w:rtl` where appropriate.
- Set `w:lang` with a bidi locale such as `ar-EG`.
- Set complex-script fonts through `w:rFonts/@w:cs` and `w:szCs`.
- Mirror list indentation, hanging indents, tabs, headers, captions, tables, and TOC styles.
- Apply `w:bidiVisual` to tables where visual column order must be RTL.
- Test mixed Arabic/English strings, DOIs, formulas, acronyms, and page numbers.

`python-docx` creates the XML; Word performs final shaping and PDF rendering. Therefore Word COM can produce good Arabic output, but only after the DOCX contains correct bidi metadata and suitable installed fonts. Visual PDF QA is mandatory.

Finally, source language and output language being different implies translation/localization work. That must be an explicit policy inside the design/rework stage, with bilingual terminology and translation-review gates. A pair of language fields alone does not provide translation support.

---

### 6. Over-engineered and under-specified elements

**Verdict: Concern**

**Over-engineered or at risk of YAGNI**

- Seven slash commands are acceptable as UX, but they should not each become separate orchestration implementations. One stage runner with command wrappers is enough.
- Full executable Claude agent files generated for every project may become hard to audit and expose prompt-injection risks. Keep shared reviewer behavior fixed; generate small, approved project-specific domain overlays containing scope, criteria, exclusions, and evidence expectations.
- Making every font size, spacing value, and Word XML choice configurable would create an untestable layout engine. Use tested LTR-English and RTL-Arabic presets plus branding overrides.
- An append-only event log is useful, but cryptographic signatures or a database would be excessive for a local one-user harness.

**Under-specified**

- No schema versions or migration policy.
- No definition of project selection, slug validation, or path containment.
- No rule for invalidating approvals after edits.
- No rubric-weight constraints or overlap policy between generic and domain pillars.
- No guarantee that baseline and final scores use the same rubric.
- No definition of independent versus self-review. The current report explicitly admits the re-score was performed by the same authoring process (`rework/REVIEW_REPORT.md:8`).
- No resume, retry, or partial-stage failure semantics.
- No provenance for source hashes, tool versions, prompts, model runs, or external reference checks.
- No offline/network policy for DOI verification.
- The reference verifier’s stated rule is not actually enforced: the docstring says missing DOI is allowed only for laws/guidance with a URL, but the implementation accepts every `NO DOI` without validation (`rework/tools/verify_refs.py:1-6,53-57`).
- No source-conversion fidelity gate for tables, figures, headings, footnotes, equations, or omitted text.
- No artifact-level build acceptance criteria.
- No Arabic acceptance corpus.
- No strategy for books whose assessment format is not ten four-option MCQs.
- No handling of books without glossary, cases, lenses, or errata. These must be project requirements, not universal assumptions.
- “No new dependencies” needs precise wording. The checker and orchestration layer can remain stdlib-only, but conversion/build are not: the existing pipeline already depends on `python-docx`, Pillow, pywin32, and installed Microsoft Word (`convert_docx_to_md.py:5-9`; `rework/tools/build_book.py:12-19,505-506,928-964`).

**Concrete fix**

Write versioned JSON Schemas and a stage contract before moving files. Define mandatory inputs, outputs, preconditions, invalidation rules, failure states, and QA evidence for each stage. Keep the orchestration core stdlib-only while documenting retained external runtime dependencies honestly.

## Hardcoded values inventory

| File:line | Hardcoded value or assumption | Proposed config key |
|---|---|---|
| `convert_docx_to_md.py:13-15` | Absolute source, Markdown output, and image paths under `D:\yasser` | `brief.source.files[]`, `paths.normalized_source`, `paths.assets` |
| `convert_docx_to_md.py:33-42` | Extracted images always use `images/<filename>` | `paths.asset_link_prefix` |
| `convert_docx_to_md.py:127-138` | English `Chapter N`, `Table of Contents`, and `p.` grammar | `locale.chapter_pattern`, `labels.contents`, `locale.page_abbreviation` |
| `convert_docx_to_md.py:142-175` | English heading recognition: `Chapter Executive Overview`, `References`, `Self-Assessment Quiz`, `Chapter … Review` | `ingest.heading_rules[]` |
| `convert_docx_to_md.py:154-155,288-289` | Book-specific title `ARTIFICIAL INTELLIGENCE IN MEDICINE` | `brief.title` and removal of title-specific cleanup |
| `convert_docx_to_md.py:247-250` | TOC ends at literal `Chapter 1:` | `ingest.toc_end_pattern` |
| `convert_docx_to_md.py:280-286` | Adds the missing medical book’s Chapter 7 and References links | Remove entirely; use structural TOC regeneration |
| `rework/tools/check_book.py:12` | Project root inferred from tool location | Explicit `--project` and project manifest |
| `rework/tools/check_book.py:14-17` | Eleven chapter budgets, English readability limits, front-matter budget | `template.chapters[].word_budget`, `template.readability.*`, `template.front_matter.word_budget` |
| `rework/tools/check_book.py:18-22` | Six English section labels, four medical box labels, four health-profession lenses | `template.sections[]`, `template.callouts[]`, `template.perspectives[]` |
| `rework/tools/check_book.py:23,83-97` | ASCII word tokenizer and English sentence splitting | `locale.tokenizer_profile`, `locale.sentence_terminators` |
| `rework/tools/check_book.py:39-49` | Literal `References` and `Self-Assessment` boundaries | `template.section_ids.references`, `template.section_ids.assessment` |
| `rework/tools/check_book.py:103-116` | `# Chapter N: Title` and literal box syntax | `template.chapter_heading_pattern`, `template.callout_syntax` |
| `rework/tools/check_book.py:120-132` | Exactly four lenses and ±20% balance | `template.perspectives.count`, `template.perspectives.balance_tolerance` |
| `rework/tools/check_book.py:136-146` | `LO` identifiers, 3–5 objectives, banned English verb `understand` | `template.learning_objectives.*`, `locale.discouraged_objective_verbs` |
| `rework/tools/check_book.py:150-199` | Ten Q-numbered MCQs, A–D only, no E, one `Case Question`, key counts 2–3, no three-letter run | `template.assessment.*` |
| `rework/tools/check_book.py:202-221` | Numeric square-bracket citation format | `template.citations.style` |
| `rework/tools/check_book.py:225-249` | Bold terms define glossary items; literal `Through Four Lenses` exception | `template.glossary.*`, semantic callout IDs |
| `rework/tools/check_book.py:252-253` | English `master-slave` ban and replacement | `locale.banned_terms[]` |
| `rework/tools/check_book.py:259-289` | `chNN`, `glossary.md`, exactly 11 chapters, `00-front-matter.md`, 17k–21k total, `errata-ledger.md`, literal `| open |`, minimum 120 glossary terms | `paths.*`, `template.chapter_manifest`, `template.total_word_budget`, `template.errata.*`, `template.glossary.minimum_terms` |
| `rework/tools/build_book.py:21-28` | Root/rework/output path and medical book title, subtitle, author | `paths.*`, `brief.title`, `brief.subtitle`, `brief.credits` |
| `rework/tools/build_book.py:30-32` | Sitka/Segoe UI fonts, palette, text width | `theme.fonts.*`, `theme.palette.*`, `theme.layout.text_width` |
| `rework/tools/build_book.py:35-44` | Medical callout labels and colours | `theme.callouts.<semantic_id>` |
| `rework/tools/build_book.py:45-51` | Three medical-AI parts, chapter spans, boxed and unlisted English sections | `template.parts[]`, `theme.boxed_section_ids`, `theme.toc_excluded_section_ids` |
| `rework/tools/build_book.py:204-237` | `en-GB` and left-aligned styles | `brief.output_locale`, `theme.direction`, `theme.alignments.*` |
| `rework/tools/build_book.py:289-317` | LTR option/reference/glossary indentation and alignment | `theme.lists.*`, `theme.direction` |
| `rework/tools/build_book.py:429-472` | Exactly four lenses in a 2×2 layout; literal `Through Four Lenses`, `Myth`, `Evidence` | `template.perspectives.*`, `labels.myth`, `labels.evidence`, `theme.perspective_layout` |
| `rework/tools/build_book.py:501-519` | Project-relative figure assumptions, PNG mirror directory, English `Figure N.N` captions | `paths.figures`, `build.figure_renditions`, `locale.figure_caption_pattern` |
| `rework/tools/build_book.py:569-573` | A4 and fixed margins/header/footer distances | `theme.page.*` |
| `rework/tools/build_book.py:598-653` | English section names and callout grammar drive rendering | Stable section/callout IDs in parsed intermediate representation |
| `rework/tools/build_book.py:663-703` | Cover detected by filename substring; English Q/LO grammar and A–E options | `theme.cover.asset`, `template.assessment.*` |
| `rework/tools/build_book.py:715-751` | Literal `References`, `Learning Objectives`, `Answers and Rationales` | `template.section_ids.*` |
| `rework/tools/build_book.py:761-805` | Fixed cover file, title-page layout, title/subtitle/author | `theme.cover.*`, `brief.*` |
| `rework/tools/build_book.py:805-825` | Four-profession audience line and named fictional-patient/clinical notice | `brief.audience_display`, `front_matter.notices[]` |
| `rework/tools/build_book.py:827-832` | English `Contents` and fallback message | `labels.contents`, `labels.update_toc_instruction` |
| `rework/tools/build_book.py:841-908` | `How to Use This Book`, `Chapter`, `Glossary`, `ch*.md`, and medical part structure | `labels.*`, `template.chapter_heading_pattern`, `paths.chapter_glob`, `template.parts[]` |
| `rework/tools/build_book.py:918-923` | Core metadata language `en-GB` | `brief.output_locale` |
| `rework/tools/build_book.py:928-964` | Microsoft Word COM, hidden Word instance, TOC styles, embedded fonts, PDF export settings | `build.backend`, `build.word_com.*`, `build.pdf.*` |
| `rework/tools/assemble.py:10-12` | Tool-relative root, `rework/`, root-level output basename | `--project`, `paths.rework`, `build.output_basename` |
| `rework/tools/assemble.py:21-23` | Rewrites `../images/` and `figures/` into root-specific destinations | Canonical project-relative asset resolver; remove string replacement |
| `rework/tools/assemble.py:28-34` | `00-front-matter.md`, `ch*.md`, `glossary.md`, `Contents`, `How to Use This Book` | `paths.*`, `labels.contents`, `template.section_ids.how_to_use` |
| `rework/tools/assemble.py:37` | Only `images/` and `rework/figures/` count as valid asset roots | `paths.allowed_asset_roots[]` |
| `rework/tools/verify_refs.py:17,44-48` | ASCII title tokenizer, first six words, 60% overlap | `references.title_match.*`, with language-aware/manual modes |
| `rework/tools/verify_refs.py:20-23` | English `References` and numbered-entry grammar | `template.section_ids.references`, `template.references.entry_pattern` |
| `rework/tools/verify_refs.py:27-40` | Crossref endpoint, user agent, five retries, 15-second timeout, fixed backoff | `references.providers.crossref.*` |
| `rework/tools/verify_refs.py:53-57` | DOI patterns; every no-DOI reference succeeds despite the stated law/guidance restriction | `references.identifier_patterns`, `references.no_doi_policy` |
| `rework/tools/renumber_refs.py:8,30-46` | Numeric square-bracket citations and English `## References` | `template.citations.style`, `template.section_ids.references` |
| `rework/_template.md:1-52` | Medical-AI chapter title, running patient, medical background, four professions, safety box, ten A–D questions and English headings | Generated project template from stable semantic config |

## Top 5 changes

1. **Put a code-enforced state machine beneath every slash command.** Bind approvals to hashes of the brief, rubric, template, agents, and source; invalidate downstream work when any input changes.

2. **Restore ingest/conversion as an explicit stage.** Include conversion-fidelity QA and make `/book-design` distinct from the approved intake brief.

3. **Define versioned schemas with stable semantic IDs.** Separate job facts (`brief.json`), scoring (`rubric.json`), content grammar (`template.json`), rendering (`theme.json`), and workflow state (`state.json`).

4. **Replace “identical PASS” with structured golden and negative regression tests.** Preserve the medical project as a live first project, but place immutable fixtures and expected diagnostic reports under `tests/fixtures/`.

5. **Treat Arabic as a full locale and rendering profile.** Add Unicode tokenization, localized grammar, bidi DOCX XML, RTL TOC/list/table handling, Arabic reference policy, mixed-script tests, and rendered DOCX/PDF visual QA.