# -*- coding: utf-8 -*-
from pathlib import Path
import re

text = Path(__file__).with_name("_gen_grok_batch_20260717_need.py").read_text(encoding="utf-8")
# Extract each book list by regex on keys
keys = re.findall(r'"(01_business_startup-20260717-\d+)":\s*\[', text)
for key in keys:
    start = text.index(f'"{key}": [')
    # find matching list end - crude: next key or BOOKS close
    sub = text[start:]
    m = re.search(r':\s*\[', sub)
    rest = sub[m.end() :]
    depth = 1
    i = 0
    while i < len(rest) and depth:
        if rest[i] == "[":
            depth += 1
        elif rest[i] == "]":
            depth -= 1
        i += 1
    body = rest[: i - 1]
    lines = re.findall(r'^\s+"(.+)",?\s*$', body, flags=re.M)
    print(key, len(lines))
