# -*- coding: utf-8 -*-
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "Books" / "02_psychology_growth"
OUT = ROOT / "tools" / ".redo_60_catalog.json"

catalog = []
for date in ("20260714", "20260715"):
    for n in range(1, 31):
        book_id = f"02_psychology_growth-{date}-{n:02d}"
        path = BASE / f"{book_id}.json"
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        catalog.append(
            {
                "id": book_id,
                "title": data.get("title"),
                "author": data.get("author"),
                "tags": data.get("tags") or [],
                "summary": data.get("summary") or "",
                "file": f"Books/02_psychology_growth/{book_id}.json",
            }
        )

OUT.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"wrote {len(catalog)} books to {OUT}")
