# -*- coding: utf-8 -*-
from pathlib import Path
import re

for f in ["_gen_batch46.py", "_batch46_b47.py", "_batch46_b48.py", "_batch46_b49.py", "_batch46_b50.py"]:
    t = Path("tools", f).read_text(encoding="utf-8")
    bodies = re.findall(r'^\s+"(.+)",?\s*$', t, re.M)
    print(f, len(bodies))
