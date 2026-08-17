# -*- coding: utf-8 -*-
import re
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _build_hl_0610 import BOOKS

NATURAL = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
out = []
for book_id, title, author, bodies in BOOKS:
    for i, body in enumerate(bodies, 1):
        match = re.match(r"^([^：:]{1,12})[：:]", body)
        if match and not match.group(1).endswith(NATURAL):
            out.append(f"{book_id}\t{i:03d}\t{body}")
Path(__file__).with_name("_colon_hits.txt").write_text("\n".join(out), encoding="utf-8")
print("wrote", len(out))
