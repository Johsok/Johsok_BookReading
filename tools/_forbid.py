# -*- coding: utf-8 -*-
import sys
from pathlib import Path
sys.path.insert(0, "tools")
from _assemble_71_75 import load_raw_blocks

blocks = load_raw_blocks()
for bid in [
    "02_psychology_growth-20260717-72",
    "02_psychology_growth-20260717-73",
    "02_psychology_growth-20260717-74",
]:
    lines = blocks[bid]
    if len(lines) != 150 and bid.endswith(("-74", "-75")):
        from _assemble_71_75 import pick_150
        lines = pick_150(lines)
    out = []
blocks = load_raw_blocks()
from _assemble_71_75 import pick_150, META, clean_line
for bid in META:
    lines = blocks[bid]
    if bid.endswith(("-74", "-75")) or len(lines) != 150:
        lines = pick_150(lines)
    out.append(f"==== {bid} n={len(lines)}")
    for i, b in enumerate(lines, 1):
        for p in ("本書", "作者指出", "本章", "這一章"):
            if p in b:
                out.append(f"{i:03d} [{p}] {b}")
Path("tools/_forbid.txt").write_text("\n".join(out), encoding="utf-8")
print("wrote")
