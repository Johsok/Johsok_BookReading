# -*- coding: utf-8 -*-
import importlib.util
import re
from collections import Counter
from pathlib import Path

p = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\_tmp\hl_36_40.py")
spec = importlib.util.spec_from_file_location("hl", p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
CJK = re.compile(r"[\u4e00-\u9fff]")
BANNED = ("本書", "作者指出", "本章", "這一章")
authors = {
    "BOOK36": "Sachi",
    "BOOK37": "李彼飛",
    "BOOK38": "江口和明",
    "BOOK39": "開平青年發展基金會",
    "BOOK40": "青井聡子",
}
print("exists", p.exists())
ok = True
for name in ("BOOK36", "BOOK37", "BOOK38", "BOOK39", "BOOK40"):
    items = getattr(mod, name)
    errs = []
    if len(items) != 150:
        errs.append(f"count {len(items)}")
    if len(set(items)) != 150:
        errs.append("dup")
    p18 = Counter(s[:18] for s in items)
    if p18.most_common(1)[0][1] >= 4:
        errs.append(f"p18 {p18.most_common(1)}")
    p8 = Counter("".join(CJK.findall(s)[:8]) for s in items)
    if p8.most_common(1)[0][1] >= 4:
        errs.append(f"p8 {p8.most_common(1)}")
    ac = sum(authors[name] in s for s in items)
    if ac > 1:
        errs.append(f"author {ac}")
    for i, s in enumerate(items, 1):
        if s.startswith(("001", "1、")) or s[:3].isdigit():
            errs.append(f"numbered {i}")
            break
        if not s.endswith("。") or len(s) < 12:
            errs.append(f"fmt {i}")
        if any(ch in s for ch in "\n\r｜|：:"):
            errs.append(f"char {i}")
        if any(b in s for b in BANNED):
            errs.append(f"ban {i} {s}")
    print(name, len(items), "minmax", min(map(len, items)), max(map(len, items)), "author", ac, "errs", errs or "none")
    if errs:
        ok = False
print("PASS" if ok else "FAIL")
