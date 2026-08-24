# -*- coding: utf-8 -*-
"""Write Grok 150 highlights into a reserved book JSON without content validation."""
from __future__ import annotations

import argparse
from pathlib import Path

import findbook_writer as writer


def parse_highlights(text: str) -> list[str]:
    lines = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line[:3].isdigit() and "、" in line[:6]:
            lines.append(line)
    return lines


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--book-id", required=True)
    parser.add_argument("--highlights-file", required=True)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    manifest = writer.read_json(root / "data.json")
    matches = [book for book in manifest.get("books", []) if book.get("id") == args.book_id]
    if len(matches) != 1:
        raise SystemExit(f"{args.book_id} 在 data.json 必須剛好出現一次")
    relative_file = str(matches[0]["file"])
    book_path = root / relative_file
    book = writer.read_json(book_path)
    text = Path(args.highlights_file).read_text(encoding="utf-8-sig")
    highlights = parse_highlights(text)
    if len(highlights) > 150:
        highlights = highlights[:150]
    book["chatgptHighlights"] = highlights
    book["chatgptStatus"] = "complete"
    book["highlightsSource"] = "grok"
    book["highlightsCapturedAt"] = writer.now_iso()
    book["updatedAt"] = writer.now_iso()[:10]
    writer.write_json_atomic(book_path, book)
    saved = writer.read_json(book_path)
    if saved.get("id") != args.book_id:
        raise SystemExit(f"{args.book_id} 寫後找不到")
    print(f"written\t{args.book_id}\t{len(saved.get('chatgptHighlights', []))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
