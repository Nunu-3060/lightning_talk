"""流体解析の結果を図にする例として、条件違いの 3 ケースの流速分布を 1 枚ずつ出力する。

題材は平行平板間の流れ (ポアズイユ流れ)。速度分布の理論解は u(y) = G / (2 mu) * y * (H - y) である。
ここで G は圧力勾配の大きさ、mu は粘度、H は平板の間隔である。
「解析結果」は、この速度分布を差分法で解いたものである。
実在する製品の出力ではなく、説明のために作った例である。

同じ関数で 3 ケースを描くので、図の体裁 (軸の範囲・色・文字の大きさ) はすべて同じになる。
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt

from common import ACCENT_COLOR, IMAGE_DIR, TEXT_COLOR, setup_matplotlib, style_axes

HEIGHT = 1.0  # 平板の間隔 H
VISCOSITY = 1.0  # 粘度 mu
GRID_POINTS = 11  # 差分法の格子点の数 (両端の壁を含む)
PRESSURE_GRADIENTS = (4.0, 8.0, 12.0)  # ケースごとの圧力勾配の大きさ G
VELOCITY_MAX = 1.6  # 横軸 (流速) の上限。全ケースで揃える

FloatArray = npt.NDArray[np.float64]


def output_path(case_number: int) -> Path:
    """ケース番号 (1 始まり) に対応する出力先を返す。"""
    return IMAGE_DIR / f"02_flow_case_{case_number}.png"


def theory(y: FloatArray, pressure_gradient: float) -> FloatArray:
    """速度分布の理論解を返す。"""
    return pressure_gradient / (2.0 * VISCOSITY) * y * (HEIGHT - y)


def solve_by_finite_difference(pressure_gradient: float) -> tuple[FloatArray, FloatArray]:
    """mu * d2u/dy2 = -G を、両端の壁で u = 0 として 2 次精度の中心差分で解く。"""
    y = np.linspace(0.0, HEIGHT, GRID_POINTS)
    dy = y[1] - y[0]
    interior = GRID_POINTS - 2

    # 内部の格子点についての連立一次方程式 A u = b を組み立てる
    matrix = (np.diag(np.full(interior, -2.0))
              + np.diag(np.ones(interior - 1), 1)
              + np.diag(np.ones(interior - 1), -1))
    rhs = np.full(interior, -pressure_gradient / VISCOSITY * dy**2)

    u = np.zeros(GRID_POINTS)
    u[1:-1] = np.linalg.solve(matrix, rhs)
    return y, u


def draw_case(case_number: int, pressure_gradient: float) -> None:
    """1 ケース分の流速分布を、解析結果 (点) と理論解 (線) を重ねて出力する。"""
    fig, ax = plt.subplots(figsize=(6.0, 4.8))

    y_fine = np.linspace(0.0, HEIGHT, 200)
    ax.plot(theory(y_fine, pressure_gradient), y_fine, color=TEXT_COLOR, linewidth=2.0, label="理論解")

    y, u = solve_by_finite_difference(pressure_gradient)
    ax.plot(u, y, "o", color=ACCENT_COLOR, markersize=9, label="解析結果")

    ax.set_title(f"ケース {case_number} (G = {pressure_gradient:g})")
    ax.set_xlabel("流速")
    ax.set_ylabel("平板間の位置")
    ax.set_xlim(0.0, VELOCITY_MAX)
    ax.set_ylim(0.0, HEIGHT)
    style_axes(ax)

    legend = ax.legend(loc="lower right", frameon=False, fontsize=16)
    for text in legend.get_texts():
        text.set_color(TEXT_COLOR)

    fig.tight_layout()
    fig.savefig(output_path(case_number), transparent=True, dpi=100)
    plt.close(fig)


def main() -> None:
    setup_matplotlib()
    for case_number, pressure_gradient in enumerate(PRESSURE_GRADIENTS, start=1):
        draw_case(case_number, pressure_gradient)


if __name__ == "__main__":
    main()
