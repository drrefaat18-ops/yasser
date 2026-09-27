# STEP 9 Codex review (verbatim)

reviewed_commit: e5dd2d74800cda2c5637a01893d910e377eaa3a9
verdict: fail
open_blocker_major: 9

## Findings

| ID | Severity (blocker/major/minor) | File:line | Problem | Concrete fix |
|---|---|---|---|---|
| S9-01 | blocker | harness/tools/build_book.py:926 | The fixed `project/build` directory is never resolved and containment-checked. A junction or symlink named `build` can make Markdown, DOCX, PDF, and report writes land outside the project. | Centralize output-path construction, resolve the destination parent, require it to remain beneath the resolved project, and reject symlink/junction output directories before every write. |
| S9-02 | major | harness/stages/build.py:67 | Rendering happens before semantic manifest checks. An invalid/outside chart source can be executed before `FIG-MANIFEST` is raised, while malformed JSON fails generically instead of producing the promised stable ID. | Split checking into a pre-render manifest/reference/source/pack validation pass, render only if it passes, then run resolution and chemistry-result checks. |
| S9-03 | major | harness/tools/build_book.py:1086; harness/tools/assemble.py:103 | Both component CLIs write owned build artifacts outside `run build`; `build_book.py` also bypasses rendering, figure checks, PubChem checks, report generation, and receipt creation. | Make these CLIs dry-run/temp-output diagnostics or remove their executable writers. Keep persistent `build/*` writes exclusively in `harness/stages/build.py`. |
| S9-04 | major | harness/figures/check_figures.py:160 | The source JSON’s `kind` is never compared with the manifest kind. A manifest declaring `chem.reaction` can point to a valid `chem.structure` spec; it renders as a structure, skips cross-checking, and produces no finding. This was reproduced read-only: `renderable=True`, findings `{}`. | Require `spec["kind"] == manifest_entry["kind"]` before render and emit a blocking manifest or chemistry finding on mismatch; add both direction mutations. |
| S9-05 | major | harness/figures/packs/chemistry/pubchem.py:23 | PubChem comparison discards stereochemistry with `isomericSmiles=False`; opposite enantiomers canonicalize identically and return `pass`. | Compare isomeric canonical SMILES whenever either side specifies stereochemistry; only use connectivity comparison when the specification intentionally contains none. Add an enantiomer-mismatch test. |
| S9-06 | major | harness/stages/contracts.py:125; harness/figures/packs/chemistry/pubchem.py:29 | PubChem cache entries decide pass/fail but are explicitly excluded from receipt inputs and trusted indefinitely. Editing or retaining a stale cache can yield `pass` without making the receipt stale or proving what response was used. | Bind every used cache response hash and request URL into the build receipt/report, add an expiry/revalidation policy, and never treat an expired entry as `pass` after a failed refresh. |
| S9-07 | major | harness/figures/charts.py:11 | The chart subprocess fixes `PYTHONHASHSEED` but does not seed Python or NumPy randomness before executing arbitrary chart source, contrary to the fixed-seed determinism requirement. | Seed `random` and NumPy before `runpy.run_path`, then add a stochastic chart fixture rendered in separate subprocesses and compare SVG/PNG bytes. |
| S9-08 | major | harness/tools/assemble.py:48; harness/tools/build_book.py:573 | The Markdown build uses the caption as image alt text and omits credit/licence; DOCX uses the proper alt and credit but never emits the licence. Thus required alt/source/licence metadata does not survive all deliverables. | Use `fig["alt"]` for Markdown alt text and emit a visible, deterministic credit-plus-licence line in both Markdown and DOCX. Test all four manifest fields in both outputs. |
| S9-09 | major | harness/state.py:41; harness/figures/packs/chemistry/__init__.py:14 | `requirements-chemistry.txt` controls pack readiness and byte-stability but is absent from build `tool_paths`; changing the RDKit pin does not stale an existing build receipt. | Add `requirements-chemistry.txt` to build `tool_paths` and extend the tool-path coverage test to non-Python files read by stage code. |
| S9-10 | minor | tests/test_figures.py:184; tests/test_chemistry.py:18 | Critical integration and chemistry coverage can be reported as skipped. In this review, the full build test skipped because Word COM was unavailable to the logon session. | Separate DOCX/figure integration from PDF finishing so most assertions run without COM, and make the STEP 9 acceptance command fail when required chemistry coverage is skipped. |

## Evidence PNGs

| File | Verdict | Notes |
|---|---|---|
| bar-chart.png | pass | Title, axes, units, ticks, and categories are legible; nothing is clipped. |
| line-chart.png | pass | Title, legend, axes, units, and series are legible; nothing is clipped. |
| diagram.png | pass | Box, push and friction labels/arrows are clear and fully within the canvas. |
| aspirin.png | pass | Unclipped and legible; correct acetylsalicylic-acid connectivity for `CC(=O)Oc1ccccc1C(=O)O`. |
| caffeine.png | pass | Unclipped and legible; correct fused-ring caffeine structure with three methyl and two carbonyl groups. |
| ethanol-oxidation.png | pass | Unclipped and legible; correctly depicts ethanol converting to ethanal for `CCO>>CC=O`. |

## Rulings

R1: sound — the manifest exception is limited to a history-imported rework receipt; ordinary harness books require the manifest.

R2: sound — rounded DPI correctly accounts for PNG pixels-per-metre representation.

R3: unsound — the Markdown path discards the dedicated alt text, and licence metadata is not placed in either deliverable.

R4: sound — a blocking manifest-level ID is necessary, although build ordering currently prevents it from consistently governing pre-render failures.

R5: sound — project-relative sources with kind-specific containment are appropriate.

R6: sound — the two figure CLIs use temporary render output; the separate persistent writers in `assemble.py` and `build_book.py` remain an ownership defect.

R7: sound — checker and DOCX builder use the same placement-width function.

R8: unsound — Python and NumPy randomness are not seeded, so arbitrary chart sources are not guaranteed byte-deterministic.

R9: sound — the added report fields provide useful render/check/version evidence.

R10: sound — copying the repository ignore rules prevents generated bytecode from falsely dirtying tool paths.

R11: unsound — `requirements-chemistry.txt`, which directly controls build behavior, is missing from `tool_paths`.

R12: sound — positive-config fixtures now satisfy the required rework manifest output contract.

R13: sound — the environment switch can only weaken results to `unverified`, which remains audit-blocking.

R14: unsound — an unbounded, unhashed mutable cache can hide stale or altered cross-check input.

R15: sound — a reaction has no single PubChem compound identity; participant validation remains local.

R16: unsound — stereo-free comparison can approve the wrong stereoisomer.

R17: sound — enforcing the installed RDKit pin is necessary for byte-stability.

R18: sound — clearing `CHEM-UNVERIFIED` requires the figure ID, user-ruling status, and an existing DEC.

R19: sound — all three chemistry evidence images are legible, chemically correct, and unclipped.

## Top 5

1. A `build` junction can redirect writes outside the project.
2. Persistent component CLIs bypass the owning build stage and figure checker.
3. A manifest/spec chemistry-kind mismatch can pass while rendering the wrong figure type.
4. Stereo-free PubChem comparison and an unbound cache can produce dishonest `pass` results.
5. Gate status: leak scan and chemistry preflight exited 0; the required unittest command exited 1 because this read-only reviewer environment had no writable temporary directory. Word COM was installed but unavailable to the current logon session.

No files were modified.
