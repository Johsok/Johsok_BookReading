# -*- coding: utf-8 -*-
from __future__ import annotations

import re
from pathlib import Path

text = Path(__file__).with_name("_gen_batch76.py").read_text(encoding="utf-8")
for name in ["BOOK76", "BOOK77", "BOOK78", "BOOK79", "BOOK80"]:
    m = re.search(rf"{name} = \[(.*?)]\n\n", text, re.S)
    if not m:
        print(name, "NOT FOUND")
        continue
    lines = re.findall(r'"([^"]+)"', m.group(1))
    print(name, "count", len(lines))
    for i, body in enumerate(lines, 1):
        reasons = []
        if len(body) < 12:
            reasons.append("short")
        if "\ufffd" in body:
            reasons.append("replacement")
        if "equ" in body:
            reasons.append("equ")
        if reasons:
            print(f"  {i}: {reasons} | {body}")
