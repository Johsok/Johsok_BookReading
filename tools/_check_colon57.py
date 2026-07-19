# -*- coding: utf-8 -*-
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
NATURAL = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
ns = {"__file__": str(Path("tools/_gen_batch56.py").resolve())}
exec(Path("tools/_gen_batch56.py").read_text(encoding="utf-8"), ns)
for i, line in enumerate(ns["BOOK57"], 1):
    m = re.match(r"^([^：:]{1,12})[：:]", line)
    if m and not m.group(1).endswith(NATURAL):
        print(i, line)
