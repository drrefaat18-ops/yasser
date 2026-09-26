"""Stdlib validator for exactly the JSON Schema subset in core §4."""
import json, pathlib, re

SCHEMAS = pathlib.Path(__file__).resolve().parent / "schemas"
KEYWORDS = {"type", "required", "properties", "additionalProperties", "items", "enum", "pattern",
            "minimum", "maximum", "minItems", "maxItems", "const"}
TYPES = {"object": dict, "array": list, "string": str, "boolean": bool, "null": type(None)}


def load_schema(name):
    return json.loads((SCHEMAS / f"{name}.v1.json").read_text(encoding="utf-8"))


def unknown_keywords(sch, ptr=""):
    bad = [f"{ptr}/{k}" for k in sch if k not in KEYWORDS]
    for k, sub in (sch.get("properties") or {}).items():
        bad += unknown_keywords(sub, f"{ptr}/properties/{k}")
    if isinstance(sch.get("items"), dict):
        bad += unknown_keywords(sch["items"], f"{ptr}/items")
    if isinstance(sch.get("additionalProperties"), dict):
        bad += unknown_keywords(sch["additionalProperties"], f"{ptr}/additionalProperties")
    return bad


def _type_ok(value, t):
    if t == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if t == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    return isinstance(value, TYPES[t])


def validate(doc, sch, ptr=""):
    errs = []
    loc = ptr or "/"
    if "type" in sch:
        types = sch["type"] if isinstance(sch["type"], list) else [sch["type"]]
        if not any(_type_ok(doc, t) for t in types):
            return [f"{loc}: expected {'|'.join(types)}"]
    if "const" in sch and doc != sch["const"]:
        errs.append(f"{loc}: must equal {sch['const']!r}")
    if "enum" in sch and doc not in sch["enum"]:
        errs.append(f"{loc}: {doc!r} not in {sch['enum']}")
    if isinstance(doc, str) and "pattern" in sch and not re.search(sch["pattern"], doc):
        errs.append(f"{loc}: does not match {sch['pattern']}")
    if isinstance(doc, (int, float)) and not isinstance(doc, bool):
        if "minimum" in sch and doc < sch["minimum"]:
            errs.append(f"{loc}: below minimum {sch['minimum']}")
        if "maximum" in sch and doc > sch["maximum"]:
            errs.append(f"{loc}: above maximum {sch['maximum']}")
    if isinstance(doc, list):
        if "minItems" in sch and len(doc) < sch["minItems"]:
            errs.append(f"{loc}: fewer than {sch['minItems']} items")
        if "maxItems" in sch and len(doc) > sch["maxItems"]:
            errs.append(f"{loc}: more than {sch['maxItems']} items")
        if isinstance(sch.get("items"), dict):
            for i, item in enumerate(doc):
                errs += validate(item, sch["items"], f"{ptr}/{i}")
    if isinstance(doc, dict):
        for k in sch.get("required", []):
            if k not in doc:
                errs.append(f"{ptr}/{k}: required")
        props = sch.get("properties", {})
        for k, v in doc.items():
            if k in props:
                errs += validate(v, props[k], f"{ptr}/{k}")
            elif sch.get("additionalProperties") is False:
                errs.append(f"{ptr}/{k}: not allowed")
            elif isinstance(sch.get("additionalProperties"), dict):
                errs += validate(v, sch["additionalProperties"], f"{ptr}/{k}")
    return errs
