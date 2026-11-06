"""手作業と自動化の累計の手間を比べ、自動化が得になる回数 (損益分岐) を示す模式図を出力する。

手作業は 1 回ごとに同じ手間がかかる。
自動化は最初にスクリプトを書く手間がかかるが、1 回ごとの手間は小さい。
数値は説明のための例である。
"""
import matplotlib.pyplot as plt
import numpy as np

from common import ACCENT_COLOR, IMAGE_DIR, TEXT_COLOR, WARNING_COLOR, setup_matplotlib, style_axes

OUTPUT = IMAGE_DIR / "08_break_even.png"

MANUAL_COST_PER_RUN = 30.0  # 手作業 1 回の手間 [分]
SCRIPT_WRITING_COST = 300.0  # スクリプトを書く手間 [分]
SCRIPT_COST_PER_RUN = 2.0  # 自動化後の 1 回の手間 [分]
MAX_RUNS = 20


def main() -> None:
    setup_matplotlib()
    fig, ax = plt.subplots(figsize=(10.0, 4.4))

    runs = np.arange(0, MAX_RUNS + 1)
    manual = MANUAL_COST_PER_RUN * runs
    automated = SCRIPT_WRITING_COST + SCRIPT_COST_PER_RUN * runs
    ax.plot(runs, manual, color=WARNING_COLOR, linewidth=3, label="手作業")
    ax.plot(runs, automated, color=ACCENT_COLOR, linewidth=3, label="自動化")

    # 2 本の直線の交点が損益分岐
    break_even = SCRIPT_WRITING_COST / (MANUAL_COST_PER_RUN - SCRIPT_COST_PER_RUN)
    ax.axvline(break_even, color=TEXT_COLOR, linestyle="--", linewidth=1.5)
    ax.text(break_even + 0.3, 30, f"損益分岐\n(約 {break_even:.0f} 回)", color=TEXT_COLOR, va="bottom")

    ax.set_xticks(range(0, MAX_RUNS + 1, 5))
    ax.set_xlabel("実行する回数")
    ax.set_ylabel("累計の手間 [分]")
    ax.set_xlim(0, MAX_RUNS)
    ax.set_ylim(0, 600)
    style_axes(ax)

    legend = ax.legend(loc="upper left", frameon=False)
    for text in legend.get_texts():
        text.set_color(TEXT_COLOR)

    fig.tight_layout()
    fig.savefig(OUTPUT, transparent=True, dpi=100)


if __name__ == "__main__":
    main()
