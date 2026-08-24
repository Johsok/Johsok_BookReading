# -*- coding: utf-8 -*-
from pathlib import Path
import json
import re
import unicodedata

PUNCT = re.compile(r"[\s\W_]+", re.UNICODE)
ROOT = Path(__file__).resolve().parents[1]
manifest = json.loads((ROOT / "data.json").read_text(encoding="utf-8-sig"))
queries = [
    "美元憑什麼",
    "進化的力量",
    "從地理看經濟",
    "款待式領導",
    "超乎常理的款待",
    "高希均",
    "不用猜市場",
    "股市金句",
    "花錢的藝術",
    "我們都有小憂鬱",
    "讓焦慮隨風而去",
    "正是時候讀康德",
    "存有心理學",
    "最有企圖心的一天",
    "幸福檔案",
    "神經可塑性",
    "半憂鬱",
    "哺乳類王朝",
    "蝴蝶熱",
    "蝴蝶誌",
    "基因圖鑑",
    "看懂建築",
    "迷走神經",
]


def key(title: str, author: str = "") -> str:
    value = unicodedata.normalize("NFKC", f"{title}|{author}").casefold()
    return PUNCT.sub("", value)


lines = [f"total={len(manifest.get('books', []))}"]
for query in queries:
    hits = []
    for book in manifest.get("books", []):
        title = str(book.get("title", ""))
        if query.lower() in title.lower():
            hits.append(
                f"{book.get('categoryId')} | {book.get('id')} | {title} | {book.get('author')}"
            )
    lines.append(f"Q {query} => {len(hits)}")
    lines.extend(f"  {hit}" for hit in hits[:8])

out = ROOT / "tools" / ".findbook_dupcheck_20260824.txt"
out.write_text("\n".join(lines), encoding="utf-8")
print(f"wrote {out} lines={len(lines)}")
