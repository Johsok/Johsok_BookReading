# -*- coding: utf-8 -*-
"""Dump highlight validation flags for books 43 and 44."""
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\_tmp")
import write_hl_07_43 as a
import write_hl_07_44 as b

out = []
for name, xs in [("43", a.B43), ("44", b.B44)]:
    out.append(f"=== {name} count={len(xs)} ===")
    for i, s in enumerate(xs, 1):
        flags = []
        n = len(s)
        if n < 32 or n > 68:
            flags.append(f"LEN{n}")
        if any(x in s for x in ("本書", "作者指出", "本章", "這一章", "｜", ":", "：")):
            flags.append("BAN")
        if "第" in s and "章" in s:
            flags.append("CH")
        letters = "".join(c for c in s if c.isascii() and c.isalpha())
        if letters:
            flags.append("EN:" + letters)
        if flags:
            out.append(f"{i:03d} {' '.join(flags)} {s}")
    pref = Counter(s[:18] for s in xs)
    for k, v in pref.items():
        if v >= 4:
            out.append(f"PREF {v} {k}")

Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\_tmp\_chk_43_44.txt").write_text(
    "\n".join(out), encoding="utf-8"
)
print("ok", len(a.B43), len(b.B44))
