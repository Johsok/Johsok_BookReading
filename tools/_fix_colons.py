# -*- coding: utf-8 -*-
import re
from pathlib import Path

path = Path(__file__).with_name("_build_hl_0610.py")
text = path.read_text(encoding="utf-8")
hits = Path(__file__).with_name("_colon_hits.txt").read_text(encoding="utf-8").splitlines()
missing = 0
for row in hits:
    body = row.split("\t", 2)[2]
    new = re.sub(r"^([^：:]{1,12})[：:]", r"\1，", body, count=1)
    if body not in text:
        print("MISSING", body[:40])
        missing += 1
        continue
    text = text.replace(body, new, 1)
path.write_text(text, encoding="utf-8")
print("missing", missing)
