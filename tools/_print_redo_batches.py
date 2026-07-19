# -*- coding: utf-8 -*-
"""Print redo book batches for dispatch."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
rows = json.loads(Path(__file__).with_name("_redo_books_20260716_03_162.json").read_text(encoding="utf-8"))
start = int(sys.argv[1]) if len(sys.argv) > 1 else 40
end = int(sys.argv[2]) if len(sys.argv) > 2 else 80
size = int(sys.argv[3]) if len(sys.argv) > 3 else 4
for i in range(start, min(end, len(rows)), size):
    chunk = rows[i : i + size]
    print("===BATCH", chunk[0]["id"], "-", chunk[-1]["id"], "===")
    for r in chunk:
        print(r["id"] + "\t" + r["author"] + "\t" + r["title"])
