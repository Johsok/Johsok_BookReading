# -*- coding: utf-8 -*-
from pathlib import Path
from importlib.machinery import SourceFileLoader

for name, attr in [
    ("_batch46_b47.py", "BOOK47"),
    ("_batch46_b48.py", "BOOK48"),
    ("_batch46_b49.py", "BOOK49"),
    ("_batch46_b50.py", "BOOK50"),
]:
    mod = SourceFileLoader(attr, f"tools/{name}").load_module()
    bodies = getattr(mod, attr)
    print(attr, len(bodies), len(set(bodies)))
