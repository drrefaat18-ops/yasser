# tests/test_ingest.py
"""Ingest stage (plan Task 8.4; core §2.4): custody, fidelity report, units, atomic swap, recovery."""
import json, os, pathlib, shutil, unittest
from unittest import mock
from harness import hashing
from tests.helpers import REPO, run_cli, stamp_project, temp_repo

FIX = REPO / "tests/fixtures/ingest"
NAMES = ["headings", "tables", "figures", "equations", "footnotes", "toc", "dropped-table"]
SLUG = "no-mcq"
INGEST = {"heading_rules": [{"pattern": "^Summary Notes$", "level": 2}], "toc_start_pattern": "^Contents$",
          "toc_entry_pattern": r"^(Chapter\s+\d+:.*?)\t+(\d+)$", "toc_end_pattern": r"^Chapter 1:[^\t]*$", "drop_source_toc": True}


def edit_json(path, fn):
    d = json.loads(path.read_text(encoding="utf-8"))
    fn(d)
    path.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def ingest_project(root, fixture):
    """A copy of a positive-config book whose approved source is one ingest fixture DOCX (re-stamped: test-only)."""
    p = root / "projects" / SLUG
    (p / "original").mkdir(exist_ok=True)
    shutil.copyfile(FIX / f"{fixture}.docx", p / "original/book.docx")
    sha = hashing.hash_file(p / "original/book.docx")
    edit_json(p / "brief.json", lambda b: b["source"].update(files=[{"path": "original/book.docx", "format": "docx", "sha256": sha}]))
    edit_json(p / "template.json", lambda t: t.update(ingest=INGEST))
    stamp_project(root, p)
    return p


def tree(p):
    return {f.relative_to(p).as_posix(): f.read_bytes() for f in sorted(p.rglob("*")) if f.is_file() and f.name != "state.json"}


def run_ingest(root):
    return run_cli(root, "--project", f"projects/{SLUG}", "run", "ingest")


class IngestFixtures(unittest.TestCase):
    def test_each_fixture_gives_its_literal_report(self):
        for name in NAMES:
            want = json.loads((FIX / f"{name}.expected.json").read_text(encoding="utf-8"))
            with self.subTest(name), temp_repo(f"positive-config/{SLUG}", slug=SLUG) as root:
                p = ingest_project(root, name)
                before = tree(p)
                r = run_ingest(root)
                self.assertEqual(r.returncode, want["exit"], r.stderr)
                if want["exit"] == 2:
                    self.assertIn("ERROR INGEST-LOST", r.stderr)
                    self.assertEqual(tree(p), before)   # previous outputs untouched
                    self.assertFalse((p / ".ingest-stage").exists())
                    st = json.loads((p / "state.json").read_text(encoding="utf-8"))
                    self.assertEqual(st["receipts"]["ingest"]["status"], "failed")
                    continue
                rep = json.loads((p / "ingest/conversion-report.json").read_text(encoding="utf-8"))
                for k, v in want["structures"].items():
                    self.assertEqual({x: rep["structures"][k][x] for x in v}, v, k)
                self.assertEqual(len(list((p / "ingest/assets").glob("*"))), want["assets"])
                if "omitted" in want:
                    self.assertEqual(rep["structures"]["text"]["omitted"], want["omitted"])
                    norm = (p / "ingest/normalized.md").read_text(encoding="utf-8")
                    for s in want["absent_from_normalized"]:
                        self.assertNotIn(s, norm)
                man = json.loads((p / "source-manifest.json").read_text(encoding="utf-8"))
                self.assertEqual(man["files"], [{"path": "source/book.docx", "original": "original/book.docx", "format": "docx",
                                                 "sha256": hashing.hash_file(p / "original/book.docx")}])
                self.assertEqual(hashing.hash_file(p / "source/book.docx"), hashing.hash_file(p / "original/book.docx"))
                v = run_cli(root, "--project", f"projects/{SLUG}", "verify", "--through", "ingest")
                self.assertEqual(v.returncode, 0, v.stderr)

    def test_units_ids_in_document_order(self):
        with temp_repo(f"positive-config/{SLUG}", slug=SLUG) as root:
            p = ingest_project(root, "headings")
            self.assertEqual(run_ingest(root).returncode, 0)
            units = json.loads((p / "ingest/units.json").read_text(encoding="utf-8"))["units"]
            self.assertEqual([(u["id"], u["heading"]) for u in units],
                             [("src-ch01", "Chapter 1: Motion"), ("src-ch01-s01", "Forces"), ("src-ch01-s02", "Summary Notes")])
            lines = (p / "ingest/normalized.md").read_text(encoding="utf-8").split("\n")
            u = units[1]
            self.assertEqual(hashing.hash_bytes("\n".join(lines[u["line_start"] - 1:u["line_end"]]).encode()), u["sha256"])
            self.assertTrue(lines[u["line_end"]].strip() == "" and units[2]["line_start"] > u["line_end"])

    def test_custody_hash_must_match_the_brief(self):
        with temp_repo(f"positive-config/{SLUG}", slug=SLUG) as root:
            p = ingest_project(root, "headings")
            with (p / "original/book.docx").open("ab") as f:
                f.write(b"\0")
            r = run_ingest(root)
            self.assertEqual(r.returncode, 1)
            self.assertIn("ERROR CUSTODY", r.stderr)

    def test_leftover_old_dir_refuses(self):
        with temp_repo(f"positive-config/{SLUG}", slug=SLUG) as root:
            p = ingest_project(root, "headings")
            (p / ".ingest-old").mkdir()
            r = run_ingest(root)
            self.assertEqual(r.returncode, 1)
            self.assertIn("ERROR INGEST-RECOVERY", r.stderr)
            self.assertTrue((p / ".ingest-old").is_dir())   # never deleted silently

    def test_new_skeleton_marker_survives_the_swap(self):
        with temp_repo(f"positive-config/{SLUG}", slug=SLUG) as root:
            p = root / "projects" / SLUG
            (p / "source").mkdir(exist_ok=True)
            (p / "source/.keep").write_text("", encoding="utf-8")
            edit_json(p / "state.json", lambda st: st["receipts"]["new"]["outputs"].update({"source/.keep": ""}))
            p = ingest_project(root, "headings")   # re-stamps: `new` records source/.keep, as a fresh `new` does
            r = run_ingest(root)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertTrue((p / "source/.keep").is_file())
            v = run_cli(root, "--project", f"projects/{SLUG}", "verify", "--through", "ingest")
            self.assertEqual(v.returncode, 0, v.stderr)

    def test_non_docx_needs_markitdown(self):
        from harness.stages import ingest
        with mock.patch.dict("sys.modules", {"markitdown": None}):
            with self.assertRaises(ingest.IngestError) as e:
                ingest._markitdown(pathlib.Path("book.pdf"))
        self.assertEqual(e.exception.code, "DEPENDENCY")
        self.assertIn("markitdown", str(e.exception))


class Swap(unittest.TestCase):
    def _project(self, tmp):
        p = pathlib.Path(tmp)
        for rel, text in (("a.txt", "old a"), ("d/b.txt", "old b")):
            (p / rel).parent.mkdir(parents=True, exist_ok=True)
            (p / rel).write_text(text)
        for rel, text in (("a.txt", "new a"), ("d/b.txt", "new b")):
            (p / ".ingest-stage" / rel).parent.mkdir(parents=True, exist_ok=True)
            (p / ".ingest-stage" / rel).write_text(text)
        return p

    def test_swap_promotes_the_stage(self):
        import tempfile
        from harness.stages import ingest
        with tempfile.TemporaryDirectory() as tmp:
            p = self._project(tmp)
            ingest.swap_dirs(p, ["a.txt", "d"])
            self.assertEqual(((p / "a.txt").read_text(), (p / "d/b.txt").read_text()), ("new a", "new b"))
            self.assertFalse((p / ".ingest-old").exists())

    def test_failure_during_swap_rolls_back(self):
        import tempfile
        from harness.stages import ingest
        with tempfile.TemporaryDirectory() as tmp:
            p = self._project(tmp)
            real, calls = os.replace, []

            def flaky(a, b):
                calls.append(1)
                if len(calls) == 2:
                    raise OSError("disk full")
                return real(a, b)
            with mock.patch("harness.stages.ingest.os.replace", side_effect=flaky):
                with self.assertRaises(OSError):
                    ingest.swap_dirs(p, ["a.txt", "d"])
            self.assertEqual(((p / "a.txt").read_text(), (p / "d/b.txt").read_text()), ("old a", "old b"))
            self.assertEqual((p / ".ingest-stage/a.txt").read_text(), "new a")   # nothing promoted


class MedicalIngest(unittest.TestCase):
    def test_medical_ingest_has_no_lost(self):
        """A fresh ingest of the medical source into a temp copy (never the real project, Rule 5)."""
        with temp_repo(project_from="projects/ai-in-medicine", stamp=True) as root:
            P = ["--project", "projects/ai-in-medicine"]
            self.assertEqual(run_cli(root, *P, "verify", "--through", "intake").returncode, 0)
            r = run_cli(root, *P, "run", "ingest")
            self.assertEqual(r.returncode, 0, r.stderr)
            rep = json.loads((root / "projects/ai-in-medicine/ingest/conversion-report.json").read_text(encoding="utf-8"))
            self.assertEqual({k for k, v in rep["structures"].items() if v["status"] == "lost"}, set())
            self.assertEqual(rep["structures"]["figures"]["output_count"], 24)
            self.assertEqual(rep["structures"]["text"]["omitted"][0]["reason"], "source_toc")


if __name__ == "__main__":
    unittest.main()
