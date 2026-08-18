# -*- coding: utf-8 -*-
import json
from pathlib import Path

base = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\Books\07_other")
for n in range(31, 41):
    f = base / f"07_other-20260717-{n:02d}.json"
    d = json.loads(f.read_text(encoding="utf-8-sig"))
    hs = d.get("chatgptHighlights", [])
    print(f"{n:02d}|{d['title']}|{d['author']}|n={len(hs)}")
