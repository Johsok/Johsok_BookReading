# -*- coding: utf-8 -*-
import re
from pathlib import Path

text = Path(__file__).with_name("_build_batch38_txt.py").read_text(encoding="utf-8")
m = re.search(r"H16 = \[(.*?)\]\n\nH17", text, re.S)
lines = re.findall(r'"([^"]+)"', m.group(1))
print("H16", len(lines))
m2 = re.search(r"H17 = \[(.*?)\]\n\n# Continue", text, re.S)
lines2 = re.findall(r'"([^"]+)"', m2.group(1))
print("H17", len(lines2))
