# tests/test_mutations.py
"""Core §9.3 minimum mutation set: each mutation yields its named check ID and a non-zero checker exit."""
import json, re, subprocess, sys, unittest
from tests.helpers import temp_repo, REPO

MUT = json.loads((REPO / "tests/fixtures/mutations/mutations.json").read_text(encoding="utf-8"))
OPS = {
    "delete_line_matching": lambda t, a: "\n".join(l for l in t.split("\n") if not re.search(a, l)),
    "replace_first": lambda t, a: t.replace(a[0], a[1], 1),
    "set_all_keys": lambda t, a: re.sub(r"(\*\*Q\d+\.) [A-D]\*\*", rf"\1 {a}**", t),
    "append_to_first_prose": lambda t, a: re.sub(r"(\n[A-Z][^\n>#|*-][^\n]*?\.)(\n)", rf"\1{a}\2", t, count=1),
    "delete_first_perspective_item": lambda t, a: re.sub(r"\n> - \*\*[^*]+:\*\*[^\n]*", "", t, count=1),
    "append_prose_words": lambda t, a: t.replace("\n## ", "\n" + " ".join(["word"] * a) + ".\n\n## ", 1),
}


def check(root):
    return subprocess.run([sys.executable, "harness/tools/check_book.py", "--project", "projects/ai-in-medicine", "--json"],
                          cwd=root, capture_output=True, text=True, encoding="utf-8")


def failing(r):
    return {c["id"] for t in json.loads(r.stdout)["targets"] for c in t["checks"] if c["status"] == "fail"}


class Mutations(unittest.TestCase):
    def test_each_mutation_yields_named_id(self):
        self.assertEqual(len(MUT), 7)
        for m in MUT:
            with self.subTest(m["name"]), temp_repo(project_from="projects/ai-in-medicine", stamp=True) as root:
                f = root / "projects/ai-in-medicine" / m["file"]
                before = f.read_text(encoding="utf-8")
                after = OPS[m["op"]](before, m["arg"])
                self.assertNotEqual(after, before, "the mutation did not change the file")
                f.write_text(after, encoding="utf-8")
                r = check(root)
                self.assertNotEqual(r.returncode, 0, r.stderr)
                self.assertIn(m["expect"], failing(r), r.stderr)

    def test_unmutated_book_passes(self):
        with temp_repo(project_from="projects/ai-in-medicine", stamp=True) as root:
            r = check(root)
            self.assertEqual(r.returncode, 0, r.stdout[-2000:] + r.stderr)
            self.assertEqual(failing(r), set())


if __name__ == "__main__":
    unittest.main()
