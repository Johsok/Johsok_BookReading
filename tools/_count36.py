# -*- coding: utf-8 -*-
from pathlib import Path
import ast

src = Path("tools/_gen_36.py").read_text(encoding="utf-8")
tree = ast.parse(src)
for node in tree.body:
    if isinstance(node, ast.Assign):
        for t in node.targets:
            if isinstance(t, ast.Name) and t.id == "BODIES":
                bodies = ast.literal_eval(node.value)
                print("count", len(bodies))
                print("unique", len(set(bodies)))
                for i, b in enumerate(bodies, 1):
                    print(f"{i:03d}|{b}")
