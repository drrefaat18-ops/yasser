"""Locale-parameterised text primitives (core §11 EXT-LOC-1). Every function takes the profile; no global language."""
import re, unicodedata

DIGITS = {"western": "0123456789", "arabic-indic": "٠١٢٣٤٥٦٧٨٩", "eastern-arabic-indic": "۰۱۲۳۴۵۶۷۸۹"}
_VALUE = {ch: i for s in DIGITS.values() for i, ch in enumerate(s)}


def _word(profile):
    return re.compile(profile["tokenizer"]["pattern"])


def tokens(text, profile):
    return _word(profile).findall(text)


def words(text, profile):
    return len(tokens(text, profile))


def sentences(text, profile):
    """Split after a terminator followed by whitespace; keep pieces that hold at least one token."""
    marks = "".join(re.escape(t) for t in profile["sentence_terminators"])
    word = _word(profile)
    return [s for s in re.split(rf"(?<=[{marks}])\s+", text) if word.search(s)]


def normalise(text, profile, purpose):
    steps = profile["normalisation"][purpose]
    for step in steps:
        if step in ("NFC", "NFD", "NFKC", "NFKD"):
            text = unicodedata.normalize(step, text)
        elif step == "casefold":
            text = text.casefold()
        else:
            raise ValueError(f"unknown normalisation step {step!r}")
    return text


def digits_value(s):
    """Integer value of a digit string in any supported system."""
    if not s or any(ch not in _VALUE for ch in s):
        raise ValueError(f"not a digit string: {s!r}")
    n = 0
    for ch in s:
        n = n * 10 + _VALUE[ch]
    return n


def mixed_digits(s):
    """True when one number mixes digits from more than one system."""
    return len({name for ch in s for name, ds in DIGITS.items() if ch in ds}) > 1
