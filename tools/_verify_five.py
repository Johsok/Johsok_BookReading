# -*- coding: utf-8 -*-
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
out = []
for i in ["223", "224", "225", "226", "227"]:
    bid = f"01_business_startup-20260716-{i}"
    p = root / "Books" / "01_business_startup" / f"{bid}.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    h = d.get("chatgptHighlights", [])
    ok = (
        d.get("highlightsSource") == "grok"
        and d.get("chatgptStatus") == "complete"
        and len(h) == 150
        and h[0].startswith("001、")
        and h[-1].startswith("150、")
    )
    out.append(f"{bid}\tok={ok}\tsource={d.get('highlightsSource')}\tcount={len(h)}")
Path(__file__).with_name("_verify_out.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
print("\n".join(out))
