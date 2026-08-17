# -*- coding: utf-8 -*-
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "Books" / "02_psychology_growth"
IDS = [
    "02_psychology_growth-20260710-42",
    "02_psychology_growth-20260710-43",
    "02_psychology_growth-20260710-44",
] + [f"02_psychology_growth-20260713-{i:02d}" for i in range(1, 41)]

rows = []
for bid in IDS:
    data = json.loads((DIR / f"{bid}.json").read_text(encoding="utf-8-sig"))
    rows.append(
        {
            "id": bid,
            "title": data.get("title", ""),
            "author": data.get("author", ""),
            "summary": data.get("summary", ""),
            "tags": data.get("tags", []),
            "n": len(data.get("chatgptHighlights") or []),
            "src": data.get("highlightsSource"),
        }
    )

out = ROOT / "tools" / "_redo_queue_20260713_psych.json"
out.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
for i, row in enumerate(rows, 1):
    print(f"{i:02d}\t{row['id']}\t{row['author']}\t{row['title']}\tn={row['n']}\tsrc={row['src']}")
print(f"TOTAL\t{len(rows)}")
