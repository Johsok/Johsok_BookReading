# -*- coding: utf-8 -*-
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from findbook_writer import NATURAL_COLON_SUFFIXES  # noqa: E402

p = Path(__file__).resolve().parent / "write_07_31_33_highlights.py"
text = p.read_text(encoding="utf-8")
out_lines = []
changed = 0
for line in text.splitlines(True):
    m = re.match(r'^(\s*")(.*)(",?\s*)$', line)
    if not m:
        out_lines.append(line)
        continue
    body = m.group(2)
    match = re.match(r"^([^：:]{1,12})[：:](.*)$", body)
    if match and not match.group(1).endswith(NATURAL_COLON_SUFFIXES):
        body = match.group(1) + "；" + match.group(2)
        changed += 1
        line = m.group(1) + body + m.group(3)
    out_lines.append(line)
p.write_text("".join(out_lines), encoding="utf-8")
print("changed", changed)
