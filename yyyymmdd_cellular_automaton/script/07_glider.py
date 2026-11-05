"""グライダーが 4 世代で斜めに 1 セル進む様子を、5 枚の盤面で示す。"""
import matplotlib.pyplot as plt

import models
import style

SIZE = 6


def main() -> None:
    style.setup()
    grid = models.place(models.GLIDER, (SIZE, SIZE), top=1, left=1)
    fig, axes = plt.subplots(1, 5, figsize=(11, 2.6))
    for generation, ax in enumerate(axes):
        style.show_cells(ax, grid, f"第 {generation} 世代")
        style.draw_grid_lines(ax, SIZE, SIZE)
        ax.set_aspect("equal")
        grid = models.life_step(grid)
    fig.tight_layout()
    style.save(fig, "07_glider.png")


if __name__ == "__main__":
    main()
