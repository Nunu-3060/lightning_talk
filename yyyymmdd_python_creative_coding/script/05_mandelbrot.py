"""マンデルブロ集合を numpy の配列演算で全画素まとめて計算する。"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUTPUT = Path(__file__).resolve().parent.parent / "image" / "05_mandelbrot.png"
SIZE = 800
MAX_ITER = 100


def main() -> None:
    x = np.linspace(-2.0, 0.6, SIZE)
    y = np.linspace(-1.3, 1.3, SIZE)
    c = x[np.newaxis, :] + 1j * y[:, np.newaxis]  # 全画素に対応する複素数
    z = np.zeros_like(c)
    count = np.zeros(c.shape, dtype=np.int64)  # 発散するまでの反復回数

    for _ in range(MAX_ITER):
        alive = np.abs(z) <= 2  # まだ発散していない画素
        z[alive] = z[alive] ** 2 + c[alive]
        count[alive] += 1

    plt.imsave(OUTPUT, np.log(count), cmap="magma")


if __name__ == "__main__":
    main()
