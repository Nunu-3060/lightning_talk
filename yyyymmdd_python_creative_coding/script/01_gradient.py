"""画像は数値の配列であることを示すグラデーション画像を生成する。"""
from pathlib import Path

import numpy as np
from PIL import Image

OUTPUT = Path(__file__).resolve().parent.parent / "image" / "01_gradient.png"
SIZE = 800


def main() -> None:
    x = np.linspace(0, 1, SIZE)
    y = np.linspace(0, 1, SIZE)
    xx, yy = np.meshgrid(x, y)  # 全画素の座標 (0 〜 1)

    img = np.zeros((SIZE, SIZE, 3), dtype=np.uint8)
    img[..., 0] = xx * 255                   # 赤: 右ほど強い
    img[..., 1] = yy * 255                   # 緑: 下ほど強い
    img[..., 2] = (1 - xx) * (1 - yy) * 255  # 青: 左上ほど強い

    Image.fromarray(img).save(OUTPUT)


if __name__ == "__main__":
    main()
