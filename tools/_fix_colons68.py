# -*- coding: utf-8 -*-
"""Fix short-colon lines in BOOK68 and re-check all books."""
from __future__ import annotations

import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "tools" / "_gen_chunk02_highlights.py"
text = path.read_text(encoding="utf-8")

spec = importlib.util.spec_from_file_location("g", path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

NATURAL = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
COLON_RE = re.compile(r"^([^：:]{1,12})[：:](.*)$")

# Manual rewrites for BOOK68 flagged lines (1-based index -> new body)
FIX68 = {
    14: "順利耗能下一步三欄反思各寫一點，就夠啟動調整。",
    30: "擴大視角做決策時，短期舒服與長期可行要同時秤量。",
    31: "干擾來時先分類成可忽略、可延後或需立即回應。",
    40: "實驗假設寫清楚若做甲，可能觀察到乙什麼變化。",
    42: "結束條件也要寫下何時停止、何時延長、何時轉向。",
    45: "成功也要拆解是方法有效，還是運氣與情境促成。",
    51: "問責語氣保持好奇，改問這週實驗如何而非指責。",
    56: "閱讀實驗設定輸出成筆記講解或小作品，輸入才沉澱。",
    60: "回饋篩選採用具體可操作建議，忽略人身攻擊噪音。",
    71: "關係中的微實驗改一種表達方式，再觀察對方反應。",
    73: "休息實驗連續三晚準時睡，測量白天清晰度變化。",
    76: "創意阻塞時改換媒介去走去畫去說，而不是死盯螢幕。",
    91: "說不也是實驗，觀察拒絕後世界是否真的崩塌。",
    99: "環境設計比意志力可靠，把工具放在視線內即可。",
    100: "阻力最小原則是把啟動步驟減少到三步以內。",
    102: "慶祝微勝利用具體語句說出我完成了今天的契約。",
    106: "會議本身也可實驗，限時限議題並限當次決策。",
    127: "一週結束問自己更認識自己哪一點了。",
    129: "保持輕盈讓下一個實驗隨時可以開始，不必等完美時機。",
    134: "最後記得生活不是考試卷，而是持續改版的實驗筆記。",
    135: "實驗夥伴每週互問三題，涵蓋做了什麼學到什麼下週試什麼。",
}

arr = list(mod.BOOK68)
for idx, new_body in FIX68.items():
    old = arr[idx - 1]
    arr[idx - 1] = new_body
    print(f"fixed {idx}: {old[:20]} -> {new_body[:20]}")

# Verify no short colons remain
bad = []
for i, body in enumerate(arr, 1):
    match = COLON_RE.match(body)
    if match and not match.group(1).endswith(NATURAL):
        bad.append(i)
if bad:
    raise SystemExit(f"still bad: {bad}")

# Replace BOOK68 list in file by rewriting via exec of fixed module write
# Safer: regenerate whole results using patched lists in memory and also patch source

# Patch source text: replace each old string with new
for idx, new_body in FIX68.items():
    old_body = mod.BOOK68[idx - 1]
    old_lit = f'    "{old_body}",'
    new_lit = f'    "{new_body}",'
    if old_lit not in text:
        raise SystemExit(f"cannot find line {idx} in source: {old_body}")
    text = text.replace(old_lit, new_lit, 1)

path.write_text(text, encoding="utf-8")
print("source patched")

# Also check BOOK69 and BOOK70 for short colons
for name in ("BOOK69", "BOOK70", "BOOK66", "BOOK67"):
    bad = []
    for i, body in enumerate(getattr(mod, name), 1):
        # use fixed BOOK68 for 68
        match = COLON_RE.match(body)
        if match and not match.group(1).endswith(NATURAL):
            bad.append((i, body))
    print(name, "short_colon", len(bad))
    if bad[:5]:
        for i, b in bad[:5]:
            print(f"  {i}: {b}")
