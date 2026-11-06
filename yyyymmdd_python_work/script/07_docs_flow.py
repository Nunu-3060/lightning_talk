"""図を作るスクリプトと文書のソースを一緒に管理すると、データの更新が文書まで届くことを Graphviz で図にする。

データ → スクリプト → 図・画像 → Sphinx → 文書 の流れのうち、
人が書いて管理するもの (スクリプトと文書のソース) を枠で囲む。
"""
from common import ACCENT_COLOR, FONT_NAME, IMAGE_DIR, TEXT_COLOR, WARNING_COLOR, render_dot

OUTPUT = IMAGE_DIR / "07_docs_flow.png"


def build_dot() -> str:
    """データから文書までの流れを表す DOT を組み立てる。"""
    return f"""
digraph docs_flow {{
    graph [rankdir=LR, bgcolor=transparent, nodesep=0.5, ranksep=0.6, dpi=110,
           fontname="{FONT_NAME}", fontsize=20, fontcolor="{ACCENT_COLOR}"];
    node [shape=box, style=rounded, fontname="{FONT_NAME}", fontsize=19, color="{TEXT_COLOR}",
          fontcolor="{TEXT_COLOR}", penwidth=2, margin="0.15,0.1"];
    edge [color="{TEXT_COLOR}", penwidth=2];

    data [label="データ", color="{WARNING_COLOR}", fontcolor="{WARNING_COLOR}"];

    subgraph cluster_managed {{
        label="テキストとして一緒に管理"; color="{ACCENT_COLOR}"; style="rounded,dashed"; penwidth=2;
        script [label="図を作る\\nスクリプト"];
        source [label="文書の\\nソース"];
    }}

    figure [label="図・画像"];
    sphinx [label="Sphinx"];
    document [label="文書\\nHTML・PDF"];

    data -> script;
    script -> figure;
    figure -> sphinx;
    source -> sphinx;
    sphinx -> document;
}}
"""


def main() -> None:
    render_dot(build_dot(), OUTPUT)


if __name__ == "__main__":
    main()
