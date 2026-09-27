"""Figure system (core §7). Shared helpers: the manifest, figure references in chapters, computed numbering.

A chapter places a figure with an image link to its manifest id: `![](fig:<id>)`. Caption, alt text, credit and
licence live in `<paths.figures>/figures.json`, never in the chapter. Numbers are computed, never stored: the n-th
distinct figure placed in chapter c (plan order, 1-based) is `template.figures.caption_pattern` with {chapter}=c, {n}=n.
Manifest `source` paths are project-relative.
"""
import json, re

MANIFEST = "figures.json"
FIG_LINK = re.compile(r"!\[[^\]]*\]\(fig:([^)\s]*)\)")
IMAGE_LINK = re.compile(r"!\[[^\]]*\]\(([^)\s]+)\)")
GENERATED = "generated"


def manifest_path(cfg):
    return cfg.path("figures") / MANIFEST


def load(cfg):
    """The manifest dict, or None when the project has no figures.json."""
    p = manifest_path(cfg)
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None


def references(cfg):
    """[(chapter entry, chapter number, [fig ids in order of appearance], [direct image links])] in plan order."""
    out = []
    for n, (entry, path) in enumerate(cfg.chapters(), 1):
        text = path.read_text(encoding="utf-8")
        direct = [l for l in IMAGE_LINK.findall(text) if not l.startswith("fig:")
                  and not re.match(r"^[a-z][a-z0-9+.-]*:", l, re.I)]
        out.append((entry, n, FIG_LINK.findall(text), direct))
    return out


def numbering(cfg):
    """{fig id: (chapter id, label)} by order of first reference; a figure referenced twice keeps its first number."""
    pattern = cfg["template"]["figures"]["caption_pattern"]
    nums = {}
    for entry, chapter_n, ids, _ in references(cfg):
        k = 0
        for fid in ids:
            if fid not in nums:
                k += 1
                nums[fid] = (entry["id"], pattern.format(chapter=chapter_n, n=k))
    return nums


def out_dir(cfg):
    return cfg.path("figures") / "out"


def out_paths(cfg, fig, out=None):
    """Rendered files of one figure: (svg or None, raster). Existing rasters keep their extension."""
    out = out or out_dir(cfg)
    if fig["kind"] == "raster.existing":
        ext = fig["source"].rsplit(".", 1)[-1].lower()
        return None, out / f"{fig['id']}.{ext}"
    return out / f"{fig['id']}.svg", out / f"{fig['id']}.png"


MAX_WIDTH_CM, TALL_WIDTH_CM, TALL_RATIO = 14, 10, 0.9   # ltr-textbook layout constants (step8 R16)


def placed_width_cm(w_px, h_px, text_width_cm):
    """Width a raster is placed at in the DOCX: the text width capped at 14 cm; tall figures (h/w > 0.9) at 10 cm.
    The builder and FIG-RESOLUTION both use this, so the checked dpi is the printed dpi."""
    if h_px / w_px > TALL_RATIO:
        return min(TALL_WIDTH_CM, text_width_cm)
    return min(text_width_cm, MAX_WIDTH_CM)
