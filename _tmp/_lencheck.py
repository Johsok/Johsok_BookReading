# -*- coding: utf-8 -*-
import json
from pathlib import Path

data = json.loads(Path("_tmp/hl_07_61_63.json").read_text(encoding="utf-8"))


def cjk(s):
    return sum(1 for c in s if "\u4e00" <= c <= "\u9fff")


for book in data["books"]:
    print("====", book["id"])
    nshort = 0
    for h in book["highlights"]:
        body = h.split("、", 1)[1]
        n = cjk(body)
        if n < 28:
            nshort += 1
            print(n, h)
    print("short", nshort)
