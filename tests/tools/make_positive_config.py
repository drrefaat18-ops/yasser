"""Test-side: (re)generate the five positive-config fixture projects (core §9.4; plan Task 8.1 Step 4).

Usage: python tests/tools/make_positive_config.py
Each fixture is a complete small project with exactly one feature disabled. The control-plane files (state.json,
decisions.md, evaluation/, ingest/, source/) come from tests/fixtures/bypass; `temp_repo(stamp=True)` re-hashes them.
"""
import copy, json, pathlib, shutil, struct, zlib

REPO = pathlib.Path(__file__).resolve().parents[2]
BYPASS = REPO / "tests" / "fixtures" / "bypass"
OUT = REPO / "tests" / "fixtures" / "positive-config"
NAMES = ["no-mcq", "no-glossary", "no-cases", "no-perspectives", "no-errata"]
COPY = ["decisions.md", "evaluation", "ingest", "source", "source-manifest.json", "rubric.json", "design/design.md",
        "design/errata-seed.md"]

OPENING = """## Starting Question

A cyclist stops pedalling on a flat road. The bike slows down and stops. Why does it stop, and what would change on ice?
"""
OBJECTIVES = """## Learning Objectives

1. [LO1] State Newton's second law in words and as an equation.
2. [LO2] Explain why a moving object slows down when friction acts on it.
3. [LO3] Predict how a larger mass changes the acceleration for the same force.
"""
CORE = """## 1.1 Force and Motion

A **force** is a push or a pull. Forces change how things move. A ball at rest starts to roll when you kick it. A rolling ball stops when the grass pushes back on it [1].

Newton described this in three laws. The second law is the one we use most. It links force, mass and acceleration in one short equation [1].

## 1.2 Mass and Acceleration

**Mass** measures how much matter an object holds. It also measures how hard the object is to speed up. A heavy truck needs a large force to start moving. A toy car needs only a small one.

**Acceleration** is the rate at which speed or direction changes. We measure it in metres per second squared. The second law says that force equals mass times acceleration [2]. Double the force and the acceleration doubles. Double the mass and the acceleration halves.

![A ball rolling to a stop](fig:ball)

> **Key Idea:** Force causes a change in motion. It does not keep motion going. An object keeps moving at a steady speed unless a force acts on it.

## 1.3 Friction

Friction is a force between two surfaces that touch. It acts against the motion. On a road, friction slows the bike. On ice, friction is small, so the bike rolls much further. Engineers use this idea when they design brakes and tyres [2].
"""
PERSPECTIVES = """
> **Viewpoints**
> - **Theory:** The second law turns a force into a number we can predict. It tells us how fast a speed will change.
> - **Experiment:** A trolley on a track shows the law. Add weights and time it. The numbers match the equation well.
> - **Engineering:** Car makers use the law for brakes. They pick a force that stops the car safely and smoothly.
"""
TAKEAWAYS = """
## Key Points

- A force is a push or a pull that changes motion.
- Force equals mass times acceleration.
- Friction acts against motion and slows objects down.
"""
CASE = """
**Case Question.** Sami pushes a shopping trolley and lets go. Explain why it stops, and what would happen on a smooth floor.
"""
QUIZ = """
## Check Yourself

**Q1.** What does a force do to an object? [LO1]
A) It always stops the object.
B) It changes the object's motion.
C) It keeps the object moving forever.
D) It makes the object lighter.

**Q2.** Why does a rolling ball slow down on grass? [LO2]
A) The grass pushes against its motion.
B) The ball loses its mass.
C) Gravity turns off.
D) The air gets heavier.

**Q3.** The same force acts on a bigger mass. What happens to the acceleration? [LO3]
A) It doubles.
B) It stays the same.
C) It becomes smaller.
D) It becomes negative.
{case}
## Answers

**Q1. B** — A force changes speed or direction [1].

**Q2. A** — Friction from the grass acts against the motion.

**Q3. C** — A larger mass means a smaller acceleration for the same force [2].
"""
REFS = """
## References

1. Newton I. Philosophiae naturalis principia mathematica. London: Royal Society; 1687.
2. Halliday D, Resnick R, Walker J. Fundamentals of physics. 10th ed. Hoboken: Wiley; 2013.
"""
FRONT = """# Motion Basics

## Using This Book

This short book explains how forces change motion. Each chapter starts with a question. It ends with a few checks and their answers. Read the chapter first. Then try the checks without looking back. The glossary lists every key term in bold.
"""
GLOSSARY = """# Glossary

**Acceleration** — The rate at which speed or direction changes.

**Force** — A push or a pull that changes how something moves.

**Mass** — How much matter an object holds; how hard it is to speed up.
"""
ERRATA = """# Errata

| # | Topic | Correct statement | Status |
|---|---|---|---|
| 1 | Units of acceleration | Metres per second squared | fixed (Ch1 §1.2) |
"""


def png(width=4, height=3):
    raw = b"".join(b"\x00" + b"\xff\x80\x00" * width for _ in range(height))
    chunk = lambda t, d: struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))


def template(slug):
    t = json.loads((BYPASS / "template.json").read_text(encoding="utf-8"))
    t["project_id"] = slug
    t["paths"] = {"chapters": "chapters", "chapter_glob": "ch*.md", "front_matter": "00-front.md", "glossary": "glossary.md",
                  "errata": "errata.md", "figures": "figures", "normalized_source": "ingest/normalized.md",
                  "assets": "ingest/assets", "asset_link_prefix": "", "allowed_asset_roots": ["ingest/assets", "chapters/figures"]}
    sec = lambda i, label, role, req=True: {"id": i, "label": label, "role": role, "required": req, "boxed": False}
    t["sections"] = [sec("opening", "Starting Question", "opening"), sec("objectives", "Learning Objectives", "objectives"),
                     sec("takeaways", "Key Points", "takeaways"), sec("assessment", "Check Yourself", "assessment"),
                     sec("answers", "Answers", "answers"), sec("references", "References", "references"),
                     sec("how-to-use", "Using This Book", "how_to_use", False)]
    t["callouts"] = [{"id": "key-idea", "label": "Key Idea", "syntax": "> **Key Idea:**", "required": True, "min": 1, "max": 2, "parts": []},
                     {"id": "viewpoints", "label": "Viewpoints", "syntax": "> **Viewpoints**", "required": True, "min": 1, "max": 1,
                      "parts": ["Theory", "Experiment", "Engineering"]}]
    t["perspectives"] = {"enabled": True, "callout_id": "viewpoints", "balance_tolerance": 0.3,
                         "items": [{"id": "theory", "label": "Theory"}, {"id": "experiment", "label": "Experiment"},
                                   {"id": "engineering", "label": "Engineering"}]}
    t["learning_objectives"] = {"enabled": True, "id_pattern": "^LO\\d+$", "min": 2, "max": 4, "discouraged_verbs": ["understand"]}
    t["assessment"] = {"mcq": {"enabled": True, "count": 3, "option_labels": list("ABCD"), "option_display_labels": list("ABCD"),
                               "allow_other_labels": False, "key_balance": {"min": 0, "max": 1}, "max_run": 1,
                               "rationale_required": True, "answers_section_role": "answers"},
                       "case_question": {"required": True, "label": "Case Question."}}
    t["citations"] = {"style": "numeric-bracket", "pattern": "\\[(\\d+(?:\\s*[,–-]\\s*\\d+)*)\\]"}
    t["references"] = dict(t["references"], entry_pattern=r"^(\d+)\. (.+)$",
                           no_doi_policy={"allowed_types": ["book"], "requires_url": False},
                           type_patterns={"book": r"(?i)\b(royal society|wiley)\b"})
    t["glossary"] = {"enabled": True, "term_syntax": "bold", "excluded_callout_ids": ["viewpoints"], "minimum_terms": 3}
    t["readability"] = {"mean_sentence_max": 16, "long_sentence_words": 28, "long_share_max": 0.05}
    t["budgets"] = {"tolerance": 0.2, "total": {"min": 300, "max": 800}, "front_matter": 50}
    t["errata"] = {"enabled": True, "status_column": "Status", "open_values": ["open"], "closed_values": ["fixed"]}
    t["front_matter"] = {"toc_insert_before_section_id": "how-to-use"}
    return t


def disable(name, t, brief):
    """Exactly one feature off; returns the chapter text for that fixture."""
    case, persp = CASE, PERSPECTIVES
    quiz = QUIZ
    if name == "no-mcq":
        t["assessment"] = {"mcq": {"enabled": False, "count": None, "option_labels": [], "option_display_labels": [],
                                   "allow_other_labels": False, "key_balance": None, "max_run": None,
                                   "rationale_required": False, "answers_section_role": None},
                           "case_question": {"required": False, "label": None}}
        t["sections"] = [s for s in t["sections"] if s["role"] not in ("assessment", "answers")]
        quiz = ""
        brief["assessment"]["cases"]["enabled"] = False
    elif name == "no-glossary":
        t["glossary"] = {"enabled": False, "term_syntax": None, "excluded_callout_ids": [], "minimum_terms": None}
        t["paths"]["glossary"] = None
    elif name == "no-cases":
        t["assessment"]["case_question"] = {"required": False, "label": None}
        case = ""
        brief["assessment"]["cases"]["enabled"] = False
    elif name == "no-perspectives":
        t["perspectives"] = {"enabled": False, "callout_id": None, "items": [], "balance_tolerance": None}
        t["callouts"] = [c for c in t["callouts"] if c["id"] != "viewpoints"]
        t["glossary"]["excluded_callout_ids"] = []
        persp = ""
        brief["perspectives"] = {"enabled": False, "items": []}
    elif name == "no-errata":
        t["errata"] = {"enabled": False, "status_column": None, "open_values": [], "closed_values": []}
        t["paths"]["errata"] = None
    if name != "no-mcq":
        brief["assessment"]["mcq"] = {"enabled": True, "per_chapter": 3, "options": 4, "format": "answers at chapter end"}
    return "# Chapter 1: Forces and Motion\n\n" + OPENING + "\n" + OBJECTIVES + "\n" + CORE + persp + TAKEAWAYS + \
        (quiz.format(case=case) if quiz else "") + REFS


def write_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")


def make(name):
    d = OUT / name
    if d.exists():
        shutil.rmtree(d)
    for rel in COPY:
        src, dst = BYPASS / rel, d / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        (shutil.copytree if src.is_dir() else shutil.copyfile)(src, dst)
    brief = json.loads((BYPASS / "brief.json").read_text(encoding="utf-8"))
    brief["project_id"] = name
    brief["identity"]["title"] = "Motion Basics"
    brief["perspectives"] = {"enabled": True, "items": [{"id": "theory", "label": "Theory"}, {"id": "experiment", "label": "Experiment"},
                                                        {"id": "engineering", "label": "Engineering"}]}
    brief["assessment"]["cases"]["enabled"] = True
    t = template(name)
    chapter = disable(name, t, brief)
    write_json(d / "template.json", t)
    write_json(d / "brief.json", brief)
    theme = json.loads((BYPASS / "theme.json").read_text(encoding="utf-8"))
    theme["project_id"] = name
    theme["output"]["basename"] = "motion-basics"
    write_json(d / "theme.json", theme)
    rubric = json.loads((d / "rubric.json").read_text(encoding="utf-8"))
    rubric["project_id"] = name
    write_json(d / "rubric.json", rubric)
    plan = {"schema_version": 1, "project_id": name, "parts": [], "dropped": [],
            "chapters": [{"id": "ch01", "file": "ch01-forces.md", "title": "Forces and Motion", "word_budget": 470,
                          "part_id": None, "source_refs": []}]}
    write_json(d / "design/chapter-plan.json", plan)
    ch = d / "chapters"
    (ch / "figures").mkdir(parents=True)
    (ch / "ch01-forces.md").write_text(chapter, encoding="utf-8", newline="\n")
    (ch / "figures" / "ball.png").write_bytes(png())
    write_json(d / "figures" / "figures.json", {"schema_version": 1, "figures": [   # core §7.1 manifest (STEP 9)
        {"id": "ball", "chapter_id": "ch01", "kind": "raster.existing", "source": "chapters/figures/ball.png",
         "caption": "A ball rolling to a stop", "alt": "An orange ball slowing down on grass", "credit": "Test fixture",
         "licence": "original", "status": "existing"}]})
    (ch / "00-front.md").write_text(FRONT, encoding="utf-8", newline="\n")
    if t["paths"]["glossary"]:
        (ch / "glossary.md").write_text(GLOSSARY, encoding="utf-8", newline="\n")
    if t["paths"]["errata"]:
        (ch / "errata.md").write_text(ERRATA, encoding="utf-8", newline="\n")
    st = json.loads((BYPASS / "state.json").read_text(encoding="utf-8"))
    st["project_id"] = name
    st["receipts"]["new"]["args"]["slug"] = name
    write_json(d / "state.json", st)


if __name__ == "__main__":
    for n in NAMES:
        make(n)
        print(f"wrote tests/fixtures/positive-config/{n}")
