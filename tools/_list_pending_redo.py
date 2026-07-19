# -*- coding: utf-8 -*-
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "Books" / "01_business_startup"
QUEUE = ROOT / "tools" / "._redo_queue_20260716_223_to_20260717_220.json"
MARKERS = (
    "閱讀時可先確認作者如何定義問題",
    "可把觀點轉成一個具體案例，觀察它在現實限制下是否仍然成立",
)


def main() -> None:
    rows = json.loads(QUEUE.read_text(encoding="utf-8"))
    pending = []
    for row in rows:
        book_id = row["id"]
        data = json.loads((DIR / f"{book_id}.json").read_text(encoding="utf-8"))
        highlights = data.get("chatgptHighlights") or []
        text = "\n".join(highlights)
        templated = any(m in text for m in MARKERS)
        ok = (
            len(highlights) == 150
            and data.get("highlightsSource") == "grok"
            and data.get("chatgptStatus") == "complete"
            and not templated
        )
        if not ok:
            pending.append(book_id)
    print(f"PENDING\t{len(pending)}")
    print(",".join(pending))


if __name__ == "__main__":
    main()
