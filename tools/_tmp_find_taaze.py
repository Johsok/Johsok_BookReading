# -*- coding: utf-8 -*-
import json
from pathlib import Path

manifest = json.loads(Path("data.json").read_text(encoding="utf-8-sig"))
rows = [
    book
    for book in manifest.get("books", [])
    if book.get("workId") == "findbook-19860901-20210901-c8"
]
lines = [f"{book['id']}\t{book['title']}\t{book['author']}" for book in rows]
Path("tools/_tmp_titles.txt").write_text("\n".join(lines), encoding="utf-8")
print(len(rows))
