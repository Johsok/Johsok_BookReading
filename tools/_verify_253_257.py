# -*- coding: utf-8 -*-
import json
from pathlib import Path

base = Path(__file__).resolve().parent.parent / "Books" / "01_business_startup"
ids = [
    "01_business_startup-20260716-253",
    "01_business_startup-20260716-254",
    "01_business_startup-20260716-255",
    "01_business_startup-20260716-256",
    "01_business_startup-20260716-257",
]
lines = []
for book_id in ids:
    d = json.loads((base / f"{book_id}.json").read_text(encoding="utf-8-sig"))
    n = len(d.get("chatgptHighlights") or [])
    src = d.get("highlightsSource")
    lines.append(f"{book_id}\t{n}\t{src}\t{d.get('chatgptStatus')}")
Path(__file__).with_name("_verify_253_257.txt").write_text("\n".join(lines), encoding="utf-8")
print("ok")
