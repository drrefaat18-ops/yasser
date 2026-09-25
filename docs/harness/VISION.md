---
type: rule
status: active
last_updated: 2026-09-25
---

# Book Harness Vision Constraint: Binding Rule for All Agents

> [!danger] This is a rule, not a preference. It binds every agent working on the book harness in `D:\yasser` (ticket: `docs/harness/TICKET.md`).

## The vision (the user's words, paraphrased only for translation)

Turn this workspace, which evaluated and then rebuilt one medical AI textbook, into a **harness**. The harness repeats the same pipeline on **any** university textbook, in **any** science. Each run follows the same order:

1. Ingest the book.
2. Evaluate it to find gaps and problems.
3. Design a stronger, simpler edition for university teachers and students.
4. Rewrite it.
5. Build Word and PDF.
6. Re-score it.

The harness must not be locked to the medical sector. It **asks the user about the book first and starts no work until that intake is done.** It must support all sciences, both culturally and in its tooling. Culturally means Arabic and English books, including translation between them. Tooling means figures such as chemical structures, reaction schemes, charts and diagrams, all laid out properly in the book.

**Execution cost is part of the vision (DEC-014).** The harness runs at the cheapest cost that still gives the highest quality. Inline execution is the default. An agent is spawned only for a real reason, and never more than 2 Claude subagents. Codex review dispatches do not count (DEC-015).

## The rule

**No agent may stray from the user's stated vision.**

An agent may suggest improvements. Those suggestions are **bounded by the vision**. They may refine *how* a step is executed. They may never change *what* the step is or *why* it exists. An agent may not:

- Add a phase, artifact or deliverable the vision did not ask for.
- Remove, merge, reorder or "optimize away" a step the vision specified. This includes the intake gate, Arabic support, translation and the chemistry figure pack.
- Substitute its own judgment for a stated instruction.
- Silently resolve an ambiguity by guessing.
- Spawn Claude subagents beyond the DEC-014/015 cap (2; Codex dispatches excluded), or spawn them without a stated reason.
- Re-couple the harness to medicine. For example, it may not hardcode professions, box names or clinical vocabulary into shared tools.

## What to do instead of guessing

If an agent genuinely cannot proceed without inventing an answer, it **stops and escalates to the user**. Escalation is only for **genuine blockers**: a real fork where the two paths produce materially different results.

Some choices are **not** blockers, and the agent decides them itself and moves on:

- wording
- file naming inside the agreed layout
- section ordering
- formatting
- helper function structure

**Over-escalation is a failure mode too.**

Log every escalation in the Blocker Register in `docs/harness/TICKET.md`. Saying it in chat is not enough.

## Why this rule exists

The first run succeeded because every stage was gated and argued out with the user. That run took the book from a 46/100 draft to a finished edition. The user now wants that discipline repeatable for books whose domain, language and figures differ from the first one.

The failure this rule prevents: an agent "helpfully" does one of these:
- skips intake because the book "looks obvious";
- keeps medical assumptions because they already work;
- drops Arabic or translation because they are large.

Each of these produces a harness that works only for the book it was built on.

## Origin

Direct instructions from the user, 2026-09-25, in the harness design conversation. Recorded as user rulings DEC-001 to DEC-009 and DEC-014 to DEC-019 in `docs/harness/DECISIONS.md`.

## Related
- `docs/harness/TICKET.md`
- `docs/harness/DECISIONS.md`
- `docs/harness/codex-design-review-2026-09-25.md`
