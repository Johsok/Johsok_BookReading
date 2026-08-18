# -*- coding: utf-8 -*-
from pathlib import Path

text = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\_tmp\write_hl_07_64_66.py").read_text(encoding="utf-8")
ns = {}
exec(text.split("def body_len")[0], ns)
lines = [f"{i:03d} {ns['PITA'][i-1][:22]}" for i in range(1, 153)]
Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\_tmp\_pita_idx.txt").write_text("\n".join(lines), encoding="utf-8")
print("pita", len(ns["PITA"]), "butler", len(ns["BUTLER"]), "brown", len(ns["BROWN"]))
