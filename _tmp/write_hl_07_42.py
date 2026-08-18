# -*- coding: utf-8 -*-
"""Overwrite chatgptHighlights for 07_other-20260717-42."""
from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading")
SRC = ROOT / r"Books\07_other\07_other-20260717-42.json"
BODIES_PATH = ROOT / r"_tmp\hl_07_42_bodies.txt"
BANNED = ("本書", "作者指出", "本章", "這一章", "｜", "《")
TITLE_BITS = ("東亞關聯史", "柳鏞泰", "朴晉雨", "朴泰均")
COLON_RE = re.compile(r"[：:]")
STAMP = "2026-08-18T09:10:00+08:00"
DATE = "2026-08-18"


def validate(bodies: list[str]) -> None:
    errors: list[str] = []
    if len(bodies) != 150:
        errors.append(f"count={len(bodies)}")
    if len(bodies) != len(set(bodies)):
        errors.append("dup_body")
    groups: dict[str, list[int]] = defaultdict(list)
    colon_hits = 0
    for i, b in enumerate(bodies, 1):
        if not (32 <= len(b) <= 68):
            errors.append(f"len_{i}:{len(b)}")
        for bad in BANNED + TITLE_BITS:
            if bad in b:
                errors.append(f"ban_{i}:{bad}")
        if "第" in b and "章" in b:
            errors.append(f"chapter_{i}")
        cc = len(COLON_RE.findall(b))
        colon_hits += cc
        groups[b[:18]].append(i)
    if colon_hits > 2:
        errors.append(f"colon_total={colon_hits}")
    for pfx, ids in groups.items():
        if len(ids) >= 4:
            errors.append(f"prefix18:{pfx}:{ids}")
    if errors:
        raise SystemExit("FAIL\n" + "\n".join(errors))


def main() -> None:
    bodies = [ln.strip() for ln in BODIES_PATH.read_text(encoding="utf-8").splitlines() if ln.strip()]
    validate(bodies)
    highlights = [f"{i:03d}、{b}" for i, b in enumerate(bodies, 1)]
    data = json.loads(SRC.read_text(encoding="utf-8-sig"))
    data["chatgptHighlights"] = highlights
    data["chatgptStatus"] = "complete"
    data["highlightsSource"] = "grok"
    data["highlightsCapturedAt"] = STAMP
    data["updatedAt"] = DATE
    tmp = SRC.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(SRC)
    print("WROTE", SRC)
    print("COUNT", len(highlights))


if __name__ == "__main__":
    main()
