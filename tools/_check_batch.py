# -*- coding: utf-8 -*-
"""Check this batch's index links and highlight counts only."""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import findbook_writer as writer
from findbook_highlights import extract_highlights

ROOT = Path(__file__).resolve().parents[1]
IDS = [
    "05_food_wellness-20210904-01",
    "05_food_wellness-20210904-02",
    "05_food_wellness-20210904-03",
    "05_food_wellness-20210904-04",
    "05_food_wellness-20210904-05",
    "06_computer_info-20210904-01",
    "06_computer_info-20210904-02",
    "06_computer_info-20210904-03",
    "06_computer_info-20210904-04",
    "06_computer_info-20210904-05",
    "07_other-20210904-01",
    "07_other-20210904-02",
    "07_other-20210904-03",
    "07_other-20210904-04",
    "07_other-20210904-05",
]


def main() -> int:
    """Print one line per committed book and return 1 if any check fails."""
    manifest = writer.read_json(ROOT / "data.json")
    books = manifest.get("books") or []
    print("totalBooks", manifest.get("totalBooks"), "len", len(books))
    errors: list[str] = []
    for book_id in IDS:
        try:
            writer.check_index_link(ROOT, book_id)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"link {book_id}: {exc}")
            continue
        matches = [item for item in books if item.get("id") == book_id]
        relative = str(matches[0]["file"])
        book = writer.read_json(ROOT / relative)
        highlights = book.get("chatgptHighlights") or []
        extracted = extract_highlights("\n".join(highlights))
        garbled = any(("\ufffd" in line or "锟斤拷" in line or "ï¿½" in line) for line in highlights)
        title = str(book.get("title") or "")
        title_ok = bool(re.search(r"[\u4e00-\u9fff]", title))
        status = book.get("chatgptStatus")
        source = book.get("highlightsSource")
        short_title = title[:24]
        print(
            f"{book_id} {status} n={len(highlights)} extracted={len(extracted)} "
            f"src={source} garbled={garbled} title={short_title}"
        )
        if status != "complete" or len(highlights) != 150 or len(extracted) != 150 or garbled or not title_ok:
            errors.append(f"content {book_id}")
        if (
            book.get("id") != book_id
            or book.get("categoryId") != matches[0].get("categoryId")
            or book.get("title") != matches[0].get("title")
            or book.get("author") != matches[0].get("author")
        ):
            errors.append(f"mismatch {book_id}")
    print("errors", len(errors))
    for item in errors:
        print("ERR", item)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
