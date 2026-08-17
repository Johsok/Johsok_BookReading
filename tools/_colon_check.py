# -*- coding: utf-8 -*-
import ast
import re
from pathlib import Path

src = Path("tools/_gen_highlights_tmp.py").read_text(encoding="utf-8")
mod = ast.parse(src)
book1 = book2 = None
for node in mod.body:
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == "BOOK1":
                book1 = ast.literal_eval(node.value)
            if isinstance(target, ast.Name) and target.id == "BOOK2":
                book2 = ast.literal_eval(node.value)

NATURAL = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
out = []
for name, bodies in (("BOOK1", book1), ("BOOK2", book2)):
    out.append(f"## {name} n={len(bodies)}")
    for i, body in enumerate(bodies, 1):
        match = re.match(r"^([^：:]{1,12})[：:]", body)
        if match and not match.group(1).endswith(NATURAL):
            out.append(f"COLON {i:03d} prefix={match.group(1)!r} | {body}")
    out.append("")
Path("tools/_colon_report.txt").write_text("\n".join(out), encoding="utf-8")
print("wrote tools/_colon_report.txt")
