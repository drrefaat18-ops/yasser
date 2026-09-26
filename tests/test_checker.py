# tests/test_checker.py
"""Config-driven checker (plan Task 8.1): parsing, not_applicable rules, config defaults, CLI contract."""
import copy, json, pathlib, subprocess, sys, tempfile, unittest
from harness import schema
from harness.tools import check_book as cb, config
from tests.helpers import REPO, temp_repo

FIX = REPO / "tests/fixtures/positive-config/no-errata"


def cfg_of(path=FIX, **template_changes):
    c = config.load(path)
    for k, v in template_changes.items():
        c["template"][k] = v
    return c


def report_for(text, cfg):
    with tempfile.TemporaryDirectory() as t:
        p = pathlib.Path(t, "ch01.md")
        p.write_text(text, encoding="utf-8")
        return {c["id"]: c for c in cb.check_chapter(p, cfg, {"id": "ch01", "word_budget": 0})["checks"]}


CHAPTER = (FIX / "chapters/ch01-forces.md").read_text(encoding="utf-8")


class CheckerTest(unittest.TestCase):
    def test_report_validates_and_every_id_once(self):
        rep = cb.check_book(cfg_of())
        sch = schema.load_schema("checker-report")
        for t in rep["targets"]:
            self.assertEqual(schema.validate(t, sch), [], t["target"])
            ids = [c["id"] for c in t["checks"]]
            self.assertEqual(len(ids), len(set(ids)), t["target"])
        self.assertEqual(cb.failures(rep), [])

    def test_labels_come_from_config(self):
        """EXT-LOC-3: renaming a section label in template.json moves the check with it."""
        cfg = cfg_of()
        for s in cfg["template"]["sections"]:
            if s["role"] == "references":
                s["label"] = "Sources"
        self.assertEqual(report_for(CHAPTER, cfg)["TPL-SECTION-MISSING"]["status"], "fail")
        self.assertEqual(report_for(CHAPTER.replace("## References", "## Sources"), cfg)["TPL-SECTION-MISSING"]["status"], "pass")

    def test_callout_count_bounds(self):
        doubled = CHAPTER.replace("> **Viewpoints**", "> **Viewpoints**\n\n> **Viewpoints**", 1)
        self.assertEqual(report_for(doubled, cfg_of())["TPL-CALLOUT-COUNT"]["status"], "fail")

    def test_readability_default_from_locale(self):
        t = json.loads((FIX / "template.json").read_text(encoding="utf-8"))
        t["readability"] = {"mean_sentence_max": None, "long_sentence_words": None, "long_share_max": None}
        filled = config.with_locale_defaults(t, config.locales.load_profile("en"))
        self.assertEqual(filled["readability"], {"mean_sentence_max": 16, "long_sentence_words": 28, "long_share_max": 0.05})
        self.assertEqual(filled["chapter_heading_pattern"], config.locales.load_profile("en")["chapter_heading_pattern"])

    def test_disabled_learning_objectives_are_not_applicable(self):
        cfg = cfg_of()
        cfg["template"]["learning_objectives"] = dict(cfg["template"]["learning_objectives"], enabled=False)
        rep = report_for(CHAPTER, cfg)
        for cid in ("LO-COUNT", "LO-VERB", "LO-UNASSESSED", "MCQ-LO-TAG", "MCQ-LO-UNKNOWN"):
            self.assertEqual(rep[cid]["status"], "not_applicable", cid)

    def test_key_run_uses_max_run(self):
        cfg = cfg_of()
        run = CHAPTER.replace("**Q1. B**", "**Q1. C**").replace("**Q2. A**", "**Q2. C**")
        self.assertEqual(report_for(run, cfg)["KEY-RUN"]["status"], "fail")
        cfg["template"]["assessment"]["mcq"]["max_run"] = 3
        cfg["template"]["assessment"]["mcq"]["key_balance"] = {"min": 0, "max": 3}
        self.assertEqual(report_for(run, cfg)["KEY-RUN"]["status"], "pass")

    def test_extra_option_label(self):
        extra = CHAPTER.replace("D) It makes the object lighter.", "D) It makes the object lighter.\nE) None of these.")
        rep = report_for(extra, cfg_of())
        self.assertEqual(rep["MCQ-EXTRA-OPTION"]["status"], "fail")
        self.assertEqual(rep["MCQ-OPTIONS"]["status"], "pass")

    def test_errata_status_cells(self):
        cfg = cfg_of(REPO / "tests/fixtures/positive-config/no-mcq")
        with tempfile.TemporaryDirectory() as t:
            p = pathlib.Path(t, "e.md")
            p.write_text("Status: `open` is the first state.\n\n| # | Status |\n|---|---|\n| 1 | fixed (Ch1) |\n| 2 | open (see Ch2) |\n",
                         encoding="utf-8")
            self.assertEqual(cb.errata_open(p, cfg), ["2"])

    def test_entry_pattern_contract(self):
        import re
        for pat, line, want in [(r"^(\d+)\. (.+)$", "3. Body text", (3, "Body text")),
                                (r"^(?P<n>\d+)\. (?P<body>.+)$", "4. More", (4, "More")),
                                (r"^(\d+)\. ", "5. Rest of line", (5, "Rest of line"))]:
            self.assertEqual(cb.entry_parts(re.search(pat, line), line), want)

    def test_parse_exposes_ids(self):
        cfg = cfg_of()
        p = cb.parse(CHAPTER, cfg)
        self.assertEqual(p["h1"], {"num": "1", "title": "Forces and Motion"})
        self.assertIn("references", [s["id"] for s in p["sections"]])
        self.assertEqual([c["id"] for c in p["callouts"]], ["key-idea", "viewpoints"])
        self.assertEqual(p["objectives"], ["1", "2", "3"])
        self.assertEqual(p["mcqs"], [1, 2, 3])
        self.assertEqual(p["key"], {1: "B", 2: "A", 3: "C"})
        self.assertEqual(p["citations"], [1, 2])

    def test_unsupported_citation_style_is_a_config_error(self):
        cfg = cfg_of()
        cfg["template"]["citations"] = dict(cfg["template"]["citations"], style="author-year")
        with self.assertRaises(cb.ConfigError):
            report_for(CHAPTER, cfg)


class ToolPathsTest(unittest.TestCase):
    def test_tool_paths_cover_every_harness_module_the_tool_imports(self):   # N9, S7-04 sibling
        import re
        from harness import state
        control = {"state", "hashing", "paths", "schema", "gate"}
        for stage, tool in (("rework", "harness/stages/complete_checks/rework.py"), ("build", "harness/stages/build.py"),
                            ("ingest", "harness/stages/ingest.py")):
            tp, todo, seen = set(state.BY_ID[stage]["tool_paths"]), [tool], set()
            while todo:
                m = todo.pop()
                if m in seen:
                    continue
                seen.add(m)
                self.assertIn(m, tp, f"{stage}: {m} is executed but not in tool_paths")
                src = (REPO / m).read_text(encoding="utf-8")
                for pkg, names in re.findall(r"^\s*from (harness(?:\.tools|\.stages)?) import (.+?)(?:\s+#.*)?$", src, re.M):
                    for n in (x.strip().split(" as ")[0] for x in names.split(",")):
                        if n not in control:
                            todo.append(f"{pkg.replace('.', '/')}/{n}.py")


class CheckerCliTest(unittest.TestCase):
    def test_gated_json_and_exit_codes(self):
        with temp_repo("positive-config/no-errata", slug="no-errata", stamp=True) as root:
            run = lambda *a: subprocess.run([sys.executable, "harness/tools/check_book.py", *a], cwd=root,
                                            capture_output=True, text=True, encoding="utf-8")
            r = run("--project", "projects/no-errata", "--json", "--chapter", "ch01")
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual([t["target"] for t in json.loads(r.stdout)["targets"]], ["ch01"])
            self.assertIn("ERROR CONFIG", run("--project", "projects/no-errata", "--chapter", "ch99").stderr)
            ch = root / "projects/no-errata/chapters/ch01-forces.md"
            ch.write_text(ch.read_text(encoding="utf-8").replace("[2]", "[7]", 1), encoding="utf-8")
            r = run("--project", "projects/no-errata")
            self.assertEqual(r.returncode, 1)
            self.assertIn("FAIL ch01 CIT-MISSING", r.stdout)
            (root / "projects/no-errata/brief.json").write_text("{}", encoding="utf-8")
            r = run("--project", "projects/no-errata")
            self.assertEqual(r.returncode, 1)
            self.assertIn("ERROR APPROVAL-STALE", r.stderr)


if __name__ == "__main__":
    unittest.main()
