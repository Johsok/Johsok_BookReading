# -*- coding: utf-8 -*-
import importlib.util
from pathlib import Path

p = Path(__file__).with_name("hl_06_29_30.py")
spec = importlib.util.spec_from_file_location("hl", p)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
out = []
for name, xs in [("HL29", m.HL29), ("HL30", m.HL30)]:
    out.append(f"==== {name} {len(xs)}")
    for i, b in enumerate(xs, 1):
        flags = []
        n = len(b)
        if n < 28 or n > 78:
            flags.append(f"LEN{n}")
        if "：" in b[:13] or ":" in b[:13]:
            flags.append("COLON")
        if flags:
            out.append(f"{i:03d} {' '.join(flags)} {b}")
Path(__file__).with_name("_chk_29_30.txt").write_text("\n".join(out), encoding="utf-8")
print("wrote", len(out))
