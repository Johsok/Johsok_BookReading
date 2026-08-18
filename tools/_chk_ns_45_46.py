# -*- coding: utf-8 -*-
import re
from collections import Counter
from pathlib import Path

p = Path(__file__).with_name("_gen_ns_45_46.py")
ns = {}
exec(compile(p.read_text(encoding="utf-8"), str(p), "exec"), ns)
forb = ["本書", "作者指出", "本章", "這一章", "｜", "：", "第一步"]
for name in ("BOOK45", "BOOK46"):
    L = ns[name]
    assert len(L) == 150 and len(set(L)) == 150
    assert all(len(s) >= 12 for s in L)
    o2 = Counter(s[:2] for s in L)
    d2 = {k: v for k, v in o2.items() if v > 1}
    print(name, "ok", "dup2", d2)
    for f in forb:
        hits = [s for s in L if f in s]
        if hits:
            print(" FORB", f, hits)
    colon = [s for s in L if ":" in s]
    if colon:
        print(" colon", colon)
    steps = [s for s in L if re.search(r"第[一二三四五六七八九十0-9]+步", s)]
    if steps:
        print(" steps", steps)
print("assert passed")
