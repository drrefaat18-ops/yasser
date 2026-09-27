"""Assemble front matter, chapters and glossary into build/<basename>.md (core §1.1; plan Task 8.1).

Usage: python harness/tools/assemble.py --project projects/<slug>
The CLI is a dry run: it assembles and prints the problems and word count; `run build` is the only writer of build/
(step9 fix S9-03).
Image links are resolved relative to their source file, must lie under template.paths.allowed_asset_roots, and are
rewritten relative to the output file (path-relative, never prefix replacement; INV-40).
Exit 0 ok; 1 if any image is missing or outside the asset roots, or the gate refuses; 2 on a config error.
"""
import os, pathlib, re, sys

REPO = pathlib.Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))
from harness import figures  # noqa: E402
from harness.tools import config  # noqa: E402

IMAGE_LINK = re.compile(r"(!\[[^\]]*\]\()([^)\s]+)(\))")


class AssetOutside(Exception):
    """An image link resolves outside every allowed asset root."""


def _external(link):
    return bool(re.match(r"^[a-z][a-z0-9+.-]*:", link, re.I)) or link.startswith("#")


def resolve_asset(source_file, link, cfg):
    """Absolute path of an image link written in `source_file`; raises AssetOutside when outside the roots."""
    path = pathlib.Path(os.path.normpath(pathlib.Path(source_file).resolve().parent / link))
    roots = [(cfg["project"] / r).resolve() for r in cfg["template"]["paths"]["allowed_asset_roots"]]
    if not any(path.is_relative_to(r) for r in roots):
        raise AssetOutside(f"image {link} resolves outside the asset roots {cfg['template']['paths']['allowed_asset_roots']}")
    return path


def rewrite_links(text, source_file, out_dir, cfg, problems):
    man = figures.load(cfg)
    by_id = {f["id"]: f for f in man["figures"]} if man else {}
    numbers = figures.numbering(cfg) if man else {}

    def one(m):
        link = m.group(2)
        if link.startswith("fig:"):   # a manifest figure: its render in <figures>/out, captioned from the manifest
            fig = by_id.get(link[4:])
            if fig is None:
                problems.append(f"{pathlib.Path(source_file).name}: {link} is not in the figure manifest")
                return m.group(0)
            path = figures.out_paths(cfg, fig)[1]
            label = numbers[fig["id"]][1] if fig["id"] in numbers else ""
            caption = f"{label} — {fig['caption']}" if label else fig["caption"]
            # alt text, then the numbered caption and the credit with its licence (core §7.1), as in the DOCX
            return (f"![{fig['alt']}](" + pathlib.Path(os.path.relpath(path, out_dir)).as_posix() + m.group(3)
                    + f"\n\n*{caption}*  \n{fig['credit']} ({fig['licence']})")
        if _external(link):
            return m.group(0)
        try:
            path = resolve_asset(source_file, link, cfg)
        except AssetOutside as e:
            problems.append(f"{pathlib.Path(source_file).name}: {e}")
            return m.group(0)
        if not path.is_file():
            problems.append(f"{pathlib.Path(source_file).name}: missing image {link}")
        return m.group(1) + pathlib.Path(os.path.relpath(path, out_dir)).as_posix() + m.group(3)
    return IMAGE_LINK.sub(one, text)


def anchor(title):
    # GitHub-style heading anchor
    a = re.sub(r"[^\w\s-]", "", title.lower()).strip()
    return re.sub(r"\s", "-", a)


def output_path(cfg):
    return cfg["project"] / "build" / f"{cfg['theme']['output']['basename']}.md"


def assemble(cfg):
    """-> (book text, problems). Order: front matter with the contents list inserted, chapters, glossary."""
    out = output_path(cfg)
    probs = []
    t = cfg["template"]
    front_file = cfg.book_file("front_matter")
    files = [p for _, p in cfg.chapters()]
    glossary = cfg.book_file("glossary") if t["glossary"]["enabled"] else None
    parts = [rewrite_links(p.read_text(encoding="utf-8"), p, out.parent, cfg, probs) for p in files]
    if glossary is not None:
        parts.append(rewrite_links(glossary.read_text(encoding="utf-8"), glossary, out.parent, cfg, probs))
    titles = [re.search(r"^# (.+)$", p, re.M).group(1) for p in parts]
    toc = f"## {cfg['theme']['labels']['contents']}\n\n" + "\n".join(f"- [{x}](#{anchor(x)})" for x in titles) + "\n"
    if front_file is None:
        book = toc
    else:
        front = rewrite_links(front_file.read_text(encoding="utf-8"), front_file, out.parent, cfg, probs)
        before = t["front_matter"]["toc_insert_before_section_id"]
        label = next((s["label"] for s in t["sections"] if s["id"] == before), None) if before else None
        marker = f"\n## {label}" if label else None
        if marker and marker in front:
            head, rest = front.split(marker, 1)
            book = head.rstrip() + "\n\n" + toc + marker + rest
        else:
            book = front.rstrip() + "\n\n" + toc
    book += "".join("\n\n---\n\n" + p.strip() + "\n" for p in parts)
    return book, probs


def main(project):
    try:
        cfg = config.load(project)
        book, probs = assemble(cfg)
    except (config.ConfigError, KeyError, FileNotFoundError, AttributeError) as e:
        print(f"ERROR CONFIG: {e}", file=sys.stderr)
        return 2
    for p in probs:
        print(p)
    print(f"assembled {output_path(cfg).name}: {len(book.split())} words (dry run, not written)")
    return 1 if probs else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    from harness.gate import enforce
    PROJECT = enforce("build", sys.argv)   # first call: no stage work before the gates pass
    sys.exit(main(PROJECT))
