# -*- coding: utf-8 -*-
from collections import Counter
from pathlib import Path
import sys

sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _gen_ot_36_40 import BOOKS  # noqa: E402

idx = int(sys.argv[1]) if len(sys.argv) > 1 else 0
pts = BOOKS[idx]["points"]
print("id", BOOKS[idx]["id"])
print("count", len(pts))
c = Counter(p[:18] for p in pts)
print("dup starts", [x for x in c.most_common(12) if x[1] > 1])
print("short", [(i + 1, len(p), p) for i, p in enumerate(pts) if len(p) < 25])
print("long", [(i + 1, len(p), p) for i, p in enumerate(pts) if len(p) > 52])
print("last5:")
for p in pts[-5:]:
    print(len(p), p)
