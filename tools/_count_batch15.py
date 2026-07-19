# -*- coding: utf-8 -*-
import ast
from pathlib import Path

src = Path(__file__).with_name("_gen_batch15_highlights.py").read_text(encoding="utf-8")
mod = ast.parse(src)
for node in mod.body:
    if isinstance(node, ast.FunctionDef) and node.name.startswith("book"):
        for stmt in node.body:
            if isinstance(stmt, ast.Return) and isinstance(stmt.value, ast.Call):
                lst = stmt.value.args[0]
                if isinstance(lst, ast.List):
                    print(node.name, len(lst.elts))
