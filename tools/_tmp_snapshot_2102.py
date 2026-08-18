# -*- coding: utf-8 -*-
"""Stable snapshot index-link check for findbook-20260818-2102."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BATCH_IDS = [
    "01_business_startup-20260818-13",
    "01_business_startup-20260818-14",
    "01_business_startup-20260818-15",
    "01_business_startup-20260818-16",
    "01_business_startup-20260818-17",
    "02_psychology_growth-20260818-13",
    "02_psychology_growth-20260818-14",
    "02_psychology_growth-20260818-15",
    "02_psychology_growth-20260818-16",
    "02_psychology_growth-20260818-17",
    "03_natural_science-20260818-03",
    "03_natural_science-20260818-04",
    "03_natural_science-20260818-05",
    "03_natural_science-20260818-06",
    "03_natural_science-20260818-07",
]


def snapshot() -> tuple[dict, float, int]:
    path = ROOT / "data.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    return data, path.stat().st_mtime, len(data.get("books", []))


def check(data: dict) -> list[str]:
    errors: list[str] = []
    books = data.get("books", [])
    if data.get("totalBooks") != len(books):
        errors.append(f"totalBooks {data.get('totalBooks')} != {len(books)}")

    ids = [item.get("id") for item in books]
    files = [str(item.get("file") or "").replace("\\", "/") for item in books]
    dup_ids = [key for key, count in Counter(ids).items() if count > 1]
    dup_files = [key for key, count in Counter(files).items() if count > 1]
    if dup_ids:
        errors.append(f"dup ids {dup_ids[:5]}")
    if dup_files:
        errors.append(f"dup files {dup_files[:5]}")

    indexed = set(files)
    disk = [path.relative_to(ROOT).as_posix() for path in (ROOT / "Books").rglob("*.json")]
    extra = sorted(set(disk) - indexed)
    missing = sorted(indexed - set(disk))
    if extra:
        errors.append(f"orphan json {len(extra)} e.g. {extra[:3]}")
    if missing:
        errors.append(f"missing files {len(missing)} e.g. {missing[:3]}")
    if len(disk) != len(books):
        errors.append(f"disk json {len(disk)} != books {len(books)}")

    found = 0
    for item in books:
        book_id = item.get("id")
        expected = f"Books/{item.get('categoryId')}/{book_id}.json"
        relative = str(item.get("file") or "").replace("\\", "/")
        path = ROOT / relative
        if not path.exists():
            errors.append(f"missing {relative}")
            continue
        book = json.loads(path.read_text(encoding="utf-8-sig"))
        if relative != expected:
            errors.append(f"path {relative} != {expected}")
        if book.get("id") != item.get("id"):
            errors.append(f"id mismatch {book_id}")
        if book.get("categoryId") != item.get("categoryId"):
            errors.append(f"category mismatch {book_id}")
        if book.get("title") != item.get("title"):
            errors.append(f"title mismatch {book_id}")
        if book.get("author") != item.get("author"):
            errors.append(f"author mismatch {book_id}")
        if book_id in BATCH_IDS:
            found += 1
            if book.get("chatgptStatus") != "complete":
                errors.append(f"status {book_id} {book.get('chatgptStatus')}")
            if book.get("highlightsSource") != "grok":
                errors.append(f"source {book_id} {book.get('highlightsSource')}")
            highlights = book.get("chatgptHighlights")
            if not isinstance(highlights, list) or not highlights:
                errors.append(f"empty highlights {book_id}")
    if found != len(BATCH_IDS):
        errors.append(f"batch found {found} != {len(BATCH_IDS)}")
    return errors


def main() -> int:
    first, mtime1, count1 = snapshot()
    generated1 = first.get("generatedAt")
    errors = check(first)
    second, mtime2, count2 = snapshot()
    if (
        generated1 != second.get("generatedAt")
        or mtime1 != mtime2
        or count1 != count2
    ):
        raise SystemExit("snapshot moved; retry needed")
    print("totalBooks", first.get("totalBooks"))
    print("books.length", count1)
    print("generatedAt", generated1)
    if errors:
        for item in errors:
            print("ERROR", item)
        raise SystemExit(1)
    print("snapshot-ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
