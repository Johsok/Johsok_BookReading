# -*- coding: utf-8 -*-
import json
import re
from pathlib import Path

root = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\Books\06_computer_info")
files = [
    "06_computer_info-20260717-03.json",
    "06_computer_info-20260717-04.json",
    "06_computer_info-20260717-05.json",
    "06_computer_info-20260717-06.json",
]
BANNED = ("本書", "作者指出", "本章", "這一章", "｜")
for fn in files:
    d = json.loads((root / fn).read_text(encoding="utf-8-sig"))
    hl = d["chatgptHighlights"]
    issues = []
    if len(hl) != 150:
        issues.append(f"count={len(hl)}")
    if not hl[0].startswith("001、"):
        issues.append("bad001")
    if not hl[-1].startswith("150、"):
        issues.append("bad150")
    if d.get("chatgptStatus") != "complete":
        issues.append("status")
    if d.get("highlightsSource") != "grok":
        issues.append("source")
    if d.get("updatedAt") != "2026-08-18":
        issues.append("updatedAt")
    if not d.get("highlightsCapturedAt"):
        issues.append("captured")
    for i, t in enumerate(hl, 1):
        for b in BANNED:
            if b in t:
                issues.append(f"banned@{i}")
        if re.search(r"[：:]", t):
            issues.append(f"colon@{i}")
        if not t.startswith(f"{i:03d}、"):
            issues.append(f"num@{i}")
    ok = not issues
    print(f"{fn}\tcount={len(hl)}\tok={ok}\t{d['title']}")
    print(f"  meta status={d['chatgptStatus']} source={d['highlightsSource']} updatedAt={d['updatedAt']}")
    print(f"  issues={issues or ['pass']}")
