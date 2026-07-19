# -*- coding: utf-8 -*-
from pathlib import Path
import re

text = Path(__file__).with_name("_gen_batch77.py").read_text(encoding="utf-8")
for name in ["BOOK36", "BOOK37", "BOOK38", "BOOK39", "BOOK40"]:
    m = re.search(rf"{name}\s*=\s*\[", text)
    if not m:
        print(name, "MISSING")
        continue
    start = m.end()
    depth = 1
    i = start
    while i < len(text) and depth:
        if text[i] == "[":
            depth += 1
        elif text[i] == "]":
            depth -= 1
        i += 1
    block = text[start : i - 1]
    strings = re.findall(r'"([^"\\]*(?:\\.[^"\\]*)*)"', block)
    print(name, len(strings), "last=", strings[-1][:40] if strings else None)
