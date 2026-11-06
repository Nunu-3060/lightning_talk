"""Sphinx で作った資料の表紙を、headless Chrome で撮影して画像にする。

Chrome は Python 以外のソフトウェアなので、subprocess.run でコマンドとして呼び出す。
撮影にはネットワーク接続が必要である。
"""
import subprocess
from pathlib import Path

from common import IMAGE_DIR

CHROME = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
URL = "https://nunu-3060.github.io/sphinx_docs_programming/python_introduction/index.html"
OUTPUT = IMAGE_DIR / "06_sphinx_screenshot.png"

# 本文の右端 (約 1100 ピクセル) に合わせた幅にして、右側の余白を写さない
WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 620


def main() -> None:
    subprocess.run(
        [
            str(CHROME),
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            f"--window-size={WINDOW_WIDTH},{WINDOW_HEIGHT}",
            f"--screenshot={OUTPUT}",
            URL,
        ],
        check=True,
    )


if __name__ == "__main__":
    main()
