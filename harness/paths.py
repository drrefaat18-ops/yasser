"""Repository root and project selection (core §1.1)."""
import pathlib, re, subprocess

NAME = re.compile(r"^[a-z0-9][a-z0-9-]{1,62}$")


def repo_root(start=None):
    here = pathlib.Path(start or __file__).resolve()
    out = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=here if here.is_dir() else here.parent,
                         capture_output=True, text=True)
    return pathlib.Path(out.stdout.strip()).resolve()


REPO = repo_root()


def resolve_project(arg, *, must_exist=True, repo=None):
    from harness.state import GateError  # ponytail: late import avoids a cycle; state owns the error type
    repo = pathlib.Path(repo or REPO).resolve()
    raw = pathlib.Path(arg)
    path = (raw if raw.is_absolute() else repo / raw).resolve()
    if path.parent != repo / "projects":
        raise GateError("PROJECT-OUTSIDE", f"{arg} resolves to {path}, not a direct child of {repo / 'projects'}")
    if not NAME.match(path.name):
        raise GateError("PROJECT-NAME", f"project name {path.name!r} must match {NAME.pattern}")
    if must_exist and not path.is_dir():
        raise GateError("PROJECT-MISSING", f"{path} does not exist")
    return path
