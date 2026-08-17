# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from findbook_writer import validate_highlights

ROOT = Path(__file__).resolve().parents[1]
OLD = "閱讀時可先確認作者如何定義問題"
lines = []
for n in range(41, 61):
    bid = f"07_other-20260716-{n}"
    path = ROOT / "Books" / "07_other" / f"{bid}.json"
    book = json.loads(path.read_text(encoding="utf-8"))
    hl = book["chatgptHighlights"]
    validate_highlights(bid, hl, book.get("title", ""), book.get("author", ""))
    old_hits = sum(OLD in x for x in hl)
    assert book.get("chatgptStatus") == "complete"
    assert book.get("highlightsSource") == "grok"
    assert len(hl) == 150
    lines.append(
        f"{bid}\tok old={old_hits} src={book['highlightsSource']} "
        f"at={book.get('highlightsCapturedAt')}"
    )
out = Path(__file__).with_name("_tmp_hl_41_60_written.txt")
out.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"verified {len(lines)}")
