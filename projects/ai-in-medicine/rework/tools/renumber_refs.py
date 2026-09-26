"""Drop uncited references and renumber citations by first appearance.

Usage: python projects/ai-in-medicine/rework/tools/renumber_refs.py projects/ai-in-medicine/rework/chNN-*.md [...]
"""
import re
import sys

GROUP = re.compile(r"\[(\d+(?:\s*[,–-]\s*\d+)*)\]")


def expand(grp):
    out = []
    for part in re.split(r"\s*,\s*", grp):
        r = re.split(r"\s*[–-]\s*", part)
        out += range(int(r[0]), int(r[-1]) + 1)
    return out


def compress(nums):
    nums, out, i = sorted(set(nums)), [], 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1:
            j += 1
        out.append(f"{nums[i]}–{nums[j]}" if j - i >= 2 else ", ".join(map(str, nums[i:j + 1])))
        i = j + 1
    return ", ".join(out)


def renumber(text):
    body, sep, refs = text.partition("\n## References")
    if not sep:
        return text
    entries = dict(re.findall(r"^(\d+)\. (.+)$", refs, re.M))
    order = []
    for g in GROUP.findall(body):
        for n in expand(g):
            if n not in order:
                order.append(n)
    new = {old: k + 1 for k, old in enumerate(order)}
    missing = [n for n in order if str(n) not in entries]
    if missing:
        raise SystemExit(f"cited but not in list: {missing}")
    body = GROUP.sub(lambda m: "[" + compress(new[n] for n in expand(m.group(1))) + "]", body)
    lst = "\n".join(f"{new[o]}. {entries[str(o)]}" for o in order)
    return body + sep + "\n" + lst + "\n"


def _selftest():
    t = "A [3]. B [1, 3]. C [5–7].\n\n## References\n1. one\n2. two\n3. three\n5. five\n6. six\n7. seven\n"
    r = renumber(t)
    assert r.startswith("A [1]. B [1, 2]. C [3–5]."), r
    assert "two" not in r and r.rstrip().endswith("5. seven"), r


if __name__ == "__main__":
    _selftest()
    for path in sys.argv[1:]:
        with open(path, encoding="utf-8") as f:
            src = f.read()
        with open(path, "w", encoding="utf-8") as f:
            f.write(renumber(src))
        print("renumbered", path)
