# -*- coding: utf-8 -*-
import sys
from pathlib import Path

sys.path.insert(0, str(Path("tools").resolve()))
from findbook_highlights import extract_highlights, write_highlights

ROOT = Path(".").resolve()
mapping = {
    "01_business_startup-20210901-31": "tools/_hl_01-31.txt",
    "01_business_startup-20210901-32": "tools/_hl_01-32.txt",
    "01_business_startup-20210901-33": "tools/_hl_01-33.txt",
}
for book_id, rel in mapping.items():
    text = Path(rel).read_text(encoding="utf-8")
    lines = extract_highlights(text)
    result = write_highlights(ROOT, book_id, lines)
    print(result["id"], result["count"])
    if result["count"] != 150:
        raise SystemExit(f"{book_id} count={result['count']}")
