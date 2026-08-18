# -*- coding: utf-8 -*-
import json
from collections import Counter
from pathlib import Path

root = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\_tmp")
banned = ["本書", "作者指出", "本章", "這一章", "｜", "作者"]
ok_end = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
errors = []
for fn, expect_id in [
    ("ns24_hl_01.json", "03_natural_science-20260724-01"),
    ("ns24_hl_02.json", "02_psychology_growth-20260724-02"),
]:
    d = json.loads((root / fn).read_text(encoding="utf-8"))
    bodies = d["bodies"]
    print(fn, "id", d.get("id"), "n", len(bodies), "unique", len(set(bodies)))
    if d.get("id") != expect_id:
        errors.append(fn + " id mismatch")
    if len(bodies) != 150 or len(set(bodies)) != 150:
        errors.append(fn + " count/unique")
    pref = Counter(x[:18] for x in bodies)
    mx = max(pref.values())
    print(" prefix max", mx)
    if mx >= 4:
        errors.append(fn + " prefix " + str({k: v for k, v in pref.items() if v >= 4}))
    lens = [len(x) for x in bodies]
    print(" len min/max/avg", min(lens), max(lens), round(sum(lens) / len(lens), 1))
    for i, x in enumerate(bodies):
        if len(x) < 12:
            errors.append(f"{fn}[{i}] short {x}")
        for w in banned:
            if w in x:
                errors.append(f"{fn}[{i}] banned {w}")
        if "|" in x or "｜" in x or "**" in x or "`" in x:
            errors.append(f"{fn}[{i}] markdown")
        for sep in ("：", ":"):
            if sep in x:
                head = x.split(sep, 1)[0]
                if not any(head.endswith(t) for t in ok_end):
                    errors.append(f"{fn}[{i}] colon [{head}] :: {x}")
        if x.startswith("第") and "步" in x[:12]:
            errors.append(f"{fn}[{i}] step")
    for i in range(1, len(bodies)):
        if bodies[i][:10] == bodies[i - 1][:10]:
            errors.append(f"{fn} adj {i}")
print("ERRORS", len(errors))
for e in errors:
    print(e)
if not errors:
    print("PASS")
