# -*- coding: utf-8 -*-
from pathlib import Path
import re

text = Path(__file__).with_name("_write_05_06.py").read_text(encoding="utf-8")
m1 = re.search(r"BOOK1 = \[(.*?)\]\n\nBOOK2_TITLE", text, re.S)
m2 = re.search(r"BOOK2 = \[(.*?)\]\n\n\ndef scrub", text, re.S)
for name, m in [("BOOK1", m1), ("BOOK2", m2)]:
    items = re.findall(r'^\s+"(.*)",?\s*$', m.group(1), re.M)
    print(name, len(items))
    print(" last:", items[-1][:40] if items else None)
    print(" first:", items[0][:40] if items else None)
