# -*- coding: utf-8 -*-
"""Scan batch77 bodies for common simplified Chinese chars."""
from pathlib import Path

# common simplified chars that should be traditional
SIMP = set("过敏发现检查医疗治疗药物症状营养风险习惯简单复杂过量焦虑牵动烟雾热量贫血果酱闹钟脑优园换")

bodies = Path(__file__).with_name("_batch77_bodies")
for path in sorted(bodies.glob("*.txt")):
    hits = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        bad = [c for c in line if c in SIMP]
        # also flag ASCII words longer than 2
        import re
        en = re.findall(r"[A-Za-z]{3,}", line)
        if bad or en:
            hits.append((i, "".join(bad), en, line[:40]))
    print(path.name, "hits", len(hits))
    for h in hits[:20]:
        print(" ", h)
