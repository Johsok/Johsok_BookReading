# -*- coding: utf-8 -*-
"""Extract usable highlight strings from incomplete _gen_batch77.py."""
from __future__ import annotations

import ast
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
text = (ROOT / "_gen_batch77.py").read_text(encoding="utf-8")


def extract(name: str) -> list[str]:
    m = re.search(rf"{name}\s*=\s*\[", text)
    if not m:
        return []
    start = m.end() - 1
    depth = 0
    i = start
    while i < len(text):
        if text[i] == "[":
            depth += 1
        elif text[i] == "]":
            depth -= 1
            if depth == 0:
                i += 1
                break
        i += 1
    block = text[start:i]
    # Fix broken trailing junk for BOOK38
    block = re.sub(r',\s*"\s*thrush".*', "\n]", block, flags=re.S)
    try:
        strings = ast.literal_eval(block)
    except Exception as e:
        print(name, "literal_eval failed", e)
        strings = re.findall(r'"([^"]{12,})"', block)
    out = []
    seen = set()
    for s in strings:
        s = str(s).strip()
        if len(s) < 12:
            continue
        if "thrush" in s.lower():
            continue
        if any(x in s for x in ("本書", "作者指出", "本章", "這一章", "｜")):
            continue
        if s not in seen:
            seen.add(s)
            out.append(s)
    return out


for name in ["BOOK36", "BOOK37", "BOOK38"]:
    lines = extract(name)
    print(name, len(lines))
    (ROOT / f"_extract_{name}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
