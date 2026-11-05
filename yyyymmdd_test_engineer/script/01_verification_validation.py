"""検証 (仕様どおりか) と妥当性確認 (目的に合うか) の違いを Graphviz で図にする。

利用者の目的 → 仕様 → ソフトウェア と作られていく流れに対して、
検証はソフトウェアを仕様と比べ、妥当性確認はソフトウェアを利用者の目的と比べることを示す。
"""
import subprocess
from pathlib import Path

OUTPUT = Path(__file__).resolve().parent.parent / "image" / "01_verification_validation.png"

TEXT_COLOR = "#fff8e1"  # gaia テーマの invert の文字色に合わせる
VERIFICATION_COLOR = "#4fc3f7"  # 検証を表す色
VALIDATION_COLOR = "#ffb74d"  # 妥当性確認を表す色


def build_dot() -> str:
    """作る流れ (上段) と、比べる流れ (下側の矢印) を表す DOT を組み立てる。"""
    return f"""
digraph vv {{
    graph [rankdir=LR, bgcolor=transparent, nodesep=0.5, ranksep=0.9, dpi=110];
    node [shape=box, style=rounded, fontname="Yu Gothic", fontsize=20, color="{TEXT_COLOR}",
          fontcolor="{TEXT_COLOR}", penwidth=2, margin="0.2,0.1"];
    edge [fontname="Yu Gothic", fontsize=18, color="{TEXT_COLOR}", fontcolor="{TEXT_COLOR}", penwidth=2];

    purpose [label="利用者の目的\\n(何をしたいか)"];
    spec [label="仕様\\n(何を作るか)"];
    software [label="ソフトウェア"];

    purpose -> spec [label="決める"];
    spec -> software [label="作る"];

    software -> spec [label="検証\\n仕様どおりか", color="{VERIFICATION_COLOR}",
                      fontcolor="{VERIFICATION_COLOR}", style=dashed, penwidth=3, constraint=false];
    software -> purpose [label="妥当性確認\\n目的に合うか", color="{VALIDATION_COLOR}",
                         fontcolor="{VALIDATION_COLOR}", style=dashed, penwidth=3, constraint=false];
}}
"""


def main() -> None:
    subprocess.run(["dot", "-Tpng", "-o", str(OUTPUT)], input=build_dot().encode("utf-8"), check=True)


if __name__ == "__main__":
    main()
