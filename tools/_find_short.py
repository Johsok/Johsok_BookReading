# -*- coding: utf-8 -*-
import re
from pathlib import Path

text = Path(__file__).with_name("_batch38_bodies.py").read_text(encoding="utf-8")
chunks = {
    "H17": text.split("H17 = [")[1].split("H18 = [")[0],
    "H18": text.split("H18 = [")[1].split("H19 = [")[0],
    "H19": text.split("H19 = [")[1].split("H20 = [")[0],
    "H20": text.split("H20 = [")[1].split("def _check")[0],
}
for name, chunk in chunks.items():
    lines = re.findall(r'"([^"]+)"', chunk)
    for i, ln in enumerate(lines, 1):
        if len(ln) < 12:
            print(name, i, len(ln), ln)
