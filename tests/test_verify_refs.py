# tests/test_verify_refs.py
"""verify_refs no-DOI policy (plan Task 8.3; INV-46) and renumber_refs (INV-47). No network: fetch is injected."""
import subprocess, sys, unittest
from harness.tools import config, renumber_refs as rr, verify_refs as vr
from tests.helpers import REPO, temp_repo

CFG = {"template": {"references": {"entry_pattern": r"^(?P<n>\d+)\. (?P<body>.+)$",
                                   "identifier_patterns": [r"DOI:\s*(10\.\S+?)\.?\s*$", r"doi\.org/(10\.\S+?)\.?\s*$"],
                                   "no_doi_policy": {"allowed_types": ["web"], "requires_url": True},
                                   "type_patterns": {"web": r"(?i)\bweb page\b"},
                                   "title_match": {"mode": "heuristic", "words": 6, "threshold": 0.6}}},
       "profile_out": {"tag": "en", "normalisation": {"compare": ["NFC", "casefold"]}}}


class VerifyRefs(unittest.TestCase):
    def test_no_doi_without_allowed_type_fails(self):
        r = vr.classify_line(1, "Smith J. A book about things. Publisher; 2020.", CFG, fetch=lambda d: None)
        self.assertEqual((r["doi_status"], r["check_id"]), ("no_doi", "REF-NO-DOI-DISALLOWED"))

    def test_no_doi_allowed_type_needs_url(self):
        ok = vr.classify_line(1, "Org. A web page on things. https://example.org/x", CFG, fetch=None)
        self.assertEqual((ok["type"], ok["check_id"]), ("web", None))
        bare = vr.classify_line(2, "Org. A web page on things.", CFG, fetch=None)
        self.assertEqual(bare["check_id"], "REF-NO-DOI-DISALLOWED")

    def test_lower_case_doi_is_still_checked(self):
        r = vr.classify_line(6, "Doe A. Deep learning for images of cells. J. 2021. doi:10.1/y", CFG,
                             fetch=lambda d: "Deep learning for images of cells")
        self.assertEqual((r["doi"], r["doi_status"]), ("10.1/y", "exists"))

    def test_network_error_is_ref_error(self):
        def boom(doi):
            raise OSError("timed out")
        r = vr.classify_line(2, "Doe A. Title words here now. J. 2021. DOI: 10.1/x", CFG, fetch=boom)
        self.assertEqual((r["doi_status"], r["check_id"]), ("error", "REF-ERROR"))

    def test_title_match(self):
        r = vr.classify_line(3, "Doe A. Deep learning for images of cells. J. 2021. DOI: 10.1/y", CFG,
                             fetch=lambda d: "Deep learning for images of cells")
        self.assertEqual((r["doi_status"], r["title_status"], r["check_id"]), ("exists", "match", None))

    def test_existence_and_title_are_separate(self):
        miss = vr.classify_line(4, "Doe A. Deep learning for images of cells. DOI: 10.1/z", CFG, fetch=lambda d: "Unrelated words entirely here")
        self.assertEqual((miss["doi_status"], miss["title_status"], miss["check_id"]), ("exists", "mismatch", "REF-TITLE-MISMATCH"))
        gone = vr.classify_line(5, "Doe A. X. DOI: 10.1/q", CFG, fetch=lambda d: None)
        self.assertEqual((gone["doi_status"], gone["check_id"]), ("not_found", "REF-NOT-FOUND"))

    def test_other_title_modes_wait_for_step10(self):
        cfg = {"template": {"references": dict(CFG["template"]["references"], title_match={"mode": "manual", "words": 6, "threshold": 0.6})},
               "profile_out": CFG["profile_out"]}
        with self.assertRaises(vr.ConfigError):
            vr.classify_line(1, "A. B. DOI: 10.1/y", cfg, fetch=lambda d: "B")

    def test_medical_policy_classification(self):
        """The approved policy (DEC-036, DEC-042): laws, regulations and guidance with a URL pass; five do not."""
        cfg = config.load(REPO / "projects/ai-in-medicine")
        bad = []
        for c, p in cfg.chapters():
            bad += [(c["id"], r["n"]) for r in vr.check_chapter(p, cfg, fetch=lambda d: None) if r["check_id"] == "REF-NO-DOI-DISALLOWED"]
        self.assertEqual(bad, [("ch01", 2), ("ch04", 3), ("ch05", 1), ("ch05", 8), ("ch11", 12)])

    def test_providers_merge_defaults_and_template(self):
        cfg = {"template": {"references": {"providers": {"crossref": {"timeout_s": 5}}}}}
        p = vr.providers(cfg)["crossref"]
        self.assertEqual((p["timeout_s"], p["retries"]), (5, 5))


class Renumber(unittest.TestCase):
    def test_renumber_by_first_appearance(self):
        cfg = config.load(REPO / "tests/fixtures/positive-config/no-mcq")
        t = "A [3]. B [1, 3]. C [5–7].\n\n## References\n1. one\n2. two\n3. three\n5. five\n6. six\n7. seven\n"
        r = rr.renumber(t, cfg)
        self.assertTrue(r.startswith("A [1]. B [1, 2]. C [3–5]."), r)
        self.assertNotIn("two", r)
        self.assertTrue(r.rstrip().endswith("5. seven"), r)
        with self.assertRaises(rr.MissingReference):
            rr.renumber("A [9].\n\n## References\n1. one\n", cfg)

    def test_cli_takes_chapter_ids_only(self):
        with temp_repo("positive-config/no-mcq", slug="no-mcq", stamp=True) as root:
            run = lambda *a: subprocess.run([sys.executable, "harness/tools/renumber_refs.py", "--project", "projects/no-mcq", *a],
                                            cwd=root, capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(run("--chapter", "ch01").returncode, 0)
            r = run("--chapter", "chapters/ch01-forces.md")
            self.assertEqual(r.returncode, 2)
            self.assertIn("ERROR CONFIG", r.stderr)


if __name__ == "__main__":
    unittest.main()
