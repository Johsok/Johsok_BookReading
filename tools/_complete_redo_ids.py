# -*- coding: utf-8 -*-
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
WRITER = TOOLS / "findbook_writer.py"

ids = sys.argv[1:]
if not ids:
    raise SystemExit("need book ids")

for book_id in ids:
    results = TOOLS / f".findbook_results_grok_{book_id}.json"
    if not results.exists():
        print(f"missing\t{book_id}")
        continue
    proc = subprocess.run(
        [
            sys.executable,
            str(WRITER),
            "--root",
            str(ROOT),
            "complete",
            "--category-id",
            "02_psychology_growth",
            "--results",
            str(results),
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    sys.stdout.write(proc.stdout or "")
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr or "")
        print(f"fail\t{book_id}\t{proc.returncode}")
