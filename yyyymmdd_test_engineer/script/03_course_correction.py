"""開発の進路が目標から逸れかけ、テスト結果を基に軌道修正される様子を模式図にする。

座標や曲線の形は概念を示すためのもので、何かを計測した値ではない。
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt

OUTPUT = Path(__file__).resolve().parent.parent / "image" / "03_course_correction.png"

TEXT_COLOR = "#fff8e1"  # gaia テーマの invert の文字色に合わせる
PATH_COLOR = "#4fc3f7"  # 実際の進路
TEST_COLOR = "#ffb74d"  # テストで軌道修正した点
DRIFT_COLOR = "#9e9e9e"  # 修正しなかった場合の進路

START = (0.0, 0.0)
GOAL = (10.0, 0.0)
# 進路が通る点。2 番目の山と 4 番目の谷が、テスト結果を基に軌道修正した点である。
WAYPOINTS = np.array([START, (1.6, 0.35), (3.3, 1.25), (5.0, 0.2), (6.7, -0.95), (8.4, -0.25), GOAL])
CORRECTION_INDICES = (2, 4)
SAMPLES_PER_SEGMENT = 30

FloatArray = npt.NDArray[np.float64]


def catmull_rom(points: FloatArray, samples: int) -> FloatArray:
    """与えた点をすべて滑らかに通る曲線 (Catmull-Rom スプライン) の座標を返す。"""
    padded = np.vstack([points[0], points, points[-1]])  # 両端でも曲線を描けるように端点を複製する
    t = np.linspace(0.0, 1.0, samples, endpoint=False)[:, np.newaxis]
    segments = []
    for i in range(len(points) - 1):
        p0, p1, p2, p3 = padded[i], padded[i + 1], padded[i + 2], padded[i + 3]
        segments.append(0.5 * (2 * p1
                               + (-p0 + p2) * t
                               + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t**2
                               + (-p0 + 3 * p1 - 3 * p2 + p3) * t**3))
    segments.append(points[-1][np.newaxis, :])
    return np.vstack(segments)


def main() -> None:
    plt.rcParams["font.family"] = "Yu Gothic"
    fig, ax = plt.subplots(figsize=(10, 4.2))

    # 目標へ一直線に向かう理想の進路
    ax.plot([START[0], GOAL[0]], [START[1], GOAL[1]], linestyle=":", color=TEXT_COLOR, linewidth=1.5)

    # 最初の修正点で止めなかった場合に進んでいたであろう進路
    first = WAYPOINTS[CORRECTION_INDICES[0]]
    ax.annotate("", xy=(first[0] + 2.2, first[1] + 1.1), xytext=(first[0], first[1]),
                arrowprops={"arrowstyle": "->", "color": DRIFT_COLOR, "linestyle": "--", "linewidth": 2})
    ax.text(first[0] + 2.3, first[1] + 1.0, "止めなければ\nこのまま逸れる", color=DRIFT_COLOR, fontsize=22,
            va="center")

    curve = catmull_rom(WAYPOINTS, SAMPLES_PER_SEGMENT)
    ax.plot(curve[:, 0], curve[:, 1], color=PATH_COLOR, linewidth=3.5)

    for index in CORRECTION_INDICES:
        x, y = WAYPOINTS[index]
        ax.plot(x, y, "o", color=TEST_COLOR, markersize=16)
        offset = 0.35 if y > 0 else -0.35
        ax.text(x, y + offset, "テスト結果で\n軌道修正", color=TEST_COLOR, fontsize=22, ha="center",
                va="bottom" if y > 0 else "top")

    ax.plot(*START, "o", color=TEXT_COLOR, markersize=12)
    ax.text(START[0], START[1] - 0.35, "開始", color=TEXT_COLOR, fontsize=22, ha="center", va="top")
    ax.plot(*GOAL, "*", color=TEXT_COLOR, markersize=30)
    ax.text(GOAL[0], GOAL[1] - 0.45, "妥当な到達点", color=TEXT_COLOR, fontsize=22, ha="center", va="top")

    ax.set_xlim(-0.8, 11.5)
    ax.set_ylim(-2.5, 3.0)
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(OUTPUT, transparent=True, dpi=100)


if __name__ == "__main__":
    main()
