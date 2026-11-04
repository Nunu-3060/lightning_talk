"""分野ごとの文書の冊数を横棒グラフにする。

冊数は sphinx_docs リポジトリの readme.md の一覧（2026/11/04 時点）から写した。
"""
from pathlib import Path

import matplotlib.pyplot as plt

OUTPUT = Path(__file__).resolve().parent.parent / "image" / "01_doc_counts.png"

# 分野名と冊数（readme.md の表の順）
COUNTS: dict[str, int] = {
    "計算機科学": 11,
    "数学・シミュレーション": 15,
    "プログラミング": 12,
    "ソフトウェア開発": 12,
    "AI": 3,
    "グラフィックス・アート": 14,
    "ゲーム制作": 14,
    "技術者の仕事": 9,
    "暮らし": 9,
    "嗜好品": 8,
}

TEXT_COLOR = "#fff8e1"  # gaia テーマの invert の文字色に合わせる
BAR_COLOR = "#81d4fa"


def main() -> None:
    plt.rcParams["font.family"] = "Yu Gothic"
    names = list(COUNTS)[::-1]  # 上から表の順に並ぶよう逆順にする
    values = [COUNTS[name] for name in names]

    fig, ax = plt.subplots(figsize=(10, 5.6))
    bars = ax.barh(names, values, color=BAR_COLOR)
    ax.bar_label(bars, padding=4, color=TEXT_COLOR, fontsize=14)
    ax.set_title(f"10 分野・{sum(values)} 冊", color=TEXT_COLOR, fontsize=18)
    ax.set_xlabel("冊数", color=TEXT_COLOR, fontsize=14)
    ax.set_xlim(0, max(values) + 2)
    ax.tick_params(colors=TEXT_COLOR, labelsize=14)
    for side in ["top", "right"]:
        ax.spines[side].set_visible(False)
    for side in ["left", "bottom"]:
        ax.spines[side].set_color(TEXT_COLOR)
    fig.tight_layout()
    fig.savefig(OUTPUT, transparent=True, dpi=100)


if __name__ == "__main__":
    main()
