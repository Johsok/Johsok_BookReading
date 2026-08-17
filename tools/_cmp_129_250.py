# -*- coding: utf-8 -*-
"""Compare 250 draft bodies against book 129 highlights."""
from __future__ import annotations

import ast
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
src = (ROOT / "tools" / "_gen_pg_250.py").read_text(encoding="utf-8")
mod = ast.parse(src)
bodies250 = None
for node in mod.body:
    if isinstance(node, ast.Assign):
        for t in node.targets:
            if isinstance(t, ast.Name) and t.id == "BOOK":
                book = ast.literal_eval(node.value)
                bodies250 = book["points"]
p129 = json.loads(
    (ROOT / "Books" / "02_psychology_growth" / "02_psychology_growth-20260716-129.json").read_text(
        encoding="utf-8-sig"
    )
)
bodies129 = [re.sub(r"^\d{3}、", "", x) for x in p129["chatgptHighlights"]]
print("250", len(bodies250))
print("exact", sum(b in set(bodies129) for b in bodies250))
p18 = set(b[:18] for b in bodies129)
hits = [b for b in bodies250 if b[:18] in p18]
print("prefix18", len(hits))
for b in hits:
    print(" ", b)


def toks(s: str) -> set[str]:
    return set(re.findall(r"[\u4e00-\u9fff]{2,}", s))


near = []
for b in bodies250:
    tb = toks(b)
    for a in bodies129:
        ta = toks(a)
        inter = tb & ta
        if len(inter) >= 7:
            near.append((len(inter), b, a))
near.sort(reverse=True)
print("near>=7", len(near))
for n, b, a in near[:20]:
    print("---", n)
    print("250", b)
    print("129", a)
