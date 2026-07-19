# -*- coding: utf-8 -*-
"""Print next pending books for 20260716-03..162 redo dispatch."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.stdout.reconfigure(encoding="utf-8")
META = json.loads((ROOT / "tools" / "_redo_books_20260716_03_162.json").read_text(encoding="utf-8"))
BASE = ROOT / "Books" / "01_business_startup"

pending = []
for row in META:
    data = json.loads((BASE / f"{row['id']}.json").read_text(encoding="utf-8"))
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
    if not ok:
        pending.append(row)

start = int(sys.argv[1]) if len(sys.argv) > 1 else 0
n = int(sys.argv[2]) if len(sys.argv) > 2 else 8
for row in pending[start : start + n]:
    print(f"{row['id']}\t{row['author']}\t{row['title']}")
print(f"TOTAL_PENDING\t{len(pending)}")
