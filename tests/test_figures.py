# tests/test_figures.py
"""Figure system (core §7; plan Task 9.1): deterministic renders, the figure checker, numbering, build gating."""
import json, os, pathlib, tempfile, unittest
from unittest import mock
from harness import figures, preflight
from harness.figures import check_figures, render
from harness.tools import config
from tests.helpers import run_cli, temp_repo

SLUG = "figures-book"
P = ["--project", f"projects/{SLUG}"]
BROWSER = preflight.check_browser("figures")["ok"]
WORD = preflight.check_word()["ok"]
CHEM = preflight.check_rdkit()["ok"]


def load(p):
    return json.loads(pathlib.Path(p).read_text(encoding="utf-8"))


def edit_manifest(project, fid, **changes):
    m = project / "figures/figures.json"
    man = load(m)
    for f in man["figures"]:
        if f["id"] == fid:
            f.update(changes)
    m.write_text(json.dumps(man, indent=1), encoding="utf-8")


def finish_rework(root):
    """Real `begin rework` + one `complete --unit` per chapter + the final `complete` (figures are rework outputs)."""
    r = run_cli(root, *P, "begin", "rework")
    assert r.returncode == 0, r.stderr
    n = r.stdout.split("nonce=")[1].split()[0]
    for u in ("ch01", "ch02"):
        r = run_cli(root, *P, "complete", "rework", "--nonce", n, "--unit", u)
        assert r.returncode == 0, r.stderr
    r = run_cli(root, *P, "complete", "rework", "--nonce", n)
    assert r.returncode == 0, r.stderr


class Figures(unittest.TestCase):
    def fixture(self):
        return temp_repo(SLUG, slug=SLUG, stamp=True)

    def render_check(self, project, out):
        cfg = config.load(project)
        render.render_all(project, cfg, out)
        return check_figures.check(project, cfg, out, crosscheck_mode="offline")

    def test_chart_bytes_identical(self):
        with self.fixture() as root, tempfile.TemporaryDirectory() as t:
            src = root / "projects" / SLUG / "figures/src/speed-bar.py"
            runs = []
            for k in (1, 2):
                svg, png = pathlib.Path(t, f"{k}.svg"), pathlib.Path(t, f"{k}.png")
                from harness.figures import charts
                charts.render(src, svg, png, 14)
                runs.append((svg.read_bytes(), png.read_bytes()))
            self.assertEqual(runs[0], runs[1])
            self.assertTrue(runs[0][0].lstrip().startswith(b"<?xml"))
            self.assertNotIn(b"<dc:date>", runs[0][0])

    @unittest.skipUnless(BROWSER, "no Edge or Chrome")
    def test_svg_raster_bytes_identical(self):
        with self.fixture() as root, tempfile.TemporaryDirectory() as t:
            src = root / "projects" / SLUG / "figures/src/friction-diagram.svg"
            a, b = pathlib.Path(t, "a.png"), pathlib.Path(t, "b.png")
            render.rasterise_svg(src, a, 14)
            render.rasterise_svg(src, b, 14)
            self.assertEqual(a.read_bytes(), b.read_bytes())

    @unittest.skipUnless(BROWSER and CHEM, "needs Edge/Chrome and rdkit (the fixture has chemistry figures)")
    def test_clean_fixture_passes(self):
        with self.fixture() as root, tempfile.TemporaryDirectory() as t:
            rep = self.render_check(root / "projects" / SLUG, pathlib.Path(t, "out"))
            self.assertEqual(check_figures.blocking(rep), [])
            self.assertEqual({c["status"] for c in rep["checks"] if c["id"].startswith("FIG-")}, {"pass"})

    @unittest.skipUnless(BROWSER and CHEM, "needs Edge/Chrome and rdkit (the fixture has chemistry figures)")
    def test_each_fig_id(self):
        """One fixture defect per check ID (core §7.3) -> that ID fails and the checker CLI logic exits 1."""
        defects = {
            "FIG-UNREFERENCED": lambda p: (p / "chapters/ch01-forces.md").write_text(
                (p / "chapters/ch01-forces.md").read_text(encoding="utf-8").replace("![](fig:speed-bar)", ""), encoding="utf-8"),
            "FIG-UNKNOWN": lambda p: (p / "chapters/ch02-friction-graphs.md").write_text(
                (p / "chapters/ch02-friction-graphs.md").read_text(encoding="utf-8") + "\n![](fig:no-such-figure)\n", encoding="utf-8"),
            "FIG-CAPTION": lambda p: edit_manifest(p, "speed-bar", caption="  "),
            "FIG-ALT": lambda p: edit_manifest(p, "speed-line", alt=""),
            "FIG-LICENCE": lambda p: edit_manifest(p, "rolling-ball", licence="all-rights-reserved"),
            "FIG-RESOLUTION": lambda p: _small_png(p / "chapters/figures/rolling-ball.png"),
            "FIG-AUTHOR-ASSET": lambda p: edit_manifest(p, "rolling-ball", kind="author-asset", status="needs-author-asset"),
        }
        for cid, apply in defects.items():
            with self.subTest(cid), self.fixture() as root, tempfile.TemporaryDirectory() as t:
                p = root / "projects" / SLUG
                apply(p)
                rep = self.render_check(p, pathlib.Path(t, "out"))
                failing = {c["id"] for c in check_figures.blocking(rep)}
                self.assertEqual(failing, {cid}, rep)

    def test_direct_image_link_is_unknown(self):
        with self.fixture() as root, tempfile.TemporaryDirectory() as t:
            p = root / "projects" / SLUG
            ch = p / "chapters/ch01-forces.md"
            ch.write_text(ch.read_text(encoding="utf-8") + "\n![x](figures/rolling-ball.png)\n", encoding="utf-8")
            rep = check_figures.check(p, config.load(p), pathlib.Path(t, "out"))
            unknown = next(c for c in rep["checks"] if c["id"] == "FIG-UNKNOWN")
            self.assertEqual(unknown["status"], "fail")
            self.assertIn("without the manifest", unknown["message"])

    def test_manifest_problems_are_fig_manifest(self):
        cases = {"kind/status": dict(status="existing"), "source outside src": dict(source="chapters/figures/rolling-ball.png"),
                 "unknown chapter": dict(chapter_id="ch09")}
        for name, change in cases.items():
            with self.subTest(name), self.fixture() as root, tempfile.TemporaryDirectory() as t:
                p = root / "projects" / SLUG
                edit_manifest(p, "speed-bar", **change)
                rep = check_figures.check(p, config.load(p), pathlib.Path(t, "out"))
                self.assertIn("FIG-MANIFEST", {c["id"] for c in check_figures.blocking(rep)})

    @unittest.skipUnless(CHEM and BROWSER, "needs rdkit and Edge/Chrome")
    def test_invalid_smiles_fails_the_figure_check(self):
        """TICKET STEP 9 exit: one invalid SMILES must fail (a blocking ID, so `run build` fails too)."""
        with self.fixture() as root, tempfile.TemporaryDirectory() as t:
            p = root / "projects" / SLUG
            spec = p / "figures/src/caffeine.json"
            spec.write_text(json.dumps(dict(load(spec), smiles="C1CC(")), encoding="utf-8")
            rep = self.render_check(p, pathlib.Path(t, "out"))   # the invalid figure is not rendered; the rest are
            self.assertEqual({c["id"] for c in check_figures.blocking(rep)}, {"CHEM-SMILES-INVALID"})
            self.assertEqual(check_figures.ids_of(rep, "CHEM-SMILES-INVALID"), ["caffeine"])

    @unittest.skipUnless(CHEM and BROWSER, "needs rdkit and Edge/Chrome")
    def test_offline_chemistry_is_unverified_not_blocking(self):
        with self.fixture() as root, tempfile.TemporaryDirectory() as t:
            rep = self.render_check(root / "projects" / SLUG, pathlib.Path(t, "out"))
            self.assertEqual(check_figures.blocking(rep), [])
            self.assertEqual(check_figures.ids_of(rep, "CHEM-UNVERIFIED"), ["aspirin", "caffeine"])   # never `pass`

    def test_numbering_by_first_reference(self):
        with self.fixture() as root:
            cfg = config.load(root / "projects" / SLUG)
            man = load(root / "projects" / SLUG / "figures/figures.json")["figures"]
            ch02 = [f["id"] for f in man if f["chapter_id"] == "ch02"]
            self.assertEqual(ch02[0], "speed-line")   # first in the manifest ...
            nums = {k: label for k, (_, label) in figures.numbering(cfg).items()}
            self.assertEqual(nums["friction-diagram"], "Figure 2.1")   # ... but placed second in the chapter
            self.assertEqual(nums["speed-line"], "Figure 2.2")
            self.assertEqual((nums["rolling-ball"], nums["speed-bar"]), ("Figure 1.1", "Figure 1.2"))

    def test_needs_author_asset_blocks_build(self):
        with self.fixture() as root:
            p = root / "projects" / SLUG
            edit_manifest(p, "rolling-ball", kind="author-asset", status="needs-author-asset")
            finish_rework(root)
            r = run_cli(root, *P, "run", "build")
            self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
            self.assertIn("FIG-AUTHOR-ASSET", r.stderr)
            self.assertEqual(load(p / "state.json")["receipts"]["build"]["status"], "failed")

    def test_no_manifest_blocks_a_harness_book(self):
        """figures.json is a required rework output, so a harness book cannot reach build without one; only a
        history-imported rework may build in legacy mode (ruling R1)."""
        with self.fixture() as root:
            (root / "projects" / SLUG / "figures/figures.json").unlink()
            with self.assertRaises(AssertionError) as e:
                finish_rework(root)
            self.assertIn("figures/figures.json", str(e.exception))

    @unittest.skipUnless(BROWSER and CHEM, "needs Edge/Chrome and rdkit (the fixture has chemistry figures)")
    def test_png_300dpi_at_text_width(self):
        with self.fixture() as root, tempfile.TemporaryDirectory() as t:
            p = root / "projects" / SLUG
            out = pathlib.Path(t, "out")
            cfg = config.load(p)
            render.render_all(p, cfg, out)
            want = round(cfg["theme"]["layout"]["text_width"] / 2.54 * 300)
            from PIL import Image
            for name in ("speed-bar.png", "speed-line.png", "friction-diagram.png"):
                with Image.open(out / name) as im:
                    self.assertEqual(tuple(round(x) for x in im.info["dpi"]), (300, 300), name)   # ruling R2
                    self.assertEqual(im.size[0], want, name)

    @unittest.skipUnless(BROWSER and WORD and CHEM, "needs Edge/Chrome, Word COM and rdkit")
    def test_build_with_figures(self):
        """Full `run build`: renders in figures/out, alt text and computed captions in the DOCX, verify exit 0."""
        with self.fixture() as root:
            p = root / "projects" / SLUG
            finish_rework(root)
            with mock.patch.dict(os.environ, {check_figures.OFFLINE_ENV: "1"}):   # PubChem is never called in tests
                r = run_cli(root, *P, "run", "build")
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            rec = load(p / "state.json")["receipts"]["build"]
            self.assertEqual(rec["figures"], "manifest")
            self.assertIn("figures/out/speed-bar.png", rec["outputs"])
            self.assertIn("figures/figures.json", rec["inputs"])
            report = load(p / "build/build-report.json")
            self.assertEqual(report["docx"]["images"], 7)
            self.assertEqual(report["chem_unverified"], ["aspirin", "caffeine"])   # offline: listed for the audit gate
            self.assertIn("rdkit", report["figure_versions"])
            import zipfile
            with zipfile.ZipFile(p / "build/motion-and-figures.docx") as z:
                doc = z.read("word/document.xml").decode("utf-8")
            self.assertIn('descr="A box on a floor with a push arrow', doc)
            self.assertIn("Figure 2.1", doc)
            v = run_cli(root, *P, "verify", "--through", "build")
            self.assertEqual(v.returncode, 0, v.stderr)


def _small_png(path):
    from PIL import Image
    from harness.figures import png
    png.write_canonical(Image.new("RGB", (400, 220), (200, 200, 200)), path, 72)


if __name__ == "__main__":
    unittest.main()
