"""図の見た目 (色・フォント・保存先) をそろえるための共通の設定。"""
from pathlib import Path

import matplotlib
import numpy as np
import numpy.typing as npt
from matplotlib.axes import Axes
from matplotlib.colors import LightSource, LinearSegmentedColormap, ListedColormap
from matplotlib.figure import Figure

matplotlib.use("Agg")

IMAGE_DIR = Path(__file__).resolve().parent.parent / "image"

TEXT_COLOR = "#fff8e1"  # gaia テーマの invert の文字色に合わせる
OFF_COLOR = "#263238"  # 状態 0 (死・空き) のセル
ON_COLOR = "#ffd54f"  # 状態 1 (生・車) のセル
ACCENT_COLOR = "#4fc3f7"  # 強調に使う色
SUB_COLOR = "#ff8a65"  # 2 種類目の強調に使う色

CELL_CMAP = ListedColormap([OFF_COLOR, ON_COLOR])


def setup() -> None:
    """日本語を表示できるフォントを設定する。"""
    matplotlib.rcParams["font.family"] = "Yu Gothic"
    matplotlib.rcParams["font.size"] = 16


def show_cells(ax: Axes, cells: npt.NDArray[np.uint8], title: str = "") -> None:
    """0・1 の 2 次元配列を、セルの色で塗った画像として描く。"""
    ax.imshow(cells, cmap=CELL_CMAP, vmin=0, vmax=1, interpolation="nearest", aspect="auto")
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    if title:
        ax.set_title(title, color=TEXT_COLOR, fontsize=22)


def draw_grid_lines(ax: Axes, rows: int, cols: int) -> None:
    """盤面の小さな図に、セルの境界線を描く。"""
    for i in range(rows + 1):
        ax.axhline(i - 0.5, color="#546e7a", linewidth=1)
    for j in range(cols + 1):
        ax.axvline(j - 0.5, color="#546e7a", linewidth=1)


def save(fig: Figure, name: str) -> None:
    """背景を透明にして image フォルダーに保存する。"""
    IMAGE_DIR.mkdir(exist_ok=True)
    fig.savefig(IMAGE_DIR / name, transparent=True, dpi=100)


SAND_CMAP = LinearSegmentedColormap.from_list("sand", ["#8d6e63", "#d7b98e", "#f5e6c8"])


def shade_sand(height: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
    """砂の高さを、左上から光を当てた砂色の画像 (RGB) に変換する。"""
    light = LightSource(azdeg=315, altdeg=35)
    rgb: npt.NDArray[np.float64] = light.shade(height, cmap=SAND_CMAP, blend_mode="soft", vert_exag=2)
    return rgb
