# -*- coding: utf-8 -*-
import importlib.util
from pathlib import Path
import re

NATURAL = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
p = Path(__file__).with_name("_gen_194.py")
spec = importlib.util.spec_from_file_location("g", p)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
hits = []
for i, b in enumerate(m.BODIES, 1):
    match = re.match(r"^([^：:]{1,12})[：:]", b)
    if match and not match.group(1).endswith(NATURAL):
        hits.append(f"{i}\t{match.group(1)}\t{b}")
Path(__file__).with_name("_colon_hits.txt").write_text(
    "\n".join(hits) + f"\ncount {len(m.BODIES)}\n", encoding="utf-8"
)
