# -*- coding: utf-8 -*-
import json
from pathlib import Path

ids = [
    "02_psychology_growth-20260716-103",
    "02_psychology_growth-20260716-104",
    "02_psychology_growth-20260716-105",
    "02_psychology_growth-20260716-106",
    "02_psychology_growth-20260716-107",
]
root = Path("Books/02_psychology_growth")
for i in ids:
    d = json.loads((root / f"{i}.json").read_text(encoding="utf-8-sig"))
    h = d.get("chatgptHighlights", [])
    print(
        i,
        d.get("chatgptStatus"),
        d.get("highlightsSource"),
        len(h),
        h[0][:28] if h else "",
        h[-1][:28] if h else "",
    )
