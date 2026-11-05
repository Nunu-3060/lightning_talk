"""解析結果を理論解と比べて妥当性を判断する様子を、説明用の例で図にする。

題材は平行平板間の流れ (ポアズイユ流れ)。速度分布の理論解は u(y) = G / (2 mu) * y * (H - y) である。
ここで G は圧力勾配の大きさ、mu は粘度、H は平板の間隔である。

「旧バージョン」と「新バージョン」は、この速度分布を差分法で解いた結果である。
新バージョンは、粘度の扱いを誤った場合を模して粘度を小さくして解いている。
実在する製品の出力ではなく、説明のために作った例である。
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt

OUTPUT = Path(__file__).resolve().parent.parent / "image" / "02_compare_with_theory.png"

TEXT_COLOR = "#fff8e1"  # gaia テーマの invert の文字色に合わせる
THEORY_COLOR = TEXT_COLOR
OLD_COLOR = "#4fc3f7"
NEW_COLOR = "#ffb74d"

HEIGHT = 1.0  # 平板の間隔 H
PRESSURE_GRADIENT = 8.0  # 圧力勾配の大きさ G (最大流速が 1 になる値)
VISCOSITY = 1.0  # 粘度 mu
WRONG_VISCOSITY_RATIO = 0.8  # 新バージョンが誤って使う粘度の倍率
GRID_POINTS = 11  # 差分法の格子点の数 (両端の壁を含む)

FloatArray = npt.NDArray[np.float64]


def theory(y: FloatArray) -> FloatArray:
    """速度分布の理論解を返す。"""
    return PRESSURE_GRADIENT / (2.0 * VISCOSITY) * y * (HEIGHT - y)


def solve_by_finite_difference(viscosity: float) -> tuple[FloatArray, FloatArray]:
    """mu * d2u/dy2 = -G を、両端の壁で u = 0 として 2 次精度の中心差分で解く。"""
    y = np.linspace(0.0, HEIGHT, GRID_POINTS)
    dy = y[1] - y[0]
    interior = GRID_POINTS - 2

    # 内部の格子点についての連立一次方程式 A u = b を組み立てる
    matrix = (np.diag(np.full(interior, -2.0))
              + np.diag(np.ones(interior - 1), 1)
              + np.diag(np.ones(interior - 1), -1))
    rhs = np.full(interior, -PRESSURE_GRADIENT / viscosity * dy**2)

    u = np.zeros(GRID_POINTS)
    u[1:-1] = np.linalg.solve(matrix, rhs)
    return y, u


def main() -> None:
    plt.rcParams["font.family"] = "Yu Gothic"
    plt.rcParams["font.size"] = 20

    fig, ax = plt.subplots(figsize=(9.5, 4.6))

    y_fine = np.linspace(0.0, HEIGHT, 200)
    ax.plot(theory(y_fine), y_fine, color=THEORY_COLOR, linewidth=2.5, label="理論解")

    y_old, u_old = solve_by_finite_difference(VISCOSITY)
    ax.plot(u_old, y_old, "o", color=OLD_COLOR, markersize=10, label="旧バージョン")

    y_new, u_new = solve_by_finite_difference(VISCOSITY * WRONG_VISCOSITY_RATIO)
    ax.plot(u_new, y_new, "s", color=NEW_COLOR, markersize=10, label="新バージョン")

    ax.set_xlabel("流速")
    ax.set_ylabel("平板間の位置")
    ax.set_xlim(0.0, 1.4)
    ax.set_ylim(0.0, HEIGHT)
    for spine in ax.spines.values():
        spine.set_color(TEXT_COLOR)
    ax.tick_params(colors=TEXT_COLOR)
    ax.xaxis.label.set_color(TEXT_COLOR)
    ax.yaxis.label.set_color(TEXT_COLOR)

    legend = ax.legend(loc="upper left", bbox_to_anchor=(1.0, 1.0), frameon=False)
    for text in legend.get_texts():
        text.set_color(TEXT_COLOR)

    fig.tight_layout()
    fig.savefig(OUTPUT, transparent=True, dpi=100)


if __name__ == "__main__":
    main()
