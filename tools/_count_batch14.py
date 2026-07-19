# -*- coding: utf-8 -*-
from pathlib import Path
import re
text = Path("tools/_gen_batch14_highlights.py").read_text(encoding="utf-8")
for name in ["BOOK_41", "BOOK_42"]:
    m = re.search(rf"{name}\s*=\s*\[(.*?)\]\s*(?:\n\n|# Will|BOOK_|def |save_)", text, re.S)
    if not m:
        print(name, "NOT FOUND")
        continue
    items = re.findall(r'"([^"]+)"', m.group(1))
    print(name, "count", len(items), "unique", len(set(items)))
