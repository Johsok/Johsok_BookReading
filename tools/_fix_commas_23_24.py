# -*- coding: utf-8 -*-
import re
from pathlib import Path

p = Path(__file__).with_name("_gen_psych_23_24.py")
text = p.read_text(encoding="utf-8")
fixed = re.sub(r"(\"[^\"]+\")(\r?\n)(    \")", r"\1,\2\3", text)
p.write_text(fixed, encoding="utf-8")
ns = {"__file__": str(p.resolve())}
exec(fixed.split("def pack")[0], ns)
print("A", len(ns["A"]), "B", len(ns["B"]))
