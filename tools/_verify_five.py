# -*- coding: utf-8 -*-
import json
from pathlib import Path

ids = [
    "02_psychology_growth-20260716-183",
    "02_psychology_growth-20260716-184",
    "02_psychology_growth-20260716-185",
    "02_psychology_growth-20260716-186",
    "02_psychology_growth-20260716-187",
]
lines = []
for book_id in ids:
    path = Path("Books/02_psychology_growth") / f"{book_id}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    highlights = data.get("chatgptHighlights", [])
    lines.append(
        f"{book_id}\t{data.get('chatgptStatus')}\t{data.get('highlightsSource')}\t{len(highlights)}\t{highlights[0][:20]}\t{highlights[-1][:20]}"
    )
Path("tools/_verify_out.txt").write_text("\n".join(lines), encoding="utf-8")
