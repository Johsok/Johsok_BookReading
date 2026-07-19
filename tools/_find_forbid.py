# -*- coding: utf-8 -*-
from pathlib import Path
import re

src = Path(__file__).with_name("_gen_chunk20_highlights.py").read_text(encoding="utf-8")
src = src.replace('if __name__ == "__main__":\n    main()\n', "")
ns = {"__name__": "g", "__file__": "x"}
exec(compile(src, "x", "exec"), ns)
forbid = ("本書", "作者指出", "本章", "這一章", "｜")
for bid, bodies in ns["BOOKS"].items():
    for i, b in enumerate(bodies, 1):
        for f in forbid:
            if f in b:
                print(bid, i, f, b)
