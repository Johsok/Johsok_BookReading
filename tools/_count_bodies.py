# -*- coding: utf-8 -*-
import re
import sys
from pathlib import Path

path = Path(sys.argv[1])
text = path.read_text(encoding="utf-8")
m = re.search(r"BODIES\s*=\s*\[(.*)\]\s*\n\n\ndef main", text, re.S)
if not m:
    raise SystemExit("no bodies")
items = re.findall(r'"([^"\\]*(?:\\.[^"\\]*)*)"', m.group(1))
print(path.name, len(items))
