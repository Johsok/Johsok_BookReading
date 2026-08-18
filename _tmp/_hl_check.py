# -*- coding: utf-8 -*-
from pathlib import Path

text = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\_tmp\write_hl_07_64_66.py").read_text(encoding="utf-8")
ns = {}
exec(text.split("def body_len")[0], ns)
out = []
for name in ("PITA", "BUTLER", "BROWN"):
    xs = ns[name]
    out.append(f"=== {name} {len(xs)} ===")
    for i, s in enumerate(xs, 1):
        n = len(s)
        flags = []
        if n < 30 or n > 70:
            flags.append(f"LEN{n}")
        letters = "".join(c for c in s if c.isascii() and c.isalpha())
        if letters:
            flags.append("EN:" + letters)
        if flags:
            out.append(f"{i:03d} {' '.join(flags)} {s}")
Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\_tmp\_hl_check.txt").write_text(
    "\n".join(out), encoding="utf-8"
)
print("ok")
