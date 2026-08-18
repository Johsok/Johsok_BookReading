# -*- coding: utf-8 -*-
from pathlib import Path
import re

text = Path("_tmp/write_ns19_01_05.py").read_text(encoding="utf-8")
NATURAL = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
out = []
for name in ["B01", "B02", "B03", "B04", "B05"]:
    m = re.search(rf"{name} = \[(.*?)\n\]\n", text, re.S)
    items = re.findall(r'^    "(.+)",?\s*$', m.group(1), re.M)
    out.append(f"{name}")
    for i, body in enumerate(items, 1):
        match = re.match(r"^([^：:]{1,12})[：:]", body)
        if match and not match.group(1).endswith(NATURAL):
            out.append(f"{i}\t{body}")
Path("_tmp/_colon_out.txt").write_text("\n".join(out), encoding="utf-8")
print("wrote", len(out))
