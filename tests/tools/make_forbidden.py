"""Test-side: write tests/fixtures/leak/forbidden.txt from the medical project's config plus the fixed clinical list
(core §9.5). Kept under tests/ so the list never sits inside the scanned code.

Usage: python tests/tools/make_forbidden.py [--check]   (--check: exit 1 if the committed file is out of date)
"""
import json, pathlib, sys

REPO = pathlib.Path(__file__).resolve().parents[2]
PROJECT = REPO / "projects" / "ai-in-medicine"
LEAK = REPO / "tests" / "fixtures" / "leak"
HONORIFICS = {"assistant", "prof", "prof.", "dr", "dr.", "professor"}


def load(rel):
    return json.loads((PROJECT / rel).read_text(encoding="utf-8"))


def terms():
    brief, template = load("brief.json"), load("template.json")
    out = [brief["identity"]["title"], brief["identity"]["subtitle"]]
    for a in brief["identity"]["authors"]:
        out.append(a["name"])
        out += [w for w in a["name"].split() if w.lower() not in HONORIFICS and len(w) > 2]
    out += brief["audience"]["programmes"]                                  # profession labels
    out += [i["label"] for i in template["perspectives"]["items"]]          # perspective labels
    out += [c["label"] for c in template["callouts"]]                       # callout labels
    for line in (LEAK / "clinical.txt").read_text(encoding="utf-8").splitlines():
        if line.strip() and not line.startswith("#"):
            out.append(line.strip())
    seen, uniq = set(), []
    for t in out:
        if t and t.lower() not in seen:
            seen.add(t.lower())
            uniq.append(t)
    return uniq


def main():
    text = "\n".join(terms()) + "\n"
    target = LEAK / "forbidden.txt"
    if "--check" in sys.argv:
        ok = target.exists() and target.read_text(encoding="utf-8") == text
        print("forbidden.txt up to date" if ok else "forbidden.txt is out of date: run tests/tools/make_forbidden.py")
        return 0 if ok else 1
    target.write_text(text, encoding="utf-8", newline="\n")
    print(f"wrote {target.relative_to(REPO).as_posix()}: {text.count(chr(10))} terms")
    return 0


if __name__ == "__main__":
    sys.exit(main())
