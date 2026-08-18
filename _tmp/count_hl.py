# -*- coding: utf-8 -*-
import re
from pathlib import Path

text = Path(__file__).with_name("write_34_36_highlights.py").read_text(encoding="utf-8")
for name in ["B34", "B35", "B36"]:
    start = text.index(f"{name} = [")
    end = text.index("\n]\n", start)
    block = text[start:end]
    n = len(re.findall(r'^\s+"', block, re.M))
    print(name, n)
