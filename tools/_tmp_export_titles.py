# -*- coding: utf-8 -*-
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
manifest = json.loads((root / "data.json").read_text(encoding="utf-8-sig"))
cats = {"01_business_startup", "02_psychology_growth", "03_natural_science"}
out = []
recent = []
for book in manifest.get("books", []):
    if book.get("categoryId") not in cats:
        continue
    line = "\t".join(
        [
            str(book.get("id", "")),
            str(book.get("categoryId", "")),
            str(book.get("title", "")),
            str(book.get("author", "")),
            str(book.get("workId", "")),
        ]
    )
    out.append(line)
    if "20260818" in str(book.get("id", "")):
        recent.append(line)
(root / "tools" / ".existing_first3_titles.txt").write_text("\n".join(out), encoding="utf-8")
(root / "tools" / ".existing_20260818_first3.txt").write_text("\n".join(recent), encoding="utf-8")
print(f"wrote {len(out)} titles, {len(recent)} from 20260818")
