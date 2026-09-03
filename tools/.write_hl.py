# -*- coding: utf-8 -*-
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from findbook_highlights import write_highlights
ROOT = Path(__file__).resolve().parents[1]
BOOKS = {}
def add(book_id: str, path: Path) -> None:
    BOOKS[book_id] = path.read_text(encoding="utf-8")
def main() -> None:
    tools = Path(__file__).resolve().parent
    for path in sorted(tools.glob(".hl_05_food_wellness-20210903-*.txt")):
        add(path.name[4:-4], path)
    for path in sorted(tools.glob(".hl_06_computer_info-20210903-*.txt")):
        add(path.name[4:-4], path)
    for path in sorted(tools.glob(".hl_07_other-20210903-*.txt")):
        add(path.name[4:-4], path)
    if not BOOKS:
        raise SystemExit("no batch hl files")
    for book_id, text in BOOKS.items():
        result = write_highlights(ROOT, book_id, text.splitlines())
        print(f"written\t{result['id']}\t{result['count']}")
if __name__ == "__main__":
    main()
