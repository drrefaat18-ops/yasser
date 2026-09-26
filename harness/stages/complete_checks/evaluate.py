"""`complete evaluate` (core §8)."""
from harness import state
from harness.stages.complete_checks.common import findings_scorecard, read_json


def evaluate(project, active_run):
    extras, probs = findings_scorecard(project, "evaluation", "codex-review.md", "self")
    extras["author_model"] = (active_run or {}).get("author_model") or ""
    rubric_reviewers = read_json(project / "rubric.json")["pillars"]
    extras["personas"] = sorted({r for p in rubric_reviewers for r in p["reviewer_ids"]})
    for k in ("author_model", "reviewer_model"):
        if not extras.get(k):
            probs.append(f"{k} is required")
    probs += state.independent_review_problems(extras)
    return extras, probs
