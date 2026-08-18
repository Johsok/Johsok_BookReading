# -*- coding: utf-8 -*-
import json
import re
from collections import Counter
from pathlib import Path

root = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\Books\05_food_wellness")
banned = ("本書", "作者指出", "本章", "這一章", "｜")
out = []
for name in [
    "05_food_wellness-20260716-15.json",
    "05_food_wellness-20260716-16.json",
]:
    data = json.loads((root / name).read_text(encoding="utf-8-sig"))
    hs = data["chatgptHighlights"]
    errs = []
    if len(hs) != 150:
        errs.append(f"count {len(hs)}")
    if len(set(hs)) != 150:
        errs.append("dup lines")
    bodies = []
    for i, line in enumerate(hs, 1):
        pre = f"{i:03d}、"
        if not line.startswith(pre):
            errs.append(f"prefix {i}")
            continue
        body = line[len(pre):]
        bodies.append(body)
        for w in banned:
            if w in line:
                errs.append(f"{i} {w}")
        if re.search(r"[：:]", line):
            errs.append(f"{i} colon")
        if "章" in line:
            errs.append(f"{i} 章")
        if re.search(r"[A-Za-z]", line):
            errs.append(f"{i} latin")
    c10 = Counter(b[:10] for b in bodies)
    for k, v in c10.items():
        if v > 1:
            errs.append(f"first10 {k} x{v}")
    out.append(
        f"{name} count={len(hs)} unique={len(set(hs))} errors={len(errs)} "
        f"status={data.get('chatgptStatus')} source={data.get('highlightsSource')} "
        f"at={data.get('highlightsCapturedAt')} updated={data.get('updatedAt')}"
    )
    for e in errs:
        out.append("  " + e)
    out.append("  first3 " + " | ".join(hs[:3]))
    out.append("  last2 " + " | ".join(hs[-2:]))
Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\_tmp\_final_05_15_16.txt").write_text(
    "\n".join(out), encoding="utf-8"
)
print("done")
