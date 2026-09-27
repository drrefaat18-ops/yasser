"""Test-side: (re)generate tests/fixtures/figures-book (plan Tasks 9.1, 9.3).

Usage: python tests/tools/make_figures_book.py
A two-chapter book built on the positive-config generator, with one figure of every kind the core renders: an
existing raster, a bar chart, a line chart and a hand SVG diagram, plus the chemistry specs of Task 9.3. In chapter 2
the manifest lists the line chart first, but the diagram is placed first, so it is Figure 2.1 (numbering by first
reference). `temp_repo(stamp=True)` re-hashes the control-plane files.
"""
import importlib.util, json, pathlib, shutil, sys

REPO = pathlib.Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))
_spec = importlib.util.spec_from_file_location("make_positive_config", REPO / "tests/tools/make_positive_config.py")
pc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pc)

OUT = REPO / "tests" / "fixtures" / "figures-book"
SLUG = "figures-book"

BAR = '''import matplotlib.pyplot as plt

objects = ["Bicycle", "Car", "Train", "Plane"]
speed = [5, 27, 83, 250]
fig, ax = plt.subplots(figsize=(6, 3.4))
ax.bar(objects, speed, color="#2B5D8A")
ax.set_ylabel("Top speed (m/s)")
ax.set_title("Typical top speeds")
for side in ("top", "right"):
    ax.spines[side].set_visible(False)
fig.tight_layout()
'''
LINE = '''import json, pathlib
import matplotlib.pyplot as plt

data = json.loads(pathlib.Path("speed-line.json").read_text(encoding="utf-8"))
fig, ax = plt.subplots(figsize=(6, 3.4))
for name, points in data["series"].items():
    ax.plot(data["time_s"], points, marker="o", label=name)
ax.set_xlabel("Time (s)")
ax.set_ylabel("Distance (m)")
ax.set_title("Distance travelled over time")
ax.legend(frameon=False)
for side in ("top", "right"):
    ax.spines[side].set_visible(False)
fig.tight_layout()
'''
LINE_DATA = {"time_s": [0, 1, 2, 3, 4, 5],
             "series": {"Steady speed": [0, 2, 4, 6, 8, 10], "Slowing down": [0, 3, 5.5, 7, 7.8, 8]}}
DIAGRAM = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 300" width="600" height="300">
  <rect x="0" y="0" width="600" height="300" fill="#ffffff"/>
  <line x1="40" y1="240" x2="560" y2="240" stroke="#1B1B1B" stroke-width="3"/>
  <rect x="230" y="160" width="140" height="80" fill="#E8EEF4" stroke="#2B5D8A" stroke-width="3"/>
  <text x="300" y="207" font-family="Arial" font-size="20" text-anchor="middle" fill="#1B1B1B">Box</text>
  <line x1="370" y1="200" x2="500" y2="200" stroke="#2B5D8A" stroke-width="5"/>
  <polygon points="500,188 524,200 500,212" fill="#2B5D8A"/>
  <text x="440" y="185" font-family="Arial" font-size="18" text-anchor="middle" fill="#2B5D8A">Push</text>
  <line x1="230" y1="228" x2="110" y2="228" stroke="#B5462F" stroke-width="5"/>
  <polygon points="110,216 86,228 110,240" fill="#B5462F"/>
  <text x="165" y="265" font-family="Arial" font-size="18" text-anchor="middle" fill="#B5462F">Friction</text>
  <text x="300" y="60" font-family="Arial" font-size="22" text-anchor="middle" fill="#1B1B1B">Forces on a sliding box</text>
</svg>
'''

CHEM = {
    "aspirin": {"kind": "chem.structure", "name": "aspirin", "smiles": "CC(=O)Oc1ccccc1C(=O)O", "pubchem_cid": 2244},
    "caffeine": {"kind": "chem.structure", "name": "caffeine", "smiles": "Cn1cnc2c1c(=O)n(C)c(=O)n2C", "pubchem_cid": 2519},
    "ethanol-oxidation": {"kind": "chem.reaction", "name": "ethanol oxidation", "smarts": "CCO>>CC=O",
                          "conditions": "acidified potassium dichromate, warm"},
}
CH1_FIGS = "\n![](fig:rolling-ball)\n\n![](fig:speed-bar)\n"
CH2 = """# Chapter 2: Friction and Graphs

## Starting Question

A box slides across a floor and stops. How can a graph show that it is slowing down?

## Learning Objectives

1. [LO1] Describe how friction acts on a sliding object.
2. [LO2] Read the slope of a distance and time graph.
3. [LO3] Compare steady motion with slowing motion on a graph.

## 2.1 Friction on a Box

When you push a box, the floor pushes back. This push is **friction**. It acts against the motion [1]. A rough floor gives more friction than a smooth one. The box slows down when you stop pushing.

![](fig:friction-diagram)

> **Key Idea:** Friction always acts against the motion. It turns the energy of motion into heat.

## 2.2 Reading a Graph

A graph of distance against time shows motion at a glance. A straight line means a steady speed. A line that flattens means the object is slowing down [2]. The slope of the line is the speed at that moment.

![](fig:speed-line)

> **Viewpoints**
> - **Theory:** The slope of a distance graph is the speed. A flat line means the object has stopped.
> - **Experiment:** Time a toy car every second. Plot the points and join them. The shape tells you the story.
> - **Engineering:** Car makers log speed and distance. The graphs show them how well the brakes work.

## 2.3 Friction and Heat

Friction turns the energy of motion into heat. Chemists draw the molecules that store and release energy. Aspirin and caffeine are two small molecules. When ethanol is oxidised, it becomes a new molecule called ethanal.

![](fig:aspirin)

![](fig:caffeine)

![](fig:ethanol-oxidation)

## Key Points

- Friction acts against motion and slows objects down.
- A straight line on a distance graph means a steady speed.
- A flattening line means the object is slowing down.

## Check Yourself

**Q1.** Which way does friction act on a sliding box? [LO1]
A) Along the motion.
B) Against the motion.
C) Straight up.
D) It does not act.

**Q2.** A distance graph is a straight line. What does this show? [LO2]
A) The object is speeding up.
B) The object has stopped.
C) The object moves at a steady speed.
D) The object moves backwards.

**Q3.** One line flattens and the other stays straight. Which object is slowing down? [LO3]
A) The one with the flattening line.
B) The one with the straight line.
C) Both of them.
D) Neither of them.

**Case Question.** Lina slides a book across a table. Sketch its distance graph and explain its shape.

## Answers

**Q1. B** — Friction acts against the motion [1].

**Q2. C** — A straight line means equal distances in equal times.

**Q3. A** — The flattening line shows less distance each second [2].

## References

1. Newton I. Philosophiae naturalis principia mathematica. London: Royal Society; 1687.
2. Halliday D, Resnick R, Walker J. Fundamentals of physics. 10th ed. Hoboken: Wiley; 2013.
"""
GLOSSARY_EXTRA = "\n**Friction** — A force between two surfaces that acts against motion.\n"


def fig(fid, chapter, kind, source, caption, alt, status="generated", credit="Figures-book fixture", licence="original"):
    return {"id": fid, "chapter_id": chapter, "kind": kind, "source": source, "caption": caption, "alt": alt,
            "credit": credit, "licence": licence, "status": status}


FIGURES = [
    fig("rolling-ball", "ch01", "raster.existing", "chapters/figures/rolling-ball.png", "A ball rolling to a stop",
        "An orange ball on green grass, slowing down", status="existing"),
    fig("speed-bar", "ch01", "chart.bar", "figures/src/speed-bar.py", "Typical top speeds of four vehicles",
        "Bar chart: bicycle 5, car 27, train 83 and plane 250 metres per second"),
    fig("speed-line", "ch02", "chart.line", "figures/src/speed-line.py", "Steady and slowing motion on a distance graph",
        "Line chart of distance against time: one straight line, one that flattens"),
    fig("aspirin", "ch02", "chem.structure", "figures/src/aspirin.json", "Aspirin (acetylsalicylic acid)",
        "Skeletal structure of aspirin: a benzene ring with an ester group and a carboxylic acid group"),
    fig("caffeine", "ch02", "chem.structure", "figures/src/caffeine.json", "Caffeine",
        "Skeletal structure of caffeine: two fused rings with three methyl groups and two carbonyl groups"),
    fig("ethanol-oxidation", "ch02", "chem.reaction", "figures/src/ethanol-oxidation.json", "Oxidation of ethanol to ethanal",
        "Reaction scheme: ethanol, an arrow, then ethanal"),
    fig("friction-diagram", "ch02", "diagram.svg", "figures/src/friction-diagram.svg", "Push and friction on a sliding box",
        "A box on a floor with a push arrow to the right and a friction arrow to the left"),
]


def ball_png():
    from PIL import Image, ImageDraw
    from harness.figures import png
    w = png.width_px(14, 300)
    im = Image.new("RGB", (w, round(w * 0.55)), (214, 234, 206))
    d = ImageDraw.Draw(im)
    d.rectangle([0, im.size[1] * 0.7, w, im.size[1]], fill=(92, 160, 76))
    for k, x in enumerate(range(200, w - 200, 300)):
        r = 120 - 12 * k
        d.ellipse([x - r, im.size[1] * 0.7 - 2 * r, x + r, im.size[1] * 0.7], fill=(236, 128, 36))
    return im


def make():
    if OUT.exists():
        shutil.rmtree(OUT)
    pc.OUT = OUT.parent / ".figures-book-tmp"
    pc.make("no-errata")
    shutil.move(str(pc.OUT / "no-errata"), str(OUT))
    shutil.rmtree(pc.OUT)
    d = OUT
    for name in ("brief.json", "template.json", "theme.json", "rubric.json", "design/chapter-plan.json", "state.json"):
        j = json.loads((d / name).read_text(encoding="utf-8"))
        j["project_id"] = SLUG
        if name == "state.json":
            j["receipts"]["new"]["args"]["slug"] = SLUG
        if name == "template.json":
            j["budgets"]["total"] = {"min": 600, "max": 1400}
        if name == "brief.json":
            j["identity"]["title"] = "Motion and Figures"
            j["figures"]["packs"] = ["charts", "chemistry"]
        if name == "theme.json":
            j["output"]["basename"] = "motion-and-figures"
        if name == "design/chapter-plan.json":
            j["chapters"].append({"id": "ch02", "file": "ch02-friction-graphs.md", "title": "Friction and Graphs",
                                  "word_budget": 470, "part_id": None, "source_refs": []})
        pc.write_json(d / name, j)
    ch = d / "chapters"
    ch1 = (ch / "ch01-forces.md").read_text(encoding="utf-8")
    ch1 = ch1.replace("\n![A ball rolling to a stop](fig:ball)\n", CH1_FIGS)
    (ch / "ch01-forces.md").write_text(ch1, encoding="utf-8", newline="\n")
    (ch / "ch02-friction-graphs.md").write_text(CH2, encoding="utf-8", newline="\n")
    g = ch / "glossary.md"
    g.write_text(g.read_text(encoding="utf-8") + GLOSSARY_EXTRA, encoding="utf-8", newline="\n")
    (ch / "figures" / "ball.png").unlink()
    from harness.figures import png
    png.write_canonical(ball_png(), ch / "figures" / "rolling-ball.png", 300)
    src = d / "figures" / "src"
    src.mkdir(parents=True)
    for name, text in (("speed-bar.py", BAR), ("speed-line.py", LINE), ("friction-diagram.svg", DIAGRAM)):
        (src / name).write_text(text, encoding="utf-8", newline="\n")
    pc.write_json(src / "speed-line.json", LINE_DATA)
    for name, spec in CHEM.items():
        pc.write_json(src / f"{name}.json", spec)
    pc.write_json(d / "figures" / "figures.json", {"schema_version": 1, "figures": FIGURES})


if __name__ == "__main__":
    make()
    print(f"wrote {OUT.relative_to(REPO).as_posix()}")
