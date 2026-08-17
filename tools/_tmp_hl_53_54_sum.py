# -*- coding: utf-8 -*-
import json
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
lines = []
for book_id in ("07_other-20260716-53", "07_other-20260716-54"):
    p = TOOLS / f".findbook_results_grok_{book_id}.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    hl = d["highlights"]
    bodies = [x.split("、", 1)[1] for x in hl]
    lines.append(f"{book_id}")
    lines.append(f"  path={p}")
    lines.append(f"  count={len(hl)} id={d['id']}")
    lines.append(f"  001={hl[0]}")
    lines.append(f"  150={hl[149]}")
    if book_id.endswith("53"):
        lines.append(f"  start共濟會={sum(b.startswith('共濟會') for b in bodies)}")
        lines.append(f"  沈以謙={sum('沈以謙' in b for b in bodies)}")
    else:
        lines.append(f"  start曾國藩={sum(b.startswith('曾國藩') for b in bodies)}")
        lines.append(f"  曾國藩_in={sum('曾國藩' in b for b in bodies)}")
        lines.append(f"  趙焰={sum('趙焰' in b for b in bodies)}")
(TOOLS / "_tmp_hl_53_54_summary.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
