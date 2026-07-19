# -*- coding: utf-8 -*-
import re
import sys
from pathlib import Path

path = Path(sys.argv[1])
t = path.read_text(encoding="utf-8")
m = re.search(r'RAW = """(.*?)"""', t, re.S)
lines = [ln.strip() for ln in m.group(1).strip().splitlines() if ln.strip()]
print("count", len(lines))
for i, b in enumerate(lines, 1):
    if len(b) < 12:
        print("SHORT", i, len(b), b)
