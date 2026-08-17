# -*- coding: utf-8 -*-
import ast, re
from pathlib import Path

bodies = ast.literal_eval(Path("tools/_hl_184.py").read_text(encoding="utf-8").split("BODIES = ", 1)[1])
print("count", len(bodies))
NATURAL = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
for i in (108, 119, 133):
    print(i, bodies[i - 1])
print("--- all short colons ---")
for i, b in enumerate(bodies, 1):
    match = re.match(r"^([^：:]{1,12})[：:]", b)
    if match and not match.group(1).endswith(NATURAL):
        print(i, match.group(1), "|", b[:60])
