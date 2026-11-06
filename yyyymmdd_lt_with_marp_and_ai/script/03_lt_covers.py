"""同じ手順で作った LT の表紙を marp-cli で画像にし、格子状に並べて出力する。

marp-cli が PATH に通っている必要がある（npm install -g @marp-team/marp-cli）。
"""
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image

LT_ROOT = Path(__file__).resolve().parent.parent.parent
OUTPUT = Path(__file__).resolve().parent.parent / "image" / "03_lt_covers.png"

# 並べる LT のフォルダー（作成順）
LT_DIRS: list[str] = [
    "yyyymmdd_python_creative_coding",
    "yyyymmdd_learning_with_ai",
    "yyyymmdd_engineer_ethics",
    "yyyymmdd_test_engineer",
    "yyyymmdd_cellular_automaton",
    "yyyymmdd_python_work",
]
COLUMNS = 3
THUMB_WIDTH = 640  # 1 枚の幅（ピクセル）
GAP = 24  # 画像の間の余白（ピクセル）


def render_cover(md_path: Path, output: Path) -> None:
    """md_path の 1 ページ目（表紙）を PNG で出力する。"""
    marp = shutil.which("marp")
    if marp is None:
        raise RuntimeError("marp-cli が見つからない")
    # 表紙が同じフォルダーの画像を参照するため、ローカルのファイルの読み込みを許可する
    subprocess.run(
        [marp, "--no-stdin", "--image", "png", "--allow-local-files", "-o", str(output), str(md_path)],
        check=True,
    )


def make_grid(paths: list[Path]) -> Image.Image:
    """画像を幅 THUMB_WIDTH に縮小し、COLUMNS 列の格子に並べる。"""
    thumbs: list[Image.Image] = []
    for p in paths:
        im = Image.open(p).convert("RGBA")
        height = round(im.height * THUMB_WIDTH / im.width)
        thumbs.append(im.resize((THUMB_WIDTH, height), Image.Resampling.LANCZOS))
    rows = -(-len(thumbs) // COLUMNS)  # 切り上げ
    cell_height = max(t.height for t in thumbs)
    width = COLUMNS * THUMB_WIDTH + (COLUMNS - 1) * GAP
    height = rows * cell_height + (rows - 1) * GAP
    canvas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    for i, thumb in enumerate(thumbs):
        row, col = divmod(i, COLUMNS)
        canvas.paste(thumb, (col * (THUMB_WIDTH + GAP), row * (cell_height + GAP)))
    return canvas


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        covers: list[Path] = []
        for name in LT_DIRS:
            cover = Path(tmp) / f"{name}.png"
            render_cover(LT_ROOT / name / "main.md", cover)
            covers.append(cover)
        make_grid(covers).save(OUTPUT)


if __name__ == "__main__":
    main()
