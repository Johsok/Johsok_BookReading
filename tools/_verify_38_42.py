# -*- coding: utf-8 -*-
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
ids = [
    "02_psychology_growth-20260716-38",
    "02_psychology_growth-20260716-39",
    "02_psychology_growth-20260716-40",
    "02_psychology_growth-20260716-41",
    "02_psychology_growth-20260716-42",
]
for i in ids:
    p = root / "Books/02_psychology_growth" / f"{i}.json"
    d = json.loads(p.read_text(encoding="utf-8-sig"))
    h = d.get("chatgptHighlights", [])
    print(f"{i}\tstatus={d.get('chatgptStatus')}\tsource={d.get('highlightsSource')}\tn={len(h)}\tupdated={d.get('updatedAt')}")
