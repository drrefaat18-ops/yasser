"""`complete design` (core §2.2 design row)."""
from harness.stages.complete_checks.common import read_json, table, validate_file
from harness.tools import config as tool_config


def design(project, active_run):
    plan, probs = validate_file(project / "design" / "chapter-plan.json", "chapter-plan")
    for f in ("design.md", "errata-seed.md"):
        if not (project / "design" / f).is_file() or not (project / "design" / f).read_text(encoding="utf-8").strip():
            probs.append(f"design/{f} is missing or empty")
    if plan is None or probs:
        return {}, probs
    probs += tool_config.problems(project)   # chapter files must stay inside the chapters directory (S8-01)
    if plan["project_id"] != project.name:
        probs.append(f"chapter-plan project_id {plan['project_id']!r} != {project.name!r}")
    ch = plan["chapters"]
    for key in ("id", "file"):
        vals = [c[key] for c in ch]
        if len(set(vals)) != len(vals):
            probs.append(f"chapter {key}s are not unique")
    parts = {p["id"] for p in plan["parts"]}
    probs += [f"{c['id']}: unknown part_id {c['part_id']!r}" for c in ch if c["part_id"] and c["part_id"] not in parts]
    total = sum(c["word_budget"] for c in ch)
    lim = read_json(project / "template.json")["budgets"]["total"]
    if lim and not lim["min"] <= total <= lim["max"]:
        probs.append(f"chapter budgets sum to {total}, outside template.budgets.total {lim['min']}-{lim['max']}")
    units_file = project / "ingest" / "units.json"
    if units_file.is_file():
        known = {u["id"] for u in read_json(units_file)["units"]} | {d["source_unit"] for d in plan["dropped"]}
        probs += [f"{c['id']}: source_refs {sorted(set(c['source_refs']) - known)} are not ingest units"
                  for c in ch if set(c["source_refs"]) - known]
    # every evaluate blocker/major finding is mapped (table `| Finding | Chapter | Reason |` in design.md; ruling)
    fpath = project / "evaluation" / "findings.json"
    serious = [f["id"] for f in read_json(fpath)["findings"] if f["severity"] in ("blocker", "major")] if fpath.is_file() else []
    mapped = {r["Finding"]: r for r in table(project / "design" / "design.md", "Finding")}
    ids = {c["id"] for c in ch}
    for fid in serious:
        r = mapped.get(fid)
        if r is None:
            probs.append(f"{fid}: blocker/major finding not mapped in design.md (`| Finding | Chapter | Reason |`)")
        elif r.get("Chapter") not in ids and not (r.get("Chapter") == "out-of-scope" and r.get("Reason", "").strip()):
            probs.append(f"{fid}: mapped to {r.get('Chapter')!r}; must be a chapter ID or `out-of-scope` with a reason")
    return {"chapter_count": len(ch), "total_budget": total}, probs
