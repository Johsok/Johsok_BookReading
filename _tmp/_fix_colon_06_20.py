# -*- coding: utf-8 -*-
import ast
import json
import re
from pathlib import Path

p = Path(__file__).with_name("_write_06_20.py")
src = p.read_text(encoding="utf-8")
tree = ast.parse(src)
suf = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
bodies = None
for n in tree.body:
    if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", None) == "BODIES":
        bodies = [e.value for e in n.value.elts]
assert bodies and len(bodies) == 150
fixed = []
for body in bodies:
    match = re.match(r"^([^：:]{1,12})[：:]", body)
    if match and not match.group(1).endswith(suf):
        body = body.replace("：", "，", 1)
        if body[len(match.group(1))] == ":":
            body = body.replace(":", "，", 1)
    fixed.append(body)
start = src.index("BODIES = [")
end = src.index("\n]\n", start)
block = "BODIES = [\n" + ",\n".join("    " + json.dumps(b, ensure_ascii=False) for b in fixed) + "\n]"
p.write_text(src[:start] + block + src[end + 2 :], encoding="utf-8")
print("fixed", sum(a != b for a, b in zip(bodies, fixed)))
