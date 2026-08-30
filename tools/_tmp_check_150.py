# -*- coding: utf-8 -*-
import re
from pathlib import Path
from collections import defaultdict

p = Path(__file__).with_name("_tmp_dollar_trap_150.txt")
lines = [ln.rstrip("\n") for ln in p.read_text(encoding="utf-8").splitlines() if ln.strip()]
print("count", len(lines))
cjk_re = re.compile(r"[\u4e00-\u9fff]")
bans = ["本書", "作者指出", "本章", "這一章", "王伯達", "美元圈套：", "如何創富與避險", "｜"]
simp_only = set("发国经济见现产会后时对与这为过还东车门长马风干广儿头进吗历换")
issues = []
starts4 = defaultdict(list)
starts2 = defaultdict(list)
for i, ln in enumerate(lines, 1):
    m = re.match(r"^(\d{3})、(.*)$", ln)
    if not m:
        issues.append(f"fmt {i}")
        continue
    if int(m.group(1)) != i:
        issues.append(f"num {i}")
    body = m.group(2)
    n = len(cjk_re.findall(body))
    if n < 20:
        issues.append(f"short {i} {n}")
    for b in bans:
        if b in ln:
            issues.append(f"ban {i} {b}")
    if "|" in ln or "｜" in ln:
        issues.append(f"pipe {i}")
    found = [ch for ch in body if ch in simp_only]
    if found:
        issues.append(f"simp {i} {found} {body[:40]}")
    starts4["".join(cjk_re.findall(body)[:4])].append(i)
    starts2["".join(cjk_re.findall(body)[:2])].append(i)
out = Path(__file__).with_name("_tmp_check_150_out.txt")
chunks = [f"count {len(lines)}", f"issues {len(issues)}"]
chunks.extend(issues)
chunks.append("dup4")
for s, idxs in starts4.items():
    if len(idxs) > 1:
        chunks.append(f"{s} {idxs}")
chunks.append("freq2")
for s, idxs in sorted(starts2.items(), key=lambda kv: -len(kv[1])):
    if len(idxs) > 1:
        chunks.append(f"{s} {len(idxs)} {idxs}")
out.write_text("\n".join(chunks), encoding="utf-8")
