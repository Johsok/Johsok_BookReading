# -*- coding: utf-8 -*-
from __future__ import annotations

import sys
from argparse import Namespace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
from findbook_writer import complete  # noqa: E402

ids = sys.argv[1:]
if not ids:
    for date in ("20260714", "20260715"):
        for n in range(1, 31):
            ids.append(f"02_psychology_growth-{date}-{n:02d}")

ok = []
bad = []
for book_id in ids:
    results = TOOLS / f".findbook_results_grok_{book_id}.json"
    if not results.exists():
        bad.append(f"missing\t{book_id}")
        continue
    args = Namespace(
        root=str(ROOT),
        results=str(results),
        category_id="02_psychology_growth",
        category_file=None,
    )
    try:
        complete(args)
        ok.append(book_id)
    except Exception as exc:
        bad.append(f"{book_id}\t{exc}")

report = TOOLS / ".redo_60_complete_report.txt"
lines = [f"ok\t{item}" for item in ok] + [f"bad\t{item}" for item in bad]
report.write_text("\n".join(lines) + f"\n# ok={len(ok)} bad={len(bad)}\n", encoding="utf-8")
print(f"ok={len(ok)} bad={len(bad)}")
