# -*- coding: utf-8 -*-
from pathlib import Path
import unicodedata
import re

root = Path(__file__).resolve().parents[1]
text = (root / "tools" / ".existing_first3_titles.txt").read_text(encoding="utf-8")
punct = re.compile(r"[\s\W_]+", re.UNICODE)

queries = [
    "才賦自由",
    "重壓的技術",
    "透視職場冰山",
    "90%高級主管",
    "打開無路之路",
    "大怒神來了",
    "AI時代的資本真相",
    "張夏準的12堂",
    "超級代理效應",
    "老錢思維",
    "三明治族的慢富",
    "創作覺醒",
    "藏在股市金句",
    "微實驗",
    "留白",
    "我們都有小憂鬱",
    "戀愛課金",
    "自我批評也是愛",
    "男人的四個原型",
    "創作之路",
    "我在生命終點站",
    "惡意是怎麼形成",
    "大人系女子",
    "藝數摺學",
    "數學女孩：黎曼",
    "看魚",
    "哺乳類王朝",
    "蝴蝶誌",
    "困境使用說明書",
    "別讓意識型態",
    "文明的原點",
    "氣候如何影響你的大腦",
    "細胞演化簡史",
    "地球生命大歷史",
    "基因圖鑑",
]
lines = []
for q in queries:
    hits = [line for line in text.splitlines() if q in line]
    if hits:
        lines.append(f"HIT\t{q}\t{hits[0][:180]}")
    else:
        lines.append(f"NEW\t{q}")
(root / "tools" / ".title_hits_20260818_2102.txt").write_text("\n".join(lines), encoding="utf-8")
print(f"wrote {len(lines)}")
