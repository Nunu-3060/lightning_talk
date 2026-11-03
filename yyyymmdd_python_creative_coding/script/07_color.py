"""同じデータを 4 種類のカラーマップで描き比べる。"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUTPUT = Path(__file__).resolve().parent.parent / "image" / "07_color.png"
N = 400
CMAPS = ["gray", "viridis", "twilight", "plasma"]


def main() -> None:
    x = np.linspace(-3, 3, N)
    xx, yy = np.meshgrid(x, x)
    r = np.hypot(xx, yy)  # 中心からの距離
    theta = np.arctan2(yy, xx)  # 中心からの角度
    data = np.sin(r * 4) * np.cos(theta * 6)  # 同心円と放射状の模様を掛け合わせる

    fig, axes = plt.subplots(1, len(CMAPS), figsize=(16, 4.2), dpi=100)
    for ax, cmap in zip(axes, CMAPS):
        ax.imshow(data, cmap=cmap)
        ax.set_title(cmap, color="white", fontsize=20)
        ax.axis("off")
    fig.savefig(OUTPUT, facecolor="black", bbox_inches="tight")


if __name__ == "__main__":
    main()
