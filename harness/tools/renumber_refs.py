"""Drop uncited references and renumber citations by first appearance (plan Task 8.3; INV-47).

Usage: python harness/tools/renumber_refs.py --project projects/<slug> --chapter ID [--chapter ID ...]
Chapters are named by their chapter-plan.json ID, never by path. Citation grammar: template.citations.pattern;
the list is the section whose role is `references`. Exit 0 ok; 1 on a refused gate or a cited number missing from
the list; 2 on a config error.
"""
import argparse, pathlib, re, sys

REPO = pathlib.Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))
from harness.tools import check_book, config  # noqa: E402


class MissingReference(Exception):
    pass


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


def renumber(text, cfg):
    if cfg["template"]["citations"]["style"] != "numeric-bracket":
        raise check_book.ConfigError(f"citations.style {cfg['template']['citations']['style']!r} is not supported")
    label = {s["role"]: s["label"] for s in cfg["template"]["sections"]}.get(cfg["template"]["references"]["section_role"])
    group = re.compile(cfg["template"]["citations"]["pattern"])
    body, sep, refs = text.partition(f"\n## {label}")
    if not sep:
        return text
    entries = {}
    rx = re.compile(cfg["template"]["references"]["entry_pattern"])
    for line in refs.splitlines():
        m = rx.search(line)
        if m:
            n, rest = check_book.entry_parts(m, line)
            entries[n] = rest
    order = []
    for g in group.findall(body):
        for n in expand(g):
            if n not in order:
                order.append(n)
    missing = [n for n in order if n not in entries]
    if missing:
        raise MissingReference(f"cited but not in the list: {missing}")
    new = {old: k + 1 for k, old in enumerate(order)}
    body = group.sub(lambda m: "[" + compress(new[n] for n in expand(m.group(1))) + "]", body)
    return body + sep + "\n" + "\n".join(f"{new[o]}. {entries[o]}" for o in order) + "\n"


def main(project, argv):
    ap = argparse.ArgumentParser(prog="renumber_refs.py")
    ap.add_argument("--chapter", action="append", required=True)
    a = ap.parse_args(argv[1:])
    try:
        cfg = config.load(project)
        paths = {c["id"]: p for c, p in cfg.chapters()}
        unknown = [c for c in a.chapter if c not in paths]
        if unknown:
            raise check_book.ConfigError(f"not in chapter-plan.json: {unknown}")
        for cid in a.chapter:
            p = paths[cid]
            p.write_text(renumber(p.read_text(encoding="utf-8"), cfg), encoding="utf-8", newline="\n")
            print(f"renumbered {cid}")
    except (check_book.ConfigError, KeyError, FileNotFoundError) as e:
        print(f"ERROR CONFIG: {e}", file=sys.stderr)
        return 2
    except MissingReference as e:
        print(f"ERROR CHECK: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    from harness.gate import enforce
    PROJECT = enforce("rework", sys.argv)   # first call: no stage work before the gates pass
    sys.exit(main(PROJECT, sys.argv))
