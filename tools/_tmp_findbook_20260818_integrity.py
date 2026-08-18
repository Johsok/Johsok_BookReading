#!/usr/bin/env python3
"""Index-link integrity check for FindBook (no content QA)."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BATCH_IDS = [
    "01_business_startup-20260818-01",
    "01_business_startup-20260818-02",
    "02_psychology_growth-20260818-01",
    "02_psychology_growth-20260818-02",
    "03_natural_science-20260818-01",
    "03_natural_science-20260818-02",
    "04_healthcare-20260818-01",
    "04_healthcare-20260818-02",
    "05_food_wellness-20260818-01",
    "05_food_wellness-20260818-02",
    "06_computer_info-20260818-01",
    "06_computer_info-20260818-02",
    "07_other-20260818-01",
    "07_other-20260818-02",
]


def main() -> None:
    data = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))
    books = data["books"]
    indexed = {str(b.get("file") or "").replace("\\", "/") for b in books}
    disk = [p.relative_to(ROOT).as_posix() for p in (ROOT / "Books").rglob("*.json")]
    extra = sorted(set(disk) - indexed)
    print("orphan_count", len(extra))
    for item in extra:
        print("ORPHAN", item)

    print("--- batch link ---")
    id_set: set[str] = set()
    file_set: set[str] = set()
    ok = True
    found = 0
    for book_index in books:
        bid = book_index.get("id")
        if bid not in BATCH_IDS:
            continue
        found += 1
        expected = f"Books/{book_index['categoryId']}/{bid}.json"
        path = ROOT / str(book_index.get("file") or "")
        book = json.loads(path.read_text(encoding="utf-8-sig"))
        checks = [
            book_index.get("file") == expected,
            path.exists(),
            book.get("id") == book_index.get("id"),
            book.get("categoryId") == book_index.get("categoryId"),
            book.get("title") == book_index.get("title"),
            book.get("author") == book_index.get("author"),
            bid not in id_set,
            book_index.get("file") not in file_set,
            book.get("chatgptStatus") == "complete",
            book.get("highlightsSource") == "grok",
            isinstance(book.get("chatgptHighlights"), list),
        ]
        id_set.add(bid)
        file_set.add(book_index.get("file"))
        if not all(checks):
            ok = False
            print("FAIL", bid, checks)
        else:
            print("OK", bid, book_index.get("title"))
    print("batch_ok", ok, "found", found)

    dup_ids = [k for k, v in Counter(b.get("id") for b in books).items() if v > 1]
    dup_files = [k for k, v in Counter(b.get("file") for b in books).items() if v > 1]
    print("dup_ids_count", len(dup_ids))
    print("dup_files_count", len(dup_files))
    print("totalBooks", data.get("totalBooks"))
    print("books.length", len(books))
    print("disk_json", len(disk))


if __name__ == "__main__":
    main()
