"""乱数で円を配置する。同じシードなら同じ絵になることを 3 枚並べて示す。"""
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

OUTPUT = Path(__file__).resolve().parent.parent / "image" / "03_random.png"
SIZE = 400
GAP = 20
SEEDS = [1, 1, 2]


def draw_circles(seed: int) -> Image.Image:
    """seed から決まる配置・大きさ・色で円を 120 個描く。"""
    rng = np.random.default_rng(seed)  # シードを固定した乱数生成器
    img = Image.new("RGB", (SIZE, SIZE), (20, 20, 30))
    draw = ImageDraw.Draw(img, "RGBA")
    for _ in range(120):
        x, y = rng.uniform(0, SIZE, 2)
        r = rng.exponential(18)  # 小さい円が多く、大きい円は少ない
        red, green, blue = (int(v) for v in rng.integers(80, 256, 3))
        draw.ellipse((x - r, y - r, x + r, y + r), fill=(red, green, blue, 150))
    return img


def main() -> None:
    out = Image.new("RGB", (SIZE * len(SEEDS) + GAP * (len(SEEDS) - 1), SIZE), "black")
    for i, seed in enumerate(SEEDS):
        out.paste(draw_circles(seed), (i * (SIZE + GAP), 0))
    out.save(OUTPUT)


if __name__ == "__main__":
    main()
