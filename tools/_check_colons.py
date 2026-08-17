# -*- coding: utf-8 -*-
import ast
import re
from pathlib import Path

src = Path("tools/_gen_43_highlights.py").read_text(encoding="utf-8")
tree = ast.parse(src)
bodies = None
for node in tree.body:
    if isinstance(node, ast.Assign):
        for t in node.targets:
            if isinstance(t, ast.Name) and t.id == "BODIES":
                bodies = ast.literal_eval(node.value)

NATURAL = ("是", "說", "在於", "表示", "等於", "就像", "好比", "意味著")
for i, body in enumerate(bodies, 1):
    m = re.match(r"^([^：:]{1,12})[：:]", body)
    if m and not m.group(1).endswith(NATURAL):
        print(f"{i:03d} LABEL={m.group(1)!r} :: {body}")
print("total", len(bodies))
