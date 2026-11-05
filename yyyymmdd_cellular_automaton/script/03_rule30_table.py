"""ルール 30 の局所規則 (8 通りの近傍と、それぞれの次の状態) を図にする。

8 通りの近傍を 111 から 000 の順に並べ、次の状態を並べた 8 桁の 2 進数がルール番号になることを示す。
"""
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.patches import Rectangle

import models
import style

RULE = 30
EDGE_COLOR = "#546e7a"


def cell(ax: Axes, x: float, y: float, state: int) -> None:
    """左下の座標が (x, y) のセルを、状態に応じた色で描く。"""
    color = style.ON_COLOR if state else style.OFF_COLOR
    ax.add_patch(Rectangle((x, y), 1, 1, facecolor=color, edgecolor=EDGE_COLOR, linewidth=2))


def main() -> None:
    style.setup()
    table = models.rule_table(RULE)
    fig, ax = plt.subplots(figsize=(12, 3.6))
    for k, number in enumerate(range(7, -1, -1)):
        left, center, right = (number >> 2) & 1, (number >> 1) & 1, number & 1
        x0 = k * 4.2
        for i, state in enumerate((left, center, right)):
            cell(ax, x0 + i, 2, state)
        cell(ax, x0 + 1, 0.5, int(table[number]))
        ax.text(x0 + 1.5, -0.4, str(table[number]), color=style.ACCENT_COLOR, ha="center", va="center",
                fontsize=26, fontweight="bold")
    ax.set_xlim(-0.5, 7 * 4.2 + 3.5)
    ax.set_ylim(-1.0, 3.2)
    ax.set_aspect("equal")
    ax.set_axis_off()
    fig.tight_layout()
    style.save(fig, "03_rule30_table.png")


if __name__ == "__main__":
    main()
