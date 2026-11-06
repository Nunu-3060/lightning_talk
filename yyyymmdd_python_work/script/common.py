"""画像を出力するスクリプトで共通に使う定数と関数。"""
import subprocess
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.axes import Axes

IMAGE_DIR = Path(__file__).resolve().parent.parent / "image"

TEXT_COLOR = "#fff8e1"  # gaia テーマの invert の文字色に合わせる
ACCENT_COLOR = "#4fc3f7"  # 強調色 1 (青)
WARNING_COLOR = "#ffb74d"  # 強調色 2 (橙)
FONT_NAME = "Yu Gothic"


def render_dot(dot: str, output: Path) -> None:
    """Graphviz の DOT 言語で書いた図を PNG に出力する。"""
    subprocess.run(["dot", "-Tpng", "-o", str(output)], input=dot.encode("utf-8"), check=True)


def setup_matplotlib() -> None:
    """日本語を表示でき、スライドで読める大きさの文字になるよう matplotlib を設定する。"""
    plt.rcParams["font.family"] = FONT_NAME
    plt.rcParams["font.size"] = 20


def style_axes(ax: Axes) -> None:
    """暗い背景のスライドで読めるよう、軸・目盛り・ラベルを明るい色にする。"""
    for spine in ax.spines.values():
        spine.set_color(TEXT_COLOR)
    ax.tick_params(colors=TEXT_COLOR)
    ax.xaxis.label.set_color(TEXT_COLOR)
    ax.yaxis.label.set_color(TEXT_COLOR)
    ax.title.set_color(TEXT_COLOR)
