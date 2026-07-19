# -*- coding: utf-8 -*-
import ast
from pathlib import Path

path = Path(__file__).with_name("_batch47_bodies.py")
mod = ast.parse(path.read_text(encoding="utf-8"))
for node in mod.body:
    if isinstance(node, ast.Assign):
        for t in node.targets:
            if isinstance(t, ast.Name) and t.id.startswith("H"):
                if isinstance(node.value, ast.List):
                    print(t.id, len(node.value.elts))
