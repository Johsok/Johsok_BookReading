# -*- coding: utf-8 -*-
"""Validate all 07_other 31-40 highlights."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading")
sys.path.insert(0, str(ROOT / "tools"))
from findbook_writer import validate_highlights  # noqa: E402

BAD_SNIPPETS = (
    "閱讀時可先確認作者如何定義問題",
    "可把觀點轉成一個具體案例",
    "應比較支持證據與可能反例",
    "實際運用時可先做小規模嘗試",
    "整理筆記時宜區分核心主張",
)

out_lines = []
base = ROOT / "Books" / "07_other"
all_ok = True
for n in range(31, 41):
    path = base / f"07_other-20260717-{n:02d}.json"
    book = json.loads(path.read_text(encoding="utf-8-sig"))
    hs = book.get("chatgptHighlights", [])
    book_id = book["id"]
    try:
        validate_highlights(book_id, hs, book.get("title", ""), book.get("author", ""))
        status = "PASS"
    except Exception as e:
        status = f"FAIL: {e}"
        all_ok = False
    template_hits = sum(1 for h in hs if any(s in h for s in BAD_SNIPPETS))
    samples = " | ".join(hs[:3]) if len(hs) >= 3 else ""
    out_lines.append(
        f"{book_id}\t{status}\tn={len(hs)}\ttemplate_hits={template_hits}\tupdatedAt={book.get('updatedAt')}"
    )
    out_lines.append(f"  samples: {samples[:200]}")

report = ROOT / "_tmp" / "verify_07_31_40.txt"
report.write_text("\n".join(out_lines) + f"\n\nALL_OK={all_ok}\n", encoding="utf-8")
print("ALL_OK" if all_ok else "HAS_FAIL")
print(str(report))
