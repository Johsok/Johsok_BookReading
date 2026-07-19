# -*- coding: utf-8 -*-
import importlib.util
import re
from pathlib import Path

path = Path("tools/_gen_chunk02_highlights.py")
spec = importlib.util.spec_from_file_location("g", path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
NATURAL = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
COLON_RE = re.compile(r"^([^：:]{1,12})[：:](.*)$")
out = []
for name in ("BOOK69", "BOOK70"):
    out.append(f"## {name}")
    for i, body in enumerate(getattr(mod, name), 1):
        match = COLON_RE.match(body)
        if match and not match.group(1).endswith(NATURAL):
            out.append(f"{i}|{body}")
Path("tools/_colon_dump.txt").write_text("\n".join(out), encoding="utf-8")
print("wrote", len(out))
