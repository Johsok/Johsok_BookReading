# -*- coding: utf-8 -*-
from pathlib import Path
import importlib.util
import json
from collections import Counter

from findbook_writer import validate_highlights

p = Path(__file__).with_name("_grok_write_159_162.py")
spec = importlib.util.spec_from_file_location("w", p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

root = Path(__file__).resolve().parents[1]
books = [
    ("01_business_startup-20260716-159", mod.BOOK_159),
    ("01_business_startup-20260716-160", mod.BOOK_160),
    ("01_business_startup-20260716-161", mod.BOOK_161),
    ("01_business_startup-20260716-162", mod.BOOK_162),
]
for book_id, lines in books:
    book = json.loads((root / "Books" / "01_business_startup" / f"{book_id}.json").read_text(encoding="utf-8-sig"))
    hl = mod.numbered(lines)
    bodies = [x.split("、", 1)[1] for x in hl]
    starts = Counter(b[:18] for b in bodies)
    top = starts.most_common(3)
    print(book_id, "top starts", top)
    try:
        validate_highlights(book_id, hl, book.get("title", ""), book.get("author", ""))
        print(book_id, "OK with title/author")
    except Exception as e:
        print(book_id, "FAIL", e)
