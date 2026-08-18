# -*- coding: utf-8 -*-
import json
from pathlib import Path

ROOT = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\Books\04_healthcare")
ids = [
    "04_healthcare-20260716-66",
    "04_healthcare-20260716-67",
    "04_healthcare-20260716-68",
    "04_healthcare-20260716-69",
    "04_healthcare-20260716-70",
    "04_healthcare-20260716-71",
    "04_healthcare-20260717-01",
    "04_healthcare-20260717-02",
    "04_healthcare-20260717-03",
    "04_healthcare-20260717-04",
    "04_healthcare-20260717-05",
]
bad = "健康資訊應區分預防"
for bid in ids:
    d = json.loads((ROOT / f"{bid}.json").read_text(encoding="utf-8"))
    hs = d["chatgptHighlights"]
    assert len(hs) == 150
    for i, line in enumerate(hs, 1):
        assert line.startswith(f"{i:03d}、"), (bid, i, line[:20])
        assert bad not in line
        assert "｜" not in line
        assert "本書" not in line
        assert "實作面第" not in line
    texts = [x.split("、", 1)[1] for x in hs]
    if len(set(texts)) != 150:
        print("DUP", bid, 150 - len(set(texts)))
    else:
        print("PASS", bid, d["title"][:18], d["highlightsSource"], d["chatgptHighlights"][0][:28])
