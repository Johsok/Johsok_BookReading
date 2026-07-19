# -*- coding: utf-8 -*-
from pathlib import Path
import re

t = Path(__file__).with_name("_gen_batch77.py").read_text(encoding="utf-8")
print("lines", t.count("\n") + 1)
print("tail", repr(t[-300:]))
for name in ("BOOK36", "BOOK37", "BOOK38", "BOOK39", "BOOK40"):
    m = re.search(rf"{name} = \[(.*?)\]\s*(?:\n\n|\Z)", t, re.S)
    if not m:
        print(name, "NOT FOUND OR OPEN")
        continue
    n = len(re.findall(r'^\s+"', m.group(1), re.M))
    print(name, n)
