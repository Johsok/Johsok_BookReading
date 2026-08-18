# -*- coding: utf-8 -*-
import json
from pathlib import Path

root = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\Books\07_other")
out = []
for name in ("07_other-20260717-41.json", "07_other-20260717-42.json"):
    p = root / name
    d = json.loads(p.read_text(encoding="utf-8-sig"))
    hl = d["chatgptHighlights"]
    out.append(f"FILE {p}")
    out.append(f"id {d['id']}")
    out.append(f"len {len(hl)}")
    out.append(f"first {hl[0]}")
    out.append(f"last {hl[-1]}")
    out.append(f"chatgptStatus {d['chatgptStatus']}")
    out.append(f"highlightsSource {d['highlightsSource']}")
    out.append(f"highlightsCapturedAt {d.get('highlightsCapturedAt')}")
    out.append(f"updatedAt {d.get('updatedAt')}")
    nums = [x.split("、", 1)[0] for x in hl]
    out.append(f"num_ok {nums == [f'{i:03d}' for i in range(1,151)]}")
    other_ok = d.get("workId") and d.get("title")
    out.append(f"kept_title {d['title']}")
    out.append(f"kept_workId {d.get('workId')}")
    out.append("---")
Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\_tmp\_verify_41_42.txt").write_text(
    "\n".join(out), encoding="utf-8"
)
print("ok")
