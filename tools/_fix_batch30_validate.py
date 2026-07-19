# -*- coding: utf-8 -*-
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from findbook_writer import validate_highlights

ROOT = Path(__file__).resolve().parents[1]
ids = [
    "01_business_startup-20260718-67",
    "01_business_startup-20260718-68",
    "01_business_startup-20260718-69",
    "01_business_startup-20260718-70",
]
for book_id in ids:
    result_path = ROOT / "tools" / f".findbook_results_grok_{book_id}.json"
    payload = json.loads(result_path.read_text(encoding="utf-8"))
    book_path = ROOT / "Books" / "01_business_startup" / f"{book_id}.json"
    book = json.loads(book_path.read_text(encoding="utf-8"))
    try:
        validate_highlights(book_id, payload["highlights"], book.get("title", ""), book.get("author", ""))
        print(f"OK\t{book_id}")
    except Exception as exc:
        print(f"FAIL\t{book_id}\t{exc}")
