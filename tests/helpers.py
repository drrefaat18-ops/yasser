# tests/helpers.py
import contextlib, pathlib, shutil, subprocess, sys, tempfile

REPO = pathlib.Path(__file__).resolve().parents[1]


LEGACY_TOOL_DIRS = ["projects/ai-in-medicine/rework/tools", "projects/ai-in-medicine/tools"]


@contextlib.contextmanager
def temp_repo(fixture=None, slug="fixture-book", *, stamp=False, with_legacy=False, project_from=None):
    """Core §9.6: a throwaway git repo with a committed copy of harness/ and one project under projects/.

    fixture      -- directory under tests/fixtures/ copied to projects/<slug>
    project_from -- instead, a real project path (e.g. "projects/ai-in-medicine") copied read-only
    with_legacy  -- also copy and commit the legacy tool dirs at the same relative paths
    stamp        -- recompute receipt/approval hashes, tool_sha and dec_row_sha256 inside the temp repo
    """
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        shutil.copytree(REPO / "harness", root / "harness", ignore=shutil.ignore_patterns("__pycache__"))
        (root / "projects").mkdir()
        run = lambda *a: subprocess.run(a, cwd=root, check=True, capture_output=True)
        run("git", "init", "-q")
        run("git", "config", "user.email", "t@t"); run("git", "config", "user.name", "t")
        tracked = ["harness"]
        if with_legacy:
            for d in LEGACY_TOOL_DIRS:
                shutil.copytree(REPO / d, root / d, ignore=shutil.ignore_patterns("__pycache__"))
            tracked += LEGACY_TOOL_DIRS
        run("git", "add", *tracked); run("git", "commit", "-qm", "tools")
        if project_from:
            slug = pathlib.PurePosixPath(project_from).name
            shutil.copytree(REPO / project_from, root / "projects" / slug, dirs_exist_ok=True,
                            ignore=shutil.ignore_patterns("__pycache__", "state.lock", "tools"))
        elif fixture:
            shutil.copytree(REPO / "tests" / "fixtures" / fixture, root / "projects" / slug)
        if stamp:
            stamp_project(root, root / "projects" / slug)
        yield root


def stamp_project(root, project):
    """Rewrite hashes inside state.json so a copied fixture is valid in this temp repo (test-only)."""
    import json
    sys.path.insert(0, str(root))
    from harness import hashing, state
    st = json.loads((project / "state.json").read_text(encoding="utf-8"))
    for sid, r in st["receipts"].items():
        for kind in ("inputs", "outputs"):
            r[kind] = {rel: hashing.hash_file(project / rel) for rel in r[kind]}
        if not r.get("imported"):   # plan N2: an imported receipt keeps tool_sha "imported"
            r["tool_sha"] = state.tool_sha(state.BY_ID[sid]["tool_paths"], repo=root)
        if r.get("dec_id"):
            r["dec_row_sha256"] = state.dec_row_hash(project, r["dec_id"])[0]
    for a in st["approvals"].values():
        a["files"] = {rel: hashing.hash_file(project / rel) for rel in a["files"]}
        a["dec_row_sha256"] = state.dec_row_hash(project, a["dec_id"])[0]
    (project / "state.json").write_text(json.dumps(st, ensure_ascii=False, indent=1, sort_keys=True) + "\n",
                                        encoding="utf-8", newline="\n")
    sys.path.remove(str(root))


def run_cli(root, *args):
    return subprocess.run([sys.executable, "harness/run_stage.py", *args], cwd=root,
                          capture_output=True, text=True, encoding="utf-8")
