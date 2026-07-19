# -*- coding: utf-8 -*-
import importlib.util
import re
from pathlib import Path

p = Path(__file__).with_name("_gen_grok_151_to_154.py")
spec = importlib.util.spec_from_file_location("gen151", p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
suf = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
for book_id, title, author, bodies in mod.BOOKS:
    bad = []
    for i, b in enumerate(bodies, 1):
        match = re.match(r"^([^：:]{1,12})[：:]", b)
        if match and not match.group(1).endswith(suf):
            bad.append((i, match.group(1), b))
    print(book_id, "short_colon", len(bad))
    for item in bad:
        print(" ", item[0], item[1], "=>", item[2][:50])
