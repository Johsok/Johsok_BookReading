# -*- coding: utf-8 -*-
import importlib.util
import re
from pathlib import Path

p = Path(__file__).with_name("_gen_chunk20_highlights.py")
src = p.read_text(encoding="utf-8").replace('if __name__ == "__main__":\n    main()\n', "")
ns = {"__name__": "g", "__file__": str(p)}
exec(compile(src, str(p), "exec"), ns)

NATURAL = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
for book_id, bodies in ns["BOOKS"].items():
    bad = []
    for i, b in enumerate(bodies, 1):
        m = re.match(r"^([^：:]{1,12})[：:]", b)
        if m and not m.group(1).endswith(NATURAL):
            bad.append((i, b[:40]))
    if bad:
        print(book_id, "short colon", len(bad))
        for x in bad:
            print(" ", x)
