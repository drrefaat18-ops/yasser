# tests/test_schema.py
import unittest
from harness import schema

S = {"type": "object", "required": ["a"], "additionalProperties": False,
     "properties": {"a": {"type": "integer", "minimum": 1}, "b": {"enum": ["x", "y"]},
                    "c": {"type": "array", "items": {"type": "string", "pattern": "^[a-z]+$"}, "maxItems": 2}}}

class SchemaTest(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(schema.validate({"a": 2, "b": "x", "c": ["ab"]}, S), [])

    def test_each_keyword_reports_pointer(self):
        errs = schema.validate({"a": 0, "b": "z", "c": ["A", "b", "c"], "d": 1}, S)
        joined = "\n".join(errs)
        for frag in ["/a", "/b", "/c/0", "/c", "/d"]:
            self.assertIn(frag, joined)

    def test_bool_is_not_integer(self):
        self.assertTrue(schema.validate({"a": True}, S))

    def test_every_shipped_schema_is_valid_subset(self):
        for name in ["brief", "rubric", "template", "theme", "chapter-plan", "overlay", "state", "findings",
                     "scorecard", "checker-report", "source-manifest", "conversion-report", "figures",
                     "golden", "golden-diff", "units"]:
            self.assertEqual(schema.unknown_keywords(schema.load_schema(name)), [], name)


class ShippedDataTest(unittest.TestCase):
    def test_locale_profiles_validate(self):
        import json, pathlib
        for f in (pathlib.Path(schema.SCHEMAS).parent / "locale").glob("*.json"):
            self.assertEqual(schema.validate(json.loads(f.read_text(encoding="utf-8")), schema.load_schema("locale")), [], f.name)
