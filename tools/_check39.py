# -*- coding: utf-8 -*-
import ast, re
from pathlib import Path
NATURAL = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
tree = ast.parse(Path("tools/_gen_39.py").read_text(encoding="utf-8"))
for node in tree.body:
    if isinstance(node, ast.Assign):
        for t in node.targets:
            if isinstance(t, ast.Name) and t.id == "BODIES":
                bodies = ast.literal_eval(node.value)
print("count", len(bodies), "unique", len(set(bodies)))
for i, b in enumerate(bodies, 1):
    m = re.match(r"^([^：:]{1,12})[：:]", b)
    if m and not m.group(1).endswith(NATURAL):
        print("COLON", i, b)
    if "冗余" in b or "本书" in b:
        print("SIMP", i, b)
