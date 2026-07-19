# -*- coding: utf-8 -*-
"""Print next pending books for dispatch."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.stdout.reconfigure(encoding="utf-8")
META = json.loads((ROOT / "tools" / "_redo_books_20260713_14.json").read_text(encoding="utf-8"))
BASE = ROOT / "Books" / "01_business_startup"

pending = []
for row in META:
    data = json.loads((BASE / f"{row['id']}.json").read_text(encoding="utf-8"))
    ok = (
        data.get("chatgptStatus") == "complete"
        and data.get("highlightsSource") == "grok"
        and len(data.get("chatgptHighlights") or []) == 150
    )
    if not ok:
        pending.append(row)

start = int(sys.argv[1]) if len(sys.argv) > 1 else 0
n = int(sys.argv[2]) if len(sys.argv) > 2 else 8
for row in pending[start : start + n]:
    summary = (json.loads((BASE / f"{row['id']}.json").read_text(encoding="utf-8")).get("summary") or "")[:120]
    print(f"{row['id']}\t{row['author']}\t{row['title']}\t{summary}")
print(f"TOTAL_PENDING\t{len(pending)}")
