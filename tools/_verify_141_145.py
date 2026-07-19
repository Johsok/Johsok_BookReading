# -*- coding: utf-8 -*-
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1] / "Books" / "01_business_startup"
for i in range(141, 146):
    bid = f"01_business_startup-20260717-{i}"
    d = json.loads((root / f"{bid}.json").read_text(encoding="utf-8-sig"))
    print(
        bid,
        d.get("highlightsSource"),
        d.get("chatgptStatus"),
        len(d.get("chatgptHighlights") or []),
        (d.get("chatgptHighlights") or [""])[0][:40],
    )
