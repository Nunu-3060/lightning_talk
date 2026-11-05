"""ウルフラムの 4 クラスの例を、同じランダムな初期配置から計算した時空図で示す。

規則はセル・オートマトンの理論と歴史 (sphinx_docs) の図と同じものを使う。
"""
import matplotlib.pyplot as plt

import models
import style

WIDTH = 121
STEPS = 100
CLASSES = [
    (160, "一様になる"),
    (108, "周期的になる"),
    (45, "乱雑になる"),
    (110, "複雑な構造"),
]


def main() -> None:
    style.setup()
    initial = models.random_cells(WIDTH, density=0.5, seed=11)
    fig, axes = plt.subplots(1, 4, figsize=(12, 4.3))
    for ax, (rule, label) in zip(axes, CLASSES):
        style.show_cells(ax, models.eca_evolve(rule, initial, STEPS), f"{label}\nルール {rule}")
        ax.set_box_aspect(STEPS / WIDTH)
    fig.tight_layout()
    style.save(fig, "04_wolfram_classes.png")


if __name__ == "__main__":
    main()
