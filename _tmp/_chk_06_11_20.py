# -*- coding: utf-8 -*-
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from findbook_writer import validate_highlights  # noqa: E402

root = ROOT / "Books" / "06_computer_info"
old = "先定義使用情境與成功指標"
for i in range(11, 21):
    bid = f"06_computer_info-20260717-{i:02d}"
    path = root / f"{bid}.json"
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    highlights = data.get("chatgptHighlights", [])
    try:
        validate_highlights(bid, highlights, data.get("title", ""), data.get("author", ""))
        status = "PASS"
    except Exception as exc:
        status = f"FAIL {exc}"
    old_n = sum(1 for line in highlights if old in line)
    print(
        f"{bid}\tn={len(highlights)}\tsrc={data.get('highlightsSource')}"
        f"\tstatus={data.get('chatgptStatus')}\tupd={data.get('updatedAt')}"
        f"\told={old_n}\t{status}"
    )
    if highlights:
        print(" ", highlights[0][:80])
        print(" ", highlights[-1][:80])
