# -*- coding: utf-8 -*-
from pathlib import Path

d = Path(__file__).with_name("_batch77_bodies")
for p in sorted(d.glob("*.txt")):
    lines = [ln.strip() for ln in p.read_text(encoding="utf-8").splitlines() if ln.strip()]
    print(p.name, len(lines), "bad" if any(x in ("thrush",) or "�" in x for x in lines) else "ok")
    if len(lines) != 150:
        print("  last3:", lines[-3:])
