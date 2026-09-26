"""Completion checks, one module per stage so a change stales only that stage (Task 7.2)."""
from harness.stages.complete_checks.audit import audit
from harness.stages.complete_checks.common import fixes_rows, review_header, score
from harness.stages.complete_checks.design import design
from harness.stages.complete_checks.evaluate import evaluate
from harness.stages.complete_checks.intake import intake, overlay_cap_problems, rubric_problems
from harness.stages.complete_checks.rework import rework

# (project, active_run, unit) -> (extras, problems). translate joins in Task 11.x.
CHECKS = {
    "intake": lambda p, ar, unit: intake(p),
    "evaluate": lambda p, ar, unit: evaluate(p, ar),
    "design": lambda p, ar, unit: design(p, ar),
    "rework": lambda p, ar, unit: rework(p, ar, unit),
    "audit": lambda p, ar, unit: audit(p, ar),
}

__all__ = ["CHECKS", "rubric_problems", "score", "fixes_rows", "review_header", "overlay_cap_problems"]
