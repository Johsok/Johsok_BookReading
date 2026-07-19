# -*- coding: utf-8 -*-
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
payloads = json.loads((ROOT / "tools" / ".findbook_payloads_46_50.json").read_text(encoding="utf-8"))
ids = [
    "01_business_startup-20260717-46",
    "01_business_startup-20260717-47",
    "01_business_startup-20260717-48",
    "01_business_startup-20260717-49",
    "01_business_startup-20260717-50",
]
for book_id in ids:
    bodies = payloads[book_id]
    highlights = [f"{i:03d}、{b}" for i, b in enumerate(bodies, 1)]
    path = ROOT / "tools" / f".findbook_results_grok_{book_id}.json"
    path.write_text(
        json.dumps({"id": book_id, "highlights": highlights}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    cmd = [
        sys.executable,
        str(ROOT / "tools" / "findbook_writer.py"),
        "complete",
        "--category-id",
        "01_business_startup",
        "--results",
        str(path),
    ]
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = ((r.stdout or "") + (r.stderr or "")).strip()
    book = json.loads((ROOT / "Books" / "01_business_startup" / f"{book_id}.json").read_text(encoding="utf-8-sig"))
    n = len(book.get("chatgptHighlights") or [])
    ok = (
        r.returncode == 0
        and f"written\t{book_id}" in (r.stdout or "")
        and n == 150
        and book.get("chatgptStatus") == "complete"
        and book.get("highlightsSource") == "grok"
    )
    print(f"{book_id}\t{'OK' if ok else 'FAIL'}\t{n}")
    if not ok:
        print(out)
        raise SystemExit(1)
