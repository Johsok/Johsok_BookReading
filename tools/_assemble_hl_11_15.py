# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from findbook_writer import validate_highlights  # noqa: E402

BOOKS = [
    (
        "02_psychology_growth-20260717-11",
        "情緒敏捷的大腦：掌握驅動自我的12種情緒需求",
        "J.D.平卡斯",
        ROOT / "tools" / "_hl_11.txt",
    ),
    (
        "02_psychology_growth-20260717-12",
        "身體知道幸福：發現感恩、幸福與喜悅的意想不到的方式",
        "尼斯·卡普蘭",
        ROOT / "tools" / "_hl_12.txt",
    ),
    (
        "02_psychology_growth-20260717-13",
        "我給自己建了一座心靈補給站",
        "埃瑪·赫伯恩",
        ROOT / "tools" / "_hl_13.txt",
    ),
    (
        "02_psychology_growth-20260717-14",
        "慢慢變成大人",
        "芭芭拉·于貝爾、桑德拉·博西",
        ROOT / "tools" / "_hl_14.txt",
    ),
    (
        "02_psychology_growth-20260717-15",
        "心理學放映廳",
        "楊眉",
        ROOT / "tools" / "_hl_15.txt",
    ),
]


def main() -> int:
    results = []
    failed = []
    for book_id, title, author, path in BOOKS:
        bodies = [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        highlights = [f"{index:03d}、{body}" for index, body in enumerate(bodies, 1)]
        print(f"{book_id} n={len(highlights)}")
        for body in bodies:
            if title in body:
                print(f"  TITLE in: {body}")
            if author in body:
                print(f"  AUTHOR in: {body}")
            if re.search(r"[A-Za-z]", body):
                print(f"  EN: {body}")
        try:
            validate_highlights(book_id, highlights, title, author)
            print("  VALIDATE OK")
        except Exception as exc:
            print(f"  VALIDATE FAIL {exc}")
            failed.append(f"{book_id}: {exc}")
        results.append({"id": book_id, "highlights": highlights})
        single = ROOT / "tools" / f".findbook_results_grok_{book_id}.json"
        single.write_text(json.dumps(results[-1], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"  wrote {single.name}")

    combined = ROOT / "tools" / ".findbook_results_grok_02_psychology_growth-20260717-11-15.json"
    combined.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {combined}")
    if failed:
        print("FAILURES:")
        for item in failed:
            print(item)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
