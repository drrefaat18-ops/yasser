"""Project config for the tools (plan STEP 8 common interfaces). Tools know config, not state files."""
import json, pathlib
from harness import locales


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


def load(project):
    project = pathlib.Path(project)
    brief, template = _json(project / "brief.json"), _json(project / "template.json")
    over = template.get("locale_overrides") or {}
    plan = project / "design" / "chapter-plan.json"
    profile_out = locales.with_overrides(locales.load_profile(brief["language"]["output"]), over)
    return Config(project=project, brief=brief, template=with_locale_defaults(template, profile_out),
                  theme=_json(project / "theme.json"),
                  chapter_plan=_json(plan) if plan.exists() else {"chapters": [], "parts": []},
                  profile_out=profile_out, profile_src=locales.load_profile(brief["language"]["source"]))


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
