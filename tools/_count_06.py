# -*- coding: utf-8 -*-
import importlib.util
import re
from collections import Counter
from pathlib import Path

path = Path(__file__).with_name("_gen_grok_06.py")
spec = importlib.util.spec_from_file_location("g06", path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
bodies = mod.BODIES
print("count", len(bodies))
suffixes = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
short = []
for i, body in enumerate(bodies, 1):
    match = re.match(r"^([^：:]{1,12})[：:]", body)
    if match and not match.group(1).endswith(suffixes):
        short.append((i, match.group(1), body[:40]))
print("short_colon", len(short))
for item in short:
    print(item)
rep = Counter(b[:18] for b in bodies if len(b) >= 18)
print("top starts", rep.most_common(8))
