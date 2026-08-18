# -*- coding: utf-8 -*-
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from findbook_writer import read_json, validate_highlights

out = []
for bid in [
    "07_other-20260717-34",
    "07_other-20260717-35",
    "07_other-20260717-36",
]:
    path = ROOT / "Books" / "07_other" / f"{bid}.json"
    data = read_json(path)
    validate_highlights(bid, data["chatgptHighlights"], data["title"], data["author"])
    lines = [
        f"## {bid}",
        f"count={len(data['chatgptHighlights'])}",
        f"updatedAt={data['updatedAt']}",
        data["chatgptHighlights"][0],
        data["chatgptHighlights"][1],
        data["chatgptHighlights"][2],
        "",
    ]
    out.extend(lines)
    print("PASS", bid, len(data["chatgptHighlights"]), data["updatedAt"])

Path(__file__).with_name("verify_34_36.txt").write_text("\n".join(out), encoding="utf-8")
