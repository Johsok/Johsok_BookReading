# -*- coding: utf-8 -*-
import json
from collections import Counter
from pathlib import Path

ROOT = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\Books\05_food_wellness")
for i in range(21, 31):
    data = json.loads((ROOT / f"05_food_wellness-20260716-{i:02d}.json").read_text(encoding="utf-8"))
    bodies = [s.split("、", 1)[1] for s in data["chatgptHighlights"]]
    pref = Counter(b[:8] for b in bodies)
    bad = [(k, v) for k, v in pref.most_common() if v >= 2]
    if bad:
        print(i, bad[:20])
