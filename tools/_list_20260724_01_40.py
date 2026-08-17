# -*- coding: utf-8 -*-
"""List 01_business_startup-20260724-01..40 titles."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "Books" / "01_business_startup"

rows = []
for i in range(1, 41):
    path = DIR / f"01_business_startup-20260724-{i:02d}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    rows.append(
        {
            "id": data["id"],
            "title": data["title"],
            "author": data["author"],
            "sourceUrl": data.get("sourceUrl", ""),
        }
    )
out = ROOT / "tools" / "._redo_queue_20260724_01_40.json"
out.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("WROTE", out, "COUNT", len(rows))
