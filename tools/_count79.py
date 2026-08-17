# -*- coding: utf-8 -*-
import ast
import re
from collections import Counter
from pathlib import Path

src = Path(__file__).with_name("_hl_78_82.py").read_text(encoding="utf-8")
mod = ast.parse(src)
name = "BOOK_82"
bodies = None
for node in mod.body:
    if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.target.id == name:
        bodies = ast.literal_eval(node.value)
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == name:
                bodies = ast.literal_eval(node.value)

NATURAL_COLON_SUFFIXES = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
lines = []
lines.append(f"count={len(bodies)}")
lines.append(f"minlen={min(len(b) for b in bodies)}")
lines.append(f"dups={len(bodies)-len(set(bodies))}")
c = Counter(b[:18] for b in bodies)
lines.append(f"maxstart={c.most_common(3)}")
for i, body in enumerate(bodies, 1):
    match = re.match(r"^([^：:]{1,12})[：:]", body)
    if match and not match.group(1).endswith(NATURAL_COLON_SUFFIXES):
        lines.append(f"COLON {i} {body}")
    if "｜" in body or "本書" in body or "作者指出" in body or "本章" in body or "這一章" in body:
        lines.append(f"FORB {i} {body}")
Path(__file__).with_name("_n82.txt").write_text("\n".join(lines), encoding="utf-8")
