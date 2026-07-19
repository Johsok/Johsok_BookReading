# -*- coding: utf-8 -*-
import re
from pathlib import Path

src = Path(__file__).with_name("_gen_grok_115_118.py").read_text(encoding="utf-8")
for name in ["H115", "H116", "H117", "H118"]:
    m = re.search(rf"{name} = \[(.*?)\]\n\n", src, re.S)
    if not m:
        print(name, "not found")
        continue
    items = re.findall(r'"([^"]*)"', m.group(1))
    print(name, len(items))
