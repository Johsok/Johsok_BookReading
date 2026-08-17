# -*- coding: utf-8 -*-
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _build_hl_0610 import BOOKS, numbered

NATURAL = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")

for book_id, title, author, bodies in BOOKS:
    hits = []
    for i, body in enumerate(bodies, 1):
        match = re.match(r"^([^：:]{1,12})[：:]", body)
        if match and not match.group(1).endswith(NATURAL):
            hits.append((i, match.group(1), body))
    print(f"\n{book_id} short-colon={len(hits)}")
    for i, prefix, body in hits:
        print(f"  {i:03d} [{prefix}] {body}")
