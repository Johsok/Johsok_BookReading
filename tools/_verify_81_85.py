# -*- coding: utf-8 -*-
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1] / "Books" / "01_business_startup"
for i in range(81, 86):
    book_id = f"01_business_startup-20260717-{i}"
    data = json.loads((root / f"{book_id}.json").read_text(encoding="utf-8-sig"))
    highlights = data.get("chatgptHighlights", [])
    print(
        book_id,
        data.get("chatgptStatus"),
        data.get("highlightsSource"),
        len(highlights),
        "OK" if data.get("chatgptStatus") == "complete" and len(highlights) == 150 else "FAIL",
    )
