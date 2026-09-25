# harness/preflight.py
"""Dependency and environment probe. Never installs anything (Rule 10)."""
import argparse, importlib.util, json, os, pathlib, subprocess, sys

REPO = pathlib.Path(__file__).resolve().parents[1]
DEFAULT_GROUPS = ["core", "ingest", "build", "figures", "golden"]
FONT_FILES = ["Sitka.ttc", "segoeui.ttf", "majalla.ttf", "majallab.ttf"]  # ponytail: moves to presets in STEP 7
BROWSERS = [r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe",
            r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe",
            r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"]


def _c(name, group, ok, detail, required=True):
    return dict(name=name, group=group, ok=bool(ok), detail=detail, required=required)


def check_module(module, group, required=True, label=None):
    found = importlib.util.find_spec(module) is not None
    return _c(label or module, group, found, "present" if found else f"missing Python package: {module}", required)


def check_python():
    return _c("python>=3.11", "core", sys.version_info >= (3, 11), sys.version.split()[0])


def check_git():
    try:
        r = subprocess.run(["git", "--version"], capture_output=True, text=True)
        return _c("git", "core", r.returncode == 0, r.stdout.strip() or r.stderr.strip())
    except FileNotFoundError:
        return _c("git", "core", False, "git not on PATH")


def check_write_lock():
    projects = REPO / "projects"
    projects.mkdir(exist_ok=True)
    probe = projects / f".preflight-{os.getpid()}"
    try:
        with open(probe, "x", encoding="utf-8") as f:
            f.write("probe")
        probe.unlink()
    except OSError as e:
        return _c("write-lock", "core", False, f"cannot exclusive-create in projects/: {e}")
    stale = [f"{p}: {p.read_text(encoding='utf-8', errors='replace').strip()}" for p in projects.glob("*/state.lock")]
    return _c("write-lock", "core", not stale, "; ".join(stale) or "exclusive-create works, no leftover locks")


def check_word():
    if importlib.util.find_spec("win32com") is None:
        return _c("word-com", "build", False, "pywin32 missing")
    import pywintypes, win32com.client
    word = None
    try:
        word = win32com.client.DispatchEx("Word.Application")
        return _c("word-com", "build", True, f"Word {word.Version}")
    except pywintypes.com_error as e:
        return _c("word-com", "build", False, f"Word COM unavailable: {e}")
    finally:
        if word is not None:
            word.Quit()


def check_browser(group):
    for raw in BROWSERS:
        path = pathlib.Path(os.path.expandvars(raw))
        if path.exists():
            return _c("browser", group, True, str(path))
    return _c("browser", group, False, "no Edge or Chrome found for SVG rasterising")


def check_fonts():
    fonts = pathlib.Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts"
    missing = [f for f in FONT_FILES if not (fonts / f).exists()]
    return _c("fonts", "build", not missing, "missing: " + ", ".join(missing) if missing else "all present")


def check_rdkit():
    if importlib.util.find_spec("rdkit") is None:
        return _c("rdkit", "chemistry", False, "missing Python package: rdkit", required=False)
    from rdkit import Chem
    return _c("rdkit", "chemistry", Chem.MolFromSmiles("CCO") is not None, "smoke test CCO", required=False)


def run(groups):
    checks = []
    if "core" in groups:
        checks += [check_python(), check_git(), check_write_lock()]
    if "ingest" in groups:
        checks += [check_module("docx", "ingest", label="python-docx"), check_module("lxml", "ingest"),
                   check_module("markitdown", "ingest", required=False)]
    if "build" in groups:
        checks += [check_module("PIL", "build", label="Pillow"), check_module("win32com", "build", label="pywin32"),
                   check_word(), check_browser("build"), check_fonts()]
    if "figures" in groups:
        checks += [check_module("matplotlib", "figures")]
    if "golden" in groups:
        checks += [check_module("pypdf", "golden")]
    if "chemistry" in groups:
        c = check_rdkit()
        c["required"] = True  # explicitly requested
        checks.append(c)
    elif groups == DEFAULT_GROUPS:
        checks.append(check_rdkit())
    return checks


def exit_code(checks):
    return 0 if all(c["ok"] for c in checks if c["required"]) else 1


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--group", action="append")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    checks = run(a.group or DEFAULT_GROUPS)
    if a.json:
        print(json.dumps(checks, ensure_ascii=False, indent=1))
    else:
        for c in checks:
            tag = "OK" if c["ok"] else ("MISSING" if c["required"] else "OPTIONAL-MISSING")
            print(f"{tag} {c['name']}: {c['detail']}")
    sys.exit(exit_code(checks))


if __name__ == "__main__":
    main()
