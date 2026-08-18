# -*- coding: utf-8 -*-
import json
import re
from pathlib import Path

from hl_54 import HL54
from hl_55 import HL55
from hl_56 import HL56

ROOT = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading")
TS = "2026-08-18T09:10:00+08:00"
DATE = "2026-08-18"
FORBIDDEN = re.compile(r"｜|本書|作者指出|本章|這一章|第[一二三四五六七八九十0-9]+章|[0-9]+面第[0-9]+步")


def validate(items, name):
    assert len(items) == 150, (name, len(items))
    bodies = []
    for i, s in enumerate(items, 1):
        assert s.startswith(f"{i:03d}、"), (name, i, s[:20])
        body = s.split("、", 1)[1]
        assert body, (name, i)
        assert FORBIDDEN.search(s) is None, (name, i, s)
        bodies.append(body)
    assert len(set(items)) == 150, name
    assert len(set(bodies)) == 150, name
    return True


def apply(path, highlights):
    p = Path(path)
    data = json.loads(p.read_text(encoding="utf-8"))
    data["chatgptHighlights"] = highlights
    data["chatgptStatus"] = "complete"
    data["highlightsSource"] = "grok"
    data["highlightsCapturedAt"] = TS
    data["updatedAt"] = DATE
    text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    p.write_text(text, encoding="utf-8")


def main():
    jobs = [
        (ROOT / "Books/06_computer_info/06_computer_info-20260716-54.json", HL54, "54"),
        (ROOT / "Books/06_computer_info/06_computer_info-20260716-55.json", HL55, "55"),
        (ROOT / "Books/06_computer_info/06_computer_info-20260716-56.json", HL56, "56"),
    ]
    for path, hl, name in jobs:
        validate(hl, name)
        apply(path, hl)
        data = json.loads(path.read_text(encoding="utf-8"))
        assert len(data["chatgptHighlights"]) == 150
        assert data["chatgptStatus"] == "complete"
        assert data["highlightsSource"] == "grok"
        assert data["highlightsCapturedAt"] == TS
        assert data["updatedAt"] == DATE
        print(path, "OK", 150)


if __name__ == "__main__":
    main()
