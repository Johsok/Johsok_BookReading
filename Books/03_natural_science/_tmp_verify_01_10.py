# -*- coding: utf-8 -*-
import json
from collections import Counter
from pathlib import Path

base = Path(__file__).resolve().parent
old_frag = "先釐清問題與目標"
for i in range(1, 11):
    p = base / f"03_natural_science-20260713-{i:02d}.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    hl = d.get("chatgptHighlights") or []
    nums = [x[:4] for x in hl]
    expect = [f"{n:03d}、" for n in range(1, 151)]
    dup = len(hl) - len(set(hl))
    starts = [(x.split("、", 1)[1][:8] if "、" in x else x[:8]) for x in hl]
    top = Counter(starts).most_common(1)[0]
    ok = (
        len(hl) == 150
        and nums == expect
        and old_frag not in "".join(hl)
        and d.get("chatgptStatus") == "complete"
        and d.get("highlightsSource") == "grok"
    )
    print(
        f"{p.name}\tok={ok}\tn={len(hl)}\tdup={dup}"
        f"\tsrc={d.get('highlightsSource')}\tupdated={d.get('updatedAt')}"
        f"\ttopstart={top}\t001={hl[0][:36]}"
    )
