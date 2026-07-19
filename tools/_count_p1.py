# -*- coding: utf-8 -*-
import re
from pathlib import Path

text = Path(__file__).with_name("_gen_grok_20260719_hl_p1.py").read_text(encoding="utf-8")
parts = re.split(r'BOOKS\["([^"]+)"\]', text)
for i in range(1, len(parts), 2):
    bid = parts[i]
    body = parts[i + 1]
    m = re.search(r"\[\n(.*?)]\s*,\s*\)", body, re.S)
    if not m:
        print(bid, "NO LIST")
        continue
    items = re.findall(r'^\s+"(.*)"[,]?$', m.group(1), re.M)
    print(bid, len(items))
    # short bodies
    short = [x for x in items if len(x) < 12]
    if short:
        print("  short:", short[:3])
    # forbidden
    for f in ("本書", "作者指出", "本章", "這一章"):
        hit = [x for x in items if f in x]
        if hit:
            print("  forbidden", f, len(hit))
    # dup starts
    from collections import Counter
    c = Counter(x[:18] for x in items if len(x) >= 18)
    top = c.most_common(3)
    print("  top starts:", top)
