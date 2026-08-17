# -*- coding: utf-8 -*-
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "Books" / "02_psychology_growth"
OUT = ROOT / "tools" / ".redo_60_written_check.txt"

old_marker = "以人生秩序、責任、自我成長為閱讀線索"
generic_marker = "閱讀時可先確認作者如何定義問題"

lines = []
ok = 0
for date in ("20260714", "20260715"):
    for n in range(1, 31):
        book_id = f"02_psychology_growth-{date}-{n:02d}"
        data = json.loads((BASE / f"{book_id}.json").read_text(encoding="utf-8-sig"))
        hl = data.get("chatgptHighlights") or []
        first = hl[0] if hl else ""
        last = hl[-1] if hl else ""
        bad = []
        if len(hl) != 150:
            bad.append(f"n={len(hl)}")
        if data.get("chatgptStatus") != "complete":
            bad.append(f"status={data.get('chatgptStatus')}")
        if data.get("highlightsSource") != "grok":
            bad.append(f"source={data.get('highlightsSource')}")
        joined = "\n".join(hl)
        if old_marker in joined or generic_marker in joined:
            bad.append("old_template")
        if not first.startswith("001、") or not last.startswith("150、"):
            bad.append("bad_number")
        status = "ok" if not bad else "bad:" + ",".join(bad)
        if status == "ok":
            ok += 1
        lines.append(f"{status}\t{book_id}\t{data.get('title')}\t{first[:40]}\t{last[:40]}")

OUT.write_text("\n".join(lines) + f"\n# ok={ok}/60\n", encoding="utf-8")
print(f"ok={ok}/60 report={OUT}")
