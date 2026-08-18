# -*- coding: utf-8 -*-
from pathlib import Path
import json

t = Path("_gen_hl_36_40.py").read_text(encoding="utf-8")
s = t.split("BOOK36 = [")[1].split("BOOK37 = [")[0]
items = []
for line in s.splitlines():
    line = line.strip()
    if line.startswith('"') and line.endswith('",'):
        items.append(line[1:-2])
    elif line.startswith('"') and line.endswith('"'):
        items.append(line[1:-1])
Path("_b36.json").write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
print(len(items), "written")
