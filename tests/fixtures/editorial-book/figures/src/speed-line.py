import json, pathlib
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
