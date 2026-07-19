# -*- coding: utf-8 -*-
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
t = Path(__file__).with_name("_batch68_make_data2.py").read_text(encoding="utf-8")
for name in ["B33", "B34", "B35"]:
    m = re.search(rf"{name} = \[(.*?)\]\nassert", t, re.S)
    if not m:
        print(name, "MISSING")
        continue
    body = m.group(1)
    n = len(re.findall(r'^\s+"', body, re.M))
    print(name, n)
