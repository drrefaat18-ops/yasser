"""Annotated figures (plan Task 9b.4; DEC-045): numbered callouts with leader lines on a base image.

Spec (JSON under <paths.figures>/src/):
  {"kind": "diagram.annotated", "base": "<project-relative raster under an allowed asset root>",
   "callouts": [{"n": 1, "at": [x, y], "badge": [x, y], "label": "..."}, ...]}
Coordinates are base-image pixels: `at` is the point the leader line touches, `badge` where the number sits. The
labels are not drawn on the image; the writers print them as the figure's key under the caption, so they stay
crisp, searchable and translatable. The SVG embeds the base image and is rasterised by the browser path (render.py).
Colours and font come from the theme (primary badges, accent leader lines, the sans font for the numbers).
"""
import base64, json, pathlib

KIND = "diagram.annotated"


def load(cfg, fig):
    return json.loads((cfg["project"] / fig["source"]).read_text(encoding="utf-8"))


def _inside(path, root):
    try:
        return path.resolve().is_relative_to(root.resolve())
    except OSError:
        return False


def problems(cfg, spec):
    """-> [message] for FIG-ANNOT; empty when the spec is sound."""
    if not isinstance(spec, dict) or spec.get("kind") != KIND:
        return [f"source kind must be {KIND}"]
    project = cfg["project"]
    base = spec.get("base")
    if not isinstance(base, str) or not base.strip():
        return ["base is missing"]
    src = project / base
    roots = [project / r for r in cfg["template"]["paths"]["allowed_asset_roots"]]
    if not any(_inside(src, r) for r in roots):
        return [f"base {base!r} must lie under an allowed asset root"]
    if not src.is_file():
        return [f"base {base} missing"]
    from PIL import Image
    with Image.open(src) as im:
        w, h = im.size
    out = []
    cs = spec.get("callouts")
    if not isinstance(cs, list) or not cs:
        return ["callouts must be a non-empty list"]
    nums = [c.get("n") if isinstance(c, dict) else None for c in cs]
    if nums != list(range(1, len(cs) + 1)):
        out.append(f"callout numbers must run 1..{len(cs)} in order, got {nums}")
    for c in cs:
        if not isinstance(c, dict):
            continue
        for key in ("at", "badge"):
            p = c.get(key)
            if not (isinstance(p, list) and len(p) == 2 and all(isinstance(v, (int, float)) for v in p)
                    and 0 <= p[0] <= w and 0 <= p[1] <= h):
                out.append(f"callout {c.get('n')}: {key} {p!r} is not a point inside the {w} x {h} image")
        if not isinstance(c.get("label"), str) or not c["label"].strip():
            out.append(f"callout {c.get('n')}: label is blank")
    return out


def to_svg(cfg, spec):
    project = cfg["project"]
    src = project / spec["base"]
    from PIL import Image
    with Image.open(src) as im:
        w, h = im.size
        mime = "image/jpeg" if im.format == "JPEG" else "image/png"
    data = base64.b64encode(src.read_bytes()).decode("ascii")
    pal, sans = cfg["theme"]["palette"], cfg["theme"]["fonts"]["sans"]
    pri, acc = "#" + pal["primary"].lstrip("#"), "#" + pal["accent"].lstrip("#")
    r = max(w, h) / 42   # badge radius; lines and dots scale with it
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {w} {h}" '
             f'width="{w}" height="{h}"><image x="0" y="0" width="{w}" height="{h}" xlink:href="data:{mime};base64,{data}"/>']
    for c in spec["callouts"]:
        (ax, ay), (bx, by) = c["at"], c["badge"]
        parts.append(f'<line x1="{bx}" y1="{by}" x2="{ax}" y2="{ay}" stroke="{acc}" stroke-width="{r / 6:.2f}" '
                     f'stroke-dasharray="{r / 2.2:.2f} {r / 3.5:.2f}"/>'
                     f'<circle cx="{ax}" cy="{ay}" r="{r / 3.2:.2f}" fill="{acc}" stroke="#fff" stroke-width="{r / 10:.2f}"/>'
                     f'<circle cx="{bx}" cy="{by}" r="{r:.2f}" fill="{pri}" stroke="#fff" stroke-width="{r / 6:.2f}"/>'
                     f'<text x="{bx}" y="{by}" dy="0.36em" text-anchor="middle" font-family="{sans}" font-weight="700" '
                     f'font-size="{r * 1.15:.2f}" fill="#fff">{int(c["n"])}</text>')
    return "".join(parts) + "</svg>"


def render(cfg, spec, out_svg, out_png, width_cm, dpi):
    from harness.figures import render as rnd
    pathlib.Path(out_svg).write_text(to_svg(cfg, spec), encoding="utf-8", newline="\n")
    rnd.rasterise_svg(out_svg, out_png, width_cm, dpi)


def key(cfg, fig):
    """[(number, label)] in number order, for the key under the caption."""
    return [(c["n"], c["label"]) for c in load(cfg, fig)["callouts"]]
