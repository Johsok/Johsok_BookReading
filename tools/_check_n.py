# -*- coding: utf-8 -*-
import ast, re
from pathlib import Path

def check(path):
    bodies = ast.literal_eval(Path(path).read_text(encoding="utf-8").split("BODIES = ", 1)[1])
    NATURAL = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
    issues = []
    if len(bodies) != 150:
        issues.append(f"count={len(bodies)}")
    starts = {}
    for i, b in enumerate(bodies, 1):
        if "本書" in b or "作者指出" in b or "本章" in b or "這一章" in b:
            issues.append(f"{i} forbidden {b[:20]}")
        if "｜" in b or "*" in b or "`" in b or "#" in b:
            issues.append(f"{i} markdown/pipe")
        if len(b) < 12:
            issues.append(f"{i} short")
        match = re.match(r"^([^：:]{1,12})[：:]", b)
        if match and not match.group(1).endswith(NATURAL):
            issues.append(f"{i} colon {match.group(1)}")
        key = b[:18]
        starts.setdefault(key, []).append(i)
    for k, idxs in starts.items():
        if len(idxs) >= 4:
            issues.append(f"start x{len(idxs)} {k} {idxs}")
    if len(set(bodies)) != len(bodies):
        issues.append("exact dup")
    return issues

out = Path("tools/_check_out.txt")
lines = []
for p in ["tools/_hl_185.py", "tools/_hl_186.py", "tools/_hl_187.py"]:
    lines.append(p)
    lines.extend(check(p) or ["ok"])
out.write_text("\n".join(lines), encoding="utf-8")
