# -*- coding: utf-8 -*-
"""Check redo progress for books 07-33."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "Books" / "01_business_startup"

done = []
pending = []
for i in range(7, 34):
    book_id = f"01_business_startup-20260711-{i:02d}"
    path = BASE / f"{book_id}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    n = len(data.get("chatgptHighlights") or [])
    src = data.get("highlightsSource")
    status = data.get("chatgptStatus")
    ok = status == "complete" and src == "grok" and n == 150
    row = f"{book_id}\t{n}\t{status}\t{src}"
    if ok:
        done.append(row)
    else:
        pending.append(row)

print(f"done={len(done)} pending={len(pending)}")
for row in done:
    print("OK", row)
for row in pending:
    print("PENDING", row)
