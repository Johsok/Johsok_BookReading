# -*- coding: utf-8 -*-
from pathlib import Path
import re

text = Path(__file__).with_name("_gen_grok_batch_98_116_117_118.py").read_text(encoding="utf-8")
parts = re.split(r'"(01_business_startup-[^"]+)": \[', text)
for i in range(1, len(parts), 2):
    bid = parts[i]
    body = parts[i + 1].split("],\n", 1)[0]
    n = len(re.findall(r'^\s+"', body, re.M))
    print(bid, n)
