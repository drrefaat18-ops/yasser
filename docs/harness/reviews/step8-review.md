# STEP 8 Codex review

One read-only Codex pass over tasks 8.1-8.4 (commits 80a22a9..4f81589), run `yasser-2026-09-26T21-07-49-814Z`, thread `01a0df8b-c875-7c90-8e86-3c90cff74ae6`. Report verbatim below.

reviewed_commit: 4f81589c8162fc88baf473285f450ec337d4bfb2
verdict: fail
open_blocker_major: 5

## Findings

| ID | Severity (blocker/major/minor) | File:line | Problem | Concrete fix |
|---|---|---|---|---|
| S8-01 | blocker | `harness/tools/config.py:9` | Configured paths are joined without resolving and verifying project containment. `template.paths.chapters`, `normalized_source`, `assets`, allowed roots, and chapter-plan filenames can contain `..` or absolute paths; gated tools such as ingest and `renumber_refs` can consequently read or overwrite files outside `projects/<slug>/`, bypassing the core §1.1 boundary. | Add one canonical safe project-path resolver using `resolve()` plus `is_relative_to(project.resolve())`; route every config, chapter-plan, contract, cover, and receipt path through it. Reject unsafe paths during intake/design completion and add CLI mutation tests proving reads and writes outside the project are refused. |
| S8-02 | major | `harness/tools/convert_docx.py:238` | Text fidelity compares unlike populations. Source text counts only body `w:t`, while output text includes inlined equation `m:t` and footnote-body text. Existing fixtures show inflation (`179 → 185` for equations and `221 → 247` for footnotes), so unrelated body text can be lost while `text.status` remains `ok`. | Count equivalent semantic text on both sides, or exclude generated equation/footnote annotation content from the output text count. Add fixtures combining a long footnote/equation with deliberately dropped body prose and require `text: lost`. |
| S8-03 | major | `harness/tools/check_book.py:222` | A required callout is considered present when its syntax occurs anywhere in the document. If the actual marker line is removed but the literal is mentioned mid-prose, `n == 0` while both `TPL-CALLOUT-MISSING` and `TPL-CALLOUT-COUNT` report pass. | Base presence on the already-computed line-marker count: fail `TPL-CALLOUT-MISSING` when `required and n == 0`. Add a mutation where the syntax remains only inside prose or a fenced block. |
| S8-04 | major | `harness/tools/build_book.py:560` | The builder does not consume `check_book.parse()` as required by Task 8.2 and INV-30; it implements a second Markdown parser. That parser also emits the hardcoded callout label `"Note"` and displays raw `Q`/`LO`/option labels instead of `theme.labels.*` and `option_display_labels`. The golden passes only because the medical configuration uses those same literals. | Expand the shared `Parsed` representation as needed and render sections, callouts, questions, objectives, and options by semantic IDs. Remove the independent grammar and all fallback/display literals; add a build test with renamed UI labels and distinct option display labels. |
| S8-05 | major | `harness/tools/check_book.py:324` | Schema-valid enabled feature configurations can crash instead of returning a checker report. For example, MCQs enabled with the schema-permitted `max_run: null` raises `TypeError`; nullable `key_balance`, objective bounds, case label, and perspective tolerance have parallel failure paths. Intake does not reject these combinations. | Add conditional cross-field validation during intake: require all operational fields when their feature is enabled. If null is intended to disable an individual check, emit that ID as `not_applicable`. Add one test for every nullable enabled-feature field. |
| S8-06 | minor | `harness/tools/check_book.py:496` | When configured front matter is missing, `BOOK-FRONT-MISSING` fails but `BUDGET-FRONT` is emitted as `pass` with no measurement. This violates the rule that a check must not pass when its input is missing. | Mark `BUDGET-FRONT` failed for missing required front matter, or `not_applicable` with an explicit missing-input reason; test both missing-file and disabled-front-matter cases. |

## Top 5

1. S8-01: Approved configuration can redirect gated reads and writes outside the selected project.
2. S8-02: Equation and footnote text can inflate fidelity counts and conceal lost body content.
3. S8-03: A prose mention can satisfy the required-callout gate without an actual callout.
4. S8-04: The builder violates the shared-parser contract and retains hardcoded display grammar.
5. S8-05: Valid enabled-feature configurations can crash the checker with uncaught `TypeError`.

No files were modified.