"""Study decks straight from a project's ingested sources, for decks-only projects (no book). Gate: evaluate.

Usage: python harness/tools/build_source_deck.py --project projects/<p> [--chapter <outline stem>] [--pdf]

The gate is that of the first stage that reads the ingest output: the intake approved at matching hashes and a
fresh ingest receipt; no design, rework or build is needed, because the deck quotes the sources themselves.
Everything else is build_study.py in source mode: the outline (<out_dir>/study/<stem>.json) names its "topic",
the `# <chapter heading>` part of ingest/normalized.md it summarises, and every word on a slide is checked
against that part.
"""
import pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    from harness.gate import enforce
    PROJECT = enforce("evaluate", sys.argv, content_only=True)   # reads ingest output only (DECISIONS: source decks)
    from harness.tools import build_study
    args = sys.argv[1:]
    only = args[args.index("--chapter") + 1] if "--chapter" in args else None
    sys.exit(build_study.main(PROJECT, only, "--pdf" in args, source=True))
