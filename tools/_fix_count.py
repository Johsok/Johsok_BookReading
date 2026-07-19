# -*- coding: utf-8 -*-
import ast
from pathlib import Path

for name in ("_gen_156.py", "_gen_157.py", "_gen_158.py"):
    t = Path(__file__).with_name(name).read_text(encoding="utf-8")
    lst = ast.literal_eval(t.split("HIGHLIGHTS = ", 1)[1].split("def main", 1)[0].strip())
    print(name, len(lst), len(set(lst)))
