# -*- coding: utf-8 -*-
import json
from pathlib import Path

for n in range(41, 46):
    p = Path(f"Books/03_natural_science/03_natural_science-20260718-{n}.json")
    d = json.loads(p.read_text(encoding="utf-8"))
    h = d.get("chatgptHighlights") or []
    print(
        d["id"],
        "status=",
        d.get("chatgptStatus"),
        "source=",
        d.get("highlightsSource"),
        "n=",
        len(h),
    )
    if h:
        print("  first:", h[0][:40])
        print("  last:", h[-1][:40])
