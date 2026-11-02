# IMPERIA COLD WAR — compare installed island map data with its backup.
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from build import ROOT, AUDIT, BACKUP


def main():
    fig, axes = plt.subplots(2, 2, figsize=(11, 8), facecolor="#111a28")
    plt.subplots_adjust(left=.08, right=.97, bottom=.12, top=.83, wspace=.15, hspace=.28)
    fig.text(.08, .93, "Cayo Blanco del Sur", color="white", fontsize=22, weight="bold")
    fig.text(.08, .875, "State 1252 · Province 16537 · Cuba · 9 land pixels, matching native MD Kharg's pixel count", color="#b9c9dc", fontsize=10)
    box = (1528, 815, 1545, 830)
    for col, (folder, label) in enumerate([(BACKUP, "Before"), (ROOT, "Installed")]):
        for row, (stem, title) in enumerate([("provinces", "Province map"), ("heightmap", "Heightmap: land > 95")]):
            ax = axes[row, col]
            image = np.asarray(Image.open(folder / f"map/{stem}.bmp"))
            ax.imshow(image[box[1]:box[3], box[0]:box[2]], extent=(box[0]-.5, box[2]-.5, box[3]-.5, box[1]-.5), interpolation="nearest", **({"cmap": "terrain", "vmin": 88, "vmax": 110} if row else {}))
            ax.add_patch(Rectangle((1533.5, 821.5), 5, 3, fill=False, edgecolor="#ffe080", linewidth=1.5, linestyle="--"))
            ax.set_title(f"{label}: {title}", color="white", loc="left", fontsize=11)
            ax.tick_params(colors="#a8bad0", labelsize=9)
            ax.set_xticks([1530, 1534, 1538, 1542])
            ax.set_yticks([816, 820, 824, 828])
    fig.text(.08, .055, "Top-left bitmap origin. Dashed box marks the new island. The row above it remains sea.", color="#b9c9dc", fontsize=10)
    fig.savefig(AUDIT / "installed_map_comparison.png", dpi=140, facecolor=fig.get_facecolor())
    plt.close(fig)


if __name__ == "__main__":
    main()
