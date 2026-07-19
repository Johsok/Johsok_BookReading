# -*- coding: utf-8 -*-
import importlib.util
from pathlib import Path

path = Path(__file__).with_name("_gen_batch59.py")
spec = importlib.util.spec_from_file_location("gen59", path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
for name in ("BOOK26", "BOOK27", "BOOK28", "BOOK29", "BOOK30"):
    lines = getattr(mod, name)
    print(name, len(lines), "unique", len(set(lines)))
