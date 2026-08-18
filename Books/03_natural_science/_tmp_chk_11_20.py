# -*- coding: utf-8 -*-
import json
from pathlib import Path

ROOT = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\Books\03_natural_science")
old = "閱讀時可先確認作者如何定義問題"
for i in range(11, 21):
    name = f"03_natural_science-20260716-{i:02d}.json"
    data = json.loads((ROOT / name).read_text(encoding="utf-8"))
    hs = data["chatgptHighlights"]
    assert len(hs) == 150, (name, len(hs))
    assert data["chatgptStatus"] == "complete"
    assert data["highlightsSource"] == "grok"
    for n, line in enumerate(hs, 1):
        assert line.startswith(f"{n:03d}、"), (name, n, line[:20])
        assert old not in line
    print("OK", name, data["title"][:20], "src", data["highlightsSource"])
