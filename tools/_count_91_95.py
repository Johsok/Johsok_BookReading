# -*- coding: utf-8 -*-
import re
from pathlib import Path

p = Path(__file__).with_name("_gen_91_95.py")
text = p.read_text(encoding="utf-8")
blocks = re.findall(r'"id": "([^"]+)".*?"bodies": r\'\'\'(.*?)\'\'\'.strip\(\)\.splitlines\(\)', text, re.S)
NAT = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
for bid, body in blocks:
    lines = [x.strip() for x in body.strip().splitlines() if x.strip()]
    print("====", bid, len(lines))
    shorts = []
    for i, l in enumerate(lines, 1):
        m = re.match(r"^([^：:]{1,12})[：:]", l)
        if m and not m.group(1).endswith(NAT):
            shorts.append((i, m.group(1), l))
        if re.search(r"[A-Za-z]", l):
            print("ENG", i, l)
    print("short_colons", len(shorts))
    for item in shorts:
        print(" ", item[0], item[1], "|", item[2][:40])
