"""ルール 184 (前が空いていれば進む) の時空図を、密度 0.3 と 0.7 で比べる。

1 が車、0 が空きで、車は右へ進む。下へ行くほど時間が進む。
密度が 1/2 以下なら渋滞は消え、1/2 を超えると渋滞が残って左 (後ろ) へ移動していく。
"""
import matplotlib.pyplot as plt

import models
import style

WIDTH = 100
STEPS = 70


def main() -> None:
    style.setup()
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.6))
    for ax, density, label in zip(axes, [0.3, 0.7], ["渋滞が消える", "渋滞が残る"]):
        history = models.eca_evolve(184, models.random_cells(WIDTH, density, seed=5), STEPS)
        style.show_cells(ax, history, f"密度 {density}：{label}")
        ax.set_aspect("equal")
    fig.tight_layout()
    style.save(fig, "10_rule184.png")


if __name__ == "__main__":
    main()
