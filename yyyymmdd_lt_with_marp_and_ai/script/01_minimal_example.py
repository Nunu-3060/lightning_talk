"""最小の Marp の例を marp-cli でスライド画像にし、2 ページを縦に並べて出力する。

marp-cli が PATH に通っている必要がある（npm install -g @marp-team/marp-cli）。
"""
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image

OUTPUT = Path(__file__).resolve().parent.parent / "image" / "01_minimal_example.png"

# スライドに載せる md と同じ内容。
# 発表資料の背景（gaia の invert）と見分けやすいように、白地の default テーマにする
MINIMAL_MD = """\
---
marp: true
theme: default
---

# Marp と AI で作る LT

Nunu_3060

---

## Marp とは

* Markdown からスライドを作る
"""

GAP = 24  # 2 ページの間の余白（ピクセル）


def render_slides(md_text: str, work_dir: Path) -> list[Path]:
    """md_text を marp-cli で PNG にし、ページ順の画像のパスを返す。"""
    marp = shutil.which("marp")
    if marp is None:
        raise RuntimeError("marp-cli が見つからない")
    md_path = work_dir / "minimal.md"
    md_path.write_text(md_text, encoding="utf-8")
    subprocess.run([marp, "--no-stdin", "--images", "png", str(md_path)], check=True)
    return sorted(work_dir.glob("minimal.*.png"))


def stack_vertically(paths: list[Path]) -> Image.Image:
    """画像を縦に並べた 1 枚の画像を作る。"""
    images = [Image.open(p).convert("RGBA") for p in paths]
    width = max(im.width for im in images)
    height = sum(im.height for im in images) + GAP * (len(images) - 1)
    canvas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    y = 0
    for im in images:
        canvas.paste(im, (0, y))
        y += im.height + GAP
    return canvas


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        pages = render_slides(MINIMAL_MD, Path(tmp))
        stack_vertically(pages).save(OUTPUT)


if __name__ == "__main__":
    main()
