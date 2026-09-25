# STEP 5 — Codex review (preflight and medical baseline freeze)

Source: codex-delegate relay, read-only, run yasser-2026-09-25T17-24-35-870Z, thread 01a0d999-0cfa-7323-bab6-2c321e8840a2, touchedFiles: []. Report below is verbatim.

reviewed_commit: c2fe5b3bb331c633d7fb1151b1464469a27b8288
verdict: fail
open_blocker_major: 6

## Findings

| ID | Severity (blocker/major/minor) | File:line | Problem | Concrete fix |
|---|---|---|---|---|
| S5-01 | major | `harness/tools/capture_golden.py:308` | Every `word/fonts/*.odttf` part is replaced with the literal `"volatile"`. This normalizes the random obfuscation key but also hides actual font/glyph changes when the part name and declared font name remain unchanged. | Resolve each embedded-font relationship and `w:fontKey`, de-obfuscate the standard obfuscated prefix, and hash the normalized font bytes. Add tests proving key-only changes compare equal while changed font payloads differ. |
| S5-02 | major | `harness/tools/capture_golden.py:269` | TOC-result removal drops a run only when it is inside the result both before and after processing that run. Valid runs containing `separate` followed by result text, or result text followed by `end`, retain the volatile page number. Synthetic checks confirmed both forms produce different normalized XML. | Traverse field children in document order and remove result content at child granularity while retaining field delimiters/instructions. Add tests for result text sharing the `separate` and `end` runs and for nested fields/hyperlinks. |
| S5-03 | major | `harness/preflight.py:84` | Explicit groups do not implement the declared dependency matrix: `--group build` omits `python-docx` and `lxml`, while `--group figures` omits the browser. Unknown group names are accepted and produce an empty successful run. This permits false-positive preflight results. | Define one validated group/check registry, give `--group` explicit choices, include shared checks in every applicable group, and add tests for `build`, `figures`, and an invalid group. |
| S5-04 | major | `harness/preflight.py:72` | The literal `C:\Windows` violates Rule 8’s absolute-path prohibition and will be caught by the planned §9.5 leak scan, breaking STEP 8. | Require `WINDIR`/`SystemRoot` from the environment and return a named failed `fonts` check when neither is available; keep no absolute fallback literal in shared code. |
| S5-05 | major | `harness/tools/capture_golden.py:430` | The shipped CLI parses an untrusted layout and uses its path values without containment validation. Absolute paths or `..` values in `legacy_tools`, deliverables, images, or other fields can read/import files outside the selected project, contradicting N1 and §1.1. | Validate the layout at the CLI boundary: require relative paths, resolve every referenced path beneath the selected project, reject escapes and unsafe globs, then pass a validated layout to `capture`. Add escape tests. |
| S5-06 | major | `tests/test_legacy_classify.py:36` | The READ-MEAN and READ-LONG cases use the identical mutation, which emits both IDs. Swapping those two classifier mappings would still pass both tests, so these N6 rows are not independently protected as required. | Use isolated prose fixtures: medium-length sentences that trigger only READ-MEAN, and mostly short sentences plus one long sentence that trigger only READ-LONG. Assert the exact classified ID for the intended emitted message. |

## Rulings R1-R8

R1 — reject: the additional XML identifiers are defensibly volatile, but discarding all embedded-font bytes is over-broad and can hide genuine glyph-content changes.

R2 — accept: `READ-NOPROSE` is demonstrably emitted by the legacy checker and belongs in the frozen legacy baseline.

R3 — accept: the corrected `check_all` lines 274/282/284/287/289 match the unchanged legacy source.

R4 — accept: placing assessment and answer labels in fixture layout data prevents a Rule 8 domain-label leak into shared code.

R5 — accept: the targets, placement of measurements, and aggregation of repeated failures are deterministic and compatible with the current chapter naming contract.

R6 — accept: refusing unknown `verify_refs` output prevents silently freezing an uninterpreted or failed result.

R7 — accept: source validation/copying precedes the golden write, missing files are restored, differing/extra files are rejected, and bytecode caches are excluded appropriately.

R8 — accept: book-level checks inherently require directory-level mutation, so using a temporary chapters copy is within the ticket and correctly covers the five book IDs.

## Top 5

1. Embedded-font normalization can conceal real rendered-content changes.
2. The shipped layout interface can escape the selected project.
3. TOC normalization is unstable for boundary characters sharing result runs.
4. Preflight can falsely pass incomplete or mistyped explicit groups and retains a Rule 8 path leak.
5. The READ-MEAN/READ-LONG mutations do not independently verify their mappings.

The scope-lock diff was empty, and both legacy tools are unchanged. The frozen baseline was internally consistent: 302 passing checks, 101/101 reference rows, matching chapter/assembled/DOCX hashes, and an exact immutable source copy.

The prescribed test run discovered 20 tests but 12 could not execute because this managed read-only environment provides no writable temporary directory. Preflight likewise could not create its write probe, and Word COM was unavailable in the non-interactive logon session. Those environmental failures are not counted above, but the required exit-zero gates remain unconfirmed here.

No files were modified.
