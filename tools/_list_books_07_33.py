# -*- coding: utf-8 -*-
import json
from pathlib import Path

base = Path(__file__).resolve().parents[1] / "Books" / "01_business_startup"
for i in range(7, 34):
    p = base / f"01_business_startup-20260711-{i:02d}.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    h = d.get("chatgptHighlights") or []
    print(
        f"{i:02d}|{len(h)}|{d.get('chatgptStatus')}|{d.get('highlightsSource')}|"
        f"{d.get('author')}|{d.get('title')}"
    )
