# -*- coding: utf-8 -*-
from pathlib import Path
import re

text = Path(__file__).with_name("_write_05_06.py").read_text(encoding="utf-8")
m1 = re.search(r"BOOK1 = \[(.*?)\]\n\nBOOK2_TITLE", text, re.S)
m2 = re.search(r"BOOK2 = \[(.*?)\]\n\n\ndef scrub", text, re.S)
out = []
for name, m in [("BOOK1", m1), ("BOOK2", m2)]:
    items = re.findall(r'^\s+"(.*)",?\s*$', m.group(1), re.M)
    out.append(f"=== {name} {len(items)} ===")
    for i, s in enumerate(items, 1):
        out.append(f"{i:03d} {s}")
    out.append("")
Path(__file__).with_name("_list_dump.txt").write_text("\n".join(out), encoding="utf-8")
print("dumped")
