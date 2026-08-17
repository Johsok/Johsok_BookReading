# -*- coding: utf-8 -*-
import re
from pathlib import Path

for name in ("_gen_highlights_186_190.py", "_hl_188_190.py"):
    text = Path(__file__).with_name(name).read_text(encoding="utf-8")
    parts = text.split('"bodies": [')
    print(name, "lists", len(parts) - 1)
    for i, part in enumerate(parts[1:], 1):
        chunk = part.split("],", 1)[0]
        n = len(re.findall(r'^\s+".+",?\s*$', chunk, re.M))
        print(" ", i, n)
