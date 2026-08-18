# -*- coding: utf-8 -*-
import ast
from pathlib import Path

src = Path("_hl_66_68.py").read_text(encoding="utf-8")
tree = ast.parse(src)
for node in tree.body:
    if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id == "HL":
        # walk keys
        for key, val in zip(node.value.keys, node.value.values):
            k = ast.literal_eval(key)
            if k.endswith("68"):
                print("ast elts", len(val.elts))
                # find concatenated (Joined? or Constant that's huge)
                for i, el in enumerate(val.elts):
                    if not isinstance(el, ast.Constant):
                        print("nonconst", i, type(el), ast.dump(el)[:200])
                    elif isinstance(el, ast.Constant) and isinstance(el.value, str) and len(el.value) > 120:
                        print("long", i, len(el.value), el.value[:80])

ns = {}
exec(src, ns)
print("exec", len(ns["HL"]["04_healthcare-20260716-68"]))
# compare
ast_list = ast.literal_eval(val) if False else None
