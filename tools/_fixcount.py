# -*- coding: utf-8 -*-
from pathlib import Path
import ast
p = Path("tools/_gen_37.py")
tree = ast.parse(p.read_text(encoding="utf-8"))
for node in tree.body:
    if isinstance(node, ast.Assign):
        for t in node.targets:
            if isinstance(t, ast.Name) and t.id == "BODIES":
                bodies = ast.literal_eval(node.value)
                print(len(bodies))
                print(repr(bodies[-3:]))
