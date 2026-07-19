# -*- coding: utf-8 -*-
from pathlib import Path
import re

code = Path(__file__).with_name("_gen_batch28_highlights.py").read_text(encoding="utf-8")
code2 = re.sub(r"^BOOKS\[.*?\]\[\d+\] = \([\s\S]*?^\)$", "", code, flags=re.M)
code2 = re.sub(r'^BOOKS\[.*?\]\[\d+\] = ".*$', "", code2, flags=re.M)
prefix = code2.split("def write_and_complete")[0]
ns = {"__file__": str(Path(__file__).resolve())}
exec(compile(prefix, "x", "exec"), ns)
for k, v in ns["BOOKS"].items():
    print(k, len(v))
    # show lines with latin letters
    for i, line in enumerate(v):
        if re.search(r"[A-Za-z]", line):
            print("  latin", i, line)
