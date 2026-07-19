# -*- coding: utf-8 -*-
import json
from pathlib import Path

ids = [
    "01_business_startup-20260718-36",
    "01_business_startup-20260718-37",
    "01_business_startup-20260718-38",
    "01_business_startup-20260718-39",
    "01_business_startup-20260718-40",
]
for book_id in ids:
    path = Path(f"Books/01_business_startup/{book_id}.json")
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    highlights = data.get("chatgptHighlights") or []
    print(
        book_id,
        data.get("chatgptStatus"),
        data.get("highlightsSource"),
        len(highlights),
        highlights[0][:24] if highlights else "-",
        highlights[-1][:24] if highlights else "-",
    )
