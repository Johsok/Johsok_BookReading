# -*- coding: utf-8 -*-
import importlib.util
import re
from collections import Counter
from pathlib import Path

p = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\_tmp\write_hl_05_15_16.py")
spec = importlib.util.spec_from_file_location("m", p)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
out = []
for name, xs in [("B15", m.B15), ("B16", m.B16)]:
    out.append(f"== {name} n={len(xs)} uniq={len(set(xs))}")
    c10 = Counter(x[:10] for x in xs)
    for k, v in c10.items():
        if v > 1:
            out.append(f"  f10 {k!r} x{v}")
    c4 = Counter(x[:4] for x in xs)
    for k, v in sorted(c4.items(), key=lambda kv: -kv[1]):
        if v > 1:
            out.append(f"  f4 {k!r} x{v}")
    for i, x in enumerate(xs, 1):
        flags = []
        if not (32 <= len(x) <= 72):
            flags.append(f"len{len(x)}")
        if re.search(r"[A-Za-z]", x):
            flags.append("latin")
        if "：" in x or ":" in x:
            flags.append("colon")
        if "章" in x:
            flags.append("zhang")
        for w in ["本書", "作者指出", "本章"]:
            if w in x:
                flags.append(w)
        if flags:
            out.append(f"  {i:03d} {' '.join(flags)} {x}")
Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\_tmp\_chk_05_15_16.txt").write_text(
    "\n".join(out), encoding="utf-8"
)
print("ok")
