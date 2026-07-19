# -*- coding: utf-8 -*-
import re
import sys
from pathlib import Path

sys.path.insert(0, "tools")
from findbook_writer import NATURAL_COLON_SUFFIXES

path = Path(sys.argv[1])
text = path.read_text(encoding="utf-8")
m = re.search(r"BODIES\s*=\s*\[(.*)\]\s*\n\n\ndef main", text, re.S)
items = re.findall(r'"([^"]*)"', m.group(1))
print(path.name, "count", len(items))
for i, b in enumerate(items, 1):
    match = re.match(r"^([^：:]{1,12})[：:]", b)
    if match and not match.group(1).endswith(NATURAL_COLON_SUFFIXES):
        print(i, repr(match.group(1)), "=>", b)
