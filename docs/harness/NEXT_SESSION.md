# Kick-off prompt for the next execution session

Paste this into a new Claude Code session opened in `D:\yasser`:

```text
Execute the book-harness ticket, STEP 8 (generalise the tools and implement ingest). STEPs 1-7 are done; HEAD is df16e7d.

Read these first, in full:
- CLAUDE.md (root: Rules 7, 8, 11)
- docs/harness/TICKET.md (rules + "STEP 8")
- docs/harness/LEDGER.md, docs/harness/DECISIONS.md (last DEC is DEC-040; next is DEC-041)
- docs/superpowers/plans/2026-09-25-book-harness.md: "Plan-spec notes" (N1-N9, esp. N3, N6, N7, N9) and "STEP 8" Tasks 8.1-8.4
- docs/superpowers/specs/2026-09-25-book-harness-core-design.md (checker IDs §9.3, golden §9.1-9.2, leak scan, ingest)
- docs/harness/reviews/step7-rulings.md and step7-fixes.md (carry-forward items below)

Binding rules:
- Stay inline. At most 2 Claude subagents, each with a stated reason; Codex does not count.
- Four tasks, each separately committed after its gates pass: 8.1 checker + assembler + positive-config fixtures + mutations + leak scan; 8.2 build; 8.3 verify_refs no-DOI policy; 8.4 ingest + fidelity. Each task makes the STAGES tool_paths and registry edits the plan names for it.
- One read-only Codex review over the whole of STEP 8, only after all four tasks pass, via codex-delegate relay.mjs with --read-only and WITHOUT --ignore-user-config (the user config's elevated Windows sandbox is needed). Save it verbatim to docs/harness/reviews/step8-review.md, then the Fix Protocol (confirm, root cause, hunt siblings, fix, verify) into step8-fixes.md. Deviations from the plan go in step8-rulings.md. No second round.
- Commit after gates pass; never push. Stop and ask me at every approval point.
- Never modify projects/ai-in-medicine/original/ or deliverables/ (Rule 5). Never edit state.json by hand.
- Scope lock: no Arabic parsing or rendering (STEP 10).

Carry-forward from STEP 7:
- The leak-scan term list (tests/fixtures/leak/clinical.txt, Task 8.1) must include diagnos, DSM and CBT (S7-09).
- The Rule 11 subagent cap is enforced per `complete` call only; enforce it across a unit stage's units when rework completion lands (S7-10).
- harness/figures/packs goes into intake's tool_paths when it is created (S7-04, STEP 9).
- verify now rebuilds each receipt's file sets from harness/stages/contracts.py, so a contract change stales existing receipts; the medical receipts are imported (DEC-039) and bind history/import.json.
- Any approval: show hashes from harness.hashing.hash_file, never sha256sum; approve refuses unless the DEC row contains the full hash of every approved file.
- docs/harness/DECISIONS.md and this file are CRLF: edit bytes and keep the line endings. Most harness files are LF.
- Full suite takes about 10 minutes and the bypass matrix about 8: run them in the background. Codex's sandbox cannot run the temp-repo tests, so run them yourself.

Exit criteria (ticket STEP 8): unittest exits 0 with every mutation yielding its named check ID and a non-zero checker exit; the medical golden matches STEP 6 except the listed verify_refs change (N7 comparison); positive-config fixtures pass; the scoped leak scan exits 0; Codex review done; LEDGER row 8 updated.

Talk to me in simple Arabic, briefly. Start with Task 8.1.
```
