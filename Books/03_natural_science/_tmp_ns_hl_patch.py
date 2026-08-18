# -*- coding: utf-8 -*-
"""Atomically overwrite chatgptHighlights for selected natural-science books."""
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\Books\03_natural_science")
STAMP = datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S%z")
STAMP = STAMP[:-2] + ":" + STAMP[-2:] if len(STAMP) >= 5 else STAMP
UPDATED = "2026-08-18"


def numbered(items):
    if len(items) != 150:
        raise SystemExit(f"need 150, got {len(items)}")
    starts = [t[:8] for t in items]
    if len(set(items)) != 150:
        raise SystemExit("duplicate full sentences")
    return [f"{i:03d}、{t}" for i, t in enumerate(items, 1)]


def patch(filename, items, summary=None):
    path = ROOT / filename
    data = json.loads(path.read_text(encoding="utf-8"))
    data["chatgptHighlights"] = numbered(items)
    data["chatgptStatus"] = "complete"
    data["highlightsSource"] = "grok"
    data["highlightsCapturedAt"] = STAMP
    data["updatedAt"] = UPDATED
    if summary:
        data["summary"] = summary
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)
    print(f"OK {filename} n={len(data['chatgptHighlights'])}")
