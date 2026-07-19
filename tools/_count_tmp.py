# -*- coding: utf-8 -*-
import re
from pathlib import Path

t = Path(__file__).with_name("_gen_grok_141_145.py").read_text(encoding="utf-8")
parts = t.split("BOOKS[")
for p in parts[1:]:
    bid = p.split("]")[0].strip().strip('"')
    # only count strings inside the list after author
    if "[" not in p:
        continue
    list_part = p.split("[", 1)[1]
    bodies = re.findall(r'^\s+"(.+)",?\s*$', list_part, re.M)
    # stop at closing of list roughly - bodies until we hit def or next BOOKS
    print(bid, len(bodies))
