"""Check that every DOI in a chapter's References exists on CrossRef and matches the cited title.

Usage: python projects/ai-in-medicine/rework/tools/verify_refs.py projects/ai-in-medicine/rework/ch04-....md [more.md ...]
Output per reference: OK n | NOT FOUND n | TITLE MISMATCH n | NO DOI n | ERROR n.
Exit 1 on NOT FOUND, TITLE MISMATCH or ERROR. NO DOI is allowed only for laws/guidance with a URL.
If api.crossref.org is unreachable from the shell, check DOIs with the WebFetch tool instead.
"""
import json
import pathlib
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

WORD = re.compile(r"[a-z0-9]+")


def references(text):
    i = text.find("\n## References")
    block = text[i:] if i >= 0 else ""
    return re.findall(r"^(\d+)\. (.+)$", block, re.M)


def crossref_title(doi):
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="/")
    req = urllib.request.Request(url, headers={"User-Agent": "rework-verify/1.0"})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                msg = json.load(r)["message"]
            break
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            if e.code != 429 or attempt == 4:
                raise
            time.sleep(3 * (attempt + 1))  # CrossRef rate limit
    time.sleep(0.5)
    return " ".join(msg.get("title") or [""])


def title_matches(ref_line, title):
    # ponytail: word-overlap heuristic on the first 6 title words; enough to catch wrong-DOI pairings
    want = [w for w in WORD.findall(title.lower()) if len(w) > 2][:6]
    have = set(WORD.findall(ref_line.lower()))
    return bool(want) and sum(w in have for w in want) / len(want) >= 0.6


def check(path):
    bad = 0
    for n, line in references(pathlib.Path(path).read_text(encoding="utf-8")):
        m = re.search(r"DOI:\s*(10\.\S+?)\.?\s*$", line) or re.search(r"doi\.org/(10\.\S+?)\.?\s*$", line)
        if not m:
            print(f"NO DOI {n}")
            continue
        try:
            title = crossref_title(m.group(1))
        except Exception as e:  # network or parse failure
            print(f"ERROR {n}: {e}")
            bad += 1
            continue
        if title is None:
            print(f"NOT FOUND {n}: {m.group(1)}")
            bad += 1
        elif not title_matches(line, title):
            print(f"TITLE MISMATCH {n}: CrossRef says '{title[:90]}'")
            bad += 1
        else:
            print(f"OK {n}")
    return bad


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    bad = sum(check(p) for p in sys.argv[1:])
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
