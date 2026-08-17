# -*- coding: utf-8 -*-
from pathlib import Path
import re
t = Path("tools/_gen_pg_203_207.py").read_text(encoding="utf-8")
m = re.search(r'"points": \[([\s\S]*?)\n        \],', t)
items = re.findall(r'^\s+"(.*)"', m.group(1), re.M)
Path("tools/_count_out.txt").write_text(
    "count %s\n" % len(items)
    + "\n".join("%03d %s" % (i, s) for i, s in enumerate(items, 1) if any(x in s for x in ("格局", "喬潔", "multip")))
    + "\nmaxstart %s dup %s short %s\n"
    % (
        max((__import__("collections").Counter(s[:18] for s in items)).values()),
        len(items) - len(set(items)),
        [s for s in items if len(s) < 12],
    ),
    encoding="utf-8",
)
starts = {}
for s in items:
    k = s[:18]
    starts[k] = starts.get(k, 0) + 1
print("max start", max(starts.values()) if starts else 0)
print("dup bodies", len(items) - len(set(items)))
print("short", [s for s in items if len(s) < 12])
