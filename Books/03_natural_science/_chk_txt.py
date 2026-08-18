# -*- coding: utf-8 -*-
import pathlib
import sys

p = pathlib.Path(sys.argv[1])
items = [ln.strip() for ln in p.read_text(encoding="utf-8").splitlines() if ln.strip()]
print("n", len(items), p.name)
seen = set()
for i, t in enumerate(items, 1):
    n = len(t)
    flags = []
    if n < 22 or n > 54:
        flags.append(f"LEN{n}")
    if t in seen:
        flags.append("DUP")
    seen.add(t)
    if any(ch.isascii() and ch.isalpha() for ch in t):
        flags.append("ASCII")
    if flags:
        print(f"{i:03d} {' '.join(flags)} {t}")
