# -*- coding: utf-8 -*-
import importlib.util

spec = importlib.util.spec_from_file_location("m", "_tmp_ns_hl_79_80.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
with open("_len79_80.txt", "w", encoding="utf-8") as out:
    for fn, payload in m.BOOKS.items():
        items = payload["items"]
        out.write(f"{fn} count={len(items)}\n")
        for i, t in enumerate(items, 1):
            n = len(t)
            if n < 28 or n > 55:
                out.write(f"BAD {i:03d} {n} {t}\n")
        shorts = sum(1 for t in items if len(t) < 28)
        longs = sum(1 for t in items if len(t) > 55)
        out.write(f"short={shorts} long={longs} unique={len(set(items))}\n")
print("wrote")
