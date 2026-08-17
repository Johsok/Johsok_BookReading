# -*- coding: utf-8 -*-
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
IDS = [f"04_healthcare-20260716-{i:02d}" for i in range(11, 21)]
results = []
for book_id in IDS:
    path = ROOT / f"{book_id}.json"
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    highlights = data.get("highlights") or data.get("chatgptHighlights")
    n = len(highlights) if isinstance(highlights, list) else type(highlights)
    print(f"{book_id}: n={n} file_id={data.get('id')}")
    if isinstance(highlights, list) and highlights:
        print(f"  first={highlights[0][:72]}")
        print(f"  last={highlights[-1][:72]}")
    results.append({"id": book_id, "highlights": highlights})

out = ROOT / "_batch_11_20.json"
out.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"wrote {out} count={len(results)}")
