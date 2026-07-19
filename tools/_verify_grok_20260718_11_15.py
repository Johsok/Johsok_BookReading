# -*- coding: utf-8 -*-
import json
from pathlib import Path

IDS = [
    "01_business_startup-20260718-11",
    "01_business_startup-20260718-12",
    "01_business_startup-20260718-13",
    "01_business_startup-20260718-14",
    "01_business_startup-20260718-15",
]

for book_id in IDS:
    path = Path(f"Books/01_business_startup/{book_id}.json")
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    highlights = data.get("chatgptHighlights", [])
    print(
        f"{book_id}\twritten\tcount={len(highlights)}\t"
        f"status={data.get('chatgptStatus')}\tsource={data.get('highlightsSource')}"
    )
    assert len(highlights) == 150
    assert data.get("chatgptStatus") == "complete"
    assert data.get("highlightsSource") == "grok"
    assert data.get("highlightsCapturedAt")
    for index, line in enumerate(highlights, 1):
        assert isinstance(line, str) and line.startswith(f"{index:03d}、")
print("ALL_OK")
