# -*- coding: utf-8 -*-
from pathlib import Path
import importlib.util
import ast

ROOT = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\Books\03_natural_science")


def load(name, attr):
    spec = importlib.util.spec_from_file_location(name, ROOT / name)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, attr)


src = (ROOT / "_tmp_ns_hl_writer.py").read_text(encoding="utf-8")
i = src.find('"items": [')
j = src.find("\n    ],", i)
text = src[i + len('"items": ') : j + len("\n    ]")]
items21 = ast.literal_eval(text)
print("21", len(items21))
for f, a in [
    ("_tmp_ns_22.py", "ITEMS_22"),
    ("_tmp_ns_23.py", "ITEMS_23"),
    ("_tmp_ns_24.py", "ITEMS_24"),
    ("_tmp_ns_25.py", "ITEMS_25"),
    ("_tmp_ns_26.py", "ITEMS_26"),
    ("_tmp_ns_27.py", "ITEMS_27"),
    ("_tmp_ns_28.py", "ITEMS_28"),
    ("_tmp_ns_29.py", "ITEMS_29"),
    ("_tmp_ns_30.py", "ITEMS_30"),
]:
    print(f, len(load(f, a)))
