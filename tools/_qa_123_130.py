# -*- coding: utf-8 -*-
import json
import re
from collections import Counter
from pathlib import Path

BASE = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\Books\01_business_startup")
TEMPLATE_MARKERS = [
    "閱讀時可先確認作者如何定義問題",
    "可把觀點轉成一個具體案例",
    "應比較支持證據與可能反例",
    "實際運用時可先做小規模嘗試並記錄結果",
    "整理筆記時宜區分核心主張、適用條件與個人延伸",
]

for i in range(123, 131):
    path = BASE / f"01_business_startup-20260716-{i}.json"
    d = json.loads(path.read_text(encoding="utf-8"))
    hl = d.get("chatgptHighlights") or []
    bodies = [re.sub(r"^\d{3}、", "", x).strip() for x in hl]
    tmpl = sum(any(m in b for m in TEMPLATE_MARKERS) for b in bodies)
    starts = Counter(b[:18] for b in bodies if len(b) >= 18)
    top = starts.most_common(1)[0] if starts else ("", 0)
    print(
        f"{i}|src={d.get('highlightsSource')}|status={d.get('chatgptStatus')}"
        f"|n={len(hl)}|uniq={len(set(bodies))}|tmpl={tmpl}|topstart={top[1]}"
    )
    if hl:
        print("  ", hl[0][:60])
        print("  ", hl[74][:60] if len(hl) > 74 else "")
