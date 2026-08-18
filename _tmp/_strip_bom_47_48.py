# -*- coding: utf-8 -*-
import json
from pathlib import Path

root = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\Books\07_other")
for name in ("07_other-20260717-47.json", "07_other-20260717-48.json"):
    path = root / name
    data = json.loads(path.read_bytes().decode("utf-8-sig"))
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)
    raw = path.read_bytes()
    print(name, "bom", raw.startswith(b"\xef\xbb\xbf"), "n", len(data["chatgptHighlights"]))
