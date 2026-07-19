# -*- coding: utf-8 -*-
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from findbook_writer import validate_highlights  # noqa: E402

src_path = Path(__file__).with_name("_gen_batch39_highlights.py")
ns = {"__file__": str(src_path)}
exec(compile(src_path.read_text(encoding="utf-8"), "b39", "exec"), ns)
batch = json.loads((ROOT / "tools" / "_batch39.json").read_text(encoding="utf-8"))
meta = {b["id"]: b for b in batch}
for book_id, category_id, lines in ns["BOOKS"]:
    cleaned = [b.strip() for b in lines]
    assert len(cleaned) == 150, (book_id, len(cleaned))
    hl = [f"{i:03d}、{b}" for i, b in enumerate(cleaned, 1)]
    validate_highlights(book_id, hl, meta[book_id]["title"], meta[book_id]["author"])
    print("VALID", book_id)
print("all ok")
