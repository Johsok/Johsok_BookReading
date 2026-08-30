# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from findbook_writer import validate_highlights
from _gen_batchA_schwartz import BODIES as SCHWARTZ
from _gen_batchA_keller import BODIES as KELLER
from _gen_batchA_matsuo import BODIES as MATSUO

BOOKS = [
    {
        "id": "01_business_startup-20260830-04",
        "title": "這樣WORK才WORK！：識破多工的效率迷思，擺脫超時賣命的職場陷阱",
        "author": "東尼．史瓦茲",
        "bodies": SCHWARTZ,
    },
    {
        "id": "01_business_startup-20260830-05",
        "title": "成功，從聚焦一件事開始：不流失專注力的減法原則(暢銷改版)",
        "author": "蓋瑞．凱勒",
        "bodies": KELLER,
    },
    {
        "id": "01_business_startup-20260830-12",
        "title": "1分鐘高效工作術：6種一分鐘思維與71項實戰心法，讓你工作提速、業績超標、下班準時！",
        "author": "松尾昭仁",
        "bodies": MATSUO,
    },
]


def diagnose(book_id: str, bodies: list[str], title: str, author: str) -> None:
    print(f"== {book_id} raw={len(bodies)}")
    if len(bodies) != 150:
        print(f"  COUNT {len(bodies)}")
    forbidden = ("本書", "作者指出", "本章", "這一章")
    for i, body in enumerate(bodies, 1):
        if any(p in body for p in forbidden):
            print(f"  FORBIDDEN {i}: {body}")
        if "｜" in body or "\n" in body:
            print(f"  FORMAT {i}: {body}")
        if title and title in body:
            print(f"  TITLE {i}")
        if author and author in body:
            print(f"  AUTHOR {i}")
        if re.search(r"[A-Za-z]{4,}", body):
            print(f"  EN {i}: {body}")
        if len(body) < 12:
            print(f"  SHORT {i}: {body}")
        m = re.match(r"^([^：:]{1,12})[：:]", body)
        if m and not m.group(1).endswith(("是", "為", "在於", "說", "問", "提醒", "表示", "指出")):
            print(f"  COLON {i}: {m.group(1)} | {body[:40]}")
    if len(set(bodies)) != len(bodies):
        c = Counter(bodies)
        for body, n in c.items():
            if n > 1:
                print(f"  DUP x{n}: {body[:40]}")
    starts = Counter(b[:18] for b in bodies if len(b) >= 18)
    for start, n in starts.most_common(5):
        if n >= 2:
            print(f"  START x{n}: {start}")


def main() -> None:
    results = []
    failed = []
    for book in BOOKS:
        bodies = list(book["bodies"])[:150]
        diagnose(book["id"], bodies, book["title"], book["author"])
        highlights = [f"{i:03d}、{body}" for i, body in enumerate(bodies, 1)]
        try:
            validate_highlights(book["id"], highlights, book["title"], book["author"])
            print("  VALIDATE OK")
        except Exception as exc:
            failed.append(str(exc))
            print(f"  VALIDATE FAIL: {exc}")
        results.append({"id": book["id"], "highlights": highlights})

    out = Path(__file__).resolve().parent / ".findbook_results_20260830_batchA.json"
    out.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote", out)
    if failed:
        raise SystemExit("\n".join(failed))


if __name__ == "__main__":
    log = Path(__file__).resolve().parent / "_tmp_batchA_val.txt"
    from io import StringIO
    buf = StringIO()
    old = sys.stdout
    sys.stdout = buf
    code = 0
    try:
        main()
    except SystemExit as exc:
        code = 1
        print(exc)
    finally:
        sys.stdout = old
    log.write_text(buf.getvalue(), encoding="utf-8")
    print(buf.getvalue())
    raise SystemExit(code)
