# -*- coding: utf-8 -*-
"""Apply 150-point highlights into healthcare book JSON files."""
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\Books\04_healthcare")
TZ = timezone(timedelta(hours=8))
STAMP = datetime.now(TZ).strftime("%Y-%m-%dT%H:%M:%S+08:00")
UPDATED = "2026-08-18"

HL = {}
for name in ["_hl_66_68.py", "_hl_69_71.py", "_hl_17_01_03.py", "_hl_17_04_05.py"]:
    ns = {}
    exec((ROOT / name).read_text(encoding="utf-8"), ns)
    HL.update(ns["HL"])


def numbered(book_id, items):
    if len(items) != 150:
        raise SystemExit(f"{book_id} need 150, got {len(items)}")
    out = []
    for i, t in enumerate(items, 1):
        t = t.strip()
        if len(t) > 4 and t[3:4] == "、" and t[:3].isdigit():
            t = t.split("、", 1)[-1]
        out.append(f"{i:03d}、{t}")
    return out


for book_id, items in HL.items():
    path = ROOT / f"{book_id}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["chatgptHighlights"] = numbered(book_id, items)
    data["chatgptStatus"] = "complete"
    data["highlightsSource"] = "grok"
    data["highlightsCapturedAt"] = STAMP
    data["updatedAt"] = UPDATED
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)
    print("OK", book_id, len(data["chatgptHighlights"]))
