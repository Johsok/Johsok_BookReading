# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "Books" / "04_healthcare"
IDS = [
    "04_healthcare-20260713-01",
    "04_healthcare-20260713-02",
    "04_healthcare-20260714-01",
    "04_healthcare-20260714-02",
    "04_healthcare-20260716-02",
    "04_healthcare-20260716-03",
    "04_healthcare-20260716-04",
    "04_healthcare-20260716-05",
    "04_healthcare-20260716-06",
    "04_healthcare-20260716-07",
    "04_healthcare-20260716-08",
    "04_healthcare-20260716-09",
    "04_healthcare-20260716-10",
]
OLD = "健康資訊應區分預防、篩檢、診斷與治療"
FORB = ("本書", "作者指出", "本章", "這一章")
lines: list[str] = []

for book_id in IDS:
    path = ROOT / f"{book_id}.json"
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    highlights = data.get("chatgptHighlights") or []
    bodies = [re.sub(r"^\d{3}、", "", line).strip() for line in highlights]
    starts = Counter(body[:18] for body in bodies if len(body) >= 18)
    top = starts.most_common(1)[0] if starts else ("", 0)
    nums_ok = all(
        highlights[index].startswith(f"{index + 1:03d}、")
        for index in range(len(highlights))
    )
    template = sum(OLD in line for line in highlights)
    forbidden = sum(any(token in body for token in FORB) for body in bodies)
    line = (
        f"{book_id}\tcount={len(highlights)}\tsrc={data.get('highlightsSource')}"
        f"\tstatus={data.get('chatgptStatus')}\tnum={nums_ok}"
        f"\tdup={len(bodies) - len(set(bodies))}\ttop18={top[1]}"
        f"\ttemplate={template}\tforb={forbidden}"
        f"\tupdated={data.get('updatedAt')}"
    )
    lines.append(line)

out = Path(__file__).resolve().parent / "_verify_hc_redo_out.txt"
out.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"wrote {out} n={len(lines)}")
