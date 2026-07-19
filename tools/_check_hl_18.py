# -*- coding: utf-8 -*-
import json
from pathlib import Path

base = Path(r"Books/01_business_startup")
for i in range(1, 21):
    p = base / f"01_business_startup-20260718-{i:02d}.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    hl = d.get("chatgptHighlights") or []
    sample = (hl[0][:48] if hl else "")
    tpl = any(
        x in (hl[0] if hl else "")
        for x in ("閱讀切面", "數位工具應縮短回饋週", "第001個")
    )
    print(
        f"{i:02d}|n={len(hl)}|st={d.get('chatgptStatus')}"
        f"|src={d.get('highlightsSource')}|tpl={tpl}|{sample}"
    )
