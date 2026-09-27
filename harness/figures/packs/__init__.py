"""Figure pack registry (core §7.4): the built-in `charts` plus each package directory under this folder."""
import importlib, pathlib

HERE = pathlib.Path(__file__).resolve().parent


def registry():
    from harness.figures import charts
    packs = {"charts": charts}
    for d in sorted(HERE.iterdir()):
        if d.is_dir() and (d / "__init__.py").is_file():
            packs[d.name] = importlib.import_module(f"harness.figures.packs.{d.name}")
    return packs


def pack_for(kind, packs=None):
    """(name, module) of the pack that renders `kind`, or (None, None)."""
    packs = packs or registry()
    if kind.startswith("chart."):
        return "charts", packs["charts"]
    for name, mod in packs.items():
        if kind in getattr(mod, "KINDS", ()):
            return name, mod
    return None, None
