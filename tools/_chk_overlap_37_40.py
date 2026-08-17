# -*- coding: utf-8 -*-
import importlib.util
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")


def load(path):
    spec = importlib.util.spec_from_file_location("m", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.POINTS


a = set(load(Path("tools/_pts_37.py")))
b = set(load(Path("tools/_pts_40.py")))
print("shared", len(a & b))
for x in sorted(a & b):
    print(x)
