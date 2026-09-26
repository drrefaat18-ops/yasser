"""Locale profiles (core §11 EXT-LOC-1), read from harness/locale/<primary>.json. Callers pass the profile as a
parameter; there is no global language. (Not harness/locale/__init__.py: a package there shadows the stdlib
`locale` module for any script run from harness/.)"""
import copy, json, pathlib

LOCALES = pathlib.Path(__file__).resolve().parent / "locale"


def primary(tag):
    """Primary language subtag of a BCP-47 tag: `ar-EG` -> `ar`."""
    return tag.split("-")[0].lower()


def exists(tag):
    return (LOCALES / f"{primary(tag)}.json").is_file()


def load_profile(tag):
    path = LOCALES / f"{primary(tag)}.json"
    if not path.is_file():
        raise FileNotFoundError(f"no locale profile for {tag!r} (looked for {path.name})")
    return json.loads(path.read_text(encoding="utf-8"))


def with_overrides(profile, overrides):
    """`template.locale_overrides` on top of a profile; nested objects merge one level deep."""
    out = copy.deepcopy(profile)
    for k, v in (overrides or {}).items():
        out[k] = {**out[k], **v} if isinstance(v, dict) and isinstance(out.get(k), dict) else v
    return out
