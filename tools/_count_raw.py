# -*- coding: utf-8 -*-
from pathlib import Path
import importlib.util

path = Path(__file__).with_name("_gen_156.py")
spec = importlib.util.spec_from_file_location("gen156", path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
print(len(mod.RAW))
for i, x in enumerate(mod.RAW, 1):
    print(f"{i:03d}\t{x}")
