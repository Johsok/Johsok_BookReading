# -*- coding: utf-8 -*-
"""Print verification for books 43 and 44."""
import json
from pathlib import Path

ROOT = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\Books\07_other")
out = []
for name in ("07_other-20260717-43.json", "07_other-20260717-44.json"):
    d = json.loads((ROOT / name).read_text(encoding="utf-8-sig"))
    hl = d["chatgptHighlights"]
    out.append(f"FILE {name}")
    out.append(f"id {d['id']}")
    out.append(f"len {len(hl)}")
    out.append(f"status {d['chatgptStatus']}")
    out.append(f"source {d['highlightsSource']}")
    out.append(f"captured {d['highlightsCapturedAt']}")
    out.append(f"updated {d['updatedAt']}")
    out.append(f"first {hl[0]}")
    out.append(f"last {hl[-1]}")
    out.append("---")
    for i, line in enumerate(hl, 1):
        body = line.split("、", 1)[1]
        out.append(f"{i:03d} [{len(body)}] {body}")
    out.append("")

Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\_tmp\_verify_43_44.txt").write_text(
    "\n".join(out), encoding="utf-8"
)
print("wrote verify")
