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
                "word/fontTable.xml": f'<w:fonts {W} {rr}><w:font w:name="X"><w:embedRegular r:id="rId1" w:fontKey="{{{i}}}"/></w:font></w:fonts>',
                "word/fonts/font1.odttf": f"obfuscated-{i}".encode()})
        self.assertEqual(self._hash(parts(1)), self._hash(parts(2)))
        changed = parts(1)
        changed["word/fontTable.xml"] = changed["word/fontTable.xml"].replace('w:name="X"', 'w:name="Y"')
        self.assertNotEqual(self._hash(parts(1)), self._hash(changed))

    def test_toc_result_and_toc_bookmarks_are_volatile(self):
        def doc(page, mark):
            return (f'<w:document {W}><w:body><w:p><w:r><w:fldChar w:fldCharType="begin"/></w:r>'
                    f'<w:r><w:instrText> TOC \\o "1-2"</w:instrText></w:r><w:r><w:fldChar w:fldCharType="separate"/></w:r>'
                    f'<w:hyperlink w:anchor="{mark}"><w:r><w:t>Intro {page}</w:t></w:r></w:hyperlink></w:p>'
                    f'<w:p><w:r><w:fldChar w:fldCharType="end"/></w:r></w:p>'
                    f'<w:p><w:bookmarkStart w:id="7" w:name="{mark}"/><w:r><w:t>Intro</w:t></w:r><w:bookmarkEnd w:id="7"/></w:p>'
                    f'</w:body></w:document>')
        a = self._hash(dict(BASE, **{"word/document.xml": doc(3, "_Toc111")}))
        b = self._hash(dict(BASE, **{"word/document.xml": doc(4, "_Toc222")}))
        self.assertEqual(a, b)
        c = self._hash(dict(BASE, **{"word/document.xml": doc(3, "_Toc111").replace("<w:t>Intro</w:t>", "<w:t>Other</w:t>")}))
        self.assertNotEqual(a, c)

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


if __name__ == "__main__":
    unittest.main()
