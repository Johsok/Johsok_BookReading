# -*- coding: utf-8 -*-
import json
import re
from collections import Counter
from pathlib import Path

path = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\_tmp\hl_07_61_63.json")
data = json.loads(path.read_text(encoding="utf-8"))
forbidden = re.compile(
    r"本書|作者指出|本章|這一章|第[一二三四五六七八九十百零\d]+章|character|｜|第\d+步|面向"
)
assert path.exists()
assert len(data["books"]) == 3
for book in data["books"]:
    hs = book["highlights"]
    assert len(hs) == 150, book["id"]
    bodies = []
    prefixes = Counter()
    colons = []
    for i, line in enumerate(hs, 1):
        assert line.startswith(f"{i:03d}、"), (book["id"], i, line[:20])
        body = line.split("、", 1)[1]
        cjk = sum(1 for c in body if "\u4e00" <= c <= "\u9fff")
        assert cjk >= 12, (i, cjk, body)
        assert not forbidden.search(line)
        if re.match(r"^.{1,8}：", body):
            colons.append((i, body[:20]))
        bodies.append(body)
        prefixes[body[:18]] += 1
    assert len(set(bodies)) == 150
    bad = [k for k, v in prefixes.items() if v >= 4]
    assert not bad, bad
    assert len(colons) <= 2, colons
    print(book["id"], "OK", "colons", colons)

print("FILE", path, "bytes", path.stat().st_size)
