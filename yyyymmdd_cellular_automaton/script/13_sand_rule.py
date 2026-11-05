"""飛砂のモデルの輸送の規則 (高い所ほど砂を遠くへ飛ばす) を、1 列の砂の高さで模式的に示す。

風は右から左へ吹き、砂は左 (風下) へ飛ぶ。飛距離は round(2 + 4 × 高さ) セルである。
低いセルと高いセルから 1 本ずつ、砂が飛ぶ様子を矢印で描く。
"""
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.patches import FancyArrowPatch

import style

HEIGHTS = [0.35, 0.5, 0.4, 0.55, 0.45, 0.3, 0.5, 0.25, 0.6, 0.85, 0.5, 0.4]
SAND_COLOR = "#d7b98e"
LOW_CELL = 7  # 高さ 0.25 → 3 セル飛ぶ
HIGH_CELL = 9  # 高さ 0.85 → 5 セル飛ぶ


def hop(ax: Axes, start: int, color: str, rad: float) -> int:
    """セル start から、高さに応じた飛距離だけ左へ飛ぶ弧の矢印を描き、着地するセルを返す。"""
    end = start - round(2 + 4 * HEIGHTS[start])
    ax.add_patch(FancyArrowPatch((start, HEIGHTS[start] + 0.03), (end + 0.15, HEIGHTS[end] + 0.03),
                                 connectionstyle=f"arc3,rad={rad}", arrowstyle="-|>", mutation_scale=30,
                                 color=color, linewidth=4))
    return end


def main() -> None:
    style.setup()
    fig, ax = plt.subplots(figsize=(10, 3.6))
    ax.bar(range(len(HEIGHTS)), HEIGHTS, width=0.9, color=SAND_COLOR)
    hop(ax, LOW_CELL, style.ACCENT_COLOR, rad=0.6)
    hop(ax, HIGH_CELL, style.SUB_COLOR, rad=0.5)
    ax.text(LOW_CELL - 1.5, -0.2, "低い所：近くへ", color=style.ACCENT_COLOR, fontsize=24, va="center", ha="center")
    ax.text(HIGH_CELL + 0.6, 1.0, "高い所：遠くへ", color=style.SUB_COLOR, fontsize=24, va="center")
    ax.annotate("", xy=(0.5, 1.45), xytext=(3.5, 1.45),
                arrowprops={"arrowstyle": "-|>", "color": style.TEXT_COLOR, "linewidth": 3, "mutation_scale": 30})
    ax.text(3.7, 1.45, "風", color=style.TEXT_COLOR, va="center", fontsize=24)
    ax.set_xlim(-0.8, 13.5)
    ax.set_ylim(-0.35, 1.6)
    ax.set_axis_off()
    fig.tight_layout()
    style.save(fig, "13_sand_rule.png")


if __name__ == "__main__":
    main()
