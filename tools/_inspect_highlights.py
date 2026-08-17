# -*- coding: utf-8 -*-
import ast
import re
from collections import Counter
from pathlib import Path

src = Path(__file__).with_name("_gen_highlights_tmp.py").read_text(encoding="utf-8")
mod = ast.parse(src)
book1 = book2 = None
for node in mod.body:
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == "BOOK1":
                book1 = ast.literal_eval(node.value)
            if isinstance(target, ast.Name) and target.id == "BOOK2":
                book2 = ast.literal_eval(node.value)

print("b1", len(book1), "b2", len(book2))
print("BOOK1 150", book1[149][:80])
print("BOOK1 151", book1[150][:80] if len(book1) > 150 else "na")
print("BOOK2 150", book2[149][:80])
print("BOOK2 151", book2[150][:80] if len(book2) > 150 else "na")

NATURAL = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
for name, bodies in (("1", book1), ("2", book2)):
    print("short colon", name)
    for i, body in enumerate(bodies, 1):
        match = re.match(r"^([^：:]{1,12})[：:]", body)
        if match and not match.group(1).endswith(NATURAL):
            print(i, body[:80])
    print("forbidden", name)
    for i, body in enumerate(bodies, 1):
        for prefix in ("本書", "作者指出", "本章", "這一章", "｜"):
            if prefix in body:
                print(i, prefix, body[:40])
        if len(body) < 12:
            print(i, "short", body)
    print("18-char", name, Counter(b[:18] for b in bodies if len(b) >= 18).most_common(3))
    print("dups", name, len(bodies) - len(set(bodies)))
    print("8-char >=3", name, [(k, v) for k, v in Counter(b[:8] for b in bodies).items() if v >= 3])
