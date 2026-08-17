# -*- coding: utf-8 -*-
import json
from pathlib import Path

root = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading")
ids = [
    "07_other-20260716-14",
    "07_other-20260716-15",
    "07_other-20260716-16",
    "07_other-20260716-17",
]
out = root / "tools" / ".hl_samples_report.txt"
lines = []
for book_id in ids:
    path = root / "Books" / "07_other" / f"{book_id}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    h = data["chatgptHighlights"]
    lines.append(f"== {book_id}")
    lines.append(f"status {data.get('chatgptStatus')}")
    lines.append(f"source {data.get('highlightsSource')}")
    lines.append(f"n {len(h)}")
    lines.append(f"P1 {h[0]}")
    lines.append(f"P50 {h[49]}")
    lines.append(f"P100 {h[99]}")
    lines.append(f"P150 {h[149]}")
    lines.append("")
out.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("wrote")
