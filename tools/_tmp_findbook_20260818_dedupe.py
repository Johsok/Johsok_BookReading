# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NEEDLES = [
    "走出金錢焦慮",
    "智慧通膨下的新商機",
    "馬斯克寶典",
    "正是時候讀康德",
    "有一種田野報告叫植物獵人",
    "從土地到餐桌的哲學思考",
    "你的AI諮商師上線了",
    "看懂訊號，重塑大腦修復力",
    "不懂程式也能自架專屬",
    "從裡到外養脾胃",
    "來炊粿",
    "精準抗癌湯",
    "老祖宗傳下來不生病的智慧",
    "一魚百味",
    "複合型AI Agent",
    "戰後台灣史",
    "穿越臺灣趣歷史",
    "開箱臺灣史",
    "臺灣人的歷史",
    "島史未竟",
    "帝國之門",
    "內在時鐘",
    "腸腦悖論",
    "半導體超圖解",
    "Vibe Coding",
]


def main() -> None:
    data = json.loads((ROOT / "data.json").read_text(encoding="utf-8-sig"))
    books = data.get("books", [])
    out_lines = [
        f"total={len(books)} generatedAt={data.get('generatedAt')}",
        f"searchDateRange={data.get('searchDateRange')}",
        "",
    ]
    for needle in NEEDLES:
        hits = []
        for book in books:
            title = str(book.get("title", ""))
            author = str(book.get("author", ""))
            if needle in title:
                hits.append(f"{book.get('id')} | {title} | {author}")
        out_lines.append(f"=== {needle}")
        if hits:
            out_lines.extend(f"HIT {row}" for row in hits[:8])
        else:
            out_lines.append("NEW")
        out_lines.append("")
    dest = ROOT / "tools" / ".findbook_dedupe_20260818.txt"
    dest.write_text("\n".join(out_lines), encoding="utf-8")
    print(dest)


if __name__ == "__main__":
    main()
