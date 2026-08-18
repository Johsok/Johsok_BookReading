# -*- coding: utf-8 -*-
import json
from pathlib import Path

root = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\Books\05_food_wellness")
old = "食譜成功先從理解食材特性"
for n in range(11, 21):
    p = root / f"05_food_wellness-20260716-{n:02d}.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    hl = d.get("chatgptHighlights", [])
    print(
        p.name,
        len(hl),
        len(set(hl)),
        d.get("highlightsSource"),
        d.get("chatgptStatus"),
        any(old in x for x in hl),
        hl[0][:20] if hl else None,
        hl[-1][:8] if hl else None,
    )
