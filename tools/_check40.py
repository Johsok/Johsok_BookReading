# -*- coding: utf-8 -*-
import ast, re
from pathlib import Path
NATURAL = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
tree = ast.parse(Path("tools/_gen_40.py").read_text(encoding="utf-8"))
for node in tree.body:
    if isinstance(node, ast.Assign):
        for t in node.targets:
            if isinstance(t, ast.Name) and t.id == "BODIES":
                bodies = ast.literal_eval(node.value)
print("count", len(bodies), "unique", len(set(bodies)))
title = "入世賽局：衝突的策略"
author = "張華"
print("title hits", sum(title in b for b in bodies))
print("author hits", sum(author in b for b in bodies))
for i, b in enumerate(bodies, 1):
    m = re.match(r"^([^：:]{1,12})[：:]", b)
    if m and not m.group(1).endswith(NATURAL):
        print("COLON", i, b[:40])
    for ch in ("烧掉", "会", "为了", "这个"):
        if ch in b:
            print("SIMP", i, b[:50])
