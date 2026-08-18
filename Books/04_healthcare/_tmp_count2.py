# -*- coding: utf-8 -*-
from pathlib import Path
ROOT = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\Books\04_healthcare")
for name in ["_hl_66_68.py", "_hl_69_71.py", "_hl_17_01_03.py", "_hl_17_04_05.py"]:
    ns = {}
    exec((ROOT / name).read_text(encoding="utf-8"), ns)
    print("FILE", name)
    for k, v in ns["HL"].items():
        print(" ", k, len(v))
