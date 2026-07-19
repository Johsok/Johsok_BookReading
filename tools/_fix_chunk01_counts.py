# -*- coding: utf-8 -*-
import ast
import pathlib

for name in [
    "_gen_chunk01_b64.py",
    "_gen_chunk01_b65.py",
]:
    p = pathlib.Path("tools") / name
    t = p.read_text(encoding="utf-8")
    start = t.index("BODIES = [")
    end = t.index("\n\nassert len")
    bodies = ast.literal_eval(t[start + len("BODIES = ") : end])
    print(name, len(bodies))
    for bad in ["口号", "危险", "不等于", "撑不久", "自以为"]:
        hits = [i for i, b in enumerate(bodies, 1) if bad in b]
        if hits:
            print(" ", bad, hits)
