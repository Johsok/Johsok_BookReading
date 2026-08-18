# -*- coding: utf-8 -*-
import json
from collections import Counter
from pathlib import Path

ROOT = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\Books\05_food_wellness")
BANNED = ("本書", "作者指出", "本章", "這一章", "｜")
OLD = "食譜成功先從理解食材特性"

for i in range(21, 31):
    name = f"05_food_wellness-20260716-{i:02d}.json"
    data = json.loads((ROOT / name).read_text(encoding="utf-8"))
    hl = data["chatgptHighlights"]
    issues = []
    if len(hl) != 150:
        issues.append(f"len={len(hl)}")
    if data.get("chatgptStatus") != "complete":
        issues.append("status")
    if data.get("highlightsSource") != "grok":
        issues.append(f"src={data.get('highlightsSource')}")
    bodies = []
    for n, s in enumerate(hl, 1):
        if not s.startswith(f"{n:03d}、"):
            issues.append(f"num{n}")
        body = s.split("、", 1)[1] if "、" in s else s
        bodies.append(body)
        for w in BANNED:
            if w in s:
                issues.append(f"banned {w} @{n}")
        if OLD in s:
            issues.append(f"oldtemplate {n}")
        if len(body) < 12:
            issues.append(f"short {n}")
    dups = [k for k, v in Counter(bodies).items() if v > 1]
    if dups:
        issues.append(f"dups {len(dups)}")
    top = Counter(b[:8] for b in bodies).most_common(1)[0]
    print(name, data["title"][:18], issues or "OK", "pref", top)
    print("  sample001:", hl[0][:60])
    print("  sample080:", hl[79][:60])
    print("  sample150:", hl[149][:60])
