"""今日紹介する Python の用途と、そのつながりを Graphviz で図にする。

用途を「データを扱う」「テストを自動化する」「伝える」の 3 つの章に分けて枠で囲み、上から順に並べる。
用途の間のデータの受け渡しを矢印で表す。
"""
from common import ACCENT_COLOR, FONT_NAME, IMAGE_DIR, TEXT_COLOR, render_dot

OUTPUT = IMAGE_DIR / "01_overview.png"


def build_dot() -> str:
    """章ごとの枠と、用途の間の矢印を表す DOT を組み立てる。"""
    return f"""
digraph overview {{
    graph [rankdir=TB, bgcolor=transparent, nodesep=0.5, ranksep=0.7, dpi=110, newrank=true,
           fontname="{FONT_NAME}", fontsize=20, fontcolor="{ACCENT_COLOR}"];
    node [shape=box, style=rounded, fontname="{FONT_NAME}", fontsize=18, color="{TEXT_COLOR}",
          fontcolor="{TEXT_COLOR}", penwidth=2, margin="0.15,0.08"];
    edge [color="{TEXT_COLOR}", penwidth=2];

    subgraph cluster_test {{
        label="テストを自動化する"; color="{ACCENT_COLOR}"; style="rounded,dashed"; penwidth=2;
        api [label="API を叩く\\nhttpx"];
        automation [label="テスト実行の自動化"];
        command [label="コマンド実行\\nsubprocess.run"];
        {{ rank=same; api; automation; command; }}
    }}

    # 枠の名前に矢印が重ならないよう、矢印が入らない側に名前を置く
    subgraph cluster_data {{
        label="データを扱う"; labeljust=r; color="{ACCENT_COLOR}"; style="rounded,dashed"; penwidth=2;
        process [label="数値計算・データ処理\\nnumpy・pandas"];
        plot [label="可視化\\nmatplotlib"];
        image [label="画像処理\\nPillow"];
        {{ rank=same; process; plot; image; }}
    }}

    subgraph cluster_docs {{
        label="伝える"; labelloc=b; color="{ACCENT_COLOR}"; style="rounded,dashed"; penwidth=2;
        docs [label="ドキュメント作成\\nSphinx"];
    }}

    api -> automation [dir=back];  # 左に置いた api へ、automation から矢印を向ける
    automation -> command;
    api -> process;
    command -> process;
    process -> plot;
    plot -> image;
    plot -> docs;
    image -> docs;
}}
"""


def main() -> None:
    render_dot(build_dot(), OUTPUT)


if __name__ == "__main__":
    main()
