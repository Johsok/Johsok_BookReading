# -*- coding: utf-8 -*-
from pathlib import Path
import json

root = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\Books\07_other")
old_sig = "理解作品需先辨認作者所處的時代"
out = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\tools\_check_07_21_40.json")
rows = []
for n in range(21, 41):
    p = root / f"07_other-20260716-{n}.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    hl = d.get("chatgptHighlights") or []
    first = hl[0] if hl else ""
    last = hl[-1] if hl else ""
    is_old = old_sig in first or any(old_sig in (x or "") for x in hl[:5])
    rows.append({
        "n": n,
        "id": d.get("id"),
        "title": d.get("title"),
        "count": len(hl),
        "status": d.get("chatgptStatus"),
        "source": d.get("highlightsSource"),
        "updatedAt": d.get("updatedAt"),
        "old": is_old,
        "first": first[:80],
        "last": last[:80],
        "n050": (hl[49][:80] if len(hl) >= 50 else ""),
    })
out.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
print("ok", sum(1 for r in rows if r["count"] == 150 and r["source"] == "grok" and not r["old"]))
print("old", [r["n"] for r in rows if r["old"]])
print("bad_count", [r["n"] for r in rows if r["count"] != 150])
