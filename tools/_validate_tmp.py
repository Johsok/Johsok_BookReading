# -*- coding: utf-8 -*-
import re
from collections import Counter
from pathlib import Path

text = Path(__file__).with_name("_gen_highlights_131_134.py").read_text(encoding="utf-8")
NATURAL = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
for name in ["BOOK132", "BOOK133", "BOOK134"]:
    m = re.search(
        rf'{name} = """(.*?)"""\.strip\(\)\.splitlines\(\)',
        text,
        re.S,
    )
    lines = [ln.strip() for ln in m.group(1).strip().splitlines() if ln.strip()]
    print(name, len(lines), "unique", len(set(lines)))
    bad = []
    for i, body in enumerate(lines, 1):
        if "｜" in body or "本書" in body or "作者指出" in body:
            bad.append((i, "forbidden", body[:40]))
        mm = re.match(r"^([^：:]{1,12})[：:]", body)
        if mm and not mm.group(1).endswith(NATURAL):
            bad.append((i, "colon", body[:60]))
        if re.search(r".{1,8}面第\d+步[，,]", body) or re.match(r"^第\d+步[，,]", body):
            bad.append((i, "step", body[:40]))
        if len(body) < 12:
            bad.append((i, "short", body))
        if re.search(r"[A-Za-z]{3,}", body):
            bad.append((i, "english", body[:60]))
    starts = Counter(h[:18] for h in lines)
    print(" maxstart", starts.most_common(1)[0])
    print(" bad", len(bad))
    for b in bad:
        print(b)
