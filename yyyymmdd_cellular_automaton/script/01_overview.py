"""表紙の次に見せる 3 枚組の図 (ライフゲーム・交通渋滞・風紋) を作る。

3 つとも、この後の章で説明する数行の規則だけから生まれた模様である。
"""
import matplotlib.pyplot as plt

import models
import style


def main() -> None:
    style.setup()
    fig, axes = plt.subplots(1, 3, figsize=(12, 4.4))

    # 生命: ランダムな初期配置からライフゲームを 100 世代進める
    grid = models.random_cells(100 * 100, density=0.35, seed=7).reshape(100, 100)
    for _ in range(100):
        grid = models.life_step(grid)
    style.show_cells(axes[0], grid, "生命 (ライフゲーム)")

    # 交通渋滞: ナーゲル・シュレッケンベルク・モデルの時空図 (横が位置、下へ時間が進む)
    road = models.nasch_evolve(length=200, density=0.25, v_max=5, p=0.25, steps=200, seed=2)
    style.show_cells(axes[1], road, "交通渋滞")

    # 風紋: 飛砂のモデルを 300 ステップ進める
    height = models.sand_initial(128, seed=1)
    for _ in range(300):
        height = models.sand_step(height)
    axes[2].imshow(style.shade_sand(height), interpolation="bilinear")
    axes[2].set_axis_off()
    axes[2].set_title("風紋", color=style.TEXT_COLOR, fontsize=22)

    for ax in axes:
        ax.set_box_aspect(1)
    fig.tight_layout()
    style.save(fig, "01_overview.png")


if __name__ == "__main__":
    main()
