# -*- coding: utf-8 -*-
from importlib.machinery import SourceFileLoader
from collections import Counter
import re

m = SourceFileLoader(
    "hl",
    r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\_tmp\hl_b08_b09_b10.py",
).load_module()


def cjk(s):
    return "".join(ch for ch in s if "\u4e00" <= ch <= "\u9fff")


out = []
for k, xs in m.BOOKS.items():
    out.append(f"=== {k} n={len(xs)} unique={len(set(xs))} ===")
    p18 = Counter(s[:18] for s in xs)
    d18 = [a for a, c in p18.items() if c > 1]
    p8 = Counter(cjk(s)[:8] for s in xs)
    bad8 = [(a, c) for a, c in p8.items() if c >= 4]
    out.append(f"len {min(map(len, xs))}-{max(map(len, xs))} dup18={d18} bad8={bad8}")
    for i, s in enumerate(xs, 1):
        flags = []
        if not (28 <= len(s) <= 55):
            flags.append(f"LEN{len(s)}")
        if re.search(r"[A-Za-z0-9]", s):
            flags.append("ALNUM")
        for w in ["本書", "作者指出", "本章", "這一章", "：", ":", "｜", "|", "該書", "楊淑媚", "蔡昆道", "陳允斌", "Hotema", "赫特瑪", "希爾頓", "食療大全", "養生先養胃", "人本食氣"]:
            if w in s:
                flags.append(w)
        if flags:
            out.append(f"{i:03d} {' '.join(flags)} {s}")

path = r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\_tmp\_hl_b08chk.txt"
open(path, "w", encoding="utf-8").write("\n".join(out))
print("\n".join(out[:20]))
print("total_lines", len(out))
