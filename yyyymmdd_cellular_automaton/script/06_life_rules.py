"""ライフゲームの規則を、周囲 8 セルの例と次の世代の状態で図にする。

規則は「周りが 3 個なら誕生、2〜3 個なら生存、それ以外は死」の 2 行だけである。
各例の左が今の 3 × 3 のセル (枠で囲んだ中央が注目するセル)、右が次の世代の中央のセルである。
"""
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.patches import Rectangle

import style

EDGE_COLOR = "#546e7a"

# (見出し, 今の 3 × 3 (O が生きたセル), 次の世代の中央の状態)
CASES = [
    ("誕生：周りが 3 個", ["O.O", "...", ".O."], 1),
    ("生存：周りが 2〜3 個", ["O..", ".O.", "..O"], 1),
    ("過疎：周りが 1 個以下", ["...", ".O.", "..O"], 0),
    ("過密：周りが 4 個以上", ["OO.", ".OO", "O.."], 0),
]


def cell(ax: Axes, x: float, y: float, alive: bool, edge: str = EDGE_COLOR, width: float = 2) -> None:
    """左上の座標が (x, y) のセルを描く (y は下向きに増える)。"""
    color = style.ON_COLOR if alive else style.OFF_COLOR
    ax.add_patch(Rectangle((x, y), 1, 1, facecolor=color, edgecolor=edge, linewidth=width))


def draw_case(ax: Axes, title: str, rows: list[str], center_next: int) -> None:
    """今の 3 × 3 と、次の世代の中央のセルを左右に並べて描く。"""
    for i, row in enumerate(rows):
        for j, char in enumerate(row):
            cell(ax, j, i, char == "O")
    cell(ax, 1, 1, rows[1][1] == "O", edge=style.ACCENT_COLOR, width=4)
    ax.annotate("", xy=(4.6, 1.5), xytext=(3.3, 1.5),
                arrowprops={"arrowstyle": "-|>", "color": style.TEXT_COLOR, "linewidth": 2})
    cell(ax, 5, 1, bool(center_next), edge=style.ACCENT_COLOR, width=4)
    ax.text(6.4, 1.5, "生" if center_next else "死", color=style.TEXT_COLOR, ha="left", va="center", fontsize=24)
    ax.set_xlim(-0.2, 7.5)
    ax.set_ylim(3.2, -0.2)
    ax.set_aspect("equal")
    ax.set_axis_off()
    ax.set_title(title, color=style.TEXT_COLOR, fontsize=24)


def main() -> None:
    style.setup()
    fig, axes = plt.subplots(2, 2, figsize=(11, 5.6))
    for ax, (title, rows, center_next) in zip(axes.flat, CASES):
        draw_case(ax, title, rows, center_next)
    fig.tight_layout()
    style.save(fig, "06_life_rules.png")


if __name__ == "__main__":
    main()
