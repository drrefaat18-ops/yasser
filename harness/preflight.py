# harness/preflight.py
"""Dependency and environment probe. Never installs anything (Rule 10)."""
import argparse, importlib.util, json, os, pathlib, subprocess, sys

REPO = pathlib.Path(__file__).resolve().parents[1]
DEFAULT_GROUPS = ["core", "ingest", "build", "figures", "golden"]
# the union over tested presets; the Arabic fonts return with the RTL preset (STEP 10)
FONT_FILES = sorted({f for p in (REPO / "harness" / "presets").glob("*.json")
                     for f in json.loads(p.read_text(encoding="utf-8"))["required_font_files"]})
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
    windir = os.environ.get("WINDIR") or os.environ.get("SystemRoot")
    if not windir:
        return _c("fonts", "build", False, "WINDIR and SystemRoot unset: cannot locate the Windows font folder")
    dirs = [pathlib.Path(windir) / "Fonts"]
    if os.environ.get("LOCALAPPDATA"):   # per-user installs (no admin) land here
        dirs.append(pathlib.Path(os.environ["LOCALAPPDATA"]) / "Microsoft" / "Windows" / "Fonts")
    missing = [f for f in FONT_FILES if not any((d / f).exists() for d in dirs)]
    return _c("fonts", "build", not missing, "missing: " + ", ".join(missing) if missing else "all present")


def check_rdkit():
    if importlib.util.find_spec("rdkit") is None:
        return _c("rdkit", "chemistry", False, "missing Python package: rdkit", required=False)
    from rdkit import Chem
    return _c("rdkit", "chemistry", Chem.MolFromSmiles("CCO") is not None, "smoke test CCO", required=False)


# One registry: (groups the check belongs to, probe). Task 5.1 table; a check listed under two groups runs once.
CHECKS = [
    (("core",), check_python),
    (("core",), check_git),
    (("core",), check_write_lock),
    (("ingest", "build"), lambda: check_module("docx", "ingest", label="python-docx")),
    (("ingest", "build"), lambda: check_module("lxml", "ingest")),
    (("ingest",), lambda: check_module("markitdown", "ingest", required=False)),
    (("build",), lambda: check_module("PIL", "build", label="Pillow")),
    (("build",), lambda: check_module("win32com", "build", label="pywin32")),
    (("build",), check_word),
    (("build", "figures"), lambda: check_browser("build")),
    (("build",), check_fonts),
    (("figures",), lambda: check_module("matplotlib", "figures")),
    (("golden",), lambda: check_module("pypdf", "golden")),
    (("build",), lambda: check_module("pypdf", "build")),   # HTML engine merge and PDF gates (Task 9b.2-9b.3)
    (("build", "evidence"), lambda: check_module("fitz", "evidence", required=False, label="pymupdf")),   # checkpoints
]
GROUPS = ["core", "ingest", "build", "figures", "golden", "chemistry", "evidence"]


def run(groups):
    unknown = sorted(set(groups) - set(GROUPS))
    if unknown:
        raise ValueError(f"unknown group(s): {', '.join(unknown)}")
    checks = [probe() for member, probe in CHECKS if set(member) & set(groups)]
    if "chemistry" in groups:
        c = check_rdkit()
        c["required"] = True  # explicitly requested
        checks.append(c)
    elif sorted(groups) == sorted(DEFAULT_GROUPS):
        checks.append(check_rdkit())
    return checks


def exit_code(checks):
    return 0 if all(c["ok"] for c in checks if c["required"]) else 1


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--group", action="append", choices=GROUPS)
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
