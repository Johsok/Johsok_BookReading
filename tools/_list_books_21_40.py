# -*- coding: utf-8 -*-
from pathlib import Path
import json

root = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\Books\07_other")
out = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\tools\_tmp_07_other_21_40.json")
rows = []
for n in range(21, 41):
    p = root / f"07_other-20260716-{n}.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    rows.append({
        "n": n,
        "id": d["id"],
        "title": d.get("title", ""),
        "author": d.get("author", ""),
        "sourceUrl": d.get("sourceUrl", ""),
        "tags": d.get("tags", []),
        "summary": d.get("summary", ""),
    })
out.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
print("wrote", len(rows), out)
