# -*- coding: utf-8 -*-
import importlib.util
from pathlib import Path

p = Path(__file__).with_name("_gen_chunk02_highlights.py")
spec = importlib.util.spec_from_file_location("gen", p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
for name in ["BOOK66", "BOOK67", "BOOK68", "BOOK69", "BOOK70"]:
    if hasattr(mod, name):
        print(name, len(getattr(mod, name)))
    else:
        print(name, "missing")
