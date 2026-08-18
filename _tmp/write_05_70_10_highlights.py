# -*- coding: utf-8 -*-
"""Write 150 book-specific highlights into 05_food_wellness JSON files."""
from __future__ import annotations

import json
import os
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading")
BOOKS = ROOT / "Books" / "05_food_wellness"
TMP = ROOT / "_tmp"
SYS_TOOLS = ROOT / "tools"
sys.path.insert(0, str(SYS_TOOLS))
from findbook_writer import validate_highlights  # noqa: E402

UPDATED = "2026-08-18"
CAPTURED = "2026-08-18T10:30:00+08:00"

MAPPING = [
    ("hl_70.txt", "05_food_wellness-20260716-70.json"),
    ("hl_71.txt", "05_food_wellness-20260716-71.json"),
    ("hl_01.txt", "05_food_wellness-20260717-01.json"),
    ("hl_02.txt", "05_food_wellness-20260717-02.json"),
    ("hl_03.txt", "05_food_wellness-20260717-03.json"),
    ("hl_04.txt", "05_food_wellness-20260717-04.json"),
    ("hl_05.txt", "05_food_wellness-20260717-05.json"),
    ("hl_06.txt", "05_food_wellness-20260717-06.json"),
    ("hl_07.txt", "05_food_wellness-20260717-07.json"),
    ("hl_08.txt", "05_food_wellness-20260717-08.json"),
    ("hl_09.txt", "05_food_wellness-20260717-09.json"),
    ("hl_10.txt", "05_food_wellness-20260717-10.json"),
]


def load_bodies(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8-sig")
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    return lines


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


def main() -> None:
    results = []
    for txt_name, json_name in MAPPING:
        txt_path = TMP / txt_name
        json_path = BOOKS / json_name
        bodies = load_bodies(txt_path)
        book_id = json_name.replace(".json", "")
        if len(bodies) != 150:
            raise SystemExit(f"{txt_name}: expected 150, got {len(bodies)}")
        with json_path.open("r", encoding="utf-8-sig") as f:
            data = json.load(f)
        numbered = [f"{i:03d}、{t}" for i, t in enumerate(bodies, 1)]
        validate_highlights(book_id, numbered, data.get("title", ""), data.get("author", ""))
        data["chatgptHighlights"] = numbered
        data["chatgptStatus"] = "complete"
        data["highlightsSource"] = "grok"
        data["highlightsCapturedAt"] = CAPTURED
        data["updatedAt"] = UPDATED
        atomic_write(json_path, data)
        saved = json.loads(json_path.read_text(encoding="utf-8-sig"))
        validate_highlights(book_id, saved["chatgptHighlights"], saved.get("title", ""), saved.get("author", ""))
        results.append({"file": json_name, "count": len(saved["chatgptHighlights"]), "ok": True})
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
