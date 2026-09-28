---
type: execution-plan
version: 3.4
status: approved-pending-execution
last_updated: 2026-09-25
---

# Book Harness: Generalise the Textbook Evaluation and Rework Pipeline

> [!important] What this document is
> This is the **ticket**. It is linear: STEP 1 → 2 → … → 13 → GOAL. A step starts only when two things are true: the previous step's exit criteria are met, and its handoff artifact exists. Each agent reads its own step, the Standing Rules and the **Definitions** section. From STEP 5 on, it also reads its **mandatory inputs** (see Definitions). Then it executes.
>
> **Binding constraint on every step:** `docs/harness/VISION.md`. Read it before touching anything.
>
> **Status:** approved by the user at commit `23d819f` (DEC-026), after 6 Codex review rounds. From now on, each artifact gets one Codex review and Claude fixes the findings through the Fix Protocol (DEC-030). That amendment was made on the user's own instruction, so it needs no separate re-approval. **STEP 1 is released.** The intake questionnaire is already approved (DEC-027). Execution sessions may commit, but never push (DEC-028).

## Why this plan exists (the problem being solved)

`D:\yasser` was built for one job. The job was to evaluate Dr. Elkholy's *AI in Medicine* manuscript (46/100) and rebuild it as *AI in Health Care: An Interprofessional Introduction*. Everything in the workspace is wired to that book:

- `CLAUDE.md` and the rubric are medical.
- `check_book.py` hardcodes "Through Four Lenses" and four health professions.
- `build_book.py` hardcodes the title, colours and cover line.
- The converter hardcodes `D:\yasser` paths.

The user wants to run **the same pipeline on other textbooks in any science, in Arabic or English, including translation both ways**. The run must be cheap and high quality. It must ask the user about the book first and do no work before that.

---

## Definitions (used by every exit criterion)

- **Stage receipt.** An entry in `projects/<book>/state.json` for one completed stage. It records:
  - the SHA-256 of every input file and output file, where JSON is hashed in canonical form;
  - the tool version (git SHA);
  - the time;
  - `status: ok|failed`.
  
  A receipt is **stale** if any input hash no longer matches. A stale receipt blocks every downstream stage.
- **User approval.** A record in `state.json`. It holds the approved artifact hashes, and a DEC ID. The DEC ID logs the user's words in this conversation. Only Claude writes it, and only right after the user explicitly approves, in chat, the exact files shown. Tests use fixture projects with fixture approvals. They never edit a real project's state.
- **Codex review done (DEC-030).** Each artifact gets **one** Codex review. That covers every spec, contract, plan and implementation step.
  - **Mode:** read-only, through `codex-delegate`.
  - **Report:** Codex emits its report as its final message. Claude saves it verbatim to `docs/harness/reviews/step<N>-review.md`. The header holds `reviewed_commit`, `verdict` and `open_blocker_major`. Claude never alters Codex's verdict.
  - **No re-review.** Claude fixes the findings using the **Fix Protocol** below.
  - **Records:** each fix is logged in `docs/harness/reviews/step<N>-fixes.md`.
  - **When the review counts as done:** once the fixes file shows every blocker and major finding as either `fixed + verified` or `ruled by user`.
- **Fix Protocol (DEC-030).** Apply it to every review, in this order:
  1. **Take the review.** Read every finding, and re-open each cited file:line to confirm the finding is real. Record any finding that is false as `rejected`, with the evidence.
  2. **Think deeply.** For each real finding, identify the **root cause**, not just the symptom. Ask why the defect got in, and what else that same cause would have broken.
  3. **Hunt for more defects.** Search beyond the cited spot for the same class of defect: sibling callers, parallel steps, other files built on the same assumption. Also look for defects the review missed. Log each new one with its own ID, marked `found-by-claude`.
  4. **Fix.** Fix the root cause once, where every caller routes through it. Do not patch each symptom separately.
  5. **Verify.** Run the test, command or check that would fail if the fix were wrong, and record both the command and its result.

  For each finding, `step<N>-fixes.md` records: ID | real / rejected | root cause | siblings found | fix | verification command → result.
- **Mandatory inputs for STEPS 5–13.** Before starting, an implementation agent reads all four of these:
  1. its exact approved task(s) in `docs/superpowers/plans/2026-09-25-book-harness.md`;
  2. the approved specs and contracts from STEPS 1–3 that the task names;
  3. the approval DECs and SHAs for the plan and the specs;
  4. the predecessor step's handoff.

  **The plan supplies every command, expected exit code and output path.** Where the plan and this ticket disagree, the agent stops and logs a blocker.
- **Receipts valid.** For a given stage set, every mandatory receipt must meet four conditions:
  - it has `status: ok`;
  - its input hashes are current;
  - its tool SHA is the expected one;
  - it carries no invalidation marker.

  All four are checked by one command: `python harness/run_stage.py --project <p> verify [--through <stage>]`. It checks intake and design approval hashes that exist up to the boundary, and every mandatory receipt up to the boundary. With no `--through` flag, it checks all stages. It exits 0 only when everything checked passes.
- **Gate commands.** Each exit criterion names its commands with expected exit codes, either in this ticket or in the approved plan task it points to. "Done" means the reviewer re-ran those commands and got the expected results.

---

## Standing Rules (apply to every step, every agent)

1. **The vision is binding.** See `docs/harness/VISION.md`. Suggestions are allowed. Deviation is not.
2. **No guessing.** Genuine blockers escalate and get logged in the Blocker Register. Cosmetic calls are the agent's own.
3. **Never self-mark as approved.** Only the user approves (see Definitions). Agents write `pending`.
4. **Evidence, not assertion.** Cite each kind of claim to a specific source:
   - Factual requirements, migration assertions and acceptance results: a file:line, a stage receipt or a test.
   - Design choices: a DEC entry.
   - Scientific claims inside books: an authoritative source.
5. **Minimal edits.** Update only what the step requires. **Never modify** the original manuscript (`AI_in_Medicine- Assistant Prof Dr Shereen Elkholy.{md,docx}`) or the finished interprofessional outputs. The only exception is the manifest-listed `git mv` in STEP 6.
6. **Log the handoff.** Each step ends with its handoff artifact plus a filled row in `docs/harness/LEDGER.md`: owner, commit SHA, receipt/review paths.
7. **The intake gate cannot be waived (DEC-005).** No stage after `intake` may run on a book unless user approval exists and its hashes match. That approval must cover `brief.json`, `rubric.json`, `template.json`, `theme.json` and the domain agent overlays.
   - This is enforced **in code, in every executable**, including legacy tools. Skill prose does not count.
   - No `rework` may run without a second user approval of the design hash.
   - Pressures that will try to break this rule, none of which waive it:
     - "the book is obviously X, just start"
     - "it's only a test"
     - "re-hashing after a tiny edit is pedantic"
8. **No domain leaks into shared code.** Shared production code and schemas under `harness/` contain no profession names, box labels, clinical terms, book titles, author names or absolute paths. All of these come from project config. The pressure to resist: "it already works for the medical book".
9. **Claude implements, and Codex reviews each implementation step (DEC-017).** Codex reviews read-only through `codex-delegate`. Claude lands the commits.
10. **Honest dependencies.** The control plane and checker use Python stdlib only. Conversion and build keep python-docx, Pillow, pywin32 and Microsoft Word. The chemistry pack adds RDKit as an optional dependency group. Runtime code **diagnoses** a missing dependency and never installs one silently.
11. **Cheapest execution at highest quality (DEC-014, DEC-015).**
    - **Inline by default.** Work happens in the main session.
    - **Spawning a Claude subagent** requires a stated reason that inline work cannot cover:
      - context isolation for a very large read, when only its conclusion is needed;
      - genuinely independent parallel work.
    - **Cap:** at most **2 Claude subagents** (Agent tool or workflows). **Codex dispatches do not count** (DEC-015), and the main session does not count.
    - **Forbidden:** "one agent per chapter", and fan-outs of 4–6 agents.
    - **Logging:** each spawn is logged with its reason in the step handoff.
    - **The harness encodes this rule too.** Its skills, `CLAUDE.md` and stage docs carry it. The evaluate stage replaces the first run's 4 parallel reviewers (`SESSION_SUMMARY.md` §1) with inline persona passes plus one Codex review.
    - **Pressures that will try to break it:** "parallel is faster", "the book is long", "each persona deserves its own agent". None of these is a reason.
12. **Use the installed skills (DEC-016) where they fit, rather than re-implementing them:**
    - `markitdown` for ingest;
    - `citation-management` and `paper-search` for reference checks;
    - `rdkit`, `matplotlib`, `scientific-visualization` and `diagram-design` for figures;
    - `peer-review` and `master-instructional-design` (pre-installed) for evaluation and design.
    - `dataviz` for chart style, only if the host session provides it. It is a built-in skill, not a file on disk, so nothing may depend on it.
    
    Never use `scientific-schematics` or any paid AI image generation for book figures. Images the user brings, AI-made ones included, are author-supplied figures and carry no AI label (DEC-044).

13. **One Codex review per artifact, then Claude fixes it (DEC-030; this supersedes DEC-025).**
    - Claude dispatches exactly **one** Codex review per artifact.
    - Claude resolves the findings through the Fix Protocol (see Definitions): take the review, think deeply, hunt for more defects, fix, then verify.
    - Claude never dispatches a second review round.
    - Minor findings that are not fixed are logged as `accepted-minor`. They do not block.
    - **Pressures that will try to break this rule, and why they do not:**
      - "Let Codex check my fixes": verifying the fixes is Claude's job, done by running them.
      - "One more round would be safer": the ticket's own rounds 3–6 found diminishing, wording-level issues (DEC-025, DEC-030).

---

## STEP 0: Scope calls

### 0a: Ruled by the user *(binding)*

1. **Stages:** all six stages are covered (DEC-001).
2. **Layout:** one repo, with `projects/<book>/`. The medical book is the first project (DEC-002).
3. **Rubric:** fixed generic pillars plus generated domain pillars, approved before evaluation (DEC-003).
4. **Content:** chapter-based university textbooks (DEC-004).
5. **Intake:** intake comes first, and no work happens before it (DEC-005).
6. **Arabic now** (DEC-006). **Translation now** (DEC-007).
7. **Sciences:** all sciences, culturally and in tooling, with figures drawn and laid out (DEC-008).
8. **Chemistry pack:** built with the core (DEC-009).
9. **Codex reviews** the design and ticket (DEC-010), and each implementation step, while Claude implements (DEC-017).
10. **Cost:** cheapest execution. Max 2 Claude subagents, and Codex does not count (DEC-014, DEC-015).
11. **Skills:** the 8 skills are installed. `scientific-schematics` is excluded (DEC-016).
12. **E2E run:** on a real book the user will send (DEC-018).
13. **Interface contracts:** the Arabic and translation interfaces are designed before the plan (DEC-019).

### 0b: Assumed by the agent *(not binding; overturn cheaply)*

1. **Approach A** (DEC-011). If wrong, STEP 1 re-plans the control plane.
2. **Codex design-review changes as triaged** (DEC-012, amended by DEC-020). If wrong, the affected items are re-added or dropped in STEP 1.
3. **Design section 1 is accepted** (DEC-013). If wrong, STEP 1 revisits the layout.
4. **Implementation order:** core → Arabic → translation. The contracts for all three are fixed first, in STEPS 1–3. If wrong, the implementation steps get reordered.
5. **Doc locations:** specs and plans go in `docs/superpowers/`, and harness docs in `docs/harness/`. This is cosmetic.
6. **Charts:** matplotlib charts are core, not a pack. If wrong, they move to a pack.

### 0c: Open

**Q1. Approve this ticket and assumptions 0b.1–0b.3?** **RESOLVED** by DEC-026: approved at `23d819f`, together with 0b.1–0b.6. The approval DEC records the exact commit SHA of `TICKET.md`, so the version label does not matter. 

**Q2. The real book for STEP 12.** Its source files and language pair are needed before STEP 12. *It does not block any earlier step.* **Deferred** (DEC-029): the user will send it.

---

## STEP 1: Claude: core harness design spec (with the intake questionnaire)

**Owner:** Claude.
**Starts when:** 0c Q1 is approved.

**Task:** Finish the brainstorming design for the **core** and write the spec. The spec covers these parts:

**(a) Layout.** The agreed layout, including `harness/figures/`.

**(b) Stage contract.** One table row per stage: `new`, `intake`, `ingest`, `evaluate`, `design`, `rework`, `build`, `audit`. Each row gives:
- inputs and outputs;
- the receipt fields;
- preconditions;
- the downstream stages it invalidates;
- failure and resume behaviour;
- QA evidence.

**(c) Approvals.** There are two user approvals: intake, and design.

**(d) Versioned schemas.** One schema each for `brief`, `rubric`, `template` and `theme`, with field lists.

**(e) Rubric core.**
- The fixed pillars.
- The reserved weight split between generic and domain pillars.
- An overlap rule, so the same defect is not scored twice.
- A rubric digest, so the baseline score and the rescore use the same rubric.

**(f) Domain-agent overlay format.** Small approved overlays on shared personas, never free-form generated agents.

**(g) Figure system and chemistry pack interface.**

**(h) Evaluate stage.** It is designed under Rule 11: inline persona passes, then one Codex review.

**(i) Regression strategy.**
- A golden JSON report with stable check IDs.
- A comparator schema.
- Mutation tests.
- Positive-config test fixtures for books with no MCQs, no glossary, no cases, no lenses and no errata.
- Scoped leak scanning.

**(j) Inventory mapping.** One row for every entry in the Codex hardcoded inventory (`docs/harness/codex-design-review-2026-09-25.md`, "Hardcoded values inventory"). Each row gets a stable ID `INV-NN` and one of two targets: a config key, or `removed`.

**(k) Locale and translation extension points.** These are named here and filled in by STEP 2.

**The intake questionnaire is already approved**: `docs/harness/INTAKE_QUESTIONNAIRE.md` (DEC-027). The spec turns A–M into the `brief` schema.

**Depth:** design only. No code, no schema files, no moves.

**Mandatory reading:**
- `docs/harness/VISION.md`
- `docs/harness/DECISIONS.md`
- `docs/harness/codex-design-review-2026-09-25.md`
- `docs/harness/reviews/ticket-review-1.md`
- `docs/superpowers/specs/2026-09-24-interprofessional-rework-design.md`
- `docs/superpowers/plans/2026-09-24-interprofessional-rework.md`
- `EVALUATION_RUBRIC.md`
- `rework/tools/*.py`
- `convert_docx_to_md.py`

**Scope lock: do NOT:**
- Write code. Doing it now would freeze interfaces before STEP 3 reviews them.
- Design Arabic or translation internals. That is STEP 2.

**Output:** `docs/superpowers/specs/2026-09-25-book-harness-core-design.md`, committed.

**Exit criteria:**
- The spec's `brief` schema covers every questionnaire item A–M (DEC-027).
- The spec is committed.
- The inventory table has one row per inventory entry, and no row is unmapped. A reviewer can check this by counting rows against the Codex inventory.
- `grep -nE "TBD|TODO|\?\?\?"` on the spec returns nothing.

---

## STEP 2: Claude: Arabic-locale and translation interface contracts

**Owner:** Claude.
**Starts when:** STEP 1 is committed.

**Task:** Write **interface-level** specs. These define what the core must expose, and they are designed before the plan (DEC-019).

**Arabic locale spec** (drawn from Codex design review §5) must cover:
- a locale profile: tokeniser, sentence terminators including `؟` and `…`, a digit policy, readability thresholds, and labels bound to stable section IDs;
- a theme direction and bidi contract: `w:bidi`, `w:rtl`, `w:lang ar-EG`, `w:rFonts/@w:cs`, `w:szCs` and `w:bidiVisual` for tables;
- RTL rules for lists, tables and the TOC;
- an Arabic reference policy that separates DOI existence from title match;
- the acceptance corpus it requires.

**Translation spec** must cover:
- where translation sits in the stage graph;
- the bilingual termbase schema and when it gets approved;
- a traceability map from source chapter to target chapter;
- a translation review gate run by a different model;
- **both directions: EN→AR and AR→EN**.

**Depth:** interfaces, schemas and acceptance criteria. No internals, no code.

**Output:**
- `docs/superpowers/specs/2026-09-25-arabic-locale-contract.md`
- `docs/superpowers/specs/2026-09-25-translation-contract.md`

Both are committed. If the core spec's extension points change, the core spec is updated in the same commit.

**Exit criteria:**
- Both files are committed.
- Each contract field maps to a named core-spec extension point.
- The grep for TBD/TODO returns nothing.

---

## STEP 3: Codex: review of the three specs, then user approval of the final hashes

**Owner:** Codex reviews, Claude triages and fixes, and the user approves.
**Starts when:** STEP 2 is committed.

**Task:** Codex reviews the three specs together, read-only, against:
- the vision;
- both earlier Codex reviews;
- the current tools.

Each finding gets a stable ID. Claude verifies every file:line that Codex cites, triages each finding (accept, reject with a reason, or ask the user) and fixes the specs. Claude applies the Fix Protocol. There is no second review round (DEC-030). Finally, the user approves the final spec commit.

**Scope lock: do NOT:** start the plan, or edit code.

**Output:**
- `docs/harness/reviews/step3-review.md` and `step3-fixes.md`
- a DEC entry recording the user's approval of the spec commit SHA

**Exit criteria:**
- Codex review done.
- The user approval DEC exists and names the commit SHA.

---

## STEP 4: Claude: implementation plan

**Owner:** Claude, using `superpowers:writing-plans`.
**Starts when:** STEP 3 is approved.

**Task:** Write a task-by-task plan for STEPS 5–11. Include:
- TDD steps;
- the exact gate commands with expected exit codes;
- one commit boundary per task;
- the migration manifest format;
- preflight checks.

Execution is Claude inline (DEC-017).

**Output:** `docs/superpowers/plans/2026-09-25-book-harness.md`, and a DEC entry recording the user's approval of the plan commit SHA.

**Exit criteria:** the user approval DEC exists and names the plan SHA.

---

## STEP 5: Claude: preflight and medical baseline freeze

**Owner:** Claude.
**Starts when:** STEP 4 is approved.

**Task:**
- **(a) Preflight script.** Write `harness/preflight.py`. It checks:
  - Python packages;
  - Word COM;
  - required fonts;
  - write locks.
  
  It exits non-zero and names what is missing. **Stop the ticket if preflight fails.**
- **(b) Baseline capture script** `harness/tools/capture_golden.py --project <p> --out <file>`. It records the current medical rework into `tests/fixtures/ai-in-medicine/golden.json`:
  - every checker check with its measured values;
  - words per chapter;
  - the chapter list;
  - reference counts;
  - image resolution;
  - `verify_refs` output;
  - DOCX package facts;
  - PDF page count and bookmarks;
  - hashes.
  
  The hashes are **semantic**: volatile fields such as timestamps and docProps are excluded and listed. The script also stores an immutable copy of the sources in `tests/fixtures/ai-in-medicine/src/`.

**Scope lock: do NOT:** change any tool's behaviour. This includes the `verify_refs` no-DOI bug, which is recorded as-is.

**Exit criteria:**
- Preflight exits 0.
- Running the capture twice produces byte-identical `golden.json`.
- Codex review done.

---

## STEP 6: Claude: manifest-driven migration

**Owner:** Claude.
**Starts when:** STEP 5 is done.

**Task:**
- **(a) Manifest.** Commit `docs/harness/migration-manifest.json`. It has one `source → destination` entry per file, for the medical book's files only.
  - The root `CLAUDE.md` is **reserved**. This step never moves it, because STEP 7 copies it.
  - The user approves the manifest. The approval is a DEC entry that names the manifest's SHA-256 and commit SHA.
  - **Commit A must not start until that DEC exists.**
- **(b) Commit A: pure moves.** `git mv` exactly the manifest's files.
  - Destinations must not exist beforehand.
  - Pre and post hashes must be identical.
  - The relative layout is preserved: `images/` sits beside `rework/`.
- **(c) Commit B: path fixes only.** Only files on an allowlist in the manifest are touched.

After the moves, re-run the baseline capture.

**Scope lock: do NOT:** generalise tools, or edit content.

**Output:** the manifest, two commits, and `docs/harness/reviews/step6-golden-diff.md`.

**Exit criteria:**
- The manifest-approval DEC exists and names the manifest SHA-256 and commit SHA.
- `git show --stat` for commit A shows renames only.
- Commit B touches only allowlisted files.
- The golden diff contains only the fields in the manifest's `expected_diff` allowlist.
- Codex review done.

---

## STEP 7: Claude: control plane, gates on every executable, and the `CLAUDE.md` split

**Owner:** Claude.
**Starts when:** STEP 6 is done.

**Task:**
- **Control plane.** Build:
  - `harness/state.py`, for receipts, approvals, staleness and invalidation;
  - `harness/run_stage.py`;
  - `harness/schemas/`;
  - `harness/rubric_core.json`;
  - `harness/agents/`, with the shared personas moved in;
  - `.claude/skills/book-*`, as thin wrappers over `run_stage.py`.
- **Gates on every executable.** Every executable calls the gate, and that includes the **legacy tools** still under `projects/ai-in-medicine/`. Each one requires an explicit `--project` inside `projects/`.
- **Intake flow.** Implement the intake flow using the questionnaire approved in STEP 1.
- **Design approval.** Implement design approval.
- **`CLAUDE.md` split, as its own commit:**
  1. Copy the current root `CLAUDE.md` verbatim to `projects/ai-in-medicine/CLAUDE.md`.
  2. Write a new root `CLAUDE.md` that describes the harness and Rules 7, 8 and 11.
- **Medical project onboarding.**
  - Claude writes `projects/ai-in-medicine/{brief,rubric,template,theme}.json` and `projects/ai-in-medicine/agents/*`. Together they reproduce the old hardcoded behaviour.
  - Claude presents all of them to the user in chat.
  - Approvals are written only after the user approves them. The approval is a DEC entry.
- **Task split.** The plan splits this step into separately committed, separately tested tasks:
  1. state and schemas;
  2. runner and skills;
  3. legacy gate shims;
  4. medical onboarding;
  5. the `CLAUDE.md` split.

  One Codex pass covers the whole batch, and only after every task's tests pass.

**Scope lock: do NOT:** generalise tool internals. That is STEP 8.

**Exit criteria:** a **bypass matrix test** exits 0. It enumerates every executable and asserts a non-zero exit plus the named error in each of these cases:
- no approval;
- an edit after approval;
- a stale upstream receipt;
- a missing design approval before `rework`;
- a path outside `projects/`.

Also:
- The `CLAUDE.md` diff has been reviewed.
- The medical-onboarding approval DEC exists.
- `python harness/run_stage.py --project projects/ai-in-medicine verify --through intake` exits 0. The intake approval hashes match.
- Codex review done.

---

## STEP 8: Claude: generalise the tools and implement ingest

**Owner:** Claude.
**Starts when:** STEP 7 is done.

**Task:**
- **Config-driven tools.** Move the tools to `harness/tools/` and drive them from config, following the INV mapping.
  - The checker emits JSON with stable check IDs.
  - Fix the `verify_refs` no-DOI policy.
- **Ingest stage.** Implement ingest:
  - source custody copy;
  - `source-manifest.json`;
  - `conversion-report.json`, a fidelity report covering headings, tables, equations, footnotes, figures and omitted text;
  - `markitdown` used for non-docx input.
- **Ingest fixtures.** Add DOCX fixtures containing each high-risk structure, each with literal expected outcomes.
- **Positive-config fixtures.** Add them for books with no MCQs, no glossary, no cases, no lenses and no errata.
- **Mutation set.** Each mutation must produce the check ID that the plan names for it. The minimum set:
  - remove a required callout;
  - break an image path;
  - skew the answer key;
  - reopen an erratum;
  - break a citation;
  - drop a lens (only where lenses are configured);
  - exceed the word budget.
- **Task split.** The plan splits this step into separately committed tasks:
  1. checker and assemble generalisation;
  2. build generalisation;
  3. the `verify_refs` policy;
  4. ingest and fidelity.

**Scope lock: do NOT:** add Arabic parsing or rendering. That is STEP 10.

**Exit criteria:**
- `python -m unittest` exits 0. The suite asserts that each mutation yields its named check ID and a non-zero checker exit.
- The medical golden report matches STEP 6. The only diff is the listed `verify_refs` change.
- Positive-config fixtures pass.
- The scoped leak scan (defined in the spec) over shared production code exits 0.
- Codex review done.

---

## STEP 9: Claude: figure system and chemistry pack

**Owner:** Claude.
**Starts when:** STEP 8 is done.

**Task:**
- **Figure system.** Build `harness/figures/`:
  - figure source code lives in `projects/<book>/figures/src/`;
  - rendering to SVG and PNG;
  - numbering, captions, source and licence, and alt text;
  - a figure checker;
  - a `needs-author-asset` flag for figures the harness cannot honestly generate.
- **Chemistry pack.** Build `harness/figures/packs/chemistry/` as an optional dependency group with pinned RDKit:
  - a Windows preflight smoke test;
  - SMILES rendering to structures, with sanitisation;
  - reaction SMARTS rendering to schemes;
  - a PubChem cross-check. Tests use mocked responses. Live mode has a timeout and a cache, and when offline the result is marked `unverified`, never `pass`.
- **Visual evidence.** Rendered sample PNGs are saved under `docs/harness/reviews/step9-evidence/` for review.

**Scope lock: do NOT:** build map or circuit packs (DEC-009).

**Exit criteria:**
- Tests pass, including one invalid SMILES that must fail.
- The evidence PNGs are committed.
- Codex review done.
- Codex inspected every committed evidence PNG.

---

## STEP 9b: Claude: absorb the Dr. Mo book-designer skill (DEC-043, DEC-044, DEC-045)

**Owner:** Claude.
**Starts when:** STEP 9 is done. Runs before STEP 10 (DEC-045).

**Task:** Take what the skill in `dr mo skill/SKILL.md` does better, as shared code driven by project config and packs; leave its book-specific content out of `harness/` (Standing Rule 8). The plan's STEP 9b tasks:
- **9b.1** One block grammar that both the DOCX and the HTML writer consume, plus inline subscript and superscript (`H~2~O`, `Ca^2+^`).
- **9b.2** The HTML PDF engine (`theme.build.pdf.engine: "html"`, headless Edge): designed cover, title page, contents with page numbers, running heads, chapter pages, bookmarks and PDF metadata. `word_com` stays the default.
- **9b.3** PDF quality gates (`check_pdf.py`) for both engines, and checkpoint PNGs.
- **9b.4** Annotated figures (`diagram.annotated`): numbered callouts with leader lines on a base image, and a key under the caption.
- **9b.5** Checker IDs: raw LaTeX left in text, prose runs longer than the configured limit, and (chemistry pack) formulas written without subscripts.
- **9b.6** An `editorial-book` fixture built with the HTML engine, and evidence PNGs.

**Scope lock: do NOT:** render RTL in the HTML engine (STEP 10); generate images with any AI service (DEC-044); copy the skill's palette, fonts, reference book or regulations into `harness/`.

**Exit criteria:**
- Tests pass; the medical build still matches its golden (the DOCX is written through the shared grammar).
- Every new check ID has a failing fixture.
- The `editorial-book` fixture builds with the HTML engine, passes `check_pdf.py`, and its evidence PNGs are committed under `docs/harness/reviews/step9b-evidence/`.
- Codex review done, and it inspected every evidence PNG.

---

## STEP 10: Claude: implement the Arabic locale per its STEP 2 contract

**Owner:** Claude.
**Starts when:** STEP 9 is done.

**Task:** Implement the approved Arabic contract. Build an Arabic fixture book and a mixed-script corpus.

**Exit criteria:**
- The Arabic fixture passes the checker.
- It builds to DOCX and PDF.
- Rendered pages are saved as evidence under `docs/harness/reviews/step10-evidence/`. They include a TOC page, a table page, a list page and a mixed-script page.
- Codex review done, and the review inspected the evidence.

---

## STEP 11: Claude: implement translation per its STEP 2 contract, in both directions

**Owner:** Claude.
**Starts when:** STEP 10 is done.

**Task:** Implement the translation stage, the termbase, traceability and the review gate. Build **two** fixtures: EN→AR and AR→EN.

**Exit criteria:** both fixtures pass all four checks:
- termbase consistency;
- traceability;
- preservation of references and mixed script;
- a translation review by a different model.

Also:
- Codex review done.
- The user has seen both outputs.

---

## STEP 12: Claude with the user: end-to-end run on the user's real book

**Owner:** Claude, with the user, who takes part in intake and approvals.
**Starts when:** all three are true:
- STEP 11 is done.
- 0c Q2 is resolved, and the source files are present and hashed.
- The user is available for the intake conversation.

**Task:** Run `new` → `audit` for real. Intake is a genuine conversation, never a pre-filled brief. Record failures as findings, fix each one in a reviewed follow-up commit, and never tune a tool mid-run to force a pass.

**Output:** `projects/<book>/` and `docs/harness/reviews/step12-e2e-report.md`.

**Exit criteria:**
- The initial gate refusal before approval was observed and recorded.
- `python harness/run_stage.py --project projects/<book> verify` exits 0, which means every receipt is valid (see Definitions).
- The audit ran against the baseline rubric digest.
- Zero audit findings remain unaccepted.
- The user has accepted, or rejected with recorded reasons, the built PDF.

---

## STEP 13: Codex: independent harness audit (one pass), then Claude fixes via the Fix Protocol

**Owner:** Codex (read-only). Claude saves the report and applies fixes.
**Starts when:** STEP 12 is done.

**Task:** Audit the whole harness against `VISION.md` and the GOAL. Cover:
- gate bypass attempts;
- domain leakage;
- Rule 11 compliance in the skills and docs;
- the Arabic and translation fixtures;
- the figure system;
- the docs.

Codex audits once. Claude resolves the findings through the Fix Protocol. There is no re-audit (DEC-030).

**Exit criteria:**
- `docs/harness/reviews/step13-review.md` and `step13-fixes.md` exist.
- Every blocker and major finding is either `fixed + verified` or `ruled by user`.
- `python harness/run_stage.py --project projects/<book> verify` still exits 0 after the fixes.
---

## GOAL

The user drops a chapter-based university textbook into `projects/<book>/`. It can be in any science, in Arabic or English. Claude then:
1. Interviews the user.
2. Refuses to proceed until the intake is approved.
3. Runs ingest → evaluate → design, then stops for a second, design approval.
4. Runs rework → build → independent audit. It translates where asked, and generates figures, chemistry included, from code.
5. Stays cheap throughout: inline by default, and no more than 2 Claude subagents.

The medical book reproduces its golden report from `projects/ai-in-medicine/`.

---

## Blocker Register

| # | Step | Raised by | Date | The blocker | Resolution |
|---|---|---|---|---|---|
| 1 | 0 | Claude | 2026-09-25 | This ticket (by commit SHA) and 0b.1–0b.3 not yet approved (0c Q1) | **Resolved**: DEC-026 approved it at `23d819f` |
| 2 | 12 | Claude | 2026-09-25 | Real book source and language pair (0c Q2) | **Open, but only blocks STEP 12** (DEC-029) |
| 3 | 0 | Codex review 1 | 2026-09-25 | Legacy-tool gate bypass; missing design approval; Arabic/translation contracts too late | Fixed in v2 (STEPS 2, 7; Definitions). Codex review 2 marked all 3 resolved |
| 4 | 0 | Codex review 2 | 2026-09-25 | The review-pass definition was circular, plus 6 major findings | Fixed in v3 (DEC-021). Codex review 3 marked 10 of 11 resolved |
| 5 | 0 | Codex review 3 | 2026-09-25 | STEP 13 compared against HEAD; approval question pointed at v2; `verify` had no stage boundary | Fixed in v3.1 (DEC-022). Codex review 4 marked 3 of 5 resolved |
| 6 | 0 | Codex review 4 | 2026-09-25 | A path-only check could not isolate the ledger hunks; the approval question still used a version label | Fixed in v3.2 (DEC-023): the ledger moved to its own file, and approval is now bound to a SHA. Codex review 5 marked 6 of 7 resolved |
| 7 | 13 | Codex review 5 | 2026-09-25 | An endpoint `git diff` misses a forbidden edit that was later reverted | Fixed in v3.3 (DEC-024). Codex review 6 found the check still passed when `git log` failed; Claude fixed that in v3.4, as the cap allows (DEC-025) |
| 8 | 9b | Claude | 2026-09-28 | PDF engine for the Dr. Mo design: keep Word, or add HTML/Edge for the PDF | **Resolved**: DEC-043, option (b) |

## Step Ledger

Moved to `docs/harness/LEDGER.md` (DEC-023).

## Related

- `docs/harness/VISION.md`
- `docs/harness/DECISIONS.md`
- `docs/harness/codex-design-review-2026-09-25.md`
- `docs/harness/reviews/ticket-review-1.md`
- `docs/harness/reviews/ticket-review-2.md`
- `docs/harness/reviews/ticket-review-3.md`
- `docs/harness/reviews/ticket-review-4.md`
- `docs/harness/reviews/ticket-review-5.md`
- `docs/harness/reviews/ticket-review-6.md`
- `docs/harness/LEDGER.md`
