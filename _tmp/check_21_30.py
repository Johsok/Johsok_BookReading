# -*- coding: utf-8 -*-
import json
from pathlib import Path

base = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\Books\07_other")
out = []
for n in range(21, 31):
    p = base / f"07_other-20260717-{n}.json"
    d = json.loads(p.read_text(encoding="utf-8-sig"))
    hs = d.get("chatgptHighlights") or []
    first = (hs[0][:60]) if hs else ""
    generic = "理解作品需先辨認作者所處的時代" in (hs[0] if hs else "")
    line = (
        f"{n}: n={len(hs)} status={d.get('chatgptStatus')} src={d.get('highlightsSource')} "
        f"generic={generic} last150={bool(hs) and hs[-1].startswith('150、')} "
        f"updated={d.get('updatedAt')}\n    {first}\n"
    )
    print(line)
    out.append(line)

Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\_tmp\check_21_30_out.txt").write_text(
    "".join(out), encoding="utf-8"
)
