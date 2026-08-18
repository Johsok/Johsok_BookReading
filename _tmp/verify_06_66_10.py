# -*- coding: utf-8 -*-
import json
import pathlib
import re
from collections import Counter

files = [
    "06_computer_info-20260716-66.json",
    "06_computer_info-20260716-67.json",
    "06_computer_info-20260716-68.json",
    "06_computer_info-20260716-69.json",
    "06_computer_info-20260716-70.json",
    "06_computer_info-20260716-71.json",
    "06_computer_info-20260717-01.json",
    "06_computer_info-20260717-02.json",
    "06_computer_info-20260717-03.json",
    "06_computer_info-20260717-04.json",
    "06_computer_info-20260717-05.json",
    "06_computer_info-20260717-06.json",
    "06_computer_info-20260717-07.json",
    "06_computer_info-20260717-08.json",
    "06_computer_info-20260717-09.json",
    "06_computer_info-20260717-10.json",
]
base = pathlib.Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\Books\06_computer_info")
bad_phrases = [
    "先定義使用情境與成功指標",
    "需求應轉成可驗收行為",
    "閱讀時可先確認作者如何定義問題",
    "可把觀點轉成一個具體案例",
    "整理筆記時宜區分核心主張",
]
out_lines = []
for f in files:
    d = json.loads((base / f).read_text(encoding="utf-8-sig"))
    hl = d.get("chatgptHighlights", [])
    issues = []
    if len(hl) != 150:
        issues.append(f"count={len(hl)}")
    if hl:
        if not hl[0].startswith("001、"):
            issues.append("bad_first")
        if not hl[-1].startswith("150、"):
            issues.append("bad_last")
    for i, line in enumerate(hl, 1):
        expect = f"{i:03d}、"
        if not line.startswith(expect):
            issues.append(f"num@{i}")
            break
        for bp in bad_phrases:
            if bp in line:
                issues.append(f"template:{bp[:8]}")
                break
        for ban in ("本書", "作者指出", "本章", "這一章", "｜"):
            if ban in line:
                issues.append(f"ban:{ban}")
                break
    # prefix collision
    bodies = [re.sub(r"^\d{3}、", "", x) for x in hl]
    prefixes = Counter(b[:18] for b in bodies)
    heavy = [(p, c) for p, c in prefixes.items() if c >= 5]
    if heavy:
        issues.append(f"prefix18x{heavy[0][1]}:{heavy[0][0][:12]}")
    status = d.get("chatgptStatus")
    src = d.get("highlightsSource")
    sample = bodies[0][:40] if bodies else ""
    out_lines.append({
        "file": f,
        "n": len(hl),
        "status": status,
        "src": src,
        "issues": issues or ["ok"],
        "sample": sample,
    })

path = pathlib.Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\_tmp\verify_06_66_10.json")
path.write_text(json.dumps(out_lines, ensure_ascii=False, indent=2), encoding="utf-8")
print("wrote", path)
fail = [x for x in out_lines if x["issues"] != ["ok"]]
print("FAIL", len(fail), "OK", len(out_lines) - len(fail))
