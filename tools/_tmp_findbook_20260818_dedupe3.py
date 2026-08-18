# -*- coding: utf-8 -*-
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NEEDLES = [
    "StatQuest",
    "孫大千",
    "AI Agent 新紀元",
    "AI Agent時代",
    "從裡到外養脾胃",
    "精準抗癌湯",
    "我們都有小憂鬱",
    "正是時候讀康德",
    "該是脫困",
    "你的AI諮商師",
    "1分鐘物理",
    "基因圖鑑：",
    "開箱臺灣史",
    "穿越臺灣趣歷史",
    "熵之道",
    "從土地到餐桌的哲學思考",
]


def main() -> None:
    data = json.loads((ROOT / "data.json").read_text(encoding="utf-8-sig"))
    books = data.get("books", [])
    lines = []
    for needle in NEEDLES:
        hits = [
            f"{book.get('id')} | {book.get('title')} | {book.get('author')}"
            for book in books
            if needle in str(book.get("title", "")) or needle in str(book.get("author", ""))
        ]
        lines.append(f"=== {needle}")
        if hits:
            lines.extend(f"HIT {row}" for row in hits[:10])
        else:
            lines.append("NEW")
        lines.append("")
    dest = ROOT / "tools" / ".findbook_dedupe_20260818_c.txt"
    dest.write_text("\n".join(lines), encoding="utf-8")
    print(dest)


if __name__ == "__main__":
    main()
