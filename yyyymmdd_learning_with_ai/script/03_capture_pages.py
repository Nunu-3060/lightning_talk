"""公開中の文書サイトの画面写真を Chrome のヘッドレス実行で撮る。

Chrome が既定の場所に無い場合は CHROME を書き換える。
"""
import subprocess
from pathlib import Path

CHROME = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
IMAGE_DIR = Path(__file__).resolve().parent.parent / "image"

# 出力ファイル名と撮る URL
SITE = "https://nunu-3060.github.io"
PAGES: dict[str, str] = {
    "00_cover.png": f"{SITE}/sphinx_docs/",
    "03_generative_art_top.png": f"{SITE}/sphinx_docs_graphics_and_art/python_generative_art/index.html",
}
WINDOW_SIZE = "1280,720"


def capture(url: str, output: Path) -> None:
    """url のページを開き、ウィンドウの大きさで画面写真を撮る。"""
    subprocess.run(
        [
            str(CHROME),
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            f"--window-size={WINDOW_SIZE}",
            "--virtual-time-budget=5000",  # ページの読み込みを待つ時間（ミリ秒）
            f"--screenshot={output}",
            url,
        ],
        check=True,
    )


def main() -> None:
    for name, url in PAGES.items():
        capture(url, IMAGE_DIR / name)


if __name__ == "__main__":
    main()
