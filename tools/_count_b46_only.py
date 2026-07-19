# -*- coding: utf-8 -*-
from pathlib import Path
import re

text = Path("tools/_gen_batch46.py").read_text(encoding="utf-8")
start = text.index("BOOK46 = [")
end = text.index("]", start)
block = text[start:end]
bodies = re.findall(r'^\s+"(.*)"\s*,?\s*$', block, re.M)
print("count", len(bodies), "unique", len(set(bodies)))
dups = [b for b in set(bodies) if bodies.count(b) > 1]
print("dups", dups)
