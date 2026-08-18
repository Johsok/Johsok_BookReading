# -*- coding: utf-8 -*-
from pathlib import Path
import re

text = Path("_tmp/write_ns19_01_05.py").read_text(encoding="utf-8")
for name in ["B01", "B02", "B03", "B04", "B05"]:
    m = re.search(rf"{name} = \[(.*?)\n\]\n", text, re.S)
    items = re.findall(r'^    "(.+)",?\s*$', m.group(1), re.M)
    print(name, len(items), "unique", len(set(items)))
    # garbage
    for s in items:
        if "peda" in s or "fort " in s or "syn " in s or "濒" in s:
            print("  BAD idx")
