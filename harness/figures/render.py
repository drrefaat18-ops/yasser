"""Render every figure of a project (core §7.2; plan Task 9.1) into <paths.figures>/out/.

Usage: python harness/figures/render.py --project projects/<slug>   (dry run: renders into a temp folder)
Charts run their matplotlib source; hand SVGs are rasterised by headless Edge/Chrome; pack kinds (chemistry) go
through their pack; existing rasters are copied byte for byte. Figures that need an author asset, or that fail
validation, are skipped here and reported by check_figures. Exit 0 ok; 1 on a render error or a refused gate;
2 on a config error.
"""
import math, pathlib, re, shutil, subprocess, sys, tempfile, xml.etree.ElementTree as ET

REPO = pathlib.Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))
from harness import figures, preflight  # noqa: E402
from harness.figures import charts, packs, png  # noqa: E402
from harness.tools import config  # noqa: E402

DPI = 300
CSS_DPI = 96


class RenderError(Exception):
    """A figure could not be rendered; the message names it."""


def _browser():
    c = preflight.check_browser("figures")
    if not c["ok"]:
        raise RenderError(c["detail"])
    return c["detail"]


def _length(v):
    m = re.match(r"^\s*([\d.]+)", v or "")
    return float(m.group(1)) if m else None


def svg_aspect(svg_path):
    """height / width of an SVG from its viewBox, else its width and height attributes."""
    root = ET.parse(svg_path).getroot()
    vb = (root.get("viewBox") or "").replace(",", " ").split()
    if len(vb) == 4 and float(vb[2]) > 0:
        return float(vb[3]) / float(vb[2])
    w, h = _length(root.get("width")), _length(root.get("height"))
    if w and h:
        return h / w
    raise RenderError(f"{svg_path.name}: no viewBox or width/height to size it")


def rasterise_svg(svg_path, out_png, width_cm, dpi=DPI):
    """Headless browser screenshot of the SVG filling the viewport, resized to the exact placed width."""
    from PIL import Image
    svg_path = pathlib.Path(svg_path).resolve()
    want_w = png.width_px(width_cm, dpi)
    want_h = round(want_w * svg_aspect(svg_path))
    scale = dpi / CSS_DPI
    css_w, css_h = math.ceil(want_w / scale), math.ceil(want_h / scale)
    with tempfile.TemporaryDirectory() as t:
        t = pathlib.Path(t)
        html = t / "page.html"
        html.write_text("<!doctype html><html><head><style>html,body{margin:0;padding:0;background:#fff;overflow:hidden}"
                        "img{display:block;width:100vw;height:100vh}</style></head><body>"
                        f"<img src=\"{svg_path.as_uri()}\"></body></html>", encoding="utf-8")
        shot = t / "shot.png"
        r = subprocess.run([_browser(), "--headless", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
                            "--allow-file-access-from-files", f"--user-data-dir={t / 'profile'}",
                            f"--screenshot={shot}", f"--window-size={css_w},{css_h}",
                            f"--force-device-scale-factor={scale}", html.as_uri()],
                           capture_output=True, text=True, timeout=120)
        if not shot.is_file():
            raise RenderError(f"{svg_path.name}: browser screenshot failed: {r.stderr.strip()[-300:]}")
        with Image.open(shot) as im:
            im.load()
            if im.size != (want_w, want_h):
                im = im.resize((want_w, want_h), Image.LANCZOS)
            png.write_canonical(im, out_png, dpi)


def versions(project_figs):
    """Versions of every renderer the figures used (recorded in build-report.json)."""
    import PIL
    v = {"Pillow": PIL.__version__}
    kinds = {f["kind"] for f in project_figs}
    if any(k.startswith("chart.") for k in kinds):
        v.update(charts.versions())
    if "diagram.svg" in kinds:
        v["browser"] = _browser_version()
    for name, mod in packs.registry().items():
        if name != "charts" and kinds & set(getattr(mod, "KINDS", ())):
            v.update(mod.versions())
    return v


def _browser_version():
    exe = pathlib.Path(_browser())
    dirs = sorted(d.name for d in exe.parent.iterdir() if d.is_dir() and re.fullmatch(r"[\d.]+", d.name))
    return f"{exe.stem} {dirs[-1]}" if dirs else exe.stem


def renderable(cfg, fig, registry):
    """True when the figure has a generated kind, an existing source and passes its pack's validation."""
    if fig.get("status") == "needs-author-asset" or fig["kind"] == "author-asset":
        return False
    src = cfg["project"] / fig["source"]
    if fig["kind"].startswith("chem."):
        name, mod = packs.pack_for(fig["kind"], registry)
        return mod is not None and not mod.preflight() and src.is_file() and not mod.validate(_spec(src))
    return src.is_file()


def _spec(src):
    import json
    return json.loads(src.read_text(encoding="utf-8"))


def render_all(project, cfg, out_dir=None):
    """-> [{id, svg, png, status}]. Clears the output folder (default <figures>/out) first: it holds only this
    build's renders."""
    man = figures.load(cfg)
    if man is None:
        return []
    out_dir = out_dir or figures.out_dir(cfg)
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)
    width = cfg["theme"]["layout"]["text_width"]
    registry = packs.registry()
    results = []
    for fig in man["figures"]:
        svg, raster = figures.out_paths(cfg, fig, out_dir)
        rel = lambda p: (p.relative_to(project).as_posix() if p.is_relative_to(project) else str(p)) if p else None
        if not renderable(cfg, fig, registry):
            results.append({"id": fig["id"], "svg": None, "png": None, "status": "skipped"})
            continue
        src = cfg["project"] / fig["source"]
        try:
            if fig["kind"] == "raster.existing":
                shutil.copyfile(src, raster)
            elif fig["kind"].startswith("chart."):
                charts.render(src, svg, raster, width, DPI)
            elif fig["kind"] == "diagram.svg":
                shutil.copyfile(src, svg)
                rasterise_svg(src, raster, width, DPI)
            else:
                name, mod = packs.pack_for(fig["kind"], registry)
                if mod is None:
                    raise RenderError(f"no pack renders kind {fig['kind']}")
                mod.render(_spec(src), svg, raster, width_cm=width, dpi=DPI)
        except (RenderError, charts.ChartError, OSError, ValueError) as e:
            raise RenderError(f"figure {fig['id']}: {e}") from e
        results.append({"id": fig["id"], "svg": rel(svg), "png": rel(raster),
                        "status": "copied" if fig["kind"] == "raster.existing" else "rendered"})
    return results


def main(project, argv):
    """Dry run (like convert_docx, step8 R32): renders into a temporary folder and prints the results. `run build`
    is the only writer of <figures>/out."""
    try:
        cfg = config.load(project)
        with tempfile.TemporaryDirectory() as t:
            res = render_all(project, cfg, pathlib.Path(t) / "out")
    except config.ConfigError as e:
        print(f"ERROR CONFIG: {e}", file=sys.stderr)
        return 2
    except RenderError as e:
        print(f"ERROR RENDER: {e}", file=sys.stderr)
        return 1
    for r in res:
        print(f"{r['status']} {r['id']}")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    from harness.gate import enforce
    PROJECT = enforce("build", sys.argv)
    sys.exit(main(PROJECT, sys.argv))
