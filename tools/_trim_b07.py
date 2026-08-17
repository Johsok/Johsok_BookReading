# -*- coding: utf-8 -*-
"""Drop 24 overlapping Book B highlights so the list is exactly 150."""
from __future__ import annotations

import importlib
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
mod = importlib.import_module("_gen_hl_04_healthcare_06_07")

DROP = {
    "音樂可有可無，節奏慢到肩能晃開就好，不必跳成有氧舞蹈才算數",
    "地毯上做可減噪音，樓下鄰居的抱怨不該變成你放棄的理由",
    "手機鬧鐘兩段各三十秒就能計時，不必買專用器材才開始",
    "超商沙拉先吃蛋白質配料，麵包塊留到最後甚至不吃",
    "同事說臉瘦了就加回主食，皮下臉頰掉得慢，肚子裡的油可能才剛開始降",
    "家用體脂計誤差大，不必每天為百分之零點二焦慮",
    "水果恐懼沒必要，重點是份量與時段，不是把所有甜味趕出廚房",
    "動作看起來好笑才對，嚴肅深蹲比較不像要讓人持續兩週的門檻",
    "早中晚拆開三組，不必連做三十分鐘把人嚇跑",
    "皮帶孔當週記，比應用程式曲線更貼近生活化追蹤",
    "數字用來激勵，真正護心的是腰圍、血壓與血糖一起改善",
    "只做操或只喝蔬果汁，把兩件拆開都會高估效果",
    "納豆味噌若配大碗白飯，發酵豆的好處救不了主食超量",
    "清湯開胃可以增加飽足，濃湯、玉米湯、麵包湯要算進碳水",
    "紅白酒熱量密度不同，所謂能喝不是無限續杯",
    "疫苗後一兩天疲憊是正常，不要用體重沒掉懲罰自己",
    "結束後每週仍有幾天主食半份，比全年放縱再季度懲罰穩",
    "學校或公司餐廳先夾兩樣菜再決定飯要不要盛，順序本身就是技術",
    "三角飯糰選鮭魚或梅子、配茶葉蛋，不要再加甜甜圈當第二主食",
    "燕麥仍是碳水不是免費蔬菜，當早餐主食份量也要減半",
    "地瓜比白飯升糖慢一點，但仍算主食，不能因為健康就吃兩條",
    "玉米濃湯看起來像湯，其實接近澱粉加奶油的主食",
    "每小時起身踏步一分鐘，比下班才懺悔有效",
    "鏡側面比正面誠實，吸氣收腹會讓自己以為已經成功",
}

pts = [p for p in mod.BOOK_B["points"] if p not in DROP]
missing = DROP - set(mod.BOOK_B["points"])
print("count_after", len(pts), "missing_drops", missing)
if len(pts) != 150:
    raise SystemExit(f"expected 150 got {len(pts)}")

path = TOOLS / "_gen_hl_04_healthcare_06_07.py"
text = path.read_text(encoding="utf-8")
start = text.index("BOOK_B = {")
end = text.index("\n\n\ndef main()")
body = "\n".join(f'        "{p}",' for p in pts)
new_block = (
    "BOOK_B = {\n"
    f'    "id": {mod.BOOK_B["id"]!r},\n'
    f'    "title": {mod.BOOK_B["title"]!r},\n'
    f'    "author": {mod.BOOK_B["author"]!r},\n'
    '    "points": [\n'
    f"{body}\n"
    "    ],\n"
    "}"
)
path.write_text(text[:start] + new_block + text[end:], encoding="utf-8")
print("rewrote BOOK_B")
