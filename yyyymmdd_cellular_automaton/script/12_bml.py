"""BML 交通モデルの盤面 (密度 0.3 と 0.5) と、密度ごとの移動率のグラフを並べる。

盤面は 128 × 128 で、1000 ステップ後の様子を描く。青は北 (上) へ、橙は東 (右) へ進む車である。
移動率は、最後の 50 ステップで 1 ステップに動いた車の割合の平均である。
"""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.colors import ListedColormap

import models
import style

SIZE = 128
STEPS = 1000
AVERAGE_STEPS = 50
CAR_CMAP = ListedColormap([style.OFF_COLOR, style.ACCENT_COLOR, style.SUB_COLOR])


def run(density: float) -> tuple[np.typing.NDArray[np.uint8], float]:
    """STEPS ステップ進めた盤面と、最後の AVERAGE_STEPS ステップの平均の移動率を返す。"""
    lattice = models.bml_initial(SIZE, density, seed=1)
    n_cars = int((lattice != models.EMPTY).sum())
    rates: list[float] = []
    for t in range(STEPS):
        lattice, moved = models.bml_step(lattice)
        if t >= STEPS - AVERAGE_STEPS:
            rates.append(moved / n_cars)
    return lattice, float(np.mean(rates))


def draw_lattice(ax: Axes, density: float, label: str) -> None:
    """盤面を 3 色 (空き・北向き・東向き) で描く。"""
    lattice, _ = run(density)
    ax.imshow(lattice, cmap=CAR_CMAP, vmin=0, vmax=2, interpolation="nearest")
    ax.set_axis_off()
    ax.set_title(f"密度 {density}：{label}", color=style.TEXT_COLOR, fontsize=22)


def draw_rate(ax: Axes) -> None:
    """密度と移動率の関係を折れ線グラフにする。"""
    densities = np.round(np.arange(0.1, 0.61, 0.05), 2)
    rates = [run(float(d))[1] for d in densities]
    ax.plot(densities, rates, marker="o", color=style.ON_COLOR, linewidth=2)
    ax.set_xlabel("密度", color=style.TEXT_COLOR, fontsize=20)
    ax.set_ylabel("移動率", color=style.TEXT_COLOR, fontsize=20)
    ax.set_ylim(-0.05, 1.05)
    ax.tick_params(colors=style.TEXT_COLOR, labelsize=16)
    for side in ["top", "right"]:
        ax.spines[side].set_visible(False)
    for side in ["left", "bottom"]:
        ax.spines[side].set_color(style.TEXT_COLOR)
    ax.set_title("密度と移動率", color=style.TEXT_COLOR, fontsize=22)
    ax.set_box_aspect(1)


def main() -> None:
    style.setup()
    fig, axes = plt.subplots(1, 3, figsize=(12.5, 4.6))
    draw_lattice(axes[0], 0.3, "流れ続ける")
    draw_lattice(axes[1], 0.5, "全体が止まる")
    draw_rate(axes[2])
    fig.tight_layout()
    style.save(fig, "12_bml.png")


if __name__ == "__main__":
    main()
