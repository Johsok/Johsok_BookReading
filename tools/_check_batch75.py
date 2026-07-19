# -*- coding: utf-8 -*-
import importlib.util
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
spec = importlib.util.spec_from_file_location("g", "tools/_gen_batch75.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

for b in m.BOOKS:
    print(b["id"], len(b["lines"]))
    for i, line in enumerate(b["lines"], 1):
        if any(p in line for p in ("本書", "作者指出", "本章", "這一章")):
            print(" FORBIDDEN", i, line)
        if len(line) < 12:
            print(" SHORT", i, line)
    try:
        h = m.numbered(b["lines"])
        m.validate_local(b["id"], h, b["title"], b["author"])
        print(" OK")
    except Exception as e:
        print(" FAIL", e)
