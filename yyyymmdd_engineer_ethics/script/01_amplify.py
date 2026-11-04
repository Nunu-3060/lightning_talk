"""1 人の判断が製品を通じて多数の利用者に届く様子を Graphviz で図にする。"""
import subprocess
from pathlib import Path

OUTPUT = Path(__file__).resolve().parent.parent / "image" / "01_amplify.png"

TEXT_COLOR = "#fff8e1"  # gaia テーマの invert の文字色に合わせる
ACCENT_COLOR = "#0277bd"
USER_COUNT = 12  # 利用者を表すノードの数 (多数であることが伝わればよい)


def build_dot() -> str:
    """技術者 → 製品 → 利用者 の広がりを表す DOT を組み立てる。"""
    users = "\n".join(f'    user{i} [label=""];' for i in range(USER_COUNT))
    edges = "\n".join(f"    product -> user{i};" for i in range(USER_COUNT))
    return f"""
digraph amplify {{
    graph [rankdir=LR, bgcolor=transparent, nodesep=0.08, ranksep=1.2, dpi=110];
    node [fontname="Yu Gothic", fontsize=18, color="{TEXT_COLOR}", fontcolor="{TEXT_COLOR}", penwidth=2];
    edge [color="{TEXT_COLOR}", penwidth=1.5, arrowsize=0.7];

    engineer [label="技術者の\\n1 つの判断", shape=box, style="rounded,filled", fillcolor="{ACCENT_COLOR}",
              margin="0.25,0.15"];
    product [label="製品・サービス\\n(複製して配布)", shape=box, style="rounded", margin="0.25,0.15"];
    node [shape=circle, width=0.22, fixedsize=true];
{users}

    engineer -> product [penwidth=2.5, arrowsize=1.0];
{edges}

    label [shape=plaintext, width=2.2, fixedsize=false, fontsize=18, label="多数の利用者"];
    {{rank=same; user{USER_COUNT - 1}; label;}}
    user{USER_COUNT - 1} -> label [style=invis];
}}
"""


def main() -> None:
    subprocess.run(["dot", "-Tpng", "-o", str(OUTPUT)], input=build_dot().encode("utf-8"), check=True)


if __name__ == "__main__":
    main()
