# -*- coding: utf-8 -*-
from pathlib import Path
import re

text = Path("_tmp/write_ns19_06_10.py").read_text(encoding="utf-8")
NATURAL = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
out = []
for name in ["B06", "B07", "B08", "B09", "B10"]:
    m = re.search(rf"{name} = \[(.*?)\n\]\n", text, re.S)
    items = re.findall(r'^    "(.+)",?\s*$', m.group(1), re.M)
    out.append(f"{name} count={len(items)} unique={len(set(items))}")
    for i, body in enumerate(items, 1):
        match = re.match(r"^([^：:]{1,12})[：:]", body)
        if match and not match.group(1).endswith(NATURAL):
            out.append(f"  COLON {i} {body[:50]}")
        if "mill " in body or "分区" in body or "蚂蚁" in body or "英语" in body:
            out.append(f"  BAD {i} {body}")
Path("_tmp/_colon_out2.txt").write_text("\n".join(out), encoding="utf-8")
print("ok")
