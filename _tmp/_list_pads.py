# -*- coding: utf-8 -*-
import json
from pathlib import Path

root = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\Books\05_food_wellness")
pads = [
    "日常執行時再對照克數",
    "實際份量仍要依醫囑微調",
    "做成習慣比單次堅持更重要",
    "回家後用飲食紀錄核對一次",
    "並與下次抽血一起回顧",
]
out = []
for name in [
    "05_food_wellness-20260716-15.json",
    "05_food_wellness-20260716-16.json",
]:
    hs = json.loads((root / name).read_text(encoding="utf-8-sig"))["chatgptHighlights"]
    out.append(name)
    for i, line in enumerate(hs, 1):
        body = line.split("、", 1)[1]
        if any(p in body for p in pads):
            out.append(f"  {i:03d} {body}")
Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\_tmp\_pads.txt").write_text(
    "\n".join(out), encoding="utf-8"
)
print("n", len(out))
