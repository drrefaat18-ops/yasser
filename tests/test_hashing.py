import pathlib, tempfile, unittest
from harness import hashing

class HashingTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.tmp.cleanup()

    def _write(self, name, data):
        p = pathlib.Path(self.tmp.name) / name
        p.write_bytes(data)
        return p

    def test_json_canonical_ignores_key_order_and_spacing(self):
        a = self._write("a.json", b'{"b": 1, "a": [1, 2]}')
        b = self._write("b.json", b'{\n  "a": [1,2],\n  "b": 1\n}')
        self.assertEqual(hashing.hash_file(a), hashing.hash_file(b))

    def test_hash_crlf_equal_bom_differs(self):
        lf = self._write("lf.md", "# T\nx\n".encode())
        crlf = self._write("crlf.md", "# T\r\nx\r\n".encode())
        bom = self._write("bom.md", "﻿# T\nx\n".encode())
        self.assertEqual(hashing.hash_file(lf), hashing.hash_file(crlf))
        self.assertNotEqual(hashing.hash_file(lf), hashing.hash_file(bom))

    def test_binary_raw(self):
        a = self._write("a.png", b"\x89PNG\r\n")
        self.assertEqual(hashing.hash_file(a), hashing.hash_bytes(b"\x89PNG\r\n"))


if __name__ == "__main__":
    unittest.main()
