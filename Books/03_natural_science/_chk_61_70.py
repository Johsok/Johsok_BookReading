# -*- coding: utf-8 -*-
import json
import re
from collections import Counter
from pathlib import Path

base = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\Books\03_natural_science")
old_frags = (
    "科學問題必須能以觀察",
    "閱讀時可先確認作者如何定義問題",
    "可把觀點轉成一個具體案例",
    "應比較支持證據與可能反例",
    "實際運用時可先做小規模嘗試並記錄結果",
    "整理筆記時宜區分核心主張",
)

for n in range(61, 71):
    p = base / f"03_natural_science-20260716-{n:02d}.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    h = d.get("chatgptHighlights", [])
    nums = []
    bad = []
    for i, line in enumerate(h, 1):
        m = re.match(r"^(\d{3})、(.+)$", line)
        if not m:
            bad.append(("fmt", i, line[:60]))
            continue
        nums.append(int(m.group(1)))
        body = m.group(2)
        if any(f in line for f in old_frags):
            bad.append(("old", i))
        if body.startswith("本書") or "作者指出" in body or "｜" in body:
            bad.append(("ban", i, body[:40]))
    expected = list(range(1, 151))
    prefixes = [re.sub(r"^\d{3}、", "", x)[:8] for x in h]
    repeats = [(k, v) for k, v in Counter(prefixes).items() if v >= 4]
    print(
        f"{n}: n={len(h)} status={d.get('chatgptStatus')} src={d.get('highlightsSource')} "
        f"updated={d.get('updatedAt')} nums_ok={nums == expected} bad={len(bad)} "
        f"prefix4={len(repeats)}"
    )
    if bad[:3]:
        print("  sample", bad[:3])
    if repeats[:6]:
        print("  prefix", repeats[:6])
