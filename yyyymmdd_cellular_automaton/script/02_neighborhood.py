"""1 次元と 2 次元のセル・オートマトンの「近傍」を図にする。

自分 (中央) の次の状態は、自分と近傍のセルの今の状態だけで決まることを示す。
"""
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.patches import FancyArrowPatch, Rectangle

import style

EDGE_COLOR = "#546e7a"


def cell(ax: Axes, x: float, y: float, color: str) -> None:
    """左下の座標が (x, y) の 1 × 1 のセルを描く。"""
    ax.add_patch(Rectangle((x, y), 1, 1, facecolor=color, edgecolor=EDGE_COLOR, linewidth=2))


def draw_1d(ax: Axes) -> None:
    """1 行のセルと、その 1 時刻後の中央のセルを描く。"""
    for x in range(7):
        color = style.OFF_COLOR
        if x == 3:
            color = style.ACCENT_COLOR
        elif x in (2, 4):
            color = style.SUB_COLOR
        cell(ax, x, 2, color)
    cell(ax, 3, 0, style.ACCENT_COLOR)
    ax.add_patch(FancyArrowPatch((3.5, 1.95), (3.5, 1.05), arrowstyle="-|>", mutation_scale=25,
                                 color=style.TEXT_COLOR, linewidth=2))
    ax.text(-0.3, 2.5, "今", color=style.TEXT_COLOR, ha="right", va="center", fontsize=24)
    ax.text(-0.3, 0.5, "次", color=style.TEXT_COLOR, ha="right", va="center", fontsize=24)
    ax.set_xlim(-1.5, 7.5)
    ax.set_ylim(-0.5, 3.5)
    ax.set_title("1 次元：左右の 2 セル", color=style.TEXT_COLOR, fontsize=26)


def draw_2d(ax: Axes) -> None:
    """5 × 5 の盤面で、中央のセルと周囲 8 セルを描く。"""
    for x in range(5):
        for y in range(5):
            color = style.OFF_COLOR
            if (x, y) == (2, 2):
                color = style.ACCENT_COLOR
            elif abs(x - 2) <= 1 and abs(y - 2) <= 1:
                color = style.SUB_COLOR
            cell(ax, x, y, color)
    ax.set_xlim(-0.5, 5.5)
    ax.set_ylim(-0.5, 5.5)
    ax.set_title("2 次元：周囲の 8 セル", color=style.TEXT_COLOR, fontsize=26)


def main() -> None:
    style.setup()
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.4), gridspec_kw={"width_ratios": [1.6, 1]})
    draw_1d(axes[0])
    draw_2d(axes[1])
    for ax in axes:
        ax.set_aspect("equal")
        ax.set_axis_off()
    fig.tight_layout()
    style.save(fig, "02_neighborhood.png")


if __name__ == "__main__":
    main()
