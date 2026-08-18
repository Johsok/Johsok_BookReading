# -*- coding: utf-8 -*-
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NEEDLES = [
    "該是脫困的時候了",
    "正常的迷思",
    "我們都有小憂鬱",
    "1分鐘物理",
    "基因圖鑑",
    "熵之道",
    "葉均蔚",
    "從土地到餐桌",
    "歡迎光臨營養師",
    "生成式 AI 實務教材",
    "開箱臺灣史",
    "AI時代的Python",
    "SOLIDWORKS Design零件",
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
        lines.extend(f"HIT {row}" for row in hits[:8] or [])
        if not hits:
            lines.append("NEW")
        lines.append("")
    dest = ROOT / "tools" / ".findbook_dedupe_20260818_b.txt"
    dest.write_text("\n".join(lines), encoding="utf-8")
    print(dest)


if __name__ == "__main__":
    main()
