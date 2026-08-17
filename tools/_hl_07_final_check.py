# -*- coding: utf-8 -*-
import json
from pathlib import Path
from collections import Counter
import sys
import re

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.findbook_writer import validate_highlights

p = Path("tools/_hl_07.json")
d = json.loads(p.read_text(encoding="utf-8"))
hl = d["highlights"]
lines = []
lines.append(f"path={p.resolve()}")
lines.append(f"id={d['id']}")
lines.append(f"count={len(hl)}")
validate_highlights(
    d["id"],
    hl,
    "格拉瑪號的遠征：古巴革命戰爭回憶錄",
    "切．格瓦拉",
)
lines.append("validate_highlights=OK")
bodies = [x.split("、", 1)[1] for x in hl]
starts = Counter(b[:18] for b in bodies)
lines.append(f"min_len={min(len(b) for b in bodies)}")
lines.append(f"max_len={max(len(b) for b in bodies)}")
lines.append(f"格瓦拉={sum(x.count('格瓦拉') for x in hl)}")
lines.append(f"游擊隊軍醫指揮官={sum(x.count('游擊隊軍醫指揮官') for x in hl)}")
lines.append(f"dup={len(bodies) - len(set(bodies))}")
lines.append(f"start_ge4={[(k, v) for k, v in starts.items() if v >= 4]}")
forbid = ["本書", "作者指出", "本章", "書名", "｜"]
hits = []
for i, line in enumerate(hl, 1):
    for tok in forbid:
        if tok in line:
            hits.append(f"{i}:{tok}")
    m = re.match(r"^([^：:]{1,12})[：:]", bodies[i - 1])
    if m and not m.group(1).endswith(("是", "為", "在於", "說", "問", "提醒", "表示", "指出")):
        hits.append(f"{i}:colon")
lines.append(f"forbidden_hits={hits or 'none'}")
lines.append("CHECK OK")
Path("tools/_hl_07_final_check.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
