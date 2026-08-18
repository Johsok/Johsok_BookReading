# -*- coding: utf-8 -*-
"""Overwrite chatgptHighlights for natural-science books 11-20."""
import json
from datetime import datetime
from pathlib import Path

from _hl_data_11_15 import BOOKS as BOOKS_A
from _hl_data_16_20 import BOOKS as BOOKS_B

ROOT = Path(__file__).resolve().parent
STAMP = datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S%z")
STAMP = STAMP[:-2] + ":" + STAMP[-2:] if len(STAMP) >= 5 else STAMP
UPDATED = "2026-08-18"


def numbered(items):
    if len(items) != 150:
        raise SystemExit(f"need 150, got {len(items)}")
    if len(set(items)) != 150:
        raise SystemExit("duplicate items")
    if any(not str(t).strip() for t in items):
        raise SystemExit("empty item")
    return [f"{i:03d}、{t}" for i, t in enumerate(items, 1)]


def patch(filename, payload):
    path = ROOT / filename
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    data["chatgptHighlights"] = numbered(payload["items"])
    data["chatgptStatus"] = "complete"
    data["highlightsSource"] = "grok"
    data["highlightsCapturedAt"] = STAMP
    data["updatedAt"] = UPDATED
    if payload.get("summary"):
        data["summary"] = payload["summary"]
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)
    print(f"OK {filename} n={len(data['chatgptHighlights'])}")


def main():
    books = {}
    books.update(BOOKS_A)
    books.update(BOOKS_B)
    expected = [f"03_natural_science-20260717-{i:02d}.json" for i in range(11, 21)]
    missing = [name for name in expected if name not in books]
    if missing:
        raise SystemExit(f"missing books: {missing}")
    for name in expected:
        patch(name, books[name])


if __name__ == "__main__":
    main()
