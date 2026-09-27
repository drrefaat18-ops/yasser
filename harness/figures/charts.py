"""Core chart pack (core §7.2, 0b.6): a figure's Python source draws with matplotlib; the harness saves it.

The source runs in a subprocess (MPLBACKEND=Agg, cwd = its folder) and draws on the current figure. Its own
figsize sets the aspect ratio; the harness sets the width to the theme's text width. Output is deterministic:
fixed seeds (random, numpy), fixed SVG hash salt, text kept as text, no date or creator metadata, PNG re-encoded
by png.write_canonical.
"""
import json, os, pathlib, subprocess, sys

REPO = pathlib.Path(__file__).resolve().parents[2]

DRIVER = r"""
import io, json, runpy, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
args = json.loads(sys.argv[1])
sys.path.insert(0, args["repo"])
from harness.figures import png
matplotlib.rcParams.update({"svg.hashsalt": "harness", "svg.fonttype": "none", "font.family": "DejaVu Sans",
                            "path.simplify": True})
import random, numpy
random.seed(0)
numpy.random.seed(0)   # fixed seeds (core 7.2): a source drawing random data renders the same bytes
runpy.run_path(args["source"], run_name="figure_source")   # top-level drawing; not run as a script
fig = plt.gcf()
w, h = fig.get_size_inches()
width_in = args["width_cm"] / 2.54
fig.set_size_inches(width_in, width_in * h / w)
fig.savefig(args["svg"], format="svg", metadata={"Date": None, "Creator": None})
buf = io.BytesIO()
fig.savefig(buf, format="png", dpi=args["dpi"], metadata={"Software": None})
from PIL import Image
buf.seek(0)
im = Image.open(buf)
im.load()
want = png.width_px(args["width_cm"], args["dpi"])
if im.size[0] != want:   # matplotlib rounds the canvas; the placed width is exact
    im = im.resize((want, round(im.size[1] * want / im.size[0])), Image.LANCZOS)
png.write_canonical(im, args["png"], args["dpi"])
"""


class ChartError(Exception):
    pass


def render(spec_path, out_svg, out_png, width_cm, dpi=300):
    spec_path = pathlib.Path(spec_path).resolve()
    args = {"repo": str(REPO), "source": str(spec_path), "svg": str(pathlib.Path(out_svg).resolve()),
            "png": str(pathlib.Path(out_png).resolve()), "width_cm": width_cm, "dpi": dpi}
    pathlib.Path(out_svg).parent.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, MPLBACKEND="Agg", PYTHONHASHSEED="0", SOURCE_DATE_EPOCH="0")
    r = subprocess.run([sys.executable, "-c", DRIVER, json.dumps(args)], cwd=spec_path.parent, env=env,
                       capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        lines = (r.stderr or r.stdout).strip().splitlines()
        raise ChartError(f"{spec_path.name}: {lines[-1] if lines else 'exit ' + str(r.returncode)}")


def versions():
    import matplotlib
    return {"matplotlib": matplotlib.__version__}
