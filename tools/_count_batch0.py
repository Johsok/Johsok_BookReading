# -*- coding: utf-8 -*-
from pathlib import Path
import re

text = Path(__file__).with_name("_gen_batch0_highlights.py").read_text(encoding="utf-8")
parts = re.split(r'BOOKS\["([^"]+)"\]\s*=\s*\[', text)
i = 1
while i < len(parts):
    bid = parts[i]
    body = parts[i + 1]
    end = re.search(r"\n\]\s*\n", body)
    block = body[: end.start()] if end else body
    strings = re.findall(r'"([^"]*)"', block)
    print(bid, len(strings))
    i += 2
