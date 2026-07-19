# -*- coding: utf-8 -*-
import json
import re
from pathlib import Path

NATURAL_COLON_SUFFIXES = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
path = Path(__file__).with_name(".findbook_results_grok_01_business_startup-20260716-253.json")
data = json.loads(path.read_text(encoding="utf-8-sig"))
out = []
for i, line in enumerate(data["highlights"], 1):
    body = re.sub(r"^\d{3}、", "", line).strip()
    m = re.match(r"^([^：:]{1,12})[：:]", body)
    if m and not m.group(1).endswith(NATURAL_COLON_SUFFIXES):
        out.append(f"{i}\t{body}")
Path(__file__).with_name("_check_253_out.txt").write_text("\n".join(out), encoding="utf-8")
print("found", len(out))
