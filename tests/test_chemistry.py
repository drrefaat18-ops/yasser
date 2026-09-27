# tests/test_chemistry.py
"""Chemistry pack (core §7.5; plan Task 9.2). PubChem is always mocked; no test reaches the network."""
import json, pathlib, tempfile, unittest
from unittest import mock
from harness.figures.packs import chemistry as chem
import importlib
audit = importlib.import_module("harness.stages.complete_checks.audit")


def answer(smiles, key="CanonicalSMILES"):
    body = json.dumps({"PropertyTable": {"Properties": [{"CID": 1, key: smiles}]}}).encode()
    return mock.MagicMock(__enter__=lambda s: s, __exit__=lambda *a: False, read=lambda: body)


ASPIRIN = {"kind": "chem.structure", "name": "aspirin", "smiles": "CC(=O)Oc1ccccc1C(=O)O"}


@unittest.skipUnless(chem.preflight() == [], "rdkit missing")
class Chemistry(unittest.TestCase):
    def setUp(self):
        self._t = tempfile.TemporaryDirectory()
        self.addCleanup(self._t.cleanup)
        self.cache = self._t.name

    def test_invalid_smiles_fails(self):
        ids = [f["id"] for f in chem.validate({"kind": "chem.structure", "smiles": "C1CC(", "name": "bad"})]
        self.assertIn("CHEM-SMILES-INVALID", ids)

    def test_unsanitisable_smiles_is_sanitize(self):
        ids = [f["id"] for f in chem.validate({"kind": "chem.structure", "smiles": "c1cccc1", "name": "bad ring"})]
        self.assertEqual(ids, ["CHEM-SANITIZE"])     # parses, but the 5-ring cannot be kekulised

    def test_valid_structure_renders(self):
        with tempfile.TemporaryDirectory() as t:
            svg, png = pathlib.Path(t, "a.svg"), pathlib.Path(t, "a.png")
            chem.render(ASPIRIN, svg, png)
            first = (svg.read_bytes(), png.read_bytes())
            chem.render(ASPIRIN, svg, png)
            self.assertEqual((svg.read_bytes(), png.read_bytes()), first)   # byte-identical re-render
            self.assertTrue(first[0].startswith(b"<?xml"))

    def test_invalid_structure_does_not_render(self):
        with tempfile.TemporaryDirectory() as t, self.assertRaises(chem.ChemistryError):
            chem.render({"kind": "chem.structure", "smiles": "C1CC(", "name": "bad"}, pathlib.Path(t, "a.svg"),
                        pathlib.Path(t, "a.png"))

    def test_reaction_render_bytes_identical(self):
        with tempfile.TemporaryDirectory() as t:
            svg, png = pathlib.Path(t, "r.svg"), pathlib.Path(t, "r.png")
            spec = {"kind": "chem.reaction", "smarts": "CCO>>CC=O", "name": "oxidation"}
            chem.render(spec, svg, png); first = (svg.read_bytes(), png.read_bytes())
            chem.render(spec, svg, png)
            self.assertEqual((svg.read_bytes(), png.read_bytes()), first)

    def test_reaction_smarts(self):
        self.assertEqual(chem.validate({"kind": "chem.reaction", "smarts": "CCO>>CC=O", "name": "oxidation"}), [])
        for bad in ("CC(>>", "CCO", ">>CC=O"):
            self.assertIn("CHEM-SMARTS-INVALID",
                          [f["id"] for f in chem.validate({"kind": "chem.reaction", "smarts": bad, "name": "bad"})], bad)

    def test_offline_is_unverified(self):
        with mock.patch("urllib.request.urlopen", side_effect=OSError("offline")):
            r = chem.crosscheck(ASPIRIN, "live", self.cache)
        self.assertEqual(r["status"], "unverified")
        self.assertEqual(chem.crosscheck({"name": "aspirin"}, "offline", self.cache)["status"], "unverified")
        self.assertEqual(list(pathlib.Path(self.cache).iterdir()), [])   # a failure is never cached

    def test_mocked_mismatch(self):
        with mock.patch("urllib.request.urlopen", return_value=answer("CCO")):
            r = chem.crosscheck(ASPIRIN, "live", self.cache)
        self.assertEqual(r["status"], "fail")

    def test_mocked_match_is_cached(self):
        for key in ("CanonicalSMILES", "ConnectivitySMILES"):   # PubChem's old and new property names
            with self.subTest(key), tempfile.TemporaryDirectory() as cache:
                with mock.patch("urllib.request.urlopen", return_value=answer("CC(=O)OC1=CC=CC=C1C(=O)O", key)) as u:
                    self.assertEqual(chem.crosscheck(ASPIRIN, "live", cache)["status"], "pass")
                    self.assertEqual(chem.crosscheck(ASPIRIN, "live", cache)["status"], "pass")
                self.assertEqual(u.call_count, 1)             # the second lookup came from the cache
                self.assertIn("timeout", u.call_args.kwargs)

    def test_enantiomer_is_a_mismatch(self):   # S9-05
        l_ala = {"kind": "chem.structure", "name": "L-alanine", "smiles": "C[C@@H](C(=O)O)N"}
        with mock.patch("urllib.request.urlopen", return_value=answer("C[C@H](C(=O)O)N", "SMILES")):
            self.assertEqual(chem.crosscheck(l_ala, "live", self.cache)["status"], "fail")
        with tempfile.TemporaryDirectory() as c, \
                mock.patch("urllib.request.urlopen", return_value=answer("N[C@@H](C)C(=O)O", "IsomericSMILES")):
            r = chem.crosscheck(l_ala, "live", c)
        self.assertEqual(r["status"], "pass")
        self.assertTrue(r["url"].endswith("/property/IsomericSMILES/JSON"))
        self.assertEqual((r["how"], len(r["response_sha256"])), ("live", 64))   # S9-06: the evidence it judged on
        with tempfile.TemporaryDirectory() as c, \
                mock.patch("urllib.request.urlopen", return_value=answer("CC(C(=O)O)N", "ConnectivitySMILES")):
            self.assertEqual(chem.crosscheck(l_ala, "live", c)["status"], "unverified")   # no stereo to compare

    def test_bad_answer_is_unverified(self):
        body = mock.MagicMock(__enter__=lambda s: s, __exit__=lambda *a: False, read=lambda: b"<html>busy</html>")
        with mock.patch("urllib.request.urlopen", return_value=body):
            self.assertEqual(chem.crosscheck(ASPIRIN, "live", self.cache)["status"], "unverified")


class AuditChemGate(unittest.TestCase):
    """core §7.5: complete audit refuses while a figure is CHEM-UNVERIFIED, unless ruled by the user with a real DEC."""

    def setUp(self):
        self._t = tempfile.TemporaryDirectory()
        self.addCleanup(self._t.cleanup)
        self.p = pathlib.Path(self._t.name)
        (self.p / "build").mkdir()
        (self.p / "audit").mkdir()
        (self.p / "build/build-report.json").write_text(json.dumps({"chem_unverified": ["aspirin"]}), encoding="utf-8")
        (self.p / "decisions.md").write_text("| DEC | Decision |\n|---|---|\n| DEC-007 | accept aspirin unverified |\n",
                                             encoding="utf-8")

    def fixes(self, row):
        (self.p / "audit/fixes.md").write_text("| ID | status | DEC |\n|---|---|---|\n" + row + "\n", encoding="utf-8")

    def test_unverified_blocks(self):
        self.assertEqual(len(audit.chem_unverified_problems(self.p)), 1)

    def test_ruled_by_user_with_real_dec_clears(self):
        self.fixes("| aspirin | ruled by user | DEC-007 |")
        self.assertEqual(audit.chem_unverified_problems(self.p), [])

    def test_ruling_needs_an_existing_dec(self):
        for row in ("| aspirin | ruled by user | DEC-999 |", "| aspirin | ruled by user | yes |", "| aspirin | fixed | DEC-007 |"):
            with self.subTest(row):
                self.fixes(row)
                self.assertEqual(len(audit.chem_unverified_problems(self.p)), 1)


if __name__ == "__main__":
    unittest.main()
