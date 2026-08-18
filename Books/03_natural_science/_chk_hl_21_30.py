# -*- coding: utf-8 -*-
import json
from pathlib import Path

root = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\Books\03_natural_science")
for n in range(21, 31):
    p = root / f"03_natural_science-20260717-{n}.json"
    d = json.loads(p.read_text(encoding="utf-8-sig"))
    hs = d.get("chatgptHighlights", [])
    texts = []
    for x in hs:
        texts.append(x.split("、", 1)[-1] if "、" in x else x)
    uniq = len(set(texts))
    bad = any("科學問題必須能以觀察" in x for x in hs)
    print(
        f"{n:02d} n={len(hs)} uniq={uniq} src={d.get('highlightsSource')} "
        f"status={d.get('chatgptStatus')} bad={bad}"
    )
