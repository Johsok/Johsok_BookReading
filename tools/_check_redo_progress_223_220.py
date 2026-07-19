# -*- coding: utf-8 -*-
"""Check redo progress for 20260716-223..282 and 20260717-01..220."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "Books" / "01_business_startup"
QUEUE = ROOT / "tools" / "._redo_queue_20260716_223_to_20260717_220.json"
TEMPLATE_MARKERS = (
    "閱讀時可先確認作者如何定義問題",
    "可把觀點轉成一個具體案例，觀察它在現實限制下是否仍然成立",
)


def main() -> None:
    rows = json.loads(QUEUE.read_text(encoding="utf-8"))
    done = []
    pending = []
    for row in rows:
        book_id = row["id"]
        path = DIR / f"{book_id}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        highlights = data.get("chatgptHighlights") or []
        text = "\n".join(highlights)
        templated = any(marker in text for marker in TEMPLATE_MARKERS)
        source = data.get("highlightsSource")
        status = data.get("chatgptStatus")
        ok = (
            len(highlights) == 150
            and source == "grok"
            and status == "complete"
            and not templated
        )
        item = {
            "id": book_id,
            "title": data.get("title", ""),
            "n": len(highlights),
            "source": source,
            "status": status,
            "templated": templated,
        }
        if ok:
            done.append(item)
        else:
            pending.append(item)
    print(f"DONE\t{len(done)}")
    print(f"PENDING\t{len(pending)}")
    print(f"TOTAL\t{len(rows)}")
    print("DONE_IDS\t" + ",".join(item["id"] for item in done))
    print("NEXT20\t" + ",".join(item["id"] for item in pending[:20]))


if __name__ == "__main__":
    main()
