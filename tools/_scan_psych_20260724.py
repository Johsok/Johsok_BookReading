# -*- coding: utf-8 -*-
"""Scan highlight quality for 02_psychology_growth-20260724-01..40."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

DIR = Path(__file__).resolve().parents[1] / "Books" / "02_psychology_growth"
MARKERS = (
    "落到具體情境，再用可觀察的結果確認做法是否有效",
    "作為判斷線索時",
    "先界定目標，再把",
    "先盤點條件，再把",
    "再把概念轉成可執行、可追蹤、可調整的下一步",
    "第001項心理勵志觀察",
    "心理勵志觀察協助讀者",
)


def main() -> None:
    for i in range(1, 41):
        book_id = f"02_psychology_growth-20260724-{i:02d}"
        data = json.loads((DIR / f"{book_id}.json").read_text(encoding="utf-8"))
        highlights = data.get("chatgptHighlights") or []
        bodies = [h[4:] if h[:4].endswith("、") else h for h in highlights]
        text = "\n".join(highlights)
        hits = [m for m in MARKERS if m in text]
        starts = Counter(b[:18] for b in bodies if len(b) >= 18)
        top_start, top_n = starts.most_common(1)[0] if starts else ("", 0)
        sample = bodies[0][:50] if bodies else ""
        flag = "BAD" if hits or top_n >= 8 else "ok"
        print(f"{i:02d}\t{flag}\tn={len(highlights)}\thits={hits}\trepeat18={top_n}:{top_start}\t{sample}")


if __name__ == "__main__":
    main()
