# -*- coding: utf-8 -*-
from pathlib import Path
import re
text = Path(__file__).with_name("_gen_grok_01_business_startup-20260713-40.py").read_text(encoding="utf-8")
chunk = text.split("RAW = [", 1)[1].split("\n]", 1)[0]
items = re.findall(r'^\s*"(.*)"\s*,?\s*$', chunk, flags=re.M)
print(len(items))
for i, s in enumerate(items, 1):
    print(f"{i:03d} {s[:20]}")
