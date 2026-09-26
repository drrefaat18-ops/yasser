"""Task 7.4: the medical project's config reproduces the old hardcoded behaviour (core §10)."""
import importlib.util, json, unittest
from harness import schema
from harness.stages import complete_checks as cc
from tests.helpers import REPO

P = REPO / "projects" / "ai-in-medicine"


def load(rel):
    return json.loads((P / rel).read_text(encoding="utf-8"))


def legacy(name):
    spec = importlib.util.spec_from_file_location(f"legacy_{name}", P / "rework" / "tools" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)   # import only: the gate shim sits under __main__
    return mod


class MedicalConfigTest(unittest.TestCase):
    def test_files_validate(self):
        for rel, name in [("brief.json", "brief"), ("rubric.json", "rubric"), ("template.json", "template"),
                          ("theme.json", "theme"), ("agents/clinical-accuracy.json", "overlay"),
                          ("design/chapter-plan.json", "chapter-plan")]:
            self.assertEqual(schema.validate(load(rel), schema.load_schema(name)), [], rel)

    def test_intake_and_design_checks_pass(self):
        self.assertEqual(cc.intake(P)[1], [])
        self.assertEqual(cc.design(P, None)[1], [])

    def test_matches_legacy_constants(self):
        cb = legacy("check_book")
        plan = load("design/chapter-plan.json")
        self.assertEqual({int(c["id"][2:]): c["word_budget"] for c in plan["chapters"]}, cb.BUDGETS)
        t = load("template.json")
        self.assertEqual([c["syntax"] for c in t["callouts"] if c["required"]], [f"> **{b}**" for b in cb.BOXES])
        self.assertEqual([i["label"] for i in t["perspectives"]["items"]], cb.LENSES)
        self.assertEqual([s["label"] for s in t["sections"] if s["required"]], cb.REQUIRED_H2)
        r = t["readability"]
        self.assertEqual((r["mean_sentence_max"], r["long_sentence_words"]), (cb.MAX_MEAN, cb.LONG))
        self.assertEqual(t["budgets"]["front_matter"], cb.FRONT_BUDGET)
