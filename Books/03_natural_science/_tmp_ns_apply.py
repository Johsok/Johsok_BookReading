# -*- coding: utf-8 -*-
from pathlib import Path
import importlib.util
import ast
import json
from datetime import datetime

ROOT = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\Books\03_natural_science")
STAMP = datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S%z")
STAMP = STAMP[:-2] + ":" + STAMP[-2:] if len(STAMP) >= 5 else STAMP
UPDATED = "2026-08-18"


def load(name, attr):
    spec = importlib.util.spec_from_file_location(name, ROOT / name)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, attr)


def numbered(items):
    if len(items) != 150:
        raise SystemExit(f"need 150, got {len(items)}")
    seen = set()
    out = []
    for i, t in enumerate(items, 1):
        t = t.strip()
        if t.startswith(f"{i:03d}、"):
            body = t
            key = t.split("、", 1)[1]
        else:
            body = f"{i:03d}、{t}"
            key = t
        if key in seen:
            raise SystemExit(f"duplicate in {i}: {key[:40]}")
        seen.add(key)
        out.append(body)
    return out


def patch(filename, items, summary):
    path = ROOT / filename
    data = json.loads(path.read_text(encoding="utf-8"))
    data["chatgptHighlights"] = numbered(items)
    data["chatgptStatus"] = "complete"
    data["highlightsSource"] = "grok"
    data["highlightsCapturedAt"] = STAMP
    data["updatedAt"] = UPDATED
    data["summary"] = summary
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)
    print(f"OK {filename}")


src = (ROOT / "_tmp_ns_hl_writer.py").read_text(encoding="utf-8")
i = src.find('"items": [')
j = src.find("\n    ],", i)
items21 = ast.literal_eval(src[i + len('"items": ') : j + len("\n    ]")])

jobs = [
    ("03_natural_science-20260716-21.json", items21, "整理 DK 物理學百科中測量、力學、能量、波動、電磁、相對論、量子與宇宙尺度的核心觀念與可檢驗推論。"),
    ("03_natural_science-20260716-22.json", load("_tmp_ns_22.py", "ITEMS_22"), "整理自然科學全圖解中天文、氣象、地質、海洋、生命、人體與物質能量的圖解式核心觀念。"),
    ("03_natural_science-20260716-23.json", load("_tmp_ns_23.py", "ITEMS_23"), "整理丹尼爾‧李伯曼從演化與自然史拆解現代運動與健康迷思的核心論點與可實踐活動設計。"),
    ("03_natural_science-20260716-24.json", load("_tmp_ns_24.py", "ITEMS_24"), "整理陳瑞麟從古代到文藝復興，西方自然哲學如何質問自然、建立方法與改變證據標準的思想史重點。"),
    ("03_natural_science-20260716-25.json", load("_tmp_ns_25.py", "ITEMS_25"), "整理上野正彥從法醫視角說明死後變化、創傷機制、死因鑑定與證據界線的人體奧祕。"),
    ("03_natural_science-20260716-26.json", load("_tmp_ns_26.py", "ITEMS_26"), "整理元素週期表公寓圖解中各族元素性格、鍵結、核性質與生活應用的核心觀念。"),
    ("03_natural_science-20260716-27.json", load("_tmp_ns_27.py", "ITEMS_27"), "整理羅伯．薩波斯基對急性與慢性壓力的生理路徑、疾病關聯與可調節出口的科普重點。"),
    ("03_natural_science-20260716-28.json", load("_tmp_ns_28.py", "ITEMS_28"), "整理看圖學基礎物理：從力學、牛頓定律、能量、波動、電磁走到天體的素養型重點。"),
    ("03_natural_science-20260716-29.json", load("_tmp_ns_29.py", "ITEMS_29"), "整理高中物理解題關鍵：模型選擇、守恆條件、力與場、波動光學與近代物理的應考重點。"),
    ("03_natural_science-20260716-30.json", load("_tmp_ns_30.py", "ITEMS_30"), "整理如何學好高中物理的方法、題幹條件解讀、錯題策略與各單元模型判斷。"),
]

for fn, items, summary in jobs:
    print(fn, len(items))
    patch(fn, items, summary)
