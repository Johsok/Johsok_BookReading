# -*- coding: utf-8 -*-
import json
from pathlib import Path

p = Path(__file__).with_name(".findbook_results_grok_01_business_startup-20260716-254.json")
d = json.loads(p.read_text(encoding="utf-8-sig"))
line = d["highlights"][108]
Path(__file__).with_name("_fix109.txt").write_text(line, encoding="utf-8")
for pref in ("本書", "作者指出", "本章", "這一章"):
    if pref in line:
        Path(__file__).with_name("_fix109.txt").write_text(line + f"\nHIT:{pref}", encoding="utf-8")
