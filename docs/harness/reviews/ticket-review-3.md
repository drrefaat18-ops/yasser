reviewed_commit: f06ceff38ff69794a60eae1f66118e3838b9b045; TICKET v3 is uncommitted working tree
verdict: fail
open_blocker_major: 3

## Review-2 finding status

| # | Review-2 finding | Status | V3 evidence |
|---:|---|---|---|
| 1 | Circular review-report commit protocol | **Partially resolved** | The general definition correctly excludes report-only commits ([TICKET.md:40-52](D:/yasser/docs/harness/TICKET.md:40)), but STEP 13 still requires `reviewed_commit` to equal `HEAD`, contradicting that definition ([TICKET.md:541-556](D:/yasser/docs/harness/TICKET.md:541)). |
| 2 | Fresh agents lack mandatory plan/spec inputs | **Resolved** | STEP 5 onward must read the approved plan tasks, applicable contracts, approval SHAs and predecessor handoff; the plan supplies commands, exit codes and paths ([TICKET.md:11](D:/yasser/docs/harness/TICKET.md:11), [TICKET.md:53-59](D:/yasser/docs/harness/TICKET.md:53)). |
| 3 | `dataviz` incorrectly treated as an installed disk skill | **Resolved** | Following the user’s correction, it is optional, host-provided and explicitly non-load-bearing ([TICKET.md:102-109](D:/yasser/docs/harness/TICKET.md:102)). |
| 4 | Migration approval absent from exit gate; root `CLAUDE.md` unreserved | **Resolved** | The root file is reserved, commit A is blocked until the approval DEC exists, and the exit checks the manifest and commit hashes ([TICKET.md:341-363](D:/yasser/docs/harness/TICKET.md:341)). |
| 5 | Medical configurations have no producer or approval exit | **Resolved** | All five configuration surfaces now have named paths, must be shown to the user, and must have a matching approval DEC and hashes before exit ([TICKET.md:386-412](D:/yasser/docs/harness/TICKET.md:386)). |
| 6 | STEPS 7–8 are oversized atomic tasks | **Resolved** | STEP 7 is divided into five committed/tested tasks and STEP 8 into four committed tasks under the approved implementation plan ([TICKET.md:390-397](D:/yasser/docs/harness/TICKET.md:390), [TICKET.md:440-444](D:/yasser/docs/harness/TICKET.md:440)). |
| 7 | E2E accepts failed or stale receipts | **Resolved** | Receipt validity now requires `status: ok`, current hashes, expected tool SHA and no invalidation marker; STEP 12 requires the aggregate verifier to exit 0 ([TICKET.md:60-66](D:/yasser/docs/harness/TICKET.md:60), [TICKET.md:532-537](D:/yasser/docs/harness/TICKET.md:532)). |
| 8 | Missing no-errata positive fixture | **Resolved** | The STEP 8 fixture set now explicitly includes books without errata ([TICKET.md:425-431](D:/yasser/docs/harness/TICKET.md:425)). |
| 9 | Ambiguous chemistry-pack path | **Resolved** | The canonical path is now `harness/figures/packs/chemistry/` ([TICKET.md:463-473](D:/yasser/docs/harness/TICKET.md:463)). |
| 10 | STEP 9 evidence not explicitly inspected | **Resolved** | Codex must inspect every committed evidence PNG ([TICKET.md:474-482](D:/yasser/docs/harness/TICKET.md:474)). |
| 11 | VISION origin omitted later user rulings | **Resolved** | The ticket binds the updated vision and identifies DEC-014–019 as user rulings ([TICKET.md:13](D:/yasser/docs/harness/TICKET.md:13), [TICKET.md:125-129](D:/yasser/docs/harness/TICKET.md:125)); VISION’s origin now names DEC-001–009 and DEC-014–019 ([VISION.md:66-68](D:/yasser/docs/harness/VISION.md:66)). |

## New findings

| Severity | File:line | Problem | Fix |
|---|---|---|---|
| **blocker** | [TICKET.md:40-52](D:/yasser/docs/harness/TICKET.md:40), [TICKET.md:541-556](D:/yasser/docs/harness/TICKET.md:541) | STEP 13 says the final report’s `reviewed_commit` must equal `HEAD`. Once Claude creates the required report-only commit, HEAD is no longer the reviewed implementation commit. This directly revives the circularity v3 intended to remove. | Replace `equals HEAD` with the definition’s rule: it equals the latest non-report-only commit. Require the report-only commit to pass an allowlist check covering only review files and the ledger hunk. |
| **major** | [TICKET.md:3-15](D:/yasser/docs/harness/TICKET.md:3), [TICKET.md:140-144](D:/yasser/docs/harness/TICKET.md:140), [TICKET.md:573-580](D:/yasser/docs/harness/TICKET.md:573) | The operative approval question and Blocker Register still ask the user to approve **ticket v2**, even though the document is v3. Approval could therefore be recorded against the wrong artifact. | Change both references to “ticket v3” and have the eventual approval DEC name the exact v3 commit or content SHA. |
| **major** | [TICKET.md:60-66](D:/yasser/docs/harness/TICKET.md:60), [TICKET.md:401-412](D:/yasser/docs/harness/TICKET.md:401), [TICKET.md:532-535](D:/yasser/docs/harness/TICKET.md:532) | `verify` is defined as validating mandatory stage receipts, but STEP 7 uses it before the medical project has run the harness stages and expects it to prove intake-approval hashes. The command has no stage boundary such as `--through intake`, and approval validation is not part of its documented contract. | Either add `verify --through intake` and define that it checks approval hashes plus receipts through that boundary, or add a separate `verify-approval` command. Keep the unqualified full `verify` for STEP 12. |
| **minor** | [TICKET.md:53-67](D:/yasser/docs/harness/TICKET.md:53), [TICKET.md:329-332](D:/yasser/docs/harness/TICKET.md:329), [TICKET.md:478-516](D:/yasser/docs/harness/TICKET.md:478) | The definition says every step’s exit criteria themselves name commands and expected codes, while several exits intentionally rely on the approved plan for those details. | Say that the ticket exit criteria **or the referenced approved plan task** must name each command and expected exit code. |
| **minor** | [TICKET.md:15](D:/yasser/docs/harness/TICKET.md:15), [TICKET.md:601-606](D:/yasser/docs/harness/TICKET.md:601) | The status says v3 incorporates review 2, but the Related section links only review 1. | Add `docs/harness/reviews/ticket-review-2.md`. |

## Verdict rationale

| Item | Assessment |
|---|---|
| Ready for approval? | **No.** V3 is close, but its final-audit gate remains internally impossible, its approval question names the wrong ticket version, and STEP 7 invokes an aggregate verifier whose documented semantics do not fit that point in the workflow. |
| Review-2 progress | Ten findings are resolved; the review-commit finding is only partially resolved. The `dataviz` correction is accepted: optional host capability with no dependency is safe. |
| Required before approval | Correct STEP 13’s comparison, change both stale `v2` references to `v3`, and define a stage-bounded approval/receipt verification command. The two minor documentation fixes can be included in the same edit. |
| Repository impact | Read-only review only; no files were modified and no commits were made. |
