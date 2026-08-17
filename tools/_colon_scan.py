# -*- coding: utf-8 -*-
import importlib.util
import re
from pathlib import Path

spec = importlib.util.spec_from_file_location("g", Path("tools/_gen_pg_196_200.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
suf = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
out = []
for name in ["B196", "B197", "B198", "B199", "B200"]:
    bodies = getattr(mod, name)
    hits = []
    for i, body in enumerate(bodies, 1):
        mm = re.match(r"^([^：:]{1,12})[：:]", body)
        if mm and not mm.group(1).endswith(suf):
            hits.append(f"{i:03d}\t[{mm.group(1)}]\t{body}")
    out.append(f"== {name} count={len(hits)}")
    out.extend(hits)
Path("tools/_colon_hits.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
print("wrote", len(out))
