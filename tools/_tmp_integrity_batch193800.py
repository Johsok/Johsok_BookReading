# -*- coding: utf-8 -*-
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))
books = data["books"]
errors = []
if data.get("totalBooks") != len(books):
    errors.append(f"totalBooks mismatch {data.get('totalBooks')} != {len(books)}")
ids = [item.get("id") for item in books]
files = [str(item.get("file") or "").replace("\\", "/") for item in books]
dup_ids = [key for key, count in Counter(ids).items() if count > 1]
dup_files = [key for key, count in Counter(files).items() if count > 1]
if dup_ids:
    errors.append(f"dup ids {len(dup_ids)}")
if dup_files:
    errors.append(f"dup files {len(dup_files)}")
indexed = set(files)
disk = [path.relative_to(ROOT).as_posix() for path in (ROOT / "Books").rglob("*.json")]
missing = [file for file in indexed if not (ROOT / file).exists()]
orphan = sorted(set(disk) - indexed)
if missing:
    errors.append(f"missing files {len(missing)} {missing[:5]}")
inconsistent = []
for item in books:
    path = ROOT / str(item.get("file") or "")
    if not path.exists():
        continue
    book = json.loads(path.read_text(encoding="utf-8-sig"))
    expected = f"Books/{item.get('categoryId')}/{item.get('id')}.json"
    if (
        item.get("file") != expected
        or book.get("id") != item.get("id")
        or book.get("categoryId") != item.get("categoryId")
        or book.get("title") != item.get("title")
        or book.get("author") != item.get("author")
    ):
        inconsistent.append(item.get("id"))
if inconsistent:
    errors.append(f"inconsistent {len(inconsistent)} {inconsistent[:5]}")

batch = [f"01_business_startup-20260818-0{index}" for index in range(3, 8)] + [
    f"02_psychology_growth-20260818-0{index}" for index in range(3, 8)
]
print("BATCH")
for book_id in batch:
    matches = [item for item in books if item.get("id") == book_id]
    if len(matches) != 1:
        print("MISSING_INDEX", book_id, len(matches))
        continue
    book = json.loads((ROOT / matches[0]["file"]).read_text(encoding="utf-8-sig"))
    highlights = book.get("chatgptHighlights") or []
    print(
        book_id,
        book.get("chatgptStatus"),
        book.get("highlightsSource"),
        "hl",
        len(highlights),
        book.get("title")[:24],
    )
print("totalBooks", data.get("totalBooks"))
print("books.length", len(books))
print("disk_json", len(disk))
print("orphan_count", len(orphan))
if orphan:
    print("orphan_sample", orphan[:10])
print("errors", errors)
