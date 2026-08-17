# -*- coding: utf-8 -*-
"""Check rewrite progress for 02_psychology_growth-20260724-01..40."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "Books" / "02_psychology_growth"
MARKERS = (
    "落到具體情境，再用可觀察的結果確認做法是否有效",
    "作為判斷線索時",
    "先界定目標，再把",
    "先盤點條件，再把",
)


def main() -> None:
    done = []
    pending = []
    for i in range(1, 41):
        book_id = f"02_psychology_growth-20260724-{i:02d}"
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
        (done if ok else pending).append(f"{i:02d}")
    print("DONE", len(done), ",".join(done))
    print("PEND", len(pending), ",".join(pending))


if __name__ == "__main__":
    main()
