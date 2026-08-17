# -*- coding: utf-8 -*-
from pathlib import Path
import ast, re
root = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\tools")
text = (root / "_hl_261.py").read_text(encoding="utf-8")
bodies = re.findall(r'^\s+"(.+)",\s*$', text, re.M)
avoid = (root / "_avoid_191.txt").read_text(encoding="utf-8").splitlines()
a18 = {}
for x in avoid:
    if len(x) >= 18:
        a18[x[:18]] = x
for b in bodies:
    if len(b) >= 18 and b[:18] in a18:
        print("MATCH", b[:18])
        print("  261:", b)
        print("  191:", a18[b[:18]])
print("count", len(bodies))
(root / "_chk261_out.txt").write_text(
    "\n".join(f"261:{b}\n191:{a18[b[:18]]}\n" for b in bodies if len(b) >= 18 and b[:18] in a18),
    encoding="utf-8",
)

