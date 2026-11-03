"""Gray-Scott モデルの反応拡散をシミュレーションする (実行に 1 分程度かかる)。"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import laplace

OUTPUT = Path(__file__).resolve().parent.parent / "image" / "06_reaction_diffusion.png"
N = 256
STEPS = 10000
DU, DV = 0.16, 0.08  # 物質 u, v の拡散係数
F, K = 0.060, 0.062  # u の供給率、v の除去率


def main() -> None:
    u = np.ones((N, N))
    v = np.zeros((N, N))
    rng = np.random.default_rng(1)
    for _ in range(20):  # v の種をランダムな位置に置く
        x, y = rng.integers(10, N - 10, 2)
        u[y - 5:y + 5, x - 5:x + 5] = 0.50
        v[y - 5:y + 5, x - 5:x + 5] = 0.25

    for _ in range(STEPS):
        uvv = u * v * v  # 反応: u が v に変わる量
        u += DU * laplace(u, mode="wrap") - uvv + F * (1 - u)
        v += DV * laplace(v, mode="wrap") + uvv - (F + K) * v

    plt.imsave(OUTPUT, v, cmap="viridis")


if __name__ == "__main__":
    main()
