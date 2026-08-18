# -*- coding: utf-8 -*-
import ast
from pathlib import Path

for f in ["_hl_66_68.py", "_hl_69_71.py", "_hl_17_01_03.py", "_hl_17_04_05.py"]:
    p = Path(f)
    if not p.exists():
        print("missing", f)
        continue
    tree = ast.parse(p.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for tgt in node.targets:
                if isinstance(tgt, ast.Name) and tgt.id == "HL":
                    d = ast.literal_eval(node.value)
                    for k, v in d.items():
                        print(f, k, len(v))
