# tests/test_manifest.py
import copy, hashlib, json, pathlib, subprocess, tempfile, unittest
from harness.tools import manifest

REPO = pathlib.Path(__file__).resolve().parents[1]
REAL = json.loads((REPO / "docs/harness/migration-manifest.json").read_text(encoding="utf-8"))
# DEC-034
APPROVED_SHA = "12785ebfcfe31a47e48577f56a084cda69ca0f17c6af22bc6e02cdaedb1f231f"
APPROVED_COMMIT = "b732b46"
# The approved hashes are of the working-tree bytes at approval time. These two sources were checked out
# CRLF while their committed blobs are LF, so a clean checkout differs from the manifest (step6-fixes.md).
EOL_DIVERGENT = {"AI_in_Medicine- Assistant Prof Dr Shereen Elkholy.md", "convert_docx_to_md.py"}

def git_repo(files):
    d = pathlib.Path(tempfile.mkdtemp())
    subprocess.run(["git", "init", "-q", str(d)], check=True)
    for rel, data in files.items():
        (d / rel).parent.mkdir(parents=True, exist_ok=True)
        (d / rel).write_bytes(data)
    subprocess.run(["git", "-C", str(d), "add", "-A"], check=True)
    return d

def one(src, dst, sha=None, **extra):
    m = {"schema_version": 1, "project": "p", "reserved": ["CLAUDE.md"], "path_fix_allowlist": [], "expected_diff": [],
         "moves": [{"source": src, "destination": dst, "sha256": sha or "0"}]}
    m.update(extra)
    return m

class ManifestInvariants(unittest.TestCase):
    def test_real_manifest_is_the_approved_one(self):
        raw = (REPO / "docs/harness/migration-manifest.json").read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), APPROVED_SHA)

    def test_real_manifest_pre_then_post_on_approved_tree(self):
        # the migration is one-way, so replay it on a worktree of the approval commit
        wt = pathlib.Path(tempfile.mkdtemp()) / "wt"
        subprocess.run(["git", "-C", str(REPO), "worktree", "add", "-q", "--detach", str(wt), APPROVED_COMMIT], check=True)
        try:
            dst = {e["source"]: e["destination"] for e in REAL["moves"]}
            self.assertEqual(manifest.problems(wt, REAL, "pre"),
                             [f"hash mismatch before move: {e['source']}" for e in REAL["moves"] if e["source"] in EOL_DIVERGENT])
            for e in REAL["moves"]:
                (wt / e["destination"]).parent.mkdir(parents=True, exist_ok=True)
                subprocess.run(["git", "-C", str(wt), "mv", e["source"], e["destination"]], check=True)
            self.assertEqual(manifest.problems(wt, REAL, "post"),
                             [f"hash mismatch after move: {dst[s]}" for s in dst if s in EOL_DIVERGENT])
        finally:
            subprocess.run(["git", "-C", str(REPO), "worktree", "remove", "--force", str(wt)], check=True)

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
        self.assertTrue(any("keep their paths" in p
                    for p in manifest.problems(REPO, one("images/a.png", "projects/p/assets/a.png"), "pre")))
        self.assertTrue(any("keep their paths" in p
                            for p in manifest.problems(REPO, one("rework/ch.md", "projects/p/src/ch.md"), "pre")))
        self.assertFalse(any("keep their paths" in p
                             for p in manifest.problems(REPO, one("images/a.png", "projects/p/images/a.png"), "pre")))

    def test_post_valid_move(self):
        d = git_repo({"projects/p/f.txt": b"x"})
        self.assertEqual(manifest.problems(d, one("f.txt", "projects/p/f.txt", sha=hashlib.sha256(b"x").hexdigest()), "post"), [])

    def test_post_changed_bytes(self):
        d = git_repo({"projects/p/f.txt": b"y"})
        probs = manifest.problems(d, one("f.txt", "projects/p/f.txt", sha=hashlib.sha256(b"x").hexdigest()), "post")
        self.assertTrue(any("hash mismatch after" in p for p in probs))

    def test_post_source_survives(self):
        d = git_repo({"f.txt": b"x", "projects/p/f.txt": b"x"})
        probs = manifest.problems(d, one("f.txt", "projects/p/f.txt", sha=hashlib.sha256(b"x").hexdigest()), "post")
        self.assertTrue(any("still present" in p for p in probs))

    def test_scope(self):
        m = one(".gitignore", "projects/p/z", path_fix_allowlist=["a.py"])
        self.assertEqual(manifest.scope_problems(REPO, m, ["a.py", "rep.md"], ["rep.md"]), [])
        self.assertTrue(manifest.scope_problems(REPO, m, ["b.py"], []))


if __name__ == "__main__":
    unittest.main()
