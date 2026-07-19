# -*- coding: utf-8 -*-
import json
from pathlib import Path

base = Path(__file__).resolve().parent.parent / "Books" / "01_business_startup"
ids = [
    "01_business_startup-20260717-161",
    "01_business_startup-20260717-162",
    "01_business_startup-20260717-163",
    "01_business_startup-20260717-164",
    "01_business_startup-20260717-165",
]
lines = []
for book_id in ids:
    data = json.loads((base / f"{book_id}.json").read_text(encoding="utf-8-sig"))
    lines.append(f"{book_id}\t{data['title']}\t{data['author']}")
out = Path(__file__).resolve().parent / "_titles_tmp.txt"
out.write_text("\n".join(lines), encoding="utf-8")
print("ok")
