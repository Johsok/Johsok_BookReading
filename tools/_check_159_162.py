# -*- coding: utf-8 -*-
from pathlib import Path
import importlib.util

p = Path(__file__).with_name("_grok_write_159_162.py")
spec = importlib.util.spec_from_file_location("w", p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

from findbook_writer import validate_highlights

for book_id, lines in [
    ("01_business_startup-20260716-159", mod.BOOK_159),
    ("01_business_startup-20260716-160", mod.BOOK_160),
    ("01_business_startup-20260716-161", mod.BOOK_161),
    ("01_business_startup-20260716-162", mod.BOOK_162),
]:
    print(book_id, "count", len(lines))
    if len(lines) != 150:
        print(book_id, "SKIP validate wrong count")
        continue
    try:
        hl = mod.numbered(lines)
        validate_highlights(book_id, hl)
        print(book_id, "OK")
    except Exception as e:
        print(book_id, "FAIL", e)
