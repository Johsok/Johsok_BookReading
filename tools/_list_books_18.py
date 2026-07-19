# -*- coding: utf-8 -*-
import json
import pathlib

base = pathlib.Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\Books\01_business_startup")
for i in range(1, 21):
    p = base / f"01_business_startup-20260718-{i:02d}.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    title = d["title"][:70]
    author = (d.get("author") or "")[:40]
    hl = d.get("chatgptHighlights") or d.get("highlights") or []
    print(f"{i:02d}|{title}|{author}|hl={len(hl)}")
