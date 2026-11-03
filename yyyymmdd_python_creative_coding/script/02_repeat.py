"""正方形を少しずつ回転・縮小しながら繰り返し描き、渦巻き模様を作る。"""
import math
from pathlib import Path

from PIL import Image, ImageDraw

OUTPUT = Path(__file__).resolve().parent.parent / "image" / "02_repeat.png"
SIZE = 800
COUNT = 60


def square(cx: float, cy: float, r: float, angle: float) -> list[tuple[float, float]]:
    """中心 (cx, cy)、中心から頂点までの距離 r、回転角 angle の正方形の頂点を返す。"""
    return [(cx + r * math.cos(angle + k * math.pi / 2),
             cy + r * math.sin(angle + k * math.pi / 2)) for k in range(4)]


def main() -> None:
    img = Image.new("RGB", (SIZE, SIZE), "black")
    draw = ImageDraw.Draw(img)

    for i in range(COUNT):
        r = 380 * 0.95 ** i          # 5 % ずつ縮める
        angle = math.radians(i * 4)  # 4 度ずつ回す
        c = 255 * i // COUNT         # 外側は紫、内側は黄
        draw.polygon(square(SIZE / 2, SIZE / 2, r, angle), outline=(255, c, 255 - c), width=2)

    img.save(OUTPUT)


if __name__ == "__main__":
    main()
