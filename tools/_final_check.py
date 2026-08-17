# -*- coding: utf-8 -*-
from pathlib import Path
import json
import re

simp_chars = set("为这们国学来对与从时会还过说让给当经现点发产创后么应该没种样进开关问间长门见觉听体实发写条处总只里干准台群")
# 只/里/干/准/台/群 are often valid TW; report contextually.

out = []
for path in [
    Path("tools/.findbook_results_grok_07_other-20260716-41.json"),
    Path("tools/.findbook_results_grok_07_other-20260716-42.json"),
]:
    data = json.loads(path.read_text(encoding="utf-8"))
    hl = data["highlights"]
    out.append(f"{path.name} count={len(hl)}")
    out.append("001 " + hl[0])
    out.append("150 " + hl[-1])
    for i, line in enumerate(hl, 1):
        body = line.split("、", 1)[1]
        hits = [ch for ch in body if ch in "为这们国学来对与从时会还过说让给当经现点发产创么应该没种样进开关问间长门见觉听体实写条处总"]
        if hits:
            out.append(f"SIMP {i:03d} {hits} {body}")
        if "裡" not in body and "里" in body:
            # 里 as inside?
            if re.search(r"[这那哪这這那哪]里|里[面頭头]|心里面|脑子里", body):
                out.append(f"LI {i:03d} {body}")
Path("tools/_final_check.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
print("wrote checks", len(out))
