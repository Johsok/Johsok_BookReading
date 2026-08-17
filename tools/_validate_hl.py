# -*- coding: utf-8 -*-
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from findbook_writer import validate_highlights

path = Path(sys.argv[1])
title = sys.argv[2]
author = sys.argv[3]
data = json.loads(path.read_text(encoding="utf-8"))
validate_highlights(data["id"], data["highlights"], title, author)
bodies = [line.split("、", 1)[1] for line in data["highlights"]]
lens = [len(body) for body in bodies]
print("ok", len(bodies), "min", min(lens), "max", max(lens), "lt35", sum(l < 35 for l in lens))
print("author_hits", sum(author in body for body in bodies), "title_hits", sum(title in body for body in bodies))
nat = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
for i, body in enumerate(bodies, 1):
    match = re.match(r"^([^：:]{1,12})[：:]", body)
    if match and not match.group(1).endswith(nat):
        print("colon", i, match.group(1))
starts = Counter(body[:18] for body in bodies)
print("top_starts", starts.most_common(3))
