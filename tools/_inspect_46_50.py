# -*- coding: utf-8 -*-
from pathlib import Path
import importlib.util

p = Path(__file__).with_name("_gen_grok_20260717_46_50.py")
spec = importlib.util.spec_from_file_location("g", p)
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

for name in ("B46", "B47", "B48", "B49", "B50"):
    bodies = getattr(g, name)
    print("====", name, len(bodies), "====")
    for i, b in enumerate(bodies, 1):
        bad = []
        if len(b) < 12:
            bad.append("short")
        if any(c.isascii() and c.isalpha() for c in b):
            bad.append("ascii")
        if " luc" in b or "overlay" in b or "domest" in b or "lucid" in b:
            bad.append("junk")
        if bad:
            print(f"{i:03d} {'/'.join(bad)} {b}")
    starts = {}
    for b in bodies:
        starts.setdefault(b[:18], []).append(b[:24])
    reps = {k: v for k, v in starts.items() if len(v) >= 2}
    if reps:
        print("repeat-starts", len(reps))
        for k, v in list(reps.items())[:8]:
            print(" ", k, len(v))
    dups = [b for b in bodies if bodies.count(b) > 1]
    if dups:
        print("dups", set(dups))
