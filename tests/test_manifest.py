# tests/test_manifest.py
import copy, json, pathlib, unittest
from harness.tools import manifest

REPO = pathlib.Path(__file__).resolve().parents[1]
REAL = json.loads((REPO / "docs/harness/migration-manifest.json").read_text(encoding="utf-8"))

def one(src, dst, sha=None, **extra):
    m = {"schema_version": 1, "project": "p", "reserved": ["CLAUDE.md"], "path_fix_allowlist": [], "expected_diff": [],
         "moves": [{"source": src, "destination": dst, "sha256": sha or "0"}]}
    m.update(extra)
    return m

class ManifestInvariants(unittest.TestCase):
    def test_real_manifest_pre_ok(self):
        self.assertEqual(manifest.problems(REPO, REAL, "pre"), [])

    def test_reserved_never_moved(self):
        self.assertTrue(any("reserved" in p for p in manifest.problems(REPO, one("CLAUDE.md", "projects/p/CLAUDE.md"), "pre")))

    def test_untracked_source(self):
        self.assertTrue(any("not tracked" in p for p in manifest.problems(REPO, one("nope.md", "projects/p/nope.md"), "pre")))

    def test_existing_destination(self):
        self.assertTrue(any("exists" in p for p in manifest.problems(REPO, one(".gitignore", "CLAUDE.md"), "pre")))

    def test_wrong_hash(self):
        self.assertTrue(any("hash" in p for p in manifest.problems(REPO, one(".gitignore", "projects/p/.gitignore", sha="0" * 64), "pre")))

    def test_duplicate_destination(self):
        m = one(".gitignore", "projects/p/x")
        m["moves"].append({"source": "CLAUDE.md", "destination": "projects/p/x", "sha256": "0"})
        self.assertTrue(any("duplicate" in p for p in manifest.problems(REPO, m, "pre")))

    def test_post_requires_moved_state(self):
        self.assertTrue(any("missing" in p for p in manifest.problems(REPO, one(".gitignore", "projects/p/never.txt"), "post")))

    def test_expected_diff_format(self):
        m = one(".gitignore", "projects/p/y", expected_diff=[{"pointer": "/x"}])
        self.assertTrue(any("expected_diff" in p for p in manifest.problems(REPO, m, "pre")))

    def test_images_beside_rework(self):
        dests = {pathlib.PurePosixPath(e["destination"]).parts[2] for e in REAL["moves"]
                 if e["source"].startswith(("images/", "rework/"))}
        self.assertEqual(dests, {"images", "rework"})

    def test_scope(self):
        m = one(".gitignore", "projects/p/z", path_fix_allowlist=["a.py"])
        self.assertEqual(manifest.scope_problems(REPO, m, ["a.py", "rep.md"], ["rep.md"]), [])
        self.assertTrue(manifest.scope_problems(REPO, m, ["b.py"], []))


if __name__ == "__main__":
    unittest.main()
