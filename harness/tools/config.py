"""Project config for the tools (plan STEP 8 common interfaces). Tools know config, not state files.

`load` refuses a config that would make a tool read or write outside the project (core §1.1) or that enables a
feature without the fields its checks need (S8-01, S8-05); `problems` is the same test for `complete intake`.
"""
import json, pathlib, posixpath, re
from harness import locales


class ConfigError(Exception):
    code, exit_code = "CONFIG", 2


class Config(dict):
    """keys: project, brief, template, theme, chapter_plan, profile_out, profile_src."""

    def path(self, key):
        """template.paths.<key> resolved against the project; None when the key is null."""
        rel = self["template"]["paths"].get(key)
        return None if rel is None else self["project"] / rel

    def book_file(self, key):
        """front_matter, glossary and errata are names inside the chapters directory (core §4.3 paths)."""
        rel = self["template"]["paths"].get(key)
        return None if rel is None else self.path("chapters") / rel

    def chapters(self):
        """[(chapter-plan entry, path)] in plan order."""
        return [(c, self.path("chapters") / c["file"]) for c in self["chapter_plan"]["chapters"]]


def _json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def _outside(project, rel):
    if not isinstance(rel, str) or not rel or rel.startswith(("/", "\\")) or re.match(r"^[A-Za-z]:", rel):
        return True
    root = pathlib.Path(project).resolve()
    return not (root / rel).resolve().is_relative_to(root)


def path_problems(project, brief, template, theme, plan):
    """Every configured path must stay inside the project; the build stem is a plain file name."""
    p, probs = template["paths"], []
    for key, rel in p.items():
        for r in (rel if isinstance(rel, list) else [rel]):
            if r is not None and key != "asset_link_prefix" and _outside(project, r):
                probs.append(f"template.paths.{key}: {r!r} is not a path inside the project")
    ch = p.get("chapters") or ""
    for key in ("front_matter", "glossary", "errata"):
        if p.get(key) is not None and _outside(project, f"{ch}/{p[key]}"):
            probs.append(f"template.paths.{key}: {p[key]!r} leaves the chapters directory's project")
    for c in plan.get("chapters", []):
        if _outside(project, f"{ch}/{c['file']}") or "/" in c["file"] or "\\" in c["file"]:
            probs.append(f"chapter-plan {c['id']}: file {c['file']!r} must be a file name inside {ch}/")
    cover = (theme.get("cover") or {}).get("asset")
    if cover is not None and _outside(project, cover):
        probs.append(f"theme.cover.asset: {cover!r} is not a path inside the project")
    # logos and font files are build inputs: under an asset root, so the build receipt hashes them (contracts.py)
    roots = [r.rstrip("/") + "/" for r in p.get("allowed_asset_roots", [])]
    design = (theme.get("cover") or {}).get("design") or {}
    extra = [("theme.cover.design.logos", r) for r in design.get("logos", [])]
    extra += [(f"theme.font_files.{fam}", r) for fam, files in (theme.get("font_files") or {}).items() for r in files.values()]
    for where, r in extra:
        norm = posixpath.normpath(str(r).replace("\\", "/"))
        if _outside(project, r) or not any(norm.startswith(root) for root in roots):
            probs.append(f"{where}: {r!r} must be a file under one of template.paths.allowed_asset_roots")
        elif not (pathlib.Path(project) / norm).is_file():   # a missing logo or font would silently drop (S9b-02)
            probs.append(f"{where}: {r!r} is not an existing file")
    base = (theme.get("output") or {}).get("basename", "")
    if not re.fullmatch(r"[^/\\:*?\"<>|]+", base or "") or base in (".", ".."):
        probs.append(f"theme.output.basename: {base!r} must be a plain file name")
    for f in brief.get("source", {}).get("files", []):
        if _outside(project, f["path"]):
            probs.append(f"brief.source.files: {f['path']!r} is not a path inside the project")
    return probs


def feature_problems(template):
    """An enabled feature needs every field its checks read (schema-valid nulls are only allowed when it is off)."""
    t, probs = template, []
    need = lambda cond, msg: probs.append(msg) if not cond else None
    roles = {s["role"] for s in t["sections"]}
    mcq = t["assessment"]["mcq"]
    if mcq["enabled"]:
        need(isinstance(mcq["count"], int), "assessment.mcq.count is required when MCQs are enabled")
        need(bool(mcq["option_labels"]), "assessment.mcq.option_labels is required when MCQs are enabled")
        kb = mcq["key_balance"] or {}
        need(isinstance(kb.get("min"), int) and isinstance(kb.get("max"), int), "assessment.mcq.key_balance {min, max} is required")
        need(isinstance(mcq["max_run"], int) and mcq["max_run"] >= 1, "assessment.mcq.max_run (>= 1) is required")
        need(mcq["answers_section_role"] in roles, "assessment.mcq.answers_section_role must name a section role")
        need("assessment" in roles, "a section with role `assessment` is required when MCQs are enabled")
    cq = t["assessment"]["case_question"]
    if cq["required"]:
        need(mcq["enabled"], "assessment.case_question.required needs MCQs enabled (it lives in the assessment section)")
        need(bool(cq["label"]), "assessment.case_question.label is required when a case question is required")
    lo = t["learning_objectives"]
    if lo["enabled"]:
        need(isinstance(lo["min"], int) and isinstance(lo["max"], int), "learning_objectives.min and max are required")
        need("objectives" in roles, "a section with role `objectives` is required when objectives are enabled")
    pe = t["perspectives"]
    if pe["enabled"]:
        need(pe["callout_id"] in {c["id"] for c in t["callouts"]}, "perspectives.callout_id must name a callout")
        need(bool(pe["items"]), "perspectives.items is required when perspectives are enabled")
        need(isinstance(pe["balance_tolerance"], (int, float)), "perspectives.balance_tolerance is required")
    g = t["glossary"]
    if g["enabled"]:
        need(g["term_syntax"] == "bold", "glossary.term_syntax must be `bold` (the only supported syntax)")
        need(isinstance(g["minimum_terms"], int), "glossary.minimum_terms is required when the glossary is enabled")
        need(t["paths"]["glossary"] is not None, "template.paths.glossary is required when the glossary is enabled")
    e = t["errata"]
    if e["enabled"]:
        need(bool(e["status_column"]) and bool(e["open_values"]), "errata.status_column and open_values are required")
        need(t["paths"]["errata"] is not None, "template.paths.errata is required when errata are enabled")
    need(isinstance(t["budgets"]["tolerance"], (int, float)), "budgets.tolerance is required")
    need(t["citations"]["style"] == "numeric-bracket", "citations.style must be `numeric-bracket` (the only supported style)")
    return probs


def problems(project):
    """Path and feature problems of a project's current config files (used by `complete intake`)."""
    project = pathlib.Path(project)
    brief, template, theme = (_json(project / f) for f in ("brief.json", "template.json", "theme.json"))
    plan = project / "design" / "chapter-plan.json"
    return path_problems(project, brief, template, theme, _json(plan) if plan.exists() else {}) + feature_problems(template)


def load(project):
    project = pathlib.Path(project)
    brief, template, theme = _json(project / "brief.json"), _json(project / "template.json"), _json(project / "theme.json")
    over = template.get("locale_overrides") or {}
    plan_file = project / "design" / "chapter-plan.json"
    plan = _json(plan_file) if plan_file.exists() else {"chapters": [], "parts": []}
    probs = path_problems(project, brief, template, theme, plan) + feature_problems(template)
    if probs:
        raise ConfigError("; ".join(probs))
    profile_out = locales.with_overrides(locales.load_profile(brief["language"]["output"]), over)
    return Config(project=project, brief=brief, template=with_locale_defaults(template, profile_out), theme=theme,
                  chapter_plan=plan, profile_out=profile_out, profile_src=locales.load_profile(brief["language"]["source"]))


def with_locale_defaults(template, profile):
    """Template fields documented as `default from locale` (core §4.3), filled when null."""
    t = json.loads(json.dumps(template))
    if t.get("chapter_heading_pattern") is None:
        t["chapter_heading_pattern"] = profile["chapter_heading_pattern"]
    if t.get("figures", {}).get("caption_pattern") is None:
        t.setdefault("figures", {})["caption_pattern"] = profile["figure_caption_pattern"]
    t["readability"] = {k: (v if v is not None else profile["readability"][k])
                        for k, v in {**profile["readability"], **{k: v for k, v in (t.get("readability") or {}).items()}}.items()}
    lo = t.get("learning_objectives") or {}
    if lo.get("enabled") and not lo.get("discouraged_verbs"):
        lo["discouraged_verbs"] = list(profile["discouraged_objective_verbs"])
    return t
