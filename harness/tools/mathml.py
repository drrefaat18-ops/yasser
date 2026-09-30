"""TeX math -> OMML for the DOCX writer, and -> MathML for the HTML engine (plan Task 9c.2).

A book that sets `template.math.enabled` may write math between `$...$` inline and `$$...$$` on a line
of its own. The chapter keeps the TeX; only the writers convert it, so the source stays diffable and
the checker keeps reading it as text.

The path is TeX -> MathML (`latex2mathml`) -> OMML (`MML2OMML.XSL`, which ships with Word). Word owns
the second step, so an equation rendered here is the same object Word would have produced from its own
equation editor: selectable, searchable, and restyled with the document's fonts rather than pasted as
a picture. `omml_available()` says whether the stylesheet was found, so a caller can fail with one
clear message instead of a stack trace per equation.
"""
import functools, os, pathlib, re

# Word ships the stylesheet with every installation; the path differs by Office generation, not by locale.
# The install roots come from the environment, so shared code holds no absolute path (Rule 8).
_OFFICE_SUBDIRS = [("root", "Office16"), ("Office16",), ("Office15",)]
XSL_CANDIDATES = [str(pathlib.Path(root, "Microsoft Office", *sub, "MML2OMML.XSL"))
                  for sub in _OFFICE_SUBDIRS
                  for root in (os.environ.get("ProgramFiles"), os.environ.get("ProgramFiles(x86)")) if root]
INLINE_MATH = re.compile(r"(?<!\\)\$(?!\s)((?:[^$\\]|\\.)+?)(?<!\s)(?<!\\)\$")
DISPLAY_MATH = re.compile(r"^\$\$\s*(.+?)\s*\$\$$", re.S)


class MathError(Exception):
    """A TeX fragment the pipeline cannot convert. Always names the fragment."""


def xsl_path():
    for p in XSL_CANDIDATES:
        if pathlib.Path(p).is_file():
            return pathlib.Path(p)
    return None


def omml_available():
    return xsl_path() is not None


@functools.lru_cache(maxsize=1)
def _transform():
    from lxml import etree
    p = xsl_path()
    if p is None:
        raise MathError("MML2OMML.XSL not found: Word's MathML stylesheet is needed to write equations")
    return etree.XSLT(etree.parse(str(p)))


@functools.lru_cache(maxsize=512)
def mathml(tex, display=False):
    """TeX -> a MathML string. Cached: a book repeats the same symbols many times."""
    try:
        import latex2mathml.converter as conv
    except ImportError as e:                                      # noqa: BLE001 - reported with the cause
        raise MathError(f"latex2mathml is not installed: {e}") from e
    try:
        return conv.convert(tex, display="block" if display else "inline")
    except Exception as e:                                        # noqa: BLE001 - any parse failure names the TeX
        raise MathError(f"cannot convert TeX {tex!r}: {type(e).__name__}: {e}") from e


@functools.lru_cache(maxsize=512)
def omml_xml(tex, display=False):
    """TeX -> an OMML fragment as a string, ready to be parsed into a docx paragraph."""
    from lxml import etree
    try:
        tree = etree.fromstring(mathml(tex, display).encode("utf-8"))
    except etree.XMLSyntaxError as e:
        raise MathError(f"TeX {tex!r} produced MathML that will not parse: {e}") from e
    return etree.tostring(_transform()(tree), encoding="unicode")


def split_inline(text):
    """-> [(is_math, fragment)] for one line, splitting on `$...$`. `\\$` is a literal dollar.

    A lone `$` (a price) leaves the text alone, because the pattern needs a closing `$` with no space
    beside either delimiter."""
    out, last = [], 0
    for m in INLINE_MATH.finditer(text):
        if m.start() > last:
            out.append((False, text[last:m.start()]))
        out.append((True, m.group(1)))
        last = m.end()
    if last < len(text):
        out.append((False, text[last:]))
    return [(is_math, frag.replace("\\$", "$") if not is_math else frag) for is_math, frag in out if frag]


def display(text):
    """The TeX of a paragraph that is entirely `$$...$$`, else None."""
    m = DISPLAY_MATH.match(text.strip())
    return m.group(1) if m else None


def strip(text):
    """Math delimiters removed, leaving the TeX as plain text: for bookmarks, running heads and the TOC."""
    d = display(text)
    if d is not None:
        return d
    return "".join(frag for _, frag in split_inline(text))
