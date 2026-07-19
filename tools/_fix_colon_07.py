# -*- coding: utf-8 -*-
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
text = Path("tools/_gen_redo_20260713_07.py").read_text(encoding="utf-8")
chunk = text[text.index("BODIES = [") : text.index("\ndef main")]
bodies = re.findall(r'"([^"]+)"', chunk)
NATURAL = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
for i, b in enumerate(bodies, 1):
    m = re.match(r"^([^：:]{1,12})[：:]", b)
    if m and not m.group(1).endswith(NATURAL):
        print(i, b)
print("count", len(bodies))
