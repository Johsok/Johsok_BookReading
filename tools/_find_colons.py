# -*- coding: utf-8 -*-
import importlib.util
import re
from pathlib import Path

NATURAL = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
p = Path(__file__).with_name("_gen_grok_67_70.py")
spec = importlib.util.spec_from_file_location("gen", p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
for name in ("B67", "B68", "B69", "B70"):
    print("===", name)
    for i, body in enumerate(getattr(mod, name), 1):
        m = re.match(r"^([^：:]{1,12})[：:]", body)
        if m and not m.group(1).endswith(NATURAL):
            line = f"{i:03d}|{m.group(1)}|{body}\n"
            Path(__file__).with_name("_colon_hits.txt").open("a", encoding="utf-8").write(line)
            print("hit", name, i)
