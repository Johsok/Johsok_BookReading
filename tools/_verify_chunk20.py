# -*- coding: utf-8 -*-
import json
from pathlib import Path

ids = [
    "02_psychology_growth-20260718-156",
    "02_psychology_growth-20260718-157",
    "02_psychology_growth-20260718-158",
    "02_psychology_growth-20260718-159",
    "02_psychology_growth-20260718-160",
]
root = Path(__file__).resolve().parents[1]
for bid in ids:
    p = root / "Books" / "02_psychology_growth" / f"{bid}.json"
    d = json.loads(p.read_text(encoding="utf-8-sig"))
    n = len(d.get("chatgptHighlights") or [])
    print(f"{bid}\t{d.get('chatgptStatus')}\t{n}\t{d.get('highlightsSource')}")
