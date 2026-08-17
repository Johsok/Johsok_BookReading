# -*- coding: utf-8 -*-
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _gen_pg_141_145 import BOOKS
from findbook_writer import NATURAL_COLON_SUFFIXES

for book in BOOKS:
    print("====", book["id"], len(book["bodies"]))
    short = []
    for i, body in enumerate(book["bodies"], 1):
        match = re.match(r"^([^：:]{1,12})[：:]", body)
        if match and not match.group(1).endswith(NATURAL_COLON_SUFFIXES):
            short.append((i, match.group(1), body[:40]))
    if short:
        print(" short-colon", len(short))
        for row in short:
            print(" ", row)
    starts = {}
    for body in book["bodies"]:
        if len(body) >= 18:
            k = body[:18]
            starts[k] = starts.get(k, 0) + 1
    bad = [(k, n) for k, n in starts.items() if n >= 4]
    if bad:
        print(" repeated starts", bad)
    dups = [b for b in book["bodies"] if book["bodies"].count(b) > 1]
    if dups:
        print(" dups", set(dups))
    for label, value in (("title", book["title"]), ("author", book["author"])):
        n = sum(value in b for b in book["bodies"])
        if n:
            print(f" {label} hits {n}")
    forbidden = ("本書", "作者指出", "本章", "這一章")
    for i, b in enumerate(book["bodies"], 1):
        if any(p in b for p in forbidden):
            print(" forbidden", i, b[:40])
        if "｜" in b or "\n" in b:
            print(" format", i)
        if len(b) < 12:
            print(" short", i, b)
