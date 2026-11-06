"""テストの実行から合否判定・可視化までを 1 本のスクリプトにまとめた流れを Graphviz で図にする。

各段階の下に、その段階で使う Python のライブラリ・関数を添える。
"""
from common import ACCENT_COLOR, FONT_NAME, IMAGE_DIR, TEXT_COLOR, render_dot

OUTPUT = IMAGE_DIR / "04_test_flow.png"

# (段階の名前, 使うライブラリ・関数)
STEPS = [
    ("解析を実行", "subprocess.run"),
    ("結果を取得", "httpx"),
    ("データ処理", "numpy・pandas"),
    ("合否を判定", "基準値と比較"),
    ("図にする", "matplotlib"),
]


def build_dot() -> str:
    """段階を左から右へ矢印でつなぎ、全体を 1 本のスクリプトの枠で囲む DOT を組み立てる。"""
    nodes = "\n".join(
        f'        step{i} [label=<{name}<br/><font point-size="15" color="{ACCENT_COLOR}">{tool}</font>>];'
        for i, (name, tool) in enumerate(STEPS)
    )
    edges = " -> ".join(f"step{i}" for i in range(len(STEPS)))
    return f"""
digraph test_flow {{
    graph [rankdir=LR, bgcolor=transparent, nodesep=0.4, ranksep=0.45, dpi=110,
           fontname="{FONT_NAME}", fontsize=20, fontcolor="{TEXT_COLOR}"];
    node [shape=box, style=rounded, fontname="{FONT_NAME}", fontsize=19, color="{TEXT_COLOR}",
          fontcolor="{TEXT_COLOR}", penwidth=2, margin="0.2,0.15"];
    edge [color="{TEXT_COLOR}", penwidth=2];

    subgraph cluster_script {{
        label="1 本のスクリプト (1 回の実行)"; color="{ACCENT_COLOR}"; style="rounded,dashed"; penwidth=2;
{nodes}
    }}

    {edges};
}}
"""


def main() -> None:
    render_dot(build_dot(), OUTPUT)


if __name__ == "__main__":
    main()
