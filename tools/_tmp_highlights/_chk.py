# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

d = Path(__file__).resolve().parent
simp = set("这们为发从对会开关学经点线国种还现时样体机进应条产长门东车头么无与问说个后启战报历愿爱乐处办让该连达过")
out: list[str] = []
for name in (
    "03_natural_science-20260710-09.json",
    "03_natural_science-20260710-10.json",
    "03_natural_science-20260710-11.json",
):
    data = json.loads((d / name).read_text(encoding="utf-8"))
    hs = data["highlights"]
    out.append(f"{data['id']} n={len(hs)} keys={list(data)}")
    bodies = [re.sub(r"^\d{3}、", "", h) for h in hs]
    out.append("  minlen=" + str(min(len(b) for b in bodies)))
    out.append("  dups=" + str(len(bodies) - len(set(bodies))))
    out.append("  本書=" + str(sum("本書" in b for b in bodies)))
    out.append(
        "  費曼="
        + str(sum(b.count("費曼") for b in bodies))
        + " start="
        + str(sum(b.startswith("費曼") for b in bodies))
    )
    out.append("  十大關鍵=" + str(sum("十大關鍵" in b for b in bodies)))
    joined = "".join(bodies)
    out.append(
        "  Challenger="
        + str(any(x in joined for x in ("挑戰者", "O環", "橡皮環", "固態火箭")))
    )
    bad = []
    for i, b in enumerate(bodies, 1):
        hit = sorted(set(b) & simp)
        if hit:
            bad.append((i, "".join(hit), b[:50]))
    out.append("  simp=" + str(bad[:20]))
    starts = Counter(b[:18] for b in bodies)
    out.append("  maxstart=" + str(starts.most_common(3)))
    ok = all(h.startswith(f"{i:03d}、") for i, h in enumerate(hs, 1))
    out.append("  numbering=" + str(ok))
    out.append("  newline=" + str(any("\n" in h or "｜" in h for h in hs)))
(d / "_chk.txt").write_text("\n".join(out), encoding="utf-8")
print("ok")
