# -*- coding: utf-8 -*-
from pathlib import Path
from collections import Counter

text = Path("tools/_gen_batch7_part1.py").read_text(encoding="utf-8-sig")
text = text.replace("Path(__file__).resolve().parents[1]", "Path('.').resolve()")
ns: dict = {}
exec(compile(text.split("print(len")[0] + "\npass", "x", "exec"), ns)
lines = ns["BOOKS"]["02_psychology_growth-20260718-36"]
print("count", len(lines))
print("minlen", min(len(l) for l in lines))
c = Counter(l[:18] for l in lines if len(l) >= 18)
print("top", c.most_common(5))
print("dups", len(lines) - len(set(lines)))
for i, l in enumerate(lines, 1):
    if "才华" in l:
        print("simp", i, l)
