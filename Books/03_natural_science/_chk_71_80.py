# -*- coding: utf-8 -*-
import json
from collections import Counter
from pathlib import Path

root = Path(__file__).resolve().parent
out = []
bads = ["本書", "作者指出", "本章", "這一章", "實作面", "決策面", "從《"]
for n in range(71, 81):
    p = root / f"03_natural_science-20260716-{n:02d}.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    h = d["chatgptHighlights"]
    nums = [x[:4] for x in h]
    bodies = [x.split("、", 1)[1] if "、" in x else x for x in h]
    lens = [len(b) for b in bodies]
    starts = [b[:4] for b in bodies]
    dup_start = [(k, v) for k, v in Counter(starts).most_common(5) if v >= 8]
    exact = [k for k, v in Counter(bodies).items() if v > 1]
    fb = [b for b in bodies if any(x in b for x in bads)]
    line = (
        f"{n:02d} n={len(h)} src={d.get('highlightsSource')} st={d.get('chatgptStatus')} "
        f"first={nums[0]} last={nums[-1]} len={min(lens)}-{max(lens)} "
        f"mean={sum(lens)/len(lens):.0f} exact_dup={len(exact)} bad={len(fb)} start={dup_start[:3]}"
    )
    out.append(line)
    out.append("  " + bodies[0])
    out.append("  " + bodies[74])
    out.append("  " + bodies[-1])
    out.append("  summary: " + d.get("summary", ""))
(root / "_chk71_80.txt").write_text("\n".join(out), encoding="utf-8")
print("wrote _chk71_80.txt")
