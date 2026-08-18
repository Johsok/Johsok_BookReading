# -*- coding: utf-8 -*-
import json
from pathlib import Path

ROOT = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\Books\05_food_wellness")


def save(book_id, highlights):
    if len(highlights) != 150:
        raise SystemExit(f"{book_id} count={len(highlights)}")
    seen = set()
    for i, h in enumerate(highlights, 1):
        prefix = f"{i:03d}、"
        if not h.startswith(prefix):
            raise SystemExit(f"{book_id} bad {i}: {h[:30]}")
        body = h[len(prefix):]
        if body in seen:
            raise SystemExit(f"{book_id} dup body {i}")
        seen.add(body)
        if "｜" in h or "本書" in h or "作者指出" in h:
            raise SystemExit(f"{book_id} banned {i}")
    path = ROOT / f"{book_id}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["chatgptHighlights"] = highlights
    data["chatgptStatus"] = "complete"
    data["highlightsSource"] = "grok"
    data["updatedAt"] = "2026-08-18"
    data["highlightsCapturedAt"] = "2026-08-18T09:45:00+08:00"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("ok", book_id, len(highlights))
