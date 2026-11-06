"""テスト結果をバージョンごとに並べ、変化に気付きやすくなることを示す図を出力する。

縦軸は、ある解析ケースの結果と基準値 (理論解など) との相対誤差である。
許容値を超えたバージョンを別の色で示す。
数値は説明のために作った例で、実在する製品の結果ではない。
"""
import matplotlib.pyplot as plt

from common import ACCENT_COLOR, IMAGE_DIR, TEXT_COLOR, WARNING_COLOR, setup_matplotlib, style_axes

OUTPUT = IMAGE_DIR / "05_test_trend.png"

VERSIONS = ["1.0", "1.1", "1.2", "1.3", "1.4", "1.5", "1.6", "1.7", "1.8"]
RELATIVE_ERRORS = [0.31, 0.30, 0.32, 0.29, 0.30, 0.31, 1.85, 0.30, 0.29]  # 基準値との相対誤差 [%]
TOLERANCE = 1.0  # 許容値 [%]


def main() -> None:
    setup_matplotlib()
    fig, ax = plt.subplots(figsize=(10.0, 4.4))

    positions = list(range(len(VERSIONS)))
    ax.plot(positions, RELATIVE_ERRORS, color=TEXT_COLOR, linewidth=1.5, zorder=1)

    colors = [WARNING_COLOR if error > TOLERANCE else ACCENT_COLOR for error in RELATIVE_ERRORS]
    ax.scatter(positions, RELATIVE_ERRORS, c=colors, s=140, zorder=2)

    ax.axhline(TOLERANCE, color=WARNING_COLOR, linestyle="--", linewidth=2)
    ax.text(len(VERSIONS) - 1, TOLERANCE + 0.07, "許容値", color=WARNING_COLOR, ha="right", va="bottom")

    worst = RELATIVE_ERRORS.index(max(RELATIVE_ERRORS))
    ax.annotate("ここで変わった", xy=(worst, RELATIVE_ERRORS[worst]), xytext=(worst - 3.2, 1.6),
                color=WARNING_COLOR, arrowprops={"arrowstyle": "->", "color": WARNING_COLOR, "linewidth": 2})

    ax.set_xticks(positions, VERSIONS)
    ax.set_xlabel("バージョン")
    ax.set_ylabel("基準値との誤差 [%]")
    ax.set_ylim(0.0, 2.2)
    style_axes(ax)

    fig.tight_layout()
    fig.savefig(OUTPUT, transparent=True, dpi=100)


if __name__ == "__main__":
    main()
