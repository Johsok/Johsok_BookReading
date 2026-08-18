# -*- coding: utf-8 -*-
"""Write Grok highlights without content validation; only index-link check."""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import findbook_writer as writer  # noqa: E402

TAIPEI = ZoneInfo("Asia/Taipei")


def highlights_from_text(text: str) -> list[str]:
    lines = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("```"):
            continue
        lines.append(line)
    return lines


def check_link(manifest: dict, book: dict, relative_file: str) -> None:
    book_id = book["id"]
    matches = [item for item in manifest.get("books", []) if item.get("id") == book_id]
    if len(matches) != 1:
        raise RuntimeError(f"{book_id} index id not unique")
    index_book = matches[0]
    if index_book.get("file") != relative_file:
        raise RuntimeError(f"{book_id} file mismatch")
    if index_book.get("categoryId") != book.get("categoryId"):
        raise RuntimeError(f"{book_id} category mismatch")
    if index_book.get("title") != book.get("title"):
        raise RuntimeError(f"{book_id} title mismatch")
    if index_book.get("author") != book.get("author"):
        raise RuntimeError(f"{book_id} author mismatch")
    files = [item.get("file") for item in manifest.get("books", [])]
    if files.count(relative_file) != 1:
        raise RuntimeError(f"{book_id} file path not unique")


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit("usage: _tmp_write_hl_noguard.py <book-id> <highlights.txt>")
    book_id = sys.argv[1]
    highlights = highlights_from_text(Path(sys.argv[2]).read_text(encoding="utf-8"))
    manifest = writer.read_json(ROOT / "data.json")
    matches = [item for item in manifest.get("books", []) if item.get("id") == book_id]
    if len(matches) != 1:
        raise RuntimeError(f"{book_id} missing from data.json")
    relative_file = str(matches[0]["file"])
    book_path = ROOT / relative_file
    book = writer.read_json(book_path)
    book["chatgptHighlights"] = highlights
    book["chatgptStatus"] = "complete"
    book["highlightsSource"] = "grok"
    book["highlightsCapturedAt"] = datetime.now(TAIPEI).isoformat(timespec="seconds")
    book["updatedAt"] = datetime.now(TAIPEI).date().isoformat()
    writer.write_json_atomic(book_path, book)
    saved = writer.read_json(book_path)
    check_link(writer.read_json(ROOT / "data.json"), saved, relative_file)
    print(f"written\t{book_id}\tlines={len(saved.get('chatgptHighlights', []))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
