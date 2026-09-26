# tests/test_golden.py
import io, json, pathlib, tempfile, unittest, zipfile
from harness.tools import capture_golden, compare_golden

def docx_bytes(parts):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        for name, data in parts.items():
            z.writestr(name, data)
    return buf.getvalue()

W = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
DOC = f'<w:document {W}><w:body><w:tbl><w:tr><w:tc><w:p><w:r><w:t>cell</w:t></w:r></w:p></w:tc></w:tr></w:tbl>' \
      f'<w:p w:rsidR="00AB"><w:r><w:t>body</w:t></w:r></w:p></w:body></w:document>'
BASE = {"word/document.xml": DOC, "word/header1.xml": f'<w:hdr {W}><w:p><w:r><w:t>head</w:t></w:r></w:p></w:hdr>',
        "word/styles.xml": f'<w:styles {W}><w:style w:styleId="Normal"/></w:styles>', "word/media/image1.png": b"\x89PNG-A"}


class DocxHashTest(unittest.TestCase):
    def _hash(self, parts):
        with tempfile.TemporaryDirectory() as t:
            p = pathlib.Path(t, "x.docx"); p.write_bytes(docx_bytes(parts))
            return capture_golden.docx_parts(p)

    def test_rsid_is_volatile(self):
        other = dict(BASE, **{"word/document.xml": DOC.replace('w:rsidR="00AB"', 'w:rsidR="00CD"')})
        self.assertEqual(self._hash(BASE), self._hash(other))

    def test_per_save_ids_are_volatile(self):
        """Word writes these random IDs on every save (seen in two builds of the same sources)."""
        w14 = 'xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml"'
        w15 = 'xmlns:w15="http://schemas.microsoft.com/office/word/2012/wordml"'
        cid = 'xmlns:w16cid="http://schemas.microsoft.com/office/word/2016/wordml/cid"'
        rr = 'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'

        def parts(i):
            return dict(BASE, **{
                "word/document.xml": DOC.replace("<w:p w:rsidR", f'<w:p {w14} w14:paraId="0{i}" w14:textId="1{i}" w:rsidR'),
                "word/settings.xml": f'<w:settings {W} {w14} {w15}><w:zoom w:percent="{i}0"/><w14:docId w14:val="{i}"/>'
                                     f'<w15:docId w15:val="{i}"/></w:settings>',
                "word/numbering.xml": f'<w:numbering {W} {cid}><w:num w16cid:durableId="{i}" w:numId="1"/></w:numbering>',
                "word/styles.xml": f'<w:styles {W}><w:style w:styleId="Normal"><w:rsid w:val="{i}"/></w:style></w:styles>',
                "word/fontTable.xml": f'<w:fonts {W} {rr}><w:font w:name="X"><w:embedRegular r:id="rId1" w:fontKey="{{{i}}}"/></w:font></w:fonts>'})
        self.assertEqual(self._hash(parts(1)), self._hash(parts(2)))
        changed = parts(1)
        changed["word/fontTable.xml"] = changed["word/fontTable.xml"].replace('w:name="X"', 'w:name="Y"')
        self.assertNotEqual(self._hash(parts(1)), self._hash(changed))

    def test_embedded_font_hash_ignores_key_but_sees_payload(self):
        rr = 'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'
        rels = ('<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                '<Relationship Id="rId1" Type="x" Target="fonts/font1.odttf"/></Relationships>')

        def parts(guid, payload):
            key = bytes.fromhex(guid.replace("-", ""))[::-1]
            data = bytearray(payload)
            for i in range(32):
                data[i] ^= key[i % 16]
            return dict(BASE, **{
                "word/fontTable.xml": f'<w:fonts {W} {rr}><w:font w:name="X"><w:embedRegular r:id="rId1" w:fontKey="{{{guid}}}"/></w:font></w:fonts>',
                "word/_rels/fontTable.xml.rels": rels, "word/fonts/font1.odttf": bytes(data)})
        font = bytes(range(64)) * 2
        g1, g2 = "0A1B2C3D-4E5F-6071-8293-A4B5C6D7E8F9", "11111111-2222-3333-4444-555555555555"
        self.assertEqual(self._hash(parts(g1, font)), self._hash(parts(g2, font)))
        # Word rewrites font bytes on every save (head checksum, timestamps), so a font is identified by its
        # declared name, embed slot and de-obfuscated length; same-length glyph edits are a known ceiling.
        self.assertNotEqual(self._hash(parts(g1, font)), self._hash(parts(g1, font + b"\x00")))
        renamed = parts(g1, font)
        renamed["word/fontTable.xml"] = renamed["word/fontTable.xml"].replace('w:name="X"', 'w:name="Y"')
        self.assertNotEqual(self._hash(parts(g1, font))["word/fonts/font1.odttf"],
                            self._hash(renamed)["word/fonts/font1.odttf"])

    def test_toc_result_and_toc_bookmarks_are_volatile(self):
        def doc(page, mark):
            return (f'<w:document {W}><w:body><w:p><w:r><w:fldChar w:fldCharType="begin"/></w:r>'
                    f'<w:r><w:instrText> TOC \\o "1-2"</w:instrText></w:r><w:r><w:fldChar w:fldCharType="separate"/></w:r>'
                    f'<w:hyperlink w:anchor="{mark}"><w:r><w:t>Intro {page}</w:t></w:r><w:r><w:rPr><w:b/></w:rPr></w:r></w:hyperlink></w:p>'
                    f'<w:p><w:r><w:fldChar w:fldCharType="end"/></w:r></w:p>'
                    f'<w:p><w:bookmarkStart w:id="7" w:name="{mark}"/><w:r><w:t>Intro</w:t></w:r><w:bookmarkEnd w:id="7"/></w:p>'
                    f'</w:body></w:document>')
        a = self._hash(dict(BASE, **{"word/document.xml": doc(3, "_Toc111")}))
        b = self._hash(dict(BASE, **{"word/document.xml": doc(4, "_Toc222")}))
        self.assertEqual(a, b)
        c = self._hash(dict(BASE, **{"word/document.xml": doc(3, "_Toc111").replace("<w:t>Intro</w:t>", "<w:t>Other</w:t>")}))
        self.assertNotEqual(a, c)

    def test_toc_result_sharing_delimiter_runs_is_volatile(self):
        """Result text in the same run as the separate or end fldChar, and a nested PAGEREF field."""
        def doc(page):
            return (f'<w:document {W}><w:body><w:p><w:r><w:fldChar w:fldCharType="begin"/>'
                    f'<w:instrText> TOC \\\\o "1-2" </w:instrText><w:fldChar w:fldCharType="separate"/><w:t>A {page}</w:t></w:r>'
                    f'<w:r><w:fldChar w:fldCharType="begin"/><w:instrText> PAGEREF _Toc1 </w:instrText>'
                    f'<w:fldChar w:fldCharType="separate"/><w:t>{page}</w:t><w:fldChar w:fldCharType="end"/></w:r>'
                    f'<w:r><w:t>B {page}</w:t><w:fldChar w:fldCharType="end"/></w:r>'
                    f'<w:r><w:t>after</w:t></w:r></w:p></w:body></w:document>')
        self.assertEqual(self._hash(dict(BASE, **{"word/document.xml": doc(3)})),
                         self._hash(dict(BASE, **{"word/document.xml": doc(4)})))
        moved = doc(3).replace("<w:t>after</w:t>", "<w:t>later</w:t>")
        self.assertNotEqual(self._hash(dict(BASE, **{"word/document.xml": doc(3)})),
                            self._hash(dict(BASE, **{"word/document.xml": moved})))

    def test_content_changes_are_detected(self):
        base = self._hash(BASE)
        for part, old, new in [("word/document.xml", "cell", "CELL"), ("word/header1.xml", "head", "HEAD"),
                               ("word/styles.xml", "Normal", "Plain"), ("word/media/image1.png", b"-A", b"-B")]:
            with self.subTest(part):
                self.assertNotEqual(self._hash(dict(BASE, **{part: BASE[part].replace(old, new)})), base)


class CompareTest(unittest.TestCase):
    def test_allowed_and_disallowed(self):
        d = compare_golden.diff({"project": "x", "words": {"total": 1}}, {"project": "y", "words": {"total": 2}},
                                [{"pointer_glob": "/project", "reason": "rename"}])
        self.assertEqual({x["pointer"]: x["allowed"] for x in d["diffs"]}, {"/project": True, "/words/total": False})

    def test_bad_allowlist_is_a_named_error(self):
        import subprocess, sys
        with tempfile.TemporaryDirectory() as tmp:
            d = pathlib.Path(tmp)
            (d / "a.json").write_text('{"x": 1}'); (d / "b.json").write_text('{"x": 2}')
            for bad in ['{"reserved": []}', '[{"pointer": "/x"}]', '"x"']:
                with self.subTest(bad=bad):
                    (d / "allow.json").write_text(bad)
                    r = subprocess.run([sys.executable, "harness/tools/compare_golden.py", str(d / "a.json"), str(d / "b.json"),
                                        "--allow", str(d / "allow.json")], capture_output=True, text=True)
                    self.assertEqual(r.returncode, 2)
                    self.assertIn("ERROR ALLOWLIST", r.stderr)

    def test_provenance_ignored(self):
        self.assertEqual(compare_golden.diff({"provenance": {"tool_sha": "a"}}, {"provenance": {"tool_sha": "b"}}, [])["diffs"], [])

    def test_checks_from_projection(self):
        a = {"checks": [{"id": "CIT-MISSING", "target": "ch01", "status": "pass"}]}
        b = {"checks": [{"id": "CIT-MISSING", "target": "ch01", "status": "pass"},
                        {"id": "READ-NOPROSE", "target": "ch01", "status": "pass"}]}
        self.assertEqual(compare_golden.diff(a, b, [], checks_from=a)["diffs"], [])
        b["checks"][1]["status"] = "fail"
        self.assertTrue(compare_golden.diff(a, b, [], checks_from=a)["diffs"])


class CaptureTest(unittest.TestCase):
    LAYOUT = json.loads((pathlib.Path(__file__).parent / "fixtures/ai-in-medicine/layout-legacy.json").read_text(encoding="utf-8"))

    def test_layout_paths_must_stay_inside_project(self):
        with tempfile.TemporaryDirectory() as t:
            root = pathlib.Path(t)
            self.assertEqual(capture_golden.layout_problems(root, self.LAYOUT), [])
            for key, bad in [("legacy_tools", "../outside"), ("chapters_dir", "/abs"), ("chapters_dir", "C:/abs"),
                             ("images", ["images", "../x"]), ("deliverables", {"md": "../a.md", "docx": "b", "pdf": "c"}),
                             ("chapter_glob", "../*.md"), ("chapter_glob", "sub/*.md")]:
                with self.subTest(key=key, bad=bad):
                    probs = capture_golden.layout_problems(root, dict(self.LAYOUT, **{key: bad}))
                    self.assertTrue(any(key in p for p in probs), probs)
                    with self.assertRaises(capture_golden.LayoutError):
                        capture_golden.capture(root, dict(self.LAYOUT, **{key: bad}), slug="x")

    def test_capture_refuses_network_error(self):
        with self.assertRaises(capture_golden.NetworkError):
            capture_golden.parse_refs_output("ch01", "OK 1\nERROR 2: timed out\n")

    def test_parse_refs_statuses(self):
        rows = capture_golden.parse_refs_output("ch01", "OK 1\nNO DOI 2\nNOT FOUND 3: 10.1/x\nTITLE MISMATCH 4: CrossRef says 'y'\n")
        self.assertEqual([r["status"] for r in rows], ["ok", "no_doi", "not_found", "title_mismatch"])
        with self.assertRaises(capture_golden.Unclassified):
            capture_golden.parse_refs_output("ch01", "garbage line\n")

    def test_dumps_stable(self):
        g = {"b": 1, "a": {"d": 2, "c": [3]}}
        self.assertEqual(capture_golden.dumps(g), capture_golden.dumps(json.loads(capture_golden.dumps(g))))


class HarnessModeTest(unittest.TestCase):
    """Plan Task 8.1: capture without --layout derives the layout from config and reads the harness checker."""
    FIX = pathlib.Path(__file__).parent / "fixtures/ai-in-medicine"

    def test_harness_mode_layout_from_config(self):
        from tests.helpers import REPO
        med = REPO / "projects/ai-in-medicine"
        want = json.loads((self.FIX / "layout-projects.json").read_text(encoding="utf-8"))
        self.assertEqual(capture_golden.derive_layout(med, "deliverables"), want)
        build = capture_golden.derive_layout(med, "build")
        self.assertEqual({k: v for k, v in build.items() if k not in ("deliverables", "src_copy")},
                         {k: v for k, v in want.items() if k not in ("deliverables", "src_copy")})
        self.assertEqual(build["deliverables"]["docx"], "build/AI_in_Health_Care_Interprofessional.docx")
        with self.assertRaises(capture_golden.LayoutError):
            capture_golden.derive_layout(med, "elsewhere")

    def test_checker_matches_step6(self):
        """Every STEP 6 (id, target) check is identical and every new ID passes (N7). verify_refs needs the network and
        is compared by the STEP 8 evidence command (Tasks 8.2-8.3), so this capture skips it."""
        from tests.helpers import temp_repo
        step6 = json.loads((self.FIX / "golden-step6.json").read_text(encoding="utf-8"))
        with temp_repo(project_from="projects/ai-in-medicine", stamp=True) as root:
            g = capture_golden.capture_harness(root / "projects/ai-in-medicine", slug="ai-in-medicine",
                                               run_refs=False, docx_from="deliverables")
        d = compare_golden.diff(step6, g, [], checks_from=step6)["diffs"]
        self.assertEqual([x["pointer"] for x in d], ["/verify_refs"])   # None here: not captured
        new = {c["id"] for c in g["checks"]} - {c["id"] for c in step6["checks"]}
        self.assertEqual(new, {"TPL-CALLOUT-COUNT", "BUDGET-FRONT", "ASSET-MISSING", "ASSET-OUTSIDE-ROOT"})

    def test_capture_refuses_a_gated_refusal(self):
        from tests.helpers import temp_repo
        with temp_repo(project_from="projects/ai-in-medicine", stamp=True) as root:
            p = root / "projects/ai-in-medicine"
            (p / "brief.json").write_text("{}", encoding="utf-8")
            with self.assertRaises(capture_golden.GateRefused):
                capture_golden.harness_report(p)


if __name__ == "__main__":
    unittest.main()
