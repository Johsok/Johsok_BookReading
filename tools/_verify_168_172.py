# -*- coding: utf-8 -*-
import json
from pathlib import Path

ids = [
    "02_psychology_growth-20260716-168",
    "02_psychology_growth-20260716-169",
    "02_psychology_growth-20260716-170",
    "02_psychology_growth-20260716-171",
    "02_psychology_growth-20260716-172",
]
root = Path("Books/02_psychology_growth")
for book_id in ids:
    data = json.loads((root / f"{book_id}.json").read_text(encoding="utf-8-sig"))
    n = len(data.get("chatgptHighlights") or [])
    print(f"written\t{data['id']}\t{n}\t{data.get('highlightsSource')}\t{data.get('chatgptStatus')}")
