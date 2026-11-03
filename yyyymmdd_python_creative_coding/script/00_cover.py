"""表紙用に作例画像 4 枚を正方形に切り抜いて横一列に並べる。

他のスクリプトで作例画像を生成した後に実行する。
"""
from pathlib import Path

from PIL import Image

IMAGE_DIR = Path(__file__).resolve().parent.parent / "image"
OUTPUT = IMAGE_DIR / "00_cover.png"
NAMES = ["02_repeat", "04_flowfield", "05_mandelbrot", "06_reaction_diffusion"]
SIZE = 300


def square_crop(img: Image.Image) -> Image.Image:
    """画像の中央を正方形に切り抜く。"""
    w, h = img.size
    m = min(w, h)
    left, top = (w - m) // 2, (h - m) // 2
    return img.crop((left, top, left + m, top + m))


def main() -> None:
    out = Image.new("RGB", (SIZE * len(NAMES), SIZE), "black")
    for i, name in enumerate(NAMES):
        img = Image.open(IMAGE_DIR / f"{name}.png").convert("RGB")
        out.paste(square_crop(img).resize((SIZE, SIZE)), (i * SIZE, 0))
    out.save(OUTPUT)


if __name__ == "__main__":
    main()
