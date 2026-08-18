# -*- coding: utf-8 -*-
import ast
import collections
import re
from pathlib import Path

src = Path(__file__).with_name("_gen_book41_42.py").read_text(encoding="utf-8")
tree = ast.parse(src)
lists = {}
for node in tree.body:
    if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
        if node.targets[0].id in ("BOOK41", "BOOK42"):
            lists[node.targets[0].id] = ast.literal_eval(node.value)

cjk = re.compile(r"[\u4e00-\u9fff]")
forb = ["本書", "作者指出", "本章", "這一章", "｜", "：", ":"]
step = re.compile(r"第\d+步|.面第\d+步")

def check(name, arr):
    print("===", name, "len", len(arr), "unique", len(set(arr)))
    p8 = collections.Counter()
    p18 = collections.Counter()
    issues = []
    for i, s in enumerate(arr, 1):
        chars = cjk.findall(s)
        n = len(chars)
        if n < 12:
            issues.append((i, "short", n, s))
        p8["".join(chars[:8])] += 1
        p18[s[:18]] += 1
        for f in forb:
            if f in s:
                issues.append((i, "forb", f, s[:50]))
        if step.search(s):
            issues.append((i, "step", s[:40]))
        if re.match(r"^\d+[、.]", s):
            issues.append((i, "num", s[:20]))
        if not chars:
            issues.append((i, "en", s))
    print("p8>=4", [(k, v) for k, v in p8.items() if v >= 4])
    print("p18>=4", [(k, v) for k, v in p18.items() if v >= 4])
    print("p8==3", [(k, v) for k, v in p8.items() if v == 3])
    dups = [x for x in collections.Counter(arr).items() if x[1] > 1]
    print("dup", dups)
    print("issues", issues)

check("BOOK41", lists["BOOK41"])
check("BOOK42", lists["BOOK42"])
