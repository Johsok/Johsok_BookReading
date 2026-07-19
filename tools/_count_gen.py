# -*- coding: utf-8 -*-
import re
from pathlib import Path

t = Path(__file__).with_name("_gen_grok_batch_64_85.py").read_text(encoding="utf-8")
for bid in [
    "01_business_startup-20260717-64",
    "01_business_startup-20260717-65",
    "01_business_startup-20260717-82",
]:
    m = re.search(rf'BOOKS\["{bid}"\] = \[(.*?)\]\n', t, re.S)
    if not m:
        print(bid, "NOT FOUND")
        continue
    items = re.findall(r'^\s+"(.*?)"\s*,?\s*$', m.group(1), re.M)
    print(bid, len(items))
