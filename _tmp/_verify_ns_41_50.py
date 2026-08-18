# -*- coding: utf-8 -*-
import json
import sys
from pathlib import Path

sys.path.insert(0, r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\tools")
from findbook_writer import validate_highlights

root = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\Books\03_natural_science")
generic = "科學問題必須能以觀察"
for i in range(41, 51):
    path = root / f"03_natural_science-20260717-{i}.json"
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    validate_highlights(
        data["id"],
        data["chatgptHighlights"],
        data.get("title", ""),
        data.get("author", ""),
    )
    assert data["chatgptStatus"] == "complete"
    assert data["highlightsSource"] == "grok"
    assert len(data["chatgptHighlights"]) == 150
    assert generic not in data["chatgptHighlights"][0]
    print(i, "OK", data["id"], len(data["chatgptHighlights"]))
