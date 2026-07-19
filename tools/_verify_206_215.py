# -*- coding: utf-8 -*-
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
base = Path(__file__).resolve().parents[1] / "Books" / "01_business_startup"
for n in range(206, 216):
    book_id = f"01_business_startup-20260717-{n}"
    d = json.loads((base / f"{book_id}.json").read_text(encoding="utf-8-sig"))
    hl = d.get("chatgptHighlights") or []
    ok = (
        d.get("chatgptStatus") == "complete"
        and d.get("highlightsSource") == "grok"
        and len(hl) == 150
    )
    print(
        f"{book_id}\tok={ok}\tsrc={d.get('highlightsSource')}\t"
        f"n={len(hl)}\tcaptured={d.get('highlightsCapturedAt')}"
    )
