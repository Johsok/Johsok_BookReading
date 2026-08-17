# -*- coding: utf-8 -*-
"""Check redo progress for 01_business_startup-20260724-01..40."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "Books" / "01_business_startup"
QUEUE = ROOT / "tools" / "._redo_queue_20260724_01_40.json"
MARKERS = (
    "以「商業理財」作為",
    "落到具體情境，再用可觀察的結果確認做法是否有效",
)


def main() -> None:
    rows = json.loads(QUEUE.read_text(encoding="utf-8"))
    done = []
    pending = []
    for row in rows:
        book_id = row["id"]
        data = json.loads((DIR / f"{book_id}.json").read_text(encoding="utf-8"))
        highlights = data.get("chatgptHighlights") or []
        text = "\n".join(highlights)
        templated = any(marker in text for marker in MARKERS)
        ok = (
            len(highlights) == 150
            and data.get("highlightsSource") == "grok"
            and data.get("chatgptStatus") == "complete"
            and not templated
        )
        (done if ok else pending).append(book_id)
    print("DONE", len(done))
    print("PEND", len(pending))
    print("DONE_IDS", ",".join(done))
    print("PEND_IDS", ",".join(pending))


if __name__ == "__main__":
    main()
