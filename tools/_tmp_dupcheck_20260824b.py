# -*- coding: utf-8 -*-
from pathlib import Path
import json

manifest = json.loads((Path(__file__).resolve().parents[1] / "data.json").read_text(encoding="utf-8-sig"))
queries = [
    "進化的力量4",
    "進化的力量04",
    "款待式領導",
    "超乎常理的款待",
    "股市金句",
    "藏在股市",
    "狗狗宇宙",
    "氣候如何影響你的大腦",
    "藝數摺學",
    "基因圖鑑",
    "無處不在的阿焦",
    "正常的迷思",
    "情緒能量",
    "高希均",
    "信任複利",
    "混亂的力量",
]
lines = []
for query in queries:
    hits = []
    for book in manifest.get("books", []):
        title = str(book.get("title", ""))
        if query in title:
            hits.append(f"{book.get('categoryId')} | {book.get('id')} | {title} | {book.get('author')}")
    lines.append(f"Q {query} => {len(hits)}")
    lines.extend(f"  {hit}" for hit in hits[:6])
out = Path(__file__).resolve().parents[1] / "tools" / ".findbook_dupcheck_20260824b.txt"
out.write_text("\n".join(lines), encoding="utf-8")
print("ok")
