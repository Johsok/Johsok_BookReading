# -*- coding: utf-8 -*-
import ast
from collections import defaultdict
from pathlib import Path

src = Path(__file__).with_name("_tmp_hl_17_18.py").read_text(encoding="utf-8")
tree = ast.parse(src)
for name in ("OYSTER", "BREAD"):
    items = None
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id == name:
                    items = ast.literal_eval(node.value)
    print(name, "count", len(items), "unique", len(set(items)))
    d = defaultdict(list)
    for i, s in enumerate(items, 1):
        d[s[:3]].append(i)
    dups = {k: v for k, v in d.items() if len(v) > 1}
    print("  3-char dups", dups or "none")
    d2 = defaultdict(list)
    for i, s in enumerate(items, 1):
        d2[s[:2]].append(i)
    dups2 = {k: v for k, v in d2.items() if len(v) > 1}
    if dups2:
        print("  2-char dups count", len(dups2))
        for k, v in list(dups2.items())[:20]:
            print("   ", k, v)
