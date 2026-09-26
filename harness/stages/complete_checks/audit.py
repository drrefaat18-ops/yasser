"""`complete audit` (core §2.2 audit row, §5.4, §7.5)."""
import json, subprocess
from harness import hashing, state
from harness.stages import contracts
from harness.stages.complete_checks.common import findings_scorecard, review_header, table


def audit(project, active_run):
    extras, probs = findings_scorecard(project, "audit", "codex-audit.md", "independent")
    extras["author_model"] = (active_run or {}).get("author_model") or ""
    for k in ("author_model", "reviewer_model"):
        if not extras.get(k):
            probs.append(f"{k} is required")
    probs += state.independent_review_problems(extras)
    ev = state.load(project)["receipts"].get("evaluate", {})
    if extras.get("rubric_digest") and ev.get("rubric_digest") != extras["rubric_digest"]:
        probs.append("rubric_digest differs from the evaluate receipt: baseline and rescore must use the same rubric")
    review = project / "audit" / "codex-audit.md"
    head = review_header(review)
    commit = head.get("reviewed_commit", "")
    if not commit:
        probs.append("codex-audit.md: `reviewed_commit:` line missing")
    else:
        probs += reviewed_commit_problems(project, commit, contracts.files(project, "audit")[0])
    # ruling (step7-rulings): the audited inputs are identified by the commit Codex reviewed plus the saved review
    extras["codex_audited_inputs"] = {"reviewed_commit": head.get("reviewed_commit", ""),
                                      "review_sha256": hashing.hash_file(review) if review.is_file() else ""}
    report = project / "build" / "build-report.json"
    unverified = json.loads(report.read_text(encoding="utf-8")).get("chem_unverified", []) if report.is_file() else []
    ruled = {r["ID"] for r in table(project / "audit" / "fixes.md", "ID")
             if r.get("status", "").strip().lower() == "ruled by user" and r.get("DEC")}
    probs += [f"CHEM-UNVERIFIED {fid}: needs a later online build or a `ruled by user` fixes row with a DEC"
              for fid in unverified if fid not in ruled]
    # ponytail: TB-PROPOSAL-OPEN (translation contract §3.3) is added with the termbase in Task 11.x
    return extras, probs


def reviewed_commit_problems(project, commit, rels):
    """The commit Codex reviewed exists and every current audit input is byte-for-byte what it held (S7-08)."""
    git = lambda *a: subprocess.run(["git", *a], cwd=project, capture_output=True, text=True)
    if git("cat-file", "-e", f"{commit}^{{commit}}").returncode != 0:
        return [f"AUDIT-COMMIT codex-audit.md: reviewed_commit {commit!r} is not a commit in this repository"]
    rels = [r for r in rels if (project / r).exists()]
    r = git("diff", "--name-only", commit, "--", *rels)
    changed = r.stdout.split() if r.returncode == 0 else [r.stderr.strip()]
    untracked = git("ls-files", "--others", "--exclude-standard", "--", *rels).stdout.split()
    return [f"AUDIT-COMMIT {f}: differs from reviewed_commit {commit[:12]}; Codex did not review this content"
            for f in changed + untracked]
