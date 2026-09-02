# -*- coding: utf-8 -*-
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))

import findbook_writer as writer
from findbook_highlights import write_highlights

LAST_IDS = [
    "07_other-20210902-09",
    "07_other-20210902-10",
]
ALL_IDS = [
    "05_food_wellness-20210902-06",
    "05_food_wellness-20210902-07",
    "05_food_wellness-20210902-08",
    "05_food_wellness-20210902-09",
    "05_food_wellness-20210902-10",
    "06_computer_info-20210902-06",
    "06_computer_info-20210902-07",
    "06_computer_info-20210902-08",
    "06_computer_info-20210902-09",
    "06_computer_info-20210902-10",
    "07_other-20210902-06",
    "07_other-20210902-07",
    "07_other-20210902-08",
    "07_other-20210902-09",
    "07_other-20210902-10",
]


def merge_lines(book_id: str) -> list[str]:
    first = TOOLS / f".hlseg_{book_id}_001.txt"
    second = TOOLS / f".hlseg_{book_id}_076.txt"
    lines = [line.strip() for line in first.read_text(encoding="utf-8").splitlines() if line.strip()]
    lines += [line.strip() for line in second.read_text(encoding="utf-8").splitlines() if line.strip()]
    return lines


def main() -> int:
    for book_id in LAST_IDS:
        lines = merge_lines(book_id)
        print(f"WRITE\t{book_id}\t{len(lines)}")
        result = write_highlights(ROOT, book_id, lines)
        print(f"OK\t{result['id']}\t{result['count']}")
    manifest = writer.read_json(ROOT / "data.json")
    print(f"totalBooks={manifest.get('totalBooks')} len={len(manifest.get('books', []))}")
    for book_id in ALL_IDS:
        writer.check_index_link(ROOT, book_id)
        matches = [item for item in manifest.get("books", []) if item.get("id") == book_id]
        book = writer.read_json(ROOT / matches[0]["file"])
        highlights = book.get("chatgptHighlights") or []
        print(
            f"LINK_OK\t{book_id}\t{len(highlights)}\t{book.get('chatgptStatus')}\t"
            f"{book.get('highlightsSource')}\t{book.get('title')}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
