# -*- coding: utf-8 -*-
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for i in ["136", "137", "138", "139", "140"]:
    p = ROOT / "Books" / "02_psychology_growth" / f"02_psychology_growth-20260718-{i}.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    h = d.get("chatgptHighlights") or []
    print(
        i,
        d.get("chatgptStatus"),
        len(h),
        d.get("highlightsSource"),
    )
