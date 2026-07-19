# -*- coding: utf-8 -*-
import json
import os

base = r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\Books\01_business_startup"
ids = ["147", "148", "149", "150", "155", "158", "159", "160"]
out = []
for i in ids:
    path = os.path.join(base, f"01_business_startup-20260717-{i}.json")
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    hl = d.get("chatgptHighlights") or []
    src = d.get("highlightsSource")
    status = d.get("chatgptStatus")
    qualified = status == "complete" and src == "grok" and len(hl) == 150
    out.append(
        {
            "id": d.get("id"),
            "qualified": qualified,
            "src": src,
            "status": status,
            "n": len(hl),
            "title": d.get("title"),
            "author": d.get("author"),
            "summary": d.get("summary"),
            "tags": d.get("tags"),
        }
    )
print(json.dumps(out, ensure_ascii=False, indent=2))
