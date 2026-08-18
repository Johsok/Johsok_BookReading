# -*- coding: utf-8 -*-
"""Add missing trailing commas on highlight string lines."""
from pathlib import Path

path = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\_tmp\write_hl_07_61_63.py")
lines = path.read_text(encoding="utf-8").splitlines(True)
out = []
for line in lines:
    stripped = line.rstrip("\n\r")
    if stripped.startswith('    "') and stripped.endswith('"') and not stripped.endswith('",'):
        line = stripped + ",\n"
    out.append(line)
path.write_text("".join(out), encoding="utf-8")
print("fixed commas")
