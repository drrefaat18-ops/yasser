# Kick-off prompt for the execution session

Paste this into a new Claude Code session opened in `D:\yasser`:

```text
Execute the book-harness ticket, starting at STEP 1.

Read these files in full first:
- docs/harness/TICKET.md
- docs/harness/VISION.md
- docs/harness/DECISIONS.md
- docs/harness/LEDGER.md
- docs/harness/INTAKE_QUESTIONNAIRE.md

Binding rules:
- The ticket was approved at commit 23d819f (DEC-026). STEP 1 is released.
- Stay inline by default. At most 2 Claude subagents at a time, each with a stated reason. Codex dispatches do not count toward this cap (DEC-014, DEC-015).
- Codex reviews each artifact once, read-only, through codex-delegate. There is no second round.
- Resolve the findings with the Fix Protocol (DEC-030):
  1. Take the review, and confirm each finding.
  2. Think deeply about the root cause.
  3. Hunt for more defects of the same class.
  4. Fix the root cause.
  5. Verify by running a check.
  Record all of it in docs/harness/reviews/step<N>-fixes.md.
- You may commit after a task passes its gates. Never push. Stop and ask me at every user-approval point (DEC-028).

Start with STEP 1, the core design spec. Stop at STEP 1's exit criteria and ask me to approve the spec.
```
