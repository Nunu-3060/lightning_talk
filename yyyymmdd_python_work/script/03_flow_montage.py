"""02_flow_cases.py が出力した 3 ケースの図を、Pillow で横に並べて 1 枚の画像にする。

先に 02_flow_cases.py を実行しておくこと。
"""
from PIL import Image

from common import IMAGE_DIR

INPUTS = [IMAGE_DIR / f"02_flow_case_{number}.png" for number in (1, 2, 3)]
OUTPUT = IMAGE_DIR / "03_flow_montage.png"
GAP = 20  # 図と図の間隔 (ピクセル)


def main() -> None:
    images = [Image.open(path) for path in INPUTS]

    width = sum(image.width for image in images) + GAP * (len(images) - 1)
    height = max(image.height for image in images)
    montage = Image.new("RGBA", (width, height), (0, 0, 0, 0))  # 背景は透過にする

    x = 0
    for image in images:
        montage.paste(image, (x, 0))
        x += image.width + GAP

    montage.save(OUTPUT)


if __name__ == "__main__":
    main()
