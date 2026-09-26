"""`complete intake`: schemas, cross-file rules (core §4.6), rubric rules (§5.2), overlay caps (§6)."""
from harness import locales, paths
from harness.stages.complete_checks.common import read_json, validate_file

SUPPORTED_PAIRS = {("en", "ar"), ("ar", "en")}          # translation contract §1
CORE_PACKS = {"charts"}                                   # core figure pack, always available (core §7.4)
OVERLAY_CAPS = {"criteria": 12, "exclusions": 8, "evidence_expectations": 8}
SCOPE_MAX, ITEM_MAX = 400, 200


def _harness():
    return paths.REPO / "harness"


def overlay_cap_problems(ov):
    probs = []
    if len(ov.get("scope", "")) > SCOPE_MAX:
        probs.append(f"overlay scope is {len(ov['scope'])} characters, max {SCOPE_MAX}")
    for key, cap in OVERLAY_CAPS.items():
        items = ov.get(key, [])
        if len(items) > cap:
            probs.append(f"overlay {key} has {len(items)} items, max {cap}")
        probs += [f"overlay {key}[{i}] is {len(s)} characters, max {ITEM_MAX}" for i, s in enumerate(items) if len(s) > ITEM_MAX]
    return probs


def rubric_problems(rubric, assessment_enabled):
    core = {p["id"]: p["weight"] for p in read_json(_harness() / "rubric_core.json")["pillars"]}
    probs = []
    pillars = rubric["pillars"]
    ids = [p["id"] for p in pillars]
    if len(set(ids)) != len(ids):
        probs.append(f"pillar IDs are not unique: {ids}")
    fixed = {p["id"]: p for p in pillars if p["kind"] == "fixed"}
    if set(fixed) != set(core):
        probs.append(f"fixed pillars {sorted(fixed)} != core {sorted(core)}")
    want = dict(core)
    if not assessment_enabled:   # the one allowed reallocation (core §5.2)
        want["G2"] += want.pop("G3")
    for pid, p in fixed.items():
        if pid == "G3" and not assessment_enabled:
            if p["applicable"]:
                probs.append("G3 must be applicable=false when MCQs, cases and exercises are all disabled")
            continue
        if not p["applicable"]:
            probs.append(f"{pid} must be applicable")
        if pid in want and p["weight"] != want[pid]:
            probs.append(f"{pid} weight {p['weight']} != {want[pid]}")
    domain = [p for p in pillars if p["kind"] == "domain"]
    if not 1 <= len(domain) <= 4:
        probs.append(f"{len(domain)} domain pillars; 1-4 allowed")
    bad = [p["id"] for p in domain if not (isinstance(p["weight"], int) and 5 <= p["weight"] <= 40)]
    if bad:
        probs.append(f"domain pillar weights must be integers 5-40: {bad}")
    if sum(p["weight"] for p in domain) != 40:
        probs.append(f"domain pillars sum to {sum(p['weight'] for p in domain)}, not 40")
    total = sum(p["weight"] for p in pillars if p["applicable"])
    if total != 100:
        probs.append(f"applicable pillar weights sum to {total}, not 100")
    probs += [f"{p['id']}: needs at least one reviewer" for p in pillars if not p["reviewer_ids"]]
    return probs


def _packs():
    d = _harness() / "figures" / "packs"
    return CORE_PACKS | ({p.name for p in d.iterdir() if p.is_dir() and (p / "__init__.py").exists()} if d.is_dir() else set())


def intake(project):
    """-> (extras, problems)."""
    probs, docs = [], {}
    for name in ("brief", "rubric", "template", "theme"):
        docs[name], p = validate_file(project / f"{name}.json", name)
        probs += p
    overlays = {}
    for f in sorted((project / "agents").glob("*.json")):
        overlays[f.stem], p = validate_file(f, "overlay")
        probs += [f"agents/{x}" for x in p]
    if probs:
        return {}, probs
    brief, rubric, template, theme = docs["brief"], docs["rubric"], docs["template"], docs["theme"]
    for name, d in docs.items():
        if d["project_id"] != project.name:
            probs.append(f"{name}.json project_id {d['project_id']!r} != directory {project.name!r}")

    # 1. domain pillars equal the brief
    dom = sorted((p["id"], p["weight"]) for p in rubric["pillars"] if p["kind"] == "domain")
    if dom != sorted((p["id"], p["weight"]) for p in brief["domain_pillars"]):
        probs.append(f"rule 1: rubric domain pillars {dom} != brief.domain_pillars")
    # 2. translation iff primary subtags differ; profiles exist; supported pair
    src, out = (locales.primary(brief["language"][k]) for k in ("source", "output"))
    if brief["language"]["translation_required"] != (src != out):
        probs.append(f"rule 2: translation_required must be {src != out} for {src} -> {out}")
    for tag in {src, out}:
        if not locales.exists(tag):
            probs.append(f"rule 2: no locale profile harness/locale/{tag}.json")
    if src != out and (src, out) not in SUPPORTED_PAIRS:
        probs.append(f"TR-PAIR-UNSUPPORTED: {src}-{out}; supported pairs: " + ", ".join(f"{a}-{b}" for a, b in sorted(SUPPORTED_PAIRS)))
    # 3. theme language and direction
    if locales.primary(theme["lang_tag"]) != out:
        probs.append(f"rule 3: theme.lang_tag {theme['lang_tag']} does not have the output subtag {out}")
    if locales.exists(out) and theme["direction"] != locales.load_profile(out)["direction"]:
        probs.append(f"rule 3: theme.direction {theme['direction']} != locale {out} direction")
    # 4. perspectives
    tp, bp = template["perspectives"], brief["perspectives"]
    if tp["enabled"] != bp["enabled"] or tp["items"] != bp["items"]:
        probs.append("rule 4: template.perspectives must equal brief.perspectives (enabled and items)")
    # 5. MCQ
    tm, bm = template["assessment"]["mcq"], brief["assessment"]["mcq"]
    if tm["enabled"] != bm["enabled"]:
        probs.append("rule 5: template and brief disagree on MCQs enabled")
    elif bm["enabled"] and (tm["count"] != bm["per_chapter"] or len(tm["option_labels"]) != bm["options"]):
        probs.append(f"rule 5: MCQ count {tm['count']}/options {len(tm['option_labels'])} != brief "
                     f"{bm['per_chapter']}/{bm['options']}")
    # 6. reviewers name a shared persona or an overlay
    personas = {f.stem for f in (_harness() / "agents").glob("*.md")}
    for p in rubric["pillars"]:
        unknown = [r for r in p["reviewer_ids"] if r not in personas and r not in overlays]
        if unknown:
            probs.append(f"rule 6: {p['id']} reviewers {unknown} are neither shared personas nor overlays")
    for oid, ov in overlays.items():
        if ov["id"] != oid:
            probs.append(f"agents/{oid}.json: id {ov['id']!r} must equal the file name")
        if ov["base_persona"] not in personas:
            probs.append(f"agents/{oid}.json: base_persona {ov['base_persona']!r} is not in harness/agents/")
        dom_ids = {p["id"] for p in rubric["pillars"] if p["kind"] == "domain"}
        if set(ov["pillar_ids"]) - dom_ids:
            probs.append(f"agents/{oid}.json: pillar_ids {sorted(set(ov['pillar_ids']) - dom_ids)} are not domain pillars")
        probs += [f"agents/{oid}.json: {x}" for x in overlay_cap_problems(ov)]
    # 7. figure packs
    missing = sorted(set(brief["figures"]["packs"]) - _packs())
    if missing:
        probs.append(f"rule 7: figure packs {missing} are not registered")
    # 8. nothing unresolved (answers A-M are enforced by the schema)
    if brief["unresolved"]:
        probs.append(f"rule 8: brief.unresolved is not empty: {brief['unresolved']}")
    # rubric rules
    a = brief["assessment"]
    probs += [f"rubric: {x}" for x in rubric_problems(rubric, a["mcq"]["enabled"] or a["cases"]["enabled"] or a["exercises"]["enabled"])]
    return {"questionnaire_ids": sorted(brief["answers"])}, probs
