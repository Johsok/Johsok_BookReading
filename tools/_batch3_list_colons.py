# -*- coding: utf-8 -*-
import importlib.util
import re
from pathlib import Path

NATURAL = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")


def load(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.LINES


for key, path in [
    ("38", "tools/_batch3_book38.py"),
    ("39", "tools/_batch3_book39.py"),
    ("40", "tools/_batch3_book40.py"),
]:
    rows = []
    for i, body in enumerate(load(Path(path)), 1):
        match = re.match(r"^([^：:]{1,12})[：:]", body)
        if match and not match.group(1).endswith(NATURAL):
            rows.append(f"{i:03d}|{match.group(1)}|{body}")
    Path(f"tools/_batch3_colon{key}.txt").write_text("\n".join(rows), encoding="utf-8")
    print(key, len(rows))
