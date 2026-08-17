# -*- coding: utf-8 -*-
import json
from pathlib import Path

root = Path("Books/02_psychology_growth")
ids = [
    "02_psychology_growth-20260716-48",
    "02_psychology_growth-20260716-49",
    "02_psychology_growth-20260716-50",
    "02_psychology_growth-20260716-51",
    "02_psychology_growth-20260716-52",
]
for book_id in ids:
    path = root / f"{book_id}.json"
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    highlights = data.get("chatgptHighlights", [])
    first = highlights[0][:28] if highlights else ""
    last = highlights[-1][:28] if highlights else ""
    print(
        f"{book_id}\tstatus={data.get('chatgptStatus')}\t"
        f"source={data.get('highlightsSource')}\tn={len(highlights)}\t"
        f"first={first}\tlast={last}"
    )
