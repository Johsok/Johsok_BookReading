# -*- coding: utf-8 -*-
from pathlib import Path
import re
src = Path(__file__).with_name("_gen_batch4_highlights.py").read_text(encoding="utf-8")
for name in ["BOOK1", "BOOK2", "BOOK3", "BOOK4", "BOOK5"]:
    m = re.search(rf"{name} = \[(.*?)\n\]", src, re.S)
    items = re.findall(r'^\s+"(.*)",?\s*$', m.group(1), re.M)
    print(name, len(items))
