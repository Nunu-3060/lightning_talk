"""時間 t で動く円のアニメーションを作り、10 フレームおきに 6 枚並べた画像を出力する。

--frames を付けて実行すると、動画化用の連番画像を frames ディレクトリに出力する。
動画化の例: ffmpeg -framerate 30 -i frames/%03d.png out.mp4
"""
import argparse
import math
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
OUTPUT = HERE.parent / "image" / "08_animation.png"
FRAME_DIR = HERE / "frames"
SIZE = 300
FRAMES = 60
DOTS = 12
GAP = 10


def frame(t: int) -> Image.Image:
    """t 番目のフレームを描く。"""
    img = Image.new("RGB", (SIZE, SIZE), "black")
    draw = ImageDraw.Draw(img)
    for i in range(DOTS):
        a = 2 * math.pi * (i / DOTS + t / 360)                      # t とともに回転する
        r = 90 + 40 * math.sin(2 * math.pi * (t / FRAMES + i / 4))  # t とともに半径が波打つ
        x, y = SIZE / 2 + r * math.cos(a), SIZE / 2 + r * math.sin(a)
        draw.ellipse((x - 12, y - 12, x + 12, y + 12), fill=(255, 80 + 14 * i, 255 - 14 * i))
    return img


def main() -> None:
    parser = argparse.ArgumentParser(description="円のアニメーションを生成する")
    parser.add_argument("--frames", action="store_true", help="連番画像を frames ディレクトリに出力する")
    args = parser.parse_args()

    frames = [frame(t) for t in range(FRAMES)]
    if args.frames:
        FRAME_DIR.mkdir(exist_ok=True)
        for t, img in enumerate(frames):
            img.save(FRAME_DIR / f"{t:03d}.png")

    picked = frames[::10]
    sheet = Image.new("RGB", (SIZE * len(picked) + GAP * (len(picked) - 1), SIZE), "black")
    for k, img in enumerate(picked):
        sheet.paste(img, (k * (SIZE + GAP), 0))
    sheet.save(OUTPUT)


if __name__ == "__main__":
    main()
