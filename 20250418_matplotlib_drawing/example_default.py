from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def main() -> None:
    fp: Path = Path(__file__).resolve().with_suffix(".png")
    x: np.ndarray = np.linspace(-np.pi, np.pi, 3601, endpoint=True)
    c: np.ndarray = np.cos(x)
    s: np.ndarray = np.sin(x)
    fig: plt.Figure
    ax: plt.Axes
    fig, ax = plt.subplots()
    ax.plot(x, c, label="cos")
    ax.plot(x, s, label="sin")
    ax.legend()
    ax.set_xlabel("x label")
    ax.set_ylabel("y label")
    fig.tight_layout()
    fig.savefig(fp)
    plt.cla()
    plt.clf()
    plt.close(fig)
    return None


if __name__ == "__main__":
    main()
