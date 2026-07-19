# -*- coding: utf-8 -*-
import importlib.util
import json
import re
import sys
from pathlib import Path

spec = importlib.util.spec_from_file_location("fw", "tools/findbook_writer.py")
fw = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fw)

path = Path(sys.argv[1])
title = sys.argv[2] if len(sys.argv) > 2 else ""
author = sys.argv[3] if len(sys.argv) > 3 else ""
d = json.loads(path.read_text(encoding="utf-8-sig"))
highlights = d["highlights"]
NATURAL = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
for i, line in enumerate(highlights, 1):
    body = re.sub(r"^\d{3}、", "", line, count=1).strip()
    m = re.match(r"^([^：:]{1,12})[：:]", body)
    if m and not m.group(1).endswith(NATURAL):
        print(f"COLON {i}: {body[:40]}")
starts = {}
for body in [re.sub(r"^\d{3}、", "", x, count=1).strip() for x in highlights]:
    if len(body) >= 18:
        k = body[:18]
        starts[k] = starts.get(k, 0) + 1
for k, v in sorted(starts.items(), key=lambda x: -x[1]):
    if v >= 3:
        print(f"START x{v}: {k}")
try:
    fw.validate_highlights(d["id"], highlights, title, author)
    print("OK")
except Exception as e:
    print("FAIL", e)
