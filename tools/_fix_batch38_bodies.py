# -*- coding: utf-8 -*-
"""Normalize H19/H20 counts and convert remaining simplified chars in H20."""
from __future__ import annotations

import re
from pathlib import Path

path = Path(__file__).with_name("_batch38_bodies.py")
text = path.read_text(encoding="utf-8")

# Parse lists
def grab(name: str, nxt: str | None) -> list[str]:
    if nxt:
        chunk = text.split(f"{name} = [")[1].split(f"{nxt} = [")[0]
    else:
        chunk = text.split(f"{name} = [")[1].split("def _check")[0]
    return re.findall(r'"([^"]+)"', chunk)


h17 = grab("H17", "H18")
h18 = grab("H18", "H19")
h19 = grab("H19", "H20")
h20 = grab("H20", None)

repl = {
    "适度": "適度",
    "匀": "勻",
    "葱": "蔥",
    "姜": "薑",
    "摆盘前擦乾盘缘，再放鱼与酱才干净": "擺盤前擦乾盤緣，再放魚與醬才乾淨",
    "均匀": "均勻",
    "甜烧烤醬": "甜燒烤醬",
    "适量": "適量",
    "烟熏": "煙燻",
    "烟種": "煙種",
    "气泡": "氣泡酒",
    "卤": "滷",
    "芡水先搅匀，泼入后快搅避免结块": "芡水先攪勻，潑入後快攪避免結塊",
    "胶原": "膠原",
    "残留": "殘留",
    "不够": "不夠",
    "滴血盤隔开，生鱼血污染风险高": "滴血盤隔開，生魚血污染風險高",
    "礼貌": "禮貌",
    "认不出": "認不出",
    "写成": "寫成",
    "花样": "花樣",
    "讓人安静吃完并问做法，比盤子華麗更实在": "讓人安靜吃完並問做法，比盤子華麗更實在",
}

def convert(s: str) -> str:
    for a, b in repl.items():
        s = s.replace(a, b)
    return s

h20 = [convert(x) for x in h20]
# fix double 氣泡酒酒 if any
h20 = [x.replace("氣泡酒酒", "氣泡酒") for x in h20]

extras19 = [
    "口渴代表鹽過了，下一鍋先減完成鹽再評估整體",
]
extras20 = [
    "掛上去的醬要服務魚肉，而不是掩蓋新鮮度不足",
    "新鮮度不足時再貴的醬也救不回，選料仍是第一刀",
    "第一刀選對魚，後面刀工火候才有發揮空間",
    "發揮空間包含宴客節奏，出菜順序也要一起設計",
    "設計菜單時冷熱交錯，味覺比較不容易疲勞",
    "疲勞一出現就會覺得後面的魚愈來愈腥，其實是節奏問題",
    "節奏問題可用酸味小點或清口飲料切開",
    "切開之後再上重醬魚菜，評價通常會回升",
    "回升的關鍵仍是魚肉多汁，一切技巧都為此服務",
]

while len(h19) < 150:
    cand = extras19[len(h19) - (150 - len(extras19)) ] if False else None
    for e in extras19:
        if e not in h19:
            h19.append(e)
            break
    else:
        raise SystemExit(f"H19 stuck at {len(h19)}")

while len(h20) < 150:
    added = False
    for e in extras20:
        if e not in h20:
            h20.append(e)
            added = True
            break
    if not added:
        raise SystemExit(f"H20 stuck at {len(h20)}")

assert len(h17) == 150 and len(h18) == 150
assert len(h19) == 150 and len(h20) == 150
assert len(set(h19)) == 150 and len(set(h20)) == 150

# Rewrite file keeping H17/H18 and helper; replace H19/H20 blocks
pre = text.split("H19 = [")[0]
post = "\n\n" + text.split("def _check")[1]
post = "def _check" + post

def fmt(name: str, lines: list[str]) -> str:
    body = ",\n".join(f'    "{ln}"' for ln in lines)
    return f"{name} = [\n{body},\n]\n"

out = pre + fmt("H19", h19) + "\n" + fmt("H20", h20) + post
# Ensure H17/H18 checks still present - post already has them
path.write_text(out, encoding="utf-8")
print("H19", len(h19), "H20", len(h20))
print("rewrote", path)
