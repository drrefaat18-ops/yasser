"""Assemble rework chapters into one book file at the repo root.

Usage: python rework/tools/assemble.py
Writes AI_in_Health_Care_Interprofessional.md and exits 1 if any image path in it is missing.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
REWORK = ROOT / "rework"
OUT = ROOT / "AI_in_Health_Care_Interprofessional.md"


def anchor(title):
    # GitHub-style heading anchor
    a = re.sub(r"[^\w\s-]", "", title.lower()).strip()
    return re.sub(r"\s", "-", a)


def fix_paths(text):
    text = text.replace("](../images/", "](images/")
    return text.replace("](figures/", "](rework/figures/")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    front = fix_paths((REWORK / "00-front-matter.md").read_text(encoding="utf-8"))
    parts = [fix_paths(p.read_text(encoding="utf-8")) for p in sorted(REWORK.glob("ch*.md"))]
    parts.append((REWORK / "glossary.md").read_text(encoding="utf-8"))
    titles = [re.search(r"^# (.+)$", p, re.M).group(1) for p in parts]
    toc = "## Contents\n\n" + "\n".join(f"- [{t}](#{anchor(t)})" for t in titles) + "\n"
    head, rest = front.split("\n## How to Use This Book", 1)
    book = head.rstrip() + "\n\n" + toc + "\n## How to Use This Book" + rest
    book += "".join("\n\n---\n\n" + p.strip() + "\n" for p in parts)
    OUT.write_text(book, encoding="utf-8")
    missing = [m for m in re.findall(r"\]\(((?:images|rework/figures)/[^)]+)\)", book) if not (ROOT / m).exists()]
    for m in missing:
        print("missing image:", m)
    print(f"wrote {OUT.name}: {len(book.split())} words, {len(titles)} sections")
    sys.exit(1 if missing else 0)


if __name__ == "__main__":
    main()
