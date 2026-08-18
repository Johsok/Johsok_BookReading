# -*- coding: utf-8 -*-
import ast
import pathlib
import sys

p = pathlib.Path(sys.argv[1])
mod = ast.parse(p.read_text(encoding="utf-8"))
for node in mod.body:
    if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
        name = node.targets[0].id
        if name.startswith("B") and isinstance(node.value, ast.List):
            print(name, len(node.value.elts))
