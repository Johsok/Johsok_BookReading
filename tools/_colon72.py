# -*- coding: utf-8 -*-
import re
import sys
from pathlib import Path

sys.path.insert(0, "tools")
from findbook_writer import validate_highlights
from _assemble_71_75 import load_raw_blocks

NATURAL = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
pat = re.compile(r"^([^：:]{1,12})[：:]")

blocks = load_raw_blocks()
bid = "02_psychology_growth-20260717-72"
title, author = "世界很吵，心很安靜：品讀20杯陶淵明的酒", "費勇"
lines = blocks[bid]
hs = [f"{i:03d}、{b}" for i, b in enumerate(lines, 1)]
out = [f"n={len(lines)}"]
# inspect each highlight the same way as validator
from findbook_writer import NUMBER_RE
short = []
for index, line in enumerate(hs, 1):
    body = NUMBER_RE.sub("", line, count=1).strip()
    match = re.match(r"^([^：:]{1,12})[：:]", body)
    if match:
        out.append(f"MATCH {index:03d} prefix=[{match.group(1)}] endswith={match.group(1).endswith(NATURAL)} body={body[:40]}")
        if not match.group(1).endswith(NATURAL):
            short.append(index)
    if "：" in body or ":" in body:
        pos = max(body.find("："), body.find(":"))
        out.append(f"COLON {index:03d} pos={body.find('：')},{body.find(':')} {body}")
out.append(f"short_colon_count={len(short)} {short[:20]}")
try:
    validate_highlights(bid, hs, title, author)
    out.append("VALIDATE OK")
except ValueError as e:
    out.append("VALIDATE " + str(e))
Path("tools/_colon72.txt").write_text("\n".join(out), encoding="utf-8")
print("done")
