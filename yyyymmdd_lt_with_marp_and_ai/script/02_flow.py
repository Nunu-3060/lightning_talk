"""資料作成の流れ図を Graphviz で出力する。"""
import subprocess
from pathlib import Path

OUTPUT = Path(__file__).resolve().parent.parent / "image" / "02_flow.png"

# 人が行う作業は塗りつぶし、Claude Code が行う作業は枠線のみで描く
DOT = r"""
digraph flow {
    graph [rankdir=TB, bgcolor=transparent, nodesep=0.7, ranksep=0.6, dpi=120];
    node [shape=box, style="rounded", fontname="Yu Gothic", fontsize=18, width=2.6,
          color="#fff8e1", fontcolor="#fff8e1", penwidth=2, margin="0.2,0.12"];
    edge [color="#fff8e1", penwidth=2, arrowsize=0.9,
          fontname="Yu Gothic", fontsize=16, fontcolor="#fff8e1"];

    human1 [label="依頼
prompt.md", style="rounded,filled", fillcolor="#0277bd"];
    ai1 [label="構成案・確認事項
result.md"];
    human2 [label="回答・執筆指示
prompt.md", style="rounded,filled", fillcolor="#0277bd"];
    ai2 [label="執筆
main.md・script.md
図のスクリプト"];
    ai3 [label="出力・検査
marp-cli
flake8・mypy"];
    human3 [label="確認", style="rounded,filled", fillcolor="#0277bd"];

    # 1 段目: 構成を決める、2 段目: 書いて確かめる
    {rank=same; human1; ai1; human2;}
    {rank=same; ai2; ai3; human3;}

    human1 -> ai1 -> human2;
    human2 -> ai1 [label="再提案", style=dashed];
    human2 -> ai2;
    ai2 -> ai3 -> human3;
    human3 -> human2 [label="修正の依頼", style=dashed];
}
"""


def main() -> None:
    subprocess.run(["dot", "-Tpng", "-o", str(OUTPUT)], input=DOT.encode("utf-8"), check=True)


if __name__ == "__main__":
    main()
