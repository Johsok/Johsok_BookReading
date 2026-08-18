# -*- coding: utf-8 -*-
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
from findbook_writer import validate_highlights, read_json

ok = True
for n in range(31, 41):
    p = ROOT / "Books/03_natural_science" / f"_hl_{n}.json"
    book = ROOT / "Books/03_natural_science" / f"03_natural_science-20260716-{n}.json"
    data = json.loads(p.read_text(encoding="utf-8-sig"))
    b = read_json(book)
    try:
        validate_highlights(data["id"], data["highlights"], b.get("title", ""), b.get("author", ""))
        print(f"OK {n} {len(data['highlights'])}")
    except Exception as e:
        ok = False
        print(f"FAIL {n}: {e}")
print("ALL_OK" if ok else "HAS_FAIL")
