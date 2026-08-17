# -*- coding: utf-8 -*-
"""Pre-validate highlight counts before writer."""
from __future__ import annotations

import collections
import importlib.util
import re
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "g", Path(__file__).with_name("_gen_pg_20260717_01_05.py")
)
m = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(m)
NATURAL = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
for book in m.BOOKS:
    pts = book["points"]
    print(f"{book['id']} count={len(pts)} unique={len(set(pts))}")
    short = []
    for i, body in enumerate(pts, 1):
        match = re.match(r"^([^：:]{1,12})[：:]", body)
        if match and not match.group(1).endswith(NATURAL):
            short.append((i, match.group(1), body[:24]))
        if len(body) < 12:
            print(" short", i, body)
    if short:
        print(" shortcolon", short)
    starts = collections.Counter(body[:18] for body in pts if len(body) >= 18)
    common = starts.most_common(5)
    if common and common[0][1] >= 3:
        print(" starts", common)
    for label, val in (("title", book["title"]), ("author", book["author"])):
        hits = sum(val in body for body in pts)
        if hits:
            print(f" {label} hits={hits}")
