# -*- coding: utf-8 -*-
from pathlib import Path
import ast
import re

p = Path("tools/_gen_pg_206.py")
t = p.read_text(encoding="utf-8")
m = re.search(r'"points": \[([\s\S]*?)\n    \],', t)
items = re.findall(r'^\s+"(.*)"', m.group(1), re.M)
from collections import Counter
c = Counter(s[:18] for s in items)
out = []
out.append(f"count={len(items)}")
out.append(f"dup={len(items)-len(set(items))}")
out.append(f"maxstart={c.most_common(3)}")
out.append(f"titlehits={sum('細節' in s for s in items)}")
out.append(f"authorhits={sum('高文斐' in s for s in items)}")
out.append(f"item45={items[44] if len(items)>44 else 'NA'}")
for i,s in enumerate(items,1):
    if any(p in s for p in ("本書", "作者指出", "本章", "這一章")):
        out.append(f"forb {i} {s}")
# prefix clusters
pref = Counter(s[:6] for s in items)
out.append("pref6=" + str(pref.most_common(8)))
Path("tools/_count_out.txt").write_text("\n".join(out), encoding="utf-8")
