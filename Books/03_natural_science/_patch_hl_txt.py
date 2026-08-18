# -*- coding: utf-8 -*-
"""Patch chatgptHighlights from a 150-line UTF-8 text file."""
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\Books\03_natural_science")
STAMP = datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S%z")
STAMP = STAMP[:-2] + ":" + STAMP[-2:] if len(STAMP) >= 5 else STAMP
UPDATED = "2026-08-18"
BANNED = ("本書", "作者", "第1版", "閱讀時可先", "整理筆記", "實際運用時可先")


def numbered(items):
    if len(items) != 150:
        raise SystemExit(f"need 150, got {len(items)}")
    seen = set()
    for i, t in enumerate(items, 1):
        n = len(t)
        if n < 22 or n > 54:
            raise SystemExit(f"len {n} #{i}: {t}")
        if t in seen:
            raise SystemExit(f"duplicate #{i}: {t}")
        seen.add(t)
        for b in BANNED:
            if b in t:
                raise SystemExit(f"banned {b} #{i}")
        if any(c.isascii() and c.isalpha() for c in t):
            raise SystemExit(f"ascii #{i}: {t}")
    return [f"{i:03d}、{t}" for i, t in enumerate(items, 1)]


def patch(json_name, txt_name, summary):
    items = [ln.strip() for ln in (ROOT / txt_name).read_text(encoding="utf-8").splitlines() if ln.strip()]
    path = ROOT / json_name
    data = json.loads(path.read_text(encoding="utf-8"))
    data["chatgptHighlights"] = numbered(items)
    data["chatgptStatus"] = "complete"
    data["highlightsSource"] = "grok"
    data["highlightsCapturedAt"] = STAMP
    data["updatedAt"] = UPDATED
    data["summary"] = summary
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)
    print(f"OK {json_name} n={len(data['chatgptHighlights'])}")


if __name__ == "__main__":
    jobs = [
        (
            "03_natural_science-20260716-137.json",
            "_hl_137.txt",
            "整理久保輝幸與羅桂環對宋代牡丹、菊、梅、蘭、菌、荔枝與橘錄等譜錄的觀察、命名與栽培知識。",
        ),
        (
            "03_natural_science-20260716-138.json",
            "_hl_138.txt",
            "整理鳥類與哺乳類恆溫動物的外觀演化：羽毛、喙齒、熱調節、運動器官、性擇與收斂形態。",
        ),
        (
            "03_natural_science-20260716-139.json",
            "_hl_139.txt",
            "整理畢曉普模式識別與機器學習的機率框架：先驗後驗、推論近似、核方法、圖模型與泛化評測。",
        ),
        (
            "03_natural_science-20260716-140.json",
            "_hl_140.txt",
            "整理寒區有機廢棄物厭氧產沼：低溫動力學、保溫換熱、酸抑制、防凍運維與淨能量核算。",
        ),
        (
            "03_natural_science-20260716-141.json",
            "_hl_141.txt",
            "整理節理岩體非線性力學：結構面參數、剪脹殘餘、滲流耦合、塊體可動性與工程應用。",
        ),
    ]
    if len(sys.argv) > 1:
        jobs = [tuple(sys.argv[1:4])]
    for json_name, txt_name, summary in jobs:
        patch(json_name, txt_name, summary)
