import matplotlib.pyplot as plt

objects = ["Bicycle", "Car", "Train", "Plane"]
speed = [5, 27, 83, 250]
fig, ax = plt.subplots(figsize=(6, 3.4))
ax.bar(objects, speed, color="#2B5D8A")
ax.set_ylabel("Top speed (m/s)")
ax.set_title("Typical top speeds")
for side in ("top", "right"):
    ax.spines[side].set_visible(False)
fig.tight_layout()
