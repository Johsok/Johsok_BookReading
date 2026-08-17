# -*- coding: utf-8 -*-
from pathlib import Path
import json
import zhconv

d = json.loads(Path("tools/_hl_07.json").read_text(encoding="utf-8"))
hl = d["highlights"]
out = []
for i, line in enumerate(hl, 1):
    body = line.split("、", 1)[1]
    trad = zhconv.convert(body, "zh-hant")
    if trad != body:
        diffs = [f"{a}->{b}" for a, b in zip(body, trad) if a != b]
        out.append(f"{i:03d} " + " | ".join(diffs))
        out.append("  SRC " + body)
        out.append("  HANT " + trad)
Path("tools/_hl_07_zhconv.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
print(f"diffs={len(out) // 3}")
