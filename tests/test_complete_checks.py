# tests/test_complete_checks.py
import unittest
from harness.stages import complete_checks as cc
from tests.helpers import temp_repo

def rubric(domain):
    fixed = [dict(id=i, kind="fixed", weight=w, reviewer_ids=["r"], applicable=True, hard_caps=[])
             for i, w in (("G1", 20), ("G2", 20), ("G3", 10), ("G4", 10))]
    return {"pillars": fixed + [dict(id=f"D{n}", kind="domain", weight=w, reviewer_ids=["r"], applicable=True, hard_caps=[])
                                 for n, w in enumerate(domain)]}

class RubricRulesTest(unittest.TestCase):
    def test_single_domain_pillar_of_40_is_valid(self):
        self.assertEqual(cc.rubric_problems(rubric([40]), assessment_enabled=True), [])

    def test_five_domain_pillars_rejected(self):
        self.assertTrue(cc.rubric_problems(rubric([8, 8, 8, 8, 8]), assessment_enabled=True))

    def test_g3_moves_to_g2_only_when_all_assessment_disabled(self):
        r = rubric([40]); r["pillars"][2]["applicable"] = False; r["pillars"][1]["weight"] = 30
        self.assertEqual(cc.rubric_problems(r, assessment_enabled=False), [])
        self.assertTrue(cc.rubric_problems(r, assessment_enabled=True))

class ScoreTest(unittest.TestCase):
    def test_total_computed_and_cap_enforced(self):
        rub = rubric([40]); rub["pillars"][0]["hard_caps"] = [
            {"trigger": {"severity": "blocker", "min_count": 1, "tag": None}, "max_score": 4, "description": "x"}]
        findings = [{"id": "F-001", "pillar_id": "G1", "severity": "blocker", "tags": []}]
        card = {"pillars": [{"id": p["id"], "score": 8, "applicable": True} for p in rub["pillars"]],
                "caps_applied": [], "total": 80.0}
        probs = cc.score(rub, card, findings, fixes={})
        self.assertTrue(any("cap" in p for p in probs))
        card["pillars"][0]["score"] = 4
        card["caps_applied"] = [{"pillar_id": "G1", "cap_index": 0, "finding_ids": ["F-001"]}]
        card["total"] = round((4 * 20 + 8 * 20 + 8 * 10 + 8 * 10 + 8 * 40) / 10, 1)
        self.assertEqual(cc.score(rub, card, findings, fixes={}), [])

    def test_fixed_finding_does_not_trigger_cap(self):
        rub = rubric([40]); rub["pillars"][0]["hard_caps"] = [
            {"trigger": {"severity": "blocker", "min_count": 1, "tag": None}, "max_score": 4, "description": "x"}]
        findings = [{"id": "F-001", "pillar_id": "G1", "severity": "blocker", "tags": []}]
        card = {"pillars": [{"id": p["id"], "score": 8, "applicable": True} for p in rub["pillars"]],
                "caps_applied": [], "total": 80.0}
        self.assertEqual(cc.score(rub, card, findings, fixes={"F-001": "fixed + verified"}), [])


class RulingTest(unittest.TestCase):
    def test_bare_ruled_by_user_does_not_close(self):
        with temp_repo("state-basic", stamp=True) as root:
            p = root / "projects" / "fixture-book"
            (p / "evaluation").mkdir(exist_ok=True)
            f = p / "evaluation" / "fixes.md"
            f.write_text("| ID | real/rejected | root cause | siblings found | fix | status | DEC | verification → result |\n"
                         "|---|---|---|---|---|---|---|---|\n"
                         "| S-01 | real | x | none | y | ruled by user |  | n/a |\n", encoding="utf-8")
            rows, probs = cc.fixes_rows(p, f)
            self.assertIn("RULING-NO-DEC", " ".join(probs))
            f.write_text(f.read_text(encoding="utf-8").replace("ruled by user |  |", "ruled by user | DEC-001 |"),
                         encoding="utf-8")
            self.assertEqual(cc.fixes_rows(p, f)[1], [])


class OverlayCapsTest(unittest.TestCase):
    def test_boundaries(self):
        ok = {"scope": "x" * 400, "criteria": ["c" * 200] * 12, "exclusions": ["e"] * 8, "evidence_expectations": ["v"] * 8}
        self.assertEqual(cc.overlay_cap_problems(ok), [])
        for key, bad in [("scope", "x" * 401), ("criteria", ["c"] * 13), ("criteria", ["c" * 201]),
                         ("exclusions", ["e"] * 9), ("evidence_expectations", ["v"] * 9)]:
            with self.subTest(key=key):
                self.assertTrue(cc.overlay_cap_problems(dict(ok, **{key: bad})))


class IntakeTest(unittest.TestCase):
    def test_fixture_intake_is_clean_and_cross_rules_bite(self):
        import json
        with temp_repo("state-basic", stamp=True) as root:
            p = root / "projects" / "fixture-book"
            self.assertEqual(cc.intake(p)[1], [])
            b = json.loads((p / "brief.json").read_text(encoding="utf-8"))
            b["language"]["output"] = "fr"
            (p / "brief.json").write_text(json.dumps(b), encoding="utf-8")
            probs = " ".join(cc.intake(p)[1])
            for frag in ("rule 2", "TR-PAIR-UNSUPPORTED", "rule 3"):
                self.assertIn(frag, probs)
