# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
from findbook_writer import validate_highlights  # noqa: E402

ids = sys.argv[1:]
if not ids:
    ids = []
    for date in ("20260714", "20260715"):
        for n in range(1, 31):
            ids.append(f"02_psychology_growth-{date}-{n:02d}")

out_lines = []
for book_id in ids:
    results = TOOLS / f".findbook_results_grok_{book_id}.json"
    book_path = ROOT / "Books" / "02_psychology_growth" / f"{book_id}.json"
    if not results.exists():
        out_lines.append(f"missing_results\t{book_id}")
        continue
    data = json.loads(results.read_text(encoding="utf-8-sig"))
    book = json.loads(book_path.read_text(encoding="utf-8-sig")) if book_path.exists() else {}
    try:
        validate_highlights(
            book_id,
            data.get("highlights"),
            str(book.get("title", "")),
            str(book.get("author", "")),
        )
        out_lines.append(f"ok\t{book_id}")
    except Exception as exc:
        out_lines.append(f"bad\t{book_id}\t{exc}")

report = TOOLS / ".redo_60_validate_report.txt"
report.write_text("\n".join(out_lines) + "\n", encoding="utf-8")
print(f"wrote {report} n={len(out_lines)}")
