# -*- coding: utf-8 -*-
import importlib.util
import re
from pathlib import Path

p = Path("tools/_gen_chunk02_highlights.py")
spec = importlib.util.spec_from_file_location("g", p)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

NATURAL = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
for i, body in enumerate(m.BOOK68, 1):
    match = re.match(r"^([^：:]{1,12})[：:]", body)
    if match and not match.group(1).endswith(NATURAL):
        print(f"{i:03d}|{body}")
