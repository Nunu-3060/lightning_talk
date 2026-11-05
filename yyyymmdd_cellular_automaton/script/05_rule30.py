"""中央の 1 セルから始めたルール 30 の時空図を描き、中央の列を強調する。

中央の列の 0・1 の並びは、統計的な乱数検定を通過するほど不規則である。
"""
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

import models
import style

WIDTH = 241
STEPS = 120


def main() -> None:
    style.setup()
    history = models.eca_evolve(30, models.single_seed(WIDTH), STEPS)
    fig, ax = plt.subplots(figsize=(11, 5.6))
    style.show_cells(ax, history)
    ax.set_aspect("equal")
    center = WIDTH // 2
    ax.add_patch(Rectangle((center - 0.5, -0.5), 1, STEPS + 1, fill=False, edgecolor=style.ACCENT_COLOR, linewidth=2))
    ax.annotate("中央の列", xy=(center, STEPS * 0.2), xytext=(center + 50, STEPS * 0.2),
                color=style.ACCENT_COLOR, fontsize=24, va="center",
                arrowprops={"arrowstyle": "-|>", "color": style.ACCENT_COLOR, "linewidth": 2},
                bbox={"boxstyle": "round", "facecolor": style.OFF_COLOR, "edgecolor": style.ACCENT_COLOR})
    fig.tight_layout()
    style.save(fig, "05_rule30.png")


if __name__ == "__main__":
    main()
