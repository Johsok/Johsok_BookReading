# -*- coding: utf-8 -*-
import re
import sys
from pathlib import Path

sys.path.insert(0, "tools")
from _assemble_71_75 import load_raw_blocks, pick_150

NATURAL = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
pat = re.compile(r"^([^：:]{1,12})[：:]")
out = []
blocks = load_raw_blocks()
for bid in [
    "02_psychology_growth-20260717-72",
    "02_psychology_growth-20260717-73",
    "02_psychology_growth-20260717-74",
]:
    lines = blocks[bid]
    if bid.endswith(("-74", "-75")) or len(lines) != 150:
        lines = pick_150(lines)
    out.append(f"==== {bid} n={len(lines)}")
    n = 0
    for i, body in enumerate(lines, 1):
        m = pat.match(body)
        if m and not m.group(1).endswith(NATURAL):
            n += 1
            out.append(f"{i:03d} [{m.group(1)}] {body}")
    out.append(f"TOTAL {n}")
Path("tools/_colon_diag.txt").write_text("\n".join(out), encoding="utf-8")
print("ok")
