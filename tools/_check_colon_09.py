# -*- coding: utf-8 -*-
import re
from pathlib import Path

text = Path(__file__).with_name("_gen_grok_01_business_startup-20260713-09.py").read_text(encoding="utf-8")
chunk = text[text.index("BODIES = [") : text.index("\n]\n\nassert")]
bodies = re.findall(r'"([^"]+)"', chunk)
NATURAL = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
print("count", len(bodies))
for i, body in enumerate(bodies, 1):
    match = re.match(r"^([^：:]{1,12})[：:]", body)
    if match and not match.group(1).endswith(NATURAL):
        print(i, body)
