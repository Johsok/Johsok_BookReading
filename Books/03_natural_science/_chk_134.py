# -*- coding: utf-8 -*-
import pathlib
ns = {}
exec(compile(pathlib.Path("_write_hl_134_137.py").read_text(encoding="utf-8"), "x", "exec"), ns)
items = ns["BOOKS"]["03_natural_science-20260716-134.json"]["items"]
print("n", len(items))
seen = set()
for i, t in enumerate(items, 1):
    n = len(t)
    if n < 22 or n > 54:
        print(i, "LEN", n, t)
    if t in seen:
        print(i, "DUP", t)
    seen.add(t)
    if any(ch.isascii() and ch.isalpha() for ch in t):
        print(i, "ASCII", t)
