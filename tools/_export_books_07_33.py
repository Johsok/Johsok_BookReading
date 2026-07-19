# -*- coding: utf-8 -*-
"""Export book metadata for redo batch 07-33."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "Books" / "01_business_startup"
OUT = ROOT / "tools" / ".redo_books_20260711_07_33.json"

books = []
for i in range(7, 34):
    book_id = f"01_business_startup-20260711-{i:02d}"
    path = BASE / f"{book_id}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    books.append(
        {
            "id": book_id,
            "title": data.get("title", ""),
            "author": data.get("author", ""),
            "summary": data.get("summary", ""),
            "tags": data.get("tags", []),
            "file": f"Books/01_business_startup/{book_id}.json",
            "categoryId": "01_business_startup",
        }
    )

OUT.write_text(json.dumps(books, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"exported {len(books)} -> {OUT}")
