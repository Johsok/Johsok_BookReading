# -*- coding: utf-8 -*-
import json
from pathlib import Path

base = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\Books\07_other")
out = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\_tmp\meta_07_31_40.txt")
lines = []
for n in range(31, 41):
    f = base / f"07_other-20260717-{n:02d}.json"
    d = json.loads(f.read_text(encoding="utf-8-sig"))
    lines.append("=" * 60)
    lines.append(f"id: {d['id']}")
    lines.append(f"title: {d['title']}")
    lines.append(f"author: {d['author']}")
    lines.append(f"url: {d.get('sourceUrl','')}")
    lines.append(f"summary: {d.get('summary','')}")
out.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("ok", out)
