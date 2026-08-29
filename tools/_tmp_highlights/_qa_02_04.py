# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from findbook_writer import validate_highlights

p = Path(__file__).with_name("02_psychology_growth-20260830-04.json")
d = json.loads(p.read_text(encoding="utf-8"))
hs = d["highlights"]
lines = [f"id={d['id']}", f"n={len(hs)}", f"keys={list(d)}"]
bodies = []
issues = []
for i, h in enumerate(hs, 1):
    if not h.startswith(f"{i:03d}、"):
        issues.append(f"num {i}")
    if "\n" in h or "\r" in h or "｜" in h:
        issues.append(f"fmt {i}")
    body = h.split("、", 1)[1]
    bodies.append(body)
    if not (45 <= len(body) <= 95):
        issues.append(f"LEN {i} {len(body)}")
lens = [len(b) for b in bodies]
lines.append(f"min={min(lens)} max={max(lens)}")
lines.append(f"dups={len(bodies) - len(set(bodies))}")
lines.append("max18=" + str(Counter(b[:18] for b in bodies).most_common(3)))
lines.append(
    "start8ge3="
    + str([(k, v) for k, v in Counter(b[:8] for b in bodies).items() if v >= 3])
)
simp = set("这们为发从对会开关学经点线国种还现时样体机进应条产长门东车头么无与问说个后启战报历愿爱乐处办让该连达过")
simp_hits = []
for i, b in enumerate(bodies, 1):
    hit = sorted(set(b) & simp)
    if hit:
        simp_hits.append((i, "".join(hit)))
lines.append("simp=" + str(simp_hits))
for i, b in enumerate(bodies, 1):
    for bad in (
        "本書",
        "作者指出",
        "本章",
        "這一章",
        "查爾斯",
        "哈尼爾",
        "世界上最神奇",
        "Master Key",
        "當你",
    ):
        if bad in b:
            issues.append(f"{i} {bad}")
lines.append(
    "dangni_start=" + str([i for i, b in enumerate(bodies, 1) if b.startswith("當你")])
)
natural = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
colon = []
for i, b in enumerate(bodies, 1):
    match = re.match(r"^([^：:]{1,12})[：:]", b)
    if match and not match.group(1).endswith(natural):
        colon.append(i)
lines.append("colon=" + str(colon))
lines.append("issues=" + str(issues))
validate_highlights(
    d["id"],
    hs,
    "世界上最神奇的24堂課【經典新譯版】（The Master Key System）",
    "查爾斯．哈尼爾",
)
lines.append("findbook=OK")
lines.append("FIRST=" + hs[0])
lines.append("LAST=" + hs[-1])
Path(__file__).with_name("_qa04.txt").write_text("\n".join(lines), encoding="utf-8")
print("ok")
