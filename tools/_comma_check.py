# -*- coding: utf-8 -*-
from pathlib import Path

lines = Path("tools/_hl_redo_07_other-20260716-42.py").read_text(encoding="utf-8").splitlines()
for i, line in enumerate(lines, 1):
    s = line.rstrip()
    if s.startswith('    "') and not s.endswith('",') and s != "    ]":
        print(f"{i}: {s}")
