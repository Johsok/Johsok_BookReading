# -*- coding: utf-8 -*-
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1] / "Books" / "01_business_startup"
for i in ["206", "207", "208", "209", "210"]:
    bid = f"01_business_startup-20260717-{i}"
    d = json.loads((root / f"{bid}.json").read_text(encoding="utf-8-sig"))
    n = len(d.get("chatgptHighlights") or [])
    print(f"{bid}\t{d.get('chatgptStatus')}\t{d.get('highlightsSource')}\t{n}")
