# -*- coding: utf-8 -*-
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from findbook_writer import validate_highlights

base = Path(__file__).resolve().parents[1] / "Books" / "01_business_startup"
ids = ["90", "103", "104", "105", "109", "110", "115", "120", "140", "165", "170", "180"]
for i in ids:
    d = json.loads((base / f"01_business_startup-20260717-{i}.json").read_text(encoding="utf-8"))
    try:
        validate_highlights(d["id"], d["chatgptHighlights"], d["title"], d["author"])
        ok = "OK"
    except Exception as e:
        ok = f"FAIL {e}"
    src = d.get("highlightsSource")
    n = len(d.get("chatgptHighlights", []))
    print(f"{i}\t{src}\t{n}\t{ok}")
