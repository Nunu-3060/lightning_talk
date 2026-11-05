"""ライフゲームで NOT の論理演算を作る仕組みを、Graphviz で模式図にする。

グライダーの有無を 1・0 とみなす。信号の列と、グライダー銃から出る「すべて 1」の列を交差させると、
1 同士は衝突して消えるので、通過した列は信号を反転したものになる。
"""
import subprocess

import style

OUTPUT = style.IMAGE_DIR / "09_life_not.png"


def build_dot() -> str:
    """信号の列・銃の列・交差・出力を表す DOT を組み立てる。"""
    text = style.TEXT_COLOR
    return f"""
digraph not_gate {{
    graph [rankdir=LR, bgcolor=transparent, nodesep=0.6, ranksep=0.8, dpi=110];
    node [shape=box, style=rounded, fontname="Yu Gothic", fontsize=22, color="{text}", fontcolor="{text}",
          penwidth=2, margin="0.25,0.12"];
    edge [color="{text}", penwidth=2, arrowsize=1.2];

    signal [label="信号の列\n1 0 1 1 0", color="{style.SUB_COLOR}", fontcolor="{style.SUB_COLOR}"];
    gun [label="グライダー銃の列\n1 1 1 1 1"];
    cross [label="交差\n1 同士は\n衝突して消える", shape=ellipse, style=solid];
    output [label="通過した列\n0 1 0 0 1", color="{style.ACCENT_COLOR}", fontcolor="{style.ACCENT_COLOR}"];

    signal -> cross;
    gun -> cross;
    cross -> output;
}}
"""


def main() -> None:
    style.IMAGE_DIR.mkdir(exist_ok=True)
    subprocess.run(["dot", "-Tpng", "-o", str(OUTPUT)], input=build_dot().encode("utf-8"), check=True)


if __name__ == "__main__":
    main()
