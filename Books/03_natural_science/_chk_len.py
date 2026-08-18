# -*- coding: utf-8 -*-
import pathlib

ns = {}
exec(compile(pathlib.Path("_write_hl_131_133.py").read_text(encoding="utf-8"), "x", "exec"), ns)
out = []
for k, v in ns["BOOKS"].items():
    items = v["items"]
    out.append(f"=== {k} n={len(items)}")
    seen = set()
    for i, t in enumerate(items, 1):
        n = len(t)
        flags = []
        if n < 22 or n > 54:
            flags.append(f"LEN{n}")
        if t in seen:
            flags.append("DUP")
        seen.add(t)
        if any(c.isascii() and c.isalpha() for c in t):
            flags.append("ASCII")
        if flags:
            out.append(f"{i:03d} {' '.join(flags)} {t}")
pathlib.Path("_chk_hl.txt").write_text("\n".join(out), encoding="utf-8")
print("wrote", len(out))
