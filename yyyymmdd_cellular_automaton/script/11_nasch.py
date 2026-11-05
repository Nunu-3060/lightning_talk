"""ナーゲル・シュレッケンベルク・モデルの時空図を、密度 0.1 と 0.3 で比べる。

最高速度 5、ランダムな減速の確率 0.25 とする。車は右へ進み、下へ行くほど時間が進む。
密度が高いと、ランダムな減速をきっかけに渋滞 (黒っぽい帯) が生まれ、左 (後ろ) へ伝わる。
"""
import matplotlib.pyplot as plt

import models
import style

LENGTH = 120
STEPS = 120


def main() -> None:
    style.setup()
    fig, axes = plt.subplots(1, 2, figsize=(11, 5.0))
    for ax, density, label in zip(axes, [0.1, 0.3], ["流れる", "渋滞が生まれる"]):
        history = models.nasch_evolve(LENGTH, density, v_max=5, p=0.25, steps=STEPS, seed=2)
        style.show_cells(ax, history, f"密度 {density}：{label}")
        ax.set_aspect("equal")
    fig.tight_layout()
    style.save(fig, "11_nasch.png")


if __name__ == "__main__":
    main()
