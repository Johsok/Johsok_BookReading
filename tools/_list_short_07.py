# -*- coding: utf-8 -*-
import importlib.util
import re
from pathlib import Path

path = Path(__file__).with_name("_gen_grok_07.py")
spec = importlib.util.spec_from_file_location("g07", path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
suffixes = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
out = Path(__file__).with_name("_short_colon_07.txt")
lines = [f"count={len(mod.BODIES)}"]
for i, body in enumerate(mod.BODIES, 1):
    match = re.match(r"^([^：:]{1,12})[：:]", body)
    if match and not match.group(1).endswith(suffixes):
        lines.append(f"{i}\t{match.group(1)}\t{body}")
out.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("wrote", out)
