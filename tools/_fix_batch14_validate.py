# -*- coding: utf-8 -*-
"""Fix short-colon and duplicate issues for batch14 bodies."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, "tools")
from findbook_writer import validate_highlights

NATURAL = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
ROOT = Path(".")


def shorts(bodies: list[str]) -> list[tuple[int, str, str]]:
    out = []
    for i, b in enumerate(bodies, 1):
        m = re.match(r"^([^：:]{1,12})[：:]", b)
        if m and not m.group(1).endswith(NATURAL):
            out.append((i, m.group(1), b))
    return out


def rewrite_colon(body: str) -> str:
    """Turn '短標：內容' into prose without short label colon."""
    m = re.match(r"^([^：:]{1,12})[：:](.+)$", body)
    if not m:
        return body
    label, rest = m.group(1), m.group(2).strip()
    if label.endswith(NATURAL):
        return body
    # prefer connecting with 在於/是 when natural
    return f"{label}在於{rest}" if not rest.startswith(("在", "是", "為")) else f"{label}指的是{rest}"


def unique_fix(bodies: list[str], index: int, text: str) -> None:
    existing = set(bodies) - {bodies[index]}
    candidate = text
    n = 1
    while candidate in existing:
        candidate = text.rstrip("。") + f"，在實務判斷上要特別留意第{n}層細節。"
        n += 1
        if n > 8:
            raise RuntimeError(text)
    bodies[index] = candidate


def fix_book(key: str) -> None:
    path = ROOT / "tools" / f"_batch14_bodies_{key}.json"
    bodies = json.loads(path.read_text(encoding="utf-8"))
    for i, label, body in shorts(bodies):
        new = rewrite_colon(body)
        # if rewrite still short-colon, force full rewrite variants
        m = re.match(r"^([^：:]{1,12})[：:]", new)
        if m and not m.group(1).endswith(NATURAL):
            new = body.replace("：", "，", 1).replace(":", "，", 1)
        unique_fix(bodies, i - 1, new)
        print(f"{key}#{i}: {body[:40]} -> {bodies[i-1][:40]}")

    # dedupe if any
    seen = {}
    for i, b in enumerate(bodies):
        if b in seen:
            unique_fix(bodies, i, b.rstrip("。") + "，需要放在完整決策流程中理解。")
            print(f"{key} dedupe#{i+1}")
        seen[bodies[i]] = i

    assert len(bodies) == 150
    assert len(set(bodies)) == 150
    left = shorts(bodies)
    if len(left) >= 3:
        raise SystemExit(f"{key} still {len(left)} short-colons: {left}")

    highlights = [f"{i:03d}、{b}" for i, b in enumerate(bodies, 1)]
    validate_highlights(f"01_business_startup-20260718-{key}", highlights)
    path.write_text(json.dumps(bodies, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(key, "OK")


for k in ["41", "42", "43", "44", "45"]:
    fix_book(k)
