# -*- coding: utf-8 -*-
"""Count and lint highlight bodies in the 06/07 generator."""
from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _gen_hl_04_healthcare_06_07 import BOOK_A, BOOK_B  # noqa: E402

LATIN = re.compile(r"[A-Za-z]{4,}")
SIMP = re.compile(r"[这们为来对会还从种过发经与后时实现医疗护脏脉肿晕头颈脸脚药诊验记图术纤维练盐钠钾胆减轻类样状态据报称虽则仅开关问难单复杂长宽围岁历钟苏]")


def inspect(book: dict) -> None:
    """Print count, latin leftovers, duplicates, and start repeats."""
    pts = book["points"]
    print(f"== {book['id']} count={len(pts)}")
    bodies = pts
    if len(set(bodies)) != len(bodies):
        c = Counter(bodies)
        print("dups", [k for k, v in c.items() if v > 1][:5])
    starts = Counter(b[:18] for b in bodies if len(b) >= 18)
    bad = [(k, v) for k, v in starts.most_common() if v >= 4]
    if bad:
        print("start4+", bad[:5])
    for i, b in enumerate(bodies, 1):
        if LATIN.search(b):
            print(f"latin {i}: {LATIN.search(b).group()} | {b}")
        if len(b) < 12:
            print(f"short {i}: {b}")
        if "｜" in b:
            print(f"pipe {i}")
        if SIMP.search(b):
            print(f"simp? {i}: {SIMP.search(b).group()} | {b[:40]}")


inspect(BOOK_A)
inspect(BOOK_B)
