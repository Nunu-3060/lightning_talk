from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def main() -> None:
    # config
    fp: Path = Path(__file__).resolve().with_suffix(".png")
    plt.rcParams["figure.dpi"] = 100
    plt.rcParams["figure.figsize"] = [19.2, 10.8]
    c0: str = "#ff6347"
    c1: str = "#fffacd"
    c2: str = "#a52a2a"
    # generate figure
    fig: plt.Figure
    ax: plt.Axes
    fig, ax = plt.subplots()
    # plot
    n: int = 5
    t: np.ndarray = np.linspace(0, 2*np.pi, 10001, endpoint=True)
    c: np.ndarray = np.cos(t)
    s: np.ndarray = np.sin(t)
    l: float = 1/np.sqrt(1-2*np.sin(np.pi/n)*np.sin(np.pi/n))
    r: float = np.sqrt(l*l-1)
    for i in range(n):
        y: float = l*np.cos(2*np.pi/n*i)+r*c
        x: float = l*np.sin(2*np.pi/n*i)+r*s
        p: np.ndarray = np.array([[k, l] for k, l in zip(x, y) if k*k+l*l < 1])
        p = p.T
        ax.plot(p[0], p[1], color=c1, marker="o", linestyle="", markersize=54)
    ax.plot(c, s, color=c2, linewidth=60)
    # arrange
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    ax.axis("off")
    ax.set_aspect("equal")
    ax.set_facecolor(c0)
    fig.set_facecolor(c0)
    fig.tight_layout()
    # output
    fig.savefig(fp)
    plt.cla()
    plt.clf()
    plt.close(fig)
    return None


if __name__ == "__main__":
    main()
