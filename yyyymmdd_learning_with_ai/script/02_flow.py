"""依頼から読むまでの流れ図を Graphviz で出力する。"""
import subprocess
from pathlib import Path

OUTPUT = Path(__file__).resolve().parent.parent / "image" / "02_flow.png"

# 人が行う作業は塗りつぶし、Claude Code が行う作業は枠線のみで描く
DOT = r"""
digraph flow {
    graph [rankdir=LR, bgcolor=transparent, nodesep=0.4, ranksep=0.5, dpi=110];
    node [shape=box, style="rounded", fontname="Yu Gothic", fontsize=16,
          color="#fff8e1", fontcolor="#fff8e1", penwidth=2, margin="0.2,0.12"];
    edge [color="#fff8e1", penwidth=2, arrowsize=0.9];

    human1 [label="依頼\nprompt.md", style="rounded,filled", fillcolor="#0277bd"];
    ai1 [label="構成の提案\nresult.md"];
    human2 [label="確認・指示\nprompt.md", style="rounded,filled", fillcolor="#0277bd"];
    ai2 [label="執筆\nrst・サンプル"];
    ai3 [label="ビルド・検査\n報告 result.md"];
    human3 [label="読む", style="rounded,filled", fillcolor="#0277bd"];

    human1 -> ai1 -> human2 -> ai2 -> ai3 -> human3;
    human3 -> human2 [label="追加の依頼", fontname="Yu Gothic", fontsize=14,
                      fontcolor="#fff8e1", style=dashed, constraint=false];
}
"""


def main() -> None:
    subprocess.run(["dot", "-Tpng", "-o", str(OUTPUT)], input=DOT.encode("utf-8"), check=True)


if __name__ == "__main__":
    main()
