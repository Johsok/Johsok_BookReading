# -*- coding: utf-8 -*-
import json
import re
from collections import defaultdict
from pathlib import Path

root = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\Books\07_other")
out = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\_tmp\_chk_41_50.txt")
ids = [f"07_other-20260717-{i:02d}" for i in range(41, 51)]
banned = ("本書", "作者指出", "本章", "這一章", "｜")
old = "理解作品需先辨認作者所處的時代"
errors = []
lines = []
for i in ids:
    p = root / f"{i}.json"
    raw = p.read_bytes()
    has_bom = raw.startswith(b"\xef\xbb\xbf")
    d = json.loads(raw.decode("utf-8-sig"))
    hl = d.get("chatgptHighlights", [])
    lines.append(
        f"=== {d['id']} n={len(hl)} status={d.get('chatgptStatus')} "
        f"src={d.get('highlightsSource')} upd={d.get('updatedAt')}"
    )
    lines.append(f"  first: {hl[0]}")
    lines.append(f"  last: {hl[-1]}")
    if len(hl) != 150:
        errors.append(f"{i} count {len(hl)}")
    bodies = []
    groups = defaultdict(list)
    colon = 0
    for n, line in enumerate(hl, 1):
        m = re.match(r"^(\d{3})、(.*)$", line)
        if not m or int(m.group(1)) != n:
            errors.append(f"{i} num {n}")
            continue
        b = m.group(2)
        bodies.append(b)
        if old in b:
            errors.append(f"{i} OLD_TEMPLATE {n}")
        for bad in banned:
            if bad in b:
                errors.append(f"{i} BAN {n} {bad}")
        if re.search(r"第.章", b) or "這一章" in b or "本章" in b:
            errors.append(f"{i} CHAPTER {n}: {b}")
        c = len(re.findall(r"[：:]", b))
        colon += c
        if c > 2:
            errors.append(f"{i} colons_line {n}={c}")
        groups[b[:18]].append(n)
        if len(b) < 20:
            errors.append(f"{i} short {n} {len(b)} {b}")
        if len(b) > 90:
            errors.append(f"{i} long {n} {len(b)} {b}")
    if len(bodies) != len(set(bodies)):
        errors.append(f"{i} dup bodies")
    if colon > 2:
        errors.append(f"{i} colon_total={colon}")
    for pref, ns in groups.items():
        if len(ns) >= 4:
            errors.append(f"{i} prefix18 x{len(ns)} {pref} {ns}")
    author = d["author"].split("、")[0]
    hits_a = sum(1 for b in bodies if author[:3] in b)
    lines.append(
        f"  bom={has_bom} author3_hits={hits_a} colons={colon} unique={len(set(bodies))}"
    )
lines.append("ERRORS " + str(len(errors)))
lines.extend(errors[:120])
out.write_text("\n".join(lines), encoding="utf-8")
print("wrote", out)
print("errors", len(errors))
