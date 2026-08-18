# -*- coding: utf-8 -*-
import ast
from pathlib import Path
src = Path("_tmp/write_ns19_06_10.py").read_text(encoding="utf-8")
mod = ast.parse(src)
for node in mod.body:
    if isinstance(node, ast.Assign):
        for t in node.targets:
            if isinstance(t, ast.Name) and t.id.startswith("B"):
                val = ast.literal_eval(node.value)
                print(t.id, len(val), len(set(val)))
