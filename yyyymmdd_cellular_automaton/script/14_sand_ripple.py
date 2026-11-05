"""飛砂のモデルで、乱雑な初期状態から風紋が現れる様子を 3 つの時点で示す。

128 × 128 の格子で、0・20・1000 ステップ後の砂の高さを、左上から光を当てた砂色で描く。
風は右から左へ吹いている。
"""
import matplotlib.pyplot as plt

import models
import style

SNAPSHOTS = [0, 20, 1000]


def main() -> None:
    style.setup()
    fig, axes = plt.subplots(1, 3, figsize=(12, 4.6))
    height = models.sand_initial(128, seed=1)
    step = 0
    for ax, target in zip(axes, SNAPSHOTS):
        while step < target:
            height = models.sand_step(height)
            step += 1
        ax.imshow(style.shade_sand(height), interpolation="bilinear")
        ax.set_axis_off()
        ax.set_title(f"{target} ステップ", color=style.TEXT_COLOR, fontsize=24)
    fig.tight_layout()
    style.save(fig, "14_sand_ripple.png")


if __name__ == "__main__":
    main()
