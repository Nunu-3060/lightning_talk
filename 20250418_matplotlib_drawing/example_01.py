from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def main() -> None:
    # config
    fp: Path = Path(__file__).resolve().with_suffix(".png")
    plt.rcParams["figure.dpi"] = 100
    plt.rcParams["figure.figsize"] = [19.2, 10.8]
    c0: str = "#5B7A97"
    c1: str = "#B7EB21"
    c2: str = "#60B683"
    # generate figure
    fig: plt.Figure
    ax: plt.Axes
    fig, ax = plt.subplots()
    # plot
    n: int = 6
    t: np.ndarray = np.linspace(0, n*np.pi, n*360+1, endpoint=True)
    r: np.ndarray = 0.25/(n*np.pi)* t
    xy: np.ndarray = r  * np.array([np.cos(t), np.sin(t)])
    for i in range(16):
        for j in range(9):
            th: float = -(i+j)/(16+9) * 2*np.pi
            c: float = np.cos(th)
            s: float = np.sin(th)
            m: np.ndarray = np.array([[c, -s], [s, c]])
            p: np.ndarray = m @ xy
            ax.plot(p[0]+i, p[1]+j, color=c1, linewidth=4)
    xy: np.ndarray = r  * np.array([np.cos(t), -np.sin(t)])
    for i in range(15):
        for j in range(8):
            th: float = (i+j+0.5)/(16+9) * 2*np.pi
            c: float = np.cos(th)
            s: float = np.sin(th)
            m: np.ndarray = np.array([[c, -s], [s, c]])
            p: np.ndarray = m @ xy
            ax.plot(p[0]+i+0.5, p[1]+j+0.5, color=c2, linewidth=4)
    # arrange
    #ax.set_xlim(-1.1, 1.1)
    #ax.set_ylim(-1.1, 1.1)
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
