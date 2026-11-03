from pathlib import Path


def main() -> None:
    home: Path = Path(__file__).resolve().parent
    fp: Path = home.joinpath("imref.md")
    text: str = ""
    for im in sorted(home.glob("image/*.png")):
        text += f"""
---

![bg cover]({im.relative_to(home).as_posix()})
"""
    print(text)
    fp.write_text(text, encoding="utf-8")
    return None


if __name__ == "__main__":
    main()
