# -*- coding: utf-8 -*-
"""Validate and overwrite chatgptHighlights for 03_natural_science-20260724-01..10."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading")
sys.path.insert(0, str(ROOT / "tools"))
from findbook_writer import validate_highlights, write_json_atomic, now_iso  # noqa: E402
from datetime import datetime
from zoneinfo import ZoneInfo

TAIPEI = ZoneInfo("Asia/Taipei")
BOOKS_DIR = ROOT / "Books" / "03_natural_science"
TMP = ROOT / "_tmp"

IDS = [f"03_natural_science-20260724-{i:02d}" for i in range(1, 11)]


def main() -> None:
    for book_id in IDS:
        n = book_id.rsplit("-", 1)[-1]
        src = TMP / f"ns24_hl_{n}.json"
        payload = json.loads(src.read_text(encoding="utf-8-sig"))
        bodies = payload["bodies"]
        if len(bodies) != 150:
            raise SystemExit(f"{src.name} count={len(bodies)}")
        highlights = [f"{i:03d}、{body.strip()}" for i, body in enumerate(bodies, 1)]
        book_path = BOOKS_DIR / f"{book_id}.json"
        book = json.loads(book_path.read_text(encoding="utf-8-sig"))
        title = str(book.get("title", ""))
        author = str(book.get("author", ""))
        cleaned = validate_highlights(book_id, highlights, title, author)
        book["chatgptHighlights"] = cleaned
        book["chatgptStatus"] = "complete"
        book["highlightsSource"] = "grok"
        book["highlightsCapturedAt"] = now_iso()
        book["updatedAt"] = datetime.now(TAIPEI).date().isoformat()
        write_json_atomic(book_path, book)
        saved = json.loads(book_path.read_text(encoding="utf-8-sig"))
        validate_highlights(book_id, saved["chatgptHighlights"], title, author)
        print(f"written\t{book_id}\t{len(saved['chatgptHighlights'])}")


if __name__ == "__main__":
    main()
