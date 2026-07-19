# -*- coding: utf-8 -*-
from pathlib import Path
import re

text = Path(__file__).with_name("_gen_batch55.py").read_text(encoding="utf-8")
for name in ["BOOK51", "BOOK52", "BOOK53", "BOOK54", "BOOK55"]:
    m = re.search(rf"{name} = \[(.*?)\]\n\n", text, re.S)
    if not m:
        print(name, "NOT FOUND")
        continue
    body = m.group(1)
    lines = re.findall(r'^\s+"(.*)"\s*,?\s*$', body, re.M)
    print(name, len(lines))
    for i, line in enumerate(lines, 1):
        if len(line) < 12 or "\ufffd" in line or "�" in line:
            print(" ", i, repr(line[:100]))
