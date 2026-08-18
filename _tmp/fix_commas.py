# -*- coding: utf-8 -*-
import re
from pathlib import Path

p = Path(__file__).with_name("write_25_26_highlights.py")
t = p.read_text(encoding="utf-8")
t2 = re.sub(r'^(\s+"\d{3}、.*。)"\s*$', r'\1",', t, flags=re.M)
p.write_text(t2, encoding="utf-8")
print("changed", t != t2)
