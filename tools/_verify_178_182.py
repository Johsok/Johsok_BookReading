# -*- coding: utf-8 -*-
import json
from pathlib import Path

ids = [
    "02_psychology_growth-20260716-178",
    "02_psychology_growth-20260716-179",
    "02_psychology_growth-20260716-180",
    "02_psychology_growth-20260716-181",
    "02_psychology_growth-20260716-182",
]
root = Path("Books/02_psychology_growth")
for book_id in ids:
    data = json.loads((root / f"{book_id}.json").read_text(encoding="utf-8-sig"))
    print(
        f"written/{data['id']}/{len(data['chatgptHighlights'])}/"
        f"{data.get('highlightsSource')}/{data.get('chatgptStatus')}"
    )
