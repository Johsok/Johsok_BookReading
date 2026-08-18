# -*- coding: utf-8 -*-
import json
import re
from collections import Counter
from pathlib import Path

root = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\Books\07_other")
old_frag = "理解作品需先辨認作者所處的時代"
for n in range(1, 11):
    p = root / f"07_other-20260717-{n:02d}.json"
    data = json.loads(p.read_text(encoding="utf-8-sig"))
    hs = data["chatgptHighlights"]
    assert len(hs) == 150, (n, len(hs))
    assert data.get("highlightsSource") == "grok"
    for i, line in enumerate(hs, 1):
        if not line.startswith(f"{i:03d}、"):
            raise SystemExit(f"bad num {p.name} {i}: {line[:50]}")
        if old_frag in line:
            raise SystemExit(f"old template {p.name} {i}")
    dups = [k for k, v in Counter(hs).items() if v > 1]
    eng = [(i, line) for i, line in enumerate(hs, 1) if re.search(r"[A-Za-z]{4,}", line)]
    print(p.name, "ok", "dups", len(dups), "latin", len(eng))
    for i, line in eng:
        print(" ", i, line[:80])
