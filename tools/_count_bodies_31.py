# -*- coding: utf-8 -*-
import ast
from pathlib import Path

src = Path(__file__).with_name("_gen_grok_01_business_startup-20260713-31.py").read_text(encoding="utf-8")
mod = ast.parse(src)
bodies = None
for node in mod.body:
    if isinstance(node, ast.Assign):
        for t in node.targets:
            if isinstance(t, ast.Name) and t.id == "BODIES":
                bodies = ast.literal_eval(node.value)
print(len(bodies))
for i, b in enumerate(bodies, 1):
    print(f"{i:03d}\t{len(b)}\t{b}")
