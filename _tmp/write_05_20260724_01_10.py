# -*- coding: utf-8 -*-
"""Rewrite 150 book-specific highlights for 05_food_wellness-20260724-01..10."""
from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading")
BOOKS = ROOT / "Books" / "05_food_wellness"
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "_tmp"))
from findbook_writer import validate_highlights  # noqa: E402

UPDATED = "2026-08-18"
CAPTURED = "2026-08-18T10:40:00+08:00"


def atomic_write(path: Path, data: dict) -> None:
    text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    fd, tmp = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            try:
                os.remove(tmp)
            except OSError:
                pass


def numbered(bodies: list[str]) -> list[str]:
    return [f"{i:03d}、{t}" for i, t in enumerate(bodies, 1)]


def main() -> None:
    from hl_20260724_bodies import BOOKS as PAYLOAD

    results = []
    for json_name, bodies in PAYLOAD.items():
        path = BOOKS / json_name
        book_id = json_name.replace(".json", "")
        if len(bodies) != 150:
            raise SystemExit(f"{json_name}: expected 150, got {len(bodies)}")
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        lines = numbered(bodies)
        validate_highlights(book_id, lines, data.get("title", ""), data.get("author", ""))
        data["chatgptHighlights"] = lines
        data["chatgptStatus"] = "complete"
        data["highlightsSource"] = "grok"
        data["highlightsCapturedAt"] = CAPTURED
        data["updatedAt"] = UPDATED
        atomic_write(path, data)
        saved = json.loads(path.read_text(encoding="utf-8-sig"))
        validate_highlights(
            book_id,
            saved["chatgptHighlights"],
            saved.get("title", ""),
            saved.get("author", ""),
        )
        results.append({"file": json_name, "count": 150, "ok": True})
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
