# -*- coding: utf-8 -*-
import json
from pathlib import Path

for i in ["151", "152", "153", "154", "155"]:
    p = Path(f"Books/02_psychology_growth/02_psychology_growth-20260718-{i}.json")
    d = json.loads(p.read_text(encoding="utf-8"))
    h = d.get("chatgptHighlights", [])
    print(
        f"{d['id']}\tstatus={d.get('chatgptStatus')}\t"
        f"source={d.get('highlightsSource')}\tcount={len(h)}"
    )
