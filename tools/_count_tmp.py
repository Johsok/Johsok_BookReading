# -*- coding: utf-8 -*-
from pathlib import Path
import re

NATURAL = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
text = Path(__file__).with_name("_gen_highlights_96_100.py").read_text(encoding="utf-8")
parts = text.split("pack(")
lines = []
for part in parts[1:]:
    match = re.search(r'"(02_[^"]+)"', part)
    if not match:
        continue
    bid = match.group(1)
    bodies = re.findall(r'^\s{8}"([^"]+)",?\s*$', part, re.M)
    lines.append(f"{bid} count {len(bodies)}")
    for i, body in enumerate(bodies, 1):
        m = re.match(r"^([^：:]{1,12})[：:]", body)
        if m and not m.group(1).endswith(NATURAL):
            lines.append(f"  colon {i}: {m.group(1)} || {body}")
        if re.search(r"[A-Za-z]{3,}", body):
            lines.append(f"  en {i}: {body}")
        if len(body) < 12:
            lines.append(f"  short {i}: {body}")
out = Path(__file__).with_name("_count_tmp_out.txt")
out.write_text("\n".join(lines), encoding="utf-8")
print("wrote", out, "lines", len(lines))
