# -*- coding: utf-8 -*-
from collections import Counter
import importlib.util
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
p = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("pts", p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
pts = mod.POINTS
print("file", p.name)
print("count", len(pts))
c = Counter(x[:18] for x in pts)
print("dup starts", [item for item in c.most_common(12) if item[1] > 1])
print("short", [(i + 1, len(x), x) for i, x in enumerate(pts) if len(x) < 25])
print("long", [(i + 1, len(x), x) for i, x in enumerate(pts) if len(x) > 52])
latin = [(i + 1, x) for i, x in enumerate(pts) if any(ord(ch) < 128 and ch.isalpha() for ch in x)]
print("latin", latin)
print("last3:")
for x in pts[-3:]:
    print(len(x), x)
