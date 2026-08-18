# -*- coding: utf-8 -*-
"""Overwrite chatgptHighlights for natural-science books 02-10."""
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\Books\03_natural_science")
STAMP = datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S%z")
STAMP = STAMP[:-2] + ":" + STAMP[-2:] if len(STAMP) >= 5 else STAMP
UPDATED = "2026-08-18"

from _tmp_ns_hl_data import BOOKS
import _tmp_ns_hl_b03  # noqa: F401
import _tmp_ns_hl_b04  # noqa: F401
import _tmp_ns_hl_b05  # noqa: F401
import _tmp_ns_hl_b06  # noqa: F401
import _tmp_ns_hl_b07  # noqa: F401
import _tmp_ns_hl_b08  # noqa: F401
import _tmp_ns_hl_b09  # noqa: F401
import _tmp_ns_hl_b10  # noqa: F401
from _tmp_ns_pad import PAD


def collect(block, extras):
    items = [ln.strip() for ln in block.strip().splitlines() if ln.strip()]
    items.extend(extras)
    if len(items) != 150:
        raise SystemExit(f"need 150, got {len(items)}")
    seen = set()
    for t in items:
        if t in seen:
            raise SystemExit(f"duplicate: {t[:40]}")
        seen.add(t)
    return [f"{i:03d}、{t}" for i, t in enumerate(items, 1)]


def patch(filename, items):
    path = ROOT / filename
    data = json.loads(path.read_text(encoding="utf-8"))
    data["chatgptHighlights"] = items
    data["chatgptStatus"] = "complete"
    data["highlightsSource"] = "grok"
    data["highlightsCapturedAt"] = STAMP
    data["updatedAt"] = UPDATED
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)
    print(f"OK {filename} n={len(items)}")


if __name__ == "__main__":
    for name, block in BOOKS.items():
        patch(name, collect(block, PAD.get(name, [])))
