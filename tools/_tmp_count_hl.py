# -*- coding: utf-8 -*-
from pathlib import Path
import importlib.util
import zhconv

out = []
for name in (
    "_hl_redo_07_other-20260716-47.py",
    "_hl_redo_07_other-20260716-48.py",
):
    path = Path(__file__).with_name(name)
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    out.append(f"== {name} zh-tw")
    n = 0
    for i, body in enumerate(mod.BODIES, 1):
        trad = zhconv.convert(body, "zh-tw")
        if trad != body:
            n += 1
            pairs = [f"{a}->{b}" for a, b in zip(body, trad) if a != b]
            out.append(f"{i:03d} " + " ".join(pairs))
            out.append("  SRC  " + body)
            out.append("  TW   " + trad)
    out.append(f"diff_n={n}")

Path(__file__).with_name("_tmp_zhconv_hl.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
print("wrote")
