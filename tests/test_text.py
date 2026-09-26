# tests/test_text.py
"""harness/text.py with the English profile reproduces the legacy tokenizer and sentence splitter (INV-11)."""
import importlib.util, re, unittest
from harness import locales, text
from tests.helpers import REPO

EN = locales.load_profile("en")
CHAPTERS = sorted((REPO / "projects/ai-in-medicine/rework").glob("ch*.md"))


def legacy():
    spec = importlib.util.spec_from_file_location("legacy_cb", REPO / "projects/ai-in-medicine/rework/tools/check_book.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TextTest(unittest.TestCase):
    def test_words_equal_legacy_on_every_medical_chapter(self):
        cb = legacy()
        self.assertEqual(len(CHAPTERS), 11)
        for p in CHAPTERS:
            t = p.read_text(encoding="utf-8")
            self.assertEqual(text.words(t, EN), len(cb.WORD.findall(t)), p.name)

    def test_sentences_equal_legacy_on_every_medical_chapter(self):
        cb = legacy()
        for p in CHAPTERS:
            for line in cb.clean_prose_lines(p.read_text(encoding="utf-8")):
                want = [s for s in re.split(r"(?<=[.!?])\s+", line) if cb.WORD.search(s)]
                self.assertEqual(text.sentences(line, EN), want, p.name)

    def test_profile_is_a_parameter(self):
        other = dict(EN, sentence_terminators=[";"], tokenizer={"kind": "x", "pattern": r"[a-z]+"})
        self.assertEqual(text.sentences("one. two; three", other), ["one. two;", "three"])
        self.assertEqual(text.words("AB cd", other), 1)
        self.assertEqual(text.tokens("AB cd", other), ["cd"])

    def test_normalise_purposes(self):
        s = "Café STRASSE"
        self.assertEqual(text.normalise(s, EN, "compare"), "café strasse")
        self.assertEqual(text.normalise(s, EN, "count"), "Café STRASSE")
        with self.assertRaises(ValueError):
            text.normalise(s, dict(EN, normalisation={"compare": ["bogus"]}), "compare")

    def test_digits(self):
        self.assertEqual(text.digits_value("2026"), 2026)
        self.assertEqual(text.digits_value("١٢"), 12)
        self.assertTrue(text.mixed_digits("1٢"))
        self.assertFalse(text.mixed_digits("12"))
        with self.assertRaises(ValueError):
            text.digits_value("1a")


if __name__ == "__main__":
    unittest.main()
