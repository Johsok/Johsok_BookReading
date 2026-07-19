# -*- coding: utf-8 -*-
import re
from pathlib import Path

path = Path(__file__).with_name("_gen_chunk15_highlights.py")
text = path.read_text(encoding="utf-8")
ns = {"__file__": str(path), "__name__": "x", "annotations": __import__("__future__").annotations}
exec(compile(text.split("def main")[0], str(path), "exec"), ns)
for name in ["BOOK_131", "BOOK_132", "BOOK_133", "BOOK_134", "BOOK_135"]:
    items = ns[name]
    print("===", name, len(items))
    for i, s in enumerate(items, 1):
        flags = []
        if len(s) < 12:
            flags.append("short")
        if "|" in s or "｜" in s:
            flags.append("bar")
        if any(p in s for p in ("本書", "作者指出", "本章", "這一章")):
            flags.append("forbid")
        if re.search(r"[A-Za-z]{4,}", s):
            flags.append("en:" + ",".join(re.findall(r"[A-Za-z]{4,}", s)))
        if "\ufffd" in s:
            flags.append("badchar")
        if "实话" in s:
            flags.append("simp")
        if flags:
            print(i, flags, s)
