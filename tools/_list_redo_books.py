# -*- coding: utf-8 -*-
"""List books that need highlight redo."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "Books" / "01_business_startup"
IDS = [f"01_business_startup-20260713-{i:02d}" for i in range(1, 61)] + [
    f"01_business_startup-20260714-{i:02d}" for i in range(1, 31)
]


def main() -> None:
    rows = []
    for bid in IDS:
        path = DIR / f"{bid}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        rows.append(
            {
                "id": bid,
                "title": data["title"],
                "author": data["author"],
                "highlightsSource": data.get("highlightsSource"),
                "n": len(data.get("chatgptHighlights") or []),
            }
        )
    out = ROOT / "tools" / "_redo_books_20260713_14.json"
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for row in rows:
        print(f"{row['id']}\t{row['highlightsSource']}\t{row['n']}\t{row['title']}\t{row['author']}")
    print(f"TOTAL\t{len(rows)}")


if __name__ == "__main__":
    main()
