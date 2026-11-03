from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def main() -> None:
    # config
    fp: Path = Path(__file__).resolve().with_suffix(".png")
    plt.rcParams["figure.dpi"] = 100
    plt.rcParams["figure.figsize"] = [19.2, 10.8]
    c0: str = "#FFE4A8"
    c1: str = "#008B52"
    c2: str = "#412554"
    # generate figure
    fig: plt.Figure
    ax: plt.Axes
    fig, ax = plt.subplots()
    # plot
    x: np.ndarray = 16*np.array([1, 1, -1, -1, 1])
    y: np.ndarray = 16*np.array([1, -1, -1, 1, 1])
    for i in range(8):
        r: float = (1+i)*0.125
        ax.plot(r*x, r*y, linewidth=6, color=c1)
    v4 = ((1, 0), (-1, 0), (0, 1), (0, -1))
    nv: dict[tuple[int, int], dict[int, tuple[int, int]]] = {
        muki: {
            z:  [v4[0], v4[2], v4[3]][z] if muki == v4[0] else
                [v4[1], v4[2], v4[3]][z] if muki == v4[1] else
                [v4[0], v4[1], v4[2]][z] if muki == v4[2] else
                [v4[0], v4[1], v4[3]][z]
            for z in range(3)
        }
        for muki in v4
    }
    rng: np.random.Generator = np.random.default_rng()
    data: list[list[int]] = [
        [[i], [16], (0, 1), 1]
        for i in range(-15, 16, 1)
    ] + [
        [[16], [i], (1, 0), 1]
        for i in range(15, -16, -1)
    ] + [
        [[i], [-16], (0, -1), 1]
        for i in range(15, -16, -1)
    ] + [
        [[-16], [i], (-1, 0), 1]
        for i in range(-15, 16, 1)
    ]
    points: set[tuple[int, int]] = {
        (i[0], j[0])
        for i, j, *_ in data
    } | {
        (i, j)
        for i in range(-15, 16)
        for j in range(-15, 16)
    }
    nx: int
    ny: int
    for dx, dy, dv, df in data:
        nx = dx[-1] + dv[0]
        ny = dy[-1] + dv[1]
        dx.append(nx)
        dy.append(ny)
        points.add((nx, ny))
    for i in range(32):
        for index, (dx, dy, dv, df) in enumerate(data):
            if df:
                pass
            else:
                continue
            z: int = rng.integers(3)
            for i in range(3):
                nextv = nv[dv][(z+i)%3]
                nx = dx[-1] + nextv[0]
                ny = dy[-1] + nextv[1]
                if (nx, ny) not in points:
                    dx.append(nx)
                    dy.append(ny)
                    points.add((nx, ny))
                    data[index][2] = nv[dv][(z+i)%3]
                    break
                else:
                    pass
            else:
                data[index][3] = 0


    for dx, dy, *_ in data:
        ax.plot(dx, dy, linewidth=6, color=c2)
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
