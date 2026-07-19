# -*- coding: utf-8 -*-
"""Check redo progress for 01_business_startup-20260716-03..162."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "Books" / "01_business_startup"
META = ROOT / "tools" / "_redo_books_20260716_03_162.json"

sys.stdout.reconfigure(encoding="utf-8")

done = []
pending = []
for row in json.loads(META.read_text(encoding="utf-8")):
    book_id = row["id"]
    path = BASE / f"{book_id}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    hl = data.get("chatgptHighlights") or []
    sample = " ".join(hl[:8])
    is_tmpl = (
        "閱讀時可先確認作者如何定義問題" in sample
        or "可把觀點轉成一個具體案例" in sample
        or "整理筆記時宜區分核心主張" in sample
    )
    ok = (
        data.get("chatgptStatus") == "complete"
        and data.get("highlightsSource") == "grok"
        and len(hl) == 150
        and not is_tmpl
    )
    if ok:
        done.append(book_id)
    else:
        pending.append(
            {
                "id": book_id,
                "title": row["title"],
                "author": row["author"],
                "summary": (data.get("summary") or "")[:160],
            }
        )

print(f"DONE\t{len(done)}")
print(f"PENDING\t{len(pending)}")
for row in pending[:12]:
    print(f"NEXT\t{row['id']}\t{row['author']}\t{row['title']}\t{row['summary']}")
