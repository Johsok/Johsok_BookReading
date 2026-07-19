# -*- coding: utf-8 -*-
from pathlib import Path
import ast

for n in [67, 68, 69, 70]:
    path = Path(f"tools/_gen_batch30_{n}.py")
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id == "bodies":
                    print(n, len(node.value.elts))
