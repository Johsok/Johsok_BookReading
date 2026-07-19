# -*- coding: utf-8 -*-
import json
import os

base = r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\Books\01_business_startup"
ids = ["123", "124", "125", "126", "127", "128", "129", "130"]
for i in ids:
    path = os.path.join(base, f"01_business_startup-20260716-{i}.json")
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    hl = d.get("chatgptHighlights") or []
    print(
        f"{i}|status={d.get('chatgptStatus')}|src={d.get('highlightsSource')}"
        f"|n={len(hl)}|title={d.get('title')}|author={d.get('author')}"
    )
