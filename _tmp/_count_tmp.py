# -*- coding: utf-8 -*-
from pathlib import Path

def load(name):
    p = Path(name)
    return [ln.strip() for ln in p.read_text(encoding="utf-8").splitlines() if ln.strip()]

for n in ["_b37.txt", "_b38.txt", "_b39.txt", "_b40.txt"]:
    lines = load(n)
    print(n, len(lines), "unique", len(set(lines)))
    bad = [i for i,x in enumerate(lines,1) if ":" in x or "：" in x or "｜" in x or "|" in x or "本書" in x or "作者指出" in x or "本章" in x or "這一章" in x or "WAIT" in x or "FIX" in x]
    print("  flags", bad[:10], "short", sum(1 for x in lines if len(x)<28), "minmax", min(map(len,lines)), max(map(len,lines)))
    print("  last", lines[-1])
