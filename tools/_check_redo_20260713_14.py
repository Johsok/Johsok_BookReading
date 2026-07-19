# -*- coding: utf-8 -*-
"""Check redo progress for 20260713-01..60 and 20260714-01..30."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "Books" / "01_business_startup"
META = ROOT / "tools" / "_redo_books_20260713_14.json"

sys.stdout.reconfigure(encoding="utf-8")

done = []
pending = []
for row in json.loads(META.read_text(encoding="utf-8")):
    book_id = row["id"]
    path = BASE / f"{book_id}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    n = len(data.get("chatgptHighlights") or [])
    src = data.get("highlightsSource")
    status = data.get("chatgptStatus")
    ok = status == "complete" and src == "grok" and n == 150
    line = f"{book_id}\t{n}\t{status}\t{src}"
    if ok:
        done.append(line)
    else:
        pending.append(line)

print(f"done={len(done)} pending={len(pending)}")
for line in pending[:20]:
    print("PENDING", line)
if len(pending) > 20:
    print(f"... and {len(pending) - 20} more pending")
