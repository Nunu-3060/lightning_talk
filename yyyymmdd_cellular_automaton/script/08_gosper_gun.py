"""ゴスパーのグライダー銃を 120 世代進めた盤面を描く。

銃は 30 世代ごとにグライダーを 1 つ放出するので、右下へ並んだグライダーの列ができる。
周期境界条件で一周したグライダーが銃に戻らないよう、盤面を十分に広くしている。
"""
import matplotlib.pyplot as plt

import models
import style

GENERATIONS = 120


def main() -> None:
    style.setup()
    grid = models.place(models.GOSPER_GLIDER_GUN, (40, 90), top=1, left=1)
    for _ in range(GENERATIONS):
        grid = models.life_step(grid)
    fig, ax = plt.subplots(figsize=(11, 4.9))
    style.show_cells(ax, grid)
    ax.set_aspect("equal")
    ax.annotate("銃", xy=(19, 6), xytext=(19, 22), color=style.ACCENT_COLOR, fontsize=28, ha="center",
                arrowprops={"arrowstyle": "-|>", "color": style.ACCENT_COLOR, "linewidth": 2})
    ax.annotate("放出されたグライダー", xy=(28, 22), xytext=(55, 30), color=style.ACCENT_COLOR,
                fontsize=28, va="center",
                arrowprops={"arrowstyle": "-|>", "color": style.ACCENT_COLOR, "linewidth": 2})
    fig.tight_layout()
    style.save(fig, "08_gosper_gun.png")


if __name__ == "__main__":
    main()
