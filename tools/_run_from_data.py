# -*- coding: utf-8 -*-
from __future__ import annotations

import importlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent


def complete(book_id: str, bodies: list[str]) -> None:
    if len(bodies) != 150:
        raise SystemExit(f"{book_id} need 150 got {len(bodies)}")
    if len(set(bodies)) != 150:
        raise SystemExit(f"{book_id} has duplicates")
    payload = {
        "id": book_id,
        "highlights": [f"{i:03d}、{b}" for i, b in enumerate(bodies, 1)],
    }
    results = TOOLS / f".findbook_results_grok_{book_id}.json"
    results.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    proc = subprocess.run(
        [
            sys.executable,
            str(TOOLS / "findbook_writer.py"),
            "--root",
            str(ROOT),
            "complete",
            "--category-id",
            "01_business_startup",
            "--results",
            str(results),
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    sys.stdout.write(proc.stdout or "")
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr or "")
        raise SystemExit(proc.returncode)
    book = json.loads(
        (ROOT / "Books" / "01_business_startup" / f"{book_id}.json").read_text(encoding="utf-8-sig")
    )
    print(f"written/{book['id']}/{len(book['chatgptHighlights'])}/{book.get('highlightsSource')}")


if __name__ == "__main__":
    which = sys.argv[1]
    mapping = {
        "36": ("01_business_startup-20260716-36", "_data_book_36", "BOOK_36"),
        "37": ("01_business_startup-20260716-37", "_data_book_37", "BOOK_37"),
        "38": ("01_business_startup-20260716-38", "_data_book_38", "BOOK_38"),
    }
    book_id, mod_name, attr = mapping[which]
    sys.path.insert(0, str(TOOLS))
    mod = importlib.import_module(mod_name)
    bodies = list(getattr(mod, attr))
    complete(book_id, bodies)
