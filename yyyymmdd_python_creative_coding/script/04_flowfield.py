"""滑らかなノイズを角度とみなしたベクトル場 (フローフィールド) に粒子を流す。"""
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter

OUTPUT = Path(__file__).resolve().parent.parent / "image" / "04_flowfield.png"
N = 200  # 場の大きさ
PARTICLES = 1500
STEPS = 60


def main() -> None:
    rng = np.random.default_rng(0)
    noise = gaussian_filter(rng.random((N, N)), sigma=12)  # ぼかして滑らかなノイズにする
    noise = (noise - noise.min()) / (noise.max() - noise.min())
    angle = noise * 4 * np.pi  # ノイズの値を進む向きに変換する
    cmap = matplotlib.colormaps["cool"]

    fig, ax = plt.subplots(figsize=(8, 8), dpi=100)
    for _ in range(PARTICLES):
        x, y = rng.uniform(0, N, 2)
        xs, ys = [x], [y]
        for _ in range(STEPS):
            a = angle[int(y) % N, int(x) % N]
            x, y = x + np.cos(a), y + np.sin(a)  # 場の向きに 1 歩進む
            xs.append(x)
            ys.append(y)
        ax.plot(xs, ys, lw=0.5, alpha=0.6, color=cmap(xs[0] / N))

    ax.set_xlim(0, N)
    ax.set_ylim(0, N)
    ax.axis("off")
    fig.savefig(OUTPUT, facecolor="black", bbox_inches="tight", pad_inches=0)


if __name__ == "__main__":
    main()
