"""AI 以前と以後で、技術を扱える人の範囲が広がる様子を概念図にする。

円の大きさは概念を示すためのもので、実際の人数の比率ではない。
"""
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.patches import Circle

OUTPUT = Path(__file__).resolve().parent.parent / "image" / "02_who_can_build.png"

TEXT_COLOR = "#fff8e1"  # gaia テーマの invert の文字色に合わせる
EXPERT_COLOR = "#0277bd"  # 仕組みを理解して技術を扱う人
USER_COLOR = "#ef6c00"  # 仕組みを理解しなくても技術を扱える人

SOCIETY_RADIUS = 1.0
EXPERT_RADIUS = 0.3
AI_USER_RADIUS = 0.82


def draw_panel(ax: Axes, title: str, with_ai: bool) -> None:
    """社会全体を表す円の中に、技術を扱える人の範囲を描く。"""
    ax.add_patch(Circle((0, 0), SOCIETY_RADIUS, fill=False, edgecolor=TEXT_COLOR, linewidth=2))
    ax.text(0, SOCIETY_RADIUS + 0.06, "社会", color=TEXT_COLOR, fontsize=24, ha="center", va="bottom")

    if with_ai:
        ax.add_patch(Circle((0, -0.12), AI_USER_RADIUS, color=USER_COLOR, alpha=0.55))
        ax.text(0, -0.55, "理解しなくても\n扱える人", color=TEXT_COLOR, fontsize=24, ha="center", va="center")

    ax.add_patch(Circle((0, 0.3), EXPERT_RADIUS, color=EXPERT_COLOR))
    ax.text(0, 0.3, "技術者", color=TEXT_COLOR, fontsize=22, ha="center", va="center")

    ax.text(0, SOCIETY_RADIUS + 0.3, title, color=TEXT_COLOR, fontsize=30, ha="center", va="bottom")
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.05, 1.65)
    ax.set_aspect("equal")
    ax.axis("off")


def main() -> None:
    plt.rcParams["font.family"] = "Yu Gothic"
    fig, (ax_before, ax_after) = plt.subplots(1, 2, figsize=(8, 4.8))
    draw_panel(ax_before, "AI 以前", with_ai=False)
    draw_panel(ax_after, "AI 以後", with_ai=True)
    fig.tight_layout()
    fig.savefig(OUTPUT, transparent=True, dpi=100)


if __name__ == "__main__":
    main()
