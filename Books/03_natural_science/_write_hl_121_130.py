# -*- coding: utf-8 -*-
"""Overwrite chatgptHighlights for natural-science books 121-130."""
import json
import re
from datetime import datetime
from pathlib import Path

from _hl_items_121_123 import ITEMS as A
from _hl_items_124_127 import ITEMS as B
from _hl_items_128_130 import ITEMS as C

ROOT = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\Books\03_natural_science")
STAMP = datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S%z")
STAMP = STAMP[:-2] + ":" + STAMP[-2:] if len(STAMP) >= 5 else STAMP
UPDATED = "2026-08-18"
STEP_RE = re.compile(r".面第\d+步|第\d+步，|面向\d")
FORBIDDEN = ("本書", "作者指出", "本章", "這一章", "第X章", "｜")

ITEMS = {}
ITEMS.update(A)
ITEMS.update(B)
ITEMS.update(C)

SUMMARIES = {
    "03_natural_science-20260716-121.json": "整理藝術、建築、音樂、天文與政治制度裡隱藏的數學結構，從畫布比例到五次方程不可解，把公式讀成文明足跡。",
    "03_natural_science-20260716-122.json": "整理《如果這樣，會怎樣？》十週年增訂與續集的極端假想題，用數量級估算把荒謬問題轉成可檢查的物理與風險判斷。",
    "03_natural_science-20260716-123.json": "整理文俶《金石昆蟲草木狀》藥草、花果與動物三冊，對照道地本草、形態辨識與現代分類，也指出摹繪與寫實的落差。",
    "03_natural_science-20260716-124.json": "整理生成式人工智慧的黑箱、遞迴自我改良與對齊困境，說明實驗室競賽如何把無法解釋的系統推向公共領域。",
    "03_natural_science-20260716-125.json": "整理西拉雅白茅草坡上臺灣草鴞的築巢、夜獵與育雛紀錄，並指出棲地流失與人為干擾才是最大威脅。",
    "03_natural_science-20260716-126.json": "整理蹄蓋蕨科至水龍骨科的根莖、孢子囊群與相似種比較，並說明步道名錄分布圖只是概略座標。",
    "03_natural_science-20260716-127.json": "整理水韭科至烏毛蕨科的石松類、樹蕨、膜蕨與水生異孢類群，並交代檢索表、孢子與海拔帶的使用方式。",
    "03_natural_science-20260716-128.json": "整理基因、表觀遺傳、微生物與激素如何塑造口味、癮頭、情緒與伴侶選擇，並提醒自由意志的範圍比直覺更窄。",
    "03_natural_science-20260716-129.json": "整理魔法師二號號全球海洋採樣與霰彈槍宏觀基因組，說明濾膜分級、公開資料庫與微生物在碳氮硫循環中的角色。",
    "03_natural_science-20260716-130.json": "整理超級電容器從雙電層、贗電容、電極電解液隔膜到模組工藝與自放電抑制，對照能量密度、功率與應用場景。",
}


def tidy(text):
    text = text.replace(",", "，").replace(";", "；")
    text = text.replace("...", "……")
    return text.strip()


def numbered(items):
    if len(items) != 150:
        raise SystemExit(f"need 150, got {len(items)}")
    return [f"{i:03d}、{t}" for i, t in enumerate(items, 1)]


def check(items, tag):
    opens = set()
    for i, raw in enumerate(items, 1):
        if not raw or raw[0].isdigit():
            raise SystemExit(f"{tag} {i:03d} bad start")
        op = raw[:18]
        if op in opens:
            raise SystemExit(f"{tag} dup first18 at {i}: {op}")
        opens.add(op)
        for w in FORBIDDEN:
            if w in raw:
                raise SystemExit(f"{tag} {i:03d} forbidden {w}")
        if STEP_RE.search(raw):
            raise SystemExit(f"{tag} {i:03d} step phrasing")
        if "：" in raw[:10] and raw.index("：") < 8:
            raise SystemExit(f"{tag} {i:03d} early colon")


def patch(filename, items, summary=None):
    items = [tidy(x) for x in items]
    check(items, filename)
    path = ROOT / filename
    data = json.loads(path.read_text(encoding="utf-8"))
    data["chatgptHighlights"] = numbered(items)
    data["chatgptStatus"] = "complete"
    data["highlightsSource"] = "grok"
    data["highlightsCapturedAt"] = STAMP
    data["updatedAt"] = UPDATED
    if summary:
        data["summary"] = summary
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)
    print(f"OK {filename} n={len(data['chatgptHighlights'])}")


def main():
    missing = [f"03_natural_science-20260716-{i}.json" for i in range(121, 131) if f"03_natural_science-20260716-{i}.json" not in ITEMS]
    if missing:
        raise SystemExit(f"missing keys {missing}")
    for name in [f"03_natural_science-20260716-{i}.json" for i in range(121, 131)]:
        patch(name, ITEMS[name], SUMMARIES.get(name))


if __name__ == "__main__":
    main()
